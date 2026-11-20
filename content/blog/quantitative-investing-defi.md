---
slug: quantitative-investing-defi
title: "Quantitative investing in DeFi: data, models and risk"
description: "Quantitative investing uses data and models to evaluate opportunities. Here is what it means in DeFi, what the Olive product describes, and where limits are."
cluster: quantitative
type: explainer
target_query: "quantitative investing in defi"
answer: "Quantitative investing uses data, statistics and models to evaluate opportunities instead of relying on a single opinion. In DeFi it draws on market and on-chain data, then tests a view before acting. Olive describes it as the research layer of its platform, supporting decisions while the user keeps authority."
published: "2026-11-19"
updated: "2026-11-19"
internal_links: ["/features/quantitative-investments/", "/blog/what-is-agentic-trading/", "/blog/what-is-olive/"]
sources: ["https://olivefinance.org/features/quantitative-investments/", "https://ethereum.org/en/defi/"]
disclaimer: financial
---

Most investment decisions start with a story. A narrative about a market, a hunch about a trend, a claim from someone confident. Quantitative investing starts with a measurement instead.

This page explains what quantitative investing in DeFi means, what the Olive product describes, and where the method stops being useful.

## What quantitative investing means

Quantitative investing uses data and models to evaluate opportunities. The aim is not to remove judgment. It is to make the judgment testable.

A quantitative process usually has three parts.

1. **Gather.** Bring the relevant data together.
2. **Analyse.** Apply a model, a statistic or a comparison.
3. **Decide.** Use the result to support a decision.

The method is only as good as the data and the assumption behind the model. That is why the third step matters. A model produces a result. It does not produce a decision.

## What it looks like in DeFi

DeFi adds a useful ingredient: public data. On-chain activity, liquidity, prices and protocol usage can be observed without asking a company for a report.

That does not make the data simple. Three problems appear immediately.

- **Coverage.** Not every market is measurable, and some data is thin.
- **Quality.** A feed can lag, miss a pool, or report a value that no one can trade at.
- **Context.** A number without a comparison is not analysis. A yield means little without risk, liquidity and duration beside it.

Quantitative work in DeFi is mostly the discipline of handling those three problems.

## What the Olive product describes

The Olive description groups the pillar into three capabilities.

| Capability | What it covers |
| --- | --- |
| Market intelligence | Prices, trends and on-chain data in one view |
| Quantitative research | Models, statistics and comparable evidence |
| RWA evaluation | Issuer, structure, income, liquidity and risk |

The flow is gather, analyse, decide. The description is explicit that analysis supports the decision and authority stays with the user.

That is the right boundary. A research tool that quietly becomes an advice tool has changed the product without saying so.

## Backtesting and its limits

Backtesting is the most misunderstood part of quantitative investing. It runs a strategy against historical data to see how it would have behaved.

It is useful for rejecting bad ideas. It is weak at predicting good ones.

Three reasons.

- **Overfitting.** A model can be tuned until it fits the past and nothing else.
- **Regime change.** Markets change shape. A rule that worked in one period may fail in the next.
- **Costs.** Fees, slippage and liquidity are easy to omit and hard to ignore.

A backtest is evidence, not a promise. The product copy says the same thing in fewer words: historical results do not guarantee future outcomes.

## Where the risk sits

Quantitative work does not remove risk. It moves the risk into the assumptions.

- **Data risk.** If the input is wrong, the output is wrong.
- **Model risk.** A model is a simplification, and the simplification can be the mistake.
- **Execution risk.** A good analysis can still be ruined by a bad price or a thin market.
- **Behavior risk.** A tested strategy is hard to follow when it loses. The model does not manage that.

The honest use of quantitative work is to narrow the set of things you might do, not to guarantee the result. A model that cannot be questioned is a story with a chart. Test the assumption, not just the model. That is why the decision stays with the user.

## How Olive frames it

Olive presents Quantitative Investments as the intelligence pillar of one system. Connected DeFi supplies access, Agentic Trading carries out authorised execution, and Asset and Portfolio Management holds the view.

You can read the product detail on the [Quantitative Investments page](/features/quantitative-investments/), the execution side in the [agentic trading explainer](/blog/what-is-agentic-trading/), and the platform summary on [What is Olive](/blog/what-is-olive/).

## Frequently asked questions

### What is quantitative investing?

Using data, statistics and models to evaluate opportunities instead of relying on a single opinion.

### Is quantitative investing safer?

No. It can make a process more testable. It does not remove data, model or execution risk.

### Does a backtest predict returns?

No. Historical and simulated results do not guarantee future outcomes.

### Does Olive give investment advice?

No. The product description says analysis supports the decision and authority stays with the user.
