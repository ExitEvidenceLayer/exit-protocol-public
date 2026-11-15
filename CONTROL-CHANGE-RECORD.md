# Control-Change Record

Format `exit.control-change/1`, published 29 October 2026.

A Control-Change Record states one change of one control setting: which setting, on which account, from which value to which
value, when it took effect on chain, when EXIT learned it, and which evidence shows it. The format is open (see
[License](#license)) so that anyone can produce, check or reuse records in the same shape.

Status (updated 15 November 2026): the format, the setting names and a checker are published. The Control Map daily
re-read, a standing job since 1 November 2026 (see the [roadmap](ROADMAP.md)), writes one record in this format for each change it
records between two reads of a setting and hands it to the [evidence log](https://exit-protocol.io/log/). On 14 November 2026 its
daily page (https://exit-protocol.io/control-map/daily/) showed 13 runs from 1 to 13 November 2026 and 0 changes recorded. Since
14 November 2026 the run can date an Ethereum change by its transaction
([How the Control Map daily run dates a change](#how-the-control-map-daily-run-dates-a-change)); every other change is written
with bracketing reads.

## One record, one change

```json
{
  "format": "exit.control-change/1",
  "chain": "solana-mainnet",
  "subject": "<the mint account>",
  "setting": "spl-token:mintAuthority",
  "scope": {},
  "old_value": "<the authority read before>",
  "new_value": null,
  "valid_at": {"basis": "bracketing_reads", "old_read_position": 300000000, "new_read_position": 300000450},
  "known_at": "2026-01-15T00:31:07.000000+00:00",
  "evidence": ["<SHA-256 of the first read's raw response>", "<SHA-256 of the second read's raw response>"],
  "reader": {"name": "exit.solana-mint-research/2", "implementation_sha256": "<SHA-256 of the reader's source>"}
}
```

| Field | Meaning |
|---|---|
| `format` | Always `exit.control-change/1`. |
| `chain` | `solana-mainnet` or `ethereum-mainnet`. |
| `subject` | The account the setting belongs to: a Solana address, or an Ethereum address in lowercase hex. This is the account that stores it, except for the `layerzero-v2:endpoint.*` and `uln.*` names: their subject is the OApp, and the contract that stores the value (endpoint or message library) is named in `scope`. |
| `setting` | A name from the [setting list](control-change/control-change-settings.json). |
| `scope` | The qualifiers the setting needs, exactly as the list declares them (for example a remote endpoint id); `{}` when none. |
| `old_value`, `new_value` | Both observed, in the value type the list declares, and different. `null` means "no key set" only where the type allows it. |
| `valid_at` | When the change took effect on chain (below). |
| `known_at` | The UTC time EXIT acquired the evidence that shows the new value. This is EXIT's own statement. |
| `evidence` | The sorted, distinct SHA-256 digests of the exact evidence bytes, such as raw RPC responses. |
| `reader` | The schema id of the reader that interpreted those bytes and the SHA-256 of its source. |

There is no free text in a record. What a setting means, and what it does not mean, is in the setting list.

## When a change took effect

A record uses one of two bases, and they prove different things:

- **`transaction`**: the transaction that made the change, with its slot or block and block time. Both values must come from
  the evidence, for example an event that carries the previous and the new admin (for an event that names only the new value,
  see [How the Control Map daily run dates a change](#how-the-control-map-daily-run-dates-a-change)). `known_at` cannot be
  earlier than the block time.
- **`bracketing_reads`**: a read at `old_read_position` showed the old value and a later read at `new_read_position` showed
  the new one, so the change took effect after the first position and no later than the second. Two reads show only the net
  change: a value that went A → B → A between them is invisible, and A → B → C appears as A → C. Both reads' evidence is
  required.

A first observation of a setting is a state, not a change, and is not written as a Control-Change Record.

## How the Control Map daily run dates a change

Since 14 November 2026, 03:01 UTC, the Control Map daily re-read (23:20 UTC each night) can write an Ethereum change with the
`transaction` basis. The run of 14 November 2026 is the earliest run in this mode. This section states what the run checks
before it does so. The run's source code is not in this repository, so the section is EXIT's statement; a dated record can
be checked against the chain and the evidence log ([below](#checking-a-dated-record)).

The run of 14 November 2026 recorded no change, so it dated none.

A change found between two reads is first built as a `bracketing_reads` record. The run writes it with the `transaction` basis
instead only when every condition below holds; otherwise it writes the bracketing record, as before. One change still gives
one record.

1. **Ethereum only.** The record's chain is `ethereum-mainnet`. A Solana change keeps `bracketing_reads`.
2. **A setting with a mapped event.** The setting is one of the nine in the table below.
3. **Two keyless public sources agree.** Two public Ethereum RPC endpoints, used without a key (eth.drpc.org and
   eth.api.pocket.network), are asked for the subject contract's control events over the bracket window: the blocks after
   `old_read_position`, up to and including `new_read_position`. Both must answer, their decoded events must be equal, and they
   must give the same block hash and block time for each event block and for the last block of the window. A refusal, a missing
   answer, a call, time or size limit, or any difference keeps the bracketing record.
4. **The window ends at the block of the later read.** The last block of the window must be the finalized block at which the
   later read was taken, by number (`new_read_position`) and by hash (the block hash recorded with that read).
5. **Exactly one event, and it names the new value.** The window holds exactly one event of the setting's type in the table
   below, and that event names the record's `new_value`. For `AdminChanged` and `OwnershipTransferred`, which also name the
   previous value, that value must equal `old_value` as well. No such event, or a second event of that type in the window, keeps
   the bracketing record.
6. **A well-formed event.** The event's transaction hash, its block (inside the window) and its block time are well formed,
   every evidence item it cites has a SHA-256 digest, and `known_at` is not earlier than the block time.

The record then has `"valid_at": {"basis": "transaction", "transaction": ..., "position": ..., "block_time": ...}` with the
event's transaction hash, block number and block time, and its `evidence` adds the digests of the two sources' log and
block-header replies for that event to those of the two reads. `old_value` and `new_value` are still the values of the two reads.

| Setting | Event | Must equal `new_value` | Must equal `old_value` |
|---|---|---|---|
| `evm:eip1967.implementation`, `evm:zos.implementation` | `Upgraded(address)` | its address | (no such field: the old value is that of the earlier read) |
| `evm:eip1967.admin`, `evm:zos.admin` | `AdminChanged(address,address)` | the second address (new admin) | the first address (previous admin) |
| `evm:eip1967.beacon` | `BeaconUpgraded(address)` | its address | (no such field) |
| `evm:owner()` | `OwnershipTransferred(address,address)` | the second address (new owner) | the first address (previous owner) |
| `circle-fiattoken:masterMinter()` | `MasterMinterChanged(address)` | its address | (no such field) |
| `circle-fiattoken:pauser()` | `PauserChanged(address)` | its address | (no such field) |
| `circle-fiattoken:blacklister()` | `BlacklisterChanged(address)` | its address | (no such field) |

`circle-fiattoken:rescuer()` and every setting not in the table have no mapped event, so their changes keep `bracketing_reads`.
At most two changed deployments per night are given an event window. A deployment whose changed settings include both a proxy
or `owner()` setting and a FiatToken role from the table is given none. A change of a deployment without a window keeps the
bracketing record.

The [daily page](https://exit-protocol.io/control-map/daily/) shows a dated change with ", changed in transaction", the first 6
and last 4 characters of the transaction hash, the block number and the block time in UTC after its values. Its section "What
this page does not show" then says: "A change shown with a transaction is dated by it: for the blocks between the two reads,
two public sources each returned exactly one event of the kind that records that setting, and that event names the new value."
For every other change it says that the time is known only to lie between the two read positions. When no shown change is
dated, the page's words on the time of a change are those used before 14 November 2026.

### Checking a dated record

A dated record does not carry the two read positions: its `valid_at` holds only the transaction, its block and its block time.
The two reads are in the [evidence log](https://exit-protocol.io/log/). Each night the run hands one record per deployment to the
log's notary inbox. For each of the two Ethereum reads behind a change, that record has `kind` `research_observation`, the
deployment's address as `subject`, the read's finalized block as `observed_at`, the read's `known_at`, and the SHA-256 digests of
the read's replies as `evidence`. A dated record has the `known_at` of the later read, and its `evidence` holds the digests of both reads. Each proof
bundle of the log contains its record, and https://exit-protocol.io/log/proofs.json lists the published bundles; for example,
the 72 records of the 13 November 2026 run are listed at tree size 1303.

1. Take the record file from its link on the daily page (daily.json lists its SHA-256) and check it as in
   [Checking a record](#checking-a-record).
2. Read the receipt of `valid_at.transaction` from an Ethereum node or a block explorer of your choice. Its block must be
   `valid_at.position`, and its logs must hold the event of the table, emitted by `subject`, naming `new_value`. The block's
   timestamp must equal `valid_at.block_time`.
3. In the published proof bundles, take the records with the dated record's `chain` and `subject` whose `evidence` digests all
   appear in the dated record's `evidence`. Among those with the dated record's `known_at`, the largest `observed_at` is the
   later read's block (the dated record's own log record is one of them, with `observed_at` equal to `valid_at.position`). The
   one with the latest earlier `known_at` is the earlier read, and its `observed_at` is the earlier read's block.
4. A log query for that event from `subject` over the blocks after the earlier read's block, up to and including the later
   read's block, must return that one event.

The read records do not say which change they belong to: step 3 matches them by digests and times. That match is the reader's
check, not a field of the dated record.

### What a transaction date does not show

- That the two sources are independent. They are two endpoint names; both may relay the same upstream provider, and their
  agreement is then one witness, not two.
- That the event block belongs to the same chain as the read block through its parent hashes. Only the last block of the window
  is tied by hash to the block of the later read; for an event block, the run checks only that both sources gave the same header
  hash and that it equals the event's block hash.
- What the transaction itself contains. The run does not fetch the transaction or its receipt; the date rests on the events and
  block headers that the two sources returned.
- The old value, for `Upgraded`, `BeaconUpgraded` and the three FiatToken role events: these events name only the new value, and
  the old value comes from the earlier read.
- Every change. A setting that changed and changed back between the two reads gives no change and no record, and a change made
  by more than one event of its type keeps the bracketing record.
- That an undated change had no transaction. A Solana change, a setting without a mapped event, a refusal, limit or disagreement
  of the sources, and a change of a deployment beyond the two per night that get a window all keep the bracketing record.
- Who sent the transaction, who holds or controls any address or key, why the setting was changed, or whether the change was
  safe or harmful.
- A later review. The date is written and shown in the run's own night, before any later check. The evidence log does not remove
  records, so a wrong date would stay in the log, and its correction would be listed in [CORRECTIONS.md](CORRECTIONS.md).

## Setting names

A setting name is `<namespace>:<path>`: the namespace is the program family and the path is the field as the program or EXIT's
reader names it, for example `spl-token:mintAuthority`, `token-2022:permanentDelegate.delegate`,
`spl-governance:governance.config.community_vote_threshold`, `evm:eip1967.admin` or
`layerzero-v2:uln.getUlnConfig.requiredDVNs`. The [setting list](control-change/control-change-settings.json) gives, for each
name, where the value is stored, its scope, its value type, the source it is read from, what it means and what it does not mean.
The meanings were checked against the programs' published source code before publication, and the checker's ranges against
the readers' own decoders in a second review.

- A name is never renamed or reused. If the meaning of a setting changes, it gets a new name; the old one stays in the list.
- `read`: an EXIT reader reads this value today, so a change can be recorded from two reads.
- `reserved`: the name is fixed for a value no reader reads yet. A reserved name may be corrected only before its first record.

As of 4 November 2026 the list holds 56 names, all read: the SPL Governance configuration reader and the LayerZero pathway
reader went live on 29 October, the LayerZero peer reader (`layerzero-v2:oapp.peers`) on 1 November. A LayerZero pathway read
exposes the subset that applies to its direction. Added on 4 November: the ZeppelinOS proxy slots (`evm:zos.implementation`,
`evm:zos.admin`), which the Ethereum contract reader reads beside the EIP-1967 slots, and the four roles of Circle's FiatToken
(`circle-fiattoken:masterMinter()`, `circle-fiattoken:pauser()`, `circle-fiattoken:blacklister()`, `circle-fiattoken:rescuer()`),
which the reader reads only when a token's proxy and implementation code equal the reviewed Circle FiatToken pair.

## Value types

| Type | Written as |
|---|---|
| `solana_address_or_null` | A Solana base58 address of 32 bytes, or `null` when no key is set. For the Token-2022 extension authorities, which the program stores as a non-zero optional key, the all-zero key means no key and is written as `null`. |
| `evm_address` | `0x` and 40 lowercase hex digits. The zero address is a value (for a proxy slot: the slot is empty), not an absence. |
| `evm_address_list` | Sorted `evm_address` values without duplicates. |
| `uint` | A JSON integer from 0 to 9007199254740991, narrowed by a setting's own constraints where the list states them. |
| `u64_string` | A decimal string without leading zeros, up to 18446744073709551615. |
| `bytes32` | `0x` and 64 lowercase hex digits. |
| `bool` | `true` or `false`. |
| `enum` | One of the strings the setting lists. |
| `vote_threshold` | `{"kind": "YesVotePercentage", "QuorumPercentage" or "Disabled", "percentage": 1 to 100, or null exactly when the kind is Disabled}`. |

A setting may narrow `uint` values with `minimum`, `maximum` and `excluded`, and scope values with `scope_constraints`, to
the ranges the programs accept: endpoint ids are 1 to 4294967295; an OApp's stored required-verifier count is 0 to 127 or
the 255 sentinel; an effective optional threshold is 0 to 127; governance time fields fit 32 bits and the required-signatory
count 8 bits. A value outside these ranges is refused even when its JSON shape is right.

## How a record enters the evidence log

A record file holds the record's canonical JSON bytes: sorted keys, the separators `,` and `:` with no spaces, UTF-8 and no
trailing newline. The record enters the log as an ordinary log record ([SPEC.txt](https://exit-protocol.io/log/SPEC.txt),
version 1), so no new log format is needed:

| Log field | Value |
|---|---|
| `kind` | `research_observation` |
| `chain`, `subject`, `known_at`, `evidence` | Copied from the record. |
| `observed_at` | `valid_at.position` for a transaction; `valid_at.new_read_position` for bracketing reads. |
| `result_sha256` | The SHA-256 of the record file. |

Once the log root that contains it is anchored, the anchor's block time is an upper bound on when EXIT held the record. It
does not show that the change happened as stated; the evidence at its own slot or block does.

## Checking a record

[`control-change/ccr.py`](control-change/ccr.py) uses the Python standard library only.

```bash
python3 control-change/ccr.py check record.json
python3 control-change/ccr.py log-record record.json
```

`check` applies every rule above that can be checked from the record itself: fields, addresses, setting name and scope, value
types, a real difference between the values, the timing basis, `known_at` against the block time, the evidence digests and the
canonical bytes. `log-record` prints the log record. To check that a published record is in the log, give the
[log verifier](tools/exit_log_verify.py) the record's proof bundle and the record file:

```bash
python3 tools/exit_log_verify.py leaf proof-bundle.json --log https://exit-protocol.io/log/ --answer record.json
```

The three `example-*.json` files next to the checker are synthetic: their addresses, transactions and digests are made up.

## What a record does not say

A record states that a stored setting changed, according to the named evidence. It does not say why the setting was changed,
who holds any key, whether the change was safe or harmful, whether a loss could have been prevented, or that no other setting
changed. Reading the evidence again at its own slot or block is the way to check the values; the record's `known_at` is EXIT's
statement, bounded from above by the log anchor.

## License

The record format, the setting list and the checker are licensed under the [MIT License](LICENSE-CODE). This page is
documentation under [CC BY-ND 4.0](LICENSE).
