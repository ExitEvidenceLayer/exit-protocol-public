# Free research API · live quick start

**OPEN:** https://api.exit-protocol.io/  
**Campaign:** 25 October–24 November 2026, **12:38:20 UTC**. One service-wide
30-day period, not a new 30-day trial for every account. No wallet, token purchase,
email, signature, payment or automatic paid conversion.

## 1. Use the research interface

Open the URL, read the supported scope and minimal-metrics notice, and select
**Get free access**. Your bearer key stays in this browser tab’s session storage.
Save it privately if you want to reuse it; losing it does not reset the campaign.
The interface lets you inspect a Solana token mint or Ethereum contract, read research records, manage on-request watches, or choose a recorded subject, question type and UTC cutoffs,
inspect freshness, read evidence-linked answers and see usage. Do not enter secrets.

## 2. Integrate the API

The following uses a private shell variable. Do not use `set -x`, print the key,
put it in a URL, or include it in screenshots and reports. Requires curl and Python 3.
Reading the notices and running enrollment expresses the two indicated consents.

```sh
EXIT_ACCESS_KEY="$(curl --fail --silent --show-error \
  https://api.exit-protocol.io/early-access/enroll \
  -H 'Content-Type: application/json' \
  --data '{"accept_terms":true,"accept_minimal_metrics":true}' \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["access_key"])')"

curl --fail --silent --show-error https://api.exit-protocol.io/v0/subjects \
  -H "Authorization: Bearer $EXIT_ACCESS_KEY"

curl --fail --silent --show-error --get https://api.exit-protocol.io/v0/control_state \
  -H "Authorization: Bearer $EXIT_ACCESS_KEY" \
  -H 'X-EXIT-Request-Id: my-usdc-control-example-1' \
  --data-urlencode 'subject_id=usdc-mint-authorities' \
  --data-urlencode 'valid_at=2026-08-01T00:00:00+00:00' \
  --data-urlencode 'known_at=2026-08-01T23:59:59+00:00'

curl --fail --silent --show-error https://api.exit-protocol.io/v0/early-access/usage \
  -H "Authorization: Bearer $EXIT_ACCESS_KEY"
```

A request ID is scoped to the access account. Reuse it only for the exact same
request; completed cached replay does not consume a second answer. If a response
is uncertain, inspect usage before issuing a different ID. A process failure can
leave a pending record requiring explicit operator resolution; no automatic retry
worker or guaranteed eventual research is offered.

To revoke this access:

```sh
curl --fail --silent --show-error -X POST \
  https://api.exit-protocol.io/early-access/revoke \
  -H "Authorization: Bearer $EXIT_ACCESS_KEY"
unset EXIT_ACCESS_KEY
```

## Live token authority research

`GET /v0/research/solana/mint` accepts a Solana token **mint address**, a bearer key and an `X-EXIT-Request-Id`. It makes a bounded finalized read of current mint/freeze and supported Token-2022 authority fields, then inspects supported holder-account structures. It does not scan all wallet activity or infer who owns a private key.

```sh
curl --fail --silent --show-error --get https://api.exit-protocol.io/v0/research/solana/mint \
  -H "Authorization: Bearer $EXIT_ACCESS_KEY" \
  -H 'X-EXIT-Request-Id: my-token-authority-check-1' \
  --data-urlencode 'mint=5vPz2s8NtkasmVRDz5ySz27V1E8UdSpzqc9xN678jups'
```

Responses use `exit.solana-mint-research/1`, identify the source and finalized slot/time, and preserve evidence and unsupported-field limits. `X-EXIT-Research-State` distinguishes a completed primary answer from an incomplete read. A null observed authority differs from a value the service could not read. The public chain-data provider sees requested mint addresses.

For scripts and agents, use [AGENT-TOOLS.md](../AGENT-TOOLS.md), [exit_client.py](../exit_client.py), [exit_mcp.py](../exit_mcp.py) and [openapi.json](../openapi.json). Requests are not retried automatically. Status, usage and freshness reads do not spend research attempts; transport rate limits still apply.

## Research records (unanswered questions)

When a supported question cannot be answered with evidence, the answer (or the provider-failure refusal) carries
`X-EXIT-Research-Record`, `X-EXIT-Research-Record-State` and `X-EXIT-Research-Gap`. Nothing is charged. Only a supported transient provider failure on the Solana mint route stays `OPEN`, for at most three explicit re-checks at least an hour apart (each one research attempt); a gap without
an executable path is recorded with its reason at once (`REASON_RECORDED`). A verified follow-up result is `RESULT_READY`
and kept for 24 hours; record details are erased after seven days. A recorded reason is not an answer.

```sh
curl --fail --silent --show-error https://api.exit-protocol.io/v0/research/records \
  -H "Authorization: Bearer $EXIT_ACCESS_KEY"
curl --fail --silent --show-error -X POST 'https://api.exit-protocol.io/v0/research/record?id=rr-<24 hex>' \
  -H "Authorization: Bearer $EXIT_ACCESS_KEY" -H 'X-EXIT-Request-Id: my-record-check-1'
```

## Pull-model watches

