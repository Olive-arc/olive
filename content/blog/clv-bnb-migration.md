---
slug: clv-bnb-migration
title: "CLV BNB migration: moving BEP20 tokens to Olive"
description: "If your CLV is on BNB Smart Chain, the migration starts from a BEP20 wallet. Here is what to check, from gas to the network shown in the app."
cluster: migration
type: task
target_query: "clv bnb migration"
answer: "CLV on BNB Smart Chain is a BEP20 token, so the migration starts from a BNB Chain wallet you control. You need BNB for network fees, the right wallet, and the network confirmed in the app. All CLV holders are eligible, and no deadline is set as of 19 November 2026."
published: "2026-11-19"
updated: "2026-11-19"
internal_links: ["/blog/clv-to-olv-migration/", "/blog/clv-migration-checklist/", "/blog/clv-migration-official-links/"]
sources: ["https://wallet.olivefinance.org/", "https://olive-whitepaper.census-explorer.workers.dev/"]
disclaimer: financial
---

CLV exists on more than one network, and the path differs by network. This page covers the CLV BNB migration path, for CLV that sits on BNB Smart Chain.

Status checked 19 November 2026.

## What BEP20 means for this migration

BEP20 is the token standard on BNB Smart Chain. If your CLV is a BEP20 token, it sits in a BNB Chain wallet, and any action on it uses BNB for network fees.

That is the practical difference from the Ethereum path. The asset is called CLV in both cases, but the network, the wallet and the fee token are different. Olive accepts both, and the app shows which one it is reading.

## What to check before you start

1. **The network.** Confirm the CLV is on BNB Smart Chain, not Ethereum and not another chain.
2. **The wallet.** Use a wallet you control, not an exchange withdrawal address.
3. **The fee token.** Keep a small amount of BNB in the wallet for network fees.
4. **The app terms.** Read the asset, network and current rate shown in the app.
5. **The official link.** Compare the domain against the official links page before you connect.

If any of those is unclear, stop before you send anything.

## The short path

1. Sign in at [wallet.olivefinance.org](https://wallet.olivefinance.org).
2. Open the migration page.
3. Read the asset and network shown in the app.
4. Follow the in-app steps from your BNB Chain wallet.
5. Keep the transaction hash and the amount.
6. Check that your OCLV balance appears after the migration completes.

The app carries the live terms. This page does not publish a rate.

## Common BNB path mistakes

**Using an Ethereum address as the source.** If the CLV is BEP20, the wallet must be on BNB Smart Chain. A bridge or a wrong-network send is not part of the migration.

**Forgetting gas.** A wallet with CLV but no BNB cannot pay the network fee. Keep a small balance.

**Withdrawing from an exchange to the wrong network.** Check the network on the withdrawal screen. A BEP20 withdrawal must go to a BNB Chain address.

**Using an address from a message.** Only the address shown in the app applies. Read the [scam warning](/blog/clv-migration-scams/) if someone sends you one.

## BNB path versus Ethereum path

| Item | BNB Smart Chain | Ethereum |
| --- | --- | --- |
| Standard | BEP20 | ERC20 |
| Fee token | BNB | ETH |
| Wallet network | BNB Chain | Ethereum |
| Destination | OCLV | OCLV |

The destination is the same. The route is not. Use the one that matches where your CLV sits.

## If you hold CLV on both networks

Treat them as two migrations. Keep a separate record for each, and start each from the wallet that holds the asset.

You do not need to consolidate first. The [full migration guide](/blog/clv-to-olv-migration/) covers the general path, and the [checklist](/blog/clv-migration-checklist/) keeps the steps in order.

## Frequently asked questions

### Can I migrate CLV from BNB Smart Chain?

Yes. CLV on BNB Smart Chain is a BEP20 token, and Olive accepts it.

### Do I need BNB to migrate?

Keep a small amount of BNB in the wallet for network fees.

### Is the BNB path different from Ethereum?

The asset and the network are different, and the destination is the same. The app shows the steps for your asset.

### Is there a deadline?

No deadline is set as of 19 November 2026.
