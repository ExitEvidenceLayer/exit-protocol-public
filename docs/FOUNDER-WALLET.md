# EXITP founder wallet report — 3 November 2026

EXIT reports the founder wallet's EXITP balance on the 1st of every month, read-only from public Solana RPC (no wallet connection, no
signing), with every movement since the previous report. This first report covers the wallet's whole history.

- Wallet: `9JL2gfGKaGJzJkY2vxjLq9kdiPTGqxHnPixaEfmUiiV7`
- EXITP mint: `5vPz2s8NtkasmVRDz5ySz27V1E8UdSpzqc9xN678jups` (token account `J6Qmi6Kesrwgc2hWq7bQbcZMgjEksWgVUkxCtCFbh8KV`)
- Balance: **14,151,336.226592 EXITP** at slot 464805581 (2026-11-03 06:55 UTC); a second provider matches (slot 464805583)
- Sales: **none**. Outgoing transfers: **none**.

| Time | Signature | EXITP | USDC | What happened on chain |
|---|---|---|---|---|
| 2026-10-25 12:15:44 UTC | `4ebFBMoCi4jAi7dgkQ8kzPWDMsDXLDKmnqKaMQFTM8vjnhmJ5gxR37HzuRCZ4isRMjMdby1ak8wKFg6W16D3Gzu8` | — | — | failed transaction; no tokens moved |
| 2026-10-25 12:15:53 UTC | `3RPNcTmMheEdjkewwugvs1iNQDSRUbCiyVkmSsQ7qbxRnXnmW5GQNE5qD19LYrxUzktzxzeYz2u1qMBLdpdnERoj` | — | — | failed transaction; no tokens moved |
| 2026-10-25 12:16:05 UTC | `GWmb53ugxMA5Jkpb59bDz9myBaXSYc21kEWdAuWjyPouP1MQvv2yynSe5eMKHhrvjxGifLMaQBLDQDvt1RcsD4f` | +8,852,036.224443 | -50.000000 | purchase: USDC to EXITP swap |
| 2026-10-26 14:58:03 UTC | `3RQxxhgF2KmLBtHpkevTxj9KR6ekoarSS8wJU4MNp7koR2d7Z6Z3eH7rTU2HMqK4ZXv9xGM2t1WzmiY7GmHZGq7L` | +2,901,491.283451 | -15.009587 | purchase: USDC to EXITP swap |
| 2026-10-27 10:37:40 UTC | `jsQXt8yrQHfnKfLMkjZjASuLw4Tnbbi4n5kdFwzC7TehCDRxZApgZtWJCZLfWqtYCPJm4LbRzdvj4vDYqSHQN2U` | +1,588,895.309029 | -8.255266 | purchase: USDC to EXITP swap |
| 2026-10-29 12:26:43 UTC | `4E7hssgjxvJanxpVsX89peJM4kXbfq8zayBjmBTFi6mZxwMBxhu7XMKeAi1rgnptLdEfnxFvGKrSxZg51ZAhDk9h` | +808,913.409669 | -4.540403 | purchase: USDC to EXITP swap |

The four purchases add up exactly to the balance. Each signature can be checked on any Solana explorer.

## The pool-creator role

EXITP trades on a Meteora bonding-curve pool (`J3mPv9st8YeBzWHbth4KcRn87BkMrAFniVYWy6xy5YU4`, not migrated). Its creator role belongs to a
Jupiter Studio proxy account (`dtsvMPr3mNMPfm4TGU9UeCQZkZy7iXjAwhYEz9HMYK7`, derived from the seeds "proxy" + the mint) that records the
founder wallet. The founder created the pool and handed the creator role to the proxy in one transaction on 25 October 2026
(`5fdBc94NX75AqavrRD2nQDG3yq6aMSxJouwNn7C5CRDsZhzymme7q3Ki7GjEHHS6YBJ8KpYnGJ5uGgvhF8kbFn4`); it is the only transaction on the proxy.
Creator trading fees not yet claimed: **3.661513 USDC**; claims so far: **none**. The proxy's program
(`GL6kwZxTaXUXMGAvmmNZSXxANnwtPmKCHprHBM82zYXp`) is upgradeable; its upgrade authority is
`CvQZZ23qYDWF2RUpxYJ8y9K4skmuvYEEjH7fK58jtipQ`, whose holder EXIT does not know. Every future claim is listed in the next report.

Machine-readable reports: [founder-report-2026-11-03-v1.json](founder-report-2026-11-03-v1.json) (whole history) and
[founder-report-2026-11-03-v2.json](founder-report-2026-11-03-v2.json) (the same day with the creator role). Each one is committed to the
evidence log as a research observation whose result hash is the report file's sha256 (delivered 3 November, admitted at the next daily
anchor), so the log entry and this file can be checked against each other.

Limits: the report covers the wallet's current EXITP token account (every signature on it); a closed earlier token account would not
appear. The labels describe the on-chain action; if tokens leave the wallet, the founder states the purpose (reward, gift, bounty or
lock) and EXIT records it as the founder's statement.
