# Composition (External Contract)

## Purpose

This document supplies the external half of P6. Where [`governance-protocol.md`](./governance-protocol.md) defines the **internal** contract (events, rules, sessions — how the tool observes and constrains its own execution), this document defines the **external** contract: how the tool composes with existing tools — OpenSpec, Superpowers, and by template Spec Kit/specs.md, Spec Kitty — under one shell.

The research document's composition mapping ("OpenSpec as change-management layer, Superpowers as execution-discipline, Spec Kitty as orchestration/governance, Spec Kit/specs.md as strict-specification") states the *intent*. This document supplies the *mechanics*: where designated homes live, how custody passes between tools, how external activity projects into the protocol's event log.

FR-6.3 acceptance criteria this document must deliver:

- **Documented, tested combinations with at least OpenSpec and Superpowers** → two documented patterns below (testing arrives with the conformance corpus, known unknown #3)
- **One designated home per artifact type** → the ownership matrix
- **Lossless round-trip** → the adapter round-trip contract

**Two design caveats** (approved in the pre-generation architecture review of 2026-10-02; recorded here for in-document provenance):

1. **Adapter mappings are templates, not version-pinned mappings.** They define what a composition must *declare*, not concrete field mappings for current external versions. The research documented exactly why: superpowers-bridge declared compatibility baselines of OpenSpec 1.4.1 / Superpowers v5.1.0 while current releases were 1.13.2 / 6.4.1 — external tools drift faster than any document here can track. Pinning mappings would convert every external release into a CP.
2. **Known unknowns are registered explicitly** — what field data must verify at first implementation.

## Terminology: adapter and bridge

- An **adapter** is the universal composition object: the declaration bundle that makes any combination workable — the eight items of the [adapter schema template](#adapter-schema-template). Adapters exist in **all three modes**.
- A **bridge** is a Mode-B adapter whose artifact mapping is a *converting* mapping (our format at rest, conversion at the boundary). In casual usage "bridge" covers all adapters; this document keeps the strict sense.
- **Adapter conversion profiles:** **identity** (Mode A — adopted homes, read and written natively; interpretation happens only at event-projection and gate-evidence boundaries), **converting** (Mode B), **observing** (Mode C — no home claimed; projection and evidence routing only).

**Baseline compatibility:** FR-6.3 ("Bridge/Combination Support") uses "bridge" as an umbrella for combination mechanisms and does not define it normatively; its acceptance criteria concern documented combinations, designated homes, and round-trip fidelity. Adapters are how that support is realized; Mode-B adapters are bridges in the strict sense. No CP arises from this vocabulary.

The external ecosystem's own names are preserved verbatim (e.g., OpenSpec's `superpowers-bridge` community schema) and are never renamed by our terminology.

## Design constraints honored

Per the [NFR-derived constraints](./README.md#nfr-derived-design-constraints):

- **NFR-2 (offline):** adapters are local converters and observers; no adapter mechanism requires network. Networked overlays (tracker sync, chat routing) are unchanged by composition.
- **NFR-3 (kill switch):** no core composition mechanism depends on a networked component; adapters are kill-switch-neutral.
- **NFR-5 (no daemon):** event projection happens at invocation points (CLI, hooks, CI), consistent with the protocol's written-not-pushed delivery semantics.

## Composition model: three modes

Modes differ by **where the designated artifact home lives** — the FR-6.3 axis — and are selected **per artifact class, not per tool**. A single composition can adopt one tool's format for one class while bridging another tool for another class.

### Mode A — Adopt-as-layer

The external tool's format *is* our format for a class. Home = external format, read and written directly; no conversion at rest. The home is **co-owned**: both tools write it (see the write-permission rule below).

- **Use when:** the team's standard already lives in that format (e.g., an OpenSpec `changes/` tree) and our value-add is execution, governance, and audit on top.
- **Trade-offs (explicit):** deepest dependency — we inherit the external format's evolution. **FR-8.6 migration guarantees do not extend to adopted formats**: we can wrap, pre-check, and warn, but not migrate another tool's format. Likewise FR-2.8: either our validator's regression suite covers the adopted format's failure classes, or the adapter declares the external validator's pass as acceptable gate evidence.

### Mode B — Bridge-via-schema

We own the format; a bridge (a converting adapter) converts at the boundary. Home = our format.

- **Use when:** format control matters (FR-8.6 migrations, FR-2.8 validation as a normative gate) but interoperation is required.
- **Trade-offs:** the bridge tracks both sides; lossless round-trip (FR-6.3) is the bridge's contract, verified by a conformance corpus.

### Mode C — Coexistence

Both tools run with their own artifacts; coordination is by the ownership matrix and **read-only observation** of each other's repo-native artifacts (both being git-native per FR-6.2). The adapter's profile is *observing*: event projection and evidence routing, no home claimed.

- **Use when:** teams keep existing tool workflows and adopt us for one layer only (e.g., governance/observability above an unchanged OpenSpec+Superpowers setup).
- **Trade-offs:** loosest coupling, weakest integration — no shared gates unless the adapter projects external artifacts as gate evidence. In Mode C the composition **claims no designated home for negotiable classes**; FR-6.3's one-home criterion applies per claimed class (the external tool's home is then the single home, and we produce no competing artifacts for it). Correspondingly there are no custody handoffs and no tripwire layer (see Phase ordering); phase-skipping detection is gate-based only, for claimed classes. This is the accepted trade of loosest coupling.

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

`spec://` references to negotiable homes resolve through the adapter's ownership declaration (URI class → physical location mapping); resolution stays local and offline (NFR-2). Mapping format → `data-formats.md`.

**Ownership flavors** (for the write-permission rule): core-owned (Mode B core homes), co-owned (Mode A adopted homes — both participants write), externally-owned (Mode C external homes — we never write, only observe).

## Documented patterns (FR-6.3)

### Pattern 1 — OpenSpec planning + core execution/governance

Layering per research: OpenSpec decides *what* (change management, delta specs, brownfield flow); core owns execution discipline, gates, governance, audit.

- **Modes:** Mode A for spec deltas and task lists (the OpenSpec `changes/` layout *is* the change-folder format); core-owned spine unchanged. The adapter's conversion profile is identity.
- **Archive:** FR-8.5 auto-archive drives the delta merge **into OpenSpec's canonical `openspec/specs/` tree** — in Mode A, "the canonical spec tree" of FR-8.5 is the adopted tree, written in its format through the adapter. Merge semantics follow the adopted format's own conventions (known unknown #6).
- **Gates:** core gates run on OpenSpec-format artifacts as evidence (drift referent = delta scenarios; declared in the adapter's gate-evidence mapping).
- **External writes are the normal operating mode, not an exception.** In Mode A the co-owned home is routinely written by OpenSpec outside our sessions. The NQ-L machinery is the *standing* reconciliation mechanism: external writes emit no events, and drift detection (FR-2.2) plus spec-sync flags (FR-8.1) reconcile at our invocation points.
- **Concurrent modification is FR-2.5 Class B territory.** When an in-flight change of ours and an OpenSpec-native change touch the same requirement, Class B arbitration applies: the accountable owner arbitrates both versions regardless of producing tool, and the losing version archives with rationale (FR-2.3). This *adds* protection the adopted tool natively lacks — the research documents OpenSpec's own edge case where archiving "silently dropped the other's scenario." One asymmetry is inherent to Mode A and accepted: arbitration *prevents* conflicts only when our archive runs; archives performed by the external tool itself are detected post-hoc via drift/sync, not prevented (known unknown #6).

### Pattern 2 — Core planning/governance + Superpowers execution

Core owns spec deltas, plans, tasks; Superpowers supplies execution discipline (TDD, subagent-driven development, systematic debugging).

- **Modes:** Mode B bridge redirects Superpowers' brainstorm/plan/verify outputs into the core change folder — the superpowers-bridge precedent, which solved exactly the duplicate-artifact problems (see anti-patterns) by redirecting output into the change folder.
- **No double-gating, with declared coverage:** Superpowers' own TDD enforcement ("Iron Law") is honored as *evidence* for our FR-3.2 gate; our gate remains the merge authority. The adapter declares **which failure classes the external enforcement covers** (test-first discipline: covered; our validator's parse-failure classes: not). Uncovered classes remain ours to gate — complementary coverage, not double-gating. A deliberately uncovered gap is an explicit, recorded configuration choice.
- **Harness coexistence:** Superpowers skills run in the harness alongside ours; interference behavior is known unknown #4.

Further patterns (Spec Kit strict-specification, specs.md AI-DLC flows, Spec Kitty orchestration) follow the same adapter template; they are not documented in v1 — FR-6.3's minimum is met, and field data from the first two patterns should inform the rest.

## Adapter schema template

What every adapter must declare — a conformance checklist, not a version-pinned mapping:

1. **Identity & versions** — participating tools, baseline versions, and a **drift-check hook wired to the pre-upgrade check** (FR-8.6). Precedent for the failure mode: superpowers-bridge's baselines drifting two major versions behind current releases.
2. **Ownership declaration** — per-class designated home with its ownership flavor (core-owned / co-owned / externally-owned), consistent with the matrix invariants; the `spec://` resolution mapping for every non-core home.
3. **Artifact mapping & round-trip contract** — per-class conversions according to the adapter's profile (identity / converting / observing); lossless round-trip verified by a conformance corpus maintained with the adapter (known unknown #3).
4. **Event projection — per-class transition signatures.** External tools emit none of our events; adapters derive them from observed artifact transitions. The adapter declares, **per artifact class**, which transition signatures map to which event types (e.g., creation of a verification artifact → `phase.completed` for the verify phase; a status transition in a task list → execution progress). Derivation is **signature-based, not diff-based**: edits matching no declared signature (a typo fix in a proposal) emit no events — they are artifact edits under NQ-L, caught by drift/sync where relevant. Signature *staleness* is covered by the drift-check hook (#1) and the conformance corpus (#3); signature *absence* is not — the drift-check compares against the adapter's own baseline, which is itself incomplete.

   **Disambiguation of missing events (phase skip vs. projection gap).** A missing phase event is ambiguous between a genuinely skipped phase and a transition no signature covers. Detection classifies at query time, composing the phase contract (#6) with the gate-evidence mapping (#5): **event present** → phase observed; **event absent, phase-output artifact present** → *projection gap*, recorded as a `projection.gap` event; **event absent, artifact absent** → *unconfirmed phase*, handled by gate evidence rules and the effective strictness profile (FR-1.4). `projection.gap` is emitted by the core detection pass (gates, tripwire checks, CI) — never eagerly per-diff — so typo-class edits stay silent while genuine gaps become observable. Residual edge, stated honestly: an artifact deleted after its phase leaves a gap indistinguishable from a skip; mitigated by evidence retention (FR-4.4) and by shrinking the gap class itself via known unknown #7. The projected-to vocabulary is **closed** (core-defined; see governance-protocol) — adapters map to existing event types only.
5. **Gate-evidence mapping** — which external artifacts satisfy which core gates, and **which failure classes the external enforcement covers** (uncovered classes remain core-gated). Gates remain core and evidence-based; the adapter routes evidence, never redefines gates.
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
- **Write-permission rule:** no tool writes a home whose declared ownership does not include it — core-owned homes are written by the core only; co-owned homes (Mode A) by both participants; externally-owned homes (Mode C) by the external tool only, with the adapter observing. Violations are detectable: a write outside declared ownership appears as an unowned-path artifact change.
- **Phase skipping is detectable, not merely forbidden:** a gate expecting evidence from a skipped phase fails on missing evidence; the custody-event tripwire adds observability. In Mode C the tripwire layer is absent (no handoffs) — detection is gate-based only, for claimed classes. What happens on detection follows the effective strictness profile (FR-1.4) — advisory under vibe, blocking otherwise.

## Command surface separation

- Our commands: a single namespace consistent with the tool name — the name is **deliberately a placeholder** in this documentation set (naming is a product decision, not an architectural one); every namespace, `--help`, and deprecation rule (FR-6.6) applies to whatever name is chosen.
- **External commands keep their namespaces; adapters never alias, rename, or shadow them.** Each tool's command surface is its own contract.
- Per-harness invocation grammar variance is the adapter's declared concern — the research documents the same OpenSpec command spelled `/opsx:propose` (Claude Code), `/opsx-propose` (Cursor, Copilot), `@opsx-propose` (Amazon Q). Our own commands follow each harness's native grammar uniformly.
- **Collisions:** install-time conflict report; the adapter fails loudly rather than overriding.

## Anti-patterns

Carried from the [README](./README.md#anti-patterns-carried-from-research) and the research, each with its documented failure and mitigation:

1. **Duplicate design output.** Failure (research): "Superpowers brainstorming writes its design to `docs/superpowers/specs/`, while OpenSpec writes `proposal.md` and `design.md` in the change folder. Two documents now describe the same decision." One practitioner: "I ended up with two spec documents for one checkbox." Mitigation: ownership matrix — one home per class.
2. **Two task lists.** Failure (research): "OpenSpec's `tasks.md` is a coarse checklist; Superpowers' plan is a list of TDD micro-steps. They track the same work in different places, and they drift." Mitigation: one home; nested sub-artifacts allowed *underneath* the home (superpowers-bridge: "tasks.md gains a Superpowers plan.md underneath it").
3. **Manual orchestration ambiguity.** Failure (research): "Someone has to decide, at every step, which tool's skill runs next." Mitigation: the phase contract sequences declaratively in the adapter — not in the operator's head.
4. **Silent phase skipping / custody bypass.** Failure (research, superpowers-bridge README): "If you say 'let's brainstorm the architecture' in plain chat, Superpowers runs its default flow and writes to `docs/superpowers/specs/` again. The README treats that as the main failure mode." Mitigation: custody events as tripwire + write-permission rule + gates failing on missing phase evidence.

## Known unknowns (field verification required)

1. **External interface state.** Research baselines may already be stale (superpowers-bridge: OpenSpec 1.4.1 / Superpowers v5.1.0 vs. currents 1.13.2 / 6.4.1). Verify schema mechanisms, artifact layouts, and skill surfaces at implementation; the drift-check hook (adapter template #1) makes this continuous rather than one-shot.
2. **Event-projection fidelity.** Whether external tools expose phase-transition signals or only artifact changes. Worst case — the research suggests artifact changes only — adapters derive events from declared transition signatures (template #4): lower temporal fidelity, acceptable under NQ-L (artifacts primary); precision preserved by signature-matching rather than raw diffs.
3. **Round-trip fidelity.** Delta-format conversion (OpenSpec ADDED/MODIFIED/REMOVED blocks ↔ core format) needs a conformance corpus before Pattern 1 can claim FR-6.3's lossless AC — and before "documented" becomes "documented, tested."
4. **Harness coexistence.** Behavior of harnesses with two installed skill/command sets: auto-trigger cross-fire, doubled always-loaded metadata cost. Feeds `triggering.md`; interference detection there inherits the consumer principle — absence of a projected event is not evidence of absence, and classification falls back to artifact state (trigger/invocation logs per FR-3.1).
5. **Bridged-flow token overhead.** FR-5.4 cost reports must separate bridged from native flows; no baseline exists yet.
6. **FR-8.5 archive semantics and concurrent writes against adopted spec-tree conventions (Mode A).** Two distinct questions: (a) delta merge into an adopted canonical tree must follow the adopted format's own merge conventions (ordering, tombstoning, cross-delta resolution) — known unknown #3 covers format *conversion*; this covers merge *semantics*; (b) co-owned homes are written by the external tool routinely, and FR-2.5 Class B arbitration must interoperate with the adopted tool's own conflict behavior (its documented whole-block replace can silently drop scenarios), including the enforcement asymmetry: arbitration prevents conflicts only on our archive; external-performed archives are detected post-hoc. Until verified, Pattern 1's archive step treats the adopted tree's merge rules as authoritative and pre-checks rather than assumes.
7. **Signature completeness (ground truth).** Declared transition signatures must be verified against the external tool's actual behavior — which legitimate transitions exist — not merely against the adapter's own baseline. Until verified, the disambiguation in adapter template #4 is the honest output: gaps are recorded as `projection.gap`, never silently absent. Verification results feed the conformance corpus (#3).

## Deferred

- Auto-trigger cross-fire between our skills and Superpowers skills under coexistence → [`triggering.md`](./triggering.md)
- Gate-evidence validators for external artifacts (well-formedness checks on bridged evidence) → [`execution-layers.md`](./execution-layers.md)
- `spec://` resolution-mapping format for non-core homes (consuming adapter ownership declarations); mission-id allocation (repo-local ULID; repo-qualified URIs give global addressability); artifact tree unification → [`data-formats.md`](./data-formats.md)

## Status

- Delivers the external half of P6; FR-6.3's two documented patterns (OpenSpec, Superpowers)
- **v1.0.1:** post-delivery review applied — adapter/bridge terminology split (Resolution A), Mode C home-claim and tripwire clarifications, co-owned homes with external-writer legality, signature-based per-class event projection, evidence-coverage declaration (Pattern 2), known unknown #6, tool-name placeholder, caveats provenance
- **v1.0.2:** second review round applied — missing-event disambiguation (phase skip vs. projection gap) with query-time classification and `projection.gap`; closed event vocabulary; KU #6 extended to concurrent writes with the enforcement asymmetry; KU #7 (signature completeness); consumer principle inherited by KU #4; Pattern 1 external-writes reframed as standing mode with Class B concurrent-modification semantics
- Template-level design per the approved caveats; known unknowns registered
- Next document: `triggering.md` (terminology and event semantics settled)
