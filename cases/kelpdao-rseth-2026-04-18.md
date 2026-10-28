# Kelp DAO rsETH, 18 April 2026: a one-verifier receive path, who set it, and when

EXIT Protocol · 28 October 2026 · all times UTC

On 18 April 2026 the rsETH LayerZero adapter on Ethereum mainnet released 116,500 rsETH to one address, about $292 million at
the time as reported. The release came from a message on the path with LayerZero endpoint id 30320, which LayerZero's published
list assigns to Unichain. We re-read Ethereum mainnet with one question: what did the chain show about this path's
configuration before the release, and when?

The parties dispute the causes and who is responsible, including in a civil claim filed in September 2026. Below, what we read
on chain is kept apart from what the parties and the press report. The second part is attributed and was not checked by us.

Terms used below:
- A Safe is a multi-signature wallet contract.
- An EOA (externally owned account) is an ordinary address controlled by one private key.
- A DVN is a verifier contract that LayerZero uses to confirm that a message was sent on the other chain.
- Confirmations are the source-chain blocks waited before a message is verified.
- The peer is the contract on the other chain whose messages the adapter accepts.

## What the chain shows

Every item below was re-read from Ethereum mainnet on 28 October 2026.

- **Who could change the path's verifier settings.**
  - On LayerZero's EndpointV2, an application's receive settings are set by its **delegate**, which can differ from the
    contract's `owner()`.
  - The adapter `0x85d456b2…` was deployed on 6 February 2024, with the deploying EOA `0x1f7a03b7…` as both owner and delegate.
    Its owner moved to Safe `0xcbcdd778…` on 12 February 2024 and has been that Safe ever since. The delegate stayed the
    deploying EOA, which was also one of the Safe's owners at that time.
  - On 2 January 2025 the Safe ran `setDelegate` twice: at 13:51:47 it re-set the deploying EOA, and at 13:52:35 it made EOA
    `0xcf7bf9d3…` the adapter's delegate. `0xcf7bf9d3…` has never been one of the Safe's owners. At that time the Safe needed 2
    of its 6 owners to sign; from 11 February 2025 it needed 3 of 6.
  - The delegate stayed that EOA until 25 August 2025 at 14:49:47, when the Safe made itself the delegate.
  - So from 2 January to 25 August 2025, one key outside the Safe's threshold could change the adapter's verifier settings
    alone, with no timelock.
- **The path's verifier setting.**
  - On 2 April 2025 at 08:14:47 (block 22,179,964) the delegate EOA called `setConfig` directly. For endpoint id 30320 it set one
    required verifier (DVN `0x589dedbd…`), no optional verifiers and 42 confirmations. That was one hour after the peer for this
    path had been set.
  - Before that block the path used the receive library's default configuration: 20 confirmations and a single required
    verifier, `0x747c7414…`, whose verified source code is published under the name `DeadDVN`. The receive library's owner at the
    time, Safe `0xcda8e3ad…`, set that default on 10 February 2025. It is still the default today.
  - So the working one-verifier setting with `0x589dedbd…` was the adapter's own value, sent by its delegate, not the library
    default. The chain does not show who recommended that value.
  - An archive read at the release block returns the same setting: one required verifier, none optional, 42 confirmations.
  - From 2 April 2025 to the release, 308 messages from endpoint id 30320 were received on this path, the release included.
- **The other paths.**
  - On 19 March 2024 two other paths (endpoint ids 30260 and 30243) were set to two required verifiers, and on 21 March 2024 both
    were changed to one, `0x589dedbd…`. The deploying EOA, then the delegate, sent both changes directly.
  - Between 13 July 2025 and 1 April 2026 eight more paths were set to one required verifier, `0x589dedbd…`. Up to 18 August
    2025 the delegate EOA sent these directly; from 15 September 2025 they went through the Safe.
  - At the release block, 24 of the adapter's 26 configured paths required only DVN `0x589dedbd…`; only endpoint ids 30217 and
    30325 had two. The most recent one-verifier path was set through the Safe on 1 April 2026, 17 days before.
  - No timelock sat between the delegate and these settings.
