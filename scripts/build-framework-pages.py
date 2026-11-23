#!/usr/bin/env python3
"""Build the static Olive framework pages from shared docs shell/content."""
from __future__ import annotations
import html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://olivefinance.org"

def shell(prefix: str) -> tuple[str, str, str]:
    src = (ROOT / "docs/roadmap/index.html").read_text(encoding="utf-8")
    defs = re.search(r'<svg width="0" height="0".*?</svg>', src, re.S).group(0)
    header = re.search(r'<a class="skip-link".*?</header>', src, re.S).group(0)
    footer = re.search(r"<footer.*?</footer>", src, re.S).group(0)
    if prefix != "../../":
        for chunk in (defs, header, footer):
            chunk = chunk.replace("../../", prefix)
        header = header.replace("../../", prefix)
        footer = footer.replace("../../", prefix)
        defs = defs.replace("../../", prefix)
    return defs, header, footer

def page(path: str, title: str, desc: str, kicker: str, lede: str, body: str, prefix: str, crumb: str) -> None:
    defs, header, footer = shell(prefix)
    out = ROOT / path / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    schema = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "url": f"{SITE}/{path}/",
        "description": desc,
        "isPartOf": {"@id": f"{SITE}/#website"},
    }
    html_doc = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(desc, quote=True)}">
  <link rel="canonical" href="{SITE}/{path}/">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(desc, quote=True)}">
  <meta property="og:url" content="{SITE}/{path}/">
  <meta property="og:site_name" content="Olive">
  <meta property="og:image" content="{SITE}/assets/img/og.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title)}">
  <meta name="twitter:description" content="{html.escape(desc, quote=True)}">
  <meta name="theme-color" content="#050604">
  <link rel="icon" href="{prefix}assets/img/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="{prefix}assets/img/favicon-32.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="{prefix}assets/img/apple-touch-icon.png">
  <link rel="stylesheet" href="{prefix}assets/css/main.css">
  <link rel="stylesheet" href="{prefix}assets/css/landing.css">
  <link rel="stylesheet" href="{prefix}assets/css/features.css">
  <link rel="stylesheet" href="{prefix}assets/css/docs.css">
  <script>document.documentElement.classList.add('js');</script>
  <script type="application/ld+json">{json.dumps(schema)}</script>
</head>
<body data-theme="black">
{defs}
{header}
<main id="top" tabindex="-1">
  <section class="docs-hero">
    <div class="container">
      <p class="docs-crumb mono"><a href="{prefix}index.html">OLIVE</a> / {crumb}</p>
      <p class="docs-kicker mono">{html.escape(kicker)}</p>
      <h1 class="docs-title">{title}</h1>
      <p class="docs-lede">{lede}</p>
      <div class="docs-meta"><span class="mono">Framework</span><span class="mono">Initial phase</span><span class="mono">Terms in app</span></div>
    </div>
  </section>
  <div class="container docs-content" style="max-width:820px;padding:64px 0 120px">
    {body}
  </div>
</main>
{footer}
<script src="{prefix}assets/js/landing.js"></script>
</body>
</html>
'''
    out.write_text(html_doc, encoding="utf-8")
    print("wrote", out)

# --- content ---
token_body = '''
<section class="docs-section"><h2>Three roles</h2>
<p>The framework separates the native token from external assets and from the representations created inside the ecosystem.</p>
<div class="docs-pillars">
  <div><span class="mono">Native</span><h3>OLV</h3><p>Olive's native platform token. Separate from adopted assets and representations.</p></div>
  <div><span class="mono">Asset</span><h3>Adopted asset</h3><p>An external asset accepted into the framework under an integration.</p></div>
  <div><span class="mono">Representation</span><h3>Asset representation</h3><p>The framework record or asset corresponding to an adopted asset. Not OLV.</p></div>
