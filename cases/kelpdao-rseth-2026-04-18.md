# Kelp DAO rsETH, 18 April 2026: the receive configuration on chain, with times

EXIT Protocol · 28 October 2026 · all times UTC

> **This note records chain data and times only. It is not an accusation.** The parties involved disagree, in public and in
> court, about the causes and about who is responsible. This note takes no position on those questions. It attributes no intent
> or fault to anyone. It does not identify any person behind any address.

On 18 April 2026 the rsETH LayerZero adapter on Ethereum mainnet released 116,500 rsETH to one address. The release came from a
message on the path with LayerZero endpoint id 30320, which LayerZero's published list assigns to Unichain. We re-read Ethereum
mainnet with one question: what did the chain show about this path's configuration before the release, and when?

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
  - On 2 January 2025 at 13:52:35 the Safe made EOA `0xcf7bf9d3…`, which is not one of the Safe's owners, the adapter's delegate.
    At that time the Safe needed 2 of its 6 owners to sign; from 11 February 2025 it needed 3 of 6.
  - The delegate stayed that EOA until 25 August 2025 at 14:49:47, when the Safe made itself the delegate.
- **The path's verifier setting.**
  - On 2 April 2025 at 08:14:47 (block 22,179,964) the delegate EOA called `setConfig` directly. For endpoint id 30320 it set one
    required verifier (DVN `0x589dedbd…`), no optional verifiers and 42 confirmations. That was one hour after the peer for this
    path had been set.
  - Before that block the path used the receive library's default configuration. Its single required verifier is a contract
    whose verified source code is published under the name `DeadDVN`.
  - An archive read at the release block returns the same setting: one required verifier, none optional, 42 confirmations.
- **The other paths.**
  - On 21 March 2024 two other paths had changed from two required verifiers to one. The deploying EOA, then the delegate, sent
    that change.
  - At the release block, 24 of the adapter's 26 configured paths required only DVN `0x589dedbd…`. The most recent was set on
    1 April 2026, 17 days before.
  - No timelock sat between the delegate and these settings.
- **The release (18 April 2026).**
  - 11:05:35: the receiving address `0x8b1b6c9a…` received 0.0978 ETH in a withdrawal from a contract whose verified source code
    is published under the name `TornadoCash_Eth_01`. This does not show who controls the receiving address.
  - 17:33:35: DVN `0x589dedbd…` attested a message with nonce 308 from the Unichain path's peer. Its payload sends 116,500 rsETH to
    `0x8b1b6c9a…`. On Ethereum, the last delivered message on this path before it was nonce 307, on 16 April.
  - 17:35:11: the verification was committed, which records it on the endpoint so that the message can be delivered. Any
    account may send this call.
  - 17:35:35 (block 24,908,285): the message was delivered to the adapter through EndpointV2, and the adapter transferred
    116,500 rsETH, 120 seconds after the attestation.
- **After the release.**
  - 18:18:11: transfers to or from ten addresses were blocked for 24 hours in the rsETH contract. The receiving address was not
    among them.
  - 18:21:59: eleven contracts, including the rsETH token contract, were paused in one transaction from a second Safe,
    `0xb6abb489…`, which is not the adapter's owner.
  - 18:23:11 (block 24,908,522): transfers to or from the receiving address were blocked the same way.
  - A second message (nonce 309, 40,000 rsETH to the same address) was attested and committed after that. Both delivery attempts
    reverted, at 18:26:35 and 18:28:11.
  - On 23 April 2026 at 09:55:23 the Safe set 25 paths, endpoint id 30320 among them, to four required verifiers with 64
    confirmations. The peer for endpoint id 30320 was removed on 15 June 2026.
- **Today.** The adapter's owner and delegate are both the Safe, 3 of 6. Endpoint id 30320 requires four verifiers.

## Two clocks

EXIT's Ethereum readers today read `owner()`, proxy slots, Safe owners and threshold, and AccessControl admins. They do not read
an EndpointV2 delegate or a LayerZero receive configuration, so no EXIT reader or radar ran here. The table only shows when each
fact became readable on chain, and how long before the release.

| What was readable | On chain since | Before the release |
|---|---|---|
| The delegate (the address that can call setConfig) is an EOA, not the owner Safe | 12 February 2024, 03:00:11, until 25 August 2025, 14:49:47 | ended about 236 days before |
| Two paths changed from two required verifiers to one | 21 March 2024, 04:55:35 | about 759 days |
| Endpoint id 30320: one required verifier, none optional | 2 April 2025, 08:14:47 | about 381 days |
| The receiving address funded | 18 April 2026, 11:05:35 | 6 hours 30 minutes |
| Message nonce 308 attested | 18 April 2026, 17:33:35 | 120 seconds |
| Verification committed | 18 April 2026, 17:35:11 | 24 seconds |

## What this shows, and what it does not

- **The chain shows the configuration and which address sent it.** A verifier count, the delegate address and the absence of a
  timelock are configuration facts. Recording them is not a verdict on anyone.
