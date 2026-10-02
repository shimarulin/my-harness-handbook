# Governance Protocol

## Purpose

This document answers Open Questions Q2 and Q6 of the [requirements baseline v2.0](../ideal-tool-requirements.md):

- **Q2 (governance layer ownership):** governance is a **separate, disableable layer** realizing a **core-adjacent protocol** — the protocol (event schema + decision record format) is part of the core API because FR-2.5, FR-4.1, FR-4.6, and FR-8.4 depend on it as a stable contract; the *implementation* of governance (routing, escalation, policy application) is a pluggable layer per P6 ("individually disableable").
- **Q6 (rule inheritance without bootstrap cost):** rule representation uses **digest-form inheritance, resolution-at-assembly, and content-digest cache keys**, keeping subagent injection within the FR-3.3 bound without an always-loaded bootstrap.

Per NQ-C, this is **one versioned contract with two facets** — event schema and rule representation — with synchronous major versioning: a major change to either facet forces a major protocol version. The protocol lives in the core (its definitions are depended upon by normative FRs); its runtime behavior is layered.

## Design constraints honored

All mechanisms in this document respect the [NFR-derived constraints](./README.md#nfr-derived-design-constraints). Specifically: no daemon (event delivery is invocation-scoped), offline-capable (no network transport in the core protocol), and startup-cheap (digests, not eager parsing).

## Facet 1: Event schema

### Principle: build on existing baseline event points

The protocol does not invent a parallel event system. Its event sources are the points the baseline already normatively defines:

| Event point | Baseline anchor | Emitted when |
|---|---|---|
| Phase boundary | FR-3.5 (context-clearing guidance marks phase completion) | a phase completes |
| Interrupt | FR-3.6 (plan deviation, external tool error, assumption invalidation, scope expansion) | an interrupt trigger fires |
| Conflict detected | FR-2.5 (Classes A/B/C detection before merge/archive) | concurrent modification is detected |
| Decision moment | FR-4.1 (decisions in the routable categories) | a decision in a listed category arises |
| Review verdict | FR-3.4 / FR-8.4 (adversarial review; cycle verdicts; arbitration) | a review or arbitration concludes |
| Archive | FR-8.5 (auto-archive on merge) | a change is archived |
| Unknown resolved | FR-2.10 (resolution flow) | a marked unknown is resolved via the flow |

These anchors are normative FRs, so every conforming tool already produces the underlying conditions; the protocol standardizes their *observation surface*.

### Event record format

Events are stored as repo-native artifacts (FR-6.2) in an append-only event log under the governance directory:

```
events/
  YYYY-MM-DD/
    <seq>-<type>.md        # human-readable event record
```

Each record carries front-matter:

```yaml
type: conflict.detected | decision.required | review.verdict | ...
actor: <session-id | user>
ts: <ISO-8601>
refs:                       # traceability links (FR-4.6)
  requirement: spec://<repo>/requirements/<id>
  change: spec://<repo>/changes/<id>
  decision: spec://<repo>/decisions/<id>
payload:                    # type-specific structured data
  ...
```

**Delivery semantics (no-daemon constraint):** events are *written*, not *pushed*. Consumers (the governance layer, dashboards, CI checks) read the log at their own invocation points — CLI commands, hooks, CI steps, dashboard refresh. This satisfies NFR-5/NFR-2: no persistent listener, no network transport. Real-time notification (Slack/Teams routing per FR-4.1) is an optional overlay that reads the same log and may use network, cleanly kill-switchable per NFR-3.

### Event taxonomy (initial)

| Type | Emitted at | Consumed by |
|---|---|---|
| `phase.completed` | phase boundary | context-recovery (FR-4.5), cost reporting (FR-5.4) |
| `interrupt.raised` | FR-3.6 trigger | governance layer (routing), mission log |
| `conflict.detected` | FR-2.5 detection | governance layer (arbitration routing) |
| `decision.required` | FR-4.1 category | governance layer (stakeholder routing) |
| `decision.recorded` | FR-4.4 write | traceability, memory (FR-4.4/4.6) |
| `review.verdict` | FR-3.4/FR-8.4 | review-cycle narrowing, escalation state |
| `arbitration.pending` | FR-8.4 SLA expiry | observability (FR-4.2 escalation-pending) |
| `arbitration.resolved` | arbitration verdict | archive unblocking |
| `change.archived` | FR-8.5 | spec-tree merge, tracker sync (opt-in) |
| `unknown.resolved` | FR-2.10 flow | spec update, validation |

The taxonomy is open: layer implementations may subscribe to the closed set above and must ignore unknown types (forward compatibility).

### Subscription and gating

The governance layer subscribes declaratively (a repo-native config mapping event types to handlers). **Tool-gates are the universal backstop**: where a normative gate exists (FR-2.2 drift, FR-3.2 TDD, FR-8.4 cycle rules, FR-8.6 pre-upgrade), the *tool* enforces it on its own execution path regardless of whether a governance subscriber observed the event. This mirrors the Q3 resolution — enforcement moves from "the agent must comply" to "the tool will not pass" — and keeps governance *observation* disableable while *normative gates* remain core.

## Facet 2: Rule representation

### What a rule set is

Governance inheritance (FR-3.3) delivers six items into subagent context. Their representation:

| Item | Representation |
|---|---|
| Constitution/doctrine | **Digest**: enforcement-relevant clauses only (tool-compilable checklist), not the full philosophical text |
| Discipline enforcement settings | Structured data (profile, toggles) — ~tens of tokens |
| Scope boundaries + task definition | Task-scoped, already bounded |
| Interrupt-trigger configuration | Structured data |
| Coding/security standards | **Reference + content digest** (resolved at assembly) |
| Relevant spec deltas | Task-scoped |

### Mechanism: resolution-at-assembly with content-digest cache

1. **Storage.** Rules live as repo-native files (FR-6.2): constitution, standards, enforcement config.
2. **Compilation.** The constitution is *compiled* once per content version into an enforcement digest — the subset of clauses that gates verify (per Q6's "rule compilation" direction). Compilation is local, deterministic, offline.
3. **Assembly.** When a subagent context package is built (FR-3.3), references are resolved: standards are expanded from storage into the package, deduplicated across tasks.
4. **Caching (FR-5.5).** Cache keys are **content digests** of the rule inputs (constitution version, standards version, profile). This subsumes FR-5.5's invalidation requirement for configuration inputs: any rule change changes the digest, producing a cache miss and regeneration. Identical fragments across tasks hit the same cache entry.
5. **Bound.** Total injected context (digest + resolved references + task-scoped items) stays within the FR-3.3 cap: max(2,000 tokens, 15% of the effective budget), counted within the budget. The enforcement digest and structured settings are engineered to a per-task overhead target well below the cap; actual cost is itemized in cost reports (FR-5.4).

### Why not hash+diff (rejected alternative)

A content hash is unusable by a model, and a diff against a baseline the subagent never received is unreadable. Digest-form (compiled, enforcement-relevant text) is the correct representation; the content digest is used *only* as a cache key, never injected.

## Governance layer runtime (pluggable)

The layer above the protocol:

- **Router** — maps `decision.required` / `conflict.detected` / `arbitration.pending` events to accountable owners per FR-2.5/FR-4.1, including the ownership-declaration fallback chain (CODEOWNERS default, equivalent ownership file elsewhere) and the NQ-F per-repo acknowledgment semantics.
- **Policy engine** — applies the effective strictness profile (FR-1.4) to event handling; renders advisory vs. enforcing behavior.
- **Observability adapter** — projects event-log state into the local dashboard / CLI (FR-4.2), including the escalation-pending filter.

All three are disableable (P6); the protocol's event log and the core tool-gates remain. Disabling the layer degrades routing/observability, never normative gates — consistent with "governance *observation* is layered; *gates* are core."

## Open items deferred to other documents

- External bridging of this protocol to OpenSpec/Superpowers surfaces → [`composition.md`](./composition.md)
- Skill-trigger mechanisms consuming `phase.completed` / interrupt events → [`triggering.md`](./triggering.md)
- Subagent package assembly details, review-cycle state machine → [`execution-layers.md`](./execution-layers.md)
- `spec://` URI scheme, link classes, migration of event/rule formats → [`data-formats.md`](./data-formats.md)

## Status

- Answers Q2, Q6 (with NQ-B/C/I mechanisms)
- Honors NFR constraints 1–5 (README)
- Protocol version: 1.0.0 (both facets, synchronized)
- Next document: `composition.md`
