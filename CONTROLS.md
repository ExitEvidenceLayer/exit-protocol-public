# EXIT's own controls

EXIT reads who controls other projects. This page applies the same question to EXIT, using only facts anyone can check. Each item
says what it controls, where it is published and how to check it. Accounts and services whose details would help an attacker
(administrator accounts, the domain registrar, server access) are not listed here, by design.

Read on 28 October 2026.

## Evidence-log anchors

| What | Fact | Check |
|---|---|---|
| Daily anchor signer | One Solana key, `4QuiVCiYFzBjHFNEzZnHu9WCYBAZPnUxtfHcWX9UkqJH`, signs the daily anchors at 00:30 UTC (tree sizes 134 and 200 so far). | [NOTARIES.md](NOTARIES.md); https://exit-protocol.io/log/notaries.json |
| First anchor signer | `HULGYk61DBoZ6FWsBMma13UdRXFqiuPScr8at8P7yDrv` signed the first anchor (tree size 68), by hand. | the same two files |
| Copies of the key list | Three copies held apart: the log's notaries.json, NOTARIES.md in this repository, and the DNS TXT record `_exit-notary.exit-protocol.io`. If two copies disagree, treat the anchors as unverified. | `dig +short TXT _exit-notary.exit-protocol.io` |
| Key changes | Only by a commit to NOTARIES.md, an anchored `EXIT-NOTARY-ADD-v1` or `EXIT-NOTARY-RETIRE-v1` memo signed by a listed key, and the updated notaries.json, in that order. | [NOTARIES.md](NOTARIES.md) |

**Limit, stated plainly:** each anchor is signed by one key held by EXIT. This is the same single-signer shape EXIT points out in
other systems. The planned remedy is a threshold notary and two or three outside witnesses that check and co-sign roots, in the
manner of Certificate Transparency. Until then, an anchor proves that EXIT's key published a root no later than its block time,
not that anyone else agreed with it.

## Outside checks of the log

| What | Fact | Check |
|---|---|---|
| Daily sentinel | A GitHub Actions job in this repository runs the published verifier against the live log every day at 00:45 UTC and writes the result to the `sentinel` branch. | `.github/workflows/log-sentinel.yml`; the `sentinel` branch |
| In-browser verifier | https://exit-protocol.io/log/ can rebuild every root and fetch every anchor transaction in the reader's own browser. | the "Verify in this browser" button; `verify.js` on that page |
| Verifier you run yourself | `exit_log_verify.py` (Python standard library only) does the same checks offline and with any Solana provider. | https://exit-protocol.io/log/exit_log_verify.py |

**Limit:** the sentinel runs in EXIT's own repository, and the in-browser verifier is served by EXIT's own site. For a check
that does not depend on EXIT, download the verifier, read it, and run it against the published files with a provider you choose.

## Token

| What | Fact | Check |
|---|---|---|
| Official mint | `5vPz2s8NtkasmVRDz5ySz27V1E8UdSpzqc9xN678jups` (standard SPL Token program, 6 decimals, supply 1,000,000,000). | [TOKEN.md](TOKEN.md) |
| Mint authority | `null`: no key can create more tokens. Read again on 28 October 2026 at slot 462,472,475. | any Solana explorer or `getAccountInfo` on the mint |
| Freeze authority | `null`: no key can freeze holders' tokens. Same read. | same |
| Lookalike token | A second token with the same name and symbol exists and is not EXITP. Always check the mint address. | [TOKEN.md](TOKEN.md) |

## Public addresses

| What | Address |
|---|---|
| Website and evidence log | https://exit-protocol.io (log at /log/) |
| API | https://api.exit-protocol.io |
| Security contact | https://exit-protocol.io/.well-known/security.txt |
| Public documentation | this repository |

## What this page does not cover

- Who holds the keys above, beyond "EXIT".
- Server, hosting or registrar details, and administrator accounts of any service: these stay private because publishing them would
  help an attacker.
- The research engine and datasets, which are not public.

Changes to the facts on this page are recorded in [CHANGELOG.md](CHANGELOG.md).