- **The chain does not show why the configuration was chosen.** The parties dispute the causes. This note takes no position.
- **Not covered here:**
  - the Unichain side of the path (its outbound nonces were not read);
  - what the parties' own statements say about causes;
  - onward movements of the released rsETH;
  - who controls any address.
  Nothing here claims the release could have been stopped.

## Evidence

All facts were read from Ethereum mainnet. Most reads used a public RPC endpoint and a public explorer API. The state at past
blocks (the setting at the release block and just before it) came from a public archive endpoint, read without a key. The raw
replies and their SHA-256 hashes are kept.

| What | Transaction or contract |
|---|---|
| Adapter deployed | [0x8159af…4ba0](https://etherscan.io/tx/0x8159afd56d6a61bd121414700adbdb308595a4da0c9151a9efdee2def7774ba0), block 19,166,120 |
| Adapter owner moved to the Safe | [0x9d3fe9…beb](https://etherscan.io/tx/0x9d3fe94fe38b4366fbc964b3cbb8294d3ffd6c2432112a0bd2eeea074ee79beb), block 19,209,128 |
| Two paths set to two required verifiers | [0xf46f6b…c513](https://etherscan.io/tx/0xf46f6bf4e4b3b0bc40ffbdef20b3ed2566176cd9fe7900e774dd39fcc72fc513) |
| The same two paths set to one required verifier | [0xf64d02…e94f](https://etherscan.io/tx/0xf64d02e59234f08841eeeafd4668ff3c30581acc200a20330a51241f00a5e94f) |
| Delegate set to the EOA (through the Safe) | [0x06bafc…7314](https://etherscan.io/tx/0x06bafce7ad28e0078f1b4f5169ac90fc06a86fc9b6e6ba38dd25788351647314) |
| Receive-library default for endpoint id 30320 (`DeadDVN`) | [0x1ab0fd…e5](https://etherscan.io/tx/0x1ab0fd5a59770a92d7fb954540fb4cffdfefbadcf899aac0f0d4e68ba4beb7e5), block 21,818,650 |
| Endpoint id 30320 set to one required verifier (by the delegate) | [0x2d48d9…592](https://etherscan.io/tx/0x2d48d9331d96c46f8b4a9f7a7bdcf256d2034dadb42f039d27dc28077d520592), block 22,179,964 |
| Delegate moved to the Safe | [0x724162…e085](https://etherscan.io/tx/0x724162d2ba3038bb6016959a46ae6b839aa588bfba3c1c9a0311479902cfe085) |
| Last delivery before the release (nonce 307) | [0xc232af…0211](https://etherscan.io/tx/0xc232af35a6c98c92fdb0b08675e93d678994c2c97d31e133f909e0cb95960211), block 24,893,208 |
| Receiving address funded | [0xcb2ee4…f7ee](https://etherscan.io/tx/0xcb2ee450d6e770216dc3061750b4ac5b5fa494666bcf7eaa936411733e2ef7ee), block 24,906,342 |
| Nonce 308 attested | [0xfe5756…f0d6f](https://etherscan.io/tx/0xfe575668f895e10f8496fca3bb928fa53bebbea3e1de567d61bcd12d935f0d6f), block 24,908,275 |
| Verification committed | [0x68eb14…b564](https://etherscan.io/tx/0x68eb14e2d0ea9eca0f6277b6e4242c898a08d83a9ffe322dd875e69112e3b564), block 24,908,283 |
| Delivery and transfer of 116,500 rsETH | [0x1ae232…4222](https://etherscan.io/tx/0x1ae232da212c45f35c1525f851e4c41d529bf18af862d9ce9fd40bf709db4222), block 24,908,285 |
| Contracts paused (second Safe `0xb6abb489…`) | [0x4f5225…1698](https://etherscan.io/tx/0x4f52256ab6c8ab95d30cf994e0264f1de27e089764bb011824d5ddd47d9a1698), block 24,908,516 |
| Four required verifiers set on 25 paths | [0xde7aa0…a5a240](https://etherscan.io/tx/0xde7aa019a29b999606335c16e60d445cfa3d25a2b9d4f565db5aed5eb1a5a240) |
| rsETH OFT adapter | `0x85d456b2dff1fd8245387c0bfb64dfb700e98ef3` |
| LayerZero EndpointV2 | `0x1a44076050125825900e736c501f859c50fe728c` |
| ReceiveUln302 (receive library) | `0xc02ab410f0734efa3f14628780e6e695156024c2` |
| The Safe that owns the adapter (and, since 25 August 2025, its delegate) | `0xcbcdd778aa25476f203814214dd3e9b9c46829a1` |
| DVN required on endpoint id 30320 at the release | `0x589dedbd617e0cbcb916a9223f4d1300c294236b` |
| Peer on the Unichain path at the release | `0xc3eacf0612346366db554c991d7858716db09f58` |

EXIT does not attribute any key or account to a person or organization.
