# A usable first release, followed by measured growth

**North Star:** evidence-based blockchain research and monitoring infrastructure.
**First specialization:** control and change analysis.

One master roadmap: the operated first release is followed by measured, continuous development toward evidence-based blockchain research and monitoring infrastructure.

The first release has a finite scope. Subsequent expansion is designed to improve
the breadth, speed and reliability of supported investigations without hiding
what the evidence cannot establish.

![First-service sequence and conditional post-launch growth; conceptual plan, not a delivery measurement](growth-map.svg)

[Open the visual phase-by-phase roadmap](https://exit-protocol.io/ROADMAP.html).

## What comes first

Current chain state can be read at any time; a record anchored on a past day
cannot be produced later. Time-stamped history that cannot be back-filled is the
asset, so scheduled re-reading of control settings and change-only records,
anchored daily even without a change, come first. An anchor shows only that EXIT
held a record by its block time, not that the record is true, known earlier or
complete.

## Current engineering sequence · 29 October

```text
LIVE: recorded research + any-Solana-mint authority read + free API
  → LIVE: durable research records and explicit pull-change checks
  → LIVE: bounded Ethereum current-contract reader
  → LIVE: saved comparisons and answer-to-source navigation
  → LIVE: one-hop authority reads, research graph, Solana and Ethereum watches (bounded)
  → LIVE: public evidence log with a daily Solana anchor (tree size 204 on 29 October); Control Map snapshot (68 of 68 answered) and by-address view
  → LIVE (limited pilot): owned webhook receivers with hourly radar reads
  → LIVE: Python and in-browser verifiers; off-server sentinel (daily at 00:45 UTC; first scheduled run passed 29 October); answers bound to the log on request
  → LIVE: keyless history, cite and verify tools for agents (/tools/); EXIT's own control page (CONTROLS.md)
  → LIVE: the same keys continue in a quota-limited free tier after 24 November (continuation deployed 29 October)
  → SET, NOT YET NEEDED: on a day without new records, the daily job re-anchors the current root
  → NEXT: SPL Governance (Realms) reader (in private testing); LayerZero delegate and verifier reader
  → NEXT: scheduled re-reads with change-only records; reproducible case files (the first is queued for the log)
  → NEXT: token-holder distribution facts in mint answers (waiting on provider access)
  → LATER: pre-registration, public error rate, Control-Change Record, threshold notary, outside witnesses
  → LATER: paid service rights, chain/wallet rehearsal, separate security acceptance
```

Research records, on-request watches (Solana and Ethereum), Ethereum
current-contract reads and the research graph over a key's own answers are live in
the SAME free service, with the same access key and quotas. A bounded
public-HTTPS operator acceptance passed on 26 October for research records, Solana
watches and Ethereum reads; Ethereum watches and the research graph, live since 27
October, were not part of it. Since 27 October a limited
radar pilot reads pending-authority scopes once an hour for watches that have an owned webhook
receiver (one watch service-wide, used by EXIT's own test); it is not continuous
monitoring, and pull checks remain the general monitoring scope. The MCP wrapper
was not checked against routes added after API version 2026-10-26.2.

Public, with no key: the evidence log, a standalone verifier, keyless cite tools
and a browser check running code served by EXIT's site. The daily sentinel, which
re-runs the verifier, runs on GitHub Actions outside EXIT's server but is
controlled by EXIT. The Control Map snapshot answers 68 of 68 deployments (two of
them from a second read on 28 October). The first two private records, radar
events, were admitted at tree size 204 on 29 October. The first-year graph, planning and anomaly
program below remains a measured growth direction.

## Readers the cases showed are missing

| Reader | Case note (28 October) | Exit / stop |
|---|---|---|
| LayerZero OApp delegate and per-path DVN settings (verifiers, confirmations, library default) | Kelp DAO rsETH: one required verifier on the released path for about 381 days; a delegate outside the owner Safe for 235 days. | Reproduces the case's settings at the stated blocks; otherwise revise or stop. |
| SPL Governance (Realms) rules (threshold, wait, veto, voting times, who may propose) and new proposals | BonkDAO: 1% threshold, zero wait, community veto disabled for years; the deciding vote came from a wallet first funded the day before. | Reproduces the case's values and agrees with the program's logs; otherwise revise or stop. |

A reader records configuration and changes, not why a setting was chosen, who
holds a key, or that a loss could have been prevented.

## Evidence discipline additions

Planned unless marked LIVE.

- **Control-Change Record:** one change per record: chain, subject, setting, old
  and new value, bracketing reads or transaction, known_at, evidence hashes, leaf.
- **Pre-registration:** salted hashes of labels, thresholds and held-out windows
  enter the log before a run (a new log record kind); a hidden commitment does not
  by itself show that no other set was committed.
- **Public error rate:** corrections counted against records, map rows and case
  notes published; unfound errors are not counted.
- **Reproducible case files:** every read, provider, slot or block, raw-reply hash
  and a re-read script; past-state reads need archive access. The first case file
  is queued for the log.
- **Keyless cite tools (LIVE, 29 October):** read-only history, cite and verify
  tools for a public record, with its proof and anchor check (/tools/).
- **EXIT's own control page (LIVE, 29 October):** public facts on the EXITP mint,
  notary keys, sentinel job and DNS record; not who holds a key (CONTROLS.md).

## First service and token sequence

| Stage | Output | Exit condition |
|---|---|---|
| Supported research service | Finite control/history/change scope. | Source/time boundaries and required operating results verified; historical operating checks closed before the free service opened. |
| 30-day free API opening | Bounded access, quotas, retries, revocation and recovery; no wallet/payment. | Corrected serving layer accepted, actual public access verified and dates/limits published. Opened 25 October 2026 at 12:38:20 UTC; the initial period ends 24 November at the same UTC time. Continuation deployed 29 October: the same keys then remain valid under the existing quota and lifetime caps, with no fixed end date or automatic payment. |
| Token creation | EXITP created on Jupiter Studio / Meteora DBC, Solana. | Created before API activation; official identity read back and published in TOKEN.md. Future financial and signing actions stay with the project's key holder. |
| Later paid API Pass | Exact usage right, commercial terms and receipt-to-credit integration. | Actual final-configuration chain/wallet rehearsal plus separate money/access security and operational acceptance. No automatic paid conversion. |

Current delivery labels are in [STATUS.md](STATUS.md). Completion of the first
release does not require completion of the four growth quarters below.

The roadmap stages and the whitepaper describe the same direction. Document version numbers identify revisions, not competing product plans. Whitepaper 0.6 predates the evidence log; where they differ, this page and STATUS.md are current.

## After launch: relative quarters

**T0** is 25 October 2026: EXITP was created at 12:14:57 UTC and free service
opened at 12:38:20 UTC. Q1–Q4 are conditional growth windows after this actual
launch date, not prerequisites retroactively imposed on the first release. Q1–Q4 mean successive
three-month planning windows after T0. They are conditional targets, not calendar
guarantees. Each requires capacity, source access and evidence of usefulness.

| Window | Development direction | Measurable exit |
|---|---|---|
| Q1 · months 1–3 | Research workflow, clearer API onboarding, bounded follow-up research and service measurement; change-only re-reads, the two readers. | A fixed supported-question bank shows improved completion or lower user effort/cost; unresolved work and billing remain visible. |
| Q2 · months 4–6 | Temporal research graph, source comparison and selective network/subject expansion; reproducible case files, public error rate. | Added subjects answer the same declared questions with provenance and time controls; added coverage is explicit. |
| Q3 · months 7–9 | Bounded control-setting anomaly research: a setting lowered, a deciding vote from a new wallet, a delegate changed. Trading and price patterns stay a separate later direction. | Labels pre-registered in the log; predeclared event datasets report false alarms, missed events and uncertainty; causal or personal attribution requires separate evidence. |
| Q4 · months 10–12 | Organizational workspaces, integration and permission-scoped reproducible reports; threshold notary, outside witnesses. | Access isolation, recovery, versioned integration and report reproduction pass defined acceptance tests; anchors verify under a published key threshold. |

## Expansion rule

Compare a new method against the existing approach on the same question set.
Continue when it improves supported-answer accuracy, completion, speed or cost
enough to justify its operational burden. Revise or stop a method that does not.
Once pre-registration and a public error rate exist (LATER above), thresholds will
be pre-registered and corrections will count toward the public error rate.

Research planning, monitoring and graph analysis are product capabilities to be
earned with evidence. Neither a larger budget nor a token changes that standard.

Not in this plan: trading or manipulation verdicts, person attribution,
all-network coverage, or paid service before its own acceptance.

## Long-term direction beyond these planning windows

Build a continuously operated research infrastructure connecting validated
multi-network authority, event and observed fund relations to inspectable query
plans, measured monitoring and machine-checkable permitted outputs. Stronger
formal or cryptographic methods require their own bounded task, assumptions,
baseline comparison and benefit. This is a direction, not a dated delivery claim.

Read the [illustrated whitepaper](https://exit-protocol.io/WHITEPAPER-v0.6.html)
and [vision/mechanism guide](VISION.md) for the larger system.
