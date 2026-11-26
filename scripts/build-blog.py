#!/usr/bin/env python3
"""Build the Olive blog, sitemap, robots.txt, llms.txt and RSS feed.

The nav and footer are extracted from docs/roadmap/index.html so there is one source
of truth for the site shell. Run from anywhere:

    python3 scripts/build-blog.py
"""

from __future__ import annotations

import html
import re
import sys
from datetime import date
from email.utils import format_datetime
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import content_lib as lib  # noqa: E402

SHELL_SOURCE = lib.ROOT / "docs" / "roadmap" / "index.html"
CLUSTER_ORDER = [
    "migration",
    "clover",
    "lucent",
    "connected",
    "agentic",
    "quantitative",
    "portfolio",
    "olive",
    "entity",
    "glossary",
]


def shell_parts() -> tuple[str, str, str]:
    src = SHELL_SOURCE.read_text(encoding="utf-8")
    defs = re.search(r'<svg width="0" height="0".*?</svg>', src, re.S)
    header = re.search(r'<a class="skip-link".*?</header>', src, re.S)
    footer = re.search(r"<footer.*?</footer>", src, re.S)
    if not (defs and header and footer):
        raise SystemExit("could not extract shell from docs/roadmap/index.html")
    return defs.group(0), header.group(0), footer.group(0)


def head(article: lib.Article) -> str:
    title = html.escape(article.title)
    desc = html.escape(article.description, quote=True)
    url = article.canonical
    image = f"{lib.SITE_URL}/assets/img/og.png"
    ld = lib.json_ld(article).replace("</", "<\\/")
    return f"""  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
  <meta property="og:site_name" content="{lib.SITE_NAME}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{image}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{html.escape(lib.SITE_NAME)}">
  <meta property="og:locale" content="en_GB">
  <meta property="article:published_time" content="{lib.iso(article.published)}">
  <meta property="article:modified_time" content="{lib.iso(article.updated or article.published)}">
  <meta property="article:section" content="{html.escape(article.cluster)}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{image}">
  <meta name="theme-color" content="#050604">
  <link rel="icon" href="../../assets/img/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="../../assets/img/favicon-32.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="../../assets/img/apple-touch-icon.png">
  <link rel="stylesheet" href="../../assets/css/main.css">
  <link rel="stylesheet" href="../../assets/css/landing.css">
  <link rel="stylesheet" href="../../assets/css/features.css">
  <link rel="stylesheet" href="../../assets/css/blog.css">
  <link rel="alternate" type="application/rss+xml" title="Olive blog" href="{lib.SITE_URL}/feed.xml">
  <script>document.documentElement.classList.add('js');</script>
  <script type="application/ld+json">
{ld}
  </script>"""


def faq_block(article: lib.Article) -> str:
    if not article.faqs:
        return ""
    items = "\n".join(
        f"        <details class=\"faq-item\"><summary>{q}</summary><div class=\"faq-answer\"><p>{a}</p></div></details>"
        for q, a in article.faqs
    )
    return f"""
      <section class="blog-faq" aria-labelledby="faq">
        <h2 id="faq">Frequently asked questions</h2>
        <div class="faq-list">
{items}
        </div>
      </section>"""


def related_block(article: lib.Article, articles: list[lib.Article]) -> str:
    links = []
    by_path = {a.url_path: a for a in articles}
    for target in article.internal_links:
        path = target.lstrip("/")
        match = by_path.get(path)
        if match:
            links.append(f'<li><a href="/{match.url_path}">{html.escape(match.title)}</a></li>')
        else:
            label = path.rstrip("/").split("/")[-1].replace("-", " ").title()
            links.append(f'<li><a href="{html.escape(target)}">{html.escape(label)}</a></li>')
    if not links:
        return ""
    return f"""
      <section class="blog-related">
        <h2>Keep reading</h2>
        <ul class="blog-related-list">
{chr(10).join('          ' + x for x in links)}
        </ul>
      </section>"""


def sources_block(article: lib.Article) -> str:
    if not article.sources:
        return ""
    items = "\n".join(
        f'          <li><a href="{html.escape(s)}" rel="noopener noreferrer">{html.escape(s)}</a></li>'
        for s in article.sources
    )
    return f"""
      <section class="blog-sources">
        <h2>Sources</h2>
        <ul>
{items}
        </ul>
      </section>"""


def disclaimer_block(article: lib.Article) -> str:
    if not article.disclaimer:
        return ""
    return f'      <p class="blog-disclaimer">{lib.DISCLAIMER}</p>'


