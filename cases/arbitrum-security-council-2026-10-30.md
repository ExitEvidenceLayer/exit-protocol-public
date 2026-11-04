# Arbitrum Security Council, 30 October 2026: an upgrade path that was on chain before it was used

EXIT Protocol · 3 November 2026 · all times UTC

On 30 October 2026 at 00:08:35, one transaction sent to the Arbitrum Security Council's Safe on Ethereum moved 74,559,805.2 ARB
and 8,425.997680 ETH on Arbitrum One out of the address `0x3e2bf1ac6bf0934bbba6456c341c2ecbced632d5`, without a signature of
that address. We re-read Ethereum and Arbitrum One with one question: what did the chain show about this path before it was used,
and when?

Below, what we read on chain is kept apart from what the Council and the press report. The second part is attributed and was not
checked by us. Every chain fact below was read from two providers and kept only when both agreed.

Terms used below:
- A Safe is a multi-signature wallet contract.
- A proxy is a contract that runs the code of another contract, its implementation; the proxy's admin can switch the implementation.
- The UpgradeExecutor is the Arbitrum contract that owns the proxy admins on Ethereum and runs upgrade actions for whoever holds its
  executor role.
- The Inbox is the Ethereum contract through which messages enter Arbitrum One.
- A type 0x65 transaction is a message from Ethereum executed on Arbitrum One in the name of an address, without that address's
  signature.

## What the chain shows

- **The path, readable at block 26,285,184 (27 October).**
  - The Inbox (`0x4dbd4fc535ac27206064b68ffcf827b0a60bab3f`) is an upgradeable proxy whose admin is
    `0x554723262467f125ac9e1cdfa9ce15cc53822dbd`.
  - That admin is owned by the UpgradeExecutor `0x3fffbadaf827559da092217e474760e2b2c3cedd`, the same contract that owns the ARB
    token's own proxy admin (`0x5613af0474eb9c528a34701a5b1662e3c8fa0678`).
  - Three addresses hold the UpgradeExecutor's executor role: the Security Council Safe
    (`0xf06e95ef589d9c38af242a8aaee8375f14023f85`, 12 owners, 9 signatures required), the L1 Timelock
    (`0xe6841d92b0c345144506576ec13ecf5103ac7f49`, minimum delay 259,200 s = 3 days) and a pause executor
    (`0x30668ee252a28986ee6dc21b26e4018ac0e339b9`).
  - Nothing on this path changed between 27 October and the block before the 30 October transaction (26,301,885).
- **The 30 October transaction.**
  - Transaction `0xb69c81774f507d46ce776aeaed8b4d31df96dd66ce6fd05073481011835355d6` (block 26,301,886, 00:08:35) was sent to the
    Council Safe and succeeded.
  - Inside it the UpgradeExecutor ran one action contract (`0x3d456fcd62f5babcf3263b72fb4ac8ff8cc5a322`) twice. Each run switched
    the Inbox to a temporary implementation (`0x980d1f93fc5809c828539c46084801673fa6a859`), delivered one message to Arbitrum One and
    switched the Inbox back to its usual implementation (`0x7c058ad1d0ee415f7e7f30e62db1bcf568470a10`): four `Upgraded` events in
    all. After the transaction the Inbox runs the same code as on 27 October (code hash unchanged).
  - The two messages are unsigned Arbitrum transactions in the name of `0x3e2bf1ac6bf0934bbba6456c341c2ecbced632d5` (its nonces 2
    and 3): a transfer of 74,559,805.2 ARB and a payment of 8,425.997680 ETH, both to `0x0000000000000000000000000000000000000DA0`,
    where they are now.
  - On Arbitrum One both landed at 00:18:20 as type 0x65 transactions with v, r and s all zero.
  - Nine of the Safe's twelve owners signed (recovered from the signatures; all nine were owners at that block).
- **Where the ARB came from.** The day before, on Arbitrum One, the 74,559,805.2 ARB reached `0x3e2bf1ac…` from
  `0x5227f603c1ee34ce3c06efe6477003bdfccb2f8c` (21:36:30), which had received it from `0xb38e8c17e38363af6ebdcb3dae12e0243582891d` at
  20:30:34.
