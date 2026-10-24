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

## How the layers work together

1. **Evidence acquisition:** identify content, source, chain position and acquisition
   time; state missing history and source permissions.
2. **Temporal facts:** separate when a fact applied from when it could be known;
   preserve corrections and conflicting observations.
3. **Research graph, planned:** retain typed, source-backed edges rather than
   infer common ownership from a transfer or a shared funder.
4. **Question planner, planned:** produce a bounded plan with identity, time,
   coverage, required evidence and cost before executing a supported investigation.
5. **Monitoring, planned expansion:** evaluate specified anomaly classes against
   labelled references; show false alarms, misses and operating latency.
6. **Delivery:** an understandable interface, a versioned API and permission-scoped
   reproducible reports. Organization workspaces are a future extension.

## A mathematical boundary that changes the answer

```text
relation = (subject, predicate, object, valid_interval, known_interval, evidence)
answer(q, valid_cutoff, known_cutoff) = evaluate(eligible_evidence, versioned_rules)
```

Synthetic example: an authority changes at 10:00; evidence becomes known at 13:00.
A query at a 12:00 knowledge cutoff must not use the 13:00 observation. A content
hash binds evaluated bytes, not the truth or completeness of every real-world claim.

## The strongest defensible destination

A continuously operated, multi-network research infrastructure with inspectable
plans, temporal relations, measured monitoring and machine-checkable permitted
outputs. Advanced formal reasoning or verifiable computation is considered only
where a bounded prototype improves a real task against the baseline.

This direction is ambitious. Claims about universal manipulation detection,
human identity, motives or market prediction are not justified by a graph alone.
Better evidence can support more precise questions; it cannot make missing evidence exist.

## What earns the next layer

Compare the same task bank before and after the change: supported-answer accuracy,
completion, unsupported conclusions, reproducibility, latency and cost. Keep the
method if the relevant benefit justifies the operational burden. Otherwise revise
or stop it. See [the measurable roadmap](ROADMAP.md) and [current status](STATUS.md).