def render_post(article: lib.Article, articles: list[lib.Article], defs: str, header: str, footer: str) -> str:
    published = lib.iso(article.published)
    updated = lib.iso(article.updated or article.published)
    return f"""<!doctype html>
<html lang="en">
<head>
{head(article)}
</head>
<body data-theme="black">

{defs}

{header}

<main id="top" class="blog-post">
  <div class="container blog-post__inner">
    <nav class="blog-crumbs mono" aria-label="Breadcrumb">
      <a href="../../">Home</a><span>/</span><a href="../../blog/">Blog</a><span>/</span><span aria-current="page">{html.escape(article.title)}</span>
    </nav>
    <article>
      <header class="blog-head">
        <p class="mono blog-kicker">{html.escape(article.cluster)} / {html.escape(article.type)}</p>
        <h1>{html.escape(article.title)}</h1>
        <p class="blog-meta mono">Published {published} &middot; Updated {updated} &middot; {article.word_count} words</p>
      </header>
      <div class="blog-answer"><p>{lib.render_inline(article.answer)}</p></div>
      <div class="prose">
{article.body}
      </div>
{faq_block(article)}
{related_block(article, articles)}
{sources_block(article)}
{disclaimer_block(article)}
    </article>
  </div>
</main>

{footer}
<script src="../../assets/js/landing.js"></script>
</body>
</html>
"""


def render_index(articles: list[lib.Article], defs: str, header: str, footer: str) -> str:
    header = header.replace("../../", "../")
    footer = footer.replace("../../", "../")
    groups: dict[str, list[lib.Article]] = {}
    for article in articles:
        groups.setdefault(article.cluster, []).append(article)

    def order(cluster: str) -> int:
        return CLUSTER_ORDER.index(cluster) if cluster in CLUSTER_ORDER else 99

    labels = {"migration": "Bridge & swap"}

    sections = []
    for cluster in sorted(groups, key=order):
        cards = "\n".join(
            f"""        <li class="post-card">
          <a href="{a.slug}/">
            <span class="mono post-card__meta">{lib.iso(a.published)} &middot; {a.word_count} words</span>
            <span class="post-card__title">{html.escape(a.title)}</span>
            <span class="post-card__desc">{html.escape(a.description)}</span>
          </a>
        </li>"""
            for a in sorted(groups[cluster], key=lambda x: x.published, reverse=True)
        )
        label = labels.get(cluster, cluster.replace("-", " ").title())
        sections.append(
            f"""      <section class="blog-group">
        <h2>{html.escape(label)}</h2>
        <ul class="post-list">
{cards}
        </ul>
      </section>"""
        )

    ld = {
        "@context": "https://schema.org",
        "@type": "Blog",
        "name": "Olive blog",
        "url": f"{lib.SITE_URL}/blog/",
        "description": "Guides and explainers on the Olive platform, connected DeFi, agentic trading, and the CLV and LUX bridge model.",
        "publisher": {"@type": "Organization", "name": lib.SITE_NAME, "url": lib.SITE_URL},
    }
    import json

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Olive blog: guides and explainers</title>
  <meta name="description" content="Guides and explainers on the Olive platform, connected DeFi, agentic trading, quantitative investing, and the CLV and LUX bridge model.">
  <link rel="canonical" href="{lib.SITE_URL}/blog/">
  <meta property="og:site_name" content="{lib.SITE_NAME}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="Olive blog: guides and explainers">
  <meta property="og:description" content="Guides and explainers on the Olive platform, connected DeFi, agentic trading, quantitative investing, and the CLV and LUX bridge model.">
  <meta property="og:url" content="{lib.SITE_URL}/blog/">
  <meta property="og:image" content="{lib.SITE_URL}/assets/img/og.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#050604">
  <link rel="icon" href="../assets/img/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="../assets/img/favicon-32.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="../assets/img/apple-touch-icon.png">
  <link rel="stylesheet" href="../assets/css/main.css">
  <link rel="stylesheet" href="../assets/css/landing.css">
  <link rel="stylesheet" href="../assets/css/features.css">
  <link rel="stylesheet" href="../assets/css/blog.css">
  <link rel="alternate" type="application/rss+xml" title="Olive blog" href="{lib.SITE_URL}/feed.xml">
  <script>document.documentElement.classList.add('js');</script>
  <script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
  </script>
</head>
<body data-theme="black">

{defs}

{header}

<main id="top" class="blog-index">
  <div class="container blog-index__inner">
    <header class="blog-index__head">
      <p class="mono blog-kicker">Olive / Blog</p>
      <h1>Guides and explainers</h1>
      <p class="blog-index__lede">How the Olive platform works, how the CLV and LUX bridges and their swaps to OLV work, and what connected DeFi and agentic trading mean.</p>
    </header>
{chr(10).join(sections) if sections else '    <p class="blog-index__lede">No articles yet.</p>'}
  </div>
</main>

