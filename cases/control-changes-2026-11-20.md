# Two mint-authority changes recorded on 20 November 2026: Global Dollar (USDG) and PayPal USD (PYUSD) on Solana

EXIT Protocol · 21 November 2026 · all times UTC

EXIT's Control Map is read again every night ([daily re-read](https://exit-protocol.io/control-map/daily/)). The run of 20 November 2026 recorded two changes of the setting `spl-token:mintAuthority`: one on the Solana mint of Global Dollar (USDG), row 21 of the map, and one on the Solana mint of PayPal USD (PYUSD), row 23. Read on 21 November 2026 at 01:23:31, the daily page said: "20 daily runs from 2026-11-01 to 2026-11-20; 2 changes recorded."

This note gives facts only: what the two Control-Change Records state, and what two public Solana providers returned for the same accounts on 21 November 2026 between 01:25:18 and 01:35:20. It gives no reason for the changes and no judgement of them, and it names no party. The token names are the ones the Control Map shows for the two mint addresses.

Terms used below:
- **Mint authority.** The setting list of the record format describes `spl-token:mintAuthority` as "The key that may create new tokens of this mint. null: no key can." and adds what it does not mean: "Who holds the key, or that it was used." ([control-change-settings.json](../control-change/control-change-settings.json)).
- **Read position.** The finalized slot at which a nightly read was taken.
- **Multisig account.** An account of the token program that stores a number of required signers (m) and a list of signer addresses (n of them).

## What the records state

