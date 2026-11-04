# Public documentation changelog

## 4 November 2026 · contract reader /5, six Control Map setting names, Arbitrum case on the homepage, claims check v3

- 06:30 UTC: the nightly Control Map comparison can compare six more setting names of the
  [Control-Change Record list](control-change/control-change-settings.json) (56 names; the list was updated here at 04:47 UTC): the
  ZeppelinOS proxy implementation and admin slots, and masterMinter(), pauser(), blacklister() and rescuer() of Circle's FiatToken.
  The contract reader reads these four getters only when a token's proxy and implementation code match the reviewed USDC pair byte
  for byte; it reads the ZeppelinOS slots on every Ethereum row, and an empty slot is compared as the zero address. The 4 November
  23:20 UTC run is expected to compare no Ethereum row, because the reader moved to /5 that day (READER_OR_SOURCE_CHANGED). From the
  first night that compares two /5 reads, expected on 5 November 23:20 UTC, each compared Ethereum row other than row 4 is expected
  to count two more compared settings than it would without the six names, and row 4 (USDC on Ethereum) six more when both of its
  reads match the reviewed pair (two otherwise): settings compared, not changes found.
- 01:35 UTC: the Ethereum contract reader answers with schema exit.ethereum-contract-research/5: a reverted owner() or issuer-getter
  call is recorded as CALL_REVERTED (what the call did; it names no holder), an invalid-opcode failure of those calls (two provider
  wordings) as CALL_FAILED_INVALID_OPCODE, and a provider error that is neither makes the read incomplete; the issuer roles for one
  reviewed issuer runtime pair (USDC); a designation for every code read, EIP-7702 delegations included. Same budget: at most 26
  read-only calls within 60 seconds. A replay of an earlier request returns its stored /1 to /4 body unchanged. API description
  2026-11-04.1; [openapi.json](openapi.json) updated. Two of its sentences are to be corrected in the next description version:
  the route summary still says twenty-one calls, and the 200 response text says "a reverted getter" where only owner() and the four
  issuer getters are meant.
