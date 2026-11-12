# Public documentation changelog

## 12 November 2026 · higher free limits, a service-capacity view and API behaviour changes

- Free limits. The service release of 12 November 2026 raised the limits of the free service. Per key per UTC day: completed answers from 20 to 50, attempts from 60 to 150. Across the service per UTC day: attempts from 300 to 1,500. Lifetime totals, which are never reset: attempts from 9,000 to 300,000, keys from 600 to 1,000. New keys: from 40 to 100 per UTC day, and from 2 to 5 per network per UTC day. The campaign limits (every figure above except the per-network one) were raised by an increase-only amendment of the running campaign, and the service keeps a record of that amendment. The per-network limit is a separate service setting. No limit was lowered, and no key or counter was reset. The amendment also raised the answer-cache size limit (`limits.cache_bytes`) from 16 MiB to 64 MiB. The campaign's dates and retention windows are unchanged. The proof of work for a new key stays at 16 bits.
- Service capacity. GET /v0/early-access now carries a `service_capacity` block (schema exit.free-service-capacity/1). It gives the attempts used and remaining for the current UTC day, the attempts used and remaining in total, and the keys registered and remaining in total (revoked keys count as registered). These are service-wide counts only: the block holds no per-key or per-network figure. A key's own usage stays on GET /v0/early-access/usage.
- Lifetime total. Once the service's lifetime attempt total is used, a request that needs a research attempt is refused with 429 FREE_RESOURCE_LIMIT_REACHED, as before. New in this release: no new key is issued then either (429 ENROLLMENT_CAP_REACHED), and the `enrollment.reason` field of GET /v0/early-access says CAMPAIGN_ATTEMPTS_USED. Daily limits reset at 00:00 UTC; the lifetime totals do not.
- Research records. A provider failure on GET /v0/research/ethereum/layerzero/peer is now recorded with the gap PROVIDER_UNAVAILABLE, as on the other live read routes (the known issue of 11 November in [STATUS.md](STATUS.md)). On the peer route these codes are RPC_UNAVAILABLE_NO_AUTOMATIC_RETRY, RESEARCH_DEADLINE_EXCEEDED, RPC_RESPONSE_INVALID and FINALIZED_BLOCK_INVALID. Earlier peer-route records keep their METHOD label. On every route EXIT's own method bounds stay METHOD: RPC_RESPONSE_TOO_LARGE and RPC_BUDGET_EXHAUSTED. These depend on the subject, not on the provider's availability; a retry is not expected to help.
- Request shape. A malformed JSON request body (JSON_REFUSED) or a duplicate JSON key (DUPLICATE_JSON_KEY) answers 400. It answered 409 before. Other refusals keep their status.
- HEAD requests. Of the routes the service itself answers, only the console page / answers a HEAD request: sent without a query string and without a request body, it gets the GET status and headers and no response body. A HEAD request for any other service route answers 405 METHOD_REFUSED. The files under /v0/log/ and /openapi.json are static files served by the web server and answer HEAD like GET. Before this release the service answered 405 to every HEAD request on its own routes.
- Alert receivers. The check that a receiver's host resolves only to public addresses now also refuses 192.0.0.0/24, 192.88.99.0/24 and fec0::/10.
- Console and API description. The console at https://api.exit-protocol.io/ shows the new limits and the service-wide capacity. Other console texts were corrected in English and 15 translations. The API description is version 2026-11-12.1; [openapi.json](openapi.json) is the live file. It lists the same routes as 2026-11-04.1. This time the repository copy of the API description was committed after the service switched, on the same UTC day, so that the new limits were not published before the service showed them. The two sentences named in the 4 November entry are corrected: the contract route's call limit (at most 26 calls within 60 seconds) and the wording on reverted getters.
- Documentation. [docs/API.md](docs/API.md), [STATUS.md](STATUS.md), [docs/CONNECT-AN-AGENT.md](docs/CONNECT-AN-AGENT.md) and the site's terms page carry the new figures. docs/API.md said "Return later if capacity is exhausted"; that was wrong for the lifetime totals, and it now says that daily limits reset at 00:00 UTC and that the lifetime totals are never reset. docs/API.md also said "Daily, enrollment and lifetime capacity limits are retained without reset" and "Later offer reductions or a scheduled end require at least 30 days notice"; it now says that existing keys, counters and the lifetime totals carry over, and that the notice applies to a reduction of the offer or an announced end. The terms page said "Existing daily, enrollment and lifetime capacity limits remain; continuation does not reset them or promise unlimited access." and "Global and per-network enrollment limits and campaign caps also apply"; it now gives the figures and says that continuation resets no counter. The terms page now says "30 days' notice" and adds that reaching a published lifetime total is not an announced end. The privacy page says five new keys per network per UTC day (two before) and describes the service-capacity block. [DELIVERY.json](DELIVERY.json) names the new API description version. [ROADMAP.md](ROADMAP.md) and the roadmap page list "higher free limits, with a service-capacity view" as live since the service release of 12 November 2026; it was planned by 13 November 2026.