- **The freezes on Ethereum.**
  - `0x5227f603…` was frozen by USDT at 21:01:35 on 29 October, in a transaction sent to
    `0xc6cde7c39eb2f0f0095f41570af89efc2c1ea828`, the USDT owner the Control Map recorded on 27 October (a multisig requiring 3 of 6),
    and by USDC at 21:04:59, from its blacklister `0x0a06be16275b95a7d2567fbdae118b36c7da78f9`, a role the 27 October USDC row did not
    record.
  - At Tether's freeze the address held 971,149,299.48 USDT; at Circle's, 823,000,000 USDC. USDT's blacklist checks only the sender,
    so 204.3 million more USDT arrived after it; 1,175,464,712.88 USDT is frozen there now, and only Tether's owner (`0xc6cde7c3…`)
    can release or destroy it.
  - Before any freeze the address had sent 700 million USDT on (20:30:11 and 20:33:23); both recipients were empty when Tether
    blacklisted them.
  - Ethereum ETH has no issuer blacklist: on 30 October at 05:15 the address sent 17,260 ETH to
    `0x03b0ee5d82990cff1bda48651ac3e436d1a020ea`, which had sent no transaction as of 3 November.
  - Tether and Circle also blacklisted `0x28c6c06298d514db089934071355e5743bf21d60` (22:06 and 23:53), the wallet the sweeps ran
    through, and Circle the smart wallet `0xee7ae85f2fe2239e27d9c1e23fffe168d63b4055` it owns (23:54:59; 2,956,093.65 USDC inside),
    from which both USDC transfers to `0x5227f603…` came. `0x28c6c062…` carried EIP-7702 code from 20:20:59 on 29 October until a
    transaction signed with its own key cleared it at 00:10:35 on 30 October; the chain does not show who held that key.
- **It had been done twice before.**
  - The temporary implementation and the action contract were created on 21 April 2026 (transaction
    `0x079984c56c5670108f5c6f664904178f9b364340351949a42e4637d1f645f770`), when the same mechanism moved 30,765.667402 ETH from
    `0x5d3919f12bcc35c26eee5f8226a9bee90c257ccc` to the same `…0DA0` address.
  - On 15 June 2026 the same two contracts were used a third time, by the DAO's L1 Timelock rather than the Council (transaction
    `0xc2e247e5869aaf5b57ff1cc5da8b56f6675161ad6f980b547846f209e43e145b`, block 25,322,204): an unsigned transaction in the name of
    `…0DA0` (its nonce 0) moved 30,765.617401709 ETH to `0x3b87db6ded35ebd28ecbf8014fb325eef23f6c07`, a Safe that needs 5 of 9
    signatures, has never executed a transaction and still holds the ETH. About 0.05 ETH stayed at `…0DA0`.
  - Each of the three uses switched the Inbox and switched it back inside one Ethereum transaction.
- **Who can move the funds now.**
  - `…0DA0` has no code and has sent one transaction in its history, the unsigned one of 15 June; no signature has ever left it.
  - On Ethereum, two executors of the UpgradeExecutor have run this exact path: the DAO's L1 Timelock (15 June) and the Council Safe
    (21 April and 30 October; 9 of 12 signatures, no timelock). Both still hold the role, and the UpgradeExecutor checks only that
    role: nothing in the contracts limits which sender the action names.
  - The action contract and the temporary implementation are still deployed, byte-identical to 21 April, and Arbitrum Nova's Inbox
    sits behind the same UpgradeExecutor.
- **The Council's other actions in 2026.** The Council Safe executed nothing from 25 September 2024 to 21 April 2026, then five
  transactions in 192 days:
  - 21 April (above);
  - 24 May: an upgrade of Arbitrum One's L1 Bridge (`0x8315177ab297ba92a06054ce80a67ed4dbd7ed3a`) whose new code rejects one call, an
    L2-to-L1 message calling renounceRole(PROPOSER_ROLE) on the L1 Timelock; still live;
  - 17 July: two members swapped through the Safe's only module, the UpgradeExecutor, after a Council vote on Arbitrum One; the
    timelock copies of the same update ran on 4 August and changed nothing;
  - 2 October: the pause executor added as the third executor;
  - 30 October (above).
  All five were submitted by one non-member address, `0x10590a5c93e8695bdb134c22f04c4d5b50755dc4`; each carries nine valid owner
  signatures, and two keys signed all five.

## Reported by the parties and the press, not checked by us

- The Council's notice of 30 October says the address is "identified with" the Binance exploit; it does not say who made that
  identification. Its notice of 21 April names the KelpDAO exploiter.
- The 30 October notice says the funds can be moved only by an ArbitrumDAO governance vote. That is a governance commitment, not a
  contract rule (see "Who can move the funds now").
