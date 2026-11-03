# Q1 accuracy baseline — result of 3 November 2026

**What was measured.** A fixed bank of 36 questions (bank v1.1, `q1-bank-v1.1.json` (this folder), sha256
`b2f4ee1776aa1336fc053f9c26d302a2cd669fd75cb587f7608dd21726bf576d`) was sent to the live API with one free key on 3 Nov 2026 between
00:05 and 00:07 UTC (run `20261103T000505Z`). Each question has an expected answer written down beforehand: an HTTP status, and where it
applies an outcome, a schema and required fields. A question counts as "met" when the live answer matches that expectation.

**Result.**

| Questions | Met | Share | 95% Wilson interval |
|---|---|---|---|
| All 36 | 31 | 86% | 71%–94% |
| The 25 whose expectation was never revised | 20 | 80% | 61%–91% |

The other 11 questions had their expected answers corrected after a first run on 2 Nov had seen the answers (`q1-erratum-v1-to-v1.1.json`:
the live contract schema had moved to /4 on 1 Nov, and one blacklist fact was wrong in the bank). All 11 were met, but they are not
independent evidence, which is why the second row exists.

**The five misses** (`q1-result-20261103T000505Z.json`, field `met_expectation`):
- Q1-03 (USDC mint) and Q1-15 (governance proposals): 503 refusals from the Solana provider. The causes were found the same night — a
  provider node behind the requested slot, and a provider that refused the program-account list — and fixed on 3 Nov 04:12 and 04:50 UTC.
- Q1-22 and Q1-24 build on the Q1-03 answer, so they could not run (409).
- Q1-27 asks for the research record of an earlier question that was a malformed input (Q1-33); the service creates no record for a
  malformed input, so the question's premise was wrong. This is a bank defect, left as a miss in this result.

**One engine.** Every answer that names an engine names 24da5740 (21 of 36; the other 15 are refusals or evidence views that carry no
engine field). The next engine release (bb49875c) was applied at 03:20 UTC, after the run.

**What these numbers do not show.** The bank was written on 2 Nov, before this run, but its hash was first published on 3 Nov, after the
run; nothing public proves the expectations predate the run. 36 questions are a small sample: the intervals above are wide. The quota
counters of the key for that UTC day were 21 counted attempts and 17 answered (questions that only read stored evidence do not count
against the free quota); they are a different measure from "met". The answer bodies are not published here; each row carries the
sha256 of the body that was received.
