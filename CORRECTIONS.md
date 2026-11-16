# Corrections and error rate

EXIT counts its own published errors. This page lists every correction note on EXIT's published research output, says which
ones corrected a fact, and gives the count per kind of output. It is updated at the end of each month and whenever a correction
is made.

Counted to 16 November 2026 for every correction and for the case outputs; the evidence-log and Control Map rows give their published figures with their own dates.

## What is counted

A correction is counted when a published statement was wrong, or misleading, or said more than the published evidence
supported, and EXIT changed it. This includes a wrong label, an incomplete list presented as complete, and a missing caveat
whose absence made a statement misleading.

Not counted, but listed below: evidence added to support an unchanged answer, a note regenerated from a newer evidence set,
removal of internal names, changes that make a statement true for a later date (the earlier statement was true when made), and
a read surface extended to a role it did not cover (the earlier answer stated its scope).
Software and documentation corrections are in the [changelog](CHANGELOG.md); posts on social media are outside this page.

Only errors that were found are counted. A low count does not show that there are no other errors. Reports are welcome
through the [correction form](https://github.com/ExitEvidenceLayer/exit-protocol-public/issues/new/choose).

## Counts

| Output | Published | Corrections counted |
|---|---|---|
| Evidence-log records | 200 records with public proof bundles at tree size 205 (anchored 30 October); the other 5 leaves are private service bindings or records held until their own publication and are not in this count. Later, not in this figure: on 3 November the log had 363 published proof bundles at tree size 370 | 0 |
| Control Map rows | 68 (one per Ethereum contract or Solana mint on the 27 October list); every row has an answer on the published page. From the 3 November 23:20 UTC re-read the nightly run has 72 rows (declared rows added, see STATUS); since 12 November 2026 the published page shows 72 rows | 2 corrected on 12 November 2026, each one cause (notes below): the owner() label on 21 rows; the second-source count on 23 rows |
| Case outputs | 9: the website's three cases (Solana PYUSD, Ethereum USDC, Ethereum PYUSD) and the Drift, BonkDAO, Kelp DAO, Arbitrum Security Council, Kava Lend, and ANSEM, TJR and LUKE case notes; translations are not counted separately | 8, in 6 of the 9 outputs |

A rate per 1,000 is not given for case outputs: nine outputs are too few, and one output can carry several corrections. The log
is append-only: a wrong record is never edited or removed; its correction would be listed here with the record's leaf index.

## Every correction note

| Date | Output | What the note says changed | Counted | Why |
|---|---|---|---|---|
| 25 Oct 2026 | Website: Solana PYUSD | The answer described five signers while the note published one signer observation; the other four were published and the answer now states what the note publishes. | Yes | The answer said more than the published evidence supported. |
| 25 Oct 2026 | Website: Solana PYUSD | The answer overstated the multisig, as if any single one of the five signers were enough; the composition is now stated from the published observations. | Yes | Wrong statement. |
| 25 Oct 2026 | Website: Solana PYUSD | An owner-program observation was treated as proof of the deriving program and of runtime execution; the equivalence was removed. | Yes | Unsupported statement. |
| 25 Oct 2026 | Website: Solana PYUSD | Source commit advanced; internal names removed from earlier correction texts. Answer and evidence unchanged. | No | No fact changed. |
| 25 Oct 2026 | Website: Ethereum USDC | The blacklister was labelled UNKNOWN, which read as an evidence gap, although the role was outside the declared read surfaces; scope statements were missing for two rows. Labels and limits corrected; answer unchanged. | Yes | Wrong label. |
| 25 Oct 2026 | Website: Ethereum USDC | A separately read blacklister response disclosed as supplemental evidence. | No | Evidence added. |
| 25 Oct 2026 | Website: Ethereum USDC | The count of 132 events could not be traced from the published file; the 20 log-chunk identities were listed. Answer unchanged. | No | Evidence added for an unchanged answer. |
| 25 Oct 2026 | Website: Ethereum USDC | Regenerated from a newer evidence set (block 26,270,414). | No | Newer evidence set. |
| 25 Oct 2026 | Website: Ethereum PYUSD | An explorer link was labelled as the event block, and the controller list showed only the controller added in the recorded event although the published observation lists five. Labels and list corrected; answer unchanged. | Yes | Wrong label and an incomplete list. |
| 25 Oct 2026 | Website: Ethereum PYUSD | One 10,000-block chunk was cited for a 200,000-block window; all 40 chunk identities were listed. Answer unchanged. | No | Evidence added for an unchanged answer. |
| 25 Oct 2026 | Website: Ethereum PYUSD | Regenerated from a newer evidence set (block 26,270,414). | No | Newer evidence set. |
| 28 Oct 2026, 11:19 | [BonkDAO case note](cases/bonkdao-2026-07-06.md) | A shared funding wallet and a shared durable-nonce key were listed as history the deciding wallet and the receiving address share, without saying that both behave like an exchange's withdrawal infrastructure. The note said control was not established, but listed this way the two links still suggested common control. Found by an outside review. | Yes | A missing caveat made it misleading. |
| 29 Oct 2026 | [Kelp DAO case note](cases/kelpdao-rseth-2026-04-18.md) | The 28 October revision said the receiving address was blocked until 19 April at 00:10:55; the `UserTransfersBlocked` event sets 19 April at 18:23:11, 24 hours after the block (a decoding error of 65,536 seconds). Found by EXIT's own review of this page's sources; re-read from the transaction receipt. | Yes | Wrong statement. |
| 3 Nov 2026 | Control Map row 4 (USDC on Ethereum) | The [Arbitrum Security Council case note](cases/arbitrum-security-council-2026-10-30.md) says that the 27 October row did not record the blacklister role that froze the address. That role was outside the row's read surface; control-map.json, the first snapshot, says it does not prove that nothing outside the readers' declared scope exists. Since 4 November 2026 the contract reader also reads blacklister(), masterMinter(), pauser() and rescuer() when a token's proxy and implementation code match the reviewed USDC pair, and the Control Map page shows them since 12 November 2026. | No | Read surface extended; the row stated its scope and did not present its list as complete. |
| 12 Nov 2026 | Control Map page, 21 Ethereum rows | The page showed `owner(): NOT_OBSERVED (RPC error; cause not established)`. On these contracts owner() reverts; it was not a provider error (found 3 November, re-read from two providers). The page now shows the nightly read, `owner(): CALL_REVERTED`. The old label is kept in control-map.json, the unchanged first snapshot. | Yes | Wrong cause in a label; no holder was named before or after. |
| 12 Nov 2026 | Control Map page, Second source column | The page showed "AGREES · 6 facts" on all 48 Ethereum rows. On 23 of them five facts had been compared and owner() was reported but not compared (21 where owner() reverted and 2 (rows 43, 45) where it returned the zero address). The column now counts only compared facts and names the others. | Yes | A count that included facts that were not compared. |
| 13 Nov 2026 | Website: Ethereum USDC | An internal run identifier was removed from the text of the 25 October regeneration note; a dated note in the case file says so. Answer and evidence unchanged. | No | No fact changed. |
| 13 Nov 2026 | Website: Ethereum PYUSD | An internal run identifier was removed from the text of the 25 October regeneration note; a dated note in the case file says so. Answer and evidence unchanged. | No | No fact changed. |
| 15 Nov 2026 | [Kava Lend case note](cases/kava-lend-2026-11-14.md) | Two sentences called providers independent: the second provider from which most key facts were re-read, and the four Kava EVM archives against which the module's KAVA cash was cross-checked. That is not shown: two endpoints may relay the same upstream provider, and their agreement is then one witness, not two. The first now says a second provider and the second four separate archives, each with a dated note; no number and no finding changed. | Yes | The note said more than the published evidence supported. |

The Drift, the Arbitrum Security Council and the ANSEM, TJR and LUKE case notes have no correction note. The same provider wording was corrected on 15 November 2026 in STATUS.md and docs/ACCURACY.md; those are documentation corrections and are listed in the [changelog](CHANGELOG.md).

## Next update

30 November 2026, or earlier with the next correction.
