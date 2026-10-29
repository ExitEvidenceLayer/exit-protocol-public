# Public documentation changelog

## 29 October 2026 · quota-limited free continuity and verifier correction

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
