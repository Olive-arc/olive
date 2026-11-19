#!/usr/bin/env python3
"""SEO and AIO gate for the Olive blog.

Fails when a page would ship thin, duplicate, unsourced or schema-less.
Run after build-blog.py.

    python3 scripts/check-seo.py
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import content_lib as lib  # noqa: E402

MIN_WORDS = {
    "guide": 900,
    "pillar": 1400,
    "explainer": 700,
    "glossary": 250,
    "comparison": 600,
    "task": 500,
}

MONEY_CLUSTERS = {
    "migration",
    "clover",
    "lucent",
    "connected",
    "agentic",
    "quantitative",
    "portfolio",
    "olive",
}

errors: list[str] = []
warnings: list[str] = []


def fail(slug: str, message: str) -> None:
    errors.append(f"{slug}: {message}")


def warn(slug: str, message: str) -> None:
    warnings.append(f"{slug}: {message}")


def first_words(text: str, n: int) -> str:
    plain = re.sub(r"[#>*_|`\[\]()]", " ", text)
    return " ".join(plain.split()[:n]).lower()


def avg_sentence_length(text: str) -> float:
    plain = re.sub(r"[#>*_|`\[\]()]", " ", text)
    sentences = [s for s in re.split(r"[.!?]+", plain) if len(s.split()) > 2]
    if not sentences:
        return 0.0
    return sum(len(s.split()) for s in sentences) / len(sentences)


def check_article(article: lib.Article) -> None:
    slug = article.slug
    if article.path.stem != slug:
        fail(slug, f"slug does not match filename {article.path.name}")

    for key in ("title", "description", "cluster", "type", "target_query", "answer", "published"):
        if not getattr(article, key):
            fail(slug, f"missing frontmatter field {key}")

    if not 45 <= len(article.title) <= 65:
        fail(slug, f"title is {len(article.title)} chars, needs 45 to 65")
    if not 140 <= len(article.description) <= 158:
        fail(slug, f"description is {len(article.description)} chars, needs 140 to 158")

    answer_words = len(article.answer.split())
    if not 35 <= answer_words <= 70:
        fail(slug, f"answer is {answer_words} words, needs 35 to 70")

    minimum = MIN_WORDS.get(article.type, 700)
    if article.word_count < minimum:
        fail(slug, f"{article.type} has {article.word_count} words, needs {minimum}")

    if len(article.internal_links) < 3:
        fail(slug, f"{len(article.internal_links)} internal links, needs 3")
    if len(article.sources) < 2:
        fail(slug, f"{len(article.sources)} sources, needs 2")
    if not 3 <= len(article.faqs) <= 5:
        fail(slug, f"{len(article.faqs)} FAQs, needs 3 to 5")

    query = article.target_query.lower()
    if query not in article.title.lower():
        fail(slug, "target query missing from title")
    if query not in article.body_md.lower() and query not in article.answer.lower():
        fail(slug, "target query missing from body")
    if query not in first_words(article.body_md, 120):
        warn(slug, "target query not in the first 120 body words")

    haystack = (article.body_md + " " + article.answer).lower()
    for phrase in lib.BANNED:
        if phrase in haystack:
            fail(slug, f"banned claim phrase: {phrase}")
    for phrase in lib.FORBIDDEN:
        if phrase in haystack:
            fail(slug, f"forbidden internal term: {phrase}")

    if article.cluster in MONEY_CLUSTERS and article.disclaimer != "financial":
        fail(slug, "money cluster needs disclaimer: financial")

    if article.cluster == "migration" and not re.search(
        r"(status checked|as of \d|no deadline is set)", article.body_md, re.I
    ):
        fail(slug, "migration page needs a dated status line")
    if "scam" in slug and "t.me/olive_eng" not in article.body_md:
        fail(slug, "scam page must name the official Telegram")

    if "\u2014" in article.body_md or "\u2014" in article.answer:
        fail(slug, "em dash found, use a period")

    sentences = avg_sentence_length(article.body_md)
    if sentences > 28:
        warn(slug, f"average sentence is {sentences:.0f} words, trim it")

    if not article.sources or not all(s.startswith("http") for s in article.sources):
        fail(slug, "sources must be absolute https URLs")

    for target in article.internal_links:
        path = target.lstrip("/")
        if path.startswith("blog/"):
            candidate = lib.BLOG / path[len("blog/"):] / "index.html"
            if not candidate.exists():
                fail(slug, f"internal link target missing: {target}")
        else:
            candidate = lib.ROOT / path / "index.html" if not path.endswith("/index.html") else lib.ROOT / path
            if not candidate.exists() and not (lib.ROOT / path).exists():
                fail(slug, f"internal link target missing: {target}")

    generated = lib.BLOG / slug / "index.html"
    if not generated.exists():
        fail(slug, "generated page missing, run build-blog.py")
        return
    page = generated.read_text(encoding="utf-8")
    for marker, label in [
        (f'<link rel="canonical" href="{article.canonical}">', "canonical"),
        ('"@type": "Article"', "Article schema"),
        ('"@type": "BreadcrumbList"', "Breadcrumb schema"),
        ('"@type": "FAQPage"', "FAQ schema"),
        (f'<meta property="og:url" content="{article.canonical}">', "og:url"),
        ('<meta name="twitter:card" content="summary_large_image">', "twitter card"),
        ("assets/css/blog.css", "blog stylesheet"),
    ]:
        if marker not in page:
            fail(slug, f"generated page missing {label}")

    if re.search(r"<h1[^>]*>.*?</h1>.*<h1", page, re.S):
        fail(slug, "more than one h1")


def check_duplicates(articles: list[lib.Article]) -> None:
    for field in ("title", "description", "target_query", "slug"):
        counts = Counter(getattr(a, field).lower() for a in articles)
        for value, count in counts.items():
            if value and count > 1:
                errors.append(f"duplicate {field}: {value!r} appears {count} times")


def check_site(articles: list[lib.Article]) -> None:
    sitemap = lib.ROOT / "sitemap.xml"
    robots = lib.ROOT / "robots.txt"
    llms = lib.ROOT / "llms.txt"
    for path in (sitemap, robots, llms):
        if not path.exists():
            errors.append(f"missing {path.name}, run build-blog.py")
    if sitemap.exists():
        text = sitemap.read_text(encoding="utf-8")
        for article in articles:
            if article.canonical not in text:
                errors.append(f"sitemap missing {article.canonical}")
    if robots.exists() and "Sitemap:" not in robots.read_text(encoding="utf-8"):
        errors.append("robots.txt has no Sitemap line")

    for page in lib.STATIC_PAGES:
        path = lib.ROOT / page / "index.html" if page else lib.ROOT / "index.html"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if "seo:auto" not in text:
            warn(page or "home", "static page not patched, run patch-seo.py")


def main() -> int:
    articles = lib.load_articles()
    if not articles:
        print("no articles found")
        return 1
    for article in articles:
        check_article(article)
    check_duplicates(articles)
    check_site(articles)

    for line in warnings:
        print(f"warn  {line}")
    for line in errors:
        print(f"FAIL  {line}")
    print(f"\n{len(articles)} articles, {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
