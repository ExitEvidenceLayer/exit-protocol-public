# EXIT evidence log: notary keys

This file is a second, independent copy of the keys that sign EXIT's evidence-log anchors. The log itself lives on
exit-protocol.io/log/; this repository is hosted separately on GitHub. If any two copies ever disagree, treat the anchors as unverified
and report it through the issue templates.

| Solana public key | Role | Anchors signed (tree size) |
|---|---|---|
| `4QuiVCiYFzBjHFNEzZnHu9WCYBAZPnUxtfHcWX9UkqJH` | Server notary key: signs the daily anchors at 00:30 UTC | 134, 200 and later daily anchors |
| `HULGYk61DBoZ6FWsBMma13UdRXFqiuPScr8at8P7yDrv` | First anchor key (manual) | 68 |

A third copy, kept apart from the log and this repository, is the DNS TXT record `_exit-notary.exit-protocol.io`, set at
07:40 UTC on 28 October 2026. It reads
`v=exit-notary1; keys=4QuiVCiYFzBjHFNEzZnHu9WCYBAZPnUxtfHcWX9UkqJH,HULGYk61DBoZ6FWsBMma13UdRXFqiuPScr8at8P7yDrv; list=github.com/ExitEvidenceLayer/exit-protocol-public`.
Check it with `dig +short TXT _exit-notary.exit-protocol.io`. It is a convenience copy, not a step of the key-change rule below;
it is updated together with step 3.

The published list is https://exit-protocol.io/log/notaries.json. Its SHA-256 earlier on 28 October 2026 was `5019ace5d5527dacb4c91f754dd62364f8b7add272ec2a97102e8554abf1fba6`;
at 09:09 UTC, after lists of anchor signatures were added (same keys), it was
`d38f62c978bfe55211d16719b71db6245f22f8bdcdeb1f0682f45a5477e1c601`. The file grows as keys sign anchors, so compare the keys, not
only the digest.

## How to check an anchor against this file
1. Run `exit_log_verify.py proof BUNDLE --rpc URL --notaries https://exit-protocol.io/log/notaries.json` (or `log SOURCE --rpc URL`).
2. Check that the signer it prints is one of the keys above.

## Key changes
A key is added or retired only through all of the following, in this order:
1. A commit to this file in this repository.
2. An anchored Solana memo `EXIT-NOTARY-ADD-v1 <key> <yyyy-mm-dd>` (or `EXIT-NOTARY-RETIRE-v1 <key> <yyyy-mm-dd>`) signed by a key
   already listed here and not retired.
3. The updated notaries.json on the log.

An anchor signed by a key that did not enter through these steps is not an EXIT anchor. The log's own verifier only checks that a
signer is listed in the log's notaries.json, which EXIT builds from its own anchors; check the key against this file. The two keys above are the initial set
(28 October 2026). Retiring a key does not invalidate the anchors it signed while it was listed.

## Key-change memos
| Date | Memo | Signed by | Transaction signature |
|---|---|---|---|
| (none yet) | | | |
