---
slug: clv-migration-status
title: "CLV bridge status: OCLV and the OLV swap explained"
description: "Olive bridges CLV into OCLV at 1:1, then offers an OCLV to OLV swap with a fee. Here is the current status and what to verify before acting."
cluster: migration
type: task
target_query: "clv bridge status"
answer: "Olive bridges CLV into OCLV at 1:1 on Ethereum and BNB Smart Chain. OCLV is not tradeable and is not listed on Trade. It can be swapped to OLV through the approved swap at a fixed 1:1 rate with a 1% fee. OLV is tradeable only when Olive enables Trade."
published: "2026-11-19"
updated: "2026-11-23"
internal_links: ["/blog/clv-to-olv-migration/", "/blog/clv-migration-guide/", "/blog/clv-migration-official-links/"]
sources: ["https://docs.clv.org/", "https://olivefinance.org/"]
disclaimer: financial
---

Status checked 23 November 2026.

This CLV bridge status page explains the CLV to OCLV bridge and the OCLV to OLV swap.

This page tracks the current Olive bridge and swap direction. The app is the authority on live availability and terms.

CLV → OCLV is a free 1:1 bridge. OCLV → OLV is a fee-bearing 1:1 swap. OLV is the native platform token, and OCLV is not listed on Trade.

## Current target

The bridge target is **OCLV**, Olive's representation of CLV.

OLV is Olive's native platform token. It is the output of the OCLV → OLV swap, not the bridge destination.

## Assets in the initial phase

| Asset | Networks | Status |
| --- | --- | --- |
| CLV | Ethereum, BNB Smart Chain | Initial framework case |
| LUX | Solana | Not part of the initial phase |

## What to verify

- the asset and network in the app
- the current terms shown in the app
- the official links page
- the scam warning

## What not to rely on

- a rate from a screenshot or post
- a link from a direct message
- an old page that says the destination is OLV
- any claim that LUX is accepted in the initial phase

## Related pages

- [CLV to OCLV bridge guide](/blog/clv-to-olv-migration/)
- [Migration map](/blog/clv-migration-guide/)
- [Official links](/blog/clv-migration-official-links/)

## Frequently asked questions

### Is OCLV tradeable?

No. OCLV is not listed on Trade. It can only be swapped to OLV through the approved swap.

### Does the bridge accept LUX?

Not in the initial phase. LUX is a separate scope decision.

### What should I check before I send?

Check the asset, the network, the bridge address, the swap fee and the official links page. If anything differs from the app, stop.

### Where are the current terms?

In the app. The app shows the bridge address and the swap fee before confirmation.