## 11 November 2026 · access wording, the alert slot, case-file and documentation indexes, dated planned work

- Free access. [DELIVERY.json](DELIVERY.json), [DOCS.md](DOCS.md), whitepaper 0.7, the homepage, the roadmap page and [STATUS.md](STATUS.md) said that 30 days' notice comes before any end of free access: "at least 30 days' notice precedes any end" (DELIVERY.json) and "(30 days' notice before any end)" (STATUS.md). That said more than the service does. The notice applies to a reduction of the offer or an announced end. The service-wide lifetime totals of research attempts and of accounts (published at https://api.exit-protocol.io/v0/early-access) are never reset: once the attempt total is used up, requests that need a research attempt are refused, and once the account total is reached, no new key is issued, with no notice period. These texts now say so. [README.md](README.md) and [PRODUCT.md](PRODUCT.md) no longer call the whole service "30-day" or say that it is open only until 24 November; the STATUS.md row is now named "Free first API (first period 30 days, then continuing)".
- Alert pilot. The 5 November snapshot said "Hourly reads for one watched subject across the whole service, currently used by EXIT's test receiver." and "the single pilot watch is also read hourly (see radar)". EXIT's test watch was created on 28 October 2026 at 04:56 UTC and a watch ends after at most seven days, so that watch had ended by 5 November. On 11 November 2026 at 06:04 UTC a read of the service's records found no receiver and no watch: the slot was free. DELIVERY.json, DOCS.md, STATUS.md, [ROADMAP.md](ROADMAP.md), [docs/API.md](docs/API.md), the roadmap page and whitepaper 0.7 now say this. STATUS.md and docs/API.md said "Since 28 Oct 04:56 UTC the single slot is used by EXIT's own end-to-end test"; they now say "From 28 Oct 04:56 UTC the single slot was used by EXIT's own end-to-end test" and add the 11 November read. docs/API.md also said that the slot "is planned for EXIT's own test run, so other accounts should not expect alerts yet"; it now says that the first account that registers a receiver takes a free slot.
- Whitepaper 0.7 (the HTML edition and [WHITEPAPER.md](WHITEPAPER.md)): the earlier sentences of the three corrected texts are quoted in a dated corrections note in its document-status block. The PDF is unchanged, and its link says that it is the 5 November text. Whitepaper 0.6 is now labelled a historical edition and links to 0.7; the 0.5 note and the site's not-found page link to 0.7.
- Site: a case-file index (https://exit-protocol.io/case-files/) and a documentation index (https://exit-protocol.io/docs/). The three case-file README.txt files now name their log leaf (204, 205 and 206), first anchor and proof bundle. The homepage's duplicate-token sentence said "Not affiliated with ... the duplicate token ... that shares EXITP's name and symbol"; that token was created by the same launch wallet 28 seconds before the official mint ([TOKEN.md](TOKEN.md)), and the sentence now says that it is not EXITP. The homepage also said that the official mint was "shown above" (it is shown below), named source version 17a0422f where the case notes carry 4521cf3f, described the Control Map as "the largest tokens" (it now gives the selection rule of the Control Map page, as README.md does) and said "a verified private intake channel is not offered yet", although security.txt gives contacts for private reports (the answer now points to security.txt and promises no response time). The privacy page now names the public chain-data providers that live reads go to (dated), the request log of the older alpha.exit-protocol.io interface and the browser request of the log page's verifier, and says that watch-change and radar-event log bindings are made by the service itself.
- STATUS.md, ROADMAP.md and docs/API.md said only that the client and MCP methods for the newer routes were checked against a loopback stub. They now add which of those routes answered with a key on the live service in the question-bank run of 3 November ([docs/q1-result-20261103T000505Z.json](docs/q1-result-20261103T000505Z.json)). docs/API.md said that re-anchoring an unchanged root "has not been observed yet"; it was first observed on 31 October and 1 November. ROADMAP.md said "Control Map daily re-read with change-only records"; every completed nightly run records one record per row.
- STATUS.md: EXIT's record of the 21 Control Map rows of the 3 November known issue (on the 4 and 9 November re-reads all 21 answered owner() as CALL_REVERTED; the public log shows the record hashes only), and two known issues: the "AGREES · 6 facts" count on 23 Ethereum rows of the Control Map page, and provider refusals on the LayerZero peer route recorded as METHOD.
- Smaller changes. The homepage access card no longer carries the daily limit figures; it points to https://api.exit-protocol.io/v0/early-access for the current limits. The offline page's card still carried the text from before the continuation ("Open 25 October–24 November 2026, 12:38:20 UTC. A single 30-day campaign") and now carries the homepage text. The terms page's link text said "30-day quota-limited free API is open"; "30-day" is dropped. On the roadmap page the stage 02 label said "Free campaign: 25 Oct–24 Nov 2026" and now says "Free service: since 25 Oct 2026 (first period to 24 Nov, then continuing)", and the page carries its new update date. STATUS.md said that recorded watch changes and radar events "can be bound into the evidence log"; the service itself binds them, and the row now says so. ROADMAP.md's line on the 21 Control Map rows now adds EXIT's record of the 4 and 9 November re-reads.
- ROADMAP.md and the roadmap page list dated planned work. The dates are latest dates, not guarantees.

## 10–11 November 2026 · client-row check read as values, one sentinel results file per run, documentation corrections

- 10 November, 15:31 UTC: [tools/claims_check.py](tools/claims_check.py) checks the server version that the client row of [STATUS.md](STATUS.md) names against [exit_mcp.py](exit_mcp.py) (some wordings, such as "server release X.Y.Z", were not yet read); when exit_mcp.py is not in the checkout, a row in which it reads a server version fails (hub commit [642cd812](https://github.com/ExitEvidenceLayer/exit-protocol-public/commit/642cd81204238f567ede8e30a585f33308a88ec6)). From hub commit [ef95f695](https://github.com/ExitEvidenceLayer/exit-protocol-public/commit/ef95f6957945f8b9ff367af752d748319c57ce9c) (15:32 UTC) the sentinel also fetches exit_mcp.py and records the client-row details in its result.
- 19:13 UTC: tools/claims_check.py reads the client row as values (hub commit [9dfb9770](https://github.com/ExitEvidenceLayer/exit-protocol-public/commit/9dfb977071470d86f3885feb01deee018053fc7f)): each three-part number (X.Y.Z) in the row's description cell must equal the server version in exit_mcp.py; tool counts written in digits before "tool" or "tools" are compared with the server's tool count when the row names a server version; and only one client row is allowed. The exact forms it reads, and its limits, are in its docstring, which says that it guards against accidental drift by the row's own author, not against deliberate hiding.
- The 15:31 UTC version had a regression, found the same day: it compared only the first "(N tools, server X)" tuple's tool count, and it read more tuple forms than the version before it, so a row with a wrong count in a later tuple could pass where the earlier version failed. The 19:13 UTC version corrects this: it compares each tool count it reads, not only the first tuple's.
- 19:14 UTC: the sentinel writes `results/<date>.json` only for the day's first scheduled run, on its first attempt; any other run or re-run writes `results/<date>-<event>-<run id>-<attempt>.json`, and no results file is overwritten (latest.json still moves) (hub commit [ee04e464](https://github.com/ExitEvidenceLayer/exit-protocol-public/commit/ee04e4640fb02d75bb7a335ea81d1efbc97c6b95)). A manual run on 10 November had replaced that day's scheduled record.
- 11 November: the 4 November update in [STATUS.md](STATUS.md) now says that its statement about the 48 Ethereum rows of the 6 November 23:20 UTC run is EXIT's record and that the public log shows hashes only. [docs/ACCURACY.md](docs/ACCURACY.md) said "One run per interpreter release so far"; the standing benchmark last ran on 2 November, and the page now says that it has not yet re-measured the later reader releases. [docs/API.md](docs/API.md) now says what enrollment and receiver registration record (since 3 November).

## 10 November 2026 · agent tools server 1.3.1 and documentation corrections

- [exit_mcp.py](exit_mcp.py) reports server version 1.3.1 (hub commit
  [84ed9680](https://github.com/ExitEvidenceLayer/exit-protocol-public/commit/84ed9680a722072e8d89496e2f33108e16f6f243), 10 November
  01:04 UTC). It adds no tools. Replies from the EXIT API and the public log and chain reads are refused when arrays and objects nest
  beyond 128 levels, by an explicit depth check that does not depend on the interpreter. A malformed HTTP reply from the EXIT API is
  reported as the error BAD_HTTP_RESPONSE; status -1 means the request was sent and the reply could not be read, so check usage
  before a new attempt. exit_verify also reports verified=false when the chain evidence it fetched cannot be checked, and
  publisher_verified is true only when the anchor's signer is in the caller's trusted set and the chain anchor check passes. Every
  tool description says that returned text is source material, not instructions. [AGENT-TOOLS.md](AGENT-TOOLS.md) now says that the
  tools were written for Python 3.10 or later and tested on 3.12, and that the chain-data providers see the addresses and accounts
  asked about, including wallet addresses given to exit_freeze_status.
- [STATUS.md](STATUS.md) and [ROADMAP.md](ROADMAP.md) still named server 1.3.0; they and [docs/API.md](docs/API.md) said that the
  script client and MCP wrapper cover every route of API version 2026-11-04.1. That was not so under 1.3.0 or 1.3.1: receiver
  registration (POST /v0/research/webhook), the account routes under /early-access/ (challenge, enrollment, rotation, revocation,
  feedback), /v0/subjects, /v0/corroboration and /v0/contract are not wrapped; AGENT-TOOLS.md lists the tools and names receiver
  registration as outside the wrapper. Until hub commit 84ed9680, AGENT-TOOLS.md's 1.3.0 section said that the wrapper covered every
  research route the free service serves. STATUS.md and ROADMAP.md now name server 1.3.1; they and docs/API.md now say which routes
  are covered. API version 2026-11-04.1 lists the same routes as 2026-11-02.2. AGENT-TOOLS.md's opening paragraph now also names
  exit_evidence.py and tools/exit_log_verify.py, which the keyless tools need.
- STATUS.md (Control Map row and 4 November update), ROADMAP.md (contract reader /5 line) and the 4 and 6 November entries below
  described, in the future tense, Control Map nights that have since passed. The dated entries keep what they expected; all now state
  what the public record shows (in the 6 November entry, "Solana reads did not change" now reads "The Solana read providers did not
  change", because it now follows the Solana comparison result): the evidence log holds an observation for each of the 72 rows of the
  4, 5, 6 and 7 November 23:20 UTC runs; the daily page shows that the 7, 8 and 9 November runs compared all 48 Ethereum rows and
  found the same settings. None of the following is shown in the public record: whether the 4 and 5 November runs compared any
  Ethereum row, how many settings the 5 and 7 November runs compared, whether the nightly records carry CALL_REVERTED, and a result
  of the after-measurement on the fixed question bank that was planned after the 4 November run.
- [README.md](README.md) said that the evidence log is anchored on Solana once a day when it grows. The
  [log page](https://exit-protocol.io/log/) says that it is anchored once a day at 00:30 UTC, with the current root again when the
  log has not grown, and [anchors.json](https://exit-protocol.io/log/anchors.json) lists an anchor for every UTC day from 27 October
  to 10 November (two on 27 October, at 12:14 and 16:58 UTC, then one at 00:30 UTC on each day from 28 October), including
  31 October and 1 November, when the root (tree size 205) was unchanged. README.md now says so. README.md's client-file SHA-256
  table still listed earlier files (exit_client.py of 26 October and exit_mcp.py of 29 October) from 2 November until this change:
  hub commits caff9534 and f16e1d49 (2 November) and 84ed9680 changed these files without updating it, although README.md said
  that the values change in the same commit. It now lists the files of hub commit 84ed9680, adds exit_evidence.py, which the
  keyless tools load, says that exit_evidence.py pins the SHA-256 of tools/exit_log_verify.py, and records that the values were
  not updated in those commits.
  STATUS.md's Control Map row described the [daily page](https://exit-protocol.io/control-map/daily/) as showing counts per date; it
  now describes what the page shows: each row's last daily read and the number of consecutive daily reads with the same settings
  since a stated date, plus a summary of the runs. The same row's statement that the main
  [Control Map page](https://exit-protocol.io/control-map/) is not refreshed by the nightly run still holds: on 10 November that page
  lists 68 rows, and the latest read time it shows is 28 October 06:55:16 UTC. STATUS.md's 3 November update said that the daily
  page showed that night's reset as BASELINE_RESET; on 10 November the page does not show that code, and the update now says what
  the page shows. STATUS.md's 28 October update said that anchoring the current root again on a day without new records was not yet
  observed; [runs.json](https://exit-protocol.io/log/runs.json) lists it (HEARTBEAT_ANCHORED) on 31 October and 1 November, and the
  update now says so.

## 7 November 2026 · Whitepaper 0.7 and delivery-document alignment

- Added the dated whitepaper 0.7 HTML/PDF, its generated text companion, DOCS.md and the shared DELIVERY.json snapshot.
- Updated document links and delivery-state labels while preserving the North Star, quarter windows, earlier editions and recorded cases.
- Removed the superseded roadmap sentence: "Whitepaper 0.6 predates the evidence log; where they differ, this page and STATUS.md are current." The current dated status and changelog remain authoritative for later releases.
- The 4 November withdrawal is retained. This documentation release does not reinstate the withdrawn authority-path roadmap item or activate paid redemption.

## 6 November 2026 (recorded 7 November) · Ethereum read provider

- 01:40 UTC: the Ethereum reads of EXIT's service moved from ethereum-rpc.publicnode.com to eth.drpc.org in a release that ran
  from 01:33 to 01:40 UTC: the Ethereum research routes of the API, the radar's Ethereum reads and the nightly Control Map reads. Answers recorded
  in that window may name either provider; answers recorded before it keep the provider they name and still replay. The nightly
  second-provider check takes its Ethereum second source from eth.api.pocket.network instead of eth.drpc.org from its 7 November 00:05 UTC
  run, so its second source is never a primary endpoint; it now stops, before any second-provider read, if its second provider is also
  a primary source or is named by a sampled answer. The first Control Map run after the release (6 November 23:20 UTC) compared none of its
  48 Ethereum rows: each was recorded as NOT_COMPARED (READER_OR_SOURCE_CHANGED), because the Ethereum reader's code changed with
  the switch (a new hash of the reader's code, not a change seen in any contract; no Ethereum contract was compared that night).
  It compared all 24 Solana rows and found no change.
  The Solana read providers did not change (reworded 10 November). This entry expected the 7 November 23:20 UTC run to be the
  first to compare two reads from the new source. What the public record shows (corrected 10 November): that run recorded an
  observation for all 72 rows in the evidence log, and on 10 November the [daily page](https://exit-protocol.io/control-map/daily/)
  shows every Ethereum row with the same settings at 4 consecutive daily reads since the 6 November read, so the 7 November run
  compared all 48 Ethereum rows with their 6 November reads and found the same settings; how many settings it compared per row is
  not shown in the public record. This entry was added on 7 November; the release was not recorded here on 6 November.

## 4 November 2026 · contract reader /5, six Control Map setting names, Arbitrum case on the homepage, claims check v3

- 06:30 UTC: the nightly Control Map comparison can compare six more setting names of the
  [Control-Change Record list](control-change/control-change-settings.json) (56 names; the list was updated here at 04:47 UTC): the
  ZeppelinOS proxy implementation and admin slots, and masterMinter(), pauser(), blacklister() and rescuer() of Circle's FiatToken.
  The contract reader reads these four getters only when a token's proxy and implementation code match the reviewed USDC pair byte
  for byte; it reads the ZeppelinOS slots on every Ethereum row, and an empty slot is compared as the zero address. This entry
  expected the 4 November 23:20 UTC run to compare no Ethereum row (the reader moved to /5 that day, READER_OR_SOURCE_CHANGED) and
  the 5 November 23:20 UTC run to be the first to compare two /5 reads, with each compared Ethereum row other than row 4 counting two
  more compared settings than without the six names and row 4 (USDC on Ethereum) six more when both of its reads match the reviewed
  pair (two otherwise). What the public record shows (corrected 10 November): both runs recorded an observation for all 72 rows in the
  [evidence log](https://exit-protocol.io/log/) (48 Ethereum, 24 Solana). Whether either run compared any Ethereum row, and how many
  settings, is not shown in the public record: the [daily page](https://exit-protocol.io/control-map/daily/) restarts each Ethereum
  row's count at the 6 November read (entry above), and its [daily.json](https://exit-protocol.io/control-map/daily/daily.json) gives
  the number of compared settings (field compared_settings_in_latest_read) only for the latest read. On 10 November, daily.json's
  latest read (9 November 23:20 UTC) gave 10 compared settings for row 4 (USDC on Ethereum) and 5 to 8 for each other Ethereum row:
  settings compared, not changes found.
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
