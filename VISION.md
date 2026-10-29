# From blockchain records to a connected research infrastructure

**North Star:** make blockchain activity understandable, investigable and
independently assessable through evidence.

![Conceptual system map; solid existing foundation, dashed planned extensions](research-system-map.svg)

## The foundation and the wider system

EXIT begins with control and change: who can act, on which object, under what
conditions, when, and on which evidence. This is a specialization within a broader
blockchain research product, not a permanent restriction to a handful of assets.

The intended wider system connects authority, events and observed fund relations
across explicitly validated network coverage. A guided interface serves individuals;
the same evidence foundation supports an API and permitted reports for organizations.

## Why history comes first

Current chain state can be read at any time; a record anchored on a past day
cannot be produced afterwards. Time-stamped history that cannot be back-filled is
therefore the asset EXIT builds first: control settings re-read on a schedule, a
record written when a setting changes, and a daily anchor even on days without
change. The daily anchor is live (tree size 204 on 29 October), the no-change
anchor is set and has not been needed yet, and scheduled re-reading comes next. In
two published case notes, control settings that the notes record were readable on
chain more than a year before the release or transfer, in places EXIT does not
read yet: a cross-chain verifier configuration and a DAO's governance rules.

## How the layers work together

1. **Evidence acquisition:** identify content, source, chain position and acquisition
   time; state missing history and source permissions.
2. **Temporal facts:** separate when a fact applied from when it could be known;
   preserve corrections and conflicting observations.
3. **Public evidence log, live:** EXIT's own records in an append-only Merkle log,
   anchored on Solana daily and checkable with a standalone verifier or, running
   code served by EXIT, in a browser. It bounds when EXIT held a record; it does
   not make the record true.
4. **Research graph, bounded live:** retain typed, source-backed edges rather than
   infer common ownership from a transfer or a shared funder. Today it joins up to
   four of an account's own answers; a temporal graph across subjects is planned.
5. **Question planner, planned:** produce a bounded plan with identity, time,
   coverage, required evidence and cost before executing a supported investigation.
6. **Monitoring, limited pilot and planned expansion:** an hourly radar pilot
   serves one watch service-wide. The expansion evaluates control-setting anomaly
   classes (a setting lowered, a deciding vote from a new wallet, a delegate
   changed) against labels to be committed to the log in advance; show false alarms,
   misses and operating latency.
7. **Delivery:** an understandable interface, a versioned API, an MCP wrapper,
   keyless history, cite and verify tools (live since 29 October) and
   permission-scoped reproducible reports (planned).
   Organization workspaces are a future extension.

## A mathematical boundary that changes the answer

```text
relation = (subject, predicate, object, valid_interval, known_interval, evidence)
answer(q, valid_cutoff, known_cutoff) = evaluate(eligible_evidence, versioned_rules)
held_by_EXIT(record) <= block_time(first anchor whose root contains it)
```

Synthetic example: an authority changes at 10:00; evidence becomes known at 13:00.
A query at a 12:00 knowledge cutoff must not use the 13:00 observation. A content
hash binds evaluated bytes, not the truth or completeness of every real-world claim.
A record's stated known time is EXIT's own statement; only the anchor's upper bound
is checkable by others.

## The strongest defensible destination

A continuously operated, multi-network research infrastructure with inspectable
plans, temporal relations, measured monitoring and machine-checkable permitted
outputs. Advanced formal reasoning or verifiable computation is considered only
where a bounded prototype improves a real task against the baseline. Later,
threshold-signed anchors and outside witnesses of roots would reduce reliance on
EXIT's own server.

This direction is ambitious. Claims about universal manipulation detection,
human identity, motives or market prediction are not justified by a graph alone.
Better evidence can support more precise questions; it cannot make missing evidence exist.

## What earns the next layer

Compare the same task bank before and after the change: supported-answer accuracy,
completion, unsupported conclusions, reproducibility, latency and cost. Keep the
method if the relevant benefit justifies the operational burden. Otherwise revise
or stop it. Later, labels and thresholds will be committed to the log before a run
(this needs a new log record kind), and corrections will be published as a public
error rate. See [the measurable roadmap](ROADMAP.md) and [current status](STATUS.md).
