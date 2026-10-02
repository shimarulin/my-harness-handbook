# Composition (External Contract)

## Purpose

This document supplies the external half of P6. Where [`governance-protocol.md`](./governance-protocol.md) defines the **internal** contract (events, rules, sessions — how the tool observes and constrains its own execution), this document defines the **external** contract: how the tool composes with existing tools — OpenSpec, Superpowers, and by template Spec Kit/specs.md, Spec Kitty — under one shell.

The research document's composition mapping ("OpenSpec as change-management layer, Superpowers as execution-discipline, Spec Kitty as orchestration/governance, Spec Kit/specs.md as strict-specification") states the *intent*. This document supplies the *mechanics*: where designated homes live, how custody passes between tools, how external activity projects into the protocol's event log.

FR-6.3 acceptance criteria this document must deliver:

- **Documented, tested combinations with at least OpenSpec and Superpowers** → two documented patterns below (testing arrives with the conformance corpus, known unknown #3)
- **One designated home per artifact type** → the ownership matrix
- **Lossless round-trip** → the bridge round-trip contract

**Two design caveats (approved):**

1. **Bridge schemas are templates, not version-pinned mappings.** They define what a bridge must *declare*, not concrete field mappings for current external versions. The research documented exactly why: superpowers-bridge declared compatibility baselines of OpenSpec 1.4.1 / Superpowers v5.1.0 while current releases were 1.13.2 / 6.4.1 — external tools drift faster than any document here can track. Pinning mappings would convert every external release into a CP.
2. **Known unknowns are registered explicitly** — what field data must verify at first implementation.

## Design constraints honored

Per the [NFR-derived constraints](./README.md#nfr-derived-design-constraints):

- **NFR-2 (offline):** bridges are local converters and observers; no bridge mechanism requires network. Networked overlays (tracker sync, chat routing) are unchanged by composition.
- **NFR-3 (kill switch):** no core composition mechanism depends on a networked component; bridges are kill-switch-neutral.
- **NFR-5 (no daemon):** event projection happens at invocation points (CLI, hooks, CI), consistent with the protocol's written-not-pushed delivery semantics.

## Composition model: three modes

Modes differ by **where the designated artifact home lives** — the FR-6.3 axis — and are selected **per artifact class, not per tool**. A single composition can adopt one tool's format for one class while bridging another tool for another class.

### Mode A — Adopt-as-layer

The external tool's format *is* our format for a class. Home = external format, read and written directly; no conversion at rest.

- **Use when:** the team's standard already lives in that format (e.g., an OpenSpec `changes/` tree) and our value-add is execution, governance, and audit on top.
- **Trade-offs (explicit):** deepest dependency — we inherit the external format's evolution. **FR-8.6 migration guarantees do not extend to adopted formats**: we can wrap, pre-check, and warn, but not migrate another tool's format. Likewise FR-2.8: either our validator's regression suite covers the adopted format's failure classes, or the bridge declares the external validator's pass as acceptable gate evidence.

### Mode B — Bridge-via-schema

We own the format; a bridge converts at the boundary. Home = our format.

- **Use when:** format control matters (FR-8.6 migrations, FR-2.8 validation as a normative gate) but interoperation is required.
- **Trade-offs:** the bridge tracks both sides; lossless round-trip (FR-6.3) is the bridge's contract, verified by a conformance corpus.

### Mode C — Coexistence

Both tools run with their own artifacts; coordination is by the ownership matrix and **read-only observation** of each other's repo-native artifacts (both being git-native per FR-6.2).

- **Use when:** teams keep existing tool workflows and adopt us for one layer only (e.g., governance/observability above an unchanged OpenSpec+Superpowers setup).
- **Trade-offs:** loosest coupling, weakest integration — no shared gates unless a bridge projects external artifacts as gate evidence.

## Artifact ownership matrix

Two tiers.

**Core-owned invariants (all modes, all patterns):**

| Artifact class | Why core |
|---|---|
| Decision records | FR-4.4 format; load-bearing for FR-2.5 arbitration, FR-2.10 resolution, FR-4.6 traceability |
| Review verdicts | FR-8.4 state-machine input (cycle narrowing, safety valve, arbitration trigger) |
| Session manifests | NQ-Q contract; FR-4.6 link targets |
| Event log | NQ-L audit trail |

These constitute the audit spine. Delegating them to external formats would place normative acceptance criteria at the mercy of external evolution. Adapters may **mirror** core-owned artifacts into external wikis and dashboards as read-only projections. *(This tiering is a v1 design decision — mechanism (b).)*

**Negotiable homes:** spec deltas, plans/design, task lists, execution evidence — the classes where the researched tools have established formats (OpenSpec `changes/<id>/` with `proposal.md`, `specs/`, `design.md`, `tasks.md`; Superpowers `docs/superpowers/specs/` and plans). One home per class per composition.

| Artifact class | Tier | Pattern 1 home | Pattern 2 home |
|---|---|---|---|
| Spec deltas | negotiable | OpenSpec `changes/<id>/specs/` — Mode A | Core change folder — Mode B (bridge imports Superpowers brainstorm output as proposal input) |
| Plans / design | negotiable | OpenSpec `design.md` or core | Core change folder — bridge redirects Superpowers `writing-plans` output here |
| Task lists | negotiable | OpenSpec `tasks.md` | Core `tasks.md`; Superpowers plan nests *underneath* the home list |
| Execution evidence | negotiable | Core | Core `verify.md` — bridge redirects Superpowers verification output |
| Decision records | **core** | Core | Core |
| Review verdicts | **core** | Core | Core |
| Session manifests | **core** | Core | Core |
| Event log | **core** | Core | Core |

`spec://` references to negotiable homes resolve through the bridge's ownership declaration (URI class → physical location mapping); resolution stays local and offline (NFR-2). Mapping format → `data-formats.md`.

## Documented patterns (FR-6.3)

### Pattern 1 — OpenSpec planning + core execution/governance

Layering per research: OpenSpec decides *what* (change management, delta specs, brownfield flow); core owns execution discipline, gates, governance, audit.

- **Modes:** Mode A for spec deltas and task lists (the OpenSpec `changes/` layout *is* the change-folder format); core-owned spine unchanged.
- **Archive:** FR-8.5 auto-archive drives the delta merge **into OpenSpec's canonical `openspec/specs/` tree** — in Mode A, "the canonical spec tree" of FR-8.5 is the adopted tree, written in its format via the bridge.
- **Gates:** core gates run on OpenSpec-format artifacts as evidence (drift referent = delta scenarios; the bridge's gate-evidence mapping declares this).

### Pattern 2 — Core planning/governance + Superpowers execution

Core owns spec deltas, plans, tasks; Superpowers supplies execution discipline (TDD, subagent-driven development, systematic debugging).

- **Modes:** Mode B bridge redirects Superpowers' brainstorm/plan/verify outputs into the core change folder — the superpowers-bridge precedent, which solved exactly the duplicate-artifact problems (see anti-patterns) by redirecting output into the change folder.
- **No double-gating:** Superpowers' own TDD enforcement ("Iron Law") is honored as *evidence* for our FR-3.2 gate; our gate remains the merge authority. The bridge declares its test-first output as acceptable evidence so discipline is verified once, not twice.
- **Harness coexistence:** Superpowers skills run in the harness alongside ours; interference behavior is known unknown #4.

Further patterns (Spec Kit strict-specification, specs.md AI-DLC flows, Spec Kitty orchestration) follow the same bridge template; they are not documented in v1 — FR-6.3's minimum is met, and field data from the first two patterns should inform the rest.

## Bridge schema template

What every bridge must declare — a conformance checklist, not a version-pinned mapping:

1. **Identity & versions** — participating tools, baseline versions, and a **drift-check hook wired to the pre-upgrade check** (FR-8.6). Precedent for the failure mode: superpowers-bridge's baselines drifting two major versions behind current releases.
2. **Ownership declaration** — per-class designated home, consistent with the matrix invariants; the `spec://` resolution mapping for every non-core home.
3. **Artifact mapping & round-trip contract** — per-class conversions; lossless round-trip verified by a conformance corpus (known unknown #3).
4. **Event projection** — external tools emit none of our events; bridges **derive** them from observed artifact changes, consistent with NQ-L (artifacts primary, log observes). Declared mapping: artifact diff → event type.
5. **Gate evidence mapping** — which external artifacts satisfy which core gates (e.g., Superpowers test-first output → FR-3.2 evidence; OpenSpec delta scenarios → FR-2.2 drift referent). Gates remain core and evidence-based; the bridge routes evidence, never redefines gates.
6. **Phase contract** — the ordered pipeline with custody handoff points (next section).
7. **Command surface map** — namespace and per-harness invocation grammar (next section).
8. **Collision policy** — install-time conflict report on namespace collision; loud failure, never silent override.

## Phase ordering and custody

Canonical pipeline (from the documented superpowers-bridge graph, generalized):

```
elicitation → proposal/spec delta → design/plan → tasks
            → execution (TDD, subagents) → verify → review → archive/retrospective
```

Rules:

- **Custody changes only at declared phase boundaries**, and each custody change emits an event — the tripwire against anti-pattern 4.
- **Write-permission rule:** no tool writes a home it does not own. Violations are detectable: a tool writing outside its home appears as an unowned-path artifact change.
- **Phase skipping is detectable, not merely forbidden:** a gate expecting evidence from a skipped phase fails on missing evidence; the custody-event tripwire adds observability. What happens on detection follows the effective strictness profile (FR-1.4) — advisory under vibe, blocking otherwise.

## Command surface separation

- Our commands: single namespace consistent with the tool name, full `--help`, unified deprecation policy (FR-6.6).
- **External commands keep their namespaces; bridges never alias, rename, or shadow them.** Each tool's command surface is its own contract.
- Per-harness invocation grammar variance is the bridge's declared concern — the research documents the same OpenSpec command spelled `/opsx:propose` (Claude Code), `/opsx-propose` (Cursor, Copilot), `@opsx-propose` (Amazon Q). Our own commands follow each harness's native grammar uniformly.
- **Collisions:** install-time conflict report; the bridge fails loudly rather than overriding.

## Anti-patterns

Carried from the [README](./README.md#anti-patterns-carried-from-research) and the research, each with its documented failure and mitigation:

1. **Duplicate design output.** Failure (research): "Superpowers brainstorming writes its design to `docs/superpowers/specs/`, while OpenSpec writes `proposal.md` and `design.md` in the change folder. Two documents now describe the same decision." One practitioner: "I ended up with two spec documents for one checkbox." Mitigation: ownership matrix — one home per class.
2. **Two task lists.** Failure (research): "OpenSpec's `tasks.md` is a coarse checklist; Superpowers' plan is a list of TDD micro-steps. They track the same work in different places, and they drift." Mitigation: one home; nested sub-artifacts allowed *underneath* the home (superpowers-bridge: "tasks.md gains a Superpowers plan.md underneath it").
3. **Manual orchestration ambiguity.** Failure (research): "Someone has to decide, at every step, which tool's skill runs next." Mitigation: the phase contract sequences declaratively in the bridge — not in the operator's head.
4. **Silent phase skipping / custody bypass.** Failure (research, superpowers-bridge README): "If you say 'let's brainstorm the architecture' in plain chat, Superpowers runs its default flow and writes to `docs/superpowers/specs/` again. The README treats that as the main failure mode." Mitigation: custody events as tripwire + write-permission rule + gates failing on missing phase evidence.

## Known unknowns (field verification required)

1. **External interface state.** Research baselines may already be stale (superpowers-bridge: OpenSpec 1.4.1 / Superpowers v5.1.0 vs. currents 1.13.2 / 6.4.1). Verify schema mechanisms, artifact layouts, and skill surfaces at implementation; the drift-check hook (bridge template #1) makes this continuous rather than one-shot.
2. **Event-projection fidelity.** Whether external tools expose phase-transition signals or only artifact changes. Worst case — the research suggests artifact changes only — bridges derive events from diffs: lower temporal fidelity, acceptable under NQ-L (artifacts primary).
3. **Round-trip fidelity.** Delta-format conversion (OpenSpec ADDED/MODIFIED/REMOVED blocks ↔ core format) needs a conformance corpus before Pattern 1 can claim FR-6.3's lossless AC — and before "documented" becomes "documented, tested."
4. **Harness coexistence.** Behavior of harnesses with two installed skill/command sets: auto-trigger cross-fire, doubled always-loaded metadata cost. Feeds `triggering.md`.
5. **Bridged-flow token overhead.** FR-5.4 cost reports must separate bridged from native flows; no baseline exists yet.

## Deferred

- Auto-trigger cross-fire between our skills and Superpowers skills under coexistence → [`triggering.md`](./triggering.md)
- Gate-evidence validators for external artifacts (well-formedness checks on bridged evidence) → [`execution-layers.md`](./execution-layers.md)
- `spec://` resolution-mapping format for non-core homes; mission-id allocation (repo-local ULID; repo-qualified URIs give global addressability); artifact tree unification → [`data-formats.md`](./data-formats.md)

## Status

- Delivers the external half of P6; FR-6.3's two documented patterns (OpenSpec, Superpowers)
- Template-level design per the approved caveats; known unknowns registered
- Version 1.0.0
- Next document: `triggering.md`
