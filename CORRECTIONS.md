# Corrections and error rate

EXIT counts its own published errors. This page lists every correction note on EXIT's published research output, says which
ones corrected a fact, and gives the count per kind of output. It is updated at the end of each month and whenever a correction
is made.

Counted to 30 October 2026.

## What is counted

A correction is counted when a published statement was wrong, or misleading, or said more than the published evidence
supported, and EXIT changed it. This includes a wrong label, an incomplete list presented as complete, and a missing caveat
whose absence made a statement misleading.

Not counted, but listed below: evidence added to support an unchanged answer, a note regenerated from a newer evidence set,
removal of internal names, and changes that make a statement true for a later date (the earlier statement was true when made).
Software and documentation corrections are in the [changelog](CHANGELOG.md); posts on social media are outside this page.

Only errors that were found are counted. A low count does not show that there are no other errors. Reports are welcome
through the [correction form](https://github.com/ExitEvidenceLayer/exit-protocol-public/issues/new/choose).

## Counts

| Output | Published | Corrections counted |
|---|---|---|
| Evidence-log records | 200 records with public proof bundles at tree size 205 (anchored 30 October); the other 5 leaves are private service bindings or records held until their own publication and are not in this count. Later, not yet counted here: on 3 November the log had 363 published proof bundles at tree size 370 | 0 |
| Control Map rows | 68 (one per Ethereum contract or Solana mint on the 27 October list); every row has an answer on the published page | 0 |
| Case outputs | 6: the website's three cases (Solana PYUSD, Ethereum USDC, Ethereum PYUSD) and the Drift, BonkDAO and Kelp DAO case notes; translations are not counted separately | 7, in 5 of the 6 outputs |

A rate per 1,000 is not given for case outputs: six outputs are too few, and one output can carry several corrections. The log
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

The Drift case note has no correction note.

## Next update

30 November 2026, or earlier with the next correction.
