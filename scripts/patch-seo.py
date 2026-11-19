#!/usr/bin/env python3
"""Add canonical, Open Graph, Twitter and JSON-LD to the hand-written pages.

Idempotent. The block between the seo:auto markers is replaced on every run.

    python3 scripts/patch-seo.py
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import content_lib as lib  # noqa: E402

PAGES = [
    ("index.html", "/", "Olive", None, "home"),
    ("features/connected-defi/index.html", "/features/connected-defi/", "Connected DeFi", "Features", "page"),
    ("features/quantitative-investments/index.html", "/features/quantitative-investments/", "Quantitative Investments", "Features", "page"),
    ("features/agentic-trading/index.html", "/features/agentic-trading/", "Agentic Trading", "Features", "page"),
    ("features/asset-portfolio-management/index.html", "/features/asset-portfolio-management/", "Asset and Portfolio Management", "Features", "page"),
    ("docs/roadmap/index.html", "/docs/roadmap/", "Roadmap", "Docs", "page"),
]

ORG = {
    "@type": "Organization",
    "@id": f"{lib.SITE_URL}/#organization",
    "name": lib.SITE_NAME,
    "url": lib.SITE_URL,
    "logo": f"{lib.SITE_URL}/assets/img/brand/olive-lockup.svg",
    "description": "Olive is the intelligent DeFi platform at olivefinance.org, combining connected DeFi, quantitative investments, agentic trading, and asset and portfolio management on one wallet foundation.",
    "sameAs": [
        "https://x.com/OliveHq_",
        "https://medium.com/@OLIVEFOUNDATION",
        "https://paragraph.com/@olivefinance",
        "https://github.com/Olive-arc",
    ],
}

WEBSITE = {
    "@type": "WebSite",
    "@id": f"{lib.SITE_URL}/#website",
    "url": lib.SITE_URL,
    "name": lib.SITE_NAME,
    "publisher": {"@id": f"{lib.SITE_URL}/#organization"},
    "inLanguage": "en",
}


def block_for(url: str, name: str, section: str | None, kind: str, description: str, has_canonical: bool) -> str:
    canonical = lib.SITE_URL + url
    image = f"{lib.SITE_URL}/assets/img/og.png"
    lines = ["<!-- seo:auto -->"]
    if not has_canonical:
        lines.append(f'  <link rel="canonical" href="{canonical}">')
    lines += [
        f'  <meta property="og:url" content="{canonical}">',
        f'  <meta property="og:site_name" content="{lib.SITE_NAME}">',
        f'  <meta property="og:image" content="{image}">',
        '  <meta property="og:image:width" content="1200">',
        '  <meta property="og:image:height" content="630">',
        '  <meta property="og:locale" content="en_GB">',
        '  <meta name="twitter:card" content="summary_large_image">',
        f'  <meta name="twitter:title" content="{html.escape(name)}">',
        f'  <meta name="twitter:description" content="{html.escape(description, quote=True)}">',
        f'  <meta name="twitter:image" content="{image}">',
    ]
    if kind == "home":
        graph = [ORG, WEBSITE]
        lines.append(
            f'  <script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graph})}</script>'
        )
    else:
        items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": f"{lib.SITE_URL}/"}]
        if section:
            items.append({"@type": "ListItem", "position": 2, "name": section, "item": f"{lib.SITE_URL}/{section.lower()}/"})
        items.append({"@type": "ListItem", "position": len(items) + 1, "name": name, "item": canonical})
        graph = [
            ORG,
            {"@type": "BreadcrumbList", "itemListElement": items},
            {
                "@type": "WebPage",
                "@id": canonical,
                "url": canonical,
                "name": name,
                "description": description,
                "isPartOf": {"@id": f"{lib.SITE_URL}/#website"},
                "inLanguage": "en",
            },
        ]
        lines.append(
            f'  <script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graph})}</script>'
        )
    lines.append("  <!-- /seo:auto -->")
    return "\n".join(lines)


def patch(path: Path, url: str, name: str, section: str | None, kind: str) -> bool:
    text = path.read_text(encoding="utf-8")
    desc_match = re.search(r'<meta name="description" content="(.*?)"', text, re.S)
    description = desc_match.group(1) if desc_match else ""
    has_canonical = '<link rel="canonical"' in text and "seo:auto" not in text
    block = block_for(url, name, section, kind, description, has_canonical)
    if "<!-- seo:auto -->" in text:
        text = re.sub(r"<!-- seo:auto -->.*?<!-- /seo:auto -->", block, text, flags=re.S)
    elif "</head>" in text:
        text = text.replace("</head>", block + "\n</head>", 1)
    else:
        raise SystemExit(f"no </head> in {path}")
    path.write_text(text, encoding="utf-8")
    return True


def main() -> int:
    changed = 0
    for rel, url, name, section, kind in PAGES:
        path = lib.ROOT / rel
        if not path.exists():
            print(f"skip missing {rel}")
            continue
        patch(path, url, name, section, kind)
        changed += 1
    print(f"patched {changed} pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
