# ANSEM, TJR and LUKE, June 2026: three pump.fun tokens created by one signer, and the accounts on both ends

EXIT Protocol · 16 November 2026 · all times UTC; a date without a year is in 2026

The chain facts were read on 15 November 2026 between Solana slots 469,797,591 and 469,842,517 (about 16:32 to 19:15 UTC). Values that can change carry the slot they were read at; a later read carries its own date. Later changes on chain will be added to this note as dated updates; the text above them will not be edited.

**Check the mint, not the symbol.** Other coins also use the symbol ANSEM (one of them is described under "15 November"), and addresses that copy the first and last characters of addresses in this note exist. This note is about these three mints:

| Token | Mint |
|---|---|
| ANSEM | `9cRCn9rGT8V2imeM2BaKs13yhMEais3ruM3rPvTGpump` |
| TJR | `4U4U8oXwDyVXGeTffMXds4NAgBgLFwq3wNvTCRTSpump` |
| LUKE | `86CFcbZBJAqGVnfgnLNcw3tPmfaTigAR2UxbUPYTpump` |

Below, a short form such as GV6U or FkCcgv is only a label for the full address given in the tables of this note; a short prefix alone does not identify an address.

On 16 June 2026 one Solana address, `yHCxHBEaJW5tbndqC8JciSThr7U1cqLpdcsvHcx6PRe` (below: the deployer), signed the CreateV2 instruction of the pump.fun program for ANSEM; on 29 and 30 June it did the same for TJR and LUKE. In each creation transaction it also bought between 76.370 and 79.293 percent of the token's supply of 1,000,000,000. It then sent 650,000,000 ANSEM, 790,000,000 TJR and 750,000,000 LUKE to three wallets, sent smaller amounts to wallets that later sold, and sold the rest of its holding in 93 sells for 1,376.880426733 SOL. Each of the three wallets was made the only recipient of that token's pump.fun creator fees, and the admin right on those three fee settings is revoked. The 27 wallets that received LUKE from the deployer sold all of it within 13 minutes, for 3,497.329185191 SOL (net); seven of them had co-signed the three TJR buys directly after TJR's creation, in the same block, and one of them, FkCcgv, had sent the deployer SOL in April and received at least 6,893.086879788 SOL from it in June and July.

On identity, with the evidence tiers defined in "Identity": the deployer is a DIRECT match to the X account @Supermanonchain, whose archived bio calls this address its "only dev wallet". The ANSEM fee shareholder `GV6UUmNxz2RpKxmNAPadYKb7uQpszwqQAu3qLJxVdC52` (below: GV6U), which received the 650,000,000 ANSEM 37 seconds after the creation, is a DIRECT match to @blknoiz06, the author of a 16 July X Article about ANSEM. That account says it took the coin over (CTO) and did not create it, and the chain shows that GV6U did not sign the creation. No other wallet in this note has an account identity; the leads that exist are WEAK and are listed apart, without account names.

We re-read the Solana chain with one question: what did the chain show, and when?

**Providers.** Every transaction in this note was first read from api.mainnet-beta.solana.com, the public mainnet-beta endpoint. On 16 November 2026 all 194 transactions that the result file lists were read again from a second provider, public.rpc.solanavibestation.com, and both providers returned the same slot, block time, transaction index, signers and balance changes for every one of them: among them the three creations, the three large transfers, the first two transfers to the deployer, the three fee-config creations, all 93 sells, the 27 LUKE transfers, the 24 transfers to FkCcgv and the three TJR buys of the creation slot. Other history rests on that one provider; "Read on two providers, and on one" says which. Current state (balances, fee settings, the mint) was read on 15 November from two providers, api.mainnet-beta.solana.com and solana-rpc.publicnode.com, which agreed in every case.

Solana is covered by EXIT's API for mint authorities and holders; this note goes further (transactions, flows and public statements) and is research done with public read-only endpoints, without keys.

Terms used below:
- **Deployer.** The address that signed CreateV2 for all three mints.
- **Creation buy.** The `buy_exact_sol_in` instruction inside the deployer's creation transaction.
- **Fee-sharing config.** An account of the pump.fun fees program (`pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ`) that lists who receives a token's creator fees, in basis points (bps; 10,000 bps = 100 percent), and an admin. Its layout was decoded from the published interface file (IDL) of pump-fun/pump-public-docs at commit `639b87fb45c3adeffa6f7c4a1bf0cb85e392bf22`.
- **Signer.** A key that signed a transaction. Several signers on one transaction means that all those keys signed it; it does not show who holds the keys.
- **DIRECT, STRONG, WEAK.** The identity tiers defined in "Identity".

## Timeline

| When | Slot | What |
|---|---|---|
| 20 Apr 13:00:49 | 414,479,400 | The deployer's first transaction: 4.431561 SOL from `BY4StcU9Y2BpgH8quZzorg31EGE4L1rjomN8FNsCBEcx`, sent with a durable nonce |
| 20 Apr 13:02:25 | 414,479,640 | 9.126416323 SOL from FkCcgv (`FkCcgvCoR6p6BRucCnU1t1DXP97Y3rJeMYBiU1o31nuv`), 1 min 36 s after the first funding |
| 16 Jun 20:59:26 | | @blknoiz06 posts that it linked its X account to a pump.fun account; the post's link opens the pump.fun profile of GV6U (third-party page) |
| 16 Jun 21:01:38 | 426,929,835 | Ten addresses, four of them later LUKE recipients, send the deployer 79.233316361 SOL |
| 16 Jun 21:05:48 | 426,930,467 | ANSEM CreateV2 by the deployer, which buys 792,454,486.758954 ANSEM in the same transaction; later in the same slot another signer completes the curve and moves it to a pump AMM pool |
| 16 Jun 21:06:25 | 426,930,558 | The deployer sends 650,000,000 ANSEM to GV6U |
| 16 Jun 21:06:29 to 21:06:38 | | 7 deployer sells of ANSEM, 159.405670644 SOL |
| 16 Jun 21:07:55 | 426,930,784 | ANSEM fee-sharing config created: 100 percent to GV6U |
| 29 Jun 13:08:45 | 429,670,768 | TJR CreateV2 by the deployer, which buys 763,701,067.609494 TJR; the next three transactions in the block are TJR buys co-signed by seven later LUKE recipients |
| 30 Jun 02:14:24 | 429,787,322 | The deployer sends 790,000,000 TJR to `9fnyojTv8GYHWr4Vaj4tvVL82scPPYYkW1CAXAbfUsdj` (9fnyoj) |
| 30 Jun 02:14:28 to 02:14:54 | | 66 deployer sells of TJR, 792.755712105 SOL |
| 30 Jun 02:16:28 | 429,787,622 | TJR fee-sharing config created: 100 percent to 9fnyoj |
| 30 Jun 06:18:29 | 429,823,473 | LUKE CreateV2 by the deployer, which buys 792,936,627.277769 LUKE |
| 30 Jun 13:30:45 | 429,887,676 | The deployer sends 750,000,000 LUKE to `5FcdrgRp9jvRYcfJ5jENdH4XABLsPuD4KWMsAyHusQyy` (5Fcdrg) |
| 30 Jun 13:30:51 to 13:31:29 | | 17 deployer sells of LUKE, 415.019059711 SOL |
| 30 Jun 13:30:59 to 13:31:00 | 429,887,710 and 429,887,711 | The deployer sends 39,439,711.940272 LUKE to 27 wallets |
| 30 Jun 13:31:23 to 13:43:37 | | The 27 wallets sell all of it |
| 30 Jun 13:34:50 | 429,888,279 | LUKE fee-sharing config created: 100 percent to 5Fcdrg |
| 16 Jul 14:26:48 to 19:36:57 | 433,289,898 to 433,334,952 | GV6U holds 584,284,604.165151 ANSEM, with no transaction on its ANSEM account in between; the X Article is posted at 18:01:07 (page time) |
| 31 Jul 22:54:39 to 1 Aug 00:09:38 | 436,445,677 to 436,456,324 | GV6U sends `7oU9nR9VEvFPwvp2PpXo2LQc6A92QRhcUTwhLWT7MsDM` (7oU9) 491,000,100 ANSEM in three transfers |
| 18 Sep 12:49:46 | 448,088,359 | 9fnyoj sends all its 790,001,160.671796 TJR to `9mX7fG5Gsnc8E4sbsYurcNkha6TBwE7WZJ5EXqVG8CGb` (9mX7fG) |
| 8 Nov 15:17:47 to 17:24:33 | 466,962,474 to 466,997,880 | The deployer buys ANSEM three times and, seconds after each buy, signs CreateV2 for a new mint, paying the ANSEM into the new curve |
| 9 Nov 23:15:18 | 467,498,291 | The deployer's ANSEM token account was closed |
| 15 Nov 18:19:39 | 469,827,596 | Another address makes the deployer the only creator-fee shareholder of a different coin that also uses the symbol ANSEM, and creates the deployer's ANSEM token account again (see "15 November") |

## What the chain shows

### The three creations and the supply bought in each

| Token | Create transaction | Slot | Time | Deployer SOL change | Creation buy (argument, SOL) | SOL received by the curve | Tokens received by the deployer | Share of the 1,000,000,000 supply |
|---|---|---|---|---|---|---|---|---|
| ANSEM | `4LteGjWEqA5RZ3EAgQMsw2pgNNnWs7ceKFebkkDSaah6uyYT91Vp8NQLNaRe2rytnSaDHCjoaMeiBnN1SgWQYc2u` | 426,930,467 | 16 Jun 21:05:48 | -86.070181840 | 85.8 | 84.742682579 | 792,454,486.758954 | 79.245% |
| TJR | `2Yh4EdCEkaSZhJq73ZhvoqkJbKuU5jrkyGGXjgi9XgtRNvCJv7CvD6JUBz1idDRijEbXWCedyGA9WAbEeToXCwhC` | 429,670,768 | 29 Jun 13:08:45 | -75.237795760 | 75.0 | 74.076015913 | 763,701,067.609494 | 76.370% |
| LUKE | `3FdyiMxn88PMaqBv8DtVENzmcjP8my2SKs3V6JRJRHnNFmHwnPFAXzhnt19GvCoDjPhiD2BFaLdD3qe3PycfuH2p` | 429,823,473 | 30 Jun 06:18:29 | -86.270754000 | 86.0 | 84.940213444 | 792,936,627.277769 | 79.293% |