- The 24 May upgrade is described by the Council as interim.
- The amended DAO proposal behind the 15 June transaction calls the receiving Safe the "Aave LLC receiving address" (per the Arbitrum
  forum). Its text gave 30,765.667501709 ETH, the figure from the 21 April notice; the chain amount was 30,765.667401709.
- Etherscan shows a "Binance 54" name tag for `0xb38e8c17…` on Ethereum (a community label, attributed, not adopted).
- CoinDesk reports that the FBI attributed the Binance hack to North Korea's TraderTraitor group on 31 October. Neither
  `0x3e2bf1ac…` nor `0x5227f603…` is in the FBI's list of 608 Ethereum addresses published that day (archived copy of 3 November;
  this absence is our check of the list, not a statement about who controls the addresses).

## Two clocks

On 27 October the Control Map read the ARB token on Ethereum (row 59, block 26,285,184). It recorded the token's proxy admin
`0x5613af04…`. It did not read that admin's owner, the UpgradeExecutor's roles or the Inbox, and its `owner()` entry for the token
was labelled as an RPC error although the call reverts (see "Correction"). No EXIT reader or radar watched the Inbox. The table shows
when each fact became readable on chain, and how long before the 30 October transaction.

| What was readable | On chain since | Before the 30 October transaction |
|---|---|---|
| The action contract and the temporary Inbox implementation deployed (first use) | 21 April 2026 | 192 days |
| The same mechanism used by the DAO's L1 Timelock | 15 June 2026, block 25,322,204 | 137 days |
| The pause executor added as the third executor | 2 October 2026 | 28 days |
| The ARB token's proxy admin recorded by the Control Map; the whole path readable at the same block | 27 October 2026, block 26,285,184 | 3 days |
| `0x5227f603…` frozen by USDT, then USDC | 29 October 2026, 21:01:35 and 21:04:59 | 3 hours 7 minutes and 3 hours 4 minutes |
| The 74,559,805.2 ARB reached `0x3e2bf1ac…` on Arbitrum One | 29 October 2026, 21:36:30 | 2 hours 32 minutes |
| The Council transaction on Ethereum | 30 October 2026, 00:08:35 | — |
| Both messages executed on Arbitrum One | 30 October 2026, 00:18:20 | 9 minutes 45 seconds after |

## What this shows, and what it does not

- **The chain shows who could use the path.** On Arbitrum One, "only the key holder can move an address's funds" holds only up to
  whoever controls the upgrade path, and that path, its holders, their threshold and the timelock were readable on chain before each
  of the three uses.
- **The chain does not judge the actions.** They were taken by the bodies Arbitrum's governance designates and announced publicly.
  Recording them is not a verdict on anyone.
- **Not covered here:**
  - Arbitrum Nova beyond the shared UpgradeExecutor;
  - what happens to the funds at `…0DA0` and at the 15 June receiving Safe;
  - the funds beyond the first hop of each freeze;
  - who controls any address.

## Correction

No correction to this note so far. Two corrections to EXIT's own earlier records came out of this case:

- The 27 October ARB row recorded the token's `owner()` as "NOT_OBSERVED (RPC error; cause not established)". The call reverts at
  every block read because the token has no such function; it is not a provider failure. The same label is on 20 other Control Map
  rows, all reverts (STATUS known issue); the reader fix is in progress.
- The stablecoin rows stop at the first hop: the USDC row did not record the blacklister role that froze the address.

Before this note was published, the first version of the case result file had the 21 April amount wrong (on chain: 30,765.667402
ETH). Its log records were held before admission and replaced by records bound to the corrected file. The list of corrections is in
[CORRECTIONS.md](../CORRECTIONS.md).

## Evidence

