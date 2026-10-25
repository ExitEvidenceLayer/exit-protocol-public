# Free research API · live quick start

**OPEN:** https://api.exit-protocol.io/  
**Campaign:** 25 October–24 November 2026, **12:38:20 UTC**. One service-wide
30-day period, not a new 30-day trial for every account. No wallet, token purchase,
email, signature, payment or automatic paid conversion.

## 1. Use the research interface

Open the URL, read the supported scope and minimal-metrics notice, and select
**Get free access**. Your bearer key stays in this browser tab’s session storage.
Save it privately if you want to reuse it; losing it does not reset the campaign.
The interface lets you choose a supported subject, question type and UTC cutoffs,
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

## Declared first-free scope

| Supported subject | Question family |
|---|---|
| `usdc-mint-authorities` | Solana reference control/history/change |
| `pyusd-mint-authorities` | Solana reference control/history/change |
| `pump-fun-program-upgrade-authority` | Solana program upgrade-control reference |

The Pump program subject is research coverage, **not the EXIT token creation venue**.
These are recorded evidence subjects in pinned runtime `7ce62fe02b0f1684be9ecb9e71168423e3040c17`.
Example dates above are historical. No arbitrary-wallet, price, prose-investigation,
current-chain or universal cross-chain service is implied. Public Ethereum case
notes are separate from this first free API scope.

| Route | Access / inputs |
|---|---|
| `GET /v0/early-access` | Public campaign status, actual dates, caps and subjects |
| `POST /early-access/enroll` | Exact two-boolean JSON above; returns one private key |
| `GET /v0/subjects`, `/v0/contract`, `/v0/freshness`, `/v0/corroboration` | Bearer key; inspect scope and contract |
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
