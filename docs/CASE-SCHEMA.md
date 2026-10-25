# Public case-note schema (`exit.public-case-note/1`)

The research desk publishes authored case notes as JSON files. A note is a summary of selected evidence; it is not the
original engine response or a full raw-evidence export. The website verifies each file against the `file_sha256` listed in
`data.json` before showing it.

## Common fields

| Field | Meaning |
|---|---|
| `schema` | Always `exit.public-case-note/1`. |
| `id`, `chain`, `asset` | Case identity; must match the entry in `data.json`. |
| `source_commit` | Commit of the private research engine that produced the note; must equal `data.json.source_commit`. |
| `english` | `question`, `answer`, `limits` — the primary explanatory text. Translations live in `data.json`. |
| `actors` | Address/role rows shown on the desk. A role can carry `UNKNOWN` or a scope statement instead of an address. |
| `observations` | Selected evidence rows (see the two variants below). |
| `times` | Valid-time and known-time information (see below). |
| `source_links` | Explorer links for inspection; current explorer pages do not prove a historical snapshot. |
| `corrections` | Dated list of later corrections: `date`, `fields`, `reason`. Earlier values are never silently replaced. |
| `full_evidence_package_included` | Always `false`: notes are not full replay packages. |
| `recorded_not_live`, `publication_scope`, `raw_archive_permissions_changed`, `origin_response_identity` | Scope and provenance markers. |

## Observation variants

**Solana (relation rows).** `relation_id`, `subject`, `predicate`, `object`, `evidence_tier`, `source_content_hash` (SHA-256 of
the evidence set the relation was derived from), `valid_time` (`at_slot` and basis) and `known_time` (`known_from` and basis).
An optional `statement` explains an object value such as `key_addressed_account`.

**Ethereum (artifact rows).** `artifact` (the engine's read name), `content_hash` (SHA-256 of the frozen JSON-RPC response),
`acquired_at`, `observed_at_slot` and `observed_at_position` (the same block number; `position_unit` is `block`),
`rpc_method` and `evidence_class`. A header artifact such as `pyusd_header_26105285` holds the header of block 26,105,285
read while the state was observed at block 26,258,569. A supplemental row is labelled as such (for example
`supplemental_single_provider_chain_read`) and states that it lies outside the frozen engine response.

## Time fields

- Solana notes: `times.rows` lists, per relation, the `valid` slot and the `known` instant.
- Ethereum notes: `times.recorded_block` is the observation block; `times.event_window_blocks` is the declared event window the
  engine read; `times.window_chunks` lists every log chunk read with its block range and content hash; `times.event_times`
  lists decoded event instants when the note summarises them individually; `times.query` states the queried valid and known
  times.

Two clocks are always distinct: when something was true on the chain (valid time) and when EXIT's evidence became available
(known time). Later knowledge is never moved into the past.