</div></section>
<section class="docs-section"><h2>OLV</h2>
<p>OLV is Olive's native platform token. Its supply, utility, governance, incentives and allocation are defined by a separate OLV specification.</p>
<p>OLV is not an adopted asset or an asset representation.</p>
<p>OLV has an admin-set reference price shown in the app. It is tradeable on the Trade page only when Olive enables trading. OLV is the output of the OCLV → OLV swap, not a bridge destination.</p></section>
<section class="docs-section"><h2>Adopted assets</h2>
<p>Each integration defines the asset identity, networks, custody, verification, representation, accounting, transferability and redemption rules.</p></section>
<section class="docs-section"><h2>Asset representations</h2>
<p>A representation corresponds to an adopted asset. It is not OLV and is not cross-chain by default. Issuance, backing and redemption are integration-specific.</p></section>
<section class="docs-section"><h2>Read next</h2>
<p><a href="../framework/">Framework overview</a> · <a href="../adoption/">Adoption</a> · <a href="../security/">Security and custody</a> · <a href="../docs/architecture/">Architecture</a></p></section>
'''

adoption_body = '''
<section class="docs-section"><h2>What adoption means</h2>
<p>Adoption is the structured path for bringing an external asset into Olive. It covers the asset, network, route, verification, representation and accounting.</p>
<p>Each integration defines its own custody, verification, representation and product-access rules. The framework defines the standards and interfaces.</p></section>
<section class="docs-section"><h2>Lifecycle</h2>
<ol class="docs-milestones"><li>Integration approval.</li><li>Asset and network registration.</li><li>Custody and route configuration.</li><li>User transfer through the approved route.</li><li>Verification and evidence review.</li><li>Custody confirmation.</li><li>Representation issuance or recording.</li><li>Accounting and reconciliation.</li><li>Product access.</li><li>Lifecycle review or retirement.</li><li>Redemption only where supported.</li></ol></section>
<section class="docs-section"><h2>No single adoption model</h2>
<p>Assets differ. Custody, verification evidence, representation standards, transferability, redemption and legal constraints are integration-specific. One integration's mechanics do not automatically apply to another.</p></section>
<section class="docs-section"><h2>Integration interface</h2>
<ul class="docs-list"><li>Asset identity and supported networks</li><li>Custody and control evidence</li><li>Deposit routes</li><li>Verification method</li><li>Representation standard</li><li>Accounting and reconciliation</li><li>Product access and transferability</li><li>Redemption, if supported</li><li>Risk and legal constraints</li></ul></section>
<section class="docs-section"><h2>Read next</h2>
<p><a href="../framework/">Framework overview</a> · <a href="../docs/architecture/">Architecture</a> · <a href="../security/">Security and custody</a> · <a href="clv/">Integration case study</a></p></section>
'''

clv_body = '''
<section class="docs-section"><h2>CLV on two networks</h2>
<div class="table-wrap"><table class="mobile-stack"><thead><tr><th>Network</th><th>Chain ID</th><th>CLV contract</th><th>Bridge address</th></tr></thead><tbody><tr><td data-label="Network">Ethereum</td><td data-label="Chain ID">1</td><td data-label="CLV contract"><code>0x80C62FE4487E1351b47Ba49809EBD60ED085bf52</code></td><td data-label="Bridge address"><code>0x8A0319844e0F22657951307642A02bF77478C6ac</code></td></tr><tr><td data-label="Network">BNB Smart Chain</td><td data-label="Chain ID">56</td><td data-label="CLV contract"><code>0x09E889BB4D5b474f561db0491C38702F367A4e4d</code></td><td data-label="Bridge address"><code>0xf14e593De9E7dD75fd21F46f579C179B841fe562</code></td></tr></tbody></table></div>
<p>Each network has its own bridge address. Check the network and contract before sending. Do not use an address from a direct message.</p></section>
<section class="docs-section"><h2>What happens to CLV</h2>
<p>Under the initial model, Olive controls the underlying CLV through its designated custody arrangement. The framework records the selected network, route and asset so the transfer can be reviewed against the current terms.</p>
<p>CLV is the underlying asset. OCLV is the representation. OLV is the native platform token.</p></section>
<section class="docs-section"><h2>Current terms</h2>
<p>CLV is bridged to OCLV at <strong>1 CLV to 1 OCLV</strong>. The Olive bridge is free; network fees may still apply.</p>
<p>OCLV is not listed on Trade. It can only be swapped to OLV through the approved OCLV → OLV swap, which carries a fee shown before confirmation.</p>
<p>LUX is not part of the initial CLV phase.</p></section>
<section class="docs-section"><h2>Verify</h2>
<p>Use the official links and the scam warning before sending anything. Support never asks for a seed phrase or a direct-message address.</p>
<p><a href="../../blog/clv-to-olv-migration/">CLV to OCLV bridge guide</a> · <a href="../../blog/clv-migration-official-links/">Official links</a> · <a href="../../docs/adoption-faq/">Adoption FAQ</a></p></section>
'''

oclv_body = '''
<section class="docs-section"><h2>OCLV is the representation of CLV</h2>
<p>OCLV is created when CLV is bridged into Olive at 1:1. It is not OLV, and it is not a cross-chain token in the initial implementation.</p>
<div class="docs-callout">OCLV is not listed on Trade. Its only approved conversion is the OCLV → OLV swap.</div></section>
<section class="docs-section"><h2>Initial boundaries</h2>
<ul class="docs-list"><li>CLV → OCLV is a 1:1 bridge.</li><li>OCLV is not cross-chain in the initial implementation.</li><li>OCLV is not tradeable on the Trade page.</li><li>OCLV can be swapped to OLV when the admin enables the swap route.</li><li>The swap has a fee shown before confirmation; the bridge is free.</li><li>Backing and redemption rules remain separate integration terms.</li></ul></section>
<section class="docs-section"><h2>Issuance and accounting</h2>
<p>OCLV is credited after the CLV bridge is reviewed and approved. Records keep custody assets, representation liabilities and the native token separate.</p>
<p>Do not assume OCLV is fully backed, guaranteed, risk-free, redeemable on demand or transferable across networks.</p></section>
<section class="docs-section"><h2>What you should not assume</h2>
<p>Do not assume OCLV is fully backed, guaranteed, risk-free, redeemable on demand or transferable across networks. Those claims require approved mechanics and evidence.</p></section>
<section class="docs-section"><h2>Read next</h2>
<p><a href="../token/">Token roles</a> · <a href="../adoption/">Adoption</a> · <a href="../security/">Security and custody</a> · <a href="../docs/adoption-faq/">Adoption FAQ</a></p></section>
'''

security_body = '''
<section class="docs-section"><h2>Security is Gate 0</h2>
<p>Security and operational readiness starts first in the framework roadmap and remains a gate on every later workstream. Representation issuance follows the app's approval and ledger controls; public custody attestation and external review remain pending.</p></section>
<section class="docs-section"><h2>Control areas</h2>
<div class="docs-pillars">
<div><span class="mono">Custody</span><h3>Asset control</h3><p>Designated custody, signing authority, access separation and movement controls.</p></div>
<div><span class="mono">Verification</span><h3>Evidence and checks</h3><p>Network, asset, route, transfer evidence and duplicate prevention.</p></div>
<div><span class="mono">Accounting</span><h3>Representation and reserves</h3><p>Separate custody assets, representation liabilities, native supply and clearing accounts.</p></div>
<div><span class="mono">Operations</span><h3>Monitoring and response</h3><p>Alerts, reconciliation, escalation, emergency controls and post-incident review.</p></div>
</div></section>
<section class="docs-section"><h2>Custody</h2>
<p>Each integration defines its legal and operational custody arrangement, control evidence, segregation or omnibus treatment, movement authorization and public disclosure.</p></section>
<section class="docs-section"><h2>Representation and reserves</h2>
<p>Representation supply is a liability, not native supply. Custody assets, representation liabilities and clearing accounts remain separate. Backing and reserve treatment are integration-specific.</p></section>
<section class="docs-section"><h2>Risks</h2>
<ul class="docs-list"><li>Custody and key-management risk</li><li>Verification and reconciliation risk</li><li>Smart contract and operational risk</li><li>Admin and access-control risk</li><li>Market, liquidity and legal risk</li><li>Future interoperability and bridge risk</li></ul></section>
<section class="docs-section"><h2>Open decisions</h2>
<p>Public custody attestation, external review, verification standards, reconciliation cadence and emergency governance remain open.</p></section>
'''

interop_body = '''
<section class="docs-section"><h2>Interoperability is a later capability</h2>
<p>Olive's long-term direction includes interoperability across supported networks. The initial phase is about framework foundations, custody and representation. It is not a claim that representations are cross-chain.</p>
<div class="docs-callout">No representation is cross-chain by default.</div></section>
<section class="docs-section"><h2>Current scope</h2>
<ul class="docs-list"><li>Integration-specific custody and representation.</li><li>Supported networks defined per integration.</li><li>Existing wallet and product experiences.</li><li>CLV → OCLV is an asset bridge, not a cross-chain bridge.</li><li>No live cross-chain Olive bridge.</li><li>No default cross-chain transfer.</li></ul></section>
<section class="docs-section"><h2>Later phases</h2>
<p>Additional networks and cross-network movement require separate architecture, verification, security review and legal analysis. Cross-chain bridge risk is distinct from the CLV → OCLV asset bridge.</p></section>
<section class="docs-section"><h2>What will not be claimed early</h2>
<p>Olive will not describe a bridge or cross-chain representation as live before it is implemented, verified and disclosed.</p></section>
'''

docs_body = '''
<section class="docs-section"><h2>Framework documents</h2>
<div class="docs-pillars">
<div><span class="mono">01</span><h3><a href="../framework/">Framework</a></h3><p>The framework model and operating principles.</p></div>
<div><span class="mono">02</span><h3><a href="../adoption/">Adoption</a></h3><p>How external assets enter the framework.</p></div>
<div><span class="mono">03</span><h3><a href="../token/">OLV and integration roles</a></h3><p>Native token and integration asset roles.</p></div>
<div><span class="mono">04</span><h3><a href="../security/">Security &amp; custody</a></h3><p>Controls, responsibilities and risk.</p></div>
<div><span class="mono">05</span><h3><a href="../interoperability/">Interoperability</a></h3><p>Current scope and later direction.</p></div>
<div><span class="mono">06</span><h3><a href="architecture/">Architecture</a></h3><p>Layers, interfaces and execution path.</p></div>
<div><span class="mono">07</span><h3><a href="adoption-faq/">Adoption FAQ</a></h3><p>Framework questions.</p></div>
<div><span class="mono">08</span><h3><a href="glossary/">Glossary</a></h3><p>Framework terminology.</p></div>
<div><span class="mono">09</span><h3><a href="whitepaper/">Whitepaper</a></h3><p>Product vision, framework, operating model and security.</p></div>
</div></section>
<section class="docs-section"><h2>Integration case study</h2>
<p><a href="../adoption/clv/">View the integration case study</a> for the first adopted asset.</p></section>
'''

faq_body = '''
<section class="docs-section"><h2>What is Olive?</h2><p>Olive is a token adoption, security and interoperability framework for bringing external assets into a controlled ecosystem.</p></section>
<section class="docs-section"><h2>Is Olive a bridge?</h2><p>CLV → OCLV is an asset bridge inside Olive. Olive is not a cross-chain bridge, and cross-network interoperability remains a later capability.</p></section>
<section class="docs-section"><h2>What is OLV?</h2><p>OLV is Olive's native platform token. It is separate from adopted assets and representations.</p></section>
<section class="docs-section"><h2>What is an adopted asset?</h2><p>An external asset accepted into the framework under an approved integration.</p></section>
<section class="docs-section"><h2>What is an asset representation?</h2><p>The framework representation of an adopted asset. OCLV is the CLV representation. It is not OLV.</p></section>
<section class="docs-section"><h2>Do all assets use the same rules?</h2><p>No. Each integration defines its own custody, verification, representation, accounting and redemption rules.</p></section>
<section class="docs-section"><h2>Is a representation cross-chain?</h2><p>Not by default.</p></section>
<section class="docs-section"><h2>Is a representation fully backed or redeemable?</h2><p>Those claims require an integration-specific approved model and evidence.</p></section>
<section class="docs-section"><h2>How do I get OLV?</h2><p>Bridge CLV to OCLV at 1:1, then swap OCLV to OLV through the approved swap route when it is enabled. The swap fee is shown before confirmation.</p></section>
<section class="docs-section"><h2>Is OCLV tradeable?</h2><p>No. OCLV is not listed on Trade. It can only be swapped to OLV.</p></section>
<section class="docs-section"><h2>Where do I find an asset's terms?</h2><p>In the app and that integration's case study. Do not apply one integration's terms to another asset.</p></section>
<section class="docs-section"><h2>Where are the official links?</h2><p>Site: <a href="https://olivefinance.org">olivefinance.org</a> · App: <a href="https://wallet.olivefinance.org">wallet.olivefinance.org</a> · Telegram: <a href="https://t.me/olive_eng">t.me/olive_eng</a>. Never use an address or link from a direct message.</p></section>
'''

glossary_body = '''
<section class="docs-section"><h2>Core terms</h2>
<div class="docs-pillars">
<div><span class="mono">OLV</span><h3>Native platform token</h3><p>Olive's native token. Separate from adopted assets and representations.</p></div>
<div><span class="mono">Asset</span><h3>Adopted asset</h3><p>An external asset accepted into the framework under an integration.</p></div>
<div><span class="mono">Representation</span><h3>Framework representation</h3><p>The framework record or asset corresponding to an adopted asset. Not OLV.</p></div>
<div><span class="mono">Integration</span><h3>Asset implementation</h3><p>The asset-specific implementation of framework standards.</p></div>
</div></section>
<section class="docs-section"><h2>Framework terms</h2>
<p><strong>Adoption.</strong> The process of bringing an external asset into the framework.</p>
<p><strong>Custody.</strong> The legal and operational arrangement for controlling the underlying asset.</p>
<p><strong>Verification.</strong> Validation of network, asset, route, evidence and confirmation policy.</p>
<p><strong>Issuance.</strong> Creation or recording of a representation under an integration's rules.</p>
<p><strong>Redemption.</strong> Return or release of an underlying asset against a representation, where supported.</p>
<p><strong>Reconciliation.</strong> Comparison of custody records, representation liabilities and ledger balances.</p>
<p><strong>Cross-chain.</strong> Movement or coordination between networks. Not default.</p>
<p><strong>Asset bridge.</strong> The CLV → OCLV conversion route inside Olive. It is not a cross-chain bridge.</p>
<p><strong>Swap.</strong> The OCLV → OLV conversion at a fixed rate, with the fee shown before confirmation.</p></section>
<section class="docs-section"><h2>Claim rules</h2>
<p>Use OLV only as the native token name. Refer to external assets generically unless the page is an integration case study.</p></section>
'''

whitepaper_body = '''
<section class="docs-section"><h2>Olive Whitepaper — A Connected Financial Platform</h2>
<p><strong>Working document · 23 November 2026.</strong> Product vision, framework architecture, operating model and security. The paper distinguishes intended platform direction, initial implementation and future development. Proposed systems are not claims of deployment, audit or general availability.</p>
<div class="docs-cta"><a class="btn btn--primary" href="/olive-whitepaper.pdf"><span>Download the PDF</span><svg class="btn__arrow" width="16" height="16" aria-hidden="true"><use href="#arr"/></svg></a></div></section>
<section class="docs-section"><h2>What it covers</h2>
<ul class="docs-list"><li>Olive's purpose and central proposition</li><li>The fragmented asset and financial experience problem</li><li>Vision, principles and framework-led platform model</li><li>Asset adoption, custody, representation and verification</li><li>Technical architecture and shared platform services</li><li>Connected DeFi, Quantitative Investments, Agentic Trading and Portfolio Management</li><li>RWA marketplace responsibilities and boundaries</li><li>Business and operating model</li><li>Security, risk management and user protection</li></ul></section>
<section class="docs-section"><h2>Status and boundaries</h2>
<p>The paper is a working document. It does not promise guaranteed returns, instant liquidity, automatic redemption, uninterrupted availability or elimination of financial and technical risk. Any audit, assessment or deployment claim must be read with its scope, date and limitations.</p></section>
'''

architecture_body = '''
<section class="docs-section"><h2>Asset and integration registry</h2>
<p>Defines supported assets, networks, routes, roles and lifecycle state. Integration configuration is registered without hardcoding asset properties into core logic.</p></section>
<section class="docs-section"><h2>Account and permissions</h2>
<p>User authority is separated from scoped execution authority. Validators, executors, hooks and guards enforce capital limits, allowlists, risk tiers, expiry and revocation.</p></section>
<section class="docs-section"><h2>Custody and asset control</h2>
<p>Underlying assets are held under an approved custody arrangement. Signing authority, movement authorization, segregation or omnibus treatment and control evidence are explicit per integration.</p></section>
<section class="docs-section"><h2>Verification and evidence</h2>
<p>Network, asset identity, route, transfer evidence and confirmation policy are validated before value is recognized. Duplicate and replay checks are mandatory.</p></section>
<section class="docs-section"><h2>Representation and issuance</h2>
<p>Representations are issued or recorded under integration-specific standards. Issuance is idempotent and linked to custody and verification evidence.</p></section>
<section class="docs-section"><h2>Accounting and reconciliation</h2>
<p>Custody assets, representation liabilities, native supply and clearing accounts remain separate. Reconciliation compares custody, liabilities and ledger records.</p></section>
<section class="docs-section"><h2>Product and protocol access</h2>
<p>Products access approved assets and representations through standard connectors. Multi-step actions execute atomically where required. Product totals follow approved accounting rules.</p></section>
<section class="docs-section"><h2>Native token and swap access</h2><p>Native-token trading and representation swaps are admin-gated product functions. They use current terms, snapshot the fee and rates at submission, and never imply a fixed market conversion outside the configured pair.</p></section>
<section class="docs-section"><h2>Monitoring and governance</h2>
<p>Transactions are simulated, activity is monitored and risk conditions trigger pause controls. Roles, approvals, audit and incident response are part of the architecture.</p></section>
<section class="docs-section"><h2>Interoperability</h2>
<p>Cross-network movement is a later layer. Lane limits, message verification, monitoring and bridge risk controls are defined before it is enabled.</p></section>
<section class="docs-section"><h2>End-to-end flow</h2>
<ol class="docs-milestones"><li>Integration is approved and configured.</li><li>User sets limits and permissions.</li><li>Asset enters the custody layer through an approved route.</li><li>Verification confirms network, asset and evidence.</li><li>Representation is issued or recorded under the integration's rules.</li><li>Accounting and reconciliation record the position.</li><li>Approved products and agents can access the representation.</li><li>Monitoring and pause controls remain active.</li></ol></section>
'''

framework_body = '''
<section class="docs-section"><h2>What the framework does</h2>
<p>Olive provides a standard way for external assets to enter a controlled ecosystem. The framework handles permissions, custody, verification, representation, accounting, product access and controls.</p></section>
<section class="docs-section"><h2>The layers</h2>
<div class="docs-pillars">
<div><span class="mono">01</span><h3>Account and permissions</h3><p>User authority, scoped execution, limits and revocation.</p></div>
<div><span class="mono">02</span><h3>Adoption and custody</h3><p>Asset registration, routes, custody and movement control.</p></div>
<div><span class="mono">03</span><h3>Representation and accounting</h3><p>Issuance, supply, liabilities and reconciliation.</p></div>
<div><span class="mono">04</span><h3>Protocol access</h3><p>Standard connectors and atomic execution across products.</p></div>
<div><span class="mono">05</span><h3>Strategy and RWA lifecycle</h3><p>Policy limits, valuation, restrictions and queued redemption.</p></div>
<div><span class="mono">06</span><h3>Monitoring and controls</h3><p>Simulation, anomaly detection, pauses and incident response.</p></div>
<div><span class="mono">07</span><h3>Interoperability</h3><p>Later cross-network movement with verification and lane controls.</p></div>
</div></section>
<section class="docs-section"><h2>How the flow works</h2>
<ol class="docs-milestones"><li>Permissions define what can happen.</li><li>Custody secures the underlying asset.</li><li>Verification confirms the transfer and evidence.</li><li>Representation and accounting record the result.</li><li>Strategy and connectors execute within limits.</li><li>Hooks, guards and monitoring enforce the boundaries.</li></ol></section>
<section class="docs-section"><h2>Built for the product stack</h2>
<p>Olive Wallet is the shared foundation. Connected DeFi, Quantitative Investments, Agentic Trading, Asset and Portfolio Management and the RWA experience sit on top of the framework.</p></section>
<section class="docs-section"><h2>Go deeper</h2>
<p><a href="../adoption/">Adoption</a> · <a href="../docs/architecture/">Architecture</a> · <a href="../security/">Security and custody</a> · <a href="../interoperability/">Interoperability</a> · <a href="../adoption/clv/">Integration case study</a></p></section>
'''

page("token", "OLV and asset roles", "OLV is Olive's native token. External assets are adopted under integration terms and represented separately. Here is how the roles separate.", "Token framework", "One native token. Separate assets. Separate representations.", token_body, "../", "TOKEN")
page("adoption", "Adoption: how external assets enter Olive", "Olive's framework for adopting an external asset, verifying the underlying transfer, representing it and integrating it into the ecosystem.", "Adoption framework", "A structured path from an external asset to a managed representation.", adoption_body, "../", "ADOPTION")
page("adoption/clv", "CLV adoption: the first framework asset", "CLV is the first adopted asset in the Olive Framework, supported on Ethereum and BNB Smart Chain.", "CLV / First adopted asset", "The first case for the framework, with two networks and one designated route.", clv_body, "../../", "ADOPTION / CLV")
page("oclv", "OCLV: Olive's representation of CLV", "OCLV represents CLV inside the Olive ecosystem. It is not OLV and is not cross-chain in the initial implementation.", "OCLV / Representation", "A representation, not the native token.", oclv_body, "../", "OCLV")
page("security", "Security and custody: controls and risk", "Olive's framework separates custody, verification, representation, accounting and operations. Here are the control areas and the risks that remain.", "Security & custody", "Security is a responsibility to be demonstrated.", security_body, "../", "SECURITY")
page("interoperability", "Interoperability: current scope and later direction", "Olive's initial phase is not cross-chain. Here is what interoperability means now, what is later, and what is not claimed.", "Interoperability", "Cross-network movement is a later capability.", interop_body, "../", "INTEROPERABILITY")
page("framework", "Olive framework overview", "Olive's asset-agnostic framework for permissions, custody, verification, representation, accounting, product access and controls.", "Framework", "One architecture. Every layer connected.", framework_body, "../", "FRAMEWORK")
page("docs", "Olive framework documentation", "The current Olive framework pages: framework model, adoption, asset roles, security, interoperability, architecture, roadmap and FAQ.", "Docs", "The current framework reference.", docs_body, "../", "DOCS")
page("docs/adoption-faq", "Adoption FAQ: framework terms", "Answers to common questions about Olive adoption, assets, representations, custody and interoperability.", "Adoption FAQ", "The short answers.", faq_body, "../../", "DOCS / ADOPTION FAQ")
page("docs/glossary", "Olive glossary: framework terms", "Plain-language definitions for the Olive Framework, asset roles, custody, issuance and interoperability.", "Glossary", "The words that carry the model.", glossary_body, "../../", "DOCS / GLOSSARY")
page("docs/whitepaper", "Olive Whitepaper — A Connected Financial Platform", "Olive whitepaper: product vision, framework architecture, operating model and security. Working document, 23 November 2026.", "Whitepaper", "A connected financial platform.", whitepaper_body, "../../", "DOCS / WHITEPAPER")
page("docs/architecture", "Olive framework architecture", "The layers and execution path behind Olive: permissions, custody, verification, representation, accounting, product access and controls.", "Architecture", "The layers and execution path behind the framework.", architecture_body, "../../", "DOCS / ARCHITECTURE")
