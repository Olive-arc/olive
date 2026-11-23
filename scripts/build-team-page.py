#!/usr/bin/env python3
from __future__ import annotations
import html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://olivefinance.org"

def shell(prefix: str):
    src = (ROOT / "docs/roadmap/index.html").read_text(encoding="utf-8")
    defs = re.search(r'<svg width="0" height="0".*?</svg>', src, re.S).group(0)
    header = re.search(r'<a class="skip-link".*?</header>', src, re.S).group(0)
    footer = re.search(r"<footer.*?</footer>", src, re.S).group(0)
    defs = defs.replace("../../", prefix)
    header = header.replace("../../", prefix)
    footer = footer.replace("../../", prefix)
    return defs, header, footer

def card(person: dict) -> str:
    links = list(person.get("links") or [])
    links.append({"label": "Profile", "url": person["source"]})
    socials = "".join(
        f'<a href="{html.escape(link["url"], quote=True)}" target="_blank" rel="noopener noreferrer">{html.escape(link["label"])}</a>'
        for link in links
    )
    return f'''<article class="team-card">
  <img class="team-card__photo" src="../assets/img/team/{html.escape(person["image"], quote=True)}" alt="{html.escape(person["name"], quote=True)}" loading="lazy" width="900" height="900">
  <div class="team-card__body">
    <p class="team-card__affiliation">{html.escape(person.get("affiliation", "Olive"))}</p>
    <h3 class="team-card__name">{html.escape(person["name"])}</h3>
    <p class="team-card__role">{html.escape(person["role"])}</p>
    <p class="team-card__focus">{html.escape(person.get("focus", ""))}</p>
    <div class="team-links">{socials}</div>
  </div>
</article>'''

def group(title: str, number: str, people: list[dict]) -> str:
    return f'''<section class="team-group">
  <div class="team-group__head"><h2>{title}</h2><span>{number}</span></div>
  <div class="team-grid">{''.join(card(p) for p in people)}</div>
</section>'''

def main():
    data = json.loads((ROOT / "content/team.json").read_text(encoding="utf-8"))
    defs, header, footer = shell("../")
    schema = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Olive team and investors",
        "url": f"{SITE}/team/",
        "itemListElement": [
            {"@type": "Person", "name": person["name"], "jobTitle": person["role"]}
            for key in ("team", "advisors", "investors")
            for person in data.get(key, [])
        ],
    }
    groups = [
        ("Team", data.get("team", [])),
        ("Advisors", data.get("advisors", [])),
        ("Investors", data.get("investors", [])),
    ]
    active_groups = [(title, people) for title, people in groups if people]
    body = "".join(
        group(title, f"{index:02d}", people)
        for index, (title, people) in enumerate(active_groups, start=1)
    )
    page = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Team and investors — OLIVE</title>
  <meta name="description" content="The team and investors behind Olive.">
  <link rel="canonical" href="{SITE}/team/">
  <meta property="og:type" content="website">
  <meta property="og:title" content="Team and investors — OLIVE">
  <meta property="og:description" content="The team and investors behind Olive.">
  <meta property="og:url" content="{SITE}/team/">
  <meta property="og:site_name" content="Olive">
  <meta property="og:image" content="{SITE}/assets/img/og.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#050604">
  <link rel="icon" href="../assets/img/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="../assets/img/favicon-32.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="../assets/img/apple-touch-icon.png">
  <link rel="stylesheet" href="../assets/css/main.css">
  <link rel="stylesheet" href="../assets/css/landing.css">
  <link rel="stylesheet" href="../assets/css/features.css">
  <link rel="stylesheet" href="../assets/css/team.css">
  <script>document.documentElement.classList.add('js');</script>
  <script type="application/ld+json">{json.dumps(schema)}</script>
</head>
<body data-theme="black">
{defs}
{header}
<main id="top" tabindex="-1">
  <section class="team-hero">
    <div class="container">
      <p class="docs-crumb mono"><a href="../index.html">OLIVE</a> / TEAM</p>
      <p class="docs-kicker mono">People</p>
      <h1>Team and<br><span>investors.</span></h1>
      <p class="lede">The team and investors supporting Olive's framework and ecosystem.</p>
    </div>
  </section>
  <div class="container team-wrap">{body}</div>
</main>
{footer}
<script src="../assets/js/landing.js"></script>
</body>
</html>
'''
    out = ROOT / "team/index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"wrote {out}")

if __name__ == "__main__":
    main()
