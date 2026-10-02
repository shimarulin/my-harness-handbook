# Architecture Documentation

## Purpose

This directory contains the architecture for the ideal tool specified in [ideal-tool-requirements.md](../ideal-tool-requirements.md) (frozen baseline v2.0) and the change-proposal mechanism defined in [change-proposal-process.md](../change-proposal-process.md).

The requirements phase is closed. This phase realizes those requirements without changing them; where a design decision selects among equally valid readings of baseline text, it is recorded per mechanism (b) of the change-proposal process (architecture document, no CP). Any change requiring normative force is an accumulated CP, not an edit here.

## Document map and dependencies

| Document | Scope | Depends on |
|---|---|---|
| [`governance-protocol.md`](./governance-protocol.md) | Q2 + Q6: the unified internal contract — event schema + rule representation | baseline event points (FR-3.5, FR-3.6, FR-4.x) |
| [`composition.md`](./composition.md) | P6 + FR-6.3: external contract — adapters and bridges, artifact ownership, surface separation with existing tools | governance-protocol (internal contract first) |
| [`triggering.md`](./triggering.md) | Q3 + NQ-A/K/H: trigger mechanisms, middleware plugin conditions, secondary metric | governance-protocol (event schema), composition (harness coexistence, KU #4) |
| [`execution-layers.md`](./execution-layers.md) | FR-3.x, FR-5.x, FR-8.x: subagent context assembly, review cycles, arbitration, cost reporting | governance-protocol (rule representation, session identity) |
| [`data-formats.md`](./data-formats.md) | Q5 + NQ-E/I: spec tree addressability, link classes, cache keys, migration formats | governance-protocol (decision record format; extends the `spec://` identifier contract defined there), composition (adapter ownership declarations) |

Build order: **governance-protocol → composition → triggering → execution-layers → data-formats**. The first is the largest open architectural surface and the input to the rest; each subsequent document consumes its outputs.

## Shared contract: what lives here vs. in layer documents

To avoid cross-reference churn between tightly coupled documents, the **shared contract** — the single versioned governance protocol with its two facets (event schema, rule representation) — is *defined once* in [`governance-protocol.md`](./governance-protocol.md) and *referenced* by all other documents. Layer documents do not restate it.

Two surfaces are kept distinct throughout:

- **Internal contract** (governance-protocol.md): events and rules *inside* the tool — how discipline enforcement, decision moments, and traceability observe and constrain execution.
- **External contract** (composition.md): how the tool bridges with existing tools (OpenSpec, Superpowers, Spec Kit/specs.md) — artifact ownership, command surface separation, schema mediation.

## NFR-derived design constraints

The following baseline NFRs are hard constraints on mechanism choice. Every layer document must state, for each mechanism it introduces, how it satisfies or respects these constraints. They are listed here once and referenced.

1. **NFR-5 — no daemon, no background service.** No mechanism may require a persistent listener. Event delivery must work through transient, invocation-scoped flows (CLI invocations, hooks, CI steps). Governance routing to Slack/Teams (FR-4.1) is an optional overlay, not a transport of the protocol itself.
2. **NFR-2 — offline mode.** The governance protocol, triggering, validation, and archive must operate with no network. Any event routing or skill triggering that uses network transport is an optional overlay that degrades cleanly (per the local/team dashboard split in FR-4.2 and the kill-switch precedence in NFR-3).
3. **NFR-1 — performance bounds.** Drift detection <30s per PR bounds its scope: it cannot be a full-repository scan; it must be scoped to the change's spec-clause pairs (FR-2.2). Spec generation <2 minutes (Standard) and dashboard render bounds (NFR-1) constrain orchestration bookkeeping to avoid serial LLM round-trips where artifacts can be derived locally.
4. **NFR-3 — kill-switch precedence.** No core mechanism may depend on a network component whose disablement breaks core behavior (formalizes NQ-A). The core trigger combo (hooks + minimal trigger list + tool-gate) must be network-independent; middleware, where permitted, is an off-by-default plugin subordinate to the kill switch, privacy-analyzed, with data-handling disclosure.
5. **NFR-5 — cold start.** CLI cold start <1s (`--version`) / <3s (`init`) constrains startup-time rule loading: governance inheritance must use digests and references resolved at assembly time, not eagerly parsed full texts.

## Anti-patterns carried from research

The composition and execution documents inherit these documented failure patterns as named constraints; they are restated here so no layer document reintroduces them:

- **Duplicate design output** — two artifacts describing the same decision (observed when Superpowers brainstorming and OpenSpec proposals coexist without a designated home)
- **Two task lists** — coarse checklist and TDD micro-step plan tracking the same work in different places, drifting apart
- **Manual orchestration ambiguity** — no designated owner deciding which tool's skill runs next

The corresponding positive constraint is FR-6.3's acceptance criterion: **one designated home per artifact type** in any combination.

## Status

- Baseline: v2.0, frozen 2026-10-02 — unchanged
- CP process: active; register complete; NQ-F confirmed (per-repo)
- Architecture phase: started 2026-10-02
  - [x] README (this document) — map, shared contract, constraints, anti-patterns
  - [x] governance-protocol.md — Q2 + Q6 unified contract (v1.1.2: review items 1–8, post-acceptance notes 1–3, and composition-review refinements applied; NQ-L/P/Q recorded)
  - [x] composition.md — external contract (v1.0.1: adapter/bridge terminology, ownership matrix, adapter template, documented patterns for OpenSpec and Superpowers)
  - [ ] triggering.md — Q3 mechanisms
  - [ ] execution-layers.md — FR-3/5/8 realization
  - [ ] data-formats.md — Q5 + formats + migrations
