# Research with EXIT

**Purpose:** help people and software inspect supported blockchain questions with
traceable evidence, explicit time boundaries and a clear account of uncertainty.

## Who uses the result?

| User | Job EXIT is designed to support | Practical value |
|---|---|---|
| Protocol security team | Review operational control and changes in privileged authority. | A source-backed control history rather than scattered screenshots. |
| Auditor or professional researcher | Check a time-bounded control claim and preserve its provenance. | A result that can be inspected and, where permitted, reproduced. |
| Application developer | Retrieve structured research through the authenticated API. | Consistent response semantics for integration. |
| Individual crypto participant | Understand a covered asset's observed authorities and evidence limits. | A more informed investigation without surrendering a wallet seed or signing a trade. |

These are intended uses, not a claim of established customers, paid demand or a
measured reduction in investment losses.

## What can I ask?

Initial questions concern supported **control surfaces and changes**. For example:
which account holds a mint authority, what condition a role requires, and which
observed event changed it. Scope includes the subject, network, question and time.

Initial Solana work and the selected Ethereum reference cases are implementations
of that broader research method. They are not a promise of immediate coverage of
every asset, wallet, application or blockchain.

Questions about price hype, manipulation or motive require additional market,
funding, liquidity and public-claim evidence. They remain a separate measured
research direction; a sequence of transactions does not establish motive by itself.

## Public web experience

The current website provides a question-to-coverage desk, selected recorded cases,
source inspection and public downloads. It can help prepare a local research brief.
Saving a local brief does not submit it to a research team or create a service order.
The website does not currently promise an answer to every free-text question.

No wallet connection or EXIT token is required to inspect public cases.

## Software integration

The free early-access service at [api.exit-protocol.io](https://api.exit-protocol.io/)
reads any Solana token mint through `GET /v0/research/solana/mint?mint=...` (current observed authority fields and supported holder structures) and any Ethereum contract through `GET /v0/research/ethereum/contract?address=...` (proxy slots, the owner() getter as an observation, code presence). The same key opens research records, on-request watches and structured `control_state`, `control_as_of` and `control_change` queries over
three declared recorded Solana reference subjects. It is open 25 October–24 November
2026, 12:38:20 UTC, with quotas and pseudonymous access. Bearer credentials are access secrets, distinct from the EXITP
blockchain token; no token, wallet or payment is required for free access.

The public [script/agent adapters](AGENT-TOOLS.md) call the same API with your own access key; they do not embed a separate research engine.

The [API quick start](docs/API.md) declares supported scope, endpoints, credential
handling, actual dates, quotas and usage conditions. This opening is a bounded
first service, not unlimited capacity or arbitrary research. Paid EXITP redemption
remains a separate future integration.

## Evidence packages and reports

Where permission allows, a result can identify the engine, query, evidence and
evaluation conditions needed for replay. Sharing is restricted to the reviewed
material; clearance for an authored public note does not clear its full source
archive. Private investigations stay private.

## When the requested answer is unavailable

The intended service separates the research result, its billing status and any
follow-up work. The private prototype charges no credit for an unanswered primary
question. A supported, explicit negative observation can still answer a question:
an authority field observed empty differs from a field that was never observed.

Bounded follow-up intake is implemented privately. An execution worker that acquires
additional sources and resolves those requests is a later scoped extension. There
is no promise of unlimited free investigations, a universal answer or a hidden
charge when new evidence eventually appears.

[Research desk](https://exit-protocol.io/#start) · [Status](STATUS.md) · [Technology](TECHNOLOGY.md)

## One free research workflow — 26 October update

The browser interface and API at https://api.exit-protocol.io/ now combine live Solana token authority reads, live Ethereum current-contract reads, recorded historical questions, research records and explicit Solana watch checks. All use one free access account and the same protective quotas. The historical three-subject selector is one tool within this workflow; it does not limit the separate live-address readers.

Free research records preserve a gap and reason; only supported transient Solana provider failures have an explicit re-check path. This is not an autonomous laboratory that guarantees an answer. The paid API Pass prototype remains separate and is not live. On-request watch checks are available now; scheduled automatic alerts remain planned.
