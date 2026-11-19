"""Shared parsing and rendering for the Olive blog.

One source of truth for frontmatter, markdown, FAQ extraction and word counts.
build-blog.py writes files. check-seo.py validates them.
"""

from __future__ import annotations

import html
import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content" / "blog"
BLOG = ROOT / "blog"
SITE_URL = "https://olivefinance.org"
SITE_NAME = "Olive"

STATIC_PAGES = [
    "",
    "features/connected-defi/",
    "features/quantitative-investments/",
    "features/agentic-trading/",
    "features/asset-portfolio-management/",
    "docs/roadmap/",
]

DISAMBIGUATION = (
    "Olive is the successor to Clover Finance and Lucent Network, adopted by a new team. "
    "It is not affiliated with oliveapp.finance, Olive Capital, or Olive Foundation Nepal."
)

DISCLAIMER = (
    "This article is general information about how Olive works. It is not financial "
    "advice, an offer, or a promise of returns. Digital assets carry risk, including "
    "total loss. Check the current terms in the app before you act."
)

BANNED = [
    "guaranteed return",
    "risk-free",
    "risk free",
    "cannot lose",
    "guaranteed profit",
    "passive income guaranteed",
    "always profitable",
    "no risk",
    "double your",
    "get rich",
]

# Backend, custody and internal material. These must never reach a public page.
FORBIDDEN = [
    "omnibus",
    "custody",
    "self-custody",
    "ledger",
    "account balance",
    "private key",
    "admin review",
    "review queue",
    "under review",
    "ratio snapshot",
    "request status",
    "database",
    "schema",
    "drizzle",
    "postgres",
    "sepolia",
    "testnet",
    "$50 million",
    "50m round",
]


@dataclass
class Article:
    path: Path
    slug: str
    title: str
    description: str
    cluster: str
    type: str
    target_query: str
    answer: str
    published: str
    updated: str
    internal_links: list[str] = field(default_factory=list)
    sources: list[str] = field(default_factory=list)
    disclaimer: str = ""
    author: str = "Olive Team"
    body: str = ""
    faqs: list[tuple[str, str]] = field(default_factory=list)
    body_md: str = ""
    errors: list[str] = field(default_factory=list)

    @property
    def url_path(self) -> str:
        return f"blog/{self.slug}/"

    @property
    def canonical(self) -> str:
        return f"{SITE_URL}/{self.url_path}"

    @property
    def word_count(self) -> int:
        faq_text = " ".join(f"{q} {re.sub(r'<[^>]+>', ' ', a)}" for q, a in self.faqs)
        return count_words(self.body_md + "\n" + faq_text)


def count_words(text: str) -> int:
    plain = re.sub(r"```.*?```", " ", text, flags=re.S)
    plain = re.sub(r"`[^`]*`", " ", plain)
    plain = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", plain)
    plain = re.sub(r"[#>*_|\-]", " ", plain)
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-]*", plain))


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        raise ValueError("missing frontmatter")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError("unterminated frontmatter")
    raw, body = parts[1], parts[2]
    data: dict = {}
    key = None
    for line in raw.splitlines():
        if not line.strip():
            continue
        if re.match(r"^\s+-\s+", line) and key:
            data.setdefault(key, []).append(_scalar(line.strip()[2:]))
            continue
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()
        if value == "":
            data[key] = []
        elif value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = [_scalar(v) for v in inner.split(",")] if inner else []
        else:
            data[key] = _scalar(value)
    return data, body.lstrip("\n")


def _scalar(value: str):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def render_inline(text: str) -> str:
    escaped = html.escape(text, quote=False)
    tokens: list[str] = []

    def stash(match: re.Match) -> str:
        tokens.append(html.escape(match.group(1), quote=False))
        return f"\x00{len(tokens) - 1}\x00"

    escaped = re.sub(r"`([^`]+)`", stash, escaped)
    escaped = re.sub(
        r"\[([^\]]+)\]\(([^)\s]+)\)",
        lambda m: f'<a href="{html.escape(m.group(2), quote=True)}">{m.group(1)}</a>',
        escaped,
    )
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", escaped)
    for index, token in enumerate(tokens):
        escaped = escaped.replace(f"\x00{index}\x00", f"<code>{token}</code>")
    return autolink(escaped)