All facts were read from Ethereum mainnet and Arbitrum One on 3 November 2026 from two public providers per chain, without keys;
a fact was kept only when both replies agreed. The raw replies and their SHA-256 hashes are kept. The case result file is
[arbitrum-security-council-2026-10-30.json](arbitrum-security-council-2026-10-30.json); its SHA-256 is the `result_sha256` of
every log record below. A read-only script that re-reads the main facts from two providers per chain:
[arbitrum-security-council-2026-10-30-reread.py](arbitrum-security-council-2026-10-30-reread.py)
(`python3 arbitrum-security-council-2026-10-30-reread.py`; standard library only, prints each check and exits 0 only if all pass).
The same facts were posted on X on 3 November 2026 ([thread](https://x.com/exitprotocolL/status/2117613055689285717)).

| Evidence-log record | Block | Leaf |
|---|---|---|
| Inbox before the first use (21 April) | 24,925,592 | [375](https://exit-protocol.io/log/proofs/462/00000375.json) |
| Inbox at the Control Map read (27 October) | 26,285,184 | [372](https://exit-protocol.io/log/proofs/462/00000372.json) |
| Inbox at the block before the 30 October transaction | 26,301,885 | [373](https://exit-protocol.io/log/proofs/462/00000373.json) |
| Inbox at the 30 October transaction | 26,301,886 | [374](https://exit-protocol.io/log/proofs/462/00000374.json) |
| USDT freeze of `0x5227f603…` | 26,300,954 | [376](https://exit-protocol.io/log/proofs/462/00000376.json) |
| USDC freeze of `0x5227f603…` | 26,300,971 | [377](https://exit-protocol.io/log/proofs/462/00000377.json) |

| What | Transaction or contract |
|---|---|
| The 30 October Council transaction | [0xb69c81…55d6](https://etherscan.io/tx/0xb69c81774f507d46ce776aeaed8b4d31df96dd66ce6fd05073481011835355d6), block 26,301,886 |
| ARB transfer executed on Arbitrum One | [0x75e81a…edb6](https://arbiscan.io/tx/0x75e81a231a86e26a61e22dd2e6521504873a71a7ac1b2143c06e52796ceeedb6), block 519,514,683 |
| ETH payment executed on Arbitrum One | [0x410af1…5f70](https://arbiscan.io/tx/0x410af166c81f9c0f26cc19b4d970c984f526225eeea2aea169179856fd615f70), block 519,514,685 |
| ARB to `0x5227f603…` on Arbitrum One | [0xa18e57…edff](https://arbiscan.io/tx/0xa18e57027dae90de066ac093bbb4ae3d63598accbe5175cdf4195c686462edff), block 519,462,549 |
| ARB to `0x3e2bf1ac…` on Arbitrum One | [0x07a5a4…b6bf](https://arbiscan.io/tx/0x07a5a47ba3cfc61098be74eb462e353fe462cb8ee11a7a7e476fb8672facb6bf), block 519,477,782 |
| First use of the mechanism (21 April) | [0x079984…f770](https://etherscan.io/tx/0x079984c56c5670108f5c6f664904178f9b364340351949a42e4637d1f645f770) |
| Use by the DAO's L1 Timelock (15 June) | [0xc2e247…145b](https://etherscan.io/tx/0xc2e247e5869aaf5b57ff1cc5da8b56f6675161ad6f980b547846f209e43e145b), block 25,322,204 |
| Inbox (proxy) | `0x4dbd4fc535ac27206064b68ffcf827b0a60bab3f` |
| Inbox proxy admin | `0x554723262467f125ac9e1cdfa9ce15cc53822dbd` |
| UpgradeExecutor | `0x3fffbadaf827559da092217e474760e2b2c3cedd` |
| Security Council Safe | `0xf06e95ef589d9c38af242a8aaee8375f14023f85` |
| L1 Timelock | `0xe6841d92b0c345144506576ec13ecf5103ac7f49` |
| Pause executor | `0x30668ee252a28986ee6dc21b26e4018ac0e339b9` |
| Action contract | `0x3d456fcd62f5babcf3263b72fb4ac8ff8cc5a322` |
| Temporary Inbox implementation | `0x980d1f93fc5809c828539c46084801673fa6a859` |
| Usual Inbox implementation | `0x7c058ad1d0ee415f7e7f30e62db1bcf568470a10` |
| ARB token on Ethereum and its proxy admin | `0xb50721bcf8d664c30412cfbc6cf7a15145234ad1`, `0x5613af0474eb9c528a34701a5b1662e3c8fa0678` |
| Submitter of the five 2026 Council transactions | `0x10590a5c93e8695bdb134c22f04c4d5b50755dc4` |

The twelve Council owners at block 26,285,184 and the nine signers of each 2026 Council transaction are listed in the case result
file. Sources: Arbitrum Security Council notices of
[21 April](https://forum.arbitrum.foundation/t/security-council-emergency-action-21-04-2026/30803) and
[30 October 2026](https://forum.arbitrum.foundation/t/security-council-emergency-action-30-10-2026/31625); CoinDesk, 3 November 2026.

EXIT does not attribute any key or account to a person or organization.