{footer}
<script src="../assets/js/landing.js"></script>
</body>
</html>
"""


def write_sitemap(articles: list[lib.Article]) -> None:
    rows = []
    for page in lib.STATIC_PAGES:
        loc = f"{lib.SITE_URL}/{page}"
        rows.append(f"  <url><loc>{loc}</loc></url>")
    rows.append(f"  <url><loc>{lib.SITE_URL}/blog/</loc></url>")
    for article in sorted(articles, key=lambda a: a.slug):
        rows.append(
            f"  <url><loc>{article.canonical}</loc><lastmod>{lib.iso(article.updated or article.published)}</lastmod></url>"
        )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(rows)
        + "\n</urlset>\n"
    )
    (lib.ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")


def write_robots() -> None:
    (lib.ROOT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\n"
        f"Sitemap: {lib.SITE_URL}/sitemap.xml\n",
        encoding="utf-8",
    )


def write_llms(articles: list[lib.Article]) -> None:
    latest = articles[:10]
    lines = [
        "# Olive",
        "",
        "> Olive is an asset-agnostic token adoption, security and interoperability framework at olivefinance.org. OLV is Olive's native platform token. External assets are adopted under integration-specific custody and representation terms.",
        "",
        f"Canonical: {lib.SITE_URL}/",
        f"App: {lib.SITE_URL.replace('https://', 'https://wallet.')}",
        "Whitepaper: https://olivefinance.org/olive-whitepaper.pdf",
        "",
        lib.DISAMBIGUATION,
        "",
        "Current model: CLV → OCLV and LUX → OLUX are 1:1 asset bridges. OCLV and OLUX are not tradeable and are not listed on Trade. OCLV → OLV and OLUX → OLV are fixed 1:1 swaps. OLV is tradeable only when Olive enables Trade. The app presents these paths as Bridge and Swap.",
        "",
        "## Framework",
        f"- [Framework]({lib.SITE_URL}/framework/): the asset-agnostic model.",
        f"- [OLV and asset roles]({lib.SITE_URL}/token/): native token and integration roles.",
        f"- [Adoption]({lib.SITE_URL}/adoption/): how an external asset enters the framework.",
        f"- [Integration case]({lib.SITE_URL}/adoption/clv/): the first adopted asset.",
        f"- [LUX bridge and migration]({lib.SITE_URL}/blog/lux-to-olv-migration/): LUX is now supported.",
        f"- [Security and custody]({lib.SITE_URL}/security/): controls and risks.",
        f"- [Interoperability]({lib.SITE_URL}/interoperability/): current scope and later direction.",
        f"- [Docs]({lib.SITE_URL}/docs/): framework reference.",
        f"- [Architecture]({lib.SITE_URL}/docs/architecture/): reference stack and execution path.",
        f"- [Team]({lib.SITE_URL}/team/): operators, advisors and investors.",
        f"- [Roadmap]({lib.SITE_URL}/docs/roadmap/)",
        "",
        "## Product",
        f"- [Connected DeFi]({lib.SITE_URL}/features/connected-defi/): one route into supported networks and protocols.",
        f"- [Quantitative Investments]({lib.SITE_URL}/features/quantitative-investments/): research, models and analysis.",
        f"- [Agentic Trading]({lib.SITE_URL}/features/agentic-trading/): authorised agents acting within user limits.",
        f"- [Asset and Portfolio Management]({lib.SITE_URL}/features/asset-portfolio-management/): one view of positions and events.",
        "",
        "## Articles",
    ]
    for a in latest:
        lines.append(f"- [{a.title}]({a.canonical}): {a.description}")
    lines += [
        "",
        "## Notes",
        "- Olive is in development. Nothing on this site is financial advice or a promise of returns.",
        "- Integration-specific assembly, custody and representation terms live in the integration case study.",
        "- The bridge address, swap terms and limits are shown inside the app after sign-in.",
        "",
    ]
    (lib.ROOT / "llms.txt").write_text("\n".join(lines), encoding="utf-8")


def write_feed(articles: list[lib.Article]) -> None:
    items = []
    for a in articles[:20]:
        dt = datetime.fromisoformat(lib.iso(a.published)).replace(tzinfo=timezone.utc)
        items.append(
            f"    <item>\n"
            f"      <title>{html.escape(a.title)}</title>\n"
            f"      <link>{a.canonical}</link>\n"
            f"      <guid isPermaLink=\"true\">{a.canonical}</guid>\n"
            f"      <pubDate>{format_datetime(dt)}</pubDate>\n"
            f"      <description>{html.escape(a.description)}</description>\n"
            f"    </item>"
        )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0"><channel>\n'
        "  <title>Olive blog</title>\n"
        f"  <link>{lib.SITE_URL}/blog/</link>\n"
        "  <description>Guides and explainers on Olive, connected DeFi, and the CLV and LUX bridges.</description>\n"
        "  <language>en</language>\n"
        + "\n".join(items)
        + "\n</channel></rss>\n"
    )
    (lib.ROOT / "feed.xml").write_text(xml, encoding="utf-8")


def main() -> int:
    articles = lib.load_articles()
    defs, header, footer = shell_parts()
    lib.BLOG.mkdir(exist_ok=True)
    for article in articles:
        out = lib.BLOG / article.slug / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_post(article, articles, defs, header, footer), encoding="utf-8")
    (lib.BLOG / "index.html").write_text(render_index(articles, defs, header, footer), encoding="utf-8")
    write_sitemap(articles)
    write_robots()
    write_llms(articles)
    write_feed(articles)
    print(f"built {len(articles)} articles, blog index, sitemap, robots, llms.txt, feed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
