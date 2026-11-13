# Control Surface: the Control Map, one view per deployment

This document regroups the published Control Map data by deployment and by read fact. It adds no reading of its own: every address, status word, time, per-row count and evidence link below is copied from the three published files listed under Sources, and the few derived values are computed from them by a fixed rule (Derived values). A value that the files do not give is written UNKNOWN. The same content as data: [control-surface.json](control-surface.json).

## Sources

| File | Format | sha256 |
|---|---|---|
| [control-map-nightly.json](https://exit-protocol.io/control-map/control-map-nightly.json) | exit.control-map-nightly/1 | `2ff53529f1df7386cf5756a1a90f50c44a70c5285cfa5c24bfeae9a68cfaeb1d` |
| [control-map.json](https://exit-protocol.io/control-map/control-map.json) | exit.control-map/1 | `5082287252821edb9ce1040550b3b90d930dba6c9e67730183adbd2511abf48a` |
| [daily.json](https://exit-protocol.io/control-map/daily/daily.json) | exit.control-map-daily-page/1 | `8f72c10f9e7b697d504ff83b230a2249571280ace7281ebc580962c269650161` |

Nightly file: night 2026-11-11, reads from 2026-11-11T23:20:12.532184+00:00 to 2026-11-11T23:23:42.939122+00:00. Daily runs: 12, from 2026-11-01 to 2026-11-12. First snapshot: token list from CoinGecko public API v3, market-cap order (coins/markets) and platform addresses (coins/list), retrieved coins-list 2026-10-27T16:26:38Z, markets 2026-10-27T16:26:35Z.

Not shown: the list fields `exit_list_label`, `exit_list_control_paths` that some rows of the nightly file carry; they are list entries, not read facts.

## What this view does not prove

Copied from the nightly file. In the copied texts of this document, "this page" means the Control Map page on the site, not this document; this document does not show the list label of rows 69 to 72 (see above).

- that a controlling address belongs to anyone in particular
- that an authority was or will be used
- that nothing outside the readers' declared scope exists
- the state after the stated slot or block
- that a second source confirmed a fact marked not compared, or any fact of a row marked not sampled
- that the label EXIT's row list gives rows 69 to 72 (shown under their names in this page's wording), or an address EXIT's row list names for them, is true: these are EXIT's own statements and were not read from the chain

Limits of the change records, copied from the daily file (basis: compared settings at successive producer-declared reads only; intervening changes are not reconstructed):

- known_at measures evidence knowledge, not an exact on-chain event time.
- Equal endpoints and clean daily samples cannot prove continuous control or exact days in force.
- A source/failed/partial/deferred/refused/gap state cannot silently inherit an uninterrupted span.

## Derived values

- `address_shown`: the fact's address; "none set" when the fact gives no address and its status word is OBSERVED_EMPTY; "zero address" when the fact gives no address and its status word is RETURNED_ZERO_ADDRESS; UNKNOWN for any other fact without an address.
- `change.last_change`: the change records of the daily runs for this row; UNKNOWN when none is recorded (the daily runs compare successive reads only).
- `counts`: counted over the subjects of this view.
- `first_snapshot`: the fact with the same field name and the same position among the facts of that name, in the same row (same chain and address) of control-map.json; UNKNOWN when the row or the fact is not there.
- `first_snapshot.same_address`: true or false when both facts give an address; UNKNOWN otherwise.
- `second_source.comparison`: "not compared (no first-read value)", the published word, when the fact is listed in second_source.facts_not_compared of the row with reason NO_FIRST_READ_VALUE; "compared" otherwise.
- `second_source.fact`: control:<field> on Solana, getter:<field> for an Ethereum getter, slot:eip1967_implementation or slot:zos_implementation for the implementation fields, and the admin slot of the same convention for "proxy admin"; "no single compared fact" when none of these names applies or the name is not among the facts the second read reported.
- `second_source.primary_equals_address`: for a compared fact, whether the first-read value that the second read compared equals the address of the fact shown (it can belong to an earlier night than the read shown); UNKNOWN for a fact that was not compared.

The address read is what the reader recorded for the field: for a Solana authority field or a proxy admin slot, the address set in it; for a getter, the address the call returned (a getter name is not a capability); for an implementation field, the address of the code, not a holder; for "Safe interface", the address that was asked; for "AccessControl DEFAULT_ADMIN_ROLE", the member that was returned. Read the status word with each address.

## Counts

- Deployments: 72 (ethereum-mainnet 48, solana-mainnet 24).
- Read facts: 297; with an address 174, "none set" 20, "zero address" 3, UNKNOWN 100.
- First snapshot: 68 of the 72 deployments are in it. Facts with the same address 168, another address 0, no address on one side 112, not in it 17.
- Daily change status: EQUAL_OBSERVED_SETTINGS 72; change records: 0.
- Second source: AGREES 53, SUPPLY_CHANGED_IN_WINDOW 7, not sampled 12; second read of the read shown: 12.
- Second-source cells of the read facts: compared 135, no single compared fact 76, not compared (no first-read value) 38, not sampled 48.
- Rows under the correction note: 21.

## Correction note

Copied from the nightly file ([corrections](https://github.com/ExitEvidenceLayer/exit-protocol-public/blob/main/CORRECTIONS.md)):

> The first snapshot labelled owner() on 21 Ethereum rows NOT_OBSERVED (RPC error; cause not established): rows 6, 9, 11, 14, 15, 18, 24, 27, 29, 32, 34, 38, 40, 42, 46, 52, 55, 56, 59, 61, 67. On these contracts owner() reverts; it was not a provider error. The nightly reader records what the call did, CALL_REVERTED, and names no holder. In this build 21 of the 21 rows read CALL_REVERTED. No other fact in the "What was read" column of these rows was affected. The first snapshot's second-source count on these rows ("6 facts") included owner(), which was not compared; see CORRECTIONS.md.

## Status words

Copied from the nightly file.

| Word | Shown in | Meaning |
|---|---|---|
| NONE_OBSERVED | proxy | the reader found no implementation address in the EIP-1967 or ZeppelinOS storage slots, and the code is not the canonical EIP-1167 clone. Other proxy designs are not read. |
| OBSERVED | proxy implementation, proxy admin | the storage slot of the named proxy convention held this address at the block. |
| UNKNOWN (empty admin slot; UUPS designs keep upgrade rights in the implementation) | proxy admin | the admin slot of the proxy convention was empty at the block; the reader does not read who can upgrade. |
| RETURNED_ADDRESS | owner() and, on row 4 (USDC), masterMinter(), pauser(), blacklister(), rescuer() | the call returned this address at the block. A getter name is not a capability. |
| RETURNED_ZERO_ADDRESS | the same getters | the call returned the zero address. |
| CALL_REVERTED | the same getters | the call reverted. This is what the call did; it names no holder. |
| SAFE_INTERFACE_ANSWERED | Safe interface | the address answered getOwners() and getThreshold(); the threshold and the number of owners are as returned. An interface answer, not proof of a Safe deployment or of who holds any owner key. |
| NOT_ANSWERED | Safe interface | getOwners() or getThreshold() reverted, failed with an invalid opcode or returned nothing: the address does not answer as a Safe. |
| CONTRACT (code present at the block) | Safe interface, after "account:" | the address held code at the block. |
| member(s) | AccessControl DEFAULT_ADMIN_ROLE | the contract declares the enumerable AccessControl interface and the address is a member of its default admin role at the block; the number is the member count the contract returned (at most four members are read). Other roles, role admins and history are not read. |
| NOT_ANSWERED | AccessControl | supportsInterface reverted, failed with an invalid opcode or returned nothing, or the contract does not declare the enumerable AccessControl interface. |
| OBSERVED_EMPTY | Solana authority fields | the mint account has this field and no address is set in it. |
| OBSERVED | Solana authority fields, in brackets | the field held the address shown. |
| multisig | Solana authority fields | the authority address is a token-program multisig account (reader status supported_multisig); threshold and number of signers are as stored in it. Who holds a signer key is not read. |
| system_owned_account | Solana authority fields | the authority address is an account owned by the system program. This does not show whether a private key can exist for the address or who controls it. |
| program_owned_unsupported | Solana authority fields | the authority address is an account owned by a program; its control structure is not read. |
| account_absent_at_pair_read | Solana authority fields | no account existed at the authority address when it was read together with the mint. |
| AGREES | Second source | every fact that was compared was equal at both sources. It says nothing about a fact that was not compared. |
| SUPPLY_CHANGED_IN_WINDOW | Second source | the token supply differed between the two slots and no other compared fact did. |
| CONFLICT | Second source | at the same block the two providers returned different values for a fact. Recorded, not judged. |
| CHANGED_OR_CONFLICT | Second source | a compared fact differed between the two slots: a change in between or a difference between providers; the read does not say which. |
| UNAVAILABLE | Second source | no fact of the row could be compared: the second provider gave no usable answer, or the row was not asked because the run had reached its time limit (code RUN_DEADLINE). |
| PRIMARY_NOT_OBSERVED | Second source | no fact of the row could be compared, because the first read observed no address in any of them. |
| not sampled | Second source | the row has not been drawn for a second read on any night used by this page. |
| not compared (no first-read value) | Second source | the first read observed no address in this authority field or getter (an authority that is not set, a getter that reverted or returned the zero address), so the second reply is not compared; where there was one, its hash is in the log record and the value is in control-map-nightly.json. |
| not compared (second read unavailable) | Second source | the second provider gave no usable answer for this fact. |
| second source returned a value the first read did not | Second source | the first read observed no address in this fact and the second provider returned one. Shown in full; not judged. |
| an older read than the one in this row | Second source | the newest second read of the row belongs to an earlier night than the read shown in the row. |
| second read of <date> compared an earlier value | Second source | the newest second read of the row belongs to an earlier night, and a fact it looked at has another value in the read shown in the row. The cell names the fact and prints no verdict; both values are in control-map-nightly.json. |
| second read unavailable that night | Second source | the row was drawn that night and no fact of it could be compared; the code in brackets is the job's own. |
| no log record | Second source | the second read compared no fact, so it made no log record. |
| no accepted read yet | What was read | the nightly run has not yet accepted a read of this row. |
| not answered | Read at (UTC) | the read of the build night obtained no answer (the code in brackets is the run's own); the row shows its last accepted read. |
| answer refused | Read at (UTC) | the answer of the build night failed the run's own replay check; the row shows its last accepted read. |
| read not accepted (comparison refused) | Read at (UTC) | the read of the build night could not be compared with the read before it and was not accepted; the row shows its last accepted read. |
| read not accepted (change deferred) | Read at (UTC) | the read of the build night was held back by the run's daily cap on change records; the row shows its last accepted read. |

## Deployments

### Row 1: Tether (USDT), ethereum-mainnet

`0xdac17f958d2ee523a2206206994597c13d831ec7` (market-cap rank at list time: 3)

- Read shown: night 2026-11-11, known at 2026-11-11T23:20:12.532184+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `1e6044f3583e284b01ea90e4b7264e477c9da4a8b967b8458d8b7d7ff2bf6a59`, [proof](https://exit-protocol.io/log/proofs/1135/00001051.json).
- First snapshot read: known at 2026-10-27T16:28:05.132999+00:00, position 26285152, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `299e9d08703c187cdabbe1525f81917074b0e4db2cec8f9cef074c804e38864f`, [proof](https://exit-protocol.io/log/proofs/134/00000068.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:20:12.187838+00:00 to 2026-11-12T23:20:12.578930+00:00 (6 clean equal comparisons, 6 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-08 (an earlier read than the one shown), https://eth.api.pocket.network against https://eth.drpc.org, mode same_block; facts compared 7, agree 7, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000875.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy | UNKNOWN | NONE_OBSERVED | no address: NONE_OBSERVED (EIP-1967 and ZeppelinOS slots) | no single compared fact |
| owner() | `0xc6cde7c39eb2f0f0095f41570af89efc2c1ea828` | RETURNED_ADDRESS | same address | AGREES (getter:owner(), 2026-11-08); earlier read, compared value equals the address shown |
| Safe interface | `0xc6cde7c39eb2f0f0095f41570af89efc2c1ea828` | NOT_ANSWERED (account: CONTRACT (code present at the block)) | same address | no single compared fact |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | no single compared fact |

### Row 2: Tether (USDT), solana-mainnet

`Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB` (market-cap rank at list time: 3)

- Read shown: night 2026-11-11, known at 2026-11-11T23:20:15.822203+00:00, slot 468305280, ACCEPTED_READ, policy `solana-finalized-mint-pair-hop/2`, provider https://solana-rpc.publicnode.com, result sha256 `0d6026eb1955ced14b70680e49f3943165f073687dc0f65c11a05d3e32ab3cd0`, [proof](https://exit-protocol.io/log/proofs/1135/00001052.json).
- First snapshot read: known at 2026-10-27T16:28:07.409715+00:00, position 462138152, policy `solana-finalized-mint-pair-hop/1`, result sha256 `07416e077238995db7172afc8c4da1af5468872a2789fa2e7fef914d343bf7ef`, [proof](https://exit-protocol.io/log/proofs/134/00000069.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-03T23:20:07.274647+00:00 to 2026-11-12T23:20:15.869678+00:00 (9 clean equal comparisons, 2 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-04 (an earlier read than the one shown), https://api.mainnet-beta.solana.com against https://solana-rpc.publicnode.com, mode window; facts compared 4, agree 4, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000540.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| mintAuthority | `Q6XprfkF8RQQKoQVG33xT88H7wi8Uk1B1CC7YAs69Gi` | multisig · 2-of-3, 3 signers (OBSERVED) | same address | AGREES (control:mintAuthority, 2026-11-04); earlier read, compared value equals the address shown |
| freezeAuthority | `Q6XprfkF8RQQKoQVG33xT88H7wi8Uk1B1CC7YAs69Gi` | multisig · 2-of-3, 3 signers (OBSERVED) | same address | AGREES (control:freezeAuthority, 2026-11-04); earlier read, compared value equals the address shown |

### Row 3: BNB (BNB), ethereum-mainnet

`0xb8c77482e45f1f44de1745f52c74426c631bdd52` (market-cap rank at list time: 4)

- Read shown: night 2026-11-11, known at 2026-11-11T23:20:18.693327+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `241f8ca5f5bff354b15df46b105d9da094ea160cfbdd36b8454690baccfbf0ef`, [proof](https://exit-protocol.io/log/proofs/1135/00001053.json).
- First snapshot read: known at 2026-10-27T16:28:10.058383+00:00, position 26285152, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `00ee386faf1cec087975884fbd06179dc27f2c36d137dab8b57c94a8c47eacef`, [proof](https://exit-protocol.io/log/proofs/134/00000070.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:20:18.470290+00:00 to 2026-11-12T23:20:18.940400+00:00 (6 clean equal comparisons, 6 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: not sampled (drawn from night 2026-11-02 on).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy | UNKNOWN | NONE_OBSERVED | no address: NONE_OBSERVED (EIP-1967 and ZeppelinOS slots) | not sampled |
| owner() | `0x00c5e04176d95a286fcce0e68c683ca0bfec8454` | RETURNED_ADDRESS | same address | not sampled |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | not sampled |

### Row 4: USDC (USDC), ethereum-mainnet

`0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48` (market-cap rank at list time: 6)

- Read shown: night 2026-11-11, known at 2026-11-11T23:20:22.061457+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `e151628b021848ffbbd684d17b2455eb2b342d63b4f1a5a9cb807d01affa916f`, [proof](https://exit-protocol.io/log/proofs/1135/00001054.json).
- First snapshot read: known at 2026-10-27T16:28:12.789463+00:00, position 26285152, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `77ed4d0c6bcc9f9dd28327bf5f769c1b6486f271d285cb59875c47ba82432ee6`, [proof](https://exit-protocol.io/log/proofs/134/00000071.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:20:21.878439+00:00 to 2026-11-12T23:20:22.357558+00:00 (6 clean equal comparisons, 10 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-10 (an earlier read than the one shown), https://eth.api.pocket.network against https://eth.drpc.org, mode same_block; facts compared 10, agree 10, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00001039.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy (ZeppelinOS) implementation | `0x43506849d7c04f9138d1a2050bbf3a0c054402dd` | OBSERVED | same address | AGREES (slot:zos_implementation, 2026-11-10); earlier read, compared value equals the address shown |
| proxy admin | `0x807a96288a1a408dbc13de2b1d087d10356395d2` | OBSERVED | same address | AGREES (slot:zos_admin, 2026-11-10); earlier read, compared value equals the address shown |
| owner() | `0xfcb19e6a322b27c06842a71e8c725399f049ae3a` | RETURNED_ADDRESS | same address | AGREES (getter:owner(), 2026-11-10); earlier read, compared value equals the address shown |
| masterMinter() | `0xe982615d461dd5cd06575bbea87624fda4e3de17` | RETURNED_ADDRESS | UNKNOWN | AGREES (getter:masterMinter(), 2026-11-10); earlier read, compared value equals the address shown |
| pauser() | `0x4914f61d25e5c567143774b76edbf4d5109a8566` | RETURNED_ADDRESS | UNKNOWN | AGREES (getter:pauser(), 2026-11-10); earlier read, compared value equals the address shown |
| blacklister() | `0x0a06be16275b95a7d2567fbdae118b36c7da78f9` | RETURNED_ADDRESS | UNKNOWN | AGREES (getter:blacklister(), 2026-11-10); earlier read, compared value equals the address shown |
| rescuer() | zero address | RETURNED_ZERO_ADDRESS | UNKNOWN | not compared (no first-read value): getter:rescuer(), second read of night 2026-11-10 |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | no single compared fact |

### Row 5: USDC (USDC), solana-mainnet

`EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` (market-cap rank at list time: 6)

- Read shown: night 2026-11-11, known at 2026-11-11T23:20:25.378666+00:00, slot 468305325, ACCEPTED_READ, policy `solana-finalized-mint-pair-hop/2`, provider https://solana-rpc.publicnode.com, result sha256 `c4d4216617a229c08a6e63ac6c5428d430bc888aefc48c3faeb5afa0e6b70ec9`, [proof](https://exit-protocol.io/log/proofs/1135/00001055.json).
- First snapshot read: known at 2026-10-28T06:55:11.728079+00:00, position 462382468, policy `solana-finalized-mint-pair-hop/1`, result sha256 `23e1b4b0dcbe3d16bb59a31ac977834c085456e37dbd1fe3822b876845476049`, [proof](https://exit-protocol.io/log/proofs/204/00000202.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-03T23:20:15.801581+00:00 to 2026-11-12T23:20:25.666073+00:00 (9 clean equal comparisons, 2 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: SUPPLY_CHANGED_IN_WINDOW, second read of night 2026-11-11 (the read shown), https://api.mainnet-beta.solana.com against https://solana-rpc.publicnode.com, mode window; facts compared 4, agree 3, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00001130.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| mintAuthority | `BJE5MMbqXjVwjAF7oxwPYXnTXDyspzZyt4vwenNw5ruG` | multisig · 2-of-4, 4 signers (OBSERVED) | same address | AGREES (control:mintAuthority, 2026-11-11) |
| freezeAuthority | `7dGbd2QZcCKcTndnHcTL8q7SMVXAkp688NTQYwrRCrar` | multisig · 2-of-4, 4 signers (OBSERVED) | same address | AGREES (control:freezeAuthority, 2026-11-11) |

### Row 6: USDS (USDS), ethereum-mainnet

`0xdc035d45d973e3ec169d2276ddab16f1e407384f` (market-cap rank at list time: 14)

- Read shown: night 2026-11-11, known at 2026-11-11T23:20:28.011705+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `181db4002523090f6ecfcd338f8b99559c9e4c530b5cede034a7820ad67c897b`, [proof](https://exit-protocol.io/log/proofs/1135/00001056.json).
- First snapshot read: known at 2026-10-27T16:28:17.803935+00:00, position 26285152, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `0db66cf793350ca6368db0135c54633f480bde562a9eab6a5c33fdc539db1259`, [proof](https://exit-protocol.io/log/proofs/134/00000072.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:20:27.937419+00:00 to 2026-11-12T23:20:28.433352+00:00 (6 clean equal comparisons, 5 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-04 (an earlier read than the one shown), https://eth.drpc.org against https://ethereum-rpc.publicnode.com, mode same_block; facts compared 6, agree 6, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000537.json).
- Correction note: this row is listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy (EIP-1967) implementation | `0x1923dfee706a8e78157416c29cbccfde7cdf4102` | OBSERVED | same address | AGREES (slot:eip1967_implementation, 2026-11-04); earlier read, compared value equals the address shown |
| proxy admin | UNKNOWN | UNKNOWN (empty admin slot; UUPS designs keep upgrade rights in the implementation) | no address: UNKNOWN (empty admin slot; UUPS designs keep upgrade rights in the implementation) | AGREES (slot:eip1967_admin, 2026-11-04); earlier read, compared with no address, as in the read shown |
| owner() | UNKNOWN | CALL_REVERTED | no address: NOT_OBSERVED (RPC error; cause not established) | not compared (no first-read value): getter:owner(), second read of night 2026-11-04 |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | no single compared fact |

### Row 7: USDS (USDS), solana-mainnet

`USDSwr9ApdHk5bvJKMjzff41FfuX8bSxdKcR81vTwcA` (market-cap rank at list time: 14)

- Read shown: night 2026-11-11, known at 2026-11-11T23:20:31.799030+00:00, slot 468305353, ACCEPTED_READ, policy `solana-finalized-mint-pair-hop/2`, provider https://solana-rpc.publicnode.com, result sha256 `a9b63de91edca3302a6f0ccc1af2f44424a0036ea9ba8574b662def29289fde0`, [proof](https://exit-protocol.io/log/proofs/1135/00001057.json).
- First snapshot read: known at 2026-10-27T16:28:20.090367+00:00, position 462138210, policy `solana-finalized-mint-pair-hop/1`, result sha256 `28f865d4305acc3612d0241deece8e7f4b665139c14e8edb2be8b8185af716ce`, [proof](https://exit-protocol.io/log/proofs/134/00000073.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-03T23:20:22.124303+00:00 to 2026-11-12T23:20:32.216044+00:00 (9 clean equal comparisons, 3 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-05 (an earlier read than the one shown), https://api.mainnet-beta.solana.com against https://solana-rpc.publicnode.com, mode window; facts compared 4, agree 4, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000626.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| mintAuthority | `BEvTHkTyXooyaJzP8egDUC7WQK8cyRrq5WvERZNWhuah` | program_owned_unsupported (OBSERVED) | same address | AGREES (control:mintAuthority, 2026-11-05); earlier read, compared value equals the address shown |
| freezeAuthority | `AYPtjx4Hc8us1ikULUedkmZ3wtiD6tmL7gK3qe4V3oHt` | system_owned_account (OBSERVED) | same address | AGREES (control:freezeAuthority, 2026-11-05); earlier read, compared value equals the address shown |

### Row 8: WhiteBIT Coin (WBT), ethereum-mainnet

`0x925206b8a707096ed26ae47c84747fe0bb734f59` (market-cap rank at list time: 15)

- Read shown: night 2026-11-11, known at 2026-11-11T23:20:34.573643+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `be3e0f49aa259c21ca5a18fe030b38686dfd1141071bc84911c001d7de8b60f5`, [proof](https://exit-protocol.io/log/proofs/1135/00001058.json).
- First snapshot read: known at 2026-10-27T16:28:22.788500+00:00, position 26285152, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `5c3dbd9c004b7e9fea067eecfda856dfaea8f37c878150def6844cef76e131dc`, [proof](https://exit-protocol.io/log/proofs/134/00000074.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:20:34.613779+00:00 to 2026-11-12T23:20:35.254377+00:00 (6 clean equal comparisons, 6 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-10 (an earlier read than the one shown), https://eth.api.pocket.network against https://eth.drpc.org, mode same_block; facts compared 7, agree 7, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00001040.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy | UNKNOWN | NONE_OBSERVED | no address: NONE_OBSERVED (EIP-1967 and ZeppelinOS slots) | no single compared fact |
| owner() | `0xd77d461d51d356569ee281795afd5eb62e2e8f0c` | RETURNED_ADDRESS | same address | AGREES (getter:owner(), 2026-11-10); earlier read, compared value equals the address shown |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | no single compared fact |

### Row 9: Chainlink (LINK), ethereum-mainnet

`0x514910771af9ca656af840dff83e8264ecf986ca` (market-cap rank at list time: 16)

- Read shown: night 2026-11-11, known at 2026-11-11T23:20:37.252775+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `497c5768ee47ded1e2fdd39ccb15e9337364a3c7f2ad5b95eb9d5b14cc536436`, [proof](https://exit-protocol.io/log/proofs/1135/00001059.json).
- First snapshot read: known at 2026-10-27T16:28:25.430309+00:00, position 26285152, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `e00c424bfb619bcc223fb50cb05e043f35778fba7e4abb8867dd4cd6c4a689e2`, [proof](https://exit-protocol.io/log/proofs/134/00000075.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:20:37.280244+00:00 to 2026-11-12T23:20:38.117973+00:00 (6 clean equal comparisons, 5 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-07 (an earlier read than the one shown), https://eth.api.pocket.network against https://eth.drpc.org, mode same_block; facts compared 6, agree 6, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000788.json).
- Correction note: this row is listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy | UNKNOWN | NONE_OBSERVED | no address: NONE_OBSERVED (EIP-1967 and ZeppelinOS slots) | no single compared fact |
| owner() | UNKNOWN | CALL_REVERTED | no address: NOT_OBSERVED (RPC error; cause not established) | not compared (no first-read value): getter:owner(), second read of night 2026-11-07 |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | no single compared fact |

### Row 10: Chainlink (LINK), solana-mainnet

`LinkhB3afbBKb2EQQu7s7umdZceV3wcvAUJhQAfQ23L` (market-cap rank at list time: 16)

- Read shown: night 2026-11-11, known at 2026-11-11T23:20:39.964769+00:00, slot 468305397, ACCEPTED_READ, policy `solana-finalized-mint-pair-hop/2`, provider https://solana-rpc.publicnode.com, result sha256 `456e64f8209ff995b5510787ccd6b89bda993f0ef566eb328d39041f234e3437`, [proof](https://exit-protocol.io/log/proofs/1135/00001060.json).
- First snapshot read: known at 2026-10-27T16:28:27.658107+00:00, position 462138246, policy `solana-finalized-mint-pair-hop/1`, result sha256 `e2c730b4f85701df6d02e36c8f85c99a7099eac490f2fcf3f04c4f62124f6109`, [proof](https://exit-protocol.io/log/proofs/134/00000076.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-03T23:20:29.996924+00:00 to 2026-11-12T23:20:40.809426+00:00 (9 clean equal comparisons, 2 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-11 (the read shown), https://api.mainnet-beta.solana.com against https://solana-rpc.publicnode.com, mode window; facts compared 4, agree 4, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00001131.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| mintAuthority | `BCk1GxBKRdoPX3hGXfKxbe6cLENAikuMts9eLxsM7A9S` | account_absent_at_pair_read (OBSERVED) | same address | AGREES (control:mintAuthority, 2026-11-11) |
| freezeAuthority | `GoFoFfEDgALWRTw5dSY3VZQSwbFpvBEhDv1sFAWzYpbf` | system_owned_account (OBSERVED) | same address | AGREES (control:freezeAuthority, 2026-11-11) |

### Row 11: LEO Token (LEO), ethereum-mainnet

`0x2af5d2ad76741191d15dfe7bf6ac92d4bd912ca3` (market-cap rank at list time: 17)

- Read shown: night 2026-11-11, known at 2026-11-11T23:20:42.574109+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `51c7d24c603a656bc50930f6acdf53eb72ff8cfedae07c1ee79868c6a588387d`, [proof](https://exit-protocol.io/log/proofs/1135/00001061.json).
- First snapshot read: known at 2026-10-27T16:28:30.253124+00:00, position 26285152, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `e77505eefb02cefba732d26e76cb355065eade4ec26f77dba8c9a90bf0b116fa`, [proof](https://exit-protocol.io/log/proofs/134/00000077.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:20:42.655194+00:00 to 2026-11-12T23:20:43.777452+00:00 (6 clean equal comparisons, 5 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-08 (an earlier read than the one shown), https://eth.api.pocket.network against https://eth.drpc.org, mode same_block; facts compared 6, agree 6, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000874.json).
- Correction note: this row is listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy | UNKNOWN | NONE_OBSERVED | no address: NONE_OBSERVED (EIP-1967 and ZeppelinOS slots) | no single compared fact |
| owner() | UNKNOWN | CALL_REVERTED | no address: NOT_OBSERVED (RPC error; cause not established) | not compared (no first-read value): getter:owner(), second read of night 2026-11-08 |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | no single compared fact |

### Row 12: Ethena USDe (USDE), ethereum-mainnet

`0x4c9edd5852cd905f086c759e8383e09bff1e68b3` (market-cap rank at list time: 23)

- Read shown: night 2026-11-11, known at 2026-11-11T23:20:45.483263+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `6c37604696e821239da8f4c72b5820b1e5c48bca34ed1a9205b93cd6ab07991f`, [proof](https://exit-protocol.io/log/proofs/1135/00001062.json).
- First snapshot read: known at 2026-10-27T16:28:33.041103+00:00, position 26285152, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `3742b0096b6ad8c7083ba736dc3e6592bd15a5e8d7f29d9e243f744034450330`, [proof](https://exit-protocol.io/log/proofs/134/00000078.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:20:45.585374+00:00 to 2026-11-12T23:20:46.713438+00:00 (6 clean equal comparisons, 6 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-04 (an earlier read than the one shown), https://eth.drpc.org against https://ethereum-rpc.publicnode.com, mode same_block; facts compared 7, agree 7, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000538.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy | UNKNOWN | NONE_OBSERVED | no address: NONE_OBSERVED (EIP-1967 and ZeppelinOS slots) | no single compared fact |
| owner() | `0xe8dc0fab349ea169283c48ccfd09d797e6db7c94` | RETURNED_ADDRESS | same address | AGREES (getter:owner(), 2026-11-04); earlier read, compared value equals the address shown |
| Safe interface | `0xe8dc0fab349ea169283c48ccfd09d797e6db7c94` | NOT_ANSWERED (account: CONTRACT (code present at the block)) | same address | no single compared fact |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | no single compared fact |

### Row 13: Ethena USDe (USDE), solana-mainnet

`DEkqHyPN7GMRJ5cArtQFAWefqbZb33Hyf6s5iCwjEonT` (market-cap rank at list time: 23)

- Read shown: night 2026-11-11, known at 2026-11-11T23:20:49.321028+00:00, slot 468305437, ACCEPTED_READ, policy `solana-finalized-mint-pair-hop/2`, provider https://solana-rpc.publicnode.com, result sha256 `17b0b7153aaecbe47a129853a656f12330916ac6476bfdae0f6c1dbd5f4df465`, [proof](https://exit-protocol.io/log/proofs/1135/00001063.json).
- First snapshot read: known at 2026-10-27T16:28:35.359056+00:00, position 462138280, policy `solana-finalized-mint-pair-hop/1`, result sha256 `a8428074807e1cd273692665aa29fb87bc73b3ccf013224f21137c09b62d7695`, [proof](https://exit-protocol.io/log/proofs/134/00000079.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-03T23:20:39.031219+00:00 to 2026-11-12T23:20:50.554575+00:00 (9 clean equal comparisons, 3 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-11 (the read shown), https://api.mainnet-beta.solana.com against https://solana-rpc.publicnode.com, mode window; facts compared 3, agree 3, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00001133.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| mintAuthority | `4x3oQtX4MhjTKGBeXDZbtTSLZ9cUWo5waN2UChAuthtS` | program_owned_unsupported (OBSERVED) | same address | AGREES (control:mintAuthority, 2026-11-11) |
| freezeAuthority | none set | OBSERVED_EMPTY | no address: OBSERVED_EMPTY | not compared (no first-read value): control:freezeAuthority, second read of night 2026-11-11 |

### Row 14: Dai (DAI), ethereum-mainnet

`0x6b175474e89094c44da98b954eedeac495271d0f` (market-cap rank at list time: 24)

- Read shown: night 2026-11-11, known at 2026-11-11T23:20:51.986271+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `cbb9789847ea39a23ca05dd2c1969b5cd96f52fb55deba8e6bab625ec3c84ddb`, [proof](https://exit-protocol.io/log/proofs/1135/00001064.json).
- First snapshot read: known at 2026-10-27T16:28:37.978650+00:00, position 26285152, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `bba32471e4aea2103fc3d0756cb9eeb9f594291ffec99712b86540e2c9bd915d`, [proof](https://exit-protocol.io/log/proofs/134/00000080.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:20:52.108789+00:00 to 2026-11-12T23:20:53.263673+00:00 (6 clean equal comparisons, 5 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-09 (an earlier read than the one shown), https://eth.api.pocket.network against https://eth.drpc.org, mode same_block; facts compared 6, agree 6, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000957.json).
- Correction note: this row is listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy | UNKNOWN | NONE_OBSERVED | no address: NONE_OBSERVED (EIP-1967 and ZeppelinOS slots) | no single compared fact |
| owner() | UNKNOWN | CALL_REVERTED | no address: NOT_OBSERVED (RPC error; cause not established) | not compared (no first-read value): getter:owner(), second read of night 2026-11-09 |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | no single compared fact |

### Row 15: Uniswap (UNI), ethereum-mainnet

`0x1f9840a85d5af5bf1d1762f925bdaddc4201f984` (market-cap rank at list time: 25)

- Read shown: night 2026-11-11, known at 2026-11-11T23:20:54.679783+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `cf58b5d331c711f952872319aceb9409b9641f6ea1c8227496c959bf9beda4c9`, [proof](https://exit-protocol.io/log/proofs/1135/00001065.json).
- First snapshot read: known at 2026-10-27T16:28:40.550136+00:00, position 26285152, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `a3f3736133099528f7d4fcdec9cdc301d4c22e3f7913ea1719103203c489218b`, [proof](https://exit-protocol.io/log/proofs/134/00000081.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:20:54.782206+00:00 to 2026-11-12T23:20:55.952014+00:00 (6 clean equal comparisons, 5 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-02 (an earlier read than the one shown), https://eth.drpc.org against https://ethereum-rpc.publicnode.com, mode same_block; facts compared 6, agree 6, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000363.json).
- Correction note: this row is listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy | UNKNOWN | NONE_OBSERVED | no address: NONE_OBSERVED (EIP-1967 and ZeppelinOS slots) | no single compared fact |
| owner() | UNKNOWN | CALL_REVERTED | no address: NOT_OBSERVED (RPC error; cause not established) | not compared (no first-read value): getter:owner(), second read of night 2026-11-02 |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | no single compared fact |

### Row 16: USD1 (USD1), ethereum-mainnet

`0x8d0d000ee44948fc98c9b98a4fa4921476f08b0d` (market-cap rank at list time: 29)

- Read shown: night 2026-11-11, known at 2026-11-11T23:20:57.763303+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `ec45b1037f82ac8d7ddcdef36e28c0757ed035cafeaaf594a5a64e42249adf21`, [proof](https://exit-protocol.io/log/proofs/1135/00001066.json).
- First snapshot read: known at 2026-10-27T16:28:43.466419+00:00, position 26285152, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `eee895398aca5caf8815d2e166b3327420c4ad3681957f6156cc02c28d7df3d7`, [proof](https://exit-protocol.io/log/proofs/134/00000082.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:20:57.948831+00:00 to 2026-11-12T23:20:59.208197+00:00 (6 clean equal comparisons, 6 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-10 (an earlier read than the one shown), https://eth.api.pocket.network against https://eth.drpc.org, mode same_block; facts compared 7, agree 7, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00001041.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy (EIP-1967) implementation | `0x694aa534bdef8ed63244eb902e7914e527891f08` | OBSERVED | same address | AGREES (slot:eip1967_implementation, 2026-11-10); earlier read, compared value equals the address shown |
| proxy admin | `0xa032fe6c496732bdfc0d235066f55f171fa4aece` | OBSERVED | same address | AGREES (slot:eip1967_admin, 2026-11-10); earlier read, compared value equals the address shown |
| owner() | `0xee9b1a09aedaced9dcda74964ea447feb93861c2` | RETURNED_ADDRESS | same address | AGREES (getter:owner(), 2026-11-10); earlier read, compared value equals the address shown |
| Safe interface | `0xa032fe6c496732bdfc0d235066f55f171fa4aece` | NOT_ANSWERED (account: CONTRACT (code present at the block)) | same address | no single compared fact |
| Safe interface | `0xee9b1a09aedaced9dcda74964ea447feb93861c2` | NOT_ANSWERED (account: CONTRACT (code present at the block)) | same address | no single compared fact |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | no single compared fact |

### Row 17: USD1 (USD1), solana-mainnet

`USD1ttGY1N17NEEHLmELoaybftRBUSErhqYiQzvEmuB` (market-cap rank at list time: 29)

- Read shown: night 2026-11-11, known at 2026-11-11T23:21:01.036458+00:00, slot 468305493, ACCEPTED_READ, policy `solana-finalized-mint-pair-hop/2`, provider https://solana-rpc.publicnode.com, result sha256 `88220c06c9670ae3791102ac78ace2e01be3e92d885935ae896d4da60d879f61`, [proof](https://exit-protocol.io/log/proofs/1135/00001067.json).
- First snapshot read: known at 2026-10-27T16:28:45.740921+00:00, position 462138330, policy `solana-finalized-mint-pair-hop/1`, result sha256 `06749d80ce00726393a865ffc4d65a5b58d74d97bee3e7097c68ef97bb9d7de4`, [proof](https://exit-protocol.io/log/proofs/134/00000083.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-03T23:20:50.221353+00:00 to 2026-11-12T23:21:02.523879+00:00 (9 clean equal comparisons, 2 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-11 (the read shown), https://api.mainnet-beta.solana.com against https://solana-rpc.publicnode.com, mode window; facts compared 4, agree 4, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00001134.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| mintAuthority | `BQh68x9D7TDqgJUXiJX1BsD1eR7kkV978owqwBEftpwK` | multisig · 1-of-4, 4 signers (OBSERVED) | same address | AGREES (control:mintAuthority, 2026-11-11) |
| freezeAuthority | `84ssq8Ud2WRzxVCuEmPa9xLPBUt4odmB8wuE8svZkh71` | system_owned_account (OBSERVED) | same address | AGREES (control:freezeAuthority, 2026-11-11) |

### Row 18: Gram (prev. Toncoin) (GRAM), ethereum-mainnet

`0x582d872a1b094fc48f5de31d3b73f2d9be47def1` (market-cap rank at list time: 31)

- Read shown: night 2026-11-11, known at 2026-11-11T23:21:03.654302+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `5ad9a9d20c7c4449b7e88d1fc876231867b2b3b970f65e2046df8561e6889fc8`, [proof](https://exit-protocol.io/log/proofs/1135/00001068.json).
- First snapshot read: known at 2026-10-27T16:28:48.317232+00:00, position 26285152, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `8a8a10484b41646b7fde022937ee7dfd3ccee5ab88276ad13dd61fa7313d0c90`, [proof](https://exit-protocol.io/log/proofs/134/00000084.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:21:03.861829+00:00 to 2026-11-12T23:21:05.442296+00:00 (6 clean equal comparisons, 5 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-07 (an earlier read than the one shown), https://eth.api.pocket.network against https://eth.drpc.org, mode same_block; facts compared 6, agree 6, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000787.json).
- Correction note: this row is listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy | UNKNOWN | NONE_OBSERVED | no address: NONE_OBSERVED (EIP-1967 and ZeppelinOS slots) | no single compared fact |
| owner() | UNKNOWN | CALL_REVERTED | no address: NOT_OBSERVED (RPC error; cause not established) | not compared (no first-read value): getter:owner(), second read of night 2026-11-07 |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | no single compared fact |

### Row 19: Tether Gold (XAUT), ethereum-mainnet

`0x68749665ff8d2d112fa859aa293f07a622782f38` (market-cap rank at list time: 33)

- Read shown: night 2026-11-11, known at 2026-11-11T23:21:06.803267+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `97e7ad2f0a47f81c76263ca75609eb3e0cc4bc1eaeddffa7b8d7aee3a317bf1b`, [proof](https://exit-protocol.io/log/proofs/1135/00001069.json).
- First snapshot read: known at 2026-10-27T16:28:51.272309+00:00, position 26285152, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `e70d9b7d6531651ac858d03c60eb8ee1521c3d18e20312cbae91b32353f6e8c4`, [proof](https://exit-protocol.io/log/proofs/134/00000085.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:21:07.119248+00:00 to 2026-11-12T23:21:08.745724+00:00 (6 clean equal comparisons, 6 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: not sampled (drawn from night 2026-11-02 on).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy (EIP-1967) implementation | `0x4c0d2c74a8d26f1e4f5653021c521f5471f9e566` | OBSERVED | same address | not sampled |
| proxy admin | `0x856fcc085290ac1e40392442211e6a333afb873e` | OBSERVED | same address | not sampled |
| owner() | `0xc6cde7c39eb2f0f0095f41570af89efc2c1ea828` | RETURNED_ADDRESS | same address | not sampled |
| Safe interface | `0x856fcc085290ac1e40392442211e6a333afb873e` | NOT_ANSWERED (account: CONTRACT (code present at the block)) | same address | not sampled |
| Safe interface | `0xc6cde7c39eb2f0f0095f41570af89efc2c1ea828` | NOT_ANSWERED (account: CONTRACT (code present at the block)) | same address | not sampled |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | not sampled |

### Row 20: Global Dollar (USDG), ethereum-mainnet

`0xe343167631d89b6ffc58b88d6b7fb0228795491d` (market-cap rank at list time: 34)

- Read shown: night 2026-11-11, known at 2026-11-11T23:21:09.684721+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `f2792d03883c991bd40613988375020f8f66f78e11b741d6fb7dfdb4baf406aa`, [proof](https://exit-protocol.io/log/proofs/1135/00001070.json).
- First snapshot read: known at 2026-10-27T16:28:54.080145+00:00, position 26285152, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `ed9cac9efa71e58b4a7ae6292205668bb26ddd7e16db74492da9a6db1c148398`, [proof](https://exit-protocol.io/log/proofs/134/00000086.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:21:10.044193+00:00 to 2026-11-12T23:21:11.877845+00:00 (6 clean equal comparisons, 6 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: not sampled (drawn from night 2026-11-02 on).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy (EIP-1967) implementation | `0xfacd5ff359adf87822374275699dd518aaf9a65f` | OBSERVED | same address | not sampled |
| proxy admin | UNKNOWN | UNKNOWN (empty admin slot; UUPS designs keep upgrade rights in the implementation) | no address: UNKNOWN (empty admin slot; UUPS designs keep upgrade rights in the implementation) | not sampled |
| owner() | `0x9036566eaa5f83e0b9e1161c6c602b0adf997654` | RETURNED_ADDRESS | same address | not sampled |
| Safe interface | `0x9036566eaa5f83e0b9e1161c6c602b0adf997654` | NOT_ANSWERED (account: CONTRACT (code present at the block)) | same address | not sampled |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | not sampled |

### Row 21: Global Dollar (USDG), solana-mainnet

`2u1tszSeqZ3qBWF3uNGPFc8TzMk2tdiwknnRMWGWjGWH` (market-cap rank at list time: 34)

- Read shown: night 2026-11-11, known at 2026-11-11T23:21:12.960205+00:00, slot 468305547, ACCEPTED_READ, policy `solana-finalized-mint-pair-hop/2`, provider https://solana-rpc.publicnode.com, result sha256 `047704f34757ee698f79350b24953927ec5e90b8419d09a6a4234e3bcca03214`, [proof](https://exit-protocol.io/log/proofs/1135/00001071.json).
- First snapshot read: known at 2026-10-28T06:55:16.945234+00:00, position 462382492, policy `solana-finalized-mint-pair-hop/1`, result sha256 `0152b304136c3a5e2857a5b9e5dd27b70b0c0920750b205a54cf971a50ff4874`, [proof](https://exit-protocol.io/log/proofs/204/00000203.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-03T23:21:02.176122+00:00 to 2026-11-12T23:21:15.160421+00:00 (9 clean equal comparisons, 11 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-07 (an earlier read than the one shown), https://api.mainnet-beta.solana.com against https://solana-rpc.publicnode.com, mode window; facts compared 13, agree 13, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000795.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| mintAuthority | `2e99QgqSDtiJSi5omGRVeZJuqNFRZdpy2YgG3mBd1AB4` | multisig · 1-of-5, 5 signers (OBSERVED) | same address | AGREES (control:mintAuthority, 2026-11-07); earlier read, compared value equals the address shown |
| freezeAuthority | `2apBGMsS6ti9RyF5TwQTDswXBWskiJP2LD4cUEDqYJjk` | system_owned_account (OBSERVED) | same address | AGREES (control:freezeAuthority, 2026-11-07); earlier read, compared value equals the address shown |
| confidentialTransferFeeConfig.authority | `2apBGMsS6ti9RyF5TwQTDswXBWskiJP2LD4cUEDqYJjk` | system_owned_account (OBSERVED) | same address | AGREES (control:confidentialTransferFeeConfig.authority, 2026-11-07); earlier read, compared value equals the address shown |
| confidentialTransferMint.authority | `2apBGMsS6ti9RyF5TwQTDswXBWskiJP2LD4cUEDqYJjk` | system_owned_account (OBSERVED) | same address | AGREES (control:confidentialTransferMint.authority, 2026-11-07); earlier read, compared value equals the address shown |
| metadataPointer.authority | `2apBGMsS6ti9RyF5TwQTDswXBWskiJP2LD4cUEDqYJjk` | system_owned_account (OBSERVED) | same address | AGREES (control:metadataPointer.authority, 2026-11-07); earlier read, compared value equals the address shown |
| mintCloseAuthority.closeAuthority | `2apBGMsS6ti9RyF5TwQTDswXBWskiJP2LD4cUEDqYJjk` | system_owned_account (OBSERVED) | same address | AGREES (control:mintCloseAuthority.closeAuthority, 2026-11-07); earlier read, compared value equals the address shown |
| permanentDelegate.delegate | `2apBGMsS6ti9RyF5TwQTDswXBWskiJP2LD4cUEDqYJjk` | system_owned_account (OBSERVED) | same address | AGREES (control:permanentDelegate.delegate, 2026-11-07); earlier read, compared value equals the address shown |
| tokenMetadata.updateAuthority | `2apBGMsS6ti9RyF5TwQTDswXBWskiJP2LD4cUEDqYJjk` | system_owned_account (OBSERVED) | same address | AGREES (control:tokenMetadata.updateAuthority, 2026-11-07); earlier read, compared value equals the address shown |
| transferFeeConfig.transferFeeConfigAuthority | `2apBGMsS6ti9RyF5TwQTDswXBWskiJP2LD4cUEDqYJjk` | system_owned_account (OBSERVED) | same address | AGREES (control:transferFeeConfig.transferFeeConfigAuthority, 2026-11-07); earlier read, compared value equals the address shown |
| transferFeeConfig.withdrawWithheldAuthority | `2apBGMsS6ti9RyF5TwQTDswXBWskiJP2LD4cUEDqYJjk` | system_owned_account (OBSERVED) | same address | AGREES (control:transferFeeConfig.withdrawWithheldAuthority, 2026-11-07); earlier read, compared value equals the address shown |
| transferHook.authority | `2apBGMsS6ti9RyF5TwQTDswXBWskiJP2LD4cUEDqYJjk` | system_owned_account (OBSERVED) | same address | AGREES (control:transferHook.authority, 2026-11-07); earlier read, compared value equals the address shown |

### Row 22: PayPal USD (PYUSD), ethereum-mainnet

`0x6c3ea9036406852006290770bedfcaba0e23a0e8` (market-cap rank at list time: 35)

- Read shown: night 2026-11-11, known at 2026-11-11T23:21:15.931164+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `61b4da6edcc46d4e0dc9afb16038a87b63f73ed7ee2d6c3b144cbb5c617949f6`, [proof](https://exit-protocol.io/log/proofs/1135/00001072.json).
- First snapshot read: known at 2026-10-27T16:28:59.028592+00:00, position 26285152, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `5f1fc40e9ba5aed4d795677f9b7b4b0185918ebb4d627b3c0d138ec7cc355053`, [proof](https://exit-protocol.io/log/proofs/134/00000087.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:21:16.360732+00:00 to 2026-11-12T23:21:18.266873+00:00 (6 clean equal comparisons, 6 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-08 (an earlier read than the one shown), https://eth.api.pocket.network against https://eth.drpc.org, mode same_block; facts compared 7, agree 7, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000873.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy (ZeppelinOS) implementation | `0x8c35caa5fd5bdc64b6b11344ad57594a3676256a` | OBSERVED | same address | AGREES (slot:zos_implementation, 2026-11-08); earlier read, compared value equals the address shown |
| proxy admin | `0xc94bcf6e1d8b3558e3b62e743630d50497e3851c` | OBSERVED | same address | AGREES (slot:zos_admin, 2026-11-08); earlier read, compared value equals the address shown |
| owner() | `0x3af3e85f4f97de7ad0f000b724fb77fe5ffc024b` | RETURNED_ADDRESS | same address | AGREES (getter:owner(), 2026-11-08); earlier read, compared value equals the address shown |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | no single compared fact |

### Row 23: PayPal USD (PYUSD), solana-mainnet

`2b1kV6DkPAnxd5ixfnxCpjxmKwqjjaYmCZfHsFu24GXo` (market-cap rank at list time: 35)

- Read shown: night 2026-11-11, known at 2026-11-11T23:21:19.202703+00:00, slot 468305577, ACCEPTED_READ, policy `solana-finalized-mint-pair-hop/2`, provider https://solana-rpc.publicnode.com, result sha256 `f681af27fc51af0e451476ea1ae930154e441a48143ad908125fcf1c1eb64226`, [proof](https://exit-protocol.io/log/proofs/1135/00001073.json).
- First snapshot read: known at 2026-10-27T16:29:01.292770+00:00, position 462138404, policy `solana-finalized-mint-pair-hop/1`, result sha256 `59316afb22c0f410d8d9333ff96eda84057c812580d03fc1ffb2f2a796d9275a`, [proof](https://exit-protocol.io/log/proofs/134/00000088.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-03T23:21:08.109475+00:00 to 2026-11-12T23:21:21.527151+00:00 (9 clean equal comparisons, 11 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-08 (an earlier read than the one shown), https://api.mainnet-beta.solana.com against https://solana-rpc.publicnode.com, mode window; facts compared 13, agree 13, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000882.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| mintAuthority | `AxJkHRY3puoofyj7Pn512M1SGBgWroXMkEdNPQypkzbu` | multisig · 1-of-5, 5 signers (OBSERVED) | same address | AGREES (control:mintAuthority, 2026-11-08); earlier read, compared value equals the address shown |
| freezeAuthority | `2apBGMsS6ti9RyF5TwQTDswXBWskiJP2LD4cUEDqYJjk` | system_owned_account (OBSERVED) | same address | AGREES (control:freezeAuthority, 2026-11-08); earlier read, compared value equals the address shown |
| confidentialTransferFeeConfig.authority | `2apBGMsS6ti9RyF5TwQTDswXBWskiJP2LD4cUEDqYJjk` | system_owned_account (OBSERVED) | same address | AGREES (control:confidentialTransferFeeConfig.authority, 2026-11-08); earlier read, compared value equals the address shown |
| confidentialTransferMint.authority | `2apBGMsS6ti9RyF5TwQTDswXBWskiJP2LD4cUEDqYJjk` | system_owned_account (OBSERVED) | same address | AGREES (control:confidentialTransferMint.authority, 2026-11-08); earlier read, compared value equals the address shown |
| metadataPointer.authority | `2apBGMsS6ti9RyF5TwQTDswXBWskiJP2LD4cUEDqYJjk` | system_owned_account (OBSERVED) | same address | AGREES (control:metadataPointer.authority, 2026-11-08); earlier read, compared value equals the address shown |
| mintCloseAuthority.closeAuthority | `2apBGMsS6ti9RyF5TwQTDswXBWskiJP2LD4cUEDqYJjk` | system_owned_account (OBSERVED) | same address | AGREES (control:mintCloseAuthority.closeAuthority, 2026-11-08); earlier read, compared value equals the address shown |
| permanentDelegate.delegate | `2apBGMsS6ti9RyF5TwQTDswXBWskiJP2LD4cUEDqYJjk` | system_owned_account (OBSERVED) | same address | AGREES (control:permanentDelegate.delegate, 2026-11-08); earlier read, compared value equals the address shown |
| tokenMetadata.updateAuthority | `2apBGMsS6ti9RyF5TwQTDswXBWskiJP2LD4cUEDqYJjk` | system_owned_account (OBSERVED) | same address | AGREES (control:tokenMetadata.updateAuthority, 2026-11-08); earlier read, compared value equals the address shown |
| transferFeeConfig.transferFeeConfigAuthority | `2apBGMsS6ti9RyF5TwQTDswXBWskiJP2LD4cUEDqYJjk` | system_owned_account (OBSERVED) | same address | AGREES (control:transferFeeConfig.transferFeeConfigAuthority, 2026-11-08); earlier read, compared value equals the address shown |
| transferFeeConfig.withdrawWithheldAuthority | `2apBGMsS6ti9RyF5TwQTDswXBWskiJP2LD4cUEDqYJjk` | system_owned_account (OBSERVED) | same address | AGREES (control:transferFeeConfig.withdrawWithheldAuthority, 2026-11-08); earlier read, compared value equals the address shown |
| transferHook.authority | `2apBGMsS6ti9RyF5TwQTDswXBWskiJP2LD4cUEDqYJjk` | system_owned_account (OBSERVED) | same address | AGREES (control:transferHook.authority, 2026-11-08); earlier read, compared value equals the address shown |

### Row 24: Quant (QNT), ethereum-mainnet

`0x4a220e6096b25eadb88358cb44068a3248254675` (market-cap rank at list time: 37)

- Read shown: night 2026-11-11, known at 2026-11-11T23:21:21.816244+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `03767b3eada86f813e1b8e58b4aeb93662ae00023d8f41e2395d250f53f8fb89`, [proof](https://exit-protocol.io/log/proofs/1135/00001074.json).
- First snapshot read: known at 2026-10-27T16:29:03.872768+00:00, position 26285152, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `7345db373ab34644367864087505c98dd9ca4904b3775779977e91645c8cccd7`, [proof](https://exit-protocol.io/log/proofs/134/00000089.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:21:22.207152+00:00 to 2026-11-12T23:21:24.332476+00:00 (6 clean equal comparisons, 5 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: not sampled (drawn from night 2026-11-02 on).
- Correction note: this row is listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy | UNKNOWN | NONE_OBSERVED | no address: NONE_OBSERVED (EIP-1967 and ZeppelinOS slots) | not sampled |
| owner() | UNKNOWN | CALL_REVERTED | no address: NOT_OBSERVED (RPC error; cause not established) | not sampled |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | not sampled |

### Row 25: Ethena (ENA), ethereum-mainnet

`0x57e114b691db790c35207b2e685d4a43181e6061` (market-cap rank at list time: 38)

- Read shown: night 2026-11-11, known at 2026-11-11T23:21:24.683048+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `e7eac87ca5385423b69a51dcb1cfb89fcc2ce1ebdd998381ed3b6f27346e7915`, [proof](https://exit-protocol.io/log/proofs/1135/00001075.json).
- First snapshot read: known at 2026-10-27T16:29:06.653586+00:00, position 26285152, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `2a5dd63df4c4406b2e0a091a1cbd4d816433ddf21e372e32c40682cf853aacc6`, [proof](https://exit-protocol.io/log/proofs/134/00000090.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:21:25.071680+00:00 to 2026-11-12T23:21:27.347761+00:00 (6 clean equal comparisons, 6 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-03 (an earlier read than the one shown), https://eth.drpc.org against https://ethereum-rpc.publicnode.com, mode same_block; facts compared 7, agree 7, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000454.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy | UNKNOWN | NONE_OBSERVED | no address: NONE_OBSERVED (EIP-1967 and ZeppelinOS slots) | no single compared fact |
| owner() | `0xe8dc0fab349ea169283c48ccfd09d797e6db7c94` | RETURNED_ADDRESS | same address | AGREES (getter:owner(), 2026-11-03); earlier read, compared value equals the address shown |
| Safe interface | `0xe8dc0fab349ea169283c48ccfd09d797e6db7c94` | NOT_ANSWERED (account: CONTRACT (code present at the block)) | same address | no single compared fact |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | no single compared fact |

### Row 26: Ethena (ENA), solana-mainnet

`72QvBVwpxqmheEPfaCwWSWqEFsUy3rhWt6JhQBMNTwD1` (market-cap rank at list time: 38)

- Read shown: night 2026-11-11, known at 2026-11-11T23:21:28.495547+00:00, slot 468305616, ACCEPTED_READ, policy `solana-finalized-mint-pair-hop/2`, provider https://solana-rpc.publicnode.com, result sha256 `a39351cd2ce71d020c963a312df0cbc78d04faa514d65e5d64cb1d1285355567`, [proof](https://exit-protocol.io/log/proofs/1135/00001076.json).
- First snapshot read: known at 2026-10-27T16:29:08.958718+00:00, position 462138440, policy `solana-finalized-mint-pair-hop/1`, result sha256 `e610a618c3379387fe5bcdc4d3b9db52cc70b65f9af70693b750e4b4e51142fb`, [proof](https://exit-protocol.io/log/proofs/134/00000091.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-03T23:21:18.685362+00:00 to 2026-11-12T23:21:31.179686+00:00 (9 clean equal comparisons, 3 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-10 (an earlier read than the one shown), https://api.mainnet-beta.solana.com against https://solana-rpc.publicnode.com, mode window; facts compared 3, agree 3, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00001050.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| mintAuthority | `D2hZiYnFqNS9YgNRoDtK7zajKjxc68139niZ1MmD8aae` | program_owned_unsupported (OBSERVED) | same address | AGREES (control:mintAuthority, 2026-11-10); earlier read, compared value equals the address shown |
| freezeAuthority | none set | OBSERVED_EMPTY | no address: OBSERVED_EMPTY | not compared (no first-read value): control:freezeAuthority, second read of night 2026-11-10 |

### Row 27: Shiba Inu (SHIB), ethereum-mainnet

`0x95ad61b0a150d79219dcf64e1e6cc01f0b64c4ce` (market-cap rank at list time: 39)

- Read shown: night 2026-11-11, known at 2026-11-11T23:21:31.111561+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `13f8607412af13cc4ac64fee6b6d6880ddfc55a3fd620ed5be9e77790df6218f`, [proof](https://exit-protocol.io/log/proofs/1135/00001077.json).
- First snapshot read: known at 2026-10-27T16:29:11.580851+00:00, position 26285152, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `8fe0856692397fed9986834a7ac6b7f5b37377703b1f81ce468720e6673d3962`, [proof](https://exit-protocol.io/log/proofs/134/00000092.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:21:31.536968+00:00 to 2026-11-12T23:21:34.007346+00:00 (6 clean equal comparisons, 5 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-11 (the read shown), https://eth.api.pocket.network against https://eth.drpc.org, mode same_block; facts compared 6, agree 6, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00001126.json).
- Correction note: this row is listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy | UNKNOWN | NONE_OBSERVED | no address: NONE_OBSERVED (EIP-1967 and ZeppelinOS slots) | no single compared fact |
| owner() | UNKNOWN | CALL_REVERTED | no address: NOT_OBSERVED (RPC error; cause not established) | not compared (no first-read value): getter:owner(), second read of night 2026-11-11 |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | no single compared fact |

### Row 28: Cronos (CRO), ethereum-mainnet

`0xa0b73e1ff0b80914ab6fe0444e65848c4c34450b` (market-cap rank at list time: 40)

- Read shown: night 2026-11-11, known at 2026-11-11T23:21:34.066698+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `26ebf7944cb0b5b35e5e0e3b85f13c114de5fc6b6bdb935be234a424968c5aa7`, [proof](https://exit-protocol.io/log/proofs/1135/00001078.json).
- First snapshot read: known at 2026-10-27T16:29:14.356696+00:00, position 26285184, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `3bd3549456f4d2275d6e8c43dec57c15760bba7b5ca2ef99cc2e6d23f82ed7bc`, [proof](https://exit-protocol.io/log/proofs/134/00000093.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:21:34.545907+00:00 to 2026-11-12T23:21:36.989653+00:00 (6 clean equal comparisons, 6 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-02 (an earlier read than the one shown), https://eth.drpc.org against https://ethereum-rpc.publicnode.com, mode same_block; facts compared 7, agree 7, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000362.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy | UNKNOWN | NONE_OBSERVED | no address: NONE_OBSERVED (EIP-1967 and ZeppelinOS slots) | no single compared fact |
| owner() | `0x3a39867b3dbc8a9dd55c4073e87cdab065430945` | RETURNED_ADDRESS | same address | AGREES (getter:owner(), 2026-11-02); earlier read, compared value equals the address shown |
| Safe interface | `0x3a39867b3dbc8a9dd55c4073e87cdab065430945` | NOT_ANSWERED (account: CONTRACT (code present at the block)) | same address | no single compared fact |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | no single compared fact |

### Row 29: Ripple USD (RLUSD), ethereum-mainnet

`0x8292bb45bf1ee4d140127049757c2e0ff06317ed` (market-cap rank at list time: 41)

- Read shown: night 2026-11-11, known at 2026-11-11T23:21:36.746559+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `67d64c9a54303b7ebbe10aaf9ae51f361512c2f24131be602e8f1546527daa95`, [proof](https://exit-protocol.io/log/proofs/1135/00001079.json).
- First snapshot read: known at 2026-10-27T16:29:17.027234+00:00, position 26285184, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `8dc6fedf4bf7b8b69c12ad5cedbd199ac83c42e7579540d1b98cee0eec6b1dc9`, [proof](https://exit-protocol.io/log/proofs/134/00000094.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:21:37.275755+00:00 to 2026-11-12T23:21:39.736463+00:00 (6 clean equal comparisons, 5 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-05 (an earlier read than the one shown), https://eth.drpc.org against https://ethereum-rpc.publicnode.com, mode same_block; facts compared 6, agree 6, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000624.json).
- Correction note: this row is listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy (EIP-1967) implementation | `0x9747a0d261c2d56eb93f542068e5d1e23170fa9e` | OBSERVED | same address | AGREES (slot:eip1967_implementation, 2026-11-05); earlier read, compared value equals the address shown |
| proxy admin | UNKNOWN | UNKNOWN (empty admin slot; UUPS designs keep upgrade rights in the implementation) | no address: UNKNOWN (empty admin slot; UUPS designs keep upgrade rights in the implementation) | AGREES (slot:eip1967_admin, 2026-11-05); earlier read, compared with no address, as in the read shown |
| owner() | UNKNOWN | CALL_REVERTED | no address: NOT_OBSERVED (RPC error; cause not established) | not compared (no first-read value): getter:owner(), second read of night 2026-11-05 |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | no single compared fact |

### Row 30: Circle USYC (USYC), ethereum-mainnet

`0x136471a34f6ef19fe571effc1ca711fdb8e49f2b` (market-cap rank at list time: 43)

- Read shown: night 2026-11-11, known at 2026-11-11T23:21:39.615813+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `acf4f1c0291ce6919f2f13c14ae181ca56dae99a9e9c35a1395842602f26dc74`, [proof](https://exit-protocol.io/log/proofs/1135/00001080.json).
- First snapshot read: known at 2026-10-27T16:29:19.800971+00:00, position 26285184, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `43aebdf21bfbcdd310d4e09f5923f870ab9c1878cc6cf2dee0608f21f250c441`, [proof](https://exit-protocol.io/log/proofs/134/00000095.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:21:40.160693+00:00 to 2026-11-12T23:21:42.660577+00:00 (6 clean equal comparisons, 6 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-07 (an earlier read than the one shown), https://eth.api.pocket.network against https://eth.drpc.org, mode same_block; facts compared 7, agree 7, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000790.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy (EIP-1967) implementation | `0xbf0f2f3aad6b99893d80c550fbacec915545eb92` | OBSERVED | same address | AGREES (slot:eip1967_implementation, 2026-11-07); earlier read, compared value equals the address shown |
| proxy admin | UNKNOWN | UNKNOWN (empty admin slot; UUPS designs keep upgrade rights in the implementation) | no address: UNKNOWN (empty admin slot; UUPS designs keep upgrade rights in the implementation) | AGREES (slot:eip1967_admin, 2026-11-07); earlier read, compared with no address, as in the read shown |
| owner() | `0x13ff8cabb86edf94a2df4f98773bda4005182dd6` | RETURNED_ADDRESS | same address | AGREES (getter:owner(), 2026-11-07); earlier read, compared value equals the address shown |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | no single compared fact |

### Row 31: Circle USYC (USYC), solana-mainnet

`7LWanZteUKtvFjv4MHYgKXXdAuCQYFPJysL9pxxdRQGn` (market-cap rank at list time: 43)

- Read shown: night 2026-11-11, known at 2026-11-11T23:21:43.454605+00:00, slot 468305684, ACCEPTED_READ, policy `solana-finalized-mint-pair-hop/2`, provider https://solana-rpc.publicnode.com, result sha256 `46fc77f21548bea61931ebab9c444646d488b39bc32c3864a15dcf61ee00c7b2`, [proof](https://exit-protocol.io/log/proofs/1135/00001081.json).
- First snapshot read: known at 2026-10-27T16:29:22.092826+00:00, position 462138500, policy `solana-finalized-mint-pair-hop/1`, result sha256 `d724a94e40bd2c359690515bbffd7d8392513f7021ccd3629c962390c124bfab`, [proof](https://exit-protocol.io/log/proofs/134/00000096.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-03T23:21:33.023772+00:00 to 2026-11-12T23:21:46.499172+00:00 (9 clean equal comparisons, 12 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-10 (an earlier read than the one shown), https://api.mainnet-beta.solana.com against https://solana-rpc.publicnode.com, mode window; facts compared 14, agree 14, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00001049.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| mintAuthority | `DZ7j2YLDq7847t2HtCWaDQUTpLJ4BinPGsY8w9Aai63y` | program_owned_unsupported (OBSERVED) | same address | AGREES (control:mintAuthority, 2026-11-10); earlier read, compared value equals the address shown |
| freezeAuthority | `DZ7j2YLDq7847t2HtCWaDQUTpLJ4BinPGsY8w9Aai63y` | program_owned_unsupported (OBSERVED) | same address | AGREES (control:freezeAuthority, 2026-11-10); earlier read, compared value equals the address shown |
| confidentialTransferFeeConfig.authority | `EMMxaez3JFNMRFdKZgnC3KtZck6gmSS4n6AMHXUMvPZL` | system_owned_account (OBSERVED) | same address | AGREES (control:confidentialTransferFeeConfig.authority, 2026-11-10); earlier read, compared value equals the address shown |
| confidentialTransferMint.authority | `EMMxaez3JFNMRFdKZgnC3KtZck6gmSS4n6AMHXUMvPZL` | system_owned_account (OBSERVED) | same address | AGREES (control:confidentialTransferMint.authority, 2026-11-10); earlier read, compared value equals the address shown |
| metadataPointer.authority | `532g6pYdfV5fx1CK4AuTHVjdYrTiq2AZfpu4Jk4rVJLb` | system_owned_account (OBSERVED) | same address | AGREES (control:metadataPointer.authority, 2026-11-10); earlier read, compared value equals the address shown |
| mintCloseAuthority.closeAuthority | `DZ7j2YLDq7847t2HtCWaDQUTpLJ4BinPGsY8w9Aai63y` | program_owned_unsupported (OBSERVED) | same address | AGREES (control:mintCloseAuthority.closeAuthority, 2026-11-10); earlier read, compared value equals the address shown |
| permanentDelegate.delegate | `DZ7j2YLDq7847t2HtCWaDQUTpLJ4BinPGsY8w9Aai63y` | program_owned_unsupported (OBSERVED) | same address | AGREES (control:permanentDelegate.delegate, 2026-11-10); earlier read, compared value equals the address shown |
| tokenMetadata.updateAuthority | `532g6pYdfV5fx1CK4AuTHVjdYrTiq2AZfpu4Jk4rVJLb` | system_owned_account (OBSERVED) | same address | AGREES (control:tokenMetadata.updateAuthority, 2026-11-10); earlier read, compared value equals the address shown |
| transferFeeConfig.transferFeeConfigAuthority | `EMMxaez3JFNMRFdKZgnC3KtZck6gmSS4n6AMHXUMvPZL` | system_owned_account (OBSERVED) | same address | AGREES (control:transferFeeConfig.transferFeeConfigAuthority, 2026-11-10); earlier read, compared value equals the address shown |
| transferFeeConfig.withdrawWithheldAuthority | `EMMxaez3JFNMRFdKZgnC3KtZck6gmSS4n6AMHXUMvPZL` | system_owned_account (OBSERVED) | same address | AGREES (control:transferFeeConfig.withdrawWithheldAuthority, 2026-11-10); earlier read, compared value equals the address shown |
| transferHook.authority | `DZ7j2YLDq7847t2HtCWaDQUTpLJ4BinPGsY8w9Aai63y` | program_owned_unsupported (OBSERVED) | same address | AGREES (control:transferHook.authority, 2026-11-10); earlier read, compared value equals the address shown |
| pausableConfig.authority | `EMMxaez3JFNMRFdKZgnC3KtZck6gmSS4n6AMHXUMvPZL` | system_owned_account (OBSERVED) | UNKNOWN | AGREES (control:pausableConfig.authority, 2026-11-10); earlier read, compared value equals the address shown |

### Row 32: Ondo US Dollar Yield (USDY), ethereum-mainnet

`0x96f6ef951840721adbf46ac996b59e0235cb985c` (market-cap rank at list time: 44)

- Read shown: night 2026-11-11, known at 2026-11-11T23:21:46.433725+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `527b0e0f028dd877ba3c218b940d810c5e122b4b3212aad3af0c4090f7945ac8`, [proof](https://exit-protocol.io/log/proofs/1135/00001082.json).
- First snapshot read: known at 2026-10-27T16:29:24.997729+00:00, position 26285184, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `8f83e23f5c819baf9f584adbd952c49a2bc3dbfbaeb0d25a28ed4fbb44f665fb`, [proof](https://exit-protocol.io/log/proofs/134/00000097.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:21:46.944595+00:00 to 2026-11-12T23:21:49.562843+00:00 (6 clean equal comparisons, 6 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-03 (an earlier read than the one shown), https://eth.drpc.org against https://ethereum-rpc.publicnode.com, mode same_block; facts compared 6, agree 6, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000452.json).
- Correction note: this row is listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy (EIP-1967) implementation | `0xea0f7eebdc2ae40edfe33bf03d332f8a7f617528` | OBSERVED | same address | AGREES (slot:eip1967_implementation, 2026-11-03); earlier read, compared value equals the address shown |
| proxy admin | `0x3ed61633057da0bc58f84b2b9002845e56f94c19` | OBSERVED | same address | AGREES (slot:eip1967_admin, 2026-11-03); earlier read, compared value equals the address shown |
| owner() | UNKNOWN | CALL_REVERTED | no address: NOT_OBSERVED (RPC error; cause not established) | not compared (no first-read value): getter:owner(), second read of night 2026-11-03 |
| Safe interface | `0x3ed61633057da0bc58f84b2b9002845e56f94c19` | NOT_ANSWERED (account: CONTRACT (code present at the block)) | same address | no single compared fact |
| AccessControl DEFAULT_ADMIN_ROLE | `0x1a694a09494e214a3be3652e4b343b7b81a73ad7` | 1 member(s) | same address | no single compared fact |

### Row 33: Ondo US Dollar Yield (USDY), solana-mainnet

`A1KLoBrKBde8Ty9qtNQUtq3C2ortoC3u7twggz7sEto6` (market-cap rank at list time: 44)

- Read shown: night 2026-11-11, known at 2026-11-11T23:21:49.733203+00:00, slot 468305715, ACCEPTED_READ, policy `solana-finalized-mint-pair-hop/2`, provider https://solana-rpc.publicnode.com, result sha256 `7ce1ee53a8ef392cd248dbcb999f7655b4ca5648ff839f5ffb9d3cce0d6343e0`, [proof](https://exit-protocol.io/log/proofs/1135/00001083.json).
- First snapshot read: known at 2026-10-27T16:29:27.256921+00:00, position 462138523, policy `solana-finalized-mint-pair-hop/1`, result sha256 `5a73cb3995075a9c1d947589aca82db572c983c77906e914410b3d47914d32c3`, [proof](https://exit-protocol.io/log/proofs/134/00000098.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-03T23:21:39.185834+00:00 to 2026-11-12T23:21:52.898890+00:00 (9 clean equal comparisons, 2 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-07 (an earlier read than the one shown), https://api.mainnet-beta.solana.com against https://solana-rpc.publicnode.com, mode window; facts compared 4, agree 4, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000797.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| mintAuthority | `8n2uiRUd1A9NN78PKESkJe6k6zMqtKCZh3MrK1j9qkB1` | multisig · 1-of-2, 2 signers (OBSERVED) | same address | AGREES (control:mintAuthority, 2026-11-07); earlier read, compared value equals the address shown |
| freezeAuthority | `51QVCuHfL1FeNjd8BDeffCKhCcAYoULnVB3yjNhShiuK` | system_owned_account (OBSERVED) | same address | AGREES (control:freezeAuthority, 2026-11-07); earlier read, compared value equals the address shown |

### Row 34: OKB (OKB), ethereum-mainnet

`0x75231f58b43240c9718dd58b4967c5114342a86c` (market-cap rank at list time: 45)

- Read shown: night 2026-11-11, known at 2026-11-11T23:21:52.360481+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `d3589c5519f08f32db0352dd9c649386c03e9ec13834cdfb47b5c3c25e880635`, [proof](https://exit-protocol.io/log/proofs/1135/00001084.json).
- First snapshot read: known at 2026-10-27T16:29:29.847415+00:00, position 26285184, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `8df04dcf4153afbb68f9218c5ba57c7d199d29dc106c8dda79083cb45576b7bb`, [proof](https://exit-protocol.io/log/proofs/134/00000099.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:21:52.911823+00:00 to 2026-11-12T23:21:55.779319+00:00 (6 clean equal comparisons, 5 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-09 (an earlier read than the one shown), https://eth.api.pocket.network against https://eth.drpc.org, mode same_block; facts compared 6, agree 6, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000960.json).
- Correction note: this row is listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy (ZeppelinOS) implementation | `0x81a4eea0ab6dd6a010b7318a662a43d0ca25e094` | OBSERVED | same address | AGREES (slot:zos_implementation, 2026-11-09); earlier read, compared value equals the address shown |
| proxy admin | UNKNOWN | UNKNOWN (empty admin slot; UUPS designs keep upgrade rights in the implementation) | no address: UNKNOWN (empty admin slot; UUPS designs keep upgrade rights in the implementation) | AGREES (slot:zos_admin, 2026-11-09); earlier read, compared with no address, as in the read shown |
| owner() | UNKNOWN | CALL_REVERTED | no address: NOT_OBSERVED (RPC error; cause not established) | not compared (no first-read value): getter:owner(), second read of night 2026-11-09 |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | no single compared fact |

### Row 35: Bitway (BTW), ethereum-mainnet

`0x3a63de3572c69a1307ff08394f3ee7702c16d25d` (market-cap rank at list time: 46)

- Read shown: night 2026-11-11, known at 2026-11-11T23:21:55.204920+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `ac268449d86236aba32512e76d0d653066a26589f22d55e5ca15ad538516c322`, [proof](https://exit-protocol.io/log/proofs/1135/00001085.json).
- First snapshot read: known at 2026-10-27T16:29:32.657452+00:00, position 26285184, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `9d872cc6ac2aae4eb9d4b2b3b5ce755090219619dba7be8d7c571efa15aff162`, [proof](https://exit-protocol.io/log/proofs/134/00000100.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:21:55.821229+00:00 to 2026-11-12T23:21:58.986405+00:00 (6 clean equal comparisons, 8 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-10 (an earlier read than the one shown), https://eth.api.pocket.network against https://eth.drpc.org, mode same_block; facts compared 7, agree 7, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00001043.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy | UNKNOWN | NONE_OBSERVED | no address: NONE_OBSERVED (EIP-1967 and ZeppelinOS slots) | no single compared fact |
| owner() | `0x89ab9241aab22a86b4b5fd05628f3e3c34f9777f` | RETURNED_ADDRESS | same address | AGREES (getter:owner(), 2026-11-10); earlier read, compared value equals the address shown |
| Safe interface | `0x89ab9241aab22a86b4b5fd05628f3e3c34f9777f` | SAFE_INTERFACE_ANSWERED · threshold 2-of-3, 3 owners | same address | no single compared fact |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | no single compared fact |

### Row 36: BlackRock USD Institutional Digital Liquidity Fund (BUIDL), ethereum-mainnet

`0x7712c34205737192402172409a8f7ccef8aa2aec` (market-cap rank at list time: 47)

- Read shown: night 2026-11-11, known at 2026-11-11T23:21:58.064934+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `47660e01627631b16499434cad723130967663b9308306c97e97c2adace7ceb1`, [proof](https://exit-protocol.io/log/proofs/1135/00001086.json).
- First snapshot read: known at 2026-10-27T16:29:35.353696+00:00, position 26285184, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `a94340bb2f6a1279bde7c16954ee76c5894e2f5f003ebe3ad52b4a0d1a27a0cb`, [proof](https://exit-protocol.io/log/proofs/134/00000101.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:21:58.757799+00:00 to 2026-11-12T23:22:01.943501+00:00 (6 clean equal comparisons, 6 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-11 (the read shown), https://eth.api.pocket.network against https://eth.drpc.org, mode same_block; facts compared 7, agree 7, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00001124.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy | UNKNOWN | NONE_OBSERVED | no address: NONE_OBSERVED (EIP-1967 and ZeppelinOS slots) | no single compared fact |
| owner() | `0xe01605f6b6dc593b7d2917f4a0940db2a625b09e` | RETURNED_ADDRESS | same address | AGREES (getter:owner(), 2026-11-11) |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | no single compared fact |

### Row 37: BlackRock USD Institutional Digital Liquidity Fund (BUIDL), solana-mainnet

`GyWgeqpy5GueU2YbkE8xqUeVEokCMMCEeUrfbtMw6phr` (market-cap rank at list time: 47)

- Read shown: night 2026-11-11, known at 2026-11-11T23:22:01.877492+00:00, slot 468305771, ACCEPTED_READ, policy `solana-finalized-mint-pair-hop/2`, provider https://solana-rpc.publicnode.com, result sha256 `7ec6290ded82048864a8ab2fbec6004f14e847ba198b9c3a2cf91bbb1028a3f4`, [proof](https://exit-protocol.io/log/proofs/1135/00001087.json).
- First snapshot read: known at 2026-10-27T16:29:37.675260+00:00, position 462138570, policy `solana-finalized-mint-pair-hop/1`, result sha256 `060f9c382e567dc7db43b05694dc2a7b285bdb8e6925f1669c8b3ffb92815809`, [proof](https://exit-protocol.io/log/proofs/134/00000102.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-03T23:21:51.921853+00:00 to 2026-11-12T23:22:05.781541+00:00 (9 clean equal comparisons, 8 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-08 (an earlier read than the one shown), https://api.mainnet-beta.solana.com against https://solana-rpc.publicnode.com, mode window; facts compared 9, agree 9, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000880.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| mintAuthority | `APm3MWbXfMMKAWgsDVnxcAGbLjvRxubPu1A8a5SA2kbJ` | program_owned_unsupported (OBSERVED) | same address | AGREES (control:mintAuthority, 2026-11-08); earlier read, compared value equals the address shown |
| freezeAuthority | `APm3MWbXfMMKAWgsDVnxcAGbLjvRxubPu1A8a5SA2kbJ` | program_owned_unsupported (OBSERVED) | same address | AGREES (control:freezeAuthority, 2026-11-08); earlier read, compared value equals the address shown |
| metadataPointer.authority | `APm3MWbXfMMKAWgsDVnxcAGbLjvRxubPu1A8a5SA2kbJ` | program_owned_unsupported (OBSERVED) | same address | AGREES (control:metadataPointer.authority, 2026-11-08); earlier read, compared value equals the address shown |
| mintCloseAuthority.closeAuthority | `APm3MWbXfMMKAWgsDVnxcAGbLjvRxubPu1A8a5SA2kbJ` | program_owned_unsupported (OBSERVED) | same address | AGREES (control:mintCloseAuthority.closeAuthority, 2026-11-08); earlier read, compared value equals the address shown |
| permanentDelegate.delegate | `APm3MWbXfMMKAWgsDVnxcAGbLjvRxubPu1A8a5SA2kbJ` | program_owned_unsupported (OBSERVED) | same address | AGREES (control:permanentDelegate.delegate, 2026-11-08); earlier read, compared value equals the address shown |
| tokenMetadata.updateAuthority | `APm3MWbXfMMKAWgsDVnxcAGbLjvRxubPu1A8a5SA2kbJ` | program_owned_unsupported (OBSERVED) | same address | AGREES (control:tokenMetadata.updateAuthority, 2026-11-08); earlier read, compared value equals the address shown |
| transferHook.authority | `APm3MWbXfMMKAWgsDVnxcAGbLjvRxubPu1A8a5SA2kbJ` | program_owned_unsupported (OBSERVED) | same address | AGREES (control:transferHook.authority, 2026-11-08); earlier read, compared value equals the address shown |

### Row 38: Aave (AAVE), ethereum-mainnet

`0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9` (market-cap rank at list time: 48)

- Read shown: night 2026-11-11, known at 2026-11-11T23:22:04.699809+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `2c585fcddd00b3d99dcf755e1b5e6adc3ce46dcdc780dba1e5f26e4213930627`, [proof](https://exit-protocol.io/log/proofs/1135/00001088.json).
- First snapshot read: known at 2026-10-27T16:29:40.441163+00:00, position 26285184, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `1a4ca721280541e01b1cfb5ac56f7a8875900aee0186cb0ff73a9d6307ebff07`, [proof](https://exit-protocol.io/log/proofs/134/00000103.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:22:05.450399+00:00 to 2026-11-12T23:22:08.603334+00:00 (6 clean equal comparisons, 5 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: not sampled (drawn from night 2026-11-02 on).
- Correction note: this row is listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy (EIP-1967) implementation | `0x5d4aa78b08bc7c530e21bf7447988b1be7991322` | OBSERVED | same address | not sampled |
| proxy admin | `0x86c3ffee349a7cff7ca88c449717b1b133bfb517` | OBSERVED | same address | not sampled |
| owner() | UNKNOWN | CALL_REVERTED | no address: NOT_OBSERVED (RPC error; cause not established) | not sampled |
| Safe interface | `0x86c3ffee349a7cff7ca88c449717b1b133bfb517` | NOT_ANSWERED (account: CONTRACT (code present at the block)) | same address | not sampled |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | not sampled |

### Row 39: Aave (AAVE), solana-mainnet

`AavE1kKKnesPw4MuRJmJ9jZs9QzEE8CPxQ3ViczUDfc1` (market-cap rank at list time: 48)

- Read shown: night 2026-11-11, known at 2026-11-11T23:22:07.406762+00:00, slot 468305802, ACCEPTED_READ, policy `solana-finalized-mint-pair-hop/2`, provider https://solana-rpc.publicnode.com, result sha256 `956b91cb01b79f72eb30d1f61668c813f1c482853eaca421cf04774786facf8e`, [proof](https://exit-protocol.io/log/proofs/1135/00001089.json).
- First snapshot read: known at 2026-10-27T16:29:42.637004+00:00, position 462138595, policy `solana-finalized-mint-pair-hop/1`, result sha256 `2323c4e96c363134318df2a41ec6181a779681656439cf49fb2c88eacbd0549f`, [proof](https://exit-protocol.io/log/proofs/134/00000104.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-03T23:21:57.269959+00:00 to 2026-11-12T23:22:11.302835+00:00 (9 clean equal comparisons, 2 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-07 (an earlier read than the one shown), https://api.mainnet-beta.solana.com against https://solana-rpc.publicnode.com, mode window; facts compared 3, agree 3, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000793.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| mintAuthority | `2qMmvHtRyRHSnhHPBUE5j9B77i4ryF8s6cN2iMyfZuNY` | account_absent_at_pair_read (OBSERVED) | same address | AGREES (control:mintAuthority, 2026-11-07); earlier read, compared value equals the address shown |
| freezeAuthority | none set | OBSERVED_EMPTY | no address: OBSERVED_EMPTY | not compared (no first-read value): control:freezeAuthority, second read of night 2026-11-07 |

### Row 40: Ondo (ONDO), ethereum-mainnet

`0xfaba6f8e4a5e8ab82f62fe7c39859fa577269be3` (market-cap rank at list time: 49)

- Read shown: night 2026-11-11, known at 2026-11-11T23:22:10.064889+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `3ed6e56f8558b4bda7cda3e3359a319eb41340f0048c50ab2c7b1bac9905cb57`, [proof](https://exit-protocol.io/log/proofs/1135/00001090.json).
- First snapshot read: known at 2026-10-27T16:29:45.278609+00:00, position 26285184, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `7857ad9dfa568f548d3fa2633c680bc90992adda39922d2f7ffe1af5924686a2`, [proof](https://exit-protocol.io/log/proofs/134/00000105.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:22:10.803744+00:00 to 2026-11-12T23:22:14.104875+00:00 (6 clean equal comparisons, 5 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: not sampled (drawn from night 2026-11-02 on).
- Correction note: this row is listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy | UNKNOWN | NONE_OBSERVED | no address: NONE_OBSERVED (EIP-1967 and ZeppelinOS slots) | not sampled |
| owner() | UNKNOWN | CALL_REVERTED | no address: NOT_OBSERVED (RPC error; cause not established) | not sampled |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | not sampled |

### Row 41: Pump.fun (PUMP), solana-mainnet

`pumpCmXqMfrsAkQ5r49WcJnRayYRqmXz6ae8H7H9Dfn` (market-cap rank at list time: 50)

- Read shown: night 2026-11-11, known at 2026-11-11T23:22:13.863127+00:00, slot 468305826, ACCEPTED_READ, policy `solana-finalized-mint-pair-hop/2`, provider https://solana-rpc.publicnode.com, result sha256 `9defbfcd5ee78297b5892a3c9c39cfd0a7f728334e9d6a6400b7e892c272b693`, [proof](https://exit-protocol.io/log/proofs/1135/00001091.json).
- First snapshot read: known at 2026-10-27T16:29:47.655599+00:00, position 462138617, policy `solana-finalized-mint-pair-hop/1`, result sha256 `a643a7ae6ca8a7c72b8999adfd1a1b31ad1d266a33b648367427321cf1328e0d`, [proof](https://exit-protocol.io/log/proofs/134/00000106.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-03T23:22:03.578118+00:00 to 2026-11-12T23:22:17.919799+00:00 (9 clean equal comparisons, 6 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: SUPPLY_CHANGED_IN_WINDOW, second read of night 2026-11-11 (the read shown), https://api.mainnet-beta.solana.com against https://solana-rpc.publicnode.com, mode window; facts compared 3, agree 2, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00001129.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| mintAuthority | none set | OBSERVED_EMPTY | no address: OBSERVED_EMPTY | not compared (no first-read value): control:mintAuthority, second read of night 2026-11-11 |
| freezeAuthority | none set | OBSERVED_EMPTY | no address: OBSERVED_EMPTY | not compared (no first-read value): control:freezeAuthority, second read of night 2026-11-11 |
| metadataPointer.authority | none set | OBSERVED_EMPTY | no address: OBSERVED_EMPTY | not compared (no first-read value): control:metadataPointer.authority, second read of night 2026-11-11 |
| tokenMetadata.updateAuthority | none set | OBSERVED_EMPTY | no address: OBSERVED_EMPTY | not compared (no first-read value): control:tokenMetadata.updateAuthority, second read of night 2026-11-11 |
| transferHook.authority | `DMdBa812dBW1CHVhmTyUyVcrBnSbZbfoFC7U14k4riH1` | program_owned_unsupported (OBSERVED) | same address | AGREES (control:transferHook.authority, 2026-11-11) |

### Row 42: Falcon USD (USDF), ethereum-mainnet

`0xfa2b947eec368f42195f24f36d2af29f7c24cec2` (market-cap rank at list time: 51)

- Read shown: night 2026-11-11, known at 2026-11-11T23:22:16.658041+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `208a08d73187d58dab5bba0239c99a5a38011c9b7a69a252bcfba16297f95c2d`, [proof](https://exit-protocol.io/log/proofs/1135/00001092.json).
- First snapshot read: known at 2026-10-27T16:29:50.543625+00:00, position 26285184, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `5a28680f144661f48c958ed4281817d6b360b69be4500384571bc3da5e7e2be6`, [proof](https://exit-protocol.io/log/proofs/134/00000107.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:22:17.434286+00:00 to 2026-11-12T23:22:21.004459+00:00 (6 clean equal comparisons, 5 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: not sampled (drawn from night 2026-11-02 on).
- Correction note: this row is listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy (EIP-1967) implementation | `0x3adf34c09dac24e4baefb1b1df4c2992edc2b789` | OBSERVED | same address | not sampled |
| proxy admin | `0x3ef1127fdf81b553066dae0faea58785a2aa6e14` | OBSERVED | same address | not sampled |
| owner() | UNKNOWN | CALL_REVERTED | no address: NOT_OBSERVED (RPC error; cause not established) | not sampled |
| Safe interface | `0x3ef1127fdf81b553066dae0faea58785a2aa6e14` | NOT_ANSWERED (account: CONTRACT (code present at the block)) | same address | not sampled |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | not sampled |

### Row 43: Pepe (PEPE), ethereum-mainnet

`0x6982508145454ce325ddbe47a25d4ec3d2311933` (market-cap rank at list time: 52)

- Read shown: night 2026-11-11, known at 2026-11-11T23:22:19.328632+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `b9728e1381870422e94fa99f8f026282b09c2154c8e91666bf7e4fe959fdb723`, [proof](https://exit-protocol.io/log/proofs/1135/00001093.json).
- First snapshot read: known at 2026-10-27T16:29:53.197191+00:00, position 26285184, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `53d5628ff0bec74c4117543e0ca0c574579e630350bdd5096e3880e43fc6072b`, [proof](https://exit-protocol.io/log/proofs/134/00000108.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:22:20.157784+00:00 to 2026-11-12T23:22:23.696669+00:00 (6 clean equal comparisons, 6 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-09 (an earlier read than the one shown), https://eth.api.pocket.network against https://eth.drpc.org, mode same_block; facts compared 6, agree 6, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000956.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy | UNKNOWN | NONE_OBSERVED | no address: NONE_OBSERVED (EIP-1967 and ZeppelinOS slots) | no single compared fact |
| owner() | zero address | RETURNED_ZERO_ADDRESS | no address: RETURNED_ZERO_ADDRESS | not compared (no first-read value): getter:owner(), second read of night 2026-11-09 |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | no single compared fact |

### Row 44: PAX Gold (PAXG), ethereum-mainnet

`0x45804880de22913dafe09f4980848ece6ecbaf78` (market-cap rank at list time: 53)

- Read shown: night 2026-11-11, known at 2026-11-11T23:22:22.407779+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `9991196db72de101da149840ba0b523e1575ae15cf75b66675892f2c09cd6bf3`, [proof](https://exit-protocol.io/log/proofs/1135/00001094.json).
- First snapshot read: known at 2026-10-27T16:29:56.176186+00:00, position 26285184, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `46267b26103a9b080a3eb155f100ff03d1aee6cb6a763495891e496f45dbed6e`, [proof](https://exit-protocol.io/log/proofs/134/00000109.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:22:23.231694+00:00 to 2026-11-12T23:22:27.043486+00:00 (6 clean equal comparisons, 6 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-11 (the read shown), https://eth.api.pocket.network against https://eth.drpc.org, mode same_block; facts compared 7, agree 7, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00001127.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy (ZeppelinOS) implementation | `0x7da4c5d9eca180a03765a6d27196f2a0380fa543` | OBSERVED | same address | AGREES (slot:zos_implementation, 2026-11-11) |
| proxy admin | `0x4a515afe11581fd87ba90d6459dc93db6591f5e3` | OBSERVED | same address | AGREES (slot:zos_admin, 2026-11-11) |
| owner() | `0x6d8b8f7ebd9860e80694665f05033df06ddc3acc` | RETURNED_ADDRESS | same address | AGREES (getter:owner(), 2026-11-11) |
| Safe interface | `0x4a515afe11581fd87ba90d6459dc93db6591f5e3` | NOT_ANSWERED (account: CONTRACT (code present at the block)) | same address | no single compared fact |
| Safe interface | `0x6d8b8f7ebd9860e80694665f05033df06ddc3acc` | NOT_ANSWERED (account: CONTRACT (code present at the block)) | same address | no single compared fact |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | no single compared fact |

### Row 45: Spiko Amundi Overnight Swap Fund (EUR) (EURSAFO), ethereum-mainnet

`0x0990b149e915cb08e2143a5c6f669c907eddc8b0` (market-cap rank at list time: 54)

- Read shown: night 2026-11-11, known at 2026-11-11T23:22:25.141676+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `f5ee907700de63d948524d515155bcb3c360eafca7aac97683a03f2be9fad968`, [proof](https://exit-protocol.io/log/proofs/1135/00001095.json).
- First snapshot read: known at 2026-10-27T16:29:58.747228+00:00, position 26285184, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `3218ac0484a17a3713a4b8009c16db08e71bf65cf576f98c616e46adfb2c8581`, [proof](https://exit-protocol.io/log/proofs/134/00000110.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:22:25.911704+00:00 to 2026-11-12T23:22:29.755635+00:00 (6 clean equal comparisons, 6 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-06 (an earlier read than the one shown), https://eth.api.pocket.network against https://eth.drpc.org, mode same_block; facts compared 6, agree 6, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000706.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy (EIP-1967) implementation | `0x13ae01cbce8530012516fbc1273803d4995aee71` | OBSERVED | same address | AGREES (slot:eip1967_implementation, 2026-11-06); earlier read, compared value equals the address shown |
| proxy admin | UNKNOWN | UNKNOWN (empty admin slot; UUPS designs keep upgrade rights in the implementation) | no address: UNKNOWN (empty admin slot; UUPS designs keep upgrade rights in the implementation) | AGREES (slot:eip1967_admin, 2026-11-06); earlier read, compared with no address, as in the read shown |
| owner() | zero address | RETURNED_ZERO_ADDRESS | no address: RETURNED_ZERO_ADDRESS | not compared (no first-read value): getter:owner(), second read of night 2026-11-06 |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | no single compared fact |

### Row 46: USDD (USDD), ethereum-mainnet

`0x4f8e5de400de08b164e7421b3ee387f461becd1a` (market-cap rank at list time: 56)

- Read shown: night 2026-11-11, known at 2026-11-11T23:22:27.820824+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `c76941d184fd8719814182a0e3136c5b043fb729801857fa026deba42a716ebf`, [proof](https://exit-protocol.io/log/proofs/1135/00001096.json).
- First snapshot read: known at 2026-10-27T16:30:01.519336+00:00, position 26285184, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `d649530820ff9bc396795e76f52dedd6b756b882a4ed39016a3fae06c3645625`, [proof](https://exit-protocol.io/log/proofs/134/00000111.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:22:28.638267+00:00 to 2026-11-12T23:22:32.674461+00:00 (6 clean equal comparisons, 5 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-08 (an earlier read than the one shown), https://eth.api.pocket.network against https://eth.drpc.org, mode same_block; facts compared 6, agree 6, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000872.json).
- Correction note: this row is listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy | UNKNOWN | NONE_OBSERVED | no address: NONE_OBSERVED (EIP-1967 and ZeppelinOS slots) | no single compared fact |
| owner() | UNKNOWN | CALL_REVERTED | no address: NOT_OBSERVED (RPC error; cause not established) | not compared (no first-read value): getter:owner(), second read of night 2026-11-08 |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | no single compared fact |

### Row 47: Mantle (MNT), ethereum-mainnet

`0x3c3a81e81dc49a522a592e7622a7e711c06bf354` (market-cap rank at list time: 57)

- Read shown: night 2026-11-11, known at 2026-11-11T23:22:30.891289+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `9caa0ebad22470deaa42b4d28b90a17ceded87f033fb8e480fadb13deb538f6c`, [proof](https://exit-protocol.io/log/proofs/1135/00001097.json).
- First snapshot read: known at 2026-10-27T16:30:04.640558+00:00, position 26285184, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `848ee4822bd7f52ba9cce26c98aed3b488fe0992597f4eb2dca3071004e21657`, [proof](https://exit-protocol.io/log/proofs/134/00000112.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:22:31.694690+00:00 to 2026-11-12T23:22:35.777586+00:00 (6 clean equal comparisons, 8 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: not sampled (drawn from night 2026-11-02 on).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy (EIP-1967) implementation | `0xcd368c1d80120b0dd92447c87eb570154f8e685c` | OBSERVED | same address | not sampled |
| proxy admin | `0x0cac2b1a172ac24012621101634dd5abd6399add` | OBSERVED | same address | not sampled |
| owner() | `0x4e59e778a0fb77fbb305637435c62faed9aed40f` | RETURNED_ADDRESS | same address | not sampled |
| Safe interface | `0x0cac2b1a172ac24012621101634dd5abd6399add` | NOT_ANSWERED (account: CONTRACT (code present at the block)) | same address | not sampled |
| Safe interface | `0x4e59e778a0fb77fbb305637435c62faed9aed40f` | SAFE_INTERFACE_ANSWERED · threshold 6-of-14, 14 owners | same address | not sampled |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | not sampled |

### Row 48: World Liberty Financial (WLFI), ethereum-mainnet

`0xda5e1988097297dcdc1f90d4dfe7909e847cbef6` (market-cap rank at list time: 59)

- Read shown: night 2026-11-11, known at 2026-11-11T23:22:33.981928+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `b4ce03ba85cb6929d7d04018a7ad968251848ed22da133b9a2ae80a742255a9c`, [proof](https://exit-protocol.io/log/proofs/1135/00001098.json).
- First snapshot read: known at 2026-10-27T16:30:07.736089+00:00, position 26285184, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `9cd239081791a0c034ce0c2eca642e1fc820412e1063b9adb7777480533c47c8`, [proof](https://exit-protocol.io/log/proofs/134/00000113.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:22:34.775944+00:00 to 2026-11-12T23:22:39.074390+00:00 (6 clean equal comparisons, 8 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-03 (an earlier read than the one shown), https://eth.drpc.org against https://ethereum-rpc.publicnode.com, mode same_block; facts compared 7, agree 7, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000453.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy (EIP-1967) implementation | `0x73fe14ff5a25e4363a72828cccd8444f0748fde7` | OBSERVED | same address | AGREES (slot:eip1967_implementation, 2026-11-03); earlier read, compared value equals the address shown |
| proxy admin | `0x7f533afa9e994b7e44673188034f9ce52886a0c0` | OBSERVED | same address | AGREES (slot:eip1967_admin, 2026-11-03); earlier read, compared value equals the address shown |
| owner() | `0x5be9a4959308a0d0c7bc0870e319314d8d957dbb` | RETURNED_ADDRESS | same address | AGREES (getter:owner(), 2026-11-03); earlier read, compared value equals the address shown |
| Safe interface | `0x7f533afa9e994b7e44673188034f9ce52886a0c0` | NOT_ANSWERED (account: CONTRACT (code present at the block)) | same address | no single compared fact |
| Safe interface | `0x5be9a4959308a0d0c7bc0870e319314d8d957dbb` | SAFE_INTERFACE_ANSWERED · threshold 3-of-5, 5 owners | same address | no single compared fact |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | no single compared fact |

### Row 49: World Liberty Financial (WLFI), solana-mainnet

`WLFinEv6ypjkczcS83FZqFpgFZYwQXutRbxGe7oC16g` (market-cap rank at list time: 59)

- Read shown: night 2026-11-11, known at 2026-11-11T23:22:36.697803+00:00, slot 468305935, ACCEPTED_READ, policy `solana-finalized-mint-pair-hop/2`, provider https://solana-rpc.publicnode.com, result sha256 `e41ed708ec0411809e90656e9a899ad25d84b185b5a5f5bd57431ac3060b6d04`, [proof](https://exit-protocol.io/log/proofs/1135/00001099.json).
- First snapshot read: known at 2026-10-27T16:30:09.955561+00:00, position 462138721, policy `solana-finalized-mint-pair-hop/1`, result sha256 `40acde023ef973b566fdff81de0ec92f7d473ccb3f1dcc7cd8f595ef047ed464`, [proof](https://exit-protocol.io/log/proofs/134/00000114.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-03T23:22:25.373822+00:00 to 2026-11-12T23:22:41.798145+00:00 (9 clean equal comparisons, 2 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: not sampled (drawn from night 2026-11-02 on).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| mintAuthority | `9K2KxrYBDQSUTWqPfg2rv4U9ewVbGkbLP4DoSNVXiw6X` | account_absent_at_pair_read (OBSERVED) | same address | not sampled |
| freezeAuthority | `2LoNg8b8wYneseTQ4FYEVQxSJWp12tsLE799oUdYPDHB` | system_owned_account (OBSERVED) | same address | not sampled |

### Row 50: Worldcoin (WLD), ethereum-mainnet

`0x163f8c2467924be0ae7b5347228cabf260318753` (market-cap rank at list time: 60)

- Read shown: night 2026-11-11, known at 2026-11-11T23:22:39.492979+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `abff5864bdee4f61f768e4e76f8a65c81d8563d44f27a2b9ebac43e3d7abe54d`, [proof](https://exit-protocol.io/log/proofs/1135/00001100.json).
- First snapshot read: known at 2026-10-27T16:30:13.175870+00:00, position 26285184, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `6519340d6510ba0f264f25f09bd2e8b44e0aa8013c1fa65c40fef336ee417d22`, [proof](https://exit-protocol.io/log/proofs/134/00000115.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:22:40.426079+00:00 to 2026-11-12T23:22:44.787157+00:00 (6 clean equal comparisons, 8 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: not sampled (drawn from night 2026-11-02 on).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy | UNKNOWN | NONE_OBSERVED | no address: NONE_OBSERVED (EIP-1967 and ZeppelinOS slots) | not sampled |
| owner() | `0x59a0f98345f54bab245a043488ece7fcecd7b596` | RETURNED_ADDRESS | same address | not sampled |
| Safe interface | `0x59a0f98345f54bab245a043488ece7fcecd7b596` | SAFE_INTERFACE_ANSWERED · threshold 1-of-1, 1 owner | same address | not sampled |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | not sampled |

### Row 51: United Stables (U), ethereum-mainnet

`0xce24439f2d9c6a2289f741120fe202248b666666` (market-cap rank at list time: 61)

- Read shown: night 2026-11-11, known at 2026-11-11T23:22:42.554291+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `661e060eeb09f31e92ba75fb7c2ea9f465822f5e90ccaee9f08b5feffeaaea96`, [proof](https://exit-protocol.io/log/proofs/1135/00001101.json).
- First snapshot read: known at 2026-10-27T16:30:16.212226+00:00, position 26285184, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `d8bb9b9f4c90f500c5071e4fa76a989842ec83ec907da7056b0c8d31783edfe9`, [proof](https://exit-protocol.io/log/proofs/134/00000116.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:22:43.520209+00:00 to 2026-11-12T23:22:48.066763+00:00 (6 clean equal comparisons, 8 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-11 (the read shown), https://eth.api.pocket.network against https://eth.drpc.org, mode same_block; facts compared 7, agree 7, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00001123.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy (EIP-1967) implementation | `0xbef21313c69c009fd7d9510a8d3a481a32473dfc` | OBSERVED | same address | AGREES (slot:eip1967_implementation, 2026-11-11) |
| proxy admin | `0x36124fa57e049846e9dc181c8caa31a3c5da4e9c` | OBSERVED | same address | AGREES (slot:eip1967_admin, 2026-11-11) |
| owner() | `0x59f94ade4f881f21ea608ad4448bf70b78e37187` | RETURNED_ADDRESS | same address | AGREES (getter:owner(), 2026-11-11) |
| Safe interface | `0x36124fa57e049846e9dc181c8caa31a3c5da4e9c` | NOT_ANSWERED (account: CONTRACT (code present at the block)) | same address | no single compared fact |
| Safe interface | `0x59f94ade4f881f21ea608ad4448bf70b78e37187` | SAFE_INTERFACE_ANSWERED · threshold 2-of-4, 4 owners | same address | no single compared fact |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | no single compared fact |

### Row 52: Sky (SKY), ethereum-mainnet

`0x56072c95faa701256059aa122697b133aded9279` (market-cap rank at list time: 62)

- Read shown: night 2026-11-11, known at 2026-11-11T23:22:45.263091+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `ceb6407d0062b588a422dfcbe7c91af8b608eaf8a1aa18ea7eca074d0139c6a8`, [proof](https://exit-protocol.io/log/proofs/1135/00001102.json).
- First snapshot read: known at 2026-10-27T16:30:18.937576+00:00, position 26285184, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `7fef0f164a42027a9705af5a9735d2d48641c1c68e6dd8c99a224682b379cff1`, [proof](https://exit-protocol.io/log/proofs/134/00000117.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:22:46.208682+00:00 to 2026-11-12T23:22:51.050459+00:00 (6 clean equal comparisons, 5 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-10 (an earlier read than the one shown), https://eth.api.pocket.network against https://eth.drpc.org, mode same_block; facts compared 6, agree 6, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00001042.json).
- Correction note: this row is listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy | UNKNOWN | NONE_OBSERVED | no address: NONE_OBSERVED (EIP-1967 and ZeppelinOS slots) | no single compared fact |
| owner() | UNKNOWN | CALL_REVERTED | no address: NOT_OBSERVED (RPC error; cause not established) | not compared (no first-read value): getter:owner(), second read of night 2026-11-10 |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | no single compared fact |

### Row 53: Morpho (MORPHO), ethereum-mainnet

`0x58d97b57bb95320f9a05dc918aef65434969c2b2` (market-cap rank at list time: 63)

- Read shown: night 2026-11-11, known at 2026-11-11T23:22:48.153617+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `f8dfc2c9ccb15221b6e3926bd459a3295dd2066fba89b06284db1b864aba3331`, [proof](https://exit-protocol.io/log/proofs/1135/00001103.json).
- First snapshot read: known at 2026-10-27T16:30:21.850871+00:00, position 26285184, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `92371d3e7937194093c42a55c0a9e00d50a120160d21d0c6fc97e963792d9549`, [proof](https://exit-protocol.io/log/proofs/134/00000118.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:22:49.170167+00:00 to 2026-11-12T23:22:54.096054+00:00 (6 clean equal comparisons, 8 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-06 (an earlier read than the one shown), https://eth.api.pocket.network against https://eth.drpc.org, mode same_block; facts compared 7, agree 7, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000704.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy (EIP-1967) implementation | `0x4364fd2371b6318159366abfa51f190df5c24852` | OBSERVED | same address | AGREES (slot:eip1967_implementation, 2026-11-06); earlier read, compared value equals the address shown |
| proxy admin | UNKNOWN | UNKNOWN (empty admin slot; UUPS designs keep upgrade rights in the implementation) | no address: UNKNOWN (empty admin slot; UUPS designs keep upgrade rights in the implementation) | AGREES (slot:eip1967_admin, 2026-11-06); earlier read, compared with no address, as in the read shown |
| owner() | `0xcba28b38103307ec8da98377fff9816c164f9afa` | RETURNED_ADDRESS | same address | AGREES (getter:owner(), 2026-11-06); earlier read, compared value equals the address shown |
| Safe interface | `0xcba28b38103307ec8da98377fff9816c164f9afa` | SAFE_INTERFACE_ANSWERED · threshold 6-of-10, 10 owners | same address | no single compared fact |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | no single compared fact |

### Row 54: Internet Computer (ICP), ethereum-mainnet

`0x00f3c42833c3170159af4e92dbb451fb3f708917` (market-cap rank at list time: 64)

- Read shown: night 2026-11-11, known at 2026-11-11T23:22:51.011432+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `9239c3f3b76e2b2e0146a156fbc14bcaebcf79b49363c84097216ee19a1407da`, [proof](https://exit-protocol.io/log/proofs/1135/00001104.json).
- First snapshot read: known at 2026-10-27T16:30:24.531810+00:00, position 26285184, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `1dacb686609fa1760dac8dacfcb13f699802828a33f82676f8397e4608e10a88`, [proof](https://exit-protocol.io/log/proofs/134/00000119.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:22:52.037404+00:00 to 2026-11-12T23:22:57.180814+00:00 (6 clean equal comparisons, 6 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-09 (an earlier read than the one shown), https://eth.api.pocket.network against https://eth.drpc.org, mode same_block; facts compared 7, agree 7, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000955.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy | UNKNOWN | NONE_OBSERVED | no address: NONE_OBSERVED (EIP-1967 and ZeppelinOS slots) | no single compared fact |
| owner() | `0x70ae25592209b57f62b3a3e832ab356228a2192c` | RETURNED_ADDRESS | same address | AGREES (getter:owner(), 2026-11-09); earlier read, compared value equals the address shown |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | no single compared fact |

### Row 55: HTX DAO (HTX), ethereum-mainnet

`0x61ec85ab89377db65762e234c946b5c25a56e99e` (market-cap rank at list time: 65)

- Read shown: night 2026-11-11, known at 2026-11-11T23:22:53.684179+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `bc5dafa196c64926464ac2b52de2ea66e62f76f59108609ac3df3550679007e4`, [proof](https://exit-protocol.io/log/proofs/1135/00001105.json).
- First snapshot read: known at 2026-10-27T16:30:27.202259+00:00, position 26285184, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `bc08e3285d82988ddebab9acd44b0003082cd6ebd247a6c22c76f6f1ba7c5563`, [proof](https://exit-protocol.io/log/proofs/134/00000120.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:22:54.766035+00:00 to 2026-11-12T23:22:59.951075+00:00 (6 clean equal comparisons, 5 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-11 (the read shown), https://eth.api.pocket.network against https://eth.drpc.org, mode same_block; facts compared 6, agree 6, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00001128.json).
- Correction note: this row is listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy | UNKNOWN | NONE_OBSERVED | no address: NONE_OBSERVED (EIP-1967 and ZeppelinOS slots) | no single compared fact |
| owner() | UNKNOWN | CALL_REVERTED | no address: NOT_OBSERVED (RPC error; cause not established) | not compared (no first-read value): getter:owner(), second read of night 2026-11-11 |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | no single compared fact |

### Row 56: Bitget Token (BGB), ethereum-mainnet

`0x54d2252757e1672eead234d27b1270728ff90581` (market-cap rank at list time: 66)

- Read shown: night 2026-11-11, known at 2026-11-11T23:22:56.354162+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `43eb204c3e1c1d1d9f8c9fb2359ffe2cd3211f48150b1d7b987c14443c7a8095`, [proof](https://exit-protocol.io/log/proofs/1135/00001106.json).
- First snapshot read: known at 2026-10-27T16:30:29.853857+00:00, position 26285184, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `02773da5b77b992ba5337c8d76d43f26ba0ad25e65ee88c37b2ac2fcb5618796`, [proof](https://exit-protocol.io/log/proofs/134/00000121.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:22:57.477796+00:00 to 2026-11-12T23:23:02.750784+00:00 (6 clean equal comparisons, 5 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-10 (an earlier read than the one shown), https://eth.api.pocket.network against https://eth.drpc.org, mode same_block; facts compared 6, agree 6, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00001044.json).
- Correction note: this row is listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy | UNKNOWN | NONE_OBSERVED | no address: NONE_OBSERVED (EIP-1967 and ZeppelinOS slots) | no single compared fact |
| owner() | UNKNOWN | CALL_REVERTED | no address: NOT_OBSERVED (RPC error; cause not established) | not compared (no first-read value): getter:owner(), second read of night 2026-11-10 |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | no single compared fact |

### Row 57: USDGO (USDGO), ethereum-mainnet

`0x4cf5920df52f5b1f246e2e38e1786ae1cf03ecf5` (market-cap rank at list time: 68)

- Read shown: night 2026-11-11, known at 2026-11-11T23:22:59.242419+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `295532ba65c2a34d1856adb24950b3959c38c916161e4adf22f23547e1a6101e`, [proof](https://exit-protocol.io/log/proofs/1135/00001107.json).
- First snapshot read: known at 2026-10-27T16:30:32.715201+00:00, position 26285184, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `197f664fc045afea4a4a2ce1cff7cd19037470dd46b0c2d6770819e627f7c02d`, [proof](https://exit-protocol.io/log/proofs/134/00000122.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:23:00.442678+00:00 to 2026-11-12T23:23:06.041249+00:00 (6 clean equal comparisons, 7 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-05 (an earlier read than the one shown), https://eth.drpc.org against https://ethereum-rpc.publicnode.com, mode same_block; facts compared 7, agree 7, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000620.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy (EIP-1967) implementation | `0xd8e25d31606e3f5b722396a936c76c028a8a72ab` | OBSERVED | same address | AGREES (slot:eip1967_implementation, 2026-11-05); earlier read, compared value equals the address shown |
| proxy admin | UNKNOWN | UNKNOWN (empty admin slot; UUPS designs keep upgrade rights in the implementation) | no address: UNKNOWN (empty admin slot; UUPS designs keep upgrade rights in the implementation) | AGREES (slot:eip1967_admin, 2026-11-05); earlier read, compared with no address, as in the read shown |
| owner() | `0xd93826bb299765c87d13aeba2a7e5d9b27a03956` | RETURNED_ADDRESS | same address | AGREES (getter:owner(), 2026-11-05); earlier read, compared value equals the address shown |
| AccessControl DEFAULT_ADMIN_ROLE | `0xd93826bb299765c87d13aeba2a7e5d9b27a03956` | 1 member(s) | same address | no single compared fact |

### Row 58: USDGO (USDGO), solana-mainnet

`72puLt71H93Z9CzHuBRTwFpL4TG3WZUhnoCC7p8gxigu` (market-cap rank at list time: 68)

- Read shown: night 2026-11-11, known at 2026-11-11T23:23:01.999267+00:00, slot 468306052, ACCEPTED_READ, policy `solana-finalized-mint-pair-hop/2`, provider https://solana-rpc.publicnode.com, result sha256 `513c9f87b26897648745a584ba9d2e47072d0344db6deaa27ac6a389e983af24`, [proof](https://exit-protocol.io/log/proofs/1135/00001108.json).
- First snapshot read: known at 2026-10-27T16:30:34.945638+00:00, position 462138837, policy `solana-finalized-mint-pair-hop/1`, result sha256 `35f8da58f368cea1cb44f4f50ea0f65c00d827a44d84683cc4fa5350b98f0fa1`, [proof](https://exit-protocol.io/log/proofs/134/00000123.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-03T23:22:49.396062+00:00 to 2026-11-12T23:23:08.784958+00:00 (9 clean equal comparisons, 11 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-02 (an earlier read than the one shown), https://api.mainnet-beta.solana.com against https://solana-rpc.publicnode.com, mode window; facts compared 14, agree 14, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000367.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| mintAuthority | `C2QJ4HKLWzWRNprAmKoyd6YqXouVHFZuLKujdqtF4ZDt` | system_owned_account (OBSERVED) | same address | AGREES (control:mintAuthority, 2026-11-02); earlier read, compared value equals the address shown |
| freezeAuthority | `FiV6goxf5fYfw9y7XwuG8bVAG6bqTb1sR1rrLomjkXa3` | system_owned_account (OBSERVED) | same address | AGREES (control:freezeAuthority, 2026-11-02); earlier read, compared value equals the address shown |
| confidentialTransferFeeConfig.authority | `8N2NFYQ5VMaoDGMAcUbfzdeJqvok6LQs2E9BxDK6mMAE` | system_owned_account (OBSERVED) | same address | AGREES (control:confidentialTransferFeeConfig.authority, 2026-11-02); earlier read, compared value equals the address shown |
| confidentialTransferMint.authority | `8N2NFYQ5VMaoDGMAcUbfzdeJqvok6LQs2E9BxDK6mMAE` | system_owned_account (OBSERVED) | same address | AGREES (control:confidentialTransferMint.authority, 2026-11-02); earlier read, compared value equals the address shown |
| metadataPointer.authority | `8N2NFYQ5VMaoDGMAcUbfzdeJqvok6LQs2E9BxDK6mMAE` | system_owned_account (OBSERVED) | same address | AGREES (control:metadataPointer.authority, 2026-11-02); earlier read, compared value equals the address shown |
| mintCloseAuthority.closeAuthority | `8N2NFYQ5VMaoDGMAcUbfzdeJqvok6LQs2E9BxDK6mMAE` | system_owned_account (OBSERVED) | same address | AGREES (control:mintCloseAuthority.closeAuthority, 2026-11-02); earlier read, compared value equals the address shown |
| permanentDelegate.delegate | `C2QJ4HKLWzWRNprAmKoyd6YqXouVHFZuLKujdqtF4ZDt` | system_owned_account (OBSERVED) | same address | AGREES (control:permanentDelegate.delegate, 2026-11-02); earlier read, compared value equals the address shown |
| tokenMetadata.updateAuthority | `8N2NFYQ5VMaoDGMAcUbfzdeJqvok6LQs2E9BxDK6mMAE` | system_owned_account (OBSERVED) | same address | AGREES (control:tokenMetadata.updateAuthority, 2026-11-02); earlier read, compared value equals the address shown |
| transferFeeConfig.transferFeeConfigAuthority | `8N2NFYQ5VMaoDGMAcUbfzdeJqvok6LQs2E9BxDK6mMAE` | system_owned_account (OBSERVED) | same address | AGREES (control:transferFeeConfig.transferFeeConfigAuthority, 2026-11-02); earlier read, compared value equals the address shown |
| transferFeeConfig.withdrawWithheldAuthority | `3WNoR4qjdBehtB6aa6fgz6qX2eceo5UiioV2niFfw26w` | system_owned_account (OBSERVED) | same address | AGREES (control:transferFeeConfig.withdrawWithheldAuthority, 2026-11-02); earlier read, compared value equals the address shown |
| transferHook.authority | `8N2NFYQ5VMaoDGMAcUbfzdeJqvok6LQs2E9BxDK6mMAE` | system_owned_account (OBSERVED) | same address | AGREES (control:transferHook.authority, 2026-11-02); earlier read, compared value equals the address shown |
| pausableConfig.authority | `fEnXbNWPAkmhVK1nL1H2sQVdkF3y4eh8CuqnCsnDXqx` | system_owned_account (OBSERVED) | UNKNOWN | AGREES (control:pausableConfig.authority, 2026-11-02); earlier read, compared value equals the address shown |

### Row 59: Arbitrum (ARB), ethereum-mainnet

`0xb50721bcf8d664c30412cfbc6cf7a15145234ad1` (market-cap rank at list time: 71)

- Read shown: night 2026-11-11, known at 2026-11-11T23:23:04.985419+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `4cef38e8ef4e1e41053326ce41f8745b2453dc68018d17b56ecf4226469b3004`, [proof](https://exit-protocol.io/log/proofs/1135/00001109.json).
- First snapshot read: known at 2026-10-27T16:30:37.820785+00:00, position 26285184, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `abef65d6fde624c2cd20f7281c46ce88d6c901ff6d845fae98996b0a6576728c`, [proof](https://exit-protocol.io/log/proofs/134/00000124.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:23:06.158026+00:00 to 2026-11-12T23:23:11.699871+00:00 (6 clean equal comparisons, 5 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-05 (an earlier read than the one shown), https://eth.drpc.org against https://ethereum-rpc.publicnode.com, mode same_block; facts compared 6, agree 6, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000623.json).
- Correction note: this row is listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy (EIP-1967) implementation | `0xad0c361ef902a7d9851ca7dcc85535da2d3c6fc7` | OBSERVED | same address | AGREES (slot:eip1967_implementation, 2026-11-05); earlier read, compared value equals the address shown |
| proxy admin | `0x5613af0474eb9c528a34701a5b1662e3c8fa0678` | OBSERVED | same address | AGREES (slot:eip1967_admin, 2026-11-05); earlier read, compared value equals the address shown |
| owner() | UNKNOWN | CALL_REVERTED | no address: NOT_OBSERVED (RPC error; cause not established) | not compared (no first-read value): getter:owner(), second read of night 2026-11-05 |
| Safe interface | `0x5613af0474eb9c528a34701a5b1662e3c8fa0678` | NOT_ANSWERED (account: CONTRACT (code present at the block)) | same address | no single compared fact |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | no single compared fact |

### Row 60: Gate (GT), ethereum-mainnet

`0xe66747a101bff2dba3697199dcce5b743b454759` (market-cap rank at list time: 74)

- Read shown: night 2026-11-11, known at 2026-11-11T23:23:07.821238+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `9913a26b6ad03733b4e065547443abc6bce8e341ffcae430bc74f68b7a3dc867`, [proof](https://exit-protocol.io/log/proofs/1135/00001110.json).
- First snapshot read: known at 2026-10-27T16:30:40.953286+00:00, position 26285184, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `f43d096bcb744564761807303e87568cca93a220e3eb0b6566b0889e10295f48`, [proof](https://exit-protocol.io/log/proofs/134/00000125.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:23:08.996027+00:00 to 2026-11-12T23:23:14.975580+00:00 (6 clean equal comparisons, 6 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-02 (an earlier read than the one shown), https://eth.drpc.org against https://ethereum-rpc.publicnode.com, mode same_block; facts compared 7, agree 7, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000359.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy | UNKNOWN | NONE_OBSERVED | no address: NONE_OBSERVED (EIP-1967 and ZeppelinOS slots) | no single compared fact |
| owner() | `0x5a0c161cdd3d3e2a82f3ace2d38a4646c32f96dd` | RETURNED_ADDRESS | same address | AGREES (getter:owner(), 2026-11-02); earlier read, compared value equals the address shown |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | no single compared fact |

### Row 61: POL (ex-MATIC) (POL), ethereum-mainnet

`0x455e53cbb86018ac2b8092fdcd39d8444affc3f6` (market-cap rank at list time: 76)

- Read shown: night 2026-11-11, known at 2026-11-11T23:23:10.651052+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `50bcac5a81de3e421eace6538f55a568f205dd93b331e49e9971bf5d655d8b84`, [proof](https://exit-protocol.io/log/proofs/1135/00001111.json).
- First snapshot read: known at 2026-10-27T16:30:43.762443+00:00, position 26285184, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `c124c1182813d6ea753ed4235a01abfde17aa405e4fc5beacc363a0c9ed6bf4d`, [proof](https://exit-protocol.io/log/proofs/134/00000126.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:23:11.843876+00:00 to 2026-11-12T23:23:18.117635+00:00 (6 clean equal comparisons, 6 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-04 (an earlier read than the one shown), https://eth.drpc.org against https://ethereum-rpc.publicnode.com, mode same_block; facts compared 6, agree 6, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000534.json).
- Correction note: this row is listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy | UNKNOWN | NONE_OBSERVED | no address: NONE_OBSERVED (EIP-1967 and ZeppelinOS slots) | no single compared fact |
| owner() | UNKNOWN | CALL_REVERTED | no address: NOT_OBSERVED (RPC error; cause not established) | not compared (no first-read value): getter:owner(), second read of night 2026-11-04 |
| AccessControl DEFAULT_ADMIN_ROLE | `0x29a6f32f36eded399763524018f17f03b1435b18` | 1 member(s) | same address | no single compared fact |

### Row 62: Jupiter (JUP), solana-mainnet

`JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN` (market-cap rank at list time: 78)

- Read shown: night 2026-11-11, known at 2026-11-11T23:23:13.423182+00:00, slot 468306106, ACCEPTED_READ, policy `solana-finalized-mint-pair-hop/2`, provider https://solana-rpc.publicnode.com, result sha256 `156fce9a591515e0e46baf6efb40df31e285bd020e5991a09033968cfb084356`, [proof](https://exit-protocol.io/log/proofs/1135/00001112.json).
- First snapshot read: known at 2026-10-27T16:30:45.973210+00:00, position 462138889, policy `solana-finalized-mint-pair-hop/1`, result sha256 `ffe57aa1044207fe2fd6a9427e0c4e34d89b2d6ce839d2b34310509dd6b2b2cf`, [proof](https://exit-protocol.io/log/proofs/134/00000127.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-03T23:23:00.116704+00:00 to 2026-11-12T23:23:20.864697+00:00 (9 clean equal comparisons, 2 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: not sampled (drawn from night 2026-11-02 on).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| mintAuthority | none set | OBSERVED_EMPTY | no address: OBSERVED_EMPTY | not sampled |
| freezeAuthority | none set | OBSERVED_EMPTY | no address: OBSERVED_EMPTY | not sampled |

### Row 63: Render (RENDER), ethereum-mainnet

`0x6de037ef9ad2725eb40118bb1702ebb27e4aeb24` (market-cap rank at list time: 79)

- Read shown: night 2026-11-11, known at 2026-11-11T23:23:16.384447+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `a5bdb5cd9306db2f6142412a4e81be84cf13589565f5c206aaf8871c95655fd7`, [proof](https://exit-protocol.io/log/proofs/1135/00001113.json).
- First snapshot read: known at 2026-10-27T16:30:48.766456+00:00, position 26285184, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `77b2616954ee41e36799e60d3f9ee6c83007fda9b2f0c9941a982ceeabeb549f`, [proof](https://exit-protocol.io/log/proofs/134/00000128.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:23:17.513471+00:00 to 2026-11-12T23:23:24.071053+00:00 (6 clean equal comparisons, 6 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-03 (an earlier read than the one shown), https://eth.drpc.org against https://ethereum-rpc.publicnode.com, mode same_block; facts compared 7, agree 7, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000455.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy (ZeppelinOS) implementation | `0x1a1fdf27c5e6784d1cebf256a8a5cc0877e73af0` | OBSERVED | same address | AGREES (slot:zos_implementation, 2026-11-03); earlier read, compared value equals the address shown |
| proxy admin | `0x000000000000000000000000000000000000dead` | OBSERVED | same address | AGREES (slot:zos_admin, 2026-11-03); earlier read, compared value equals the address shown |
| owner() | `0xde68d53200577005cb716aaff0523b11a62084e8` | RETURNED_ADDRESS | same address | AGREES (getter:owner(), 2026-11-03); earlier read, compared value equals the address shown |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | no single compared fact |

### Row 64: Render (RENDER), solana-mainnet

`rndrizKT3MK1iimdxRdWabcF7Zg7AR5T4nud4EkHBof` (market-cap rank at list time: 79)

- Read shown: night 2026-11-11, known at 2026-11-11T23:23:20.205638+00:00, slot 468306132, ACCEPTED_READ, policy `solana-finalized-mint-pair-hop/2`, provider https://solana-rpc.publicnode.com, result sha256 `29707a5067a135a80cd34c9efd29ed4f76e6f1038a1380ec2b1b353ac5e9acca`, [proof](https://exit-protocol.io/log/proofs/1135/00001114.json).
- First snapshot read: known at 2026-10-27T16:30:51.080816+00:00, position 462138912, policy `solana-finalized-mint-pair-hop/1`, result sha256 `6cf6028b2cc3b0f48e6f47c5e209d510a577222a63b480f59faaa54b825ba6e9`, [proof](https://exit-protocol.io/log/proofs/134/00000129.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-03T23:23:06.604714+00:00 to 2026-11-12T23:23:27.930642+00:00 (9 clean equal comparisons, 4 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: SUPPLY_CHANGED_IN_WINDOW, second read of night 2026-11-09 (an earlier read than the one shown), https://api.mainnet-beta.solana.com against https://solana-rpc.publicnode.com, mode window; facts compared 4, agree 3, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000961.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| mintAuthority | `CFyeujXVymxgP2YR9kLbPsaCv2rKrtXMWtJ3EbAN2pdc` | program_owned_unsupported (OBSERVED) | same address | AGREES (control:mintAuthority, 2026-11-09); earlier read, compared value equals the address shown |
| freezeAuthority | `3LNxAhNnQpbCPcvgiamZhUbBugZTzxbjhcMwJ5jE65r5` | program_owned_unsupported (OBSERVED) | same address | AGREES (control:freezeAuthority, 2026-11-09); earlier read, compared value equals the address shown |

### Row 65: Open USD (OUSD), ethereum-mainnet

`0x9f6f3991d525015a6f8caf062c83b62fd3ac4436` (market-cap rank at list time: 82)

- Read shown: night 2026-11-11, known at 2026-11-11T23:23:23.148457+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `633d0f5074f3939391ba1fe0c2686f3b6df0039396077d4d006b188347a0023a`, [proof](https://exit-protocol.io/log/proofs/1135/00001115.json).
- First snapshot read: known at 2026-10-27T16:30:53.860335+00:00, position 26285184, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `c876781a070f945134332dd54e642d8803ca89700590fa82307b7a5f33a28c38`, [proof](https://exit-protocol.io/log/proofs/134/00000130.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:23:24.283961+00:00 to 2026-11-12T23:23:31.032582+00:00 (6 clean equal comparisons, 7 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: not sampled (drawn from night 2026-11-02 on).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy (EIP-1967) implementation | `0x264048239dd1b5939599fae8e6000df40248d524` | OBSERVED | same address | not sampled |
| proxy admin | UNKNOWN | UNKNOWN (empty admin slot; UUPS designs keep upgrade rights in the implementation) | no address: UNKNOWN (empty admin slot; UUPS designs keep upgrade rights in the implementation) | not sampled |
| owner() | `0x79c6631fa15cda38777fb9dd7a6348baee794a4e` | RETURNED_ADDRESS | same address | not sampled |
| AccessControl DEFAULT_ADMIN_ROLE | `0x79c6631fa15cda38777fb9dd7a6348baee794a4e` | 1 member(s) | same address | not sampled |

### Row 66: Open USD (OUSD), solana-mainnet

`ousd2mJsPEckLHcSCDxyKD7NDGARZcfLbDZkKiatYHB` (market-cap rank at list time: 82)

- Read shown: night 2026-11-11, known at 2026-11-11T23:23:25.888178+00:00, slot 468306165, ACCEPTED_READ, policy `solana-finalized-mint-pair-hop/2`, provider https://solana-rpc.publicnode.com, result sha256 `3e1e346c4c5e2df587cb7fbe4adaf6871508d2dc8873a76cc18a84c8309a9f96`, [proof](https://exit-protocol.io/log/proofs/1135/00001116.json).
- First snapshot read: known at 2026-10-27T16:30:56.057587+00:00, position 462138937, policy `solana-finalized-mint-pair-hop/1`, result sha256 `4c757344bbc800cf911ae3186fc29c2f7074d966c54bd06ff9aad1297f460f8c`, [proof](https://exit-protocol.io/log/proofs/134/00000131.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-03T23:23:11.979289+00:00 to 2026-11-12T23:23:33.869297+00:00 (9 clean equal comparisons, 8 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: SUPPLY_CHANGED_IN_WINDOW, second read of night 2026-11-05 (an earlier read than the one shown), https://api.mainnet-beta.solana.com against https://solana-rpc.publicnode.com, mode window; facts compared 11, agree 10, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000627.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| mintAuthority | `EBArgZpd8iv7QRgUFhCasaHxck5oujhHNCkonoa1kEKA` | account_absent_at_pair_read (OBSERVED) | same address | AGREES (control:mintAuthority, 2026-11-05); earlier read, compared value equals the address shown |
| freezeAuthority | `H2UbwLLJAen1W2z6oRCYqZCFo6BidkU4QFDw2eWxL9W4` | account_absent_at_pair_read (OBSERVED) | same address | AGREES (control:freezeAuthority, 2026-11-05); earlier read, compared value equals the address shown |
| confidentialTransferMint.authority | `E7JdFMP5AqdndJKstZV2mHdekLwAQbNWRHMpoozyB3qw` | system_owned_account (OBSERVED) | same address | AGREES (control:confidentialTransferMint.authority, 2026-11-05); earlier read, compared value equals the address shown |
| metadataPointer.authority | `E7JdFMP5AqdndJKstZV2mHdekLwAQbNWRHMpoozyB3qw` | system_owned_account (OBSERVED) | same address | AGREES (control:metadataPointer.authority, 2026-11-05); earlier read, compared value equals the address shown |
| mintCloseAuthority.closeAuthority | `E7JdFMP5AqdndJKstZV2mHdekLwAQbNWRHMpoozyB3qw` | system_owned_account (OBSERVED) | same address | AGREES (control:mintCloseAuthority.closeAuthority, 2026-11-05); earlier read, compared value equals the address shown |
| permanentDelegate.delegate | `Aj2gxCSQ7A7eTnUL2VnyT3KQa79AcZi5x15rPRSnw6RA` | account_absent_at_pair_read (OBSERVED) | same address | AGREES (control:permanentDelegate.delegate, 2026-11-05); earlier read, compared value equals the address shown |
| tokenMetadata.updateAuthority | `E7JdFMP5AqdndJKstZV2mHdekLwAQbNWRHMpoozyB3qw` | system_owned_account (OBSERVED) | same address | AGREES (control:tokenMetadata.updateAuthority, 2026-11-05); earlier read, compared value equals the address shown |
| transferHook.authority | `E7JdFMP5AqdndJKstZV2mHdekLwAQbNWRHMpoozyB3qw` | system_owned_account (OBSERVED) | same address | AGREES (control:transferHook.authority, 2026-11-05); earlier read, compared value equals the address shown |
| pausableConfig.authority | `E7JdFMP5AqdndJKstZV2mHdekLwAQbNWRHMpoozyB3qw` | system_owned_account (OBSERVED) | UNKNOWN | AGREES (control:pausableConfig.authority, 2026-11-05); earlier read, compared value equals the address shown |

### Row 67: Injective (INJ), ethereum-mainnet

`0xe28b3b32b6c345a34ff64674606124dd5aceca30` (market-cap rank at list time: 83)

- Read shown: night 2026-11-11, known at 2026-11-11T23:23:28.493588+00:00, block 26394863, ACCEPTED_READ, policy `ethereum-finalized-admin-surface-outcome-issuer/1`, provider https://eth.drpc.org, result sha256 `821d7eee078a485599c1dcf8e2f9be37cda455e93879d1f09a5d83403e727b66`, [proof](https://exit-protocol.io/log/proofs/1135/00001117.json).
- First snapshot read: known at 2026-10-27T16:30:58.659135+00:00, position 26285184, policy `ethereum-finalized-admin-surface-hop-ac/1`, result sha256 `5873ab26252eaf408dad2446895882c779a2b19f5e390af807776881b5f7688a`, [proof](https://exit-protocol.io/log/proofs/134/00000132.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-06T23:23:29.669943+00:00 to 2026-11-12T23:23:36.732275+00:00 (6 clean equal comparisons, 5 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-11 (the read shown), https://eth.api.pocket.network against https://eth.drpc.org, mode same_block; facts compared 6, agree 6, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00001125.json).
- Correction note: this row is listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| proxy | UNKNOWN | NONE_OBSERVED | no address: NONE_OBSERVED (EIP-1967 and ZeppelinOS slots) | no single compared fact |
| owner() | UNKNOWN | CALL_REVERTED | no address: NOT_OBSERVED (RPC error; cause not established) | not compared (no first-read value): getter:owner(), second read of night 2026-11-11 |
| AccessControl | UNKNOWN | NOT_ANSWERED | no address: NOT_ANSWERED | no single compared fact |

### Row 68: Injective (INJ), solana-mainnet

`1NJMqVM4PadjuzYmeB7zV7q7DV8oB3ExaQCd9x6KsLz` (market-cap rank at list time: 83)

- Read shown: night 2026-11-11, known at 2026-11-11T23:23:32.299642+00:00, slot 468306188, ACCEPTED_READ, policy `solana-finalized-mint-pair-hop/2`, provider https://solana-rpc.publicnode.com, result sha256 `8a503cbab70354b88c4801c409e745f77ccf6358409e8e14f7209754df69b623`, [proof](https://exit-protocol.io/log/proofs/1135/00001118.json).
- First snapshot read: known at 2026-10-27T16:31:01.066704+00:00, position 462138961, policy `solana-finalized-mint-pair-hop/1`, result sha256 `8160e547cec978d09062f3b9b664f24e209ea1aac706dbad9a4b4005e9365941`, [proof](https://exit-protocol.io/log/proofs/134/00000133.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-03T23:23:18.474101+00:00 to 2026-11-12T23:23:40.551489+00:00 (9 clean equal comparisons, 3 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-05 (an earlier read than the one shown), https://api.mainnet-beta.solana.com against https://solana-rpc.publicnode.com, mode window; facts compared 3, agree 3, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000630.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| mintAuthority | `5uVJjzgHV5a3o7cn9ynR2wXDA9i3dXwiBxBMRG5wYYKn` | program_owned_unsupported (OBSERVED) | same address | AGREES (control:mintAuthority, 2026-11-05); earlier read, compared value equals the address shown |
| freezeAuthority | none set | OBSERVED_EMPTY | no address: OBSERVED_EMPTY | not compared (no first-read value): control:freezeAuthority, second read of night 2026-11-05 |

### Row 69: EXIT Protocol (EXITP), solana-mainnet

`5vPz2s8NtkasmVRDz5ySz27V1E8UdSpzqc9xN678jups` (market-cap rank at list time: UNKNOWN)

- Read shown: night 2026-11-11, known at 2026-11-11T23:23:34.957689+00:00, slot 468306203, ACCEPTED_READ, policy `solana-finalized-mint-pair-hop/2`, provider https://solana-rpc.publicnode.com, result sha256 `ed5a67ac40357b5cef553a304e1a369160be57d4900c8aacd9f9f5a358604a2d`, [proof](https://exit-protocol.io/log/proofs/1135/00001119.json).
- First snapshot read: UNKNOWN (the deployment is not in control-map.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-03T23:23:21.133065+00:00 to 2026-11-12T23:23:43.209549+00:00 (9 clean equal comparisons, 2 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: AGREES, second read of night 2026-11-10 (an earlier read than the one shown), https://api.mainnet-beta.solana.com against https://solana-rpc.publicnode.com, mode window; facts compared 2, agree 2, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00001046.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| mintAuthority | none set | OBSERVED_EMPTY | UNKNOWN | not compared (no first-read value): control:mintAuthority, second read of night 2026-11-10 |
| freezeAuthority | none set | OBSERVED_EMPTY | UNKNOWN | not compared (no first-read value): control:freezeAuthority, second read of night 2026-11-10 |

### Row 70: Raydium (RAY), solana-mainnet

`4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R` (market-cap rank at list time: UNKNOWN)

- Read shown: night 2026-11-11, known at 2026-11-11T23:23:37.604197+00:00, slot 468306215, ACCEPTED_READ, policy `solana-finalized-mint-pair-hop/2`, provider https://solana-rpc.publicnode.com, result sha256 `34b1b9d6c0ada57360eec17fbccc2d69ebc5ca3a18eb03910d661256836b4a6a`, [proof](https://exit-protocol.io/log/proofs/1135/00001120.json).
- First snapshot read: UNKNOWN (the deployment is not in control-map.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-03T23:23:23.791680+00:00 to 2026-11-12T23:23:45.880036+00:00 (9 clean equal comparisons, 2 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: SUPPLY_CHANGED_IN_WINDOW, second read of night 2026-11-11 (the read shown), https://api.mainnet-beta.solana.com against https://solana-rpc.publicnode.com, mode window; facts compared 2, agree 1, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00001132.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| mintAuthority | none set | OBSERVED_EMPTY | UNKNOWN | not compared (no first-read value): control:mintAuthority, second read of night 2026-11-11 |
| freezeAuthority | none set | OBSERVED_EMPTY | UNKNOWN | not compared (no first-read value): control:freezeAuthority, second read of night 2026-11-11 |

### Row 71: The Black Bull (ANSEM), solana-mainnet

`9cRCn9rGT8V2imeM2BaKs13yhMEais3ruM3rPvTGpump` (market-cap rank at list time: UNKNOWN)

- Read shown: night 2026-11-11, known at 2026-11-11T23:23:40.276645+00:00, slot 468306227, ACCEPTED_READ, policy `solana-finalized-mint-pair-hop/2`, provider https://solana-rpc.publicnode.com, result sha256 `139a4b3f3010a055f04c4d4a9f0796c13c335edbdfc10add2b8d55632bb259d2`, [proof](https://exit-protocol.io/log/proofs/1135/00001121.json).
- First snapshot read: UNKNOWN (the deployment is not in control-map.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-03T23:23:26.463083+00:00 to 2026-11-12T23:23:48.540764+00:00 (9 clean equal comparisons, 4 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: SUPPLY_CHANGED_IN_WINDOW, second read of night 2026-11-09 (an earlier read than the one shown), https://api.mainnet-beta.solana.com against https://solana-rpc.publicnode.com, mode window; facts compared 2, agree 1, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000965.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| mintAuthority | none set | OBSERVED_EMPTY | UNKNOWN | not compared (no first-read value): control:mintAuthority, second read of night 2026-11-09 |
| freezeAuthority | none set | OBSERVED_EMPTY | UNKNOWN | not compared (no first-read value): control:freezeAuthority, second read of night 2026-11-09 |
| metadataPointer.authority | none set | OBSERVED_EMPTY | UNKNOWN | not compared (no first-read value): control:metadataPointer.authority, second read of night 2026-11-09 |
| tokenMetadata.updateAuthority | none set | OBSERVED_EMPTY | UNKNOWN | not compared (no first-read value): control:tokenMetadata.updateAuthority, second read of night 2026-11-09 |

### Row 72: STONK (STONK), solana-mainnet

`6GmAFSYs4gk3FDao5FzzySQpPZaWsa4rUJHacpMpUNgx` (market-cap rank at list time: UNKNOWN)

- Read shown: night 2026-11-11, known at 2026-11-11T23:23:42.939122+00:00, slot 468306240, ACCEPTED_READ, policy `solana-finalized-mint-pair-hop/2`, provider https://solana-rpc.publicnode.com, result sha256 `ade1ce411f0f71f999ad61641e185a73d3bc57da301747672f59d59719c763f3`, [proof](https://exit-protocol.io/log/proofs/1135/00001122.json).
- First snapshot read: UNKNOWN (the deployment is not in control-map.json).
- Change (daily runs 2026-11-01 to 2026-11-12): EQUAL_OBSERVED_SETTINGS; equal settings observed from 2026-11-03T23:23:29.114488+00:00 to 2026-11-12T23:23:51.237670+00:00 (9 clean equal comparisons, 2 settings compared in the latest read); continuous chain state proven: false; change records: 0; last change: UNKNOWN.
- Second source: SUPPLY_CHANGED_IN_WINDOW, second read of night 2026-11-08 (an earlier read than the one shown), https://api.mainnet-beta.solana.com against https://solana-rpc.publicnode.com, mode window; facts compared 2, agree 1, differ 0; [proof](https://exit-protocol.io/log/proofs/1135/00000881.json).
- Correction note: this row is not listed.

| Field | Address read | Status | First snapshot | Second source |
|---|---|---|---|---|
| mintAuthority | none set | OBSERVED_EMPTY | UNKNOWN | not compared (no first-read value): control:mintAuthority, second read of night 2026-11-08 |
| freezeAuthority | none set | OBSERVED_EMPTY | UNKNOWN | not compared (no first-read value): control:freezeAuthority, second read of night 2026-11-08 |

Built from the files listed under Sources by a fixed generator (format exit.control-surface-view/1).
