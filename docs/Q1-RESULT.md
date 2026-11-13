# Q1 accuracy measurements — baseline of 3 November 2026 and after-run of 5 November 2026

## After-run of 5 November 2026 (added 13 November 2026)

**What was measured.** The same 36 questions were sent again to the live API with one free key on 5 Nov 2026 between 00:05 and
00:08 UTC (run `20261105T000505Z`, one UTC day: 36 sent, none carried over, 30 answered with HTTP 200). The run used bank **v1.2**
(`q1-bank-v1.2.json`, this folder, sha256 `226d59a5e5305a026e4421fd1f7d9bcc5f55db4a731f25865eb2ef6591227d3b`). v1.2 is v1.1 with one
change, written on 4 Nov 2026 at 02:54 UTC, before this run (`q1-erratum-v1.2-20261104.md`, this folder, sha256
`892e067e899b3e56983d50808a91e1ce1b3cb088df47255a28f7b540ff6ba01a`): the expected schema of Q1-06 to Q1-11 is
`exit.ethereum-contract-research/5` instead of `/4`. The Ethereum contract reader went to schema /5 on 4 Nov at 01:35 UTC, and the
erratum was written after /5 answers had been seen. The hash of v1.2 is first published here, after the run.

The recorded answers are graded against v1, v1.1 and v1.2 with the same check as the baseline, without any API call, every body bound
to its recorded sha256; the regrade on v1.2 reproduces the run's own recorded result. Per question: `q1-result-20261105T000505Z.json`
(this folder; each row carries the sha256 of the answer body, not the body).

**Result, next to the baseline.**

| Questions | Graded against | 3 Nov run: met (95% Wilson interval) | 5 Nov run: met (95% Wilson interval) |
|---|---|---|---|
| All 36 | v1 (published before both runs) | 21 (42.2–72.9%) | 24 (50.3–79.8%) |
| All 36 | v1.1 | 31 (71.3–93.9%) | 28 (61.9–88.3%) |
| All 36 | v1.2 | not graded: that run answered in schema /4 | 34 (81.9–98.5%) |
| The 25 never revised (identical in v1, v1.1 and v1.2) | any | 20 (60.9–91.1%) | 23 (75.0–97.8%) |
| The 30 unchanged between v1.1 and v1.2 | v1.1 (3 Nov), v1.2 (5 Nov) | 25 (66.4–92.7%) | 28 (78.7–98.2%) |

v1 is publicly dated before both runs and v1.1 before the 5 November run (its hash was published on 3 Nov); v1.2 is not publicly
dated before that run. On v1.1 the after-run is lower (28) because
Q1-06 to Q1-11 now answer in schema /5 while v1.1 expects /4; that is the erratum, not a failed answer. Their passes on v1.2 are not
independent evidence.

**What moved** (per question, from the two recorded results):
- Q1-03 (USDC mint) and Q1-15 (governance proposals), both Solana: 503 on 3 Nov, 200 on 5 Nov. Q1-22 and Q1-24 build on the Q1-03
  answer: 409 on 3 Nov, 200 on 5 Nov.
- Q1-14 (Solana governance): 200 on 3 Nov, 503 on 5 Nov (error code `RPC_RESPONSE_INVALID`; no automatic retry, no credit charged).
  Its cause is not established.
- Q1-27 stays a miss: the bank defect described below (its premise is a record that a refused input never creates).

These changes are in Solana reads and in questions that build on them. The baseline below names fixes of 3 Nov 04:12 and 04:50 UTC
for the causes of the Q1-03 and Q1-15 refusals. This run does not isolate the effect of those fixes or of any other service release
between the two runs, and with 36 questions and one run on each side the intervals overlap: the two runs are not separated.

**One engine.** Every answer that names an engine names bb49875c (22 of 36). The other 14 carry no engine field: 6 refusals and 8
workflow answers (record lists, comparisons, graphs, a log binding and a watch).

**What these numbers do not show.** A small fixed question bank is not a measure of usefulness to a person. The answer bodies are
not published here; each row carries the sha256 of the body that was received.

## Baseline of 3 November 2026

**What was measured.** A fixed bank of 36 questions was sent to the live API with one free key on 3 Nov 2026 between 00:05 and 00:07 UTC
(run `20261103T000505Z`). Each question has an expected answer: an HTTP status, and where it applies an outcome, a schema and required
fields. A question counts as "met" when the live answer matches that expectation. The same recorded answers are graded against two
versions of the expectations:

- **v1** (`tools/q1-bank-v1.json`, sha256 `524db8d997dcb9955c8506478f6c5fbcdfe5af1879114b209a615e22c189a5ea`), published in this repository
  on 2 Nov 2026 at 06:57:02 UTC (commit 65aed6ff), 17 hours before this run. It was published three minutes after a first, exploratory
  run had started (06:54:13 UTC); it was not changed after that run, and it still contains the four errors that run exposed.
