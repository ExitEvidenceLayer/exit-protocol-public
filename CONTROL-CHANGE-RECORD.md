# Control-Change Record

Format `exit.control-change/1`, published 29 October 2026.

A Control-Change Record states one change of one control setting: which setting, on which account, from which value to which
value, when it took effect on chain, when EXIT learned it, and which evidence shows it. The format is open (see
[License](#license)) so that anyone can produce, check or reuse records in the same shape.

Status: the format, the setting names and a checker are published. EXIT does not publish records in this format yet. The
first planned source is the scheduled re-read of control settings in the [roadmap](ROADMAP.md); every record EXIT publishes
will also enter the [evidence log](https://exit-protocol.io/log/).

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
  the evidence, for example an event that carries the previous and the new admin. `known_at` cannot be earlier than the block
  time.
- **`bracketing_reads`**: a read at `old_read_position` showed the old value and a later read at `new_read_position` showed
  the new one, so the change took effect after the first position and no later than the second. Two reads show only the net
  change: a value that went A → B → A between them is invisible, and A → B → C appears as A → C. Both reads' evidence is
  required.

A first observation of a setting is a state, not a change, and is not written as a Control-Change Record.

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

As of 1 November 2026 the list holds 50 names, all read: the SPL Governance configuration reader and the LayerZero pathway
reader went live on 29 October, the LayerZero peer reader (`layerzero-v2:oapp.peers`) on 1 November. A LayerZero pathway read
exposes the subset that applies to its direction.

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
