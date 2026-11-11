# One project, several document roles

Delivery snapshot: 5 November 2026 (the change-checks, radar and access texts were corrected on 11 November 2026; see CHANGELOG.md). One accepted direction, not competing product plans.

- The master roadmap orders outcomes and dependencies. Q1-Q4 are three-month windows from 25 October 2026, not delivery guarantees.
- The whitepaper explains mechanisms and limits. Edition 0.7 is the current aligned edition; earlier editions remain historical.
- STATUS.md and CHANGELOG.md retain dated release records. A staged or locally tested candidate is not a live feature.
- VISION.md describes the longer direction. Wider graphs, planning and organization workflows remain conditional growth.
- DELIVERY.json is the shared machine-readable snapshot in this repository and on the official site. It is not an automatic live feed.

## What the user can rely on at this snapshot

| Capability | State | Boundary |
|---|---|---|
| Supported research | LIVE / BOUNDED | Solana mint and SPL Governance reads; Ethereum contract, issuer-freeze and LayerZero reads. Explicit parsers, source availability and per-route limits apply. |
| Continuing research | LIVE / BOUNDED | Research records, saved comparisons and answer-to-source navigation. Unanswered requests retain a gap or reason; there is no general automatic research worker. |
| Research graph | LIVE / BOUNDED | Joins one to four of an account's own cached answers. Typed relations and source conflicts remain visible; this is not a global multi-chain graph. |
| Change checks | LIVE / ON REQUEST | Solana and Ethereum watches re-read on request under published quotas; a watch with a registered receiver (at most one across the whole service) is also read hourly (see radar). This is not general continuous monitoring. |
| Radar and webhook delivery | LIMITED PILOT | Hourly reads for one watched subject across the whole service. EXIT's own end-to-end test used the slot from 28 October 2026; on 11 November 2026 the slot was free (no watch had a receiver). Broader scheduled alerting is not delivered. |
| Public evidence log | PUBLIC / SOLANA-ANCHORED | Append-only record commitments, daily anchor job and public verifiers. A checked inclusion proof establishes the commitment's presence by the anchor time, not the truth, completeness or earlier knowledge of its content. |
| Paid API Pass | PRIVATE PROTOTYPE / NOT LIVE | Receipt-to-credit production integration still requires its actual chain/wallet rehearsal and separate security and operating acceptance. Holding EXITP alone does not currently grant credits. |

The initial period runs from 25 October 2026, 12:38:20 UTC, to 24 November 2026 at the same time. Existing keys then continue in the same quota-limited free service without a fixed end date or automatic payment. Daily quotas reset at 00:00 UTC each day. The service-wide lifetime totals of research attempts and of accounts (published at https://api.exit-protocol.io/v0/early-access) are never reset: once the attempt total is used up, requests that need a research attempt are refused, and once the account total is reached, no new key is issued. A reduction of the offer or an announced end of free access requires at least 30 days' notice; reaching a lifetime total has no notice period.

Technical tests and operated routes do not establish independent human usefulness or commercial demand. These outcomes remain unmeasured unless a dated result states otherwise.

## Why this work is useful

Explorers, monitoring and simulation tools already provide important parts of blockchain research. EXIT's intended value is the continuing workflow: a bounded question, identified evidence, distinct chain and knowledge times, later changes, corrections and inspectable limits. The two-time model is an established data technique, not an invention or a claim of unique market coverage. Repeated task completion, user effort, unsupported conclusions, reproducibility and cost must establish the benefit.

The next engineering work preserves data continuity, source availability and the reliability of the supported research workflow. A larger number of features or tests is not human-usefulness evidence. No paid API Pass, reward budget, token transfer or new network is activated by these documents.
