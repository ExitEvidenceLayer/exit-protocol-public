# EXIT 3.0 scope

**Snapshot: 29 October 2026.**

EXIT 3.0 is the first delivery milestone in EXIT's development program: a finite set of eight technical outcomes. The scope was accepted on 26 October 2026 against pinned internal evidence, with the limits stated below. It does not claim universal coverage, usefulness to people or paying customers. Current status of every surface: [STATUS.md](STATUS.md).

Status words describe public availability on 29 October 2026:

- **LIVE**: usable in the free service at https://api.exit-protocol.io/, within its published quotas. The initial free period ends on 24 November 2026 at 12:38:20 UTC; the same keys continue afterwards in the quota-limited free tier.
- **LIMITED PILOT**: live under limits that exclude most accounts. No outcome below is in this state.
- **NOT LIVE**: built and tested privately; not offered to the public.

## The eight outcomes

**1. Answer a control question with its source, time boundary, later change and uncertainty (R1). LIVE.**
Public form: `control_state`, `control_as_of` and `control_change` for three recorded Solana reference subjects: the USDC and PYUSD mint authorities and the Pump program's upgrade authority.
Limits: acceptance used one fixed PYUSD question, answered by one isolated language-model consumer in three evidence variants and checked by a deterministic grader. This does not measure usefulness to people. Answers are only as recent as the latest recorded evidence cut, which `/v0/freshness` reports.

**2. Inspect which account holds which authority over which object, with evidence (R2). LIVE for the recorded subjects.**
Public form: recorded-subject answers give each authority's controller (or none observed, or unknown) with evidence hashes and acquisition times.
Limits: acceptance used four pinned reference cases (an observed controller, an observed absence, an unobserved period and a transfer) and a composed answer to "who can mint PYUSD"; that composed answer is not a public route. No person or organisation is inferred from an address.

**3. Separate what changed on chain from what EXIT learned or corrected (R3). LIVE for the two time axes.**
Public form: `control_as_of` takes a valid time and a known time as separate inputs.
Limits: correction handling was tested only on labelled synthetic cases. No real correction has been documented. No public route shows correction history.

**4. Know what monitoring covers and how fresh an answer is (R4). LIVE, on demand.**
Public form: each live answer names its finalized slot or block and its own acquisition time; `/v0/freshness` reports evidence coverage.
Limits: recorded evidence cuts are taken by the operator when needed, not on a schedule. Change detection was tested on a fixed replay, including a synthetic A→B→A case. This is not continuous monitoring; repeated reads do not prove that every chain event was captured.

**5. Export an investigation that someone else can reproduce (R5). NOT LIVE.**
A versioned export bundle and a separate replay check exist privately. Of its 1,120 evidence files, 49 EXIT-authored files are declared shareable under CC BY-ND 4.0 and 1,071 provider responses are held. Sharing is not authorized, and a receiver could not replay the export from the shareable files alone. A matching hash proves byte integrity, not that a chain state is true.

**6. A software or agent consumer uses the evidence without raising its certainty (R6). NOT LIVE.**
Acceptance used EXIT's own reference consumer, run separately on an export bundle, including missing, stale and conflicting inputs. The public Python client and MCP adapter were not part of this acceptance.

**7. Ask the same bounded control questions on Solana and one EVM chain, Ethereum (R7). Current state LIVE; history NOT LIVE.**
Acceptance used USDC and PYUSD on Ethereum mainnet, read at fixed blocks for declared surfaces, with Solana and Ethereum identities kept apart. Closest public form: the Ethereum current-contract reader. Recorded Ethereum history is not an API route.
Limits: no real revocation was observed; revocation was tested on synthetic windows only. Other EVM chains and control surfaces are not covered.

**8. A supported, operated service (R8). LIVE.**
Public form: the free API, with published quotas, rate limits and key revocation.
Limits: one main server. The host checks behind this outcome cover one day and one engine source version; a cold-connection latency check failed and stays on record. The current free-serving layer had its own separate checks. No availability level is promised.

At acceptance, no release-blocking correctness, security or data-loss defect was recorded as open. The acceptance evidence was prepared and reviewed inside the project; no outside party has reviewed it, and it is not published.

## Not part of EXIT 3.0

- **Paid API Pass and token-to-credit redemption: NOT LIVE.** A private prototype exists; chain and wallet rehearsal and a separate security acceptance remain open.
- **The EXITP token.** Created on 25 October 2026 at 12:14:57 UTC, the day before the acceptance. Holding it grants no service right.
- **Market integrity and anomaly research.** Planned as a separate later module; not delivered.
- **Human usefulness, a public audience and paying customers.** Not measured.
- **Wider coverage.** Other chains, all wallets, all control surfaces, who holds a key, prediction, risk scores, verdicts and any automated action.
- **Raw provider evidence.** Held, not shared.
- **Live features outside the eight outcomes.** Released before the acceptance: the any-Solana-mint reader, research records, pull watches and the public client. Released after it (see STATUS.md): saved comparisons and answer-to-source views (26 October); one-hop reads, the research graph, Solana path and Ethereum contract watches, webhook receivers with hourly radar reads (LIMITED PILOT), the evidence log and the Control Map (27 October); log bindings, the Control Map by-address view and the in-browser verifier (28 October); keyless evidence tools and the free-tier continuation (29 October).
