# Governance Protocol

## Purpose

This document answers Open Questions Q2 and Q6 of the [requirements baseline v2.0](../ideal-tool-requirements.md):

- **Q2 (governance layer ownership):** governance is a **separate, disableable layer** realizing a **core-adjacent protocol**. The protocol — event schema, decision record format, session identity, identifier contract — is part of the core API; the *implementation* of governance (routing, escalation, policy application) is a pluggable layer per P6 ("individually disableable"). The protocol cannot be a pure plugin because normative acceptance criteria reference its constructs: FR-2.5 requires arbitration verdicts "recorded as a decision record per FR-4.4", and FR-4.6 requires links to decision records and the implementing session. The contract defining those constructs must therefore ship with the core, while runtime behaviors remain swappable.
- **Q6 (rule inheritance without bootstrap cost):** rule representation uses **digest-form inheritance, resolution-at-assembly, and content-digest cache keys**, keeping subagent injection within the FR-3.3 bound without an always-loaded bootstrap.

Per NQ-C, this is **one versioned contract with two facets** — event schema and rule representation — with synchronous major versioning: a major change to either facet forces a major protocol version.

This revision (1.1.0) applies the post-review decisions: the authority model (NQ-L: artifacts-as-primary, log as audit), log structure and compaction (NQ-P: per-mission logs, cross-mission stream, compaction on archive), the session identity contract (NQ-Q), a minimal `spec://` identifier contract, and the gate-vs-trigger separation.
Revision 1.1.1 applies the post-acceptance review notes: `spec://` addressability granularity, mission-id allocation deferral to `data-formats.md`, and a corrected signed-manifest wording (no v1 profile requires signatures).
Revision 1.1.2 refines two wordings from the composition review: `spec://` mission-record resolution semantics (the record exists from mission start as the live index), and the signed-manifest CP formulation (a new normative requirement extending FR-1.4 / touching NFR-3, not a modification of either).

## Design constraints honored

