# Execution Layers

## Purpose

This document realizes the execution-facing requirements of the [baseline v2.0](../ideal-tool-requirements.md) — FR-3.x, FR-5.x, FR-8.x — and resolves the open inputs registered by the earlier documents: the **gate-to-skill dispatch mechanism** (triggering KU #6), the **atomic event emission** condition (governance-protocol v1.2.1), the **signed-manifest verification mechanism** (deferred there), and the **reference corpus** (deferred from triggering.md).

It composes the contracts already settled: session identity and rule representation (governance-protocol), the trigger/compliance split (triggering), event semantics with the consumer principle by emitter class (governance-protocol v1.2.1).

## Design constraints honored

- **NFR-5 (no daemon):** gates, arbitration timers, and escalation are invocation-scoped — evaluated at CLI/hook/CI entry points and by deadline arithmetic, never by background processes.
- **NFR-2 / FR-6.7 (offline):** every mechanism here is local; SLA re-notification may use network overlays, kill-switchable per NFR-3.
- **NFR-1 (performance):** drift detection is scoped to the change's spec-clause pairs (FR-2.2), never a repository scan; review-cycle prompts are narrowed per FR-8.4.
- **Consumer principle:** core event emission is atomic with the actions this document defines (below), so silence is a tripwire about them.

## Layer 1: Subagent context assembly (FR-3.3, FR-3.5)

### Assembly pipeline

For each task, package assembly runs **in tool code, never in agent context**:

1. **Collect** the task definition, affected spec deltas, module interface contracts (FR-3.3 minimal context package).
2. **Resolve governance** — rule representation per governance-protocol Facet 2: enforcement digest, structured settings, interrupt config, standards by reference with content digest.
3. **Inherit session identity** — the parent session creates a child manifest (`parent_session_id` chain, FR-3.3 inheritance).
4. **Assemble** the bounded package: total injected context within the FR-3.3 cap — the greater of 2,000 tokens or 15% of the effective budget — counted within, not in addition to, that budget.
5. **Report** the itemized injection cost (FR-5.4).

**Verification of inheritance (FR-3.3 AC):** the manifest records `governance_digest`; a subagent's first action is a tool-verified check that its working config matches the parent's declared profile — the verifiable-presence mechanism for "subagent prompts verifiably contain the constitution and effective enforcement settings." A mismatch blocks the subagent before any work (this is a gate, not a prompt instruction — evidence, not compliance prose).

### Context-clearing guidance (FR-3.5)

At each phase completion, the tool emits guidance naming the minimal state to preserve (mission pointer, active deltas, session manifest id) and whether clearing is safe. The `phase.completed` event is emitted **atomically with the phase artifact commit** — satisfying the governance-protocol v1.2.1 condition that core-event silence be a tripwire: a committed phase artifact without its event is an anomaly the detection pass flags.

## Layer 2: Review-cycle state machine (FR-8.4)

### States

```
implement → review(cycle-1: full contract)
   ├─ accept → next stage
   ├─ reject → rework → review(cycle-2: feedback + delta since prior)
   │             ├─ accept → next stage
   │             ├─ reject → rework → review(cycle-3: feedback items only)
   │             │             ├─ accept → next stage
   │             │             └─ reject/unchanged → arbitration
   │             └─ safety valve (new critical defect) → review(full contract, one cycle) → re-narrow
   └─ ...
```

- **Narrowing is prompt-scoped:** cycle 2+ review prompts contain only the delta, prior feedback, unresolved items; settled items listed as treated-as-settled (FR-8.4 AC).
- **Safety valve:** a new critical defect outside narrowed scope resets coverage for one cycle (logged).
- **Non-convergence → arbitration:** routed per FR-2.5 Class B, including the fallback chain (accountable owner → ownership declaration → blocking configuration error).
- **Arbitration SLA (default 72h):** SLA expiry is **deadline arithmetic at invocation points** — every CLI/CI entry computes pending deadlines from `arbitration.pending` timestamps; expiry flips mission state to escalation-pending, surfaced in FR-4.2 observability, with re-notification on a configurable cadence. No timer process exists (NFR-5). Re-notification may use the network overlay, kill-switchable (NFR-3).
- **Atomic emission:** `review.verdict` commits with the verdict artifact; `arbitration.pending` with the deadline computation record. Silence about a completed review is a tripwire, not an absence of evidence.

## Layer 3: Gate runtime and remedial dispatch (triggering KU #6)

### Gates as evidence checks

Every gate (FR-2.2 drift, FR-3.2 TDD, FR-8.4 cycle, FR-8.6 pre-upgrade) is tool code checking named evidence — never skill invocations (gate/trigger separation). A gate's verdict is a **core-emitted event committed atomically with its decision record**.

### The dispatch mechanism (KU #6 resolved)

A two-channel dispatch, with the split chosen so that a channel exists in every context where gates run:

1. **Interactive channel (agent-present contexts).** The gate injects the remedial request into the session's next-turn context — same injection path as the trigger list (triggering, mechanism 2): a compact, match-conditioned block naming the blocked evidence and the producing skill. Delivery is guaranteed because the gate controls the tool-side injection point; the agent then invokes the skill through the harness's native grammar. This is the universal channel for interactive harnesses (FR-6.1) and requires no hook surface.
2. **Headless channel (CI/agent-absent contexts).** No agent context exists to inject into. The gate **fails the step with a remedial exit code** and a structured failure payload naming the evidence and skill. Remedial invocation is then performed by whatever runner invokes the tool (CI job, pre-commit hook) — our command surface exposes `run <skill>` headlessly. The "may dispatch" of triggering.md v1.0.0 resolves to: *interactive contexts get guaranteed in-session dispatch; headless contexts get guaranteed failure-plus-command, and the backstop guarantee is that the step does not pass — which was always the core claim.*

**Loop bound (per FR-8.4 cycle):** one dispatch per gate blocking per review cycle; persistent failure escalates (FR-3.6 interrupt or FR-8.4 rejection), never retries.

**Known unknown #1 (this document):** whether two channels suffice — specifically, whether every interactive harness in the FR-6.1 set exposes a tool-controllable injection point usable for channel 1. FR-6.1's integration profiles (data-formats) must record this per harness.

## Layer 4: Cost reporting and ceremony accounting (FR-5.4, FR-1.1/1.4)

Cost reports itemize, per mission and phase:

- Ceremony-baseline overhead vs. **strict-enforcement allowance** (FR-1.4) — separately attributed, per the v1.4 resolution.
- **Subagent package injection cost** (FR-3.3), per package.
- **Preemptive/remedial split** of skill invocations (NQ-H, observability-only; target-setting is a CP).
- **Bridged vs. native flows** (composition KU #5).
- Baseline comparison against the project's running average.

Reports are derived from the event log + manifests (artifacts primary, NQ-L) at invocation points — no accounting daemon.

## Layer 5: Reference corpus (FR-3.1 / NQ-H measurement)

The corpus is the ground-truth judge for the primary metric (triggering v1.0.1):

- **Composition:** a set of representative tasks per ceremony level (trivial/standard/critical), each with **ground-truth labels of which skills are applicable** — labeled at authoring time by the corpus maintainers, reviewed like any artifact (FR-6.2).
- **Measurement:** run the corpus per harness; score auto-trigger rate as *correctly-triggered applicable invocations without explicit user command, judged by corpus labels*; report the preemptive/remedial split alongside (no target in v1).
- **Sizing:** enough tasks per harness class to make the 80% threshold meaningful — exact count is corpus-maintainer judgment; the initial corpus ships with the tool, grows via community contribution, and its labels are themselves versioned artifacts.
- **Known unknown #2 (this document):** corpus representativeness for real-world task distributions — the gap between curated tasks and organic work is exactly what field data must measure.

## Layer 6: Signed-manifest verification mechanism (deferred from governance-protocol)

Capability design only — **no v1 profile requires signatures** (governance-protocol v1.2.1 wording governs; any mandate is an accumulated CP extending FR-1.4 / touching NFR-3, second reviewer required when NFR-3 is affected).

Where a signature *would* be checked, should the capability be enabled:

- **Check point:** merge/archive gates read the session manifest's signature field; a present-but-invalid signature **fails the gate** (tamper-evidence), an absent signature under a non-requiring configuration **passes** (capability, not mandate).
- **What is signed:** the manifest content (canonical serialization) — not the event log (append-only, NQ-L) and not artifacts (git objects already carry integrity).
- **Key handling:** out of scope here — key distribution, revocation, and offline constraints (NFR-2, FR-6.7) are specified only if/when a CP makes signatures normative; designing them now would be speculative ceremony (P2).

## Interrupt and human-in-the-loop integration (FR-3.6)

Interrupt triggers are evaluated tool-side at the same invocation points as gates (deviation detection compares plan-referenced state against artifact state — artifacts primary). A raised interrupt pauses and emits `interrupt.raised` atomically with its record; resumption requires a logged response. In subagent contexts, interrupt config is inherited (FR-3.3 item 4), so child sessions pause identically.

## Deferred to data-formats.md

- Reference-corpus file format and label schema
- Injection-block format (channel 1) and `run <skill>` command grammar
- Cost-report artifact format
- Harness integration profiles recording channel-1 injection-point availability (known unknown #1)

## Known unknowns (this document)

1. **Two-channel sufficiency:** whether every interactive harness exposes a tool-controllable injection point for channel 1 (recorded per harness in FR-6.1 integration profiles).
2. **Corpus representativeness:** the gap between curated corpus tasks and organic work distributions.
3. **SLA cadence defaults:** the 72h arbitration SLA and re-notification cadence need field calibration.

## Status

- Realizes FR-3.x, FR-5.x, FR-8.x; resolves triggering KU #6 (dispatch) and the atomic-emission condition; delivers the reference corpus and the signed-manifest verification mechanism
- Honors NFR constraints 1–5
- Version 1.0.0
- Next document: `data-formats.md` (final)