- In each transaction the deployer is the first signer, the `user` account of `create_v2` and the decoded `creator` argument; the new mint is the only other signer. The instruction prefixes match the IDL for `create_v2` (`d6904cec5f8b31b4`) and `buy_exact_sol_in` (`38fc74089edfcd5f`).
- The deployer's SOL change includes the buy, fees, rent and a transfer of 0.003 SOL to a fee address.
- Each mint is a Token-2022 mint and carries its name and symbol in its own metadata, written in the creation transaction. The ANSEM name is "The Black Bull"; it matters in "Identity". The other two names are not written here because one is a personal name.
- The program ids were checked against the `address` fields of the published IDLs at the commit above. pump.fun's program source is not published, so the ids are checked against IDLs, not against source code.

### ANSEM: authorities, curve completion and migration in the creation slot

- **Authorities.** Inside the creation transaction the mint authority was set to the pump.fun mint-authority address `TSLvdd1pWpHVjahSpsvCXUbgwsL3JAcvokwaKt1eokM` with no freeze authority; the metadata update authority was moved to none; 1,000,000,000 tokens were minted to the curve; then the mint authority was set to none. On 15 November the mint, freeze and metadata update authorities were all none on both providers.
- **No transfer fee.** The mint has only the metadataPointer and tokenMetadata extensions.
- **Curve completed by another signer in the same slot.** The creation transaction is at index 279 of block 426,930,467. At index 1,383, `9ryBR3SnxgGPhWsKvsfxuNHUCTt6tSpLe8wrKCShXLaq`, through program `J7iAnje8zMfiTtUzNhHCyr2tHwVjPVVDu2XCD8sAXGy9`, bought the last 645,513.241046 tokens on the curve (`UGfH7ngiC1bq14Lwdw9Jp5PVCeDBksBJcenAPpoQCSZJhhmmxNF7YRFBjjL9NNzW4GbabZi7GG4RbFzga4bybjz`).
- **Migration in the same slot.** At index 1,384 the same signer migrated the curve to the pump AMM pool `FnzKY6x7entQ1eR3D225dQyT7ybfka4PskBMQhb8L3CC` and bought 30,077,097.302155 tokens from it (`Q8uA1zn27PzG7zhe53VPm5qkE7duD4MLdPpj5s8Ugf8FMNksqUDN5aAPTuZSV6MRmC4C57UxypxF6zaHzt1QT8K`). 206,900,000 tokens and 84.990359057 wrapped SOL went to the pool; the LP tokens minted (4,193,388.282529) were burned in the same transaction.
- So the deployer's creation buy did not by itself complete the ANSEM curve; another signer completed and migrated it about 1,100 transactions later in the same slot. Whether that signer is linked to any other address here was not tested. For TJR and LUKE, only that the curves were complete on 15 November was read, not when or by whom.

### The three large transfers

| Token | To | Amount | Transaction | Slot | Time | After the creation |
|---|---|---|---|---|---|---|
| ANSEM | GV6U | 650,000,000 | `5SGKQKgDfKYRv8XerDKWWEycXpz44JCdThmm4Rx6FzuaJujoGRhyYWf1dCVdakkHZPSeKTy3R9KgAR9TNfmEB3Db` | 426,930,558 | 16 Jun 21:06:25 | 37 s |
| TJR | 9fnyoj | 790,000,000 | `26yjQeSMibS1JFDkDu6KfjzTomwTJiZogZSUHonXHPLqXGmgc3LPKemvzd2reM77EfpBay2UJ9vLGRh8LXF2apeE` | 429,787,322 | 30 Jun 02:14:24 | 13 h 5 min 39 s |
| LUKE | 5Fcdrg | 750,000,000 | `1TASvAtpcTZ2Rp8GMiTH8PsPU3xRprPX89mTGRXJ7dbWquDpm7Brh3Ng2mbb4Gq86cmdHU3cnP2QYTvBk49XC3` | 429,887,676 | 30 Jun 13:30:45 | 7 h 12 min 16 s |