- **The release (18 April 2026).**
  - 11:05:35: the receiving address `0x8b1b6c9a…` received 0.0978 ETH in a withdrawal from a contract whose verified source code
    is published under the name `TornadoCash_Eth_01`. This does not show who controls the receiving address.
  - 17:33:35: account `0xd95d7761…` (266,368 transactions in its history) submitted DVN `0x589dedbd…`'s attestation, with two
    signatures, of a message with nonce 308 from the Unichain path's peer. Its payload sends 116,500 rsETH to `0x8b1b6c9a…`. It is
    the only attestation of this message in the seven days of logs we scanned. On Ethereum, the last delivered message on this
    path before it was nonce 307, on 16 April.
  - 17:35:11: account `0x49662606…`, which has sent 6 transactions in its whole history, committed the verification. That
    records it on the endpoint so that the message can be delivered; any account may send this call. The commit cleared the
    DVN's attestation record, which the receive library does only for a verifier in the path's effective configuration.
  - 17:35:35 (block 24,908,285): the same account `0x49662606…` delivered the message to the adapter through EndpointV2, and the
    adapter transferred 116,500 rsETH, 120 seconds after the attestation.
  - 17:37:23 to 17:41:59: seven rsETH transfers left `0x8b1b6c9a…`. The first sent 53,000 rsETH to `0x1f4c1c2e…`. We did not
    trace the funds further.
- **After the release.**
  - 17:56:23: EOA `0x1c294e1c…` called `pause()` on an unverified contract, `0x6706618c…`. Its relation to the release was not
    established.
  - 18:18:11, 42 minutes after the release: transfers to or from ten addresses, `0x1f4c1c2e…` among them, were blocked in the rsETH
    contract through the adapter's owner Safe. The receiving address was not among them.
  - 18:21:59, 46 minutes after the release: eleven contracts, including the rsETH token contract, were paused in one transaction
    from a second Safe, `0xb6abb489…`, which is not the adapter's owner.
  - 18:23:11 (block 24,908,522): transfers to or from the receiving address were blocked until 19 April at 00:10:55.
  - A second message, nonce 309, paying 40,000 rsETH to the same address, followed. DVN `0x589dedbd…`'s attestation was submitted
    at 18:25:47 by `0xd3a22772…`, and `0x49662606…` committed it at 18:26:23. Both delivery attempts reverted, at 18:26:35 and
    18:28:11. A simulation of the delivery returns the rsETH error `TransfersBlocked` for the receiving address. In the blocks we
    scanned after the release (to block 24,930,000, about three days), only nonces 308 and 309 were verified from the Unichain
    peer on Ethereum. The endpoint's inbound nonce for this path is 320 today; how nonces 310 to 320 were used was not traced.
  - 19 April at 07:15:59: 40,373.72 rsETH was recovered from the adapter to `0xb3696a81…` (`FrozenFundsRecovered`), and a further
    35,972.45 rsETH on 12 September 2026.
  - On 23 April 2026 at 09:55:23 the Safe set 25 paths, endpoint id 30320 among them, to four required verifiers with 64
    confirmations. The peer for endpoint id 30320 was removed on 15 June 2026.
- **Today** (read on 28 October 2026). The adapter's owner and delegate are both the Safe, 3 of 6, after owner changes on 10 and
  23 July 2026. Endpoint id 30320 requires four verifiers with 64 confirmations, and the adapter now pins its own receive library.
  The library's default for endpoint id 30320 is still `DeadDVN`.

## Reported by the parties and the press, not checked by us

Each item below is what the named source says. We read these sources on 28 October 2026 and did not check their claims.

