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

Enrollment needs a proof of work. `GET /early-access/challenge` returns a signed challenge; solve it
locally: SHA-256 of `challenge:nonce` (decimal nonce) must begin with 16 zero bits. The challenge
expires after 600 seconds, is bound to the network that fetched it and works once. It is not a CAPTCHA
or an identity attestation. `GET /v0/early-access` shows the remaining registration capacity before you
start. Its per-network figures are advisory and are null when your network cannot be identified; enrollment itself is
the authoritative check. A missing proof is refused with `428 ENROLLMENT_PROOF_REQUIRED`, a used challenge with
`409 ENROLLMENT_PROOF_USED`, and a full day or network with `429 ENROLLMENT_CAP_REACHED` or
`ENROLLMENT_NETWORK_LIMIT_REACHED`.

```sh
EXIT_ACCESS_KEY="$(curl --fail --silent --show-error https://api.exit-protocol.io/early-access/challenge \
  | python3 -c '
import hashlib, json, sys
c = json.load(sys.stdin)
n = 0
while int.from_bytes(hashlib.sha256((c["challenge"] + ":" + str(n)).encode()).digest(), "big") >> (256 - int(c["bits"])):
    n += 1
print(json.dumps({"accept_terms": True, "accept_minimal_metrics": True,
                  "proof": {"challenge": c["challenge"], "nonce": str(n)}}))' \
  | curl --fail --silent --show-error https://api.exit-protocol.io/early-access/enroll \
      -H 'Content-Type: application/json' --data-binary @- \
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

`GET /v0/research/solana/mint` accepts a Solana token **mint address**, a bearer key and an `X-EXIT-Request-Id`. It makes one finalized read of at most five read-only RPC calls. Three calls cover current mint/freeze and supported Token-2022 authority fields and the supported holder-account structures. Only when a holder is a multisig or program-owned does the read go one hop behind it: the kind of each signer account, and the owner program with its upgrade authority or the absence of one. Deeper paths are not investigated. It does not scan all wallet activity or infer who owns a private key.

```sh
curl --fail --silent --show-error --get https://api.exit-protocol.io/v0/research/solana/mint \
  -H "Authorization: Bearer $EXIT_ACCESS_KEY" \
  -H 'X-EXIT-Request-Id: my-token-authority-check-1' \
  --data-urlencode 'mint=5vPz2s8NtkasmVRDz5ySz27V1E8UdSpzqc9xN678jups'