def autolink(text: str) -> str:
    """Link bare http(s) URLs in text nodes, never inside an existing anchor."""
    parts = re.split(r"(<[^>]+>)", text)
    out: list[str] = []
    in_anchor = False
    for part in parts:
        if part.startswith("<"):
            if re.match(r"<a\b", part, re.I):
                in_anchor = True
            elif re.match(r"</a>", part, re.I):
                in_anchor = False
            out.append(part)
        elif in_anchor:
            out.append(part)
        else:
            out.append(re.sub(r"https?://[^\s<]+", lambda m: f'<a href="{m.group(0)}">{m.group(0)}</a>', part))
    return "".join(out)


def render_markdown(md: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            lang = line.strip("`").strip()
            code: list[str] = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1
            cls = f' class="language-{html.escape(lang)}"' if lang else ""
            out.append(f"<pre><code{cls}>{html.escape(chr(10).join(code))}</code></pre>")
            continue
        if not line.strip():
            i += 1
            continue
        heading = re.match(r"^(#{2,4})\s+(.*)$", line)
        if heading:
            level = len(heading.group(1))
            out.append(f"<h{level}>{render_inline(heading.group(2).strip())}</h{level}>")
            i += 1
            continue
        if re.match(r"^---+$", line.strip()):
            out.append("<hr>")
            i += 1
            continue
        if line.lstrip().startswith(">"):
            quote: list[str] = []
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                quote.append(lines[i].lstrip()[1:].strip())
                i += 1
            out.append(f"<blockquote><p>{render_inline(' '.join(quote))}</p></blockquote>")
            continue
        if line.strip().startswith("|") and i + 1 < len(lines) and re.match(
            r"^\|[\s:|-]+\|$", lines[i + 1].strip()
        ):
            header = _cells(line)
            i += 2
            rows: list[list[str]] = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(_cells(lines[i]))
                i += 1
            thead = "".join(f"<th>{render_inline(c)}</th>" for c in header)
            tbody = "".join(
                "<tr>" + "".join(f"<td>{render_inline(c)}</td>" for c in row) + "</tr>"
                for row in rows
            )
            out.append(f"<div class=\"table-wrap\"><table><thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody></table></div>")
            continue
        if re.match(r"^[-*]\s+", line):
            items = []
            while i < len(lines) and re.match(r"^[-*]\s+", lines[i]):
                raw = re.sub(r"^[-*]\s+", "", lines[i])
                task = re.match(r"^\[([ xX])\]\s+(.*)$", raw)
                if task:
                    done = task.group(1).lower() == "x"
                    cls = "task task--done" if done else "task"
                    items.append(f'<li class="{cls}"><span class="task-box" aria-hidden="true"></span>{render_inline(task.group(2))}</li>')
                else:
                    items.append(f"<li>{render_inline(raw)}</li>")
                i += 1
            out.append("<ul>" + "".join(items) + "</ul>")
            continue
        if re.match(r"^\d+\.\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i]):
                items.append(re.sub(r"^\d+\.\s+", "", lines[i]))
                i += 1
            out.append("<ol>" + "".join(f"<li>{render_inline(x)}</li>" for x in items) + "</ol>")
            continue
        para: list[str] = []
        while i < len(lines) and lines[i].strip() and not _starts_block(lines[i]):
            para.append(lines[i].strip())
            i += 1
        out.append(f"<p>{render_inline(' '.join(para))}</p>")
    return "\n".join(out)


def _starts_block(line: str) -> bool:
    return bool(
        line.startswith("```")
        or re.match(r"^(#{2,4})\s+", line)
        or re.match(r"^[-*]\s+", line)
        or re.match(r"^\d+\.\s+", line)
        or line.lstrip().startswith(">")
        or line.strip().startswith("|")
        or re.match(r"^---+$", line.strip())
    )


def _cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def split_faq(md: str) -> tuple[str, list[tuple[str, str]]]:
    lines = md.splitlines()
    start = None
    for index, line in enumerate(lines):
        if re.match(r"^##\s+.*(faq|frequently asked)", line, re.I):
            start = index
            break
    if start is None:
        return md, []
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if re.match(r"^##\s+", lines[index]):
            end = index
            break
    faqs: list[tuple[str, str]] = []
    current_q = None
    answer: list[str] = []
    for line in lines[start + 1 : end]:
        q = re.match(r"^###\s+(.*)$", line)
        if q:
            if current_q:
                faqs.append((current_q, _faq_answer(answer)))
            current_q = q.group(1).strip()
            answer = []
        elif current_q is not None:
            answer.append(line)
    if current_q:
        faqs.append((current_q, _faq_answer(answer)))
    remaining = "\n".join(lines[:start] + lines[end:])
    return remaining, faqs


def _faq_answer(lines: list[str]) -> str:
    text = " ".join(line.strip() for line in lines if line.strip())
    return render_inline(text)


def load_article(path: Path) -> Article:
    data, body = parse_frontmatter(path.read_text(encoding="utf-8"))
    body_md, faqs = split_faq(body)
    article = Article(
        path=path,
        slug=data.get("slug") or path.stem,
        title=data.get("title", ""),
        description=data.get("description", ""),
        cluster=data.get("cluster", ""),
        type=data.get("type", "guide"),
        target_query=data.get("target_query", ""),
        answer=data.get("answer", ""),
        published=data.get("published", ""),
        updated=data.get("updated", ""),
        internal_links=data.get("internal_links", []),
        sources=data.get("sources", []),
        disclaimer=data.get("disclaimer", ""),
        author=data.get("author", "Olive Team"),
        body=render_markdown(body_md),
        faqs=faqs,
        body_md=body_md,
    )
    if isinstance(article.internal_links, str):
        article.internal_links = [article.internal_links]
    if isinstance(article.sources, str):
        article.sources = [article.sources]
    return article


def load_articles(content_dir: Path = CONTENT) -> list[Article]:
    if not content_dir.exists():
        return []
    articles = [load_article(p) for p in sorted(content_dir.glob("*.md"))]
    return sorted(articles, key=lambda a: (a.published, a.slug), reverse=True)


def iso(data: str) -> str:
    try:
        return date.fromisoformat(data).isoformat()
    except Exception:
        return date.today().isoformat()


def json_ld(article: Article) -> str:
    import json

    graph = [
        {
            "@type": "Article",
            "headline": article.title,
            "description": article.description,
            "datePublished": iso(article.published),
            "dateModified": iso(article.updated or article.published),
            "author": {"@type": "Organization", "name": article.author, "url": SITE_URL},
            "publisher": {
                "@type": "Organization",
                "name": SITE_NAME,
                "url": SITE_URL,
                "logo": {"@type": "ImageObject", "url": f"{SITE_URL}/assets/img/favicon-32.png"},
            },
            "mainEntityOfPage": {"@type": "WebPage", "@id": article.canonical},
            "image": f"{SITE_URL}/assets/img/og.png",
            "articleSection": article.cluster,
            "wordCount": article.word_count,
            "inLanguage": "en",
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE_URL}/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{SITE_URL}/blog/"},
                {"@type": "ListItem", "position": 3, "name": article.title, "item": article.canonical},
            ],
        },
    ]
    if article.faqs:
        graph.append(
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)},
                    }
                    for q, a in article.faqs
                ],
            }
        )
    payload = {"@context": "https://schema.org", "@graph": graph}
    return json.dumps(payload, ensure_ascii=False, indent=2)
