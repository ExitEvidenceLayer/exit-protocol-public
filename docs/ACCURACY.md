# Accuracy notes

EXIT publishes what it measured, with the rule fixed before the first read. Every run below is pre-registered (the hashes of the design,
the harness and the reader bytes are recorded before any read), uses labels the reader never sees (independent providers, independent
decoding), and reports facts compared, facts correct and a 95% Wilson interval per group. A fact is a single field of an answer (an
authority, a slot, a code class, a listed flag, a balance). Precision is about the facts EXIT states; it says nothing about facts a
reader does not read.

## Standing benchmark (AB-0), runs on 1–2 November 2026

| Run | Surface | Sample facts correct / compared | Notes |
|---|---|---|---|
| v2, 1 Nov 18:33 UTC | Solana mints, Ethereum contracts | 207/207 Solana, 170/170 Ethereum | gate for the mint reader /2 |
| v3, 1 Nov | same, labeler rule v2 (EIP-1167 clones) | 210/210 Solana, 158/158 Ethereum | gate for the clone recognition |
| v4, 1 Nov 19:19 UTC | Token-2022 stratified Solana sample | 178/178 Solana (103/103 Token-2022), 174/174 Ethereum | one transport incomplete |
| v5, 1 Nov 20:40 UTC | the /2 mint reader before its release | 185/185 Solana (149/149 Token-2022), 160/160 Ethereum | pre-release gate |
| v6, 2 Nov 04:04 UTC | + issuer freeze (USDT, USDC, PYUSD) | 120/120 freeze, 169/169 Ethereum, 204/204 Solana | one transport incomplete |

The four fixed control subjects (USDC and PYUSD on both chains, plus a publicly listed address for the freeze surface) were correct on
every fact in every run; the table shows the fresh random samples only.
v6 was pre-registered twice: a first attempt at 02:11 UTC was voided when the operator's machine lost network (the Ethereum and freeze
halves failed; the Solana half had completed, 66/66 correct), a harness defect it exposed was fixed (a transport failure had been classified
as out of scope), and the design was re-hashed at 03:54 UTC before the counted run. The voided attempt is kept and not counted; for v6,
"pre-registered" therefore means before the counted run, not before every read. The Q1 question bank is a separate measurement with its
own two-column result (docs/Q1-RESULT.md).
A transport incomplete is a provider failure during the read, counted in coverage, not as an error. Two LABEL_STATE_MOVED subjects
in v5 (the label and the read saw different states within the window) are excluded by rule.

## Documented controllers (level I), 2 November 2026

Where a publisher names a controller address, EXIT's observation agreed: the USDS implementation equals Sky's chainlog `USDS_IMP`; the
AAVE token's proxy admin equals the Aave address book's `PROXY_ADMIN_LONG`; the USDG Ethereum OFT's LayerZero peer for Solana decodes to
the Solana OFT contract Paxos publishes. Paxos and Circle publish token addresses only, no controller addresses. No disagreement found.

## Limits

One run per interpreter release so far (a weekly cadence is a separate decision). Labels and reads share the same chain state, so a
fact neither side can see is not compared. Precision intervals for small groups are wide and are printed as such. Nothing here is a
claim about tomorrow's state or about who operates an address.