Each was signed by the deployer alone; in each the deployer paid 0.00239908 SOL (the fee and the new token account's rent) and received no SOL. The three receiving wallets are System-program accounts (ordinary wallets).

**Smaller transfers of the three tokens:**
- 29 Jun 13:15:59, slot 429,671,819: one transaction co-signed by `5xTa1Jk8D8qMKQdFz4Zf6bq2v3k3J3FErp3i8QDwUF6b`, `ETfskvN5iRqcTeeqTqy4qxUsBk16DY7e8QMXY4kKLKVZ` and `BphLTDUQPLUrbrePpjgBbb6SxvbFSdqQ9KoMhH1jSa4d` sent 15,058,297.691107 TJR to the deployer (`3onSzncUDQkGR4sYjpSTCxzDPy7ujYHCtwW4aGRfumaNqtz81iW18dY5dDqPxaz1ZEmdBgcraho7cz5YdR6ok6tA`), 7 min 14 s after the TJR creation. All three later received LUKE from the deployer.
- 30 Jun 02:14:45, slot 429,787,376: the deployer sent 29,048,787.424471 TJR in five transfers to `5JW5RHytofKA6C2WUMRPxjUjkQXiEQFUTSo2BJ1E8rbA`, `BKy5rx5YX5gVciAWNSnP1dSs3xehtR4TY82pK9jWCoCJ`, `G4ahiioRtcpB3QoBzGqxgEko2FyvqLcGqm5w2NZWSyVi`, `5X9hRtsBQWPJbhQMQXJxPfbWJgpo3MvwRxF1oePuaU9b` and `8rhFtjcpKhsiswF64FsTezike6kE6AoitVT185uS8WvA`. All five received LUKE from the deployer 11 hours later.
- 30 Jun 13:30:59 to 13:31:00: 39,439,711.940272 LUKE to 27 wallets (see "The 27 LUKE recipients").
- To GV6U, 16 to 29 June: 14 transfers of 14 other mints, 5M to 650M tokens each, each signed by the deployer alone. GV6U moved none of them out in the transactions read. To 9fnyoj: the 790,000,000 TJR, 100M of mint `2b27LMa8FbkWbHt8C5JzHciFyeKejFkCRyZ434Axpump` (30 Jun), 650M of mint `35y2jmNgXunevTnTmzJFiFhNenQpoEopDtQnpH5bV3W2` (20 Sep) and 600M of mint `Hc6295k1Cu9emcLYzMZNZHoqg87CqKXkpPvBMjramk9q` (9 Nov). Who created those other mints was not checked.

### The deployer's sells

A sell below is a transaction in which the deployer's token balance fell, its SOL rose and the logs show a Sell instruction; SOL is the deployer's net lamport change. All 93 sells went through program `FLASHX8DrLbgeR8FcfNV1F5krxYcYMUdBkrP1EPBtxB9` into the pump AMM (`pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA`); what the FLASHX program is was not identified.

| Token | Sells | Window | Tokens sold | SOL |
|---|---|---|---|---|
| ANSEM | 7 | 16 Jun 21:06:29 to 21:06:38 | 142,454,486.758954 | 159.405670644 |
| TJR | 3 | 29 Jun 13:14 to 13:15 | | 9.699984273 |
| TJR | 66 | 30 Jun 02:14:28 to 02:14:54 | | 792.755712105 |
| TJR, both windows | 69 | | 38,201,641.798321 | 802.455696378 |
| LUKE | 17 | 30 Jun 13:30:51 to 13:31:29 | 3,496,915.337497 | 415.019059711 |
| **All** | **93** | | | **1,376.880426733** |

- The ANSEM sells began 4 seconds after the 650,000,000 transfer; the 30 June TJR sells 4 seconds after the 790,000,000 transfer; the LUKE sells 6 seconds after the 750,000,000 transfer. The first three TJR sells came on 29 June, minutes after the TJR creation.
- The deployer also bought TJR once: 29 Jun 13:15:56, slot 429,671,811, 78,491,063.922191 TJR for 45.000205 SOL on the pump AMM (`3hVfvXyAFcS7S4KGiv1ajUHqKfkVHn3DAYGo6nbCUyPxkvye6Ab5GqX97AzzWM9TbU9g1zYFwwtVyqBDB1NJozGw`).
- **The deployer's books close at zero for each mint:** ANSEM 792,454,486.758954 in = 650,000,000 transferred + 142,454,486.758954 sold; TJR 763,701,067.609494 + 78,491,063.922191 bought + 15,058,297.691107 received = 790,000,000 + 29,048,787.424471 transferred + 38,201,641.798321 sold; LUKE 792,936,627.277769 = 750,000,000 + 39,439,711.940272 transferred + 3,496,915.337497 sold. When read on 15 November it held 0 of each of the three tokens.

### Creator fees: the configs, their admin and the payouts

Each fee-sharing config was created in one transaction signed by the deployer. Its log lists, in order: two CollectCreatorFeeV2, two CollectCoinCreatorFee, ExtendAccount, CreateFeeSharingConfig (shareholder: the deployer at 10,000 bps), MigrateBondingCurveCreator, MigratePoolCoinCreator, UpdateFeeSharesV2 (100 percent to the new shareholder) and DistributeCreatorFeesV2 (0 lamports).

| Token | Config | Created | Slot | Transaction | Shareholder (bps) | Created after |
|---|---|---|---|---|---|---|
| ANSEM | `9ENSWnedBEAvVB7jJKZrLRZ9vuVuJdBE7uJt2oAsG1jr` | 16 Jun 21:07:55 | 426,930,784 | `4ac9uBpNZZfraa5h2UPALPe5yPJKyrTnCpsabKDrS94e9691V5kH2dEWXoUFTx94mHD3GmRtTwwQtA9SsPdeaytV` | GV6U (10,000) | the 650,000,000 transfer and all 7 sells (1 min 17 s after the last) |
| TJR | `Hzzb5g5AcZMkmcDb9h4mFddEETeTosnjqR6KLCwLkvB5` | 30 Jun 02:16:28 | 429,787,622 | `4SMGuvieEeeHAFx8HVcTiFLDdSafrEEX9DGkohR5k587Ye4PcoLfefgozgfqdWDwBGbTZDZQbdGZfH6nPbLWXubW` | 9fnyoj (10,000) | the 790,000,000 transfer and all 69 sells |
| LUKE | `5q9aPR9bpJMxJeBKN6Yss82Vt2iNycd5ZEHj5MWhUn6y` | 30 Jun 13:34:50 | 429,888,279 | `5R61UtcfMZeCeL4BucxJBxBeiWj8GboBDHaiLBC6oDzQuxrxqEzHkxz7HeUWckJC8dtWn943m6urbaT7wq5FkbAU` | 5Fcdrg (10,000) | the 750,000,000 transfer, all 17 sells and the 27 transfers |

- **Decoded state, 15 November** (two providers, identical bytes): version 2, status Active, admin = the deployer, **admin_revoked = true**, one shareholder at 10,000 bps as above. The seeds `["sharing-config", mint]` give all three addresses. We infer that, with the admin revoked, the shareholder lists can no longer be changed through `update_fee_shares`. The transaction that set admin_revoked was not found.
- **Curves and pools point at the configs.** On 15 November each bonding curve's creator field and each pump AMM pool's `coin_creator` field was its config (two providers). We infer that the MigrateBondingCurveCreator and MigratePoolCoinCreator steps above are where these fields changed from the deployer to the config.
- **Before the configs existed**, creator fees accrued to the deployer. In each config-creation transaction the deployer's AMM creator-vault account `6SGwLrPy8MgNPqgHy3jhUU6mhZEwVWj6wQgXDD8nHBfo` held 0.494664926 (ANSEM), 0.652213533 (TJR) and 2.464723545 (LUKE) wrapped SOL before and 0 after; the deployer's net SOL change in those transactions was +0.485689111, +0.643289280 and +2.455780542. That vault is per creator, not per token, so these amounts may include fees from the deployer's other tokens.
- **Payouts read** (one provider). The amount of each `DistributeCreatorFeesEvent` equals the shareholder's lamport change in all 169 nonzero payouts not signed by the shareholder.

  | Token | Shareholder | Nonzero payouts | SOL paid out | First and last nonzero payout | Coverage |
  |---|---|---|---|---|---|
  | TJR | 9fnyoj | 18 | 1,071.122709502 | 30 Jun 02:18:49, 5 Nov 01:50:39 | complete |
  | LUKE | 5Fcdrg | 4 | 360.257210030 | 30 Jun 17:52:59, 11 Oct 00:18:16 | complete |
  | ANSEM | GV6U | 161 read | at least 2,694.835774176 | 16 Jun 21:11:00, 14 Nov 00:42:32 | partial: 446 of 672 successful vault transactions (3 to 17 Jul) not read |

  - A spread sample of 60 of the 446 unread transactions (58 payouts) suggests that the unread part is several hundred SOL. That is a sample estimate, not a chain total, and no total is given here.
  - Anyone can trigger a distribution; most ANSEM payouts were sent by `pisDHRFwgiqEzdkHsu7gwigjSW1qesyfQdpgDMVwwA4` on a 30-minute schedule. The sender of a payout is not its payee.
- **Not yet distributed** (two providers, 15 November, slot 469,834,178): wrapped SOL in the AMM creator vaults of ANSEM 5.948410879, TJR 3.500914010 and LUKE 1.947417580.

### Where the transferred tokens went

- **ANSEM, GV6U.**
  - 16 to 17 Jun: four inflows of 1,000,000 ANSEM from `4aArEDkqkPBwFiSCShd6GJ8dTFHzZboGf3GD7qwxxTu3`; GV6U's balance was then 654,000,000.
  - 17 Jun 13:14 to 27 Jun 23:56:59: no transaction on GV6U's ANSEM account (10.4 days).
  - 28 Jun 02:07:53 to 02:28:54: GV6U signed 7 transfers of ANSEM to seven wallets. No sale.
  - 29 Jun, about 09:50 to 19:00: GV6U signed many transfers of under 1 million ANSEM each; the 22 sampled went to 22 different owners. Their full count and recipients were not read.
  - 16 Jul, the article date: 584,284,604.165151 ANSEM after slot 433,289,898 (14:26:48) and before slot 433,334,952 (19:36:57), with no transaction on the account in between. That is 58.428 percent of 1,000,000,000; the supply on 16 July was not read, and against the supply of 15 November (997,353,904.476913) it is 58.583 percent.
  - 31 Jul 22:54:39 to 1 Aug 00:09:38: GV6U sent 7oU9 100, then 1,000,000, then 490,000,000 ANSEM. 7oU9 had sent no ANSEM when read on 15 November: all 46 transactions on its token account were read.
  - No GV6U sale was seen in the transactions read, and none of them changed GV6U's SOL by more than 0.05 SOL (within the transactions read).
- **TJR, 9fnyoj.** On 18 Sep 12:49:46 (slot 448,088,359) 9fnyoj sent all 790,001,160.671796 TJR to 9mX7fG (`vm1YtcxhyGyVC83zrhikREY7UV3AhMbVPVtw97h12zUeBM6mKHJz1RFzgwBQ9HFQ5ycCLMZjVSPA7iw2RfPmEyC`). Nothing had moved from 9mX7fG when read on 15 November.
- **LUKE, 5Fcdrg.** The 750,000,000 had not moved when read on 15 November; there were only three dust inflows (+10, +3, +100), so the account held 750,000,113 LUKE.

### The 27 LUKE recipients and the TJR creation-slot buyers

On 30 Jun at 13:30:59 (slot 429,887,710, 8 transfers) and 13:31:00 (slot 429,887,711, 19 transfers), the deployer sent 39,439,711.940272 LUKE to 27 wallets, in 27 transactions it signed alone. Every one of the 27 then sold. All 884 transactions on the 27 LUKE token accounts were read. On 15 November all 27 held 0 LUKE (two providers).

| # | Wallet | LUKE received | Sells | SOL from the sells (net) | First sell | Last sell |
|---|---|---|---|---|---|---|
| 1 | `BffHd1bcMpCg7aWXdDzT9dKx3msovaJiTq5ocFXy6RRK` | 1,728,630.761034 | 30 | 202.095389964 | 13:32:06 | 13:43:29 |
| 2 | `5JW5RHytofKA6C2WUMRPxjUjkQXiEQFUTSo2BJ1E8rbA` | 1,677,375.468911 | 23 | 197.194087240 | 13:31:45 | 13:33:13 |
| 3 | `FkCcgvCoR6p6BRucCnU1t1DXP97Y3rJeMYBiU1o31nuv` | 1,573,105.096328 | 12 | 188.195024846 | 13:31:23 | 13:31:29 |
| 4 | `4SA9AGeRRvtcwGmwBoBjQ3GTbyMZf6Ug1rScAy1HNk79` | 1,682,707.277949 | 20 | 172.912358568 | 13:32:06 | 13:34:27 |
| 5 | `5xTa1Jk8D8qMKQdFz4Zf6bq2v3k3J3FErp3i8QDwUF6b` | 1,716,522.018761 | 19 | 171.639628786 | 13:34:03 | 13:34:27 |
| 6 | `FAiQ6YFHwUSQYHxPK7VXoMUqhCDhxT54mPjDQPY7rywU` | 1,550,991.199829 | 23 | 170.836720651 | 13:33:27 | 13:34:57 |
| 7 | `2j1fFCiNF5PKuwnPC6LZf3woHRwtP55oQsK9qfHjSUE5` | 1,322,224.543002 | 42 | 157.995797111 | 13:31:40 | 13:33:25 |
| 8 | `9x8erDpq4LFvynx4uf5XdRArT8QjTnPE8fGXv6gKp59z` | 1,371,725.873901 | 23 | 151.485829228 | 13:33:27 | 13:34:57 |
| 9 | `SxDasgLe2c97QU14P1oqa1JUoC4pST2tspC3Q7FyZzU` | 1,201,480.919983 | 44 | 143.157650002 | 13:31:40 | 13:33:25 |
| 10 | `BphLTDUQPLUrbrePpjgBbb6SxvbFSdqQ9KoMhH1jSa4d` | 1,322,824.735714 | 25 | 137.743515030 | 13:32:38 | 13:34:38 |
| 11 | `34qWhtTEmLYBwZnFWjU1qDHwgaGScDHwSfFbGF1oBX2Z` | 1,294,370.939507 | 24 | 134.539126008 | 13:32:38 | 13:34:38 |
| 12 | `2SA6T5FAMdv4MZiE6283n7QkMMaBB3bG7rk2Lhgts1FB` | 1,712,361.459578 | 24 | 132.542022187 | 13:40:17 | 13:43:23 |
| 13 | `ETfskvN5iRqcTeeqTqy4qxUsBk16DY7e8QMXY4kKLKVZ` | 1,535,858.185545 | 66 | 124.454079549 | 13:35:01 | 13:36:03 |
| 14 | `FHXS2GanXbNfXkSJB7xiPa3cjsLTfVDaAiFEmTBXWRm3` | 1,466,754.444153 | 20 | 120.435749613 | 13:40:23 | 13:43:37 |
| 15 | `GuEFvJidK7zk2mCKbM1XTcX8NCqrMQR7YthHnsUPsBih` | 1,472,954.493132 | 67 | 119.768830702 | 13:35:01 | 13:36:02 |
| 16 | `7UobKbZk92u7QwmgUpWNnER5pQenBvhmVrxYQCkpbWgm` | 1,616,465.069526 | 58 | 119.135476552 | 13:35:24 | 13:36:03 |
| 17 | `7tJx8rxJx37S3S1egDDAbwpv68kDteCbXKWUm75B7q1i` | 1,652,423.768039 | 13 | 114.595874387 | 13:37:12 | 13:37:23 |
| 18 | `8rhFtjcpKhsiswF64FsTezike6kE6AoitVT185uS8WvA` | 1,578,221.302158 | 15 | 111.984032539 | 13:36:47 | 13:37:07 |
| 19 | `G4ahiioRtcpB3QoBzGqxgEko2FyvqLcGqm5w2NZWSyVi` | 1,338,860.952622 | 22 | 108.877263014 | 13:31:45 | 13:40:08 |
| 20 | `5vKQ5VczYpQyiTKGzTwCebyF8RN9RnD8zfLTCB7ECMc` | 1,622,600.600113 | 21 | 101.834965977 | 13:36:06 | 13:38:16 |
| 21 | `JDAG2JuAQtdpyV7GHt9dkh4kXYeap7Ew1Gc2am6v9WXD` | 1,289,062.438924 | 57 | 95.096276591 | 13:35:24 | 13:36:02 |
| 22 | `8NXt2YRnkASr7BEJHMwYwzpPaPMsePZdVSZ1fCqVPM9X` | 1,470,810.115289 | 21 | 92.489897173 | 13:36:06 | 13:38:13 |
| 23 | `A6b21eYxLY4sVZE7KLRcKo38aztjqJXhXo8E4q9VMnoW` | 1,413,057.171270 | 17 | 88.629312650 | 13:35:52 | 13:36:02 |
| 24 | `BKy5rx5YX5gVciAWNSnP1dSs3xehtR4TY82pK9jWCoCJ` | 1,192,979.161092 | 16 | 88.121356337 | 13:38:36 | 13:38:58 |
| 25 | `5X9hRtsBQWPJbhQMQXJxPfbWJgpo3MvwRxF1oePuaU9b` | 1,209,161.055843 | 13 | 87.541644340 | 13:39:30 | 13:39:49 |
| 26 | `71qcJSAfTNc8GDwd1Jjd6GEy6VfZc1EMBqWP6FjzdDx5` | 1,211,923.107737 | 11 | 85.383187061 | 13:39:03 | 13:39:27 |
| 27 | `23xmd6BXDNVc65ogLAf6j7EAx4R1Je5cEL8ju1dxtvKc` | 1,214,259.780332 | 12 | 78.644089085 | 13:37:26 | 13:38:07 |
| | **Total** | **39,439,711.940272** | | **3,497.329185191** | | |

- SOL from the sells is the wallet's lamport and wrapped SOL change over its sells (a transaction in which its LUKE fell and its SOL rose).
- The first sell (FkCcgv) came 23 s after the last transfer; the last sell was at 13:43:37.
- **TJR creation-slot buyers.** Block 429,670,768 holds 2,108 transactions. The TJR creation is at index 1,433. Indexes 1,434, 1,435 and 1,436 are three TJR buys, each co-signed by two or three wallets that later received LUKE:

  | Index | Transaction | Co-signers (all later LUKE recipients) | TJR bought |
  |---|---|---|---|
  | 1,434 | `3WPzvvc2k2NmxBhK9NAKGU42362iKfgysSxMBiEkrCV4eAjTFKe2i7kFgqgCED3z3GSoe5EX9AWV6ufMoaQ5pUP8` | 5xTa1J (9,805,479.586748), BphLTD (2,727,006.166295), ETfskv (3,207,563.479637) | 15,740,049.232680 |
  | 1,435 | `565AEMQTEdqbDxgysUkFMmjAvumC4K1VeLtG9MD16rCFAX5eYqTJdAVaTvHVC1tYZzXoMVsj9obfnZkYroHCs3UT` | 2SA6T5 (2,620,476.523853), SxDasgLe (2,574,106.667271) | 5,194,583.191124 |
  | 1,436 | `4VyaCC3pGa15dd7N3bprB1ttYYSdfjwQtfj5rdv6JNppBM8Vv5fyRuRk2s4ijSsM7toSE45SXTo8Vi49SoN13pTW` | 2j1fFC (3,652,572.476742), 34qWht (3,439,882.786066) | 7,092,455.262808 |

  So seven LUKE recipients bought TJR in its creation slot, in the three transactions directly after the creation. Three of them (5xTa1J, ETfskv, BphLTD) co-signed the 15,058,297.691107 TJR transfer back to the deployer 7 min 14 s after the creation.

### SOL to and from FkCcgv, bounded

- **First funds.** The deployer's first transaction is `4bv34kJFT2BnsvW7sbCRNPS59Y6Ggjj6REQdpQLZ1DYQh6Zw9AtXoWPoQVBZxQRemDoTt3QyuFSrXfxdAK5Nu7Z7` (20 Apr 13:00:49, slot 414,479,400): 4.431561 SOL from BY4StcU9, sent with a durable nonce (nonce authority `38QU8LKVK1Ew5uzsqttamNTTFxvnfzgi2ACQvj3ekuom`). Before the 13:02:25 transfer from FkCcgv, the deployer's address has exactly this one signature. BY4StcU9 held 1,996.263788767 SOL before that transfer.
- **20 Apr 13:02:25** (slot 414,479,640): 9.126416323 SOL from FkCcgv (`3dsLwZLx7qLirUthoDoLvCdYh72DPQpY66UjSa3vikjwAtjc3XQ8DMuqkWVTfeXna2evpry2JiB1cYc8we78Cg77`), 1 min 36 s after the first funding. FkCcgv is also one of the 27 LUKE recipients.
- **Four minutes before the ANSEM creation.** In slot 426,929,835 (16 Jun 21:01:38), ten addresses sent the deployer 79.233316361 SOL in ten transfers:

  | From | SOL | Transaction |
  |---|---|---|
  | `FkCcgvCoR6p6BRucCnU1t1DXP97Y3rJeMYBiU1o31nuv` (LUKE recipient) | 13.053702027 | `25A4WR8gjAXTxMYn5DcdM3SDtmyfKHr8RFLLAoEQ1i3uoBW74cXWcrjRu4ZtyCWzhy2SDoMiM9XSeDrf3USDT6Ye` |
  | `23xmd6BXDNVc65ogLAf6j7EAx4R1Je5cEL8ju1dxtvKc` (LUKE recipient) | 9.547408877 | `2vLBjnKQVDE4EtfGe4AHZihfNxuZFvft13cX8zNUpo3wkZ1vydiu4u97YQR59ioouSxTBJuQXLQ3xjiW4v2DoNkA` |
  | `7tJx8rxJx37S3S1egDDAbwpv68kDteCbXKWUm75B7q1i` (LUKE recipient) | 9.193772293 | `45rKp9k7k9fJw2XsYYsjqyNfwYv6oV33XUriwqnZvbWMfX3TsNKXhn3L6A5JJ4U6y8BNnBRk7We9JRzXfTDdXutz` |
  | `HvEu15xLgndNraJZ5D62ByxQ9G3wTBrSKUQRgPtoDW2k` | 7.953890908 | `c8Bk7HKXLy3KBu1ZqDnE11n6reaBvy97MmktK2gvAK61FEXKAoHgKjTBxsKxK4QuB9DAyyH2eqpfnkdgjGiHB69` |
  | `73y3pskdVhF7U99icJXvEvLSEvhyzPZbotd6FfCnjVtn` | 7.105528899 | `5RGXcPeq4aaxT3ecxfALtzBar26186S1jXbbfwS3Xhva5giaRuJRHZ7kMWnPxJvdkfQmvGwqemGrCgNoTF5JHipN` |
  | `3AUdGcxHNhgRipbsT8ge8T899xBejRoiCvAhirDx9fvd` | 6.953053779 | `3Qq1wxUTFWxq5djXmqzs4SLfvMkRSttPCKM84ynRB2LkaapJeFsK4PKymdzeD68PoQyVj21hWWexQ77EDHMMGnGq` |
  | `5aLNJiyqpLyBidUrAaZzf2fHWqHN9F7AvghaeLVetksp` | 6.890475054 | `5CHDx7u7bvCiGNY9zjfxyRnwpe7B8vufnMDftaco4JCETdCd84C53Q9kZvuLEJdf5mrnRfqpH8XSHE418yk5FE7B` |
  | `94yrHzw2RizzReNWoKR5MrzygjpzyABBH92Lw1zxutz1` | 6.719109256 | `59hY2j84y6rsh1GiSnCnpyQxBXfTWuTWRngA6QH8ajg7Kkkt4wRygNg6CDwSwLUcrAKRupMhJc7PDp7zzLCDUFup` |
  | `GDW9y6sT4bXKMqmZFh7CUStjqwAexyfafzBkrRYVnTHf` | 6.390695684 | `3vZkSXGjSyXPM6Mu2BerANREmuzAYnD1FZbLMGNUZ83DZYrUip4KWA5KDSqDojz8stnebs999WVRwYWdrtEEbMjm` |
  | `SxDasgLe2c97QU14P1oqa1JUoC4pST2tspC3Q7FyZzU` (LUKE recipient) | 5.425679584 | `4BYnnT34DUe8Kg97GVEtLTS1Ha3CERiLsKsifMGSLtRbAikjtMZZumdAtdFKkPNq7WqiAvfeLCJBuF3R6XL6UJrf` |

  The creation at 21:05:48 cost the deployer 86.070181840 SOL. `3AUdGcxHNhgRipbsT8ge8T899xBejRoiCvAhirDx9fvd` had itself been funded by BY4StcU9 on 17 May. Three of the other senders (`94yrHzw2RizzReNWoKR5MrzygjpzyABBH92Lw1zxutz1`, `HvEu15xLgndNraJZ5D62ByxQ9G3wTBrSKUQRgPtoDW2k`, `73y3pskdVhF7U99icJXvEvLSEvhyzPZbotd6FfCnjVtn`) were first funded by `BmFdpraQhkiDQE6SnfG5omcA1VwzqfXrwtNYBwWTymy6` (3.0 to 3.9 SOL each, 30 Apr to 26 May).
- **Look-alike dust senders.** In the same minutes two addresses whose first four and last four characters copy addresses above sent the deployer 10,000 lamports (0.00001 SOL) each: `FkCc2K2KhD3rSM4PtoeQPf67Bz3mA9gQqEJ8Lh9o1nuv` (21:04:06, slot 426,930,210; it copies FkCcgv) and `7tJxYWDjfTnJU8yucm6Yzx9TyTvZkgQhi8dFaRGe7q1i` (21:02:13, slot 426,929,924; it copies 7tJx8r).
- **Bound.** Between 20 April and the ANSEM creation the deployer has 23,797 signatures, 6,551 of them successful; 80 successful ones were read in full (the first 40 and the last 40). The funding picture above is a lower bound.
- **Deployer to FkCcgv.** 24 SOL transfers from the deployer to FkCcgv between 16 June and 1 July, each signed by the deployer, gave FkCcgv 6,893.086879788 SOL in total. This is a lower bound, from the transactions fetched only. The transfers after each sell window:

  | Window | Transfers to FkCcgv | SOL received by FkCcgv |
  |---|---|---|
  | ANSEM, 16 Jun 21:40:25 | 1 (and 10.27 SOL to F5XqYt in the next minute) | 147.876822828 |
  | TJR, 30 Jun 02:34:44 and 02:38:16 | 2 | 989.228614234 |
  | LUKE, 30 Jun 13:54:07 and 13:54:36 | 2 | 1,183.872029593 |
  | **These three windows** | **5** | **2,320.977466655** |

  The other 19 were on 28 Jun (8), 29 Jun (4), 30 Jun 15:18 to 19:05 (6) and 1 Jul 23:03:08 (1). Further deployer-to-FkCcgv transfers outside these 24 were seen on 30 June, 1 July and 5 to 7 July. FkCcgv's full history was not read. The deployer's balance rose between the TJR and LUKE windows from inflows not attributed here, so the 13:54 transfers are not shown to be only LUKE proceeds.
- **FkCcgv to the deployer.** Six transfers, 506.865536809 SOL, signed by FkCcgv, between 20 April and 30 June (lower bound).
- **LUKE recipients to FkCcgv.** In slot 429,891,218 (30 Jun 13:54:36), the slot of the deployer's 287.968865158 SOL transfer to FkCcgv, at least 13 of the LUKE recipients each sent FkCcgv SOL in a transaction it signed alone. Between 05:40:01 and 05:40:08 that day (38 minutes before the LUKE creation) twelve wallets that later received LUKE sent FkCcgv more than 818.07 SOL in 23 transfers. Over all transactions fetched, the 26 recipients other than FkCcgv sent FkCcgv more than 5,061.19 SOL. These are lower bounds.
- **From FkCcgv onward.** On 30 June FkCcgv sent 2,000 SOL to `FZEFKLaBSjQ4XaxuLnGWdzxpkujt4MxVjdi7z34NyLbA` (13:55:38), 1,500 SOL to `F5XqYtdUWUT7bbuuKEjckDs8Hwk7j7mhdwGe3YKn5Xf7` (13:58:36) and 1,500 SOL to `AvYukzeAFzFo66i1GJHShcdBbb4jeSkZiEJnNMds54mo` (13:58:45), and later round amounts to these wallets, to `9bxyzm6MFn3TWEedvYuMzSaZkkGWKSyTgWpRXCzMP3dm` and to `ALQS3TWUEMisWpkuaoj8JVxFVrL6xxxfzYS6TXQKweS9`. This list is incomplete: 90 of the 1,098 FkCcgv signatures listed for the window read were read. None of the second-hop wallets FZEFKL, F5XqYt, AvYukz and 9bxyzm shares a transaction with GV6U, 7oU9 or 9fnyoj in the periods read.
- **On 15 November** (two providers): FZEFKL held 10,000.151415719 SOL; it received 4,000 SOL from FkCcgv in the transactions read and its other inflows were not read, so its balance is not shown to be these funds. AvYukz and ALQS3T no longer existed; of the ten largest LUKE recipients, the nine other than FkCcgv no longer existed.

### The ANSEM mint on 15 November, and the 8 and 9 November activity

- **Mint.** Token-2022, 6 decimals, mint authority none, freeze authority none, metadata update authority none, only the metadataPointer and tokenMetadata extensions. Supply 997,353,904.476913 at slot 469,840,902: 2,646,095.523087 ANSEM fewer than the 1,000,000,000 minted. Supply can only fall, by burns; when they happened was not read. The mint account holds 26.201510966 SOL against a rent minimum of 0.00268732 SOL; where the 26.198823646 SOL above the minimum came from was not read.
- **Curve and pool.** Bonding curve `FxC6pJJSiu6efSn8PmBMQjQaYm6dkSqmQYohui6NPnrf`: complete, reserves 0, creator field = the ANSEM fee config. Pool: `FnzKY6x7entQ1eR3D225dQyT7ybfka4PskBMQhb8L3CC` (pump AMM).
- **Largest holders** (all Token-2022 accounts of the mint, read at slot 469,801,574: 384,547 accounts, 156,035 of them not empty; owners read on both providers):

  | Rank | Wallet (token-account owner) | ANSEM | Wallet type |
  |---|---|---|---|
  | 1 | 7oU9 | 491,003,700.487968 | system wallet |
  | 2 | GV6U | 87,469,335.103990 | system wallet |
  | 3 | `87ZDLDDbMAqmHJwsAgNjpJVCf9gZvwMJJMbFbXNTrkva` | 26,010,449.754830 | system wallet |
  | 4 | `9SLPTL41SPsYkgdsMzdfJsxymEANKr5bYoBsQzJyKpKS` | 12,518,553.231214 | system wallet holding 417,591.430903745 SOL |
  | 5 | the pool FnzKY6 | 11,961,103.542249 | pump AMM pool account |

  GV6U and 7oU9 together held 578,473,035.591958 ANSEM, about 58.0 percent of the supply. Later reads: GV6U 87,470,495.169219 (slot 469,840,873) and 332.930413498 SOL (slot 469,842,504); 7oU9 491,003,700.487968 (unchanged) and 0.150142025 SOL.
- **8 November.** Three pairs of deployer transactions, each pair seconds apart, all version 1:

  | Time | Slot | Transaction | What |
  |---|---|---|---|
  | 15:17:47 | 466,962,474 | `4ju3sB4zmA35YWjDHd52qRq7Ppj6JUhJBe7S5KMA8MiZTGKUzHFG4V8s59Bby3hNqtwwDXXkUijwEt5HWPuoHRHb` | The deployer buys 231,442.748187 ANSEM from the pool FnzKY6; its SOL change is -121.401593741 |
  | 15:17:47 | 466,962,476 | `fAYrjfuU4CXwLDgK4n3c4hB2qE2XrDfREAqGBMaojPQc5XjBb3xcPzTU7nRyb1mxiwP6rUvBFfBM4EPXCR9vX6e` | CreateV2 of mint `3JmVNVLfvSpcoVx5VEUXfejdYrok81GqenpZSqFbpump` (signers: the deployer and the new mint); in the same transaction the deployer pays all 231,442.748187 ANSEM in and receives 801,663,094.88667 of the new token |
  | 15:47:43 | 466,970,842 | `4nuxbkTLXAJGPrQu72dwekvHQhu1xjjsbueEEEmbZSKeQr4idAyAxrURkCNZikzaFTT2nJy7AffE5XBJNM3Ma2bC` | Buys 201,991.198324 ANSEM; SOL change -112.454285563 |
  | 15:47:43 | 466,970,843 | `4tABx6NLW8yNgtFYWnCLTY8wiKwuQdsdkyNLNCRQFxKbHHPyYRV1ksTsbZ2QngxuNGqykeajATP65SyG4VWwnmyZ` | CreateV2 of `ErvM3kEjJeCJZ24RSs4H75nSHGxkNxZaDyDKb2odpump`; pays 201,991.198324 ANSEM in; receives 802,005,124.709152 of the new token |
  | 17:24:32 | 466,997,874 | `2MjVk28kVJkvihq6GVEg9JZUUpCotAMyHqjDbV9PEx7hmXgBZLWQV8JUe6MvX1vY83uanbuwqdUeNjyMqosEwBoz` | Buys 174,544.556078 ANSEM; SOL change -115.365457176 |
  | 17:24:33 | 466,997,880 | `2TpHy4m3EjV5BrYi3vpwbB9oh5SgpKwpzYtE3GtTMRvtREJknpxUbdsM3UXtBxyidtx9jrbTgc5njz48SqVA6qgQ` | CreateV2 of `9zeTqCPi9Ct8eFmgBSY9dr47U8o7e5DWKXkBVqQYpump`; pays 174,544.556078 ANSEM in; receives 801,285,591.077938 of the new token |

  - The three buys total 349.221336480 SOL of deployer change. Each creation transaction logs CreateV2 and BuyExactQuoteInV3; we infer that the three new tokens use ANSEM as their quote token, and that in each the deployer took about 80 percent of the new supply.
  - What happened to the three new tokens after their creation was not read.
- **9 November.** At 15:06:46 (slot 467,361,872) the deployer moved its last 0.098528 ANSEM out, and at 23:15:18 (slot 467,498,291) its ANSEM token account `4T8fGRJtHQeDn4PhXAehEvFYrXho21h8RPYWsbkmpTLA` was closed in a transaction co-signed by `AxiomRYAid8ZDhS1bJUAzEaNSr69aTWB9ATfdDLfUbnc` (`2UQ47VmdTGvthKUXVBpVGDkbHnBwoocspB7EXqZUZgjJXuwj7Q932WRbNuyveh6zsisGEEfyeHaddiuZjAuCp58W`).

### 15 November: another coin with the symbol ANSEM

This is a dated fact, read by EXIT on 16 November 2026; it falls inside the read window of 15 November above.

- On 15 November 2026 at 18:19:39 UTC (slot 469,827,596), transaction `3WTMRP8LPQJDGoHSCfiKPW2gdEeJVuzS2kn1Hp2ZKHA33buwvYsyUQWPxD7whWQm5zFAeh5UPMWg2uTFySu4KyBa` (version 1), signed by `HpKUzxQetUfbEMRRt96HfGZ5w1MjqYaQkhZaLyxDooDW` alone (the deployer did not sign it), logged SweepCreatorFee, CreateFeeSharingConfig, MigrateBondingCurveCreator, UpdateFeeSharesV2 and DistributeCreatorFeesV2 for mint `6r1BRGRNS6mWDz7FLR8s1SQsT9XiXp6MSMdNAzarpump`. That is a different Token-2022 mint, whose metadata name is "The Xmas Bull" and whose symbol is also ANSEM.
- Its fee-sharing config `AZ4auxKRdmA8QuE9PnYmGNi6d4sc2hSDrSLUuPr2acZM` lists one shareholder, the deployer, at 10,000 bps; its admin is HpKUzx, and the admin right is revoked (both providers, 16 November).
- The same transaction created the deployer's ANSEM token account `4T8fGRJtHQeDn4PhXAehEvFYrXho21h8RPYWsbkmpTLA` again, with 0 ANSEM. That account had been closed on 9 November; at slot 469,840,896 it held 0 ANSEM.
- Who controls HpKUzx, and whether it is linked to any address in this note, was not tested.

### The 30 June claim, tested

A third-party post of 30 June 18:02:54 says, in paraphrase, that the article author took money made on other tokens and bought back into his own token. We tested it for two hops:
- **GV6U (DIRECT @blknoiz06).** Every transaction on GV6U's ANSEM account was read for 16 Jun 21:06 to 28 Jun 14:23 and for 29 Jun 13:10 to 30 Jun 18:26; no buy by GV6U appears. The only buys delivered to that account were made by a third party, `GdWaMFZ2Ajp4q6h52jRAJAMXENUEUKbH47JRsjmS7DtD`: about 2,250 ANSEM in all, bought with fees from its own coin. For 28 Jun 14:23 to 29 Jun 13:10 and 30 Jun 18:26 to 16 Jul only balance samples were taken; they show no net inflow above 5,000 ANSEM, and a buy offset by GV6U's own outflows in the same interval could be missed. GV6U never held TJR or LUKE.
- **The sale proceeds.** The deployer made no ANSEM buy between 16 June and 8 November (its ANSEM account history is complete for that period); its three ANSEM buys of 8 November are above. FkCcgv never had an ANSEM account. No transaction includes both FkCcgv and GV6U between 16 June and 16 July (both signature lists complete for that period). None of the four second-hop wallets touches GV6U, 7oU9 or 9fnyoj.
- **9fnyoj (TJR fee shareholder, no account identity).** On 30 June it bought more than 929,000 ANSEM in five buys (02:23, 02:27, 02:41, 15:27 and 18:34). The first three were paid with USDC from `F7p3dFrjRTbtRp8FRF6qHLomXbKRBzpvBLjtQcfcgmNe`, a wallet with over 12,000 signatures in 8 hours; the last two used SOL swapped to USDC. Between 02:29 and 18:34, 9fnyoj received SOL from the TJR creator-fee vault and from other coins' fee vaults.
- **Result.** Not supported for GV6U in the windows read. The described pattern appears for 9fnyoj, which has no DIRECT or STRONG identity.
- **Limits of this test.** GV6U's SOL outflows, and any buys or liquidity adds delivered to an account other than its ANSEM account `2U9XFtekYTstzMYXmuyDCNdFxRYB91dMtSKxtUB5rVct`, were not traced. 28 Jun 14:23 to 29 Jun 13:10 was only balance-sampled.

## Identity

**Tiers** (EXIT's rule for this note):
- **DIRECT:** the account's own public statement or profile, or token metadata the creator set, names the address or mint.
- **STRONG:** a verifiable on-chain transfer or signature link to an address that is DIRECT.
- **WEAK:** anything else, such as timing, third-party claims or tags in other people's posts.
- Only DIRECT and STRONG are shown as matches, with the account named. WEAK items are unconfirmed leads; their account names are not published.

A DIRECT match means that the account publicly named, or badge-linked, the address; it does not prove sole control at every point in time. A STRONG link says that a wallet transacted with a DIRECT address; it does not say who controls that wallet. The pump.fun profile badges are as they stood on 15 November 2026 (pump.fun pages are third-party pages, not chain facts). Account statements are quoted briefly, as the account wrote them.

### Matches (DIRECT and STRONG)

| # | Account | Address or mint | Tier | Evidence | Date |
|---|---|---|---|---|---|
| M1 | @blknoiz06 | GV6U, the ANSEM fee shareholder (100 percent) | **DIRECT** | Own post "i just linked my X to a pumpfun account" (https://x.com/blknoiz06/status/2066989048497905753); its short link redirects to pump.fun/profile/GV6UUmNxz2RpKxmNAPadYKb7uQpszwqQAu3qLJxVdC52. That pump.fun profile ("ansemconzimp") shows the wallet GV6U and a verified X badge to user ID 973261472, which resolves to @blknoiz06. | post 16 Jun 20:59:26; profile read 15 Nov |
| M2 | @blknoiz06 | ANSEM mint | **Self-stated takeover (CTO), not creator** | Own posts: "i said i would CTO it" (16 Jul, https://x.com/blknoiz06/status/2077778065401295299), and a 9 July post whose $ANSEM cashtag resolves to this mint. The CreateV2 signer of ANSEM is the deployer, not GV6U. | 9 to 16 Jul |
| M3 | @Supermanonchain (suspended when read) | the deployer, `yHCxHBEaJW5tbndqC8JciSThr7U1cqLpdcsvHcx6PRe` (CreateV2 signer and fee-config admin of ANSEM, TJR and LUKE) | **DIRECT** | Wayback Machine copy of 2 October 2026 of that account's page (https://web.archive.org/web/20261002043156/https://x.com/Supermanonchain/status/2071581476207182216): bio "My only dev wallet : yHCxHBEaJW5tbndqC8JciSThr7U1cqLpdcsvHcx6PRe" (the full address, string-equal). The pump.fun profile of the address ("supermandev") shows a verified X badge to user ID 2024679536110292994, the ID of the archived page. | archive copy 2 Oct; profile read 15 Nov |
| M4 | @Supermanonchain | TJR mint | **DIRECT** | TJR's creator-set metadata cites post 2071581476207182216; that post, 39 s before the mint, reads "im the dev of the TJR coin". The TJR CreateV2 signer is the deployer. | 29 Jun |
| M5 | @Supermanonchain | LUKE mint | **STRONG** (through the CreateV2 signature of the DIRECT deployer) | The LUKE creation is signed by the deployer and logs CreateV2. Support only: LUKE's creator-set metadata cites a @Supermanonchain post 6.5 s before the mint; that post could not be read (account suspended, no archive copy). | 30 Jun |
| M6 | @Supermanonchain | ANSEM mint (on-chain name "The Black Bull") | **DIRECT** | Own post and bio in the archive copy: "im the dev behind The Black Bull" and "Dev of $ANSEM The Black Bull"; the on-chain name of the ANSEM mint is "The Black Bull"; the CreateV2 signer is the deployer. | archive copy 2 Oct |
| M7 | the deployer (M3) to GV6U (M1) | 650,000,000 ANSEM | **STRONG** (both ends DIRECT) | Transfer signed by the deployer alone, 37 s after the creation. | 16 Jun 21:06:25 |
| M8 | the deployer to GV6U | 14 transfers of 14 other mints, 5M to 650M each | **STRONG** | All signed by the deployer alone; GV6U moved none of them out in the transactions read. | 16 to 29 Jun |
| M9 | the deployer and FkCcgv | SOL both ways: 24 transfers, 6,893.086879788 SOL to FkCcgv (lower bound); 6 transfers, 506.865536809 SOL back, including the 9.126416323 SOL of 20 April | **STRONG**; FkCcgv has no account identity | Transactions signed by the deployer and by FkCcgv | 20 Apr to 1 Jul |
| M10 | the deployer to the 27 LUKE recipients | 39,439,711.940272 LUKE in 27 transfers signed by the deployer alone | **STRONG**; no recipient has an account identity | the 27 transfers | 30 Jun 13:30:59 to 13:31:00 |
| M11 | the deployer to 9fnyoj | 790,000,000 TJR; 100M of 2b27LM; 650M of 35y2jm; 600M of Hc6295 | **STRONG**; 9fnyoj has no account identity | each signed by the deployer alone | 30 Jun to 9 Nov |
| M12 | GV6U to 7oU9 | 491,000,100 ANSEM in three transfers signed by GV6U | **STRONG**; 7oU9 has no account identity | the three transfers | 31 Jul to 1 Aug |

The seven LUKE recipients who bought TJR in its creation slot, 5Fcdrg, FZEFKL, F5XqYt, AvYukz, 9bxyzm and ALQS3T are reached only through these links; none of them has an account identity. 5Fcdrg is STRONG to the deployer through the 750,000,000 LUKE transfer and has only a WEAK lead (W1).

**Denials.** @blknoiz06 answered "no" when asked whether `AVAZvHLR2PcWpDf8BXY4rVxNHYRBytycHkcB5z5QNXYm` is his (16 Jun 21:09:58, https://x.com/blknoiz06/status/2066991697842655572); so that address is not matched to him. On 16 June at 15:36:21 the same account wrote that an unnamed wallet was not its wallet; no address was given, and none is assigned.

### Unconfirmed leads (WEAK), not matches

| # | Subject | Why it is WEAK |
|---|---|---|
| W1 | 5Fcdrg (LUKE fee shareholder, 750,000,000 LUKE unmoved) | A pump.fun profile bio of the wallet, written by whoever controls the wallet's profile, names an X account; there is no X badge, and no post by that account naming the address was found (the search was incomplete). |
| W2 | ANSEM mint | ANSEM's creator-set metadata cites a third-party post of 21:04:39, 69 s before the creation; the post names no mint or wallet. |
| W3 | ANSEM mint | A community account in an aggregator's social field; it names no wallet. |
| W4 | a token named in a third-party post of 1 July, mint `Gpw8BDVDFrpCGgHmpPpdEQUsodypt2x7YfnGMQ9XVTw1` | Its creator is `Avo3RzF84vumgpSHt5Q8sCSJTSqy29UguEPKQAdV4KRJ`, not the deployer; that address shares no transaction with the wallets of this note in the periods covered, and its only tie to TJR and LUKE is that post. |
| W5 | ANSEM, TJR and LUKE | Third-party commentary of 30 June and 1 July; the 30 June claim is tested above. |
| W6 | the deployer as the ANSEM dev | A third-party post; it agrees with M3. |
| W7 | ANSEM mint | A third-party post that names a different account as the ANSEM deployer; it conflicts with M3 and with the CreateV2 signer. |
| W8 | 9fnyoj (TJR fee shareholder) | Third-party coins co-tag 9fnyoj with an X account; no post by that account naming 9fnyoj was found. |
| W9 | GV6U, 9fnyoj, the deployer, 5Fcdrg | Shared creator-fee shares on about 19 coins made by other creators, set by third parties; not a transfer between the wallets. |
| W10 | TJR mint | The website field of the TJR coin record names the coin's subject, not a wallet holder. |

**No identity found** for 9fnyoj, 7oU9, FkCcgv (pump.fun usernames only, no X link), the second-hop wallets, `F7p3dFrjRTbtRp8FRF6qHLomXbKRBzpvBLjtQcfcgmNe`, `GdWaMFZ2Ajp4q6h52jRAJAMXENUEUKbH47JRsjmS7DtD` and Avo3Rz. None of the three fee configs uses pump.fun's on-chain social-fee account type, so nothing on chain binds a shareholder to an X account; M1 rests on the pump.fun profile and the account's own post.

## The X Article's checkable claims, against the chain

The X Article on ANSEM was posted, by the page's own time, on 16 July 2026 at 18:01:07 (https://x.com/blknoiz06/status/2077815810458870267). It was read in full. It names no mint, wallet or transaction.

**Pairing.** The rows below pair the article's author with GV6U. That pairing rests only on M1 (DIRECT: the account's own post linking GV6U, and its pump.fun badge). The chain itself does not show whose address GV6U is; every row is a chain fact about GV6U, and its bearing on the author holds only as far as M1 holds.

| Claim in the article | What the chain shows |
|---|---|
| The author holds about 58 percent of the supply ("I have ~58% of total token supply") | GV6U held 584,284,604.165151 ANSEM on the article date, 58.428 percent of 1,000,000,000 (58.583 percent of the supply of 15 November; the supply on 16 July was not read). 7oU9 held none until 31 July. |
| The author took over a coin that had traded low for over a week | GV6U received 650,000,000 ANSEM from the creating signer 37 s after the creation; of the 654,000,000 it held by 17 June, 650,000,000 came from the creating signer and 4,000,000 from 4aArED. GV6U's ANSEM account then had no transaction for 10.4 days. The chain shows the holding arriving by transfer at launch, not by purchase after a week. GV6U's own post linking it to pump.fun was 6 min 22 s before the creation. |
| The launch was fair; no party got supply on preferential terms | An evaluation, not a chain quantity. The creating signer bought 79.245 percent of the supply in the creation transaction; it sent 650,000,000 ANSEM to GV6U with no SOL coming back in that transaction; it sold 142,454,486.758954 ANSEM within 50 s of the creation. Another signer completed and migrated the curve in the creation slot. |
| No high trading tax and no limiting bonding curve | True for the token: no transfer-fee extension; the curve is complete; the authorities are none. |
| Creator fees can go to individual wallets | True for this mint: 100 percent to GV6U since 16 Jun 21:07:55, admin revoked. |
| Large creator-fee income in the two weeks before the article | Stated in USD and across coins: not checkable on chain without a cited price source, and none is used here. ANSEM payouts to GV6U total at least 2,694.835774176 SOL to 14 November; the payouts of 2 to 16 July were not summed separately. |
| Airdrops and fee use are plans | Future intentions: not checkable. Two weeks after the article, 491,000,100 ANSEM (84.03 percent of GV6U's article-date holding) went to one wallet, 7oU9, which had sent none when read on 15 November. That is a move to a single recipient; it neither confirms nor rules out a later distribution. |
| A treasury of a stated USD size | No account labelled as a treasury can be identified on chain; the only large holdings found are GV6U and 7oU9. No USD value is computed here. |

**Prices.** No USD conversion is made in this note, and no figure is given in USD.

## Read on two providers, and on one

- **First reading.** Every transaction and signature list in this note was read on 15 November 2026 from api.mainnet-beta.solana.com, with getTransaction, getSignaturesForAddress, getBlock and getProgramAccounts at commitment finalized.
- **Second provider.** The second keyless provider used on 15 November, solana-rpc.publicnode.com, keeps no history this old: it returned null for every historical transaction asked of it. On 16 November 2026 the transactions listed in the result file were read again from public.rpc.solanavibestation.com. All 194 returned the values the result file lists, on both providers (16 November 2026, 02:59:36 to 03:03:17 UTC): the three creations; the ANSEM curve completion and migration; the three large transfers; the first transaction and the 20 April transfer from FkCcgv; the ten transfers of 16 June 21:01:38; the three fee-config creations; the three TJR buys of the creation slot, with their transaction indexes 1,434 to 1,436 (the creation is at 1,433); the two GV6U transactions around the article; the three GV6U-to-7oU9 transfers; the 9fnyoj-to-9mX7fG transfer; all 93 deployer sells; the deployer's TJR buy, the co-signed TJR transfer back to it and its five TJR transfers of 30 June 02:14:45; the 27 LUKE transfers; the 24 deployer-to-FkCcgv transfers; the three FkCcgv transfers of 30 June 13:55 to 13:58; the six 8 November transactions; and the two 9 November transactions. The 15 November transaction described above was read on both providers as well.
- **Current state** (balances, owners, the fee configs, the ANSEM mint, curve and pool, the top 20 holders' owners) was read on 15 November on api.mainnet-beta.solana.com and solana-rpc.publicnode.com, and all agreed.
- **On one provider only** (api.mainnet-beta.solana.com): the other history, including the 884 transactions behind the LUKE recipients' sells, the creator-fee payouts, the FkCcgv flows other than the transactions listed, the TJR creation block itself (the transaction index of each of its four listed transactions is in the second-provider check), the holder scan of slot 469,801,574 and the on-chain links in "Identity" other than the transactions listed.

## What this does not show

- **Who controls the addresses.** Co-signatures, funding links and shared slots are on-chain facts about keys and transactions. They do not show whether the deployer, the three shareholder wallets, the 27 recipients and FkCcgv are controlled by one party or by several.
- **Identity beyond the tiers.** M1 and M3 are DIRECT: each account publicly named or badge-linked its address. That does not prove sole control at every point in time. When the deployer's pump.fun badge was linked is unknown, and its pump.fun username changed on 17 August. The STRONG links (M5, M7 to M12) show a transfer or signature to a DIRECT address, not who holds the other side. The WEAK leads (W1 to W10) must not be presented as identities; that includes 5Fcdrg and 9fnyoj.
- **Intent.** Why any of these transactions were made. We draw no conclusion about intent, and this note makes no judgement about any account.
- **That GV6U was bought into.** The transactions read show no GV6U buy in the windows read; they do not cover every hour (see "The 30 June claim, tested").
- **The 9ryBR3 signer.** Whether the address that completed and migrated the ANSEM curve is linked to any address here was not tested.
- **FZEFKL's balance.** The 10,000.151415719 SOL FZEFKL holds is not shown to be these funds: 4,000 SOL came in from FkCcgv in the transactions read, and its other inflows were not read.
- **The deployer's other tokens.** The deployer has 23,797 signatures before the ANSEM creation alone and created three more mints on 8 November; an aggregator's token data credits it with 971 mints (third-party data). This note covers only ANSEM, TJR, LUKE, the transfers of other mints listed and the 8 November mints; it does not show these are its only tokens. Its transactions after 9 November were not read, apart from the 15 November transaction above, which it did not sign.
- **Service wallets.** Whether BY4StcU9 and BmFdpr are service wallets (BY4StcU9 used a durable nonce and held 1,996.263788767 SOL) was not tested. The same holds for `F7p3dFrjRTbtRp8FRF6qHLomXbKRBzpvBLjtQcfcgmNe` and 9SLPTL (417,591.430903745 SOL).
- **The FLASHX program.** What `FLASHX8DrLbgeR8FcfNV1F5krxYcYMUdBkrP1EPBtxB9` is, through which all 93 deployer sells and some FkCcgv transactions went.
- **The fee-vault split.** Whether the 0.494664926, 0.652213533 and 2.464723545 wrapped SOL collected before each config came only from that token.
- **The ANSEM payout total.** ANSEM payouts are a lower bound (446 transactions unread).
- **That the 13:54 transfers to FkCcgv are LUKE proceeds.** The deployer had inflows not attributed here.
- **Complete flows.** FkCcgv's history before 1 March, its flows beyond the second hop, and 1,008 of its 1,098 signatures in the window read; the deployer's 6,471 unread successful transactions between 20 April and 16 June.
- **The X Article's USD figures**, follower counts and other off-chain claims.
- **Burns and the mint lamports.** When the 2,646,095.523087 ANSEM were burned, and where the 26.198823646 SOL above the rent minimum on the mint account came from.
- **TJR and LUKE curves.** How and by whom they were completed and migrated.
- **Liquidity adds.** A 6 July statement by @blknoiz06 about adding SOL liquidity from creator fees was not tested on chain.
- **Commitments.** No commitment by @blknoiz06 to lock, burn or buy back ANSEM was found; the article gives "~58%" and no address.
- **The other ANSEM coin.** Who created mint 6r1BRG and whether HpKUzx is linked to any address here.

## Correction

No correction to this note so far. The list of corrections is in [CORRECTIONS.md](../CORRECTIONS.md).

## Evidence

The chain facts above were read on 15 November 2026 from api.mainnet-beta.solana.com and solana-rpc.publicnode.com, and on 16 November 2026 from api.mainnet-beta.solana.com and public.rpc.solanavibestation.com, with keyless JSON-RPC, read-only, at commitment finalized, plus HTTPS reads of the pump.fun IDLs at commit `639b87fb45c3adeffa6f7c4a1bf0cb85e392bf22`. The identity sources are public pages read without signing in (X posts, the pump.fun profiles, creator-set metadata files and a Wayback Machine copy). The raw replies and their SHA-256 hashes are kept.

The case result file is [ansem-tjr-luke-2026-06.json](ansem-tjr-luke-2026-06.json); its SHA-256 is `c98bcd425f6e2d7f66a177a0dbd4c18aadd8def2b54f9f5fbcd23dc2eada000b`. It holds the main facts as data: for every transaction the note relies on (the creations, the large transfers, all 93 sells, the 27 LUKE transfers, the 24 transfers to FkCcgv, the fee-config creations and the other transactions named above), its signature, slot, block time, transaction index, signers and the lamport and token changes, with the method, params and provider of the reading and the SHA-256 of the reply as saved; the decoded fee configs and the balances of 15 November with their slots; the second-provider result; the identity tiers with their sources; and the list of facts that rest on one provider.

A read-only script re-reads the main facts: [ansem-tjr-luke-2026-06-reread.py](ansem-tjr-luke-2026-06-reread.py) (`python3 ansem-tjr-luke-2026-06-reread.py`; standard library only, no keys; it needs the result file next to it). It asks two public providers, api.mainnet-beta.solana.com and public.rpc.solanavibestation.com, for every transaction in the result file and passes a transaction only when both return the values listed. It reads the values that can change (the three fee configs, the ANSEM mint, the ANSEM supply, five token balances, and the fee config and metadata of the other coin with the symbol ANSEM) from both providers, prints each next to its value of 15 November and marks it SAME or CHANGED: a later change shows as a change, not as a failure. It exits 0 only when every transaction passes on both providers and both providers agree on every current value.

| Main transactions | Transaction | Slot |
|---|---|---|
| ANSEM CreateV2 and creation buy (16 Jun 21:05:48) | `4LteGjWEqA5RZ3EAgQMsw2pgNNnWs7ceKFebkkDSaah6uyYT91Vp8NQLNaRe2rytnSaDHCjoaMeiBnN1SgWQYc2u` | 426,930,467 |
| 650,000,000 ANSEM to GV6U (21:06:25) | `5SGKQKgDfKYRv8XerDKWWEycXpz44JCdThmm4Rx6FzuaJujoGRhyYWf1dCVdakkHZPSeKTy3R9KgAR9TNfmEB3Db` | 426,930,558 |
| ANSEM fee config created (21:07:55) | `4ac9uBpNZZfraa5h2UPALPe5yPJKyrTnCpsabKDrS94e9691V5kH2dEWXoUFTx94mHD3GmRtTwwQtA9SsPdeaytV` | 426,930,784 |
| TJR CreateV2 and creation buy (29 Jun 13:08:45) | `2Yh4EdCEkaSZhJq73ZhvoqkJbKuU5jrkyGGXjgi9XgtRNvCJv7CvD6JUBz1idDRijEbXWCedyGA9WAbEeToXCwhC` | 429,670,768 |
| 790,000,000 TJR to 9fnyoj (30 Jun 02:14:24) | `26yjQeSMibS1JFDkDu6KfjzTomwTJiZogZSUHonXHPLqXGmgc3LPKemvzd2reM77EfpBay2UJ9vLGRh8LXF2apeE` | 429,787,322 |
| TJR fee config created (02:16:28) | `4SMGuvieEeeHAFx8HVcTiFLDdSafrEEX9DGkohR5k587Ye4PcoLfefgozgfqdWDwBGbTZDZQbdGZfH6nPbLWXubW` | 429,787,622 |
| LUKE CreateV2 and creation buy (30 Jun 06:18:29) | `3FdyiMxn88PMaqBv8DtVENzmcjP8my2SKs3V6JRJRHnNFmHwnPFAXzhnt19GvCoDjPhiD2BFaLdD3qe3PycfuH2p` | 429,823,473 |
| 750,000,000 LUKE to 5Fcdrg (13:30:45) | `1TASvAtpcTZ2Rp8GMiTH8PsPU3xRprPX89mTGRXJ7dbWquDpm7Brh3Ng2mbb4Gq86cmdHU3cnP2QYTvBk49XC3` | 429,887,676 |
| LUKE fee config created (13:34:50) | `5R61UtcfMZeCeL4BucxJBxBeiWj8GboBDHaiLBC6oDzQuxrxqEzHkxz7HeUWckJC8dtWn943m6urbaT7wq5FkbAU` | 429,888,279 |
| GV6U to 7oU9, 490,000,000 ANSEM (1 Aug 00:09:38) | `4mKqcX4taUZsv3v8aDmYEacW3HwQfjX7z96LxxUUMmRU47XKfZ23X8ps8pQJFUHCt9NAZfpG6mC6emHzH4NSrJC9` | 436,456,324 |
| The deployer's first transaction (20 Apr 13:00:49) | `4bv34kJFT2BnsvW7sbCRNPS59Y6Ggjj6REQdpQLZ1DYQh6Zw9AtXoWPoQVBZxQRemDoTt3QyuFSrXfxdAK5Nu7Z7` | 414,479,400 |
| 9.126416323 SOL from FkCcgv (13:02:25) | `3dsLwZLx7qLirUthoDoLvCdYh72DPQpY66UjSa3vikjwAtjc3XQ8DMuqkWVTfeXna2evpry2JiB1cYc8we78Cg77` | 414,479,640 |

| Addresses | Address |
|---|---|
| The deployer (CreateV2 signer of ANSEM, TJR and LUKE) | `yHCxHBEaJW5tbndqC8JciSThr7U1cqLpdcsvHcx6PRe` |
| GV6U, ANSEM fee shareholder | `GV6UUmNxz2RpKxmNAPadYKb7uQpszwqQAu3qLJxVdC52` |
| GV6U's ANSEM token account | `2U9XFtekYTstzMYXmuyDCNdFxRYB91dMtSKxtUB5rVct` |
| 9fnyoj, TJR fee shareholder | `9fnyojTv8GYHWr4Vaj4tvVL82scPPYYkW1CAXAbfUsdj` |
| 5Fcdrg, LUKE fee shareholder | `5FcdrgRp9jvRYcfJ5jENdH4XABLsPuD4KWMsAyHusQyy` |
| FkCcgv | `FkCcgvCoR6p6BRucCnU1t1DXP97Y3rJeMYBiU1o31nuv` |
| 7oU9 | `7oU9nR9VEvFPwvp2PpXo2LQc6A92QRhcUTwhLWT7MsDM` |
| 9mX7fG | `9mX7fG5Gsnc8E4sbsYurcNkha6TBwE7WZJ5EXqVG8CGb` |
| BY4StcU9, the first funder | `BY4StcU9Y2BpgH8quZzorg31EGE4L1rjomN8FNsCBEcx` |
| ANSEM fee config | `9ENSWnedBEAvVB7jJKZrLRZ9vuVuJdBE7uJt2oAsG1jr` |
| TJR fee config | `Hzzb5g5AcZMkmcDb9h4mFddEETeTosnjqR6KLCwLkvB5` |
| LUKE fee config | `5q9aPR9bpJMxJeBKN6Yss82Vt2iNycd5ZEHj5MWhUn6y` |
| ANSEM bonding curve | `FxC6pJJSiu6efSn8PmBMQjQaYm6dkSqmQYohui6NPnrf` |
| ANSEM pump AMM pool | `FnzKY6x7entQ1eR3D225dQyT7ybfka4PskBMQhb8L3CC` |
| pump.fun program; pump AMM; pump.fun fees program | `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P`; `pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA`; `pfeeUxB6jkeY1Hxd7CsFCAjcbHA9rWtchMGdZ6VojVZ` |

The hashes are given in full, without explorer links.

EXIT names an account next to an address only where the account itself named or badge-linked that address (DIRECT), or where a verifiable on-chain link joins the address to a DIRECT one (STRONG), as set out in "Identity". It attributes no other key or account to a person or organization.