- 01:43 UTC: the sentinel recorded DOCS_DRIFT: this repository's API description was still 2026-11-02.2 while the service already
  served 2026-11-04.1 ([sentinel result](https://github.com/ExitEvidenceLayer/exit-protocol-public/blob/2c6265ada311edb7ddd32854898b9e00f467c67f/results/2026-11-04.json)); the repository copy followed at 02:20:40 UTC. To avoid a repeat, EXIT
  intends to commit a changed API description here before switching it live; the sentinel's daily api_description_version
  check records a difference that is present when it runs.
- Not recorded here before: on 30 October 04:31 UTC the contract reader gained schema /4, a native-owner read for one reviewed
  smart-account runtime pair (ERC1967Proxy with SingleOwnerMSCA: getNativeOwner() compared with its storage slot), which raised the
  budget to 26 calls / 60 s. [STATUS.md](STATUS.md) and [docs/API.md](docs/API.md) still said "at most twenty-one read-only calls"
  and docs/API.md dated /4 to 1 November (the date of the clone recognition, entry below); both now describe /4 and /5 with their dates.
- 01:11 UTC: the homepage coverage table links [the Arbitrum Security Council case note](cases/arbitrum-security-council-2026-10-30.md).
- [tools/claims_check.py](tools/claims_check.py) v3: the sitemap rule accounts for every entry. A page date that cannot be read is
  a mismatch instead of a skip (one HEAD request per page), an entry without a date must name the check that covers it (only
  /log/), and the output states what was checked. Before, an undated or unreadable entry was skipped and the rule still passed.
- [ROADMAP.md](ROADMAP.md): the issuer-role, revert and code-designation item moved from NEXT to LIVE.
- [ROADMAP.md](ROADMAP.md): the NEXT and LATER lines added on 3 November (evening) are withdrawn until a roadmap decision is made:
  a declared watch list of upgrade-path contracts on Ethereum, multi-hop control paths (Safe modules and guards, role sets rebuilt
  from events) and control edges on a second network. The order of the other items is unchanged.
- [STATUS.md](STATUS.md): the evidence-log row points to https://exit-protocol.io/log/anchors.json for every anchor (it listed
  only the first four) and says what the browser check's PARTLY CHECKED result means; the Control Map row says how rows 70-72
  came to be listed and which six setting names the nightly comparison can compare from 06:30 UTC; the 3 November core release
  entry says that the Control Map's next run compared none of the 68 rows it had read before.

## 3 November 2026 (evening) · proposals gap records, a known Control Map labelling issue, founder holding, Arbitrum case

- 13:50 UTC: when the provider refuses a read for /v0/research/solana/governance/proposals, the research record now names the gap
  PROVIDER_UNAVAILABLE, as it already did for /v0/research/solana/governance. Before, such a refusal was recorded as METHOD ("the method
  cannot answer"), which was wrong. Records written before keep their gap; nothing else changed. Health checks passed after the release.
- STATUS known issue: 21 Ethereum rows of the Control Map show `owner(): NOT_OBSERVED (RPC error; cause not established)`. On those
  contracts owner() reverts: re-read on 3 November from two providers, at block 26,334,869 and at each row's snapshot block, all 21
  reverted at both. The label is corrected in the next contract-reader release; the rows' other facts are not affected.
- [TOKEN.md](TOKEN.md) and [TRANSPARENCY.md](TRANSPARENCY.md): the founder holding, dated 3 November (wallet, 14,151,336.226592 EXITP,
  four purchases, no sales, no lock), replacing "to be disclosed".
- [cases/arbitrum-security-council-2026-10-30.md](cases/arbitrum-security-council-2026-10-30.md): the Arbitrum Security Council case,
  in the same format as the other case notes.
- Control Map: from the 3 November 23:20 UTC re-read the nightly run covers 72 rows (row 69 is EXITP, listed as EXIT's
  own token; rows 70-72 are Raydium (RAY), The Black Bull (ANSEM) and STONK, listed as declared rows).
- [ROADMAP.md](ROADMAP.md): synced with the internal plan of 3 November.

## 3 November 2026 (later) · Q1 result in two columns, sentinel v4, founder wallet report, roadmap page

- Q1 result: the same recorded answers are now graded against both bank versions. Against bank v1, published before the run (2 Nov 06:57 UTC), 21 of 36 questions met their expectation; against bank v1.1, in which 11 expectations were corrected after a first run had been seen, 31 of 36; of the 25 questions never revised, 20. The earlier sentence "31 of 36 questions met their pre-registered expectation" was wrong and is replaced in STATUS ([docs/Q1-RESULT.md](docs/Q1-RESULT.md), per-question table and [two-column file](docs/q1-two-column-20261103T000505Z.json)).
- [docs/ACCURACY.md](docs/ACCURACY.md): the 2 Nov v6 run was pre-registered twice (a first attempt was voided by a local network outage and a classifier fix followed); stated, with what "pre-registered" then means.
- Sentinel workflow v4: only a log integrity failure fails the job; DOCS_DRIFT (a public text differs from the live service) is a warning annotation on a passing run and still recorded as its own status.
- [docs/FOUNDER-WALLET.md](docs/FOUNDER-WALLET.md): the first monthly report on the founder wallet's EXITP — 14,151,336.226592 EXITP, four purchases, no sales or outgoing transfers; the pool-creator role (a Jupiter Studio proxy recording the founder wallet) with 3.661513 USDC of creator fees not yet claimed and no claim so far.
- Website: the roadmap page's acceptance line for the Solana mint route and its dates were brought up to date (the authenticated acceptance read was recorded on 2 November).

## 3 November 2026 · wording correction

- The 3 Nov second-provider sentence (STATUS and the 00:05 entry below) mixed row and fact counts: the control and getter facts it listed were not disagreements but facts without a primary observation; reworded with the fact counts, and the second providers are named.
## 3 November 2026 (04:50–04:57 UTC) · sentinel result states, Solana read pause

- About the evidence-log sentinel result of 3 Nov 01:44 UTC (FAILED): every log check passed — the log verified on chain, the newest anchor and the newest daily run were fresh and the run outcome was valid. The only false check was public_claims_match_live: the sitemap date for /log/ was behind the page, which the daily anchor run rewrites at 00:30 UTC. The sitemap entry for /log/ now declares a daily change instead of a fixed date (02:46 UTC).
- 04:57: sentinel workflow v3 (result format exit.log-sentinel/3). It reports three states: OK, DOCS_DRIFT (the log verified and is fresh, but a public text differs from the live service) and FAILED (a log check failed); the job still fails visibly on DOCS_DRIFT. The heartbeat outcome HEARTBEAT_ANCHORED counts as a valid daily run. Anchor transactions are read from api.mainnet-beta.solana.com, then from api.mainnet.solana.com (another public endpoint of the official cluster, same operator), then from solana-rpc.publicnode.com (it keeps only about two days of transactions); every attempt is recorded. Freshness is matched by anchor signature, not tree size.
- 04:50: chained Solana reads pause 0.5 s before a read that requires the provider to have reached a given slot; no extra request, the published call limits are unchanged. On the host, the two Control Map mints whose answers need all five reads went from 7 of 8 and 5 of 8 answered to 8 of 8 each.
## 3 November 2026 (later) · core release, usage fields, consent record, proposals route fixed

- 03:20: core release bb49875c applied (after the Q1 baseline run; every baseline answer that names an engine names 24da5740).
- 03:43: GET /v0/early-access/usage reports limits, answers_remaining, attempts_remaining and resets_at_utc (exit.free-usage/2).
- 03:53: console continuation wording; 04:03: recorded consent (hash of the served console and time, no content).
- 04:12: /v0/research/solana/governance/proposals reads the official Solana endpoint (the shared provider refused its list call); bounded same-id re-send of chained Solana reads.
- STATUS: the 3 November known issue is marked resolved; the core sentence states when it was applied; the Q1 numbers are explained.

## 3 November 2026 · a nightly second opinion, the nightly re-read and an off-host state copy

- 00:05: first scheduled second-provider check — 12 rows: 9 agree on every fact both sources observed; 3 differ only in token supply within the read window (3 facts); 7 further facts (5 control, 2 getter) had no primary observation and were not compared; 74 facts agree; the 12 records were admitted at the 00:30 UTC anchor (tree size 370); STATUS.md row "Control Map second-provider check".
- 00:35: the evidence log, Control Map state and unit files are copied daily off the host as a verified archive with a restore drill; key material, ledgers and access records are excluded by rule.
- 2 Nov 23:20 UTC nightly Control Map re-read (worker V12, up to three attempts with backoff): 68 rows, 67 answered, 1 not answered (RPC_RESPONSE_INVALID); 2 retries, 0 rows recovered after a retry. Every row has a record in the evidence log (a read without an answer is recorded with its code).

## 2 November 2026 (later) · the agent tools caught up with the API; one status row corrected

- 13:04: the script client and MCP wrapper gained the twelve routes added since API version 2026-10-26.2 (freeze status, governance realm and
  proposals, LayerZero pathway and peer, research graph, compare, evidence view, log binding, contract watches, webhook list and delete):
  30 MCP tools, server 1.3.0, [AGENT-TOOLS.md](AGENT-TOOLS.md). Checked against a loopback stub of the API description, not against the live
  service with a key; no autonomous worker, no engine source. ROADMAP.md: the sentence saying the wrapper was not checked against the newer
  routes is replaced by that checked fact.
- Correction (documentation): STATUS.md's "Public script/agent client" row said the repository copy of the API description was version
  2026-11-02.1; the copy and the live document have both been 2026-11-02.2 since 2 November (found by byte comparison). The row now says so.
- 13:12: [tools/claims_check.py](tools/claims_check.py) gained a fifth check, `status_client_row_version`: the status row about the API copy
  must name the version the repository copy carries, and, when exit_mcp.py is in the checkout, the row's tool count and server version must
  match that file. The row above had been a version behind and no check compared the sentence with the copy; now one does.
- 13:22: correction (documentation): [docs/API.md](docs/API.md) said the repository copy of the API description was version 2026-11-01.3 and
  that the client and MCP were not checked against the newer routes; both sentences were behind (found by a sweep of every public text for
  version sentences after the status-row correction). The paragraph now names 2026-11-02.2 and the loopback-stub check.
- 16:51: correction (documentation): ROADMAP.md and VISION.md still described three delivered things as pending — the public error rate (live since
  29 October) as LATER, the BonkDAO and Kelp DAO case-file records as queued (they entered the log at the 2 November 00:30 UTC anchor, tree size 274),
  and the issuer-freeze read without PYUSD (live since 2 November 01:50:42 UTC). The sentences now state the delivered facts.
- 17:10: correction (documentation), from a check of every retention statement against the service code: docs/API.md named only the mint
  and contract routes for answer bindings, while all seven live read routes bind on request; it now lists them. It also now says what
  revocation removes and what expires on its normal window, describes the account record exactly (a sequential account number and a
  hash of the key) and lists the aggregate minimal metrics. STATUS.md no longer calls research records durable without saying that
  their route, subject and scope are erased after 7 days.
- 17:45: privacy (service operation and documentation). A check of every retention statement found that the reverse proxy's error lines
  carried the client's address and the request path into the server's system logs, which kept them longer than the published 7-day window.
  Since today those lines carry neither, the system journal keeps at most about 7 days, and the copies in the system log files were removed.
  docs/API.md and the privacy page now state this and correct the backup sentence: no scheduled backup of the account records exists.

## 1 November 2026 · freeze reads, scheduled re-reads, proposals, peers, reproducible case files

- 10:43: `GET /v0/research/ethereum/freeze` went live: whether one Ethereum address is on the USDT or USDC issuer blacklist at one
  finalized block, with its balances (six read-only calls; the tokens' own getters; a reverted getter is NOT_OBSERVED, never
  "not frozen"), with the same key, quotas and opt-in log binding (OpenAPI 2026-11-01.1, [openapi.json](openapi.json)). A freeze is
  not a recovery and the time of a freeze is not read.
- 12:26: the Control Map daily re-read started as a standing job: every row re-read once a day, a Control-Change Record only when
  a setting changed, the same settings re-anchored as consecutive daily reads (first scheduled run 23:20 UTC; a page for the daily
  reads follows once the first runs are anchored).
- 12:33: radar kind R-FREEZE: for Ethereum watches the subject and its named holders are read against the two blacklists at each
  research block; a listing is one open object per address and token, closed when a later read answers false. Radar kind
  R-GOV-PROPOSAL: for Solana governance watches, a newly listed or newly closed proposal is a signal.
- 12:47: `GET /v0/research/solana/governance/proposals` went live: the proposals of one supported SPL Governance V2 account counted
  by state (at most 600 listed) and the open ones decoded (at most 100; options with raw weights, deny/abstain/veto weights, times,
  threshold, name and link), three or four read-only calls (OpenAPI 2026-11-01.2, 12:51). Vote records, voters, transaction
  contents and outcomes are not read.
- 13:02: `GET /v0/research/ethereum/layerzero/peer` went live: which peer one LayerZero V2 OApp holds for one remote endpoint id
  at one finalized block (four read-only calls; a zero-padded 20-byte value is also given as an address, a reverted getter is
  NOT_OBSERVED, never "unset"; OpenAPI 2026-11-01.3). The Control-Change setting layerzero-v2:oapp.peers is now readable.
- 13:08: reproducible case files on the site: `case-files/bonkdao-2026-07-06-recorded-v1/` (20 of 21 claims recomputed from the
  retained replies and matched; one transaction not retained) and `case-files/kelpdao-rseth-2026-04-18-recorded-v1/` (20 of 23;
  two explorer-read times and one archive wrapper not recomputable). Their case_note records were queued for the daily anchor at
  00:30 on 2 November.
- Public tools hardened after an outside review: the evidence client reports publisher identity as a separate result (pass
  trusted notary keys from outside the log to verify the publisher); the sentinel verifies without write permission from one
  snapshot of the log documents, judges freshness on the anchor it confirmed and checks the last run's outcome; the MCP server and
  the Control-Change checker refuse oversized or deeply nested input instead of failing.
- Repository: public-surface inventory adds the API's `openapi.json`; the engine's creation read requests transaction version 1.
- 16:45: fix to the proposals route released. Its first keyed read (16:14) answered 503 `RPC_BUDGET_EXHAUSTED`: the shared Solana
  transport admitted three calls of three methods and the route needs a fourth method. The route now runs on its own session (four
  calls, `getProgramAccounts` admitted; body identical to the shared transport except the gate line, asserted by a test) and its
  acquisition is tested through the real transport with a stub connection. Lesson recorded: a route is ready only after a real
  read through the real transport, not after fixture replays.
- 18:56: the Ethereum contract reader recognises the canonical EIP-1167 minimal-proxy clone from the code it already reads: the
  implementation is taken from the clone's PUSH20, admin is reported as not applicable, no extra call; variants stay NOT_OBSERVED.
  Policy `ethereum-finalized-admin-surface-native-owner/2`; stored /1 answers replay unchanged. Released after a fresh benchmark
  sample over the new bytes showed no regression (benchmark notes under `docs/`).
- 20:41: the Solana mint reader interprets two Token-2022 authorities it previously only disclosed by name: the pause authority (can pause and
  resume transfers, mints and burns) and the scaled-UI-amount authority (can change the displayed multiplier). They appear as controls with
  their meaning; the state facts behind them (paused, multiplier, pending multiplier and its effective time) are reported, never followed as
  authorities. Policy `solana-finalized-mint-pair-hop/2`; stored /1 answers replay unchanged; a pre-release benchmark over fresh live mints
  matched an independent decoder on every compared fact. Engine core commit 24da5740.
- 2 November, 01:50: the freeze read covers PYUSD as well as USDT and USDC (eight read-only calls; policy `ethereum-finalized-issuer-freeze/2`;
  PYUSD's `isFrozen(address)` getter, with the PaxosTokenV2 transfer semantics stated from the published source). The radar's R-FREEZE
  scope reads the same three tokens. Stored `/1` answers replay unchanged. OpenAPI 2026-11-02.1.

## 29 October 2026 · quota-limited free continuity and verifier correction

- 12:28: `GET /v0/research/ethereum/layerzero` went live: one LayerZero V2 OApp pathway on Ethereum (OApp, remote endpoint id,
  direction): delegate, message library, raw, default and effective verifier configuration, at most eleven read-only calls, with
  the same key, quotas and opt-in log binding (OpenAPI 2026-10-29.3, [openapi.json](openapi.json)).
- [Kelp DAO case note](cases/kelpdao-rseth-2026-04-18.md): correction of the time the receiving address was blocked until
  (19 April 18:23:11, 24 hours after the block, not 00:10:55); dated correction section added. Counted in CORRECTIONS.md.
- 11:11 to 11:13: `GET /v0/research/solana/governance` went live: one supported SPL Governance V2 account and its paired realm
  and configuration, at most three read-only calls, with the same key, quotas and opt-in log binding (OpenAPI 2026-10-29.2). It reads configuration only: no proposals, votes, holdings or plugin logic.
- [CONTROL-CHANGE-RECORD.md](CONTROL-CHANGE-RECORD.md): an open format (`exit.control-change/1`) for one control-setting change,
  with 50 stable setting names (49 read by EXIT today, 1 reserved), a standard-library checker with source-bound value ranges and
  three synthetic examples in `control-change/`; meanings checked against program sources, ranges against the readers' decoders. A record enters the evidence log as an ordinary record. No records in
  this format are published yet.
- [CORRECTIONS.md](CORRECTIONS.md): every correction of a published fact in log records, Control Map rows and case notes, with
  the count per kind of output: 0 in 200 records with public proof bundles, 0 in 68 rows, 7 corrections in 6 case outputs; all
  13 correction notes are listed with whether each corrected a fact. Updated monthly.
- [LICENSE-CODE](LICENSE-CODE): the log verifiers, the evidence-log and Control-Change Record formats and the `control-change/`
  folder are now under the MIT License. Documentation stays under CC BY-ND 4.0.
- A versioned continuation is deployed before the initial 24 November boundary. Existing keys continue under the same daily, enrollment and lifetime capacity caps; no account, revocation, usage counter or profile is reset. No automatic payment, wallet or token requirement is introduced. A later announced end requires at least 30 days notice.
- First-period watches/receivers and binding lookups keep their original expiry; new-period ones keep the existing seven-day limit. Request-body and query-detail retention remain 24 hours and seven days.
- Console status, terms, privacy and OpenAPI 2026-10-29.1 describe the same service contract. HTML structure and styles are unchanged.
- Installed daily assurance now passes 26 modules / 703 executions; continuation admission/notice guards also passed four deliberate mutation checks. Finite tests are not a blanket security claim.
- Keyless evidence tools: public-log history, citation and finalized-anchor checks (`exit_history`, `exit_cite`, `exit_verify`) in the
  existing stdio MCP interface. They reuse the published pinned verifier; fixed-origin transport, no research key, no arbitrary URL
  and no automatic retry. The source bundle is at https://exit-protocol.io/tools/.
- 00:30:00: the daily run anchored tree size 204. Its new records include the 28 October re-reads of the USDC and USDG Solana rows.
  The sentinel's first scheduled run (started by GitHub at 01:37) passed.
- 09:42:53: the Control Map shows the USDC and USDG Solana rows from those re-reads (records anchored at tree size 204): 68 of 68
  deployments answered. These two rows have no second-source read yet. The by-address view was rebuilt from the same file.
- [CONTROLS.md](CONTROLS.md): EXIT's own controls (notary keys and their copies, the single-signer limit of the anchors, the
  sentinel, the token's authorities) from facts anyone can check. Administrator, registrar and server details are left out by
  design.
- [EXIT-3.0-SCOPE.md](EXIT-3.0-SCOPE.md): the EXIT 3.0 scope accepted on 26 October, item by item, with each item's status and
  limits and what it does not include.
- ROADMAP.md and VISION.md describe what is live today (evidence log and anchors, verifiers, sentinel, keyless tools, Control
  Map, research graph, radar pilot, free-tier continuation) and the order that follows from it: history that cannot be filled in
  later comes first; next the SPL Governance (Realms) and LayerZero readers the cases showed are missing; Q3 narrowed to
  control-setting anomalies with labels to be registered in advance.
- Python verifier boundary correction: ASCII memo grammar, exact integer types, malformed notary/message checks and JSON-RPC error classification. The corrected tools/ copy matches the site and API mirror. No new anchor or signature was made for this correction.


## 28 October 2026 (afternoon) · in-browser verifier, Control Map by address, revised cases

All times UTC.

- 09:48:57: the 27 October Control Map snapshot is also grouped by the address that holds each role, at
  /control-map/by-controller/. It is built only from the published control-map.json and adds no new reads.
- 11:19: both case notes were revised to the full findings, each fact re-read on chain or at its source, with the parties' and
  the press's statements in their own attributed section.
- 11:42:31: the log page gained a "Verify in this browser" button. verify.js, served next to the log and listed in its
  SHA256SUMS, runs the checks of `exit_log_verify.py log` in the reader's browser: every root rebuilt from the leaves, every
  consistency proof, and every anchor transaction fetched and compared. Log specification 1.4 lists verify.js. The page's
  Content-Security-Policy lets the browser contact the listed Solana provider only on /log/ and on the API's /v0/log/.
- 12:12:58: the provider list was reduced to solana-rpc.publicnode.com. In a real browser, api.mainnet-beta.solana.com answered
  403 to every request that carries a website origin; it was removed from the page and from the /log/ policy. The Python
  verifier still works with any provider. The button runs code served by EXIT's own site; for a check that does not depend on
  EXIT, run exit_log_verify.py.
- PRODUCT.md names the limited hourly radar pilot for owned webhook receivers (general scheduled alerts remain planned).


## 28 October 2026 (later) · answer bindings on request, a daily anchor from 29 October, an off-server sentinel, and two cases

All times UTC.

**Release with API document 2026-10-28.1** (09:03:05 to 09:03:11)
- Research answers can be bound to the evidence log on request. A 200 ANSWERED response of `/v0/research/solana/mint` or
  `/v0/research/ethereum/contract` carries `X-EXIT-Log-Binding` only when the request sends `X-EXIT-Log-Bind: 1`.
- Each key can bind at most 5 answers per UTC day; reads and answers themselves are not limited by this.
- `GET /v0/research/log-binding` returns a key's own binding and admission state for 7 days, or until the free period ends if
  that is sooner.
- When this entry was written, no answer binding had been admitted; the earliest possible admission is the 29 October 00:30 run,
  and it is not guaranteed.
- The private intake takes radar events first, then watch changes, then answers.
- From the 29 October run, the daily job is set to anchor the current root again on a day without new records. Each day the job
  runs successfully is then meant to leave one anchor, at most one per UTC day. This has not been observed yet.
- The log publishes `runs.json` with each run that recorded an outcome. It is EXIT's own unsigned statement; the anchors are what
  can be checked on chain.
- Log specification 1.3 adds a plain-words summary and rewrites the section on private records.

**Repository documents**
- openapi.json is now a copy of the live API document 2026-10-28.1.
- NOTARIES.md names the DNS copy of the notary keys.
- tools/exit_log_verify.py is the published verifier (the same SHA-256 as on the log), used by the sentinel.

**Another copy of the notary keys and an off-server check of the log**
- 07:40: the notary keys were published as the DNS TXT record `_exit-notary.exit-protocol.io`, a third copy apart from the log
  and this repository (see NOTARIES.md).
- 09:06: an outside sentinel started. It is a GitHub Actions job in this repository (`.github/workflows/log-sentinel.yml`). Every
  day at 00:45 it runs the verifier in `tools/` against the published log and Solana, and checks that the newest anchor and the
  newest run are at most 26 hours old. It writes the result to the `sentinel` branch; the job fails visibly when a check
  fails. Its first run passed.

**Control Map**
- The USDC and USDG Solana rows were not answered on 27 October (RPC_RESPONSE_INVALID: the provider's replies were not usable).
  Both were read again at 06:55; their records are due to enter the log with the next nightly root (29 October, 00:30). The page
  will be updated after that anchor.

**Cases**
- Two case notes: [BonkDAO, 6 July 2026](cases/bonkdao-2026-07-06.md) and
  [Kelp DAO rsETH, 18 April 2026](cases/kelpdao-rseth-2026-04-18.md) (chain data and times only; not an accusation).

## 28 October 2026 · anchor at tree size 200, bounded private log bindings and a notary-key rule

All times UTC.

**Evidence log**
- The first scheduled run of the daily job anchored tree size 200 at 00:30:07 (block time; slot 462273926), signed by the server
  notary key. EXIT then verified the whole log from outside its server with the published verifier against two Solana RPC
  providers: 200 leaves, roots at sizes 66, 68, 134 and 200, anchors at sizes 68, 134 and 200.

**Release with API document 2026-10-27.13** (00:48:56 to 00:49:03)
- Private log bindings, as a bounded intake: an account's watch changes and radar events (radar events come only from the limited alert pilot; see 27 October) can now be bound into the evidence log.
  The record and its salt go only to the account; the log publishes only a salted leaf and its known_at. Public leaves still
  expose timing and activity, and a hash does not prove possession of the raw evidence bytes. A service binding is not
  operator-authored public research.
- Watch rows and radar event metadata carry an admission status as side metadata (for example PENDING_ADMISSION,
  ADMITTED_NOT_ANCHORED, ADMITTED_ANCHORED, NOT_ADMITTED_EXPIRED, or NOT_BOUND with a reason; the API document lists all values).
  The bound changes and the delivery bodies never change. ADMITTED_ANCHORED is EXIT's status note; only an inclusion
  proof checked against the anchor transaction establishes anchoring.
- Intake limits: at most 128 new private leaves per UTC day, within a fixed lifetime total. Radar events keep a reserved share of
  each run's capacity, so a watch change can be NOT_BOUND (ADMISSION_CAPACITY) while radar events are still bound. (Later on 28
  October, internal per-run figures and the lifetime total were removed from this entry, and "each daily intake" was corrected to
  "each run's capacity"; they are not part of the public contract.) A private submission that is not admitted within seven days expires (NOT_ADMITTED_EXPIRED).
- Roots made after this release carry ordering=append-sequence/2 (the size-200 root above predates it): a late stated known_at does not backdate insertion or prove earlier knowledge.
- When this entry was written, no private binding had been admitted; inclusion in the next nightly root is not guaranteed.
- Alerts: EXIT's own end-to-end test took the pilot's single watch slot at 04:56; its receiver accepted signed deliveries from the
  live radar from 04:59, and the radar's first two private event bindings entered the intake at 04:58 (admission is due at the
  next nightly run, not guaranteed).
- Notary keys: the evidence-log SPEC now has a key rule. A key is added or retired only by these steps, in this order: (1) a commit to NOTARIES.md in this
  repository, (2) an anchored EXIT-NOTARY-ADD-v1 or EXIT-NOTARY-RETIRE-v1 memo signed by a key already listed and not retired, and
  (3) the updated notaries.json. An anchor signed by a key outside this chain is not an EXIT anchor. The verifier's notaries.json
  check is not an authorization check; check a signer against NOTARIES.md.
- Verifier: exit_log_verify.py gained a `leaf` mode (`leaf BINDING --log SOURCE`, with `--event` for the full radar event) that
  checks an account's own binding against the published log. It also takes `--answer BODY` (a file with the exact answer bytes)
  and a saved X-EXIT-Log-Binding header value. Both are prepared for answer bindings, which are not live: research answers do not
  carry that header yet.

**Repository documents**
- NOTARIES.md: the second copy of the notary keys, kept apart from the log, with the key rule above. The initial set is the first
  anchor key (tree size 68) and the server notary key (134, 200 and later daily anchors).
- docs/API.md, STATUS.md and openapi.json: updated to the live state on 28 October; openapi.json is now a copy of the live API
  document 2026-10-27.13.
- CHANGELOG.md: the 26 October entry on research records, on-request watches and Ethereum contract reads was moved into date
  order, wording unchanged. In "26 October 2026 · one research console", "the earlier entry below" means "26 October 2026 ·
  bounded live-token research and public adapters".

## 27 October 2026 · evidence log, Control Map, deeper reads and a limited alert pilot

All times UTC. Every item below was live on 27 October (the case study in this repository, not on the service). Routes that need
a key were checked from outside only without one. Prepared or held work is listed separately.

**Evidence log**
- EXIT's evidence log is public at https://exit-protocol.io/log/: an append-only RFC 6962 Merkle log of EXIT's own records, with
  every leaf and its known_at, every root (each one after the first with an RFC 9162 consistency proof from the previous root),
  every anchor, the notary keys, proof bundles for public records, SPEC.txt and a standalone verifier (exit_log_verify.py, Python
  standard library only).
- First Solana anchor at 12:14:06 (tree size 68, slot 462066497). A daily job on EXIT's server was installed at 16:57: at 00:30 UTC,
  when the log has grown, it sends one memo transaction signed by the server notary key
  4QuiVCiYFzBjHFNEzZnHu9WCYBAZPnUxtfHcWX9UkqJH, checks the finalized transaction and publishes the log. At most one anchor per UTC
  day, no automatic retries; a day without new records sends nothing. Tree size 134 was anchored by that key from a manual start of the installed job.
- The same files are served by the API without a key since 17:19: GET /v0/log/{file} and GET /v0/log/proofs/{size}/{leaf}.json.
- An anchor proves only that EXIT held these exact records no later than the transaction's block time. It does not prove that the
  chain facts are true, that EXIT knew them earlier, or that nothing was left out.

**Control Map** (16:59)
- https://exit-protocol.io/control-map/ lists the addresses EXIT's readers saw holding the control roles of the 50 largest tokens
  (CoinGecko market-cap order at 16:26:35) that have an Ethereum contract or a Solana mint (68 deployments), each read once at one
  finalized block or slot. 66 of 68 were answered; every answered row is a record in the evidence log with a link to its proof. A
  dated snapshot with no score and no verdict; a NOT_ANSWERED row is not "no admin". The map does not say who an address belongs
  to.

**Deeper reads** (12:37 and 13:05)
- Solana mints (exit.solana-mint-research/2): when an authority holder is a multisig or a program-owned account, the answer reads
  one hop behind it (signer accounts, owner program and its upgrade authority), in at most five read-only RPC calls.
- Ethereum contracts (exit.ethereum-contract-research/3): for up to two named addresses that hold code, the multisig interface
  getOwners()/getThreshold(); when a contract declares the AccessControl enumerable interface, the DEFAULT_ADMIN_ROLE member count
  and up to four members. At most 21 read-only calls at one finalized block. Interface answers, not proof of who holds a key.
- GET /v0/research/graph joins one to four of your own answers into one typed graph (who holds which role, one hop where read,
  conflicts listed). It fetches nothing and spends no research attempt. Since 19:49 it also shows pending-authority edges from the
  radar, only for a watch with an active alert receiver (see the pilot limits below). A pending-role edge is not a role grant;
  radar edges have no known time and say nothing between reads.

**Watches** (13:28 and 13:38)
- POST /v0/research/watch also accepts ?contract= for an Ethereum mainnet contract. Watches record changes one hop behind an
  authority when the answer was read one hop deep. Pull model: you re-read a watch with ?id=, at most every six hours, one research
  attempt each; at most 3 watches per key and 300 in total; a watch ends after seven days. Creating a watch reads nothing. This is
  not continuous monitoring; separately, a watch with an active alert receiver is also read hourly by the radar (see Alerts).

**Alerts: limited pilot** (16:19)
- /v0/research/webhook (GET, POST, DELETE) lets an account attach an HTTPS receiver to one of its own watches. The receiver passes a
  one-time challenge; deliveries are signed (X-EXIT-Signature, HMAC-SHA256) and sent at least once (not exactly once), retried
  after 1 min, 5 min, 30 min, 2 h and 6 h; three failed events in a row pause the receiver until its owner resumes it with a new
  challenge. The radar reads the watch's pending-authority scopes (Solana: durable nonce accounts, upgradeable-loader buffers,
  Squads v4 proposals; Ethereum: OpenZeppelin/Compound timelock calls, pending owner/admin transfers, default-admin transfers, Safe
  configuration) once an hour. These are hourly reads, not continuous monitoring; nothing is said between reads.
- Pilot limits: only one watch across the whole service can have a receiver; once it is taken, registrations for other watches
  are refused (429). EXIT planned to use that slot for its own rehearsal. At most two receivers per account; a bounded daily RPC
  budget; data kept for at most seven days (deleted when the radar's maintenance runs). When this entry was written, no end-to-end alert delivery from the live radar to any
  receiver was claimed; EXIT's own rehearsal with its test receiver did not run on 27 October.

**Research console and documents**
- Research console: one-hop and AccessControl answers, a "Watch this contract" action, and "Records & watches" moved above "The
  answer has a trail". English is the main language; the other languages stay selectable.
- Case study: cases/drift-2026-04-01.md, what the chain showed before the Drift admin takeover on 1 April 2026.

**Prepared, not live on 27 October**
- Account-private bindings of watch changes and radar events into the evidence log (held for a security review, then reworked;
  see 28 October).
- Token-2022 pause and scaled-amount authority interpretation; second-source corroboration of the Control Map's 66 answered rows.

## 26 October 2026 · one research console

- The browser interface at api.exit-protocol.io is now one research console in 16 languages: one address field that recognises a Solana token mint or an Ethereum contract, an evidence graph with times and limits, records and watches, a developer section and a limits and privacy section.
- Live Ethereum contract reads, research records and on-request watches are open in the same free service; the earlier entry below records the state before they opened.
- README and PRODUCT describe the live scope; the outdated sentence about a separate older alpha was removed.
- OpenAPI: refusal codes are explained, including ENROLLMENT_NETWORK_LIMIT_REACHED (two new free keys per network per UTC day).
- test_agent_records.py: an internal working label was removed from the module docstring.

## 2026-10-26 — research records, on-request watches and Ethereum contract reads

- Records name the unresolved question and evidence gap. Supported transient Solana provider failures allow explicit bounded follow-ups; a recorded reason is not an answer.
- Solana authority watches re-read only on request, at most every six hours.
- Ethereum current-contract reads inspect declared proxy slots, owner() observations, code identities and named holder account types at a provider-reported finalized block.
- Published client/MCP additions expose these same live routes. Transport and privacy safeguards remain in force.
- Public-HTTPS operator acceptance: 21 checks passed, 4 attempts / 2 answered / 0 credits, replay exact, test access revoked and denied. Finite acceptance is not a universal coverage or security guarantee.

## 26 October 2026 · bounded live-token research and public adapters

- Documented the live any-Solana-mint authority endpoint separately from recorded reference history and public Ethereum case notes.
- Closed the one-shot authenticated own-mint acceptance, including replay, usage and access revocation.
- Added a public standard-library Python client, stdio MCP wrapper, OpenAPI document and synthetic security regressions; HTTP redirects cannot forward bearer keys. Ethereum contract calls remain capability-gated and not live.
- Linked the visual roadmap and preserved the conditional growth windows.
- Applied API/alpha security headers with live checks, without widening research routes or changing campaign limits.
- Research records and pull watches remain a private candidate under separate review; no public migration or continuous detection claim.
- Removed internal role terminology from current public descriptions; historical dated delivery records remain historical.


## 25 October 2026 · reviewed successor

- Published illustrated whitepaper 0.6 with actual token/free-access facts and an explicitly future paid-integration boundary; retained the historical 0.5 edition.
- Corrected a Solana-case overstatement: an account’s owner program alone does not identify its deriving/signing program or prove runtime execution. Source observations remain unchanged, with a dated correction and all eight case locales updated.
- Verified the deployed overview against all eight locale catalogs; added case-schema documentation and clearer contribution/transparency guidance.
- Applied backed-up site security headers, www-to-apex redirect and a real 404 response while preserving the separate API/alpha blocks.
- Recorded separate v4 source-review acceptance and actual-host time synchronization ordering. No campaign reset, token transaction, private engine publication or paid API Pass activation.


## 25 October 2026 · actual free-service opening

- Opened https://api.exit-protocol.io/ at 12:38:20 UTC for one quota-limited 30-day campaign.
- Added anonymous key issuance, structured-query quick start, limits, expiry and no-payment boundary.
- Verified actual public HTTPS answer/replay/restart/revocation and encrypted state restore in an isolated copy; historical alpha remains separate.
- Published the official EXITP mint after two finalized read-backs; replaced obsolete “no mint” and “not open” current-status wording.
- Recorded that token creation preceded API activation; preserved historical records and v0.5 paper.
- Token-to-credit/paid API Pass redemption remains future integration, not an effect of buying or holding EXITP.

### Earlier same-day documentation snapshots (historical)

## 25 October 2026 · Current venue, free-first sequence and source corrections

- Free API: private corrected candidate, not yet open; the month-end is not a token-creation gate. Historical R8 operating closure remains distinct from the new free-serving layer.
- Website case presentation: five Solana signer observations, event versus observation block labels, event-window attribution, and explicit not-read versus unknown boundaries. Old evidence identities and dated paper v0.5 are preserved.
- TOKEN.md: the token is to be created through Jupiter Studio on the Meteora Dynamic Bonding Curve program after the free early-access API opens; the official mint address is published after creation. The earlier venue preference is withdrawn.
- TRANSPARENCY.md: financial reporting names operator revenue from the service and, if any, from the token's trading venue, replacing the earlier fee wording.
- WHITEPAPER.md: wording of the reserved launch actions simplified (the PDF edition is regenerated separately).
- README.md: "Official identity" (non-affiliation) and "License" sections added; LICENSE file added (CC BY-ND 4.0 for the documentation; names and marks are not licensed; engine, datasets and API remain proprietary).

This entry records documentation changes only. The creation venue is selected. No token mint address, launch date, sale or claim process is announced.

## 25 October 2026 · Public reading and correction workflow

- Added the illustrated whitepaper as a downloadable, 14-page PDF.
- Added public access and service FAQ, search metadata and a minimal sitemap.
- Added contribution guidance, a pull request checklist and structured forms for public website problems and source-linked corrections.
- Kept sensitive security reports outside public issues. These forms are not research orders, bounty offers or guaranteed service commitments.

This update concerns public presentation and documentation. The API remains restricted and the API Pass remains a private prototype; operating and launch acceptance are separate.

## 2026-10-24 · Research and service documentation expanded

- Broadened the project identity to evidence-based blockchain research and monitoring,
  while retaining control and change analysis as the first specialization.
- Added product, technology, delivery status, roadmap, token/service-rights,
  transparency, support and private security-reporting guides.
- Added conceptual graphics for the research pipeline and post-launch growth.
- Distinguished available recorded research, restricted API access and the privately
  tested API Pass prototype from public production availability.
- Reflected the unanswered-primary-query no-charge rule and bounded research intake.
- Separated first-service readiness, later token decisions and conditional Q1–Q4 growth.
- Removed incidental platform-specific expansion examples from the main positioning.

This entry records documentation changes. It does not announce a software release,
live API deployment, token mint, financial transaction or completed launch gate.

## 24 October 2026 · Public vision and whitepaper edition 0.5

- Published the illustrated public whitepaper and a versioned text mirror.
- Added a system map connecting the first specialization to the wider research vision.
- Aligned post-launch quarter numbering and added measurable long-term development boundaries.
- Preserved recorded case identities, restricted-alpha status and the prototype/production distinction.