| | Row 21 · Global Dollar (USDG) | Row 23 · PayPal USD (PYUSD) |
|---|---|---|
| Mint (the record's `subject`) | `2u1tszSeqZ3qBWF3uNGPFc8TzMk2tdiwknnRMWGWjGWH` | `2b1kV6DkPAnxd5ixfnxCpjxmKwqjjaYmCZfHsFu24GXo` |
| Setting | `spl-token:mintAuthority` | `spl-token:mintAuthority` |
| Old value | `2e99QgqSDtiJSi5omGRVeZJuqNFRZdpy2YgG3mBd1AB4` | `AxJkHRY3puoofyj7Pn512M1SGBgWroXMkEdNPQypkzbu` |
| New value | `8kC6WyMQvcKynL3oXxJdH1aH6sEpuL4KQHX2tY8nDkwy` | `DRXA1H9SjZPyPCEeuAWpfwk8GqVW6dZsKFAtdfpFwApX` |
| Earlier read position | slot 471,517,625 | slot 471,517,652 |
| Later read position | slot 471,919,352 | slot 471,919,381 |
| `known_at` | `2026-11-20T23:20:59.699213+00:00` | `2026-11-20T23:21:05.485070+00:00` |
| Record file | [ccr/2026-11-20/0001.json](https://exit-protocol.io/control-map/daily/ccr/2026-11-20/0001.json), 1,048 bytes | [ccr/2026-11-20/0002.json](https://exit-protocol.io/control-map/daily/ccr/2026-11-20/0002.json), 1,048 bytes |
| SHA-256 of the file | `4fc18b4ebf8e68845365819cfd718342a3564b1d1b9dc7f1584d72978b69d062` | `10e06d017ca6caff93f45c57b26963270ae392b3f0e1bebb5db104de1b4332ef` |
| Evidence-log leaf | 1832 | 1835 |

- **Basis.** Both records have the basis `bracketing_reads`: a read at the earlier position showed the old value and a read at the later position showed the new one, so the change took effect after the first position and no later than the second. A record of a Solana change carries no transaction and no time of the change ([CONTROL-CHANGE-RECORD.md](../CONTROL-CHANGE-RECORD.md)).
- **`known_at`** is the time EXIT acquired the evidence of the later read. It is EXIT's own statement, not the time of the change.
- **The files.** [daily.json](https://exit-protocol.io/control-map/daily/daily.json) lists both files with the SHA-256 above, and both pass `ccr.py check` ([control-change/ccr.py](../control-change/ccr.py)).
- **The log.** Each record file is a record of the [evidence log](https://exit-protocol.io/log/): leaves 1832 and 1835, whose `result_sha256` is the SHA-256 of the file. Both are in the tree of size 1898, anchored on Solana by transaction `3onZqkJMvkiA3XtzxUw1XGzJyzHvYdDPDBYAvDP65xDW9EpqwESwSD5MZBiqFQ4PwC93xdJtALbd9SZohj71aKmW` (slot 471,938,618, block time 21 November 2026, 00:30:08). We checked both proof bundles with exit_log_verify.py (`proof`), with the anchor transaction read from each of the two providers below.

## What the chain shows

Read on 21 November 2026 between 01:25:18 and 01:35:20 from two public Solana RPC endpoints without a key: `api.mainnet-beta.solana.com` and `solana-rpc.publicnode.com`. Every fact in this section was returned alike by both. That two endpoints agree does not show that they are independent: both may relay the same upstream provider.

### The two transactions

In the signature list of each old authority account, the last transaction before the later read position holds a SetAuthority instruction of the token program. The mint's own signature list holds the same transaction.

| | Global Dollar (USDG) | PayPal USD (PYUSD) |
|---|---|---|
| Transaction | `4hks8xmLa7QcaA82U6MSVpDQxcRsxaE6gwDiUrekKcQ4Cgie5WXSsdAMMZo5NqVhk4puk4vNx8YCiSauiKjHC1PF` | `5twa7J6ogXAjX7BKT3pmdE8puqxQxSd58uY5tTnEFskWbZ5vzipY2PgAEsAamd3tnb5PYAtEiEGx3qa8QyRc1ppR` |
| Slot | 471,856,298 | 471,856,534 |
| Block time | 20 November 2026, 19:34:39 | 20 November 2026, 19:35:29 |
| Authority type | `mintTokens` | `mintTokens` |
| Mint | `2u1tsz…jGWH` | `2b1kV6…4GXo` |
| Authority before (a multisig account) | `2e99Qg…1AB4` | `AxJkHR…kzbu` |
| New authority | `8kC6Wy…Dkwy` | `DRXA1H…wApX` |
| Signer named in the instruction | `2apBGM…YJjk` | `2apBGM…YJjk` |
| Nonce account advanced | `5bWLbnmGJZ4mjk5rLAeF2G7Wn2vDMzskgRyJKCzS1i9v` | `RTF4qNLh6JRxB2BskjJxzpHGAuZFsDnHiM9Qbcau3r9` |

- Each transaction succeeded, has two instructions and one signature. The first is the System Program's instruction that advances a nonce account; the second is the SetAuthority instruction. There are no inner instructions.
- In each, the mint, the authority before and the new authority are the record's subject, old value and new value.
- Each slot lies after the record's earlier read position and before its later one. The block times of the read positions, which the records do not carry, are:
  - Global Dollar (USDG): slot 471,517,625 at 19 November 2026, 23:21:02 and slot 471,919,352 at 20 November 2026, 23:20:58;
  - PayPal USD (PYUSD): slot 471,517,652 at 19 November 2026, 23:21:08 and slot 471,919,381 at 20 November 2026, 23:21:04.

### Between the two read positions

A record with bracketing reads shows only the net change between two reads. For each mint we therefore took, from the providers' signature lists, every transaction that names the old or the new authority account between the record's two read positions, and read each one.

- **Global Dollar (USDG).** After slot 471,517,625 and up to slot 471,919,352:
  - the old authority account `2e99Qg…1AB4` is named in 26 transactions. 25 of them hold MintTo instructions for the mint with that account
    as authority and no SetAuthority instruction. The other one, the last in slot order, is the transaction above (slot 471,856,298);
  - the new authority account `8kC6Wy…Dkwy` is named in 4 transactions, all after that transaction. Each holds a MintTo or MintToChecked instruction
    for the mint with that account as authority; none holds a SetAuthority instruction.
- **PayPal USD (PYUSD).** After slot 471,517,652 and up to slot 471,919,381:
  - the old authority account `AxJkHR…kzbu` is named in 23 transactions. 22 of them hold MintTo or MintToChecked instructions for the mint with that account
    as authority and no SetAuthority instruction. The other one, the last in slot order, is the transaction above (slot 471,856,534);
  - the new authority account `DRXA1H…wApX` is named in 4 transactions, all after that transaction. Each holds a MintTo or MintToChecked instruction
    for the mint with that account as authority; none holds a SetAuthority instruction.

The mints' own signature lists are long and were read only around the two transactions above; see "What this shows, and what it does not".

### The authority accounts

All four are multisig accounts of the token program: 355 bytes of data, not executable, owned by the token program.

| Account | m | n | Signer addresses, in the stored order |
|---|---|---|---|
| USDG old authority `2e99QgqSDtiJSi5omGRVeZJuqNFRZdpy2YgG3mBd1AB4` | 1 | 5 | `2apBGM…YJjk`, `GdJywa…Hngg`, `CzSG2j…e56L`, `75sq4x…2bnp`, `E6ZSah…FKbv` |
| USDG new authority `8kC6WyMQvcKynL3oXxJdH1aH6sEpuL4KQHX2tY8nDkwy` | 1 | 6 | `2apBGM…YJjk`, `GdJywa…Hngg`, `CzSG2j…e56L`, `75sq4x…2bnp`, `E6ZSah…FKbv`, `4x9udX…vBxP` |
| PYUSD old authority `AxJkHRY3puoofyj7Pn512M1SGBgWroXMkEdNPQypkzbu` | 1 | 5 | `2apBGM…YJjk`, `3QaqDJ…ro7d`, `BfWsvy…z3LN`, `AuVW19…SeGh`, `HVU44Q…pgEU` |
| PYUSD new authority `DRXA1H9SjZPyPCEeuAWpfwk8GqVW6dZsKFAtdfpFwApX` | 1 | 6 | `2apBGM…YJjk`, `3QaqDJ…ro7d`, `BfWsvy…z3LN`, `AuVW19…SeGh`, `HVU44Q…pgEU`, `8rjAiC…2Z3X` |

- **m and n** are the account's stored numbers of required signers and of signer addresses. For each mint, the new account lists the five signer addresses of the old account in the same order and one more: `4x9udX…vBxP` for USDG, `8rjAiC…2Z3X` for PYUSD.
- **Read at** finalized slots 471,955,310 to 471,955,694. The old authority accounts still exist.
- **Creation.** Each new authority account was created before the record's earlier read position, by a transaction with two instructions: the System Program creates the account (355 bytes, owned by the token program) and the token program initializes it as a multisig with m = 1 and the six signer addresses above.
  - USDG: transaction `5mtDyjg95kXjJq2xDkGjcJD9oDcpGQL3EzMug5QkU4Em5xLum24e79PRjEjBRzaMHezK1sAt3UMwEPdgVpemPkJS`, slot 471,483,241, block time 19 November 2026, 21:17:32.
  - PYUSD: transaction `5LvWgc4yqy3a77h52yUA45xANqtZoYoi6rMYb2fwJpzmTDJWNU9FDYMmDMAVuym3ZY6xddrkXJhXgy5N3EjfLV23`, slot 471,486,515, block time 19 November 2026, 21:29:17.
  - Each was signed by the new account's own key and by the fee payer `Ad5YH3AoPHXeHxxWt5uFTZHw9HFGKV9wDfQCV19wN4dH`, which also funded the account.

The accounts behind the 11 signer addresses (none is executable), read at finalized slots 471,956,134 to 471,956,142:

| Signer address | Listed in | Kind of account |
|---|---|---|
| `2apBGMsS6ti9RyF5TwQTDswXBWskiJP2LD4cUEDqYJjk` | USDG old and new; PYUSD old and new | owned by the System Program, 0 bytes of data |
| `GdJywa1Mye4fA7ST5WuJw2eEsxbPPgNc7AsCT8D6Hngg` | USDG old and new | account of 170 bytes owned by a program other than the System Program |
| `CzSG2jccXqr19Xcbr7E1yCPs4nbQj3ggsZtK7BGwe56L` | USDG old and new | account of 170 bytes owned by a program other than the System Program |
| `75sq4xbQ1snnWKmwZ9sDZjzaLxgiZedPcegXwCCQ2bnp` | USDG old and new | account of 223 bytes owned by a program other than the System Program |
| `E6ZSahbyZhgat4f2UCVvErurgJbC2LjKH9jPTcG1FKbv` | USDG old and new | no account at the slot read |
| `4x9udXzGKa3q8QrhaC3SpKWTrRuWfU9JLxG2jE2yvBxP` | USDG new only | account of 170 bytes owned by a program other than the System Program |
| `3QaqDJS5angcPhW1HsMbB74vJbzWNcy1r5bwtATUro7d` | PYUSD old and new | account of 170 bytes owned by a program other than the System Program |
| `BfWsvypxRvQ4KUhyJ2gLeFEkhRx3LgfkVahXMj6Kz3LN` | PYUSD old and new | account of 170 bytes owned by a program other than the System Program |
| `AuVW19qwit2bxZqcspGZLsbq2ZiqosvryTNXE8UZSeGh` | PYUSD old and new | account of 223 bytes owned by a program other than the System Program |
| `HVU44QhbeMGuMvmnqsjsoRmZiSB6iFp1z2rXEiJnpgEU` | PYUSD old and new | no account at the slot read |
| `8rjAiCX71uGK7FQLkfbMLvikLkB6HfNjnX81VnYY2Z3X` | PYUSD new only | account of 170 bytes owned by a program other than the System Program |

We did not follow the signers further: 8 of these accounts are owned by a program other than the System Program. This note does not give the addresses of those programs; what the programs do, and who can change them, was not read.

### The mints and the token program

- **Now.** At finalized slots 471,954,005 to 471,954,010 (read on 21 November 2026 between 01:25:18 and 01:25:20), the mint authority of each mint was the record's new value. The freeze authority of both mints was `2apBGMsS6ti9RyF5TwQTDswXBWskiJP2LD4cUEDqYJjk`.
- **Token program.** Both mints and all four multisig accounts are owned by the program `TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb`, which the providers label `spl-token-2022`. It is an upgradeable program: its program data account is `DoU57AYuPFu2QU514RktNPG22QhApEjnKxnBcu4BHDTY`, the slot of its last deployment is 460,497,271 and its upgrade authority is `AeLmXCbPaQHGWRLr2saFsEVfmMNuKnxRAbWCT9P5twgz` (finalized slots 471,955,725 and 471,955,727).

### What the two changes share

- **Not a transaction.** The changes are two transactions, 236 slots and 50 seconds apart.
- **A signer.** Both transactions carry one signature, that of `2apBGMsS6ti9RyF5TwQTDswXBWskiJP2LD4cUEDqYJjk`. This address is the fee payer, the authority of the nonce account and the signer named in the SetAuthority instruction of both. It is also the freeze authority of both mints, and it is listed in all four multisig accounts, each time as the leading entry of the stored order.
- **Not a new authority.** The two new authorities are different accounts. `2apBGM…YJjk` is the one signer address they have in common; the same holds for the two old accounts.
- **A fee payer of the creating transactions.** The two transactions that created the new authority accounts have the same fee payer, `Ad5YH3…N4dH`. What else that address pays for was not read; a shared fee payer does not by itself show common control.
- **The token program.** Both mints are owned by the same token program.

## Reported, not checked by us

Nothing. This note cites no announcement, press report, label or other outside statement, and none was read for it.

## What this shows, and what it does not

- **It shows** that the stored mint authority of each mint changed from one multisig account of the token program to another, in one transaction each, on 20 November 2026 at 19:34:39 and 19:35:29, and that EXIT's nightly re-read recorded both changes at its next read.
- **It shows** which addresses the old and the new multisig accounts list, and that the two transactions were signed by the same address.
- **It does not show** who holds or controls any key or account, why the setting was changed, or whether the change was safe or harmful. A record says none of these either ([CONTROL-CHANGE-RECORD.md](../CONTROL-CHANGE-RECORD.md), "What a record does not say").
- **It does not show** that a mint authority was used, or will be, beyond the mint instructions counted above.
- **It does not show** every transaction of the two mints between the read positions. We listed the transactions that name the old or the new authority account. In the token program's layout a SetAuthority instruction names the current authority among its accounts, so a change away from an authority would appear in that account's list; this is the program's layout, not something these reads prove.
- **It does not show** that no other setting changed. The daily page lists this one setting for each of the two rows; settings outside the reader's declared scope are not read.
- **It does not show** the state after the slots named above.
- **Providers.** `solana-rpc.publicnode.com` does not keep the whole history, and the start of what it keeps moves forward: its first available block was 471,412,567 at 21 November 2026, 01:35:20, 471,415,848 at 02:01:31 and 471,429,696 at 03:30:21. At those times it still served every transaction named here, so no fact in this note rests on one provider. Once its first available block passes a slot named here, that fact can be re-read at one provider only, beginning with the two creating transactions (slots 471,483,241 and 471,486,515); the reread script then prints ONE_PROVIDER for it.
- **EXIT's API.** EXIT's live API has a route that reads a Solana mint, `GET /v0/research/solana/mint` ([docs/API.md](../docs/API.md)). It needs an access key. No key was created for this note and the route was not called, so the note does not say what the API answers for these two mints.

## Check it yourself

You need Python 3.9 or later and a copy of this repository; the commands are run from its root. Nothing else is installed.

1. Get a record file, compare its SHA-256 with the table above and check its form:

   ```
   curl -sSO https://exit-protocol.io/control-map/daily/ccr/2026-11-20/0001.json
   shasum -a 256 0001.json
   python3 control-change/ccr.py check 0001.json
   ```

2. Check that the record is in an anchored tree of the evidence log (the same for leaf 1835; any Solana provider works in place of the public endpoint):

   ```
   python3 tools/exit_log_verify.py proof https://exit-protocol.io/log/proofs/1898/00001832.json --rpc https://api.mainnet-beta.solana.com
   ```

   It must print `"verified": true`, and the bundle's `result_sha256` must be the SHA-256 of the record file.

3. Re-read the chain facts of this note:

   ```
   python3 cases/control-changes-2026-11-20-reread.py
   ```

   The script asks the two providers named above (or two of your choice, `--rpc URL URL`). It prints PASS for a fixed fact that both providers return as stated here, ONE_PROVIDER when one of them no longer serves that part of the history, FAIL otherwise, and SAME or CHANGED for the values that can change. A later change of a mint authority shows as CHANGED, not as a failure. `--save DIR` keeps every request and reply.

## Correction

No correction to this note so far. The list of corrections is in [CORRECTIONS.md](../CORRECTIONS.md).

## Evidence

| What | Where |
|---|---|
| The two records | [ccr/2026-11-20/0001.json](https://exit-protocol.io/control-map/daily/ccr/2026-11-20/0001.json), [ccr/2026-11-20/0002.json](https://exit-protocol.io/control-map/daily/ccr/2026-11-20/0002.json); listed in [daily.json](https://exit-protocol.io/control-map/daily/daily.json) |
| The rows | [daily re-read](https://exit-protocol.io/control-map/daily/) and [Control Map](https://exit-protocol.io/control-map/), rows 21 and 23 |
| Record format and setting names | [CONTROL-CHANGE-RECORD.md](../CONTROL-CHANGE-RECORD.md), [control-change-settings.json](../control-change/control-change-settings.json) |
| Proof bundles of the two records | [proofs/1898/00001832.json](https://exit-protocol.io/log/proofs/1898/00001832.json), [proofs/1898/00001835.json](https://exit-protocol.io/log/proofs/1898/00001835.json) |
| Anchor of tree size 1898 | [anchors.json](https://exit-protocol.io/log/anchors.json) |
| Chain facts as data | [control-changes-2026-11-20.json](control-changes-2026-11-20.json), SHA-256 `d8e97d0a43923a3041447d40651e8fae75fd967a362f87fff0a060ef8d366be8` |
| Re-read script | [control-changes-2026-11-20-reread.py](control-changes-2026-11-20-reread.py) (Python standard library, no keys) |

The result file holds every fact above as data: the records' fields, the two transactions, every transaction counted between the read positions with its slot, the four multisig accounts, the signer accounts, the token program, the slots each provider answered at, and each provider's first available block.

| Transactions | Signature | Slot |
|---|---|---|
| USDG: SetAuthority, mint authority (20 November 2026, 19:34:39) | `4hks8xmLa7QcaA82U6MSVpDQxcRsxaE6gwDiUrekKcQ4Cgie5WXSsdAMMZo5NqVhk4puk4vNx8YCiSauiKjHC1PF` | 471,856,298 |
| PYUSD: SetAuthority, mint authority (20 November 2026, 19:35:29) | `5twa7J6ogXAjX7BKT3pmdE8puqxQxSd58uY5tTnEFskWbZ5vzipY2PgAEsAamd3tnb5PYAtEiEGx3qa8QyRc1ppR` | 471,856,534 |
| USDG: creation of the new authority account (19 November 2026, 21:17:32) | `5mtDyjg95kXjJq2xDkGjcJD9oDcpGQL3EzMug5QkU4Em5xLum24e79PRjEjBRzaMHezK1sAt3UMwEPdgVpemPkJS` | 471,483,241 |
| PYUSD: creation of the new authority account (19 November 2026, 21:29:17) | `5LvWgc4yqy3a77h52yUA45xANqtZoYoi6rMYb2fwJpzmTDJWNU9FDYMmDMAVuym3ZY6xddrkXJhXgy5N3EjfLV23` | 471,486,515 |
| Anchor of the evidence-log tree of size 1898 (21 November 2026, 00:30:08) | `3onZqkJMvkiA3XtzxUw1XGzJyzHvYdDPDBYAvDP65xDW9EpqwESwSD5MZBiqFQ4PwC93xdJtALbd9SZohj71aKmW` | 471,938,618 |

The signatures are given in full, without explorer links.

EXIT does not attribute any key or account to a person or organization.