All mechanisms respect the [NFR-derived constraints](./README.md#nfr-derived-design-constraints): no daemon (event delivery is invocation-scoped), offline-capable (no network transport in the core protocol), and startup-cheap (digests, not eager parsing).

## Authority model (NQ-L)

**Artifacts are primary; the event log is an append-only audit trail.**

- **Source of truth:** the spec tree, decision records, and mission/change state — all repo-native artifacts (FR-6.2).
- The event log records **tool-observed activity**. It never defines artifact state, and consumers must never derive artifact state from it.
- Manual and out-of-tool edits (permitted by FR-1.2) change artifacts directly and emit no events; divergence is detected by **artifact comparison** — drift detection (FR-2.2) and spec-sync flags (FR-8.1) — not by log replay.
- Consequence for design: `data-formats.md` defines artifact formats as authoritative schemas; event records *reference* artifacts, never the reverse. Bidirectional synchronization was rejected: it creates a conflict class (log ↔ artifact) the baseline does not cover.

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

### Log structure and compaction (NQ-P)

Per-mission logs plus a cross-mission stream:

```
events/
  missions/<mission-id>/log.jsonl     # append-only within a mission
  global/log.jsonl                    # cross-mission events (protocol upgrades, ownership changes, kill-switch toggles)
```

**Compaction on `change.archived` (FR-8.5):** the mission log folds into the mission record stored with the archived change. **Retained:** verdicts, decision references, escalation records, session references. **Dropped:** per-cycle review detail — mirroring FR-8.4's own finding that "by the third pass the marginal signal is close to zero." Rejected changes compact the same way on rejection-archive, with the rejection reasoning retained as a decision record (FR-2.3).

This honors P2 in spirit: post-archive, per-event files serve no downstream consumer that the mission record would not; compaction keeps what does.

### Event record format

Events are stored as repo-native artifacts (FR-6.2):

```yaml
type: conflict.detected | decision.required | review.verdict | ...
session: spec://<repo>/sessions/<session-id>   # emitting session (see Session identity)
ts: <ISO-8601>
mission: spec://<repo>/missions/<mission-id>
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

### Subscription, gating, and the gate/trigger separation

The governance layer subscribes declaratively (a repo-native config mapping event types to handlers).

**Gates vs. triggers.** A *trigger* decides whether a skill is invoked (agent-context level, at or before execution). A *gate* decides whether a workflow step passes — merge, archive, phase advance (tool level). Both consume the same event stream; they act at different stages and must not be conflated:

- Gates are core and normative (FR-2.2, FR-3.2, FR-8.4, FR-8.6); triggering is the pluggable Q3 combo (→ [`triggering.md`](./triggering.md)).
- Gates verify **evidence** — the artifacts an acceptance criterion names — never skill invocations as such. A merge never passes because "the TDD skill ran"; it passes because test-first evidence exists (FR-3.2).
- A gate may *cause* a remedial skill invocation as a consequence of a blocked step. Such gate-forced invocations count toward FR-3.1's rate (they occur without an explicit user command) and are audited separately as remedial per NQ-H.

This separation is protocol-level so that `triggering.md` designs mechanisms without redefining gates, and gates cannot be made redundant by trigger design.

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
2. **Compilation.** The constitution is *compiled* once per content version into an enforcement digest — the subset of clauses that gates verify. Compilation is local, deterministic, offline.
3. **Assembly.** When a subagent context package is built (FR-3.3), references are resolved: standards are expanded from storage into the package, deduplicated across tasks.
4. **Caching (FR-5.5).** Cache keys are **content digests of the inputs** — rules and configuration, spec deltas, plan artifacts — which covers FR-5.5's invalidation requirement across all of its input classes; configuration is one class among them. Any input change changes the digest, producing a cache miss and regeneration; identical fragments across tasks hit the same cache entry.
5. **Bound.** Total injected context (digest + resolved references + task-scoped items) stays within the FR-3.3 cap: max(2,000 tokens, 15% of the effective budget), counted within the budget. Actual cost is itemized in cost reports (FR-5.4).

### Why not hash+diff (rejected alternative)

A content hash is unusable by a model, and a diff against a baseline the subagent never received is unreadable. Digest-form (compiled, enforcement-relevant text) is the correct representation; the content digest is used *only* as a cache key, never injected.

## Session identity contract (NQ-Q)

FR-4.6 requires traceability to "the implementing agent/session" — link resolvability, not cryptographic proof of authorship.

### session_id

- Opaque, unique, immutable, never reused (UUIDv7 or ULID).
- **Not derived** from (harness, branch, timestamp): branches rename and force-push (destabilized further by FR-5.3 worktree isolation), timestamps collide, and derivation provides no parent/child linkage (FR-3.3) and no defense against backdated records. Those fields are manifest *metadata*, not identity.

### Session manifest

A versioned repo-native artifact (FR-6.2) per session, at a stable sharded path keyed by session_id (exact tree in `data-formats.md`):

```json
{
  "session_id": "…",
  "parent_session_id": null,
  "continues_session_id": null,
  "kind": "main | subagent | human",
  "harness": "…",
  "agent": "…",
  "operator": null,
  "repo": "…", "branch": "…", "worktree": "…",
  "mission_id": "…", "task_id": "…",
  "started_at": "…", "ended_at": "…",
  "commit_shas": [],
  "config_digest": "…", "governance_digest": "…",
  "decision_ids": [], "review_ids": []
}
```

All mission/change/decision/review artifacts reference sessions by `session_id`; the CI validator resolves every reference to an existing manifest with consistent fields (a refinement of FR-4.6's "broken links fail CI", not a new criterion).

### Segmentation, lineage, and human attribution

- **A session is one continuous agent context.** A context clear (FR-3.5) ends a session; resumption starts a new one linked by `continues_session_id`, with `mission_id` stable across the mission. Context-window granularity is the correct attribution unit — it is what actually performed the work.
- **Subagents** carry `parent_session_id`, forming the FR-3.3 inheritance chain.
- **Humans:** interactive human tool sessions get `kind: human` manifests. Out-of-tool edits (FR-1.2) attribute through git committer identity; git history is authoritative for human edits, consistent with the authority model.

### Retention and compaction interaction

Session manifests are permanent identity records — never moved or deleted, or FR-4.6 links break. On compaction, mission records embed manifest *summaries* (session_id, kind, harness, agent/operator, key refs, digests); the files remain as link targets. Manifests are excluded from FR-7.4 ceremony artifact-count limits: they are audit infrastructure serving FR-4.6's traceability consumer (P2-justified), and their growth is bounded by being small structured records.

Privacy: no secrets, minimal PII (NFR-3); manifests are scanned like any artifact.

### Optional enhancement: signed manifests

Cryptographic signing (manifest signatures, signed commits with session trailers, attestation artifacts) would add tamper-evidence and non-repudiation for NFR-3 audit trails. It is **not part of the v1 contract**: it brings key management, revocation, offline constraints (NFR-2, FR-6.7), and install weight (NFR-5). No v1 profile requires signatures. `execution-layers.md` may specify the verification mechanism — where a signature would be checked, should the capability ever be enabled — but any mandate for signed manifests is a **new normative requirement**: where it attaches to profile semantics it extends FR-1.4, and where it affects audit integrity it touches NFR-3; either way it is an accumulated CP, with a second reviewer when NFR-3 is affected, per the change-proposal process.

## Identifier contract: `spec://` (minimal)

```
spec://<repo>/<class>/<id>
  classes: requirements | changes | decisions | missions | sessions
```

- `<repo>` is the configured repository identifier — the Q5 future-proofing (repo-identifier addressability); single-repo v1 resolves the local default.
- Resolution is local and offline (NFR-2), against the repository's artifact tree.
- **Addressability granularity:** individual event-log records are not `spec://`-addressable. `spec://…/missions/<id>` resolves to the mission record — created at mission start as the mission's live index, folded with event detail at compaction — which is thus the only `spec://`-addressable unit for mission-scoped activity. Physical resolution targets are defined in `data-formats.md`.
- Link classes (broken vs. unresolvable, NQ-E) and cross-repo resolution semantics are extended in `data-formats.md`, which owns the artifact tree.
- The scheme follows FR-8.6 migration classes once artifacts exist in the wild.

Defining the minimal contract here — rather than in `data-formats.md` — removes the circular dependency flagged in review: this document uses `spec://` in its record formats, so identifier semantics are protocol-level; `data-formats.md` extends, not defines, them.

## Protocol versioning

One semver for both facets; major versions synchronized (NQ-C). Protocol-produced artifacts (event records, manifests, digests) are subject to FR-8.6's migration classes once released; pre-release layout revisions require no migration. Current: **1.1.0** — added the authority model, log structure/compaction, session identity, identifier contract, and gate/trigger separation; storage layout revised prior to any release.

## Governance layer runtime (pluggable)

The layer above the protocol:

- **Router** — maps `decision.required` / `conflict.detected` / `arbitration.pending` events to accountable owners per FR-2.5/FR-4.1, including the ownership-declaration fallback chain (CODEOWNERS default, equivalent ownership file elsewhere) and the NQ-F per-repo acknowledgment semantics.
- **Policy engine** — applies the effective strictness profile (FR-1.4) to event handling; renders advisory vs. enforcing behavior.
- **Observability adapter** — projects event-log state into the local dashboard / CLI (FR-4.2), including the escalation-pending filter.

All three are disableable (P6); the protocol's event log and the core tool-gates remain. Disabling the layer degrades routing/observability, never normative gates — governance *observation* is layered; *gates* are core.

## Open items deferred to other documents

- External bridging of this protocol to OpenSpec/Superpowers surfaces → [`composition.md`](./composition.md)
- Skill-trigger mechanisms consuming `phase.completed` / interrupt events → [`triggering.md`](./triggering.md)
- Subagent package assembly details, review-cycle state machine, signed-manifest verification mechanism → [`execution-layers.md`](./execution-layers.md)
- Artifact tree unification (sessions/events paths), `spec://` extensions (link classes, cross-repo resolution, resolution mappings for adapter-declared non-core homes per [`composition.md`](./composition.md)), mission-id allocation semantics (repo-local ULID in v1; repo-qualified URIs provide global addressability), format migrations → [`data-formats.md`](./data-formats.md)

## Status

- Answers Q2, Q6 (with NQ-B/C/I mechanisms); records NQ-L, NQ-P, NQ-Q
- Review items 1–8 applied; post-acceptance notes 1–3 applied; composition-review refinements applied (mission-record resolution, signed-manifest CP formulation)
- Honors NFR constraints 1–5 (README)
- Protocol version: 1.1.2 (both facets, synchronized)
- Next document: [`triggering.md`](./triggering.md) (unblocked; terminology settled)