`POST /v0/research/watch?mint=` watches a Solana token mint (at most three per key; a watch ends after seven days; adding reads
nothing). Nothing is read until you ask: `POST /v0/research/watch?id=watch-<24 hex>` with a request id re-reads it (at most
every six hours, even after a failed attempt; one research attempt) and records only semantic authority or holder changes
with their evidence; an incomplete read records no change. `GET /v0/research/watch` lists watches and changes;
`DELETE /v0/research/watch?id=` stops one. No e-mail, push delivery or continuous monitoring.

## Ethereum own-contract research

`GET /v0/research/ethereum/contract?address=0x…` (bearer + request id) reads, at one provider-reported finalized block and with
at most eleven read-only calls, the proxy implementation and admin slots, the `owner()` getter as an observation and whether
each named address holds code. An empty admin slot is unknown, not "no admin"; what an address may do is not established
without the published source; an address without code or an EIP-7702 delegated account is refused (422) without spending the
answer allowance. Responses use `exit.ethereum-contract-research/1`.

## Recorded reference scope

| Supported subject | Question family |
|---|---|
| `usdc-mint-authorities` | Solana reference control/history/change |
| `pyusd-mint-authorities` | Solana reference control/history/change |
| `pump-fun-program-upgrade-authority` | Solana program upgrade-control reference |

The Pump program subject is research coverage, **not the EXIT token creation venue**.
These are recorded evidence subjects in pinned runtime `7ce62fe02b0f1684be9ecb9e71168423e3040c17`.
Example dates above are historical. No arbitrary-wallet, price, prose-investigation or universal cross-chain service is implied. Current-chain authority reads use the separate mint endpoint above. Public Ethereum historical case notes are separate from the live Ethereum current-contract reader described above.

| Route | Access / inputs |
|---|---|
| `GET /v0/early-access` | Public campaign status, actual dates, caps and subjects |
| `POST /early-access/enroll` | Exact two-boolean JSON above; returns one private key |
| `GET /v0/subjects`, `/v0/contract`, `/v0/freshness`, `/v0/corroboration` | Bearer key; inspect scope and contract |
| `GET /v0/research/solana/mint` | Bearer + request ID + mint; one bounded current authority read |
| `GET /v0/research/ethereum/contract` | Bearer + request ID + address; one bounded finalized-block contract read |
| `GET /v0/research/records`, `GET /v0/research/record?id=` | Bearer; your research records (reading spends no attempt) |
| `POST /v0/research/record?id=` | Bearer + request ID; explicit re-check of an OPEN provider-failure record |
| `GET`, `POST`, `DELETE /v0/research/watch` | Bearer; list / create (`?mint=`) or re-read (`?id=` + request ID) / stop (`?id=`) |
| `GET /v0/control_state`, `/v0/control_as_of` | Bearer + request ID + subject_id, valid_at, known_at |
| `GET /v0/control_change` | Bearer + request ID + subject_id, valid_at_from, valid_at_to, known_at |
| `GET /v0/early-access/usage` | Own usage; credits_charged is 0 |
| `POST /early-access/rotate`, `/early-access/revoke` | Bearer key; empty body; old key ceases to work |
| `POST /early-access/feedback` | Bearer; own request_id, helpful boolean and reason enum shown by UI |

Unsupported routes are not research orders. The paid API Pass routes are not exposed.
The older `alpha.exit-protocol.io` remains separately restricted and unauthenticated
calls return 401; a free key is not a credential for that older alpha.

## Limits and privacy

20 completed answers/account/UTC day; 60 attempts/account/UTC day; 300 attempts
across the service/UTC day; 9,000 attempts/campaign; at most 600 enrolled accounts
and 20 new enrollments/UTC day. These are protective caps, not a guaranteed fair
allocation or Sybil resistance. Return later if capacity is exhausted.

All research is free. Incomplete, failed and unsupported requests do not spend the
completed-answer allowance, although attempt and abuse limits can still apply.
No raw prose, contact details or wallet keys are requested. Optional cached response
copies expire after 24 hours; structured request details and feedback are pruned
after 7 days during healthy maintenance. Pseudonymous account, quota and hashed
replay records persist for campaign/recovery; encrypted operational backups have
separate retention. No deletion-from-all-backups or legal-compliance guarantee.

## Verified real opening

On 25 October, the actual public HTTPS service produced the example query’s answer,
with `X-EXIT-Credits-Charged: 0`. A repeated request returned byte-identical cached
content and only one answered allowance was consumed. Real unit restarts preserved
the campaign start, expiry and access; revocation caused immediate 401 denial.
The full JSON response SHA-256 was
`a69623eb7f77533c97d880a4a90b073d87de31a07394ef97e08fa838b376bbdd`.
These finite checks do not prove human usefulness, unlimited capacity or the absence
of all security defects. [Current status](../STATUS.md) · [Privacy](https://exit-protocol.io/privacy.html).

Research records, pull-model watches and Ethereum own-contract reads are live since 26 October 2026 (05:38:15 and 05:51:30
UTC); they were host-verified at deployment. A bounded public-HTTPS operator acceptance passed on 26 October at 07:49:39 UTC (records, watch lifecycle, Ethereum answer/replay/refusals, 4 attempts / 2 answers / 0 credits, and revocation). They change no quota,
limit or campaign date.

The HTTP transport also has burst/rate limits independent of research allowances: up to 20 burst units per account, refilling at 20 units/minute. A `429` with `Retry-After` is a refusal before route work. Status/usage reads are free of research-attempt charges but still count toward transport limits. Do not automatically retry research after an ambiguous connection failure.