```

Responses use `exit.solana-mint-research/2` (a replay of an earlier request returns its stored body, which can be `/1`), identify the source and finalized slot/time, and preserve evidence and unsupported-field limits. `X-EXIT-Research-State` distinguishes a completed primary answer from an incomplete read. A null observed authority differs from a value the service could not read. The public chain-data provider sees requested mint addresses.

For scripts and agents, use [AGENT-TOOLS.md](../AGENT-TOOLS.md), [exit_client.py](../exit_client.py), [exit_mcp.py](../exit_mcp.py) and [openapi.json](../openapi.json). The repository openapi.json is a copy of the live API document, version 2026-10-27.13 (28 October 2026); exit_client.py and exit_mcp.py were not checked against the routes added after version 2026-10-26.2. The live API document at https://api.exit-protocol.io/openapi.json is the reference for every route, parameter and limit. Requests are not retried automatically. Status, usage and freshness reads do not spend research attempts; transport rate limits still apply.

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

`POST /v0/research/watch?mint=` watches a Solana token mint and `POST /v0/research/watch?contract=0x…` an Ethereum mainnet
contract (EIP-55 checked when mixed case; `409 WATCH_CHAIN_NOT_AVAILABLE` when no Ethereum interpreter is configured). At most
three watches per key and 300 in total across both chains; a watch ends after seven days; adding reads nothing. Nothing is read
until you ask: `POST /v0/research/watch?id=watch-<24 hex>` with a request id re-reads it (at most every six hours, even after a
failed attempt; one research attempt) and records only semantic changes with their evidence; an incomplete read records no change.
For a Solana mint these are authority or holder changes and, for answers read one hop deep, changes one hop behind an observed
authority; each change lists the compared keys that differ (`changed`). For an Ethereum contract the comparison covers code
identity, proxy convention, implementation, admin and beacon, the `owner()` getter, the named holders and their account types and,
where the answer reads them, holder paths and AccessControl default-admin members, with the finalized block as the frontier. A
section only one of two answers carries is not compared. `GET /v0/research/watch` lists watches and changes;
`DELETE /v0/research/watch?id=` stops one. No e-mail. The pull re-read is not continuous monitoring; separately, a watch with an
active owned receiver is also read on the radar's own schedule (see the receiver pilot below).

## Ethereum contract research

`GET /v0/research/ethereum/contract?address=0x…` (bearer + request id) reads, at one provider-reported finalized block, the proxy
implementation and admin slots, the `owner()` getter as an observation and whether each named address holds code (at most eleven
read-only calls). For at most two named addresses that hold code, it then asks the multisig interface `getOwners()` and
`getThreshold()`. Last, it asks `supportsInterface` for the AccessControl enumerable interface and, only when it is declared, reads
the `DEFAULT_ADMIN_ROLE` member count and up to four members. That is at most twenty-one read-only calls in all. These are interface
answers at that block, not proof of who holds keys; member accounts, other roles and role admins are not read. An empty admin slot
is unknown, not "no admin"; what an address may do is not established without the published source; an address without code or an
EIP-7702 delegated account is refused (422) without spending the answer allowance. Responses use
`exit.ethereum-contract-research/3` (a replay of an earlier request returns its stored body, which can be `/1` or `/2`).

## Answer views (no new reads)

Three bearer-key routes work over your own cached answers (kept 24 hours). They fetch nothing and spend no research attempt.
Another key's request id answers like an unknown id (`404 ANSWER_NOT_FOUND`).

- `GET /v0/research/evidence?request_id=` (`exit.private-evidence-view/2`): an answer-to-source view with the question, the
  declared scope, the evidence artifacts with their hashes and acquisition times, what was not read, and the limits. The cached
  answer is first re-checked by replaying its evidence.
- `GET /v0/research/compare?a=&b=` (`exit.research-comparison/1`): two answers of the same kind, field by field. Same at both
  observations does not mean unchanged in between.
- `GET /v0/research/graph?request_id=` (one to four, as repeated parameters; `exit.research-graph/1`): one typed graph of who
  holds which declared role, one hop behind a holder where the answers read it. Every answer edge lists the observations it was
  seen at, each with a valid time and a known time. Solana and Ethereum nodes never join. When one of your watches has an active
  receiver, the graph can also carry pending-authority edges from radar reads; their known time is null and their valid time is
  only the slot or block of the last complete read. A pending role edge is not a role grant or proof that the transfer will
  complete.

None of them gives a ranking, risk score, verdict or personal identity. Conflicting answers are listed without choosing a winner.

## Owned webhook receivers (limited pilot)

`/v0/research/webhook` (bearer key) lets an account attach an HTTPS receiver to one of its own watches. In this pilot only
one watch across the whole service can have a receiver. That slot is planned for EXIT's own test run, so other accounts should
not expect alerts yet.

- `POST` with the exact JSON `{"watch_id":"watch-<24 hex>","url":"https://…","accept_external_delivery":true}` registers a
  receiver after it passes a challenge. The signing secret is shown once. With `?id=hook-<24 hex>`, `{"action":"rotate"}`
  returns a new secret with a 300-second overlap, and `{"action":"resume","accept_external_delivery":true}` resumes a paused
  receiver after a new challenge. A failed resume challenge deletes the paused receiver.
- `GET` lists your receivers with up to 100 recent event and delivery entries; `?delivery=` returns one payload part of at most
  16 KiB. Lists never contain a secret.
- `DELETE ?id=` removes a receiver and its queued deliveries.

For a watch with an active receiver, the radar reads the watch's pending-authority scopes once an hour and sends signed
`BASELINE`, `OPENED`, `CHANGED` and `CLOSED` events. On Solana it reads durable nonce accounts, upgrade buffers and Squads v4
proposals; on Ethereum, timelock calls, pending owner, pending admin and default-admin transfers, and Safe configuration.
An absence of events does not mean nothing is pending. Only scopes derived from the watch's verified answer are read, and each
scope states what it does not cover (for example, a buffer staged under another key and then moved). Safe transactions pending
off chain are not read, and neither is what a Squads proposal would do. Reads are limited by a daily budget and a read can be
incomplete. A pending owner, admin or default admin is not a role grant and may never take effect.
Delivery is at least once, not exactly once: deduplicate by `webhook_id`, `event_id` and `part`; an event is complete only after
all its parts arrive. `X-EXIT-Signature` has the form `t=<unix seconds>,v1=<hex>` (two `v1` values during a secret rotation).
Each `v1` is HMAC-SHA256 over `t` + `.` + the exact body, keyed with the hex-decoded secret bytes. The timestamp tolerance is
300 seconds.

The receiver URL must use HTTPS on port 443 with a host name that resolves only to public addresses; redirects are not followed.
A failed delivery is retried after 1 minute, 5 minutes, 30 minutes, 2 hours and 6 hours. Three failed events in a row pause the
receiver until you resume it with a new challenge.

Pilot limits: one watch across the whole service can have a receiver (once it is taken, registration is refused with `429`);
at most two receivers per account; a bounded daily read budget. Refusals charge nothing, and the routes answer `503` when the
radar is not enabled. No wallet, payment or paid credit. No end-to-end delivery from the live radar to any receiver is claimed
yet. Since 28 Oct 04:56 UTC the single slot is used by EXIT's own rehearsal (a PYUSD watch with a test receiver on EXIT's server).

## Evidence log and log bindings

EXIT keeps an append-only Merkle log of its own records. It is public at https://exit-protocol.io/log/ and, with the same bytes
and no key, through the API:

- `GET /v0/log/{file}`: `leaves.json` (every leaf with its known_at), `roots.json` (every root, each after the first with its
  RFC 9162 consistency proof from the previous root), `anchors.json`, `notaries.json`, `proofs.json`, `SPEC.txt`,
  `exit_log_verify.py` (a standalone verifier that uses only the Python standard library) and `SHA256SUMS`.
- `GET /v0/log/proofs/{size}/{leaf}.json`: one `exit.evidence-proof/1` bundle (8-digit leaf index) for each published leaf at
  each anchored size. Public record kinds only; service answers and records held until their own publication are not published
  (`proofs.json` lists which are).

A daily job at 00:30 UTC sends one Solana memo transaction (`EXIT-ROOT-v1`) signed by the server notary key when the log has
grown, at most one per UTC day. The 28 October 00:30 UTC run anchored tree size 200 in slot 462273926 (block time
00:30:07 UTC). The whole log (200 leaves; roots at sizes 66, 68, 134 and 200; anchors at 68, 134 and 200) was then verified
from outside with the published verifier on two Solana providers.

Notary keys are listed in `notaries.json` and, as a separate copy, in [NOTARIES.md](../NOTARIES.md) in this repository. A key is
added or retired only by these steps, in this order: a commit to NOTARIES.md, then an anchored `EXIT-NOTARY-ADD-v1` or `EXIT-NOTARY-RETIRE-v1` memo signed by
a key that is already listed and not retired, plus the updated notaries.json. An anchor signed by a key outside this chain is not
an EXIT anchor; retiring a key does not invalidate the anchors it signed while it was listed. The verifier's notaries.json check
is not an authorization check: compare the signer it prints with NOTARIES.md.

```sh
SOLANA_RPC='https://…'   # any Solana RPC URL
curl --fail --silent --show-error -O https://api.exit-protocol.io/v0/log/exit_log_verify.py
python3 exit_log_verify.py log https://exit-protocol.io/log/ --rpc "$SOLANA_RPC"
python3 exit_log_verify.py proof 'https://api.exit-protocol.io/v0/log/proofs/<size>/<leaf>.json' \
  --rpc "$SOLANA_RPC" --notaries https://api.exit-protocol.io/v0/log/notaries.json
