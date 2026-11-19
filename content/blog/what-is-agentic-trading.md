---
slug: what-is-agentic-trading
title: "What is agentic trading? Authorised agents explained"
description: "Agentic trading means authorised agents act on a strategy within limits you set. Here is what you configure, what they can do, and who keeps authority."
cluster: agentic
type: explainer
target_query: "what is agentic trading"
answer: "Agentic trading means authorised agents act on a strategy within limits you set. You define the objectives, assets, risk and capital limits, and you authorise the mandate. Agents can analyse market conditions and execute only inside that mandate. Authority stays with you, and you can review, adjust or revoke it. It is not financial advice."
published: "2026-11-19"
updated: "2026-11-19"
internal_links: ["/features/agentic-trading/", "/blog/what-is-connected-defi/", "/features/quantitative-investments/"]
sources: ["https://www.nist.gov/itl/ai-risk-management-framework", "https://www.sec.gov/oiea/investor-alerts-and-bulletins/ib_autotrading"]
disclaimer: financial
---

Most trading tools fall into two groups. One group places a rule you wrote and repeats it. The other group tells you what it thinks and waits for you to act. Agentic trading is the third group. It carries out a strategy inside a mandate you define.

This article explains what agentic trading means according to the Olive product description, what you configure, and why the limits matter more than the strategy.

## What is agentic trading?

Agentic trading means authorised agents act on a strategy within limits you assign. You set the objectives, the assets, the risk and the capital limits. You authorise the mandate. The agent can then analyse market conditions, identify opportunities, and execute only inside that mandate.

Three parts have to exist for the description to be honest.

- A strategy you assign, not one the agent invents for you.
- A mandate that sets what is permitted.
- Oversight that lets you review, adjust or revoke authority.

Remove the mandate and you have software with broad permission. Remove oversight and you cannot correct it. Keep both and the question becomes whether the mandate is clear enough to mean something.

## What you define

The product description lists three configuration areas.

| Area | What you set |
| --- | --- |
| Agent configuration | Objectives, assets, risk and capital limits |
| Authorised execution | Permitted activity only within your mandate |
| Monitoring and oversight | Activity, positions and permissions to review |

That is the useful part. The user does the defining. The agent works inside the definition.

A mandate is only meaningful if it names what is out of scope. "Trade well" is not a mandate. A set of assets, a capital limit, a risk boundary and a review point is.

## Authorised execution

Agents act only within the strategy, limits and permissions you assign. That sentence carries the whole product claim.

Authorised execution is not a promise that the agent is right. It is a promise about the boundary. The agent may still choose a permitted action you would not have chosen. A boundary reduces the set of possible mistakes. It cannot remove them.

This is why the description uses the word authorised rather than automated. Automation says the steps run. Authorisation says who allowed them and within what.

## Monitoring and oversight

Oversight is where the user keeps authority. The description puts three things in view.

- Activity, so you can see what the agent did.
- Positions, so you can see the result.
- Permissions, so you can see what remains allowed.

A system without a clear review point turns delegation into drift. Review is not a formality. It is the step that keeps the mandate current as conditions change.

The user can review, adjust or revoke authority. That is the control. The agent does not own the account.

## How it differs from a bot and from advice

A bot runs a fixed rule. It does the same thing each time the condition appears. That makes it easy to audit and easy to break when the market changes shape.

An agent can choose among steps inside the mandate. It might size an order, split it, or stop when a condition no longer holds. That flexibility is the point, and it is also why the mandate has to be precise.

Advice is different again. Advice tells you what someone thinks you should do. An agent acts. The result lands on your account, not in a report.

| Question | Bot | Agent | Advice |
| --- | --- | --- | --- |
| Who acts | The rule | The agent, within the mandate | You |
| Adapts to conditions | No | Within limits | Not applicable |
| Main risk | The rule stops working | A permitted but unintended action | You follow it badly |

## Why the limits are the product

The strategy is the part that changes. The limits are the part that has to hold.

Useful limits cover size, assets, risk, capital and time. A limit written in a prompt is a suggestion. A limit enforced after the agent makes a choice is a control. The difference is the whole safety story.

Before you use any agent, ask what it can do without a new approval, which limits are enforced rather than requested, what happens when a limit is hit, and how fast a revoke takes effect. If the answer is "the model is careful", keep asking.

## How Olive describes it

Olive presents Agentic Trading as the execution pillar of one system. Connected DeFi supplies access, Quantitative Investments supplies research, and Agentic Trading carries out authorised strategies within your limits. Asset and Portfolio Management provides the oversight view.

The product is in development. The feature page sets out the capabilities, the flow and the control line: agents act within the mandate, and authority stays with the user.

You can read the product detail on the [Agentic Trading page](/features/agentic-trading/), the access layer in the [connected DeFi explainer](/blog/what-is-connected-defi/), and the research side on [Quantitative Investments](/features/quantitative-investments/).

## Frequently asked questions

### What is agentic trading?

Agentic trading means authorised agents act on a strategy within limits you set. You define the objectives, assets, risk and capital limits, and the agent executes only inside that mandate.

### What can an agent do?

It can act within the strategy, limits and permissions you assign. It can analyse market conditions and identify opportunities inside the mandate. It does not act outside it.

### Who keeps authority?

The user. Authority can be reviewed, adjusted or revoked, and the agent does not own the account.

### Is agentic trading financial advice?

No. Advice tells you what someone thinks you should do. An agent acts inside a mandate you define, and the result lands on your account.

### What happens when a limit is hit?

A limit should stop the action or block it before it runs. The exact behaviour depends on the mandate. Ask how a limit is enforced before you rely on it.

## The short version

Agentic trading means authorised agents act on a strategy within limits you set. You define the mandate. They execute inside it. You keep authority to review, adjust or revoke.

Judge the mandate first. If the limits are clear, enforced and easy to stop, the agent has a chance to be useful. If they are only described, it is a demo with your capital attached.