- **v1.1** (`q1-bank-v1.1.json`, this folder, sha256 `b2f4ee1776aa1336fc053f9c26d302a2cd669fd75cb587f7608dd21726bf576d`): the same 36
  questions with the expected answers of 11 questions corrected after that first run had been seen (`q1-erratum-v1-to-v1.1.json`: the live
  contract schema had moved to /4 on 1 Nov, the evidence view's required field names were wrong, and one blacklist fact was wrong). Its
  hash was first published on 3 Nov, after this run.

The two hashes differ because they are two files; v1.1 is not a re-hash of v1.

**Result.**

| Questions | Graded against | Met | Share | 95% Wilson interval |
|---|---|---|---|---|
| All 36 | v1 (published before the run) | 21 | 58% | 42%–73% |
| All 36 | v1.1 (11 expectations revised after a first run) | 31 | 86% | 71%–94% |
| The 25 never revised (identical in v1 and v1.1) | either | 20 | 80% | 61%–91% |

The v1 row is the only one whose expectations are publicly dated before the run. 10 of the 11 revised questions are met only under v1.1;
they are corrections of bank errors, but they are not independent evidence. Per-question differences: `q1-two-column-20261103T000505Z.json` (this folder; graded from the
recorded answers without any API call, every body bound to its recorded sha256).

| Question | HTTP status | v1 | v1.1 | Note |
|---|---|---|---|---|
| Q1-01 | 200 | met | met |  |
| Q1-02 | 200 | met | met |  |
| Q1-03 | 503 | miss | miss |  |
| Q1-04 | 200 | met | met |  |
| Q1-05 | 200 | met | met |  |
| Q1-06 | 200 | miss | met | revised: schema |
| Q1-07 | 200 | miss | met | revised: schema |
| Q1-08 | 200 | miss | met | revised: schema |
| Q1-09 | 200 | miss | met | revised: schema |
| Q1-10 | 200 | miss | met | revised: schema |
| Q1-11 | 200 | miss | met | revised: schema |
| Q1-12 | 200 | met | met |  |
| Q1-13 | 200 | miss | met | revised: expect.tokens, question |
| Q1-14 | 200 | met | met |  |
| Q1-15 | 503 | miss | miss |  |
| Q1-16 | 200 | met | met |  |
| Q1-17 | 200 | met | met |  |
| Q1-18 | 200 | met | met |  |
| Q1-19 | 200 | met | met |  |
| Q1-20 | 200 | miss | met | revised: required |
| Q1-21 | 200 | miss | met | revised: required |
| Q1-22 | 409 | miss | miss |  |
| Q1-23 | 200 | met | met |  |
| Q1-24 | 409 | miss | miss |  |
| Q1-25 | 200 | met | met |  |
| Q1-26 | 200 | met | met |  |
| Q1-27 | 409 | miss | miss |  |
| Q1-28 | 200 | met | met |  |
| Q1-29 | 200 | met | met |  |
| Q1-30 | 200 | miss | met | revised: required |
| Q1-31 | 422 | met | met |  |
| Q1-32 | 422 | met | met |  |
| Q1-33 | 422 | met | met |  |
| Q1-34 | 200 | met | met |  |
| Q1-35 | 409 | met | met |  |
| Q1-36 | 200 | met | met | revised: required |

**The five misses under both versions** (`q1-result-20261103T000505Z.json`):
- Q1-03 (USDC mint) and Q1-15 (governance proposals): 503 refusals from the Solana provider. The causes were found the same night — a
  provider node behind the requested slot, and a provider that refused the program-account list — and fixed on 3 Nov 04:12 and 04:50 UTC.
- Q1-22 and Q1-24 build on the Q1-03 answer, so they could not run (409).
- Q1-27 asks for the research record of an earlier question that was a malformed input (Q1-33); the service creates no record for a
  malformed input, so the question's premise was wrong. This is a bank defect, left as a miss in this result.

**One engine.** Every answer that names an engine names 24da5740 (21 of 36; the other 15 carry no engine field: 9 refusals and 6
workflow answers (record lists, comparisons, graphs, a log binding and a watch); corrected 13 November 2026: this sentence said "the other 15
are refusals or evidence views", but the evidence views name the engine). The next engine release (bb49875c) was applied at
03:20 UTC, after the run.

**What these numbers do not show.** 36 questions are a small sample: the intervals above are wide. The quota counters of the key for that
UTC day were 21 counted attempts and 17 answered (questions that only read stored evidence do not count against the free quota); they are
a different measure from "met". The answer bodies are not published here; each row carries the sha256 of the body that was received.