```

A passing check shows that EXIT held a record no later than the anchor's block time. It does not prove that the chain state a
record describes is true, that EXIT knew it earlier, or that nothing was left out.

**Log bindings.** Account-private bindings of watch changes and radar events into the log are switched on as a bounded intake.
A binding is a timestamp commitment, not operator-authored public research: it does not authenticate the content, and admission
does not show that the content is correct. A binding's record and salt go only to your account; the log publishes a salted leaf
and its known_at. Watch rows carry `log_admissions` and radar event metadata carries `log_admission`, as side metadata only; the
bound change and the delivery body never change. Admission states:

- `PENDING_ADMISSION` (every private submission starts here), `DEFERRED_RUN_CAP`, `DEFERRED_DAILY_CAP`
- `ADMITTED_NOT_ANCHORED`, `ADMITTED_ANCHORED`
- `NOT_ADMITTED_LIFETIME_CAP`, `NOT_ADMITTED_EXPIRED`, `PRIVATE_DROP_DISABLED`, `ADMISSION_STATUS_UNAVAILABLE`,
  `INVALID_BINDING`, and `NOT_BOUND` (no binding was made; the `log` field gives the reason, for example `ADMISSION_CAPACITY` or
  `BINDING_TOO_LARGE`)

`ADMITTED_ANCHORED` is EXIT's status note; only an inclusion proof checked against the anchor transaction establishes anchoring.
Limits: 128 files and 1 MiB per run, 8 KiB per file, 128 new private leaves per UTC day and 10,000 in total. A deferral is not
inclusion: writes newer than 600 seconds at the daily scan wait for a later batch, so inclusion in the next daily root is not
guaranteed. Radar events keep a reserved share of each daily intake (the last 16 files), so a watch change can be `NOT_BOUND`
with `ADMISSION_CAPACITY` while radar events are still bound. A private submission not admitted within seven days is discarded.
Roots made after the 28 October 2026 00:49 UTC release carry `ordering=append-sequence/2`: a late stated known_at does not backdate insertion or prove earlier knowledge. As of 28 October 2026 no private binding has been
admitted; inclusion in the next nightly root is not guaranteed (files written less than 10 minutes before the scan wait for a later run).

The binding arrives in the `log` field (`exit.log-binding/1`) of a watch change or radar event. Save it: the log keeps no record
or salt after admission, and your account's copy is deleted with the watch or radar data (see Limits and privacy).

Check a binding you hold (the `{record, salt}` JSON, as a file or URL):

```sh
python3 exit_log_verify.py leaf binding.json --log https://exit-protocol.io/log/ --rpc "$SOLANA_RPC"
```

`leaf` recomputes the leaf, finds it in the published leaves, checks the audit path against the first anchored root that contains
it and, with `--rpc`, that anchor's transaction and signer. Add `--event EVENT` with the full radar event (all parts) to check the
event against the binding. Without `--event`, a pass proves only that the record is included, not that it matches an event shown
separately. A watch change made by radar polling (`log_binding_scope=RADAR_EVENT`) binds the complete CHANGED event, not the watch
row; check it with `--event`. Research answers are not bound to the log yet. The published verifier already accepts `leaf --answer BODY`, but it has nothing
to check until a later release binds answers. Public leaves expose timing and activity; a hash does not prove possession of the raw evidence bytes.

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
| `GET /v0/early-access` | Public campaign status, actual dates, caps and subjects, and remaining registration capacity |
| `GET /early-access/challenge` | Public; one signed proof-of-work challenge (16 bits, 600 seconds, network-bound, one use) |
| `POST /early-access/enroll` | `accept_terms`, `accept_minimal_metrics` and `proof` (`challenge`, `nonce`) as above; returns one private key |
| `GET /v0/subjects`, `/v0/contract`, `/v0/freshness`, `/v0/corroboration` | Bearer key; inspect scope and contract |
| `GET /v0/research/solana/mint` | Bearer + request ID + mint; one bounded current authority read |
| `GET /v0/research/ethereum/contract` | Bearer + request ID + address; one bounded finalized-block contract read |
| `GET /v0/research/records`, `GET /v0/research/record?id=` | Bearer; your research records (reading spends no attempt) |
| `POST /v0/research/record?id=` | Bearer + request ID; explicit re-check of an OPEN provider-failure record |
| `GET`, `POST`, `DELETE /v0/research/watch` | Bearer; list / create (`?mint=` or `?contract=`) or re-read (`?id=` + request ID) / stop (`?id=`) |
| `GET /v0/research/evidence`, `/v0/research/compare`, `/v0/research/graph` | Bearer; `request_id` / `a` and `b` / one to four `request_id`; views of your own cached answers (no attempt spent) |
| `GET`, `POST`, `DELETE /v0/research/webhook` | Bearer; list (`?delivery=` for one part) / register, or rotate and resume (`?id=`) / delete (`?id=`); limited pilot |
| `GET /v0/control_state`, `/v0/control_as_of` | Bearer + request ID + subject_id, valid_at, known_at |
| `GET /v0/control_change` | Bearer + request ID + subject_id, valid_at_from, valid_at_to, known_at |
| `GET /v0/early-access/usage` | Own usage; credits_charged is 0 |
| `POST /early-access/rotate`, `/early-access/revoke` | Bearer key; empty body; old key ceases to work |
| `POST /early-access/feedback` | Bearer; own request_id, helpful boolean and reason enum shown by UI |
| `GET /v0/log/{file}`, `GET /v0/log/proofs/{size}/{leaf}.json` | Public, no key; evidence-log files and proof bundles |

Unsupported routes are not research orders. The paid API Pass routes are not exposed.
The older `alpha.exit-protocol.io` remains separately restricted and unauthenticated
calls return 401; a free key is not a credential for that older alpha.

## Limits and privacy

20 completed answers/account/UTC day; 60 attempts/account/UTC day; 300 attempts
across the service/UTC day; 9,000 attempts/campaign; at most 600 enrolled accounts,
40 new keys/UTC day and 2 new keys per network/UTC day (shared networks share this
limit; it does not disable an existing key or its quota). These are protective caps,
not a guaranteed fair allocation or Sybil resistance. Return later if capacity is exhausted.

All research is free. Incomplete, failed and unsupported requests do not spend the
completed-answer allowance, although attempt and abuse limits can still apply.
No raw prose, contact details or wallet keys are requested (the limited alert pilot stores a receiver's HTTPS address and signing
secret while its watch is active). Optional cached response
copies expire after 24 hours; structured request details and feedback are pruned
after 7 days during healthy maintenance. Webhook receivers, events and deliveries are
kept for up to 7 days and end sooner on watch, account or campaign expiry or deletion.
A log binding's record and salt go only to the account; the public log shows a salted
leaf and its known_at. Public leaves are permanent (the log is append-only): the 7-day
deletion and key revocation do not remove them. Leaf count and known_at reveal activity
volume and timing, and salting does not guarantee anonymity against correlation. The
service makes these bindings itself; the API document lists no option to turn them off.
Pseudonymous account, quota and hashed replay records persist for campaign/recovery;
encrypted operational backups and deploy-time copies of service records have separate
retention. No deletion-from-all-backups or legal-compliance guarantee.

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
limit or campaign date. Later changes (deeper reads, Ethereum contract watches, the receiver pilot, the evidence log and log
bindings) are listed in the [changelog](../CHANGELOG.md).

The HTTP transport also has burst/rate limits independent of research allowances: up to 20 burst units per account, refilling at 20 units/minute. A `429` with `Retry-After` is a refusal before route work. Status/usage reads are free of research-attempt charges but still count toward transport limits. Do not automatically retry research after an ambiguous connection failure.