- **How the message was forged.** LayerZero says two RPC nodes that its DVN relied on were compromised and their software
  swapped, and a DDoS on the healthy nodes forced the DVN to fail over to them; the DVN then verified a message that was never
  sent ([CoinDesk](https://www.coindesk.com/tech/2026/04/20/layerzero-blames-kelp-s-setup-for-usd290-million-exploit-attributes-it-to-north-korea-s-lazarus),
  20 April 2026; [Nexus Mutual](https://nexusmutual.io/blog/kelpdao-layerzero-incident-report)).
  [QuillAudits](https://www.quillaudits.com/blog/hack-analysis/kelp-dao-hack) calls `0xd95d7761…` the DVN admin and says the
  real Unichain outbound nonce was 307. We did not read the Unichain side.
- **Who and when.** On 20 April LayerZero attributed the attack "with preliminary confidence" to North Korea's Lazarus Group and
  its TraderTraitor unit (CoinDesk, above). LayerZero's incident report
  ([LayerZero](https://layerzero.network/blog/layerzero-labs-kelpdao-incident-report), 20 May 2026) says the breach began on
  6 March 2026, when an attacker socially engineered a LayerZero Labs developer to harvest session keys, and that Mandiant,
  CrowdStrike and independent researchers attribute the attack to TraderTraitor, also known as UNC4899. Kelp's civil claim
  gives the same start date: a LayerZero developer's machine compromised on 6 March 2026 after social engineering
  ([Crypto Briefing](https://cryptobriefing.com/kelpdao-developer-sues-layerzero-ceo-over-292-million-exploit-and-blame-shifting/),
  [The Block](https://theblock.co/news/regulation/2026-09-25-kelpdao-sues-layerzero-claims-it-endorsed-setup-used-in-292-million-rseth-exploit-416361)).
- **The configuration dispute.**
  - LayerZero's statement of 19 April says: "Despite these recommendations, KelpDAO chose to utilize a 1/1 DVN configuration"
    ([LayerZero](https://layerzero.network/blog/kelpdao-incident-statement); CoinDesk, above).
    [The Defiant](https://thedefiant.io/news/hacks/layerzero-s-incident-report-says-kelp-downgraded-from-2-of-2-to-1-of-1-before-usd292m-exploit)
    headlines that LayerZero's report says Kelp downgraded from 2-of-2 to 1-of-1. We did not find that sentence in LayerZero's
    statement of 19 April or its report of 20 May. On chain, the Unichain path never required two verifiers: it went from the
    library default (`DeadDVN`) straight to one. The change from two required verifiers to one happened on two other paths
    (endpoint ids 30260 and 30243) on 21 March 2024.
  - Kelp says one-of-one is the configuration in LayerZero's documentation, shipped as the default for new OFT deployments, and
    that it was "affirmatively confirmed as appropriate" during its L2 expansion
    ([The Block](https://www.theblock.co/post/398204/kelp-dao-shifts-blame-layerzero), 20 April 2026;
    [CoinDesk](https://www.coindesk.com/tech/2026/04/20/kelp-dao-claims-layerzero-s-default-settings-are-what-actually-caused-the-usd290-million-disaster)).
    Its civil claim says LayerZero reviewed and endorsed its deployment and configuration in writing before the exploit
    ([Cointelegraph](https://cointelegraph.com/news/kelpdao-layerzero-lawsuit-rseth-exploit), 25 September 2026).
  - What we read on chain is above: the delegate EOA sent the one-verifier value for this path, and the receive library's
    default for this path was `DeadDVN`. The chain does not show what either party advised.
- **Follow-up attempts.** Nexus Mutual reports that the pause blocked two follow-up attempts totalling about $200 million;
  CoinDesk reports the same. In the blocks we scanned we find one more verified message on this path, nonce 309 (40,000 rsETH).
  Other paths and other chains were not checked. The label "LayerZero Labs DVN" for `0x589dedbd…` rests on the parties'
  statements and coverage; its verified contract name is only `DVN`.
- **Loss and spread.** About $292 million (Nexus Mutual, CoinDesk). The released rsETH was used as collateral to borrow on Aave;
  Cointelegraph reports about $195 million of Aave bad debt
  ([Cointelegraph](https://cointelegraph.com/news/layerzero-kelp-exploit-aave-loss), 20 April 2026), and Nexus Mutual gives
  scenarios from about $124 million to $230 million. Nexus Mutual also reports that the Arbitrum Security Council froze 30,766
  ETH linked to the attacker.
- **Court.** Evercrest Technologies, which operates KelpDAO, filed a notice of civil claim in the Supreme Court of British
  Columbia against two LayerZero Labs companies and a LayerZero co-founder, reported on 25 September 2026 (The Block, above). The
  co-founder said on X that the claim "continues to be meritless" (The Block).
- **Afterwards.** Kelp says it moved rsETH from LayerZero to Chainlink CCIP
  ([coin360](https://coin360.com/news/kelpdao-layerzero-exploit-chainlink-migration)).

## Two clocks

EXIT's Ethereum readers today read `owner()`, proxy slots, Safe owners and threshold, and AccessControl admins. They do not read
an EndpointV2 delegate or a LayerZero receive configuration, so no EXIT reader or radar ran here. The table only shows when each
fact became readable on chain, and how long before the release.

| What was readable | On chain since | Before the release |
|---|---|---|
| The delegate (the address that can call setConfig) is an EOA, not the owner Safe | 12 February 2024, 03:00:11, until 25 August 2025, 14:49:47 | ended about 236 days before |
| The delegate is an EOA that is not one of the Safe's owners | 2 January 2025, 13:52:35, until 25 August 2025, 14:49:47 | readable for 235 days; ended about 236 days before |
| Two paths changed from two required verifiers to one | 21 March 2024, 04:55:35 | about 758 days |
| Endpoint id 30320: one required verifier, none optional | 2 April 2025, 08:14:47 | about 381 days |
| The receiving address funded | 18 April 2026, 11:05:35 | 6 hours 30 minutes |
| Message nonce 308 attested | 18 April 2026, 17:33:35 | 120 seconds |
| Verification committed | 18 April 2026, 17:35:11 | 24 seconds |

## What this shows, and what it does not

- **The chain shows the configuration and which address sent it.** A verifier count, the delegate address and the absence of a
  timelock are configuration facts. Recording them is not a verdict on anyone.
- **The chain does not show why the configuration was chosen, or who recommended it.** That is the subject of the dispute.
- **What a reader would have shown.** A reader of `EndpointV2.delegates` and the receive library's per-path configuration would
  have shown, ahead of time: a delegate outside the Safe from January to August 2025; endpoint id 30320 on one required verifier
  for 381 days; and 24 of 26 paths on one verifier at the release, with the adapter holding more than 116,500 rsETH. On the day,
  a watch on the receive library had 120 seconds from attestation to release, or 24 seconds from commit to release. Telling
  that nonce 308 was forged needs the Unichain side, which EXIT does not read.
- **The response is on chain too.** The address blocks and the pause at 42 and 46 minutes stopped the nonce-309 message.
- **Not covered here:**
  - the Unichain side of the path (its outbound nonces were not read);
  - how nonces 310 to 320 on this path were used (the endpoint's inbound nonce is 320 today);
  - the funds after the seven transfers out of the receiving address, including the Aave positions;
  - the other 23 one-verifier paths' optional defaults;
  - who controls any address.
  Nothing here claims the release could have been stopped.

## Evidence

All facts were read from Ethereum mainnet on 28 October 2026. Most reads used a public RPC endpoint and a public explorer API;
the complete log histories were scanned (7,296 configuration logs and 277 default-configuration logs on the receive library,
8,228 delegate logs on EndpointV2). The state at past blocks (the setting at the release block and just before it) came from a
public archive endpoint, read without a key. The raw replies and their SHA-256 hashes are kept. Press and party statements are
linked where they are cited above.

| What | Transaction or contract |
|---|---|
| Adapter deployed | [0x8159af…4ba0](https://etherscan.io/tx/0x8159afd56d6a61bd121414700adbdb308595a4da0c9151a9efdee2def7774ba0), block 19,166,120 |
| Adapter owner moved to the Safe | [0x9d3fe9…beb](https://etherscan.io/tx/0x9d3fe94fe38b4366fbc964b3cbb8294d3ffd6c2432112a0bd2eeea074ee79beb), block 19,209,128 |
| Two paths set to two required verifiers | [0xf46f6b…c513](https://etherscan.io/tx/0xf46f6bf4e4b3b0bc40ffbdef20b3ed2566176cd9fe7900e774dd39fcc72fc513) |
| The same two paths set to one required verifier | [0xf64d02…e94f](https://etherscan.io/tx/0xf64d02e59234f08841eeeafd4668ff3c30581acc200a20330a51241f00a5e94f) |
| Receive-library default for endpoint id 30320 (`DeadDVN`), set by the library owner's Safe `0xcda8e3ad…` | [0x1ab0fd…e5](https://etherscan.io/tx/0x1ab0fd5a59770a92d7fb954540fb4cffdfefbadcf899aac0f0d4e68ba4beb7e5), block 21,818,650 |
| Delegate set to the EOA (through the Safe) | [0x06bafc…7314](https://etherscan.io/tx/0x06bafce7ad28e0078f1b4f5169ac90fc06a86fc9b6e6ba38dd25788351647314) |
| Endpoint id 30320 set to one required verifier (by the delegate) | [0x2d48d9…592](https://etherscan.io/tx/0x2d48d9331d96c46f8b4a9f7a7bdcf256d2034dadb42f039d27dc28077d520592), block 22,179,964 |
| Delegate moved to the Safe | [0x724162…e085](https://etherscan.io/tx/0x724162d2ba3038bb6016959a46ae6b839aa588bfba3c1c9a0311479902cfe085) |
| Last delivery before the release (nonce 307) | [0xc232af…0211](https://etherscan.io/tx/0xc232af35a6c98c92fdb0b08675e93d678994c2c97d31e133f909e0cb95960211), block 24,893,208 |
| Receiving address funded | [0xcb2ee4…f7ee](https://etherscan.io/tx/0xcb2ee450d6e770216dc3061750b4ac5b5fa494666bcf7eaa936411733e2ef7ee), block 24,906,342 |
| Nonce 308 attested | [0xfe5756…f0d6f](https://etherscan.io/tx/0xfe575668f895e10f8496fca3bb928fa53bebbea3e1de567d61bcd12d935f0d6f), block 24,908,275 |
| Verification committed | [0x68eb14…b564](https://etherscan.io/tx/0x68eb14e2d0ea9eca0f6277b6e4242c898a08d83a9ffe322dd875e69112e3b564), block 24,908,283 |
| Delivery and transfer of 116,500 rsETH | [0x1ae232…4222](https://etherscan.io/tx/0x1ae232da212c45f35c1525f851e4c41d529bf18af862d9ce9fd40bf709db4222), block 24,908,285 |
| Most recent one-verifier path, set through the Safe on 1 April 2026 | [0x53e538…e086](https://etherscan.io/tx/0x53e5389c75d592cc7f0e57b9b0d74303253d35f1357cf151e97166df0969e086) |
| Ten addresses blocked in rsETH (through the owner Safe) | [0x5ab849…c835](https://etherscan.io/tx/0x5ab8496916bac414affc3fdfbd2ab5be9e361ba14a0c92b8d25516d976e3c835), block 24,908,497 |
| Contracts paused (second Safe `0xb6abb489…`) | [0x4f5225…1698](https://etherscan.io/tx/0x4f52256ab6c8ab95d30cf994e0264f1de27e089764bb011824d5ddd47d9a1698), block 24,908,516 |
| Receiving address blocked (through the owner Safe) | [0xa1495d…25fc](https://etherscan.io/tx/0xa1495d12abdd7369bb92ecfc0cbdbdc2a7f631604f783abc1e985f3e682e25fc), block 24,908,522 |
| Nonce 309 attested | [0xa3e663…36b7](https://etherscan.io/tx/0xa3e663b98704def447350b7960d3824340e5c3bad538da529c3a7d21b48836b7), block 24,908,535 |
| Nonce 309 committed | [0xea851c…58aa](https://etherscan.io/tx/0xea851cd85ca45d7ca7012df929e4ef1c602d9a3de5ec93746aa8f24ccafb58aa), block 24,908,538 |
| Nonce 309 delivery attempts (both reverted) | [0x850953…3e53](https://etherscan.io/tx/0x8509533aed1c9257242b44447daf4fc5d0c562972f366c98cea92dc531783e53), block 24,908,539; [0x48d9b3…d792](https://etherscan.io/tx/0x48d9b3e8fc30c3780d3345743f5defc84ea57e5214ec9d3c4abd04f90465d792), block 24,908,547 |
| Four required verifiers set on 25 paths | [0xde7aa0…a5a240](https://etherscan.io/tx/0xde7aa019a29b999606335c16e60d445cfa3d25a2b9d4f565db5aed5eb1a5a240) |
| rsETH OFT adapter | `0x85d456b2dff1fd8245387c0bfb64dfb700e98ef3` |
| LayerZero EndpointV2 | `0x1a44076050125825900e736c501f859c50fe728c` |
| ReceiveUln302 (receive library) | `0xc02ab410f0734efa3f14628780e6e695156024c2` |
| The Safe that owns the adapter (and, since 25 August 2025, its delegate) | `0xcbcdd778aa25476f203814214dd3e9b9c46829a1` |
| DVN required on endpoint id 30320 at the release | `0x589dedbd617e0cbcb916a9223f4d1300c294236b` |
| Delegate EOA, 2 January to 25 August 2025 | `0xcf7bf9d3a485b9c4d4a38d65e4d68e081a585662` |
| Account that committed and delivered nonces 308 and 309 | `0x4966260619701a80637cdbdac6a6ce0131f8575e` |
| Account that submitted the nonce-308 attestation | `0xd95d7761a585bbc1b59b4b6f441b9edc2878dade` |
| Receiving address | `0x8b1b6c9a6db1304000412dd21ae6a70a82d60d3b` |
| Peer on the Unichain path at the release | `0xc3eacf0612346366db554c991d7858716db09f58` |

EXIT does not attribute any key or account to a person or organization.
