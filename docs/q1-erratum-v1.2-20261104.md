# Q1 question bank v1.2 - erratum of 4 November 2026

Written 2026-11-04T02:54:31Z (UTC), after the Ethereum contract reader went to schema exit.ethereum-contract-research/5 (live since 4 Nov 01:35
UTC) and after /5 answers had been seen: the release's own test answers (four answered rows in its selftest fixture) and its Control
Map dry run (48 Ethereum rows answered under /5). No Q1 question had been run against /5 when this erratum was written: the only Q1 run
is 3 November 00:05 UTC (run 20261103T000505Z, under /4); the Q1 daemon has been inert since (4 Nov 00:05 UTC receipt "SKIPPED
INERT:COMPLETE").

Change: in the oracles of Q1-06, Q1-07, Q1-08, Q1-09, Q1-10 and Q1-11 only, "schema": "exit.ethereum-contract-research/4" becomes
"schema": "exit.ethereum-contract-research/5". No other byte changes: six bytes ('4' -> '5') at offsets 5276, 5861, 6435, 7007, 7567
and 8163 (0-based), file size unchanged. The /4 text inside errata_from_run_1 is kept, and so is the file's internal "version": "1.1"
field (changing it would change another byte); v1.2 is identified by its file name and its sha256.

Why: the six questions keep their expected outcome (ANSWERED_WITHIN_DECLARED_SCOPE) and required fields; /5 answers carry all of
them. The runner compares the schema by string equality, so under v1.1 a /5 answer would fail on the version line alone.

Hashes:
- v1.1 (unchanged, kept as its own file): q1-bank-v1.1.json  sha256 b2f4ee1776aa1336fc053f9c26d302a2cd669fd75cb587f7608dd21726bf576d
- v1.2 (this erratum):                    q1-bank-v1.2.json  sha256 226d59a5e5305a026e4421fd1f7d9bcc5f55db4a731f25865eb2ef6591227d3b

Use: the 3 November before-run stays graded on v1.1 (it ran under /4). The 5 November after-run is graded on v1.2, and also on v1.1 so
that the effect of this erratum stays visible, as was done for v1 and v1.1.
