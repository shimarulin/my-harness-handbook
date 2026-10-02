# Triggering

## Purpose

This document answers Open Question Q3 of the [requirements baseline v2.0](../ideal-tool-requirements.md): how discipline skills auto-trigger at the FR-3.1 rate (≥80% of applicable invocations without an explicit user command) without Superpowers' always-loaded bootstrap and its recurring token cost. It records the mechanisms decided post-freeze: NQ-A (middleware excluded from the core combo), NQ-K (plugin conditions), NQ-H (secondary metric, observability-only in v1).

The core insight carried from the Q3 resolution: **separate triggering from compliance.** Triggering — *should a skill be invoked?* — is delegated to cheap, partly deterministic mechanisms. Compliance — *did the workflow honor the discipline?* — is guaranteed by tool-gates, which are core (see the gate/trigger separation in [governance-protocol.md](./governance-protocol.md): gates verify evidence, never skill invocations). Superpowers' bootstrap spends its tokens on both at once; this design spends almost nothing on compliance prose and buys triggering with three cheap mechanisms.

## Design constraints honored

- **NFR-5 (no daemon):** trigger conditions evaluate at invocation points; nothing watches persistently.
- **NFR-2 (offline):** no core trigger mechanism requires network.
- **NFR-3 (kill switch):** the core combo is network-independent by construction; the middleware plugin is subordinate (below).
- **NFR-5 / FR-5.2 (cold start, progressive disclosure):** the always-loaded surface is metadata-sized (~100 tokens per skill); skill bodies load only on trigger.
- **Consumer principle (governance-protocol v1.2.1):** trigger decisions are logged by the core (FR-3.1 AC) and are therefore core-emitted — authoritative about *our* invocations; silence about external skill activity belongs to the projected class and is not evidence of absence.

## The three-mechanism combo

| Mechanism | Evaluation cost | Injection cost | Reliability | Harness dependence |
|---|---|---|---|---|
| **Harness hooks** | zero (tool-side) | tokens, only on trigger | high | high (hook surface required) |
| **Trigger list** | metadata, always-loaded (FR-5.2) | tokens, only on trigger | medium (stochastic) | low |
| **Tool-gates** | zero (evidence check) | tokens, only on remedial dispatch | high (backstop) | none |

This table corrects an earlier working claim that hooks are "zero cost": the *evaluation* is free, but a triggered injection still enters agent context. All three mechanisms are cheap because injection is on-trigger only.

### 1. Harness hooks (deterministic, where available)

Where a harness exposes pre/post-action hooks, trigger conditions are evaluated in tool code, outside agent context. Preferred path: deterministic, no ambient cost. FR-3.7 already normatively requires exactly this shape for the debugging skill ("triggers on error detection without user invocation") — the baseline contains the precedent; this mechanism generalizes it.

### 2. Minimal always-loaded trigger list (stochastic fallback)

Where no hook surface exists, a compact always-loaded list carries **match conditions only — not skill bodies, not enforcement prose**:

```
- skill: systematic-debugging
  when: [test-failure, tool-error]
  load: skills/systematic-debugging/SKILL.md
```

This is the essential difference from Superpowers' bootstrap, which bundles trigger conditions with compliance language ("IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE"): compliance has moved to gates, so the list shrinks to predicates and pointers. Per-harness placement (system prefix, rules file) and the entry format are deferred to [data-formats.md](./data-formats.md).

Deterministic predicates are preferred (`test-failure`, `error-in-tool-output`). **Predicate semantics follow the carrier mechanism:** on the hooks path, conditions are evaluated as code by tool-side hook logic — deterministic; on the fallback path, the list is read by the agent as natural-language match conditions over context — stochastic, and this document claims no more than that for the fallback. Skills with no machine-observable applicability predicate may be explicit-only — FR-3.1 permits up to 20% — and are marked as such in the list.

### 3. Tool-gates (universal backstop, core)

Gates are the harness-independent guarantee and the reason a **single 80% threshold applies to all harnesses** (decided post-freeze; no per-harness baselines, no CP on FR-3.1): whatever the stochastic path misses, the gate catches as a remedial invocation. See below.

## Force-triggering

Every discipline skill is force-triggerable by an explicit command (FR-3.1 AC), in our namespace, following each harness's native invocation grammar (command-surface separation in [composition.md](./composition.md)).

## Gate-forced remedial invocation

A gate that blocks on missing evidence names the evidence and may dispatch the skill that produces it:

- The invocation occurs without an explicit user command, so it **counts toward the FR-3.1 rate** — the reading recorded post-freeze — and is audited separately as **remedial** (NQ-H).
- **Loop bound:** one remedial dispatch per gate blocking per review cycle (the cycle of the FR-8.4 state machine, see [execution-layers.md](./execution-layers.md)). Persistent failure is not retried; it escalates as an interrupt (FR-3.6) or a review rejection (FR-8.4) — never a gate↔skill ping-pong.

**Dispatch mechanism (open — known unknown #6).** "Dispatch" mechanically means: the gate names the producing skill and invokes it through a delivery channel that must exist and be reliable across harnesses. The open question is which channel: our command surface is the one guaranteed cross-harness channel (FR-6.1) but is user-facing and absent in CI/headless contexts where gates run; harness hooks, where present, are tool-side but not universal. Until resolved, "universal backstop" is the design claim and the gate's *blocking* is the hard guarantee — dispatch is resolved in [`execution-layers.md`](./execution-layers.md), which owns the gate runtime.

This is where triggering and compliance meet: the gate does not trust the skill, it trusts the evidence the skill produces — and blocks again if the evidence is still absent.

## Metrics

- **Primary (FR-3.1):** auto-trigger rate over the reference corpus — the fraction of applicable skill invocations occurring without an explicit user command, **where "applicable" is judged by corpus ground-truth labels, not by our runtime predicates** (a predicate-judged rate is self-graded: an always-on predicate scores 100% on itself). Runtime predicate logs serve as debugging evidence, never as the score. This also keeps the rate comparable with external measurements (MCP.Directory's Superpowers evaluation, Superpowers' own v6 evals), which counted invocations against external controls. Target ≥80%, single threshold, all harnesses.
- **Secondary (NQ-H, observability-only in v1):** the preemptive/remedial split, reported per mission in cost reports (FR-5.4). No target in v1 — a number set before the corpus baseline exists is either gamified or dead letter. The corpus run establishes the baseline; setting a target afterward is a CP (it adds an acceptance criterion to FR-3.1).
- **Audit trail:** trigger decisions are logged (FR-3.1 AC) — core-emitted, hence authoritative about our invocations; this log is the artifact basis for interference classification below.

## Middleware plugin (permitted, non-recommended)

Middleware/proxy inspection of assistant traffic is **not part of the core combo** (NQ-A). The precise objections: a proxy over assistant traffic is an uninspectable observation point over sensitive content (prompts, code, specs); a cloud-hosted middleware violates local-first outright; and any core dependency on it would make the kill switch destructive to triggering. It is permitted as a plugin under NFR-4, subject to four conditions:

1. Disabled by default.
2. Subordinate to the kill switch (NFR-3): disabling it removes only the plugin's contribution; the core combo is unaffected.
3. Privacy analysis against NFR-2 (local-first) before marketplace listing: a cloud-hosted middleware is a direct violation; a local one requires data-handling analysis of the sensitive-content observation point (prompts, code, specs).
4. Security disclosure of the observation surface — what traffic it inspects, what it retains — extending FR-6.8's permission/scope-disclosure machinery to the listing.

## Harness coexistence (composition KU #4)

When our skills coexist with external skill sets (e.g., Superpowers installed alongside ours):

- **Cross-fire.** Both sets may trigger on the same stimulus. Classification applies the consumer principle by emitter class: our trigger/invocation logs are authoritative about *our* invocations; external skill activity is not logged by us and is visible only through its effects — artifact changes matched by adapter projection signatures, or unowned-path changes. Absence of a projected event about external activity is not evidence of absence; classification falls back to artifact state.
- **Doubled ambient cost.** Both sets' always-loaded metadata rides the context. Mitigations: our trigger list is metadata-only (FR-5.2); adapter command-surface maps (composition template #7) make external surfaces *declared*, so overlap is at least visible. Full resolution awaits field data (known unknown #3 below).
- **Discipline collision.** Where an external skill and ours claim the same discipline (two TDD enforcers), composition's evidence-coverage declaration governs in adapted patterns (Pattern 2: evidence verified once, gaps remain core-gated). In plain coexistence without an adapter, external discipline output is not declared evidence — our gates demand our evidence forms.

## Known unknowns (field verification required)

1. **Hook surface coverage** across the ten supported harnesses (FR-6.1): which offer pre/post-action hooks — this determines the deterministic/stochastic split per harness.
2. **Stochastic-path efficacy:** the measured preemptive rate of the trigger list alone (before the gate backstop), per harness class — this sizes the list, quantifies how much work the gate is doing, and is the natural NQ-H baseline.
3. **Cross-fire behavior and doubled ambient cost** (inherited from composition KU #4).
4. **Remedial-bound calibration:** whether one dispatch per gate per cycle is the right bound.
5. **Trigger-list vs. coexistence budget:** the interaction between our always-loaded list and external skill sets' metadata under a shared context ceiling.
6. **Gate-to-skill dispatch mechanism:** the reliable cross-harness channel by which a blocked gate delivers the remedial invocation — command surface, hooks where present, or an internal path — with CI/headless contexts as the hard case. Resolved in [execution-layers.md](./execution-layers.md), which owns the gate runtime.

## Deferred

- Reference-corpus composition for FR-3.1/NQ-H measurement → [execution-layers.md](./execution-layers.md) (measurement machinery lives there)
- Trigger-list entry format, per-harness placement, and harness integration profiles (hook grammars) → [data-formats.md](./data-formats.md)
- Skill packaging and marketplace-listing integration → [data-formats.md](./data-formats.md) (with FR-6.8 security requirements)

## Status

- Answers Q3; records NQ-A/K/H mechanisms; inherits the consumer principle (emitter classes) and the gate/trigger separation
- Honors NFR constraints 1–5 (README)
- Version 1.0.1: NFR-2 misreference fixed (middleware condition 3), primary metric grounded in corpus ground-truth labels, KU #6 (gate-to-skill dispatch) registered, remedial bound anchored to the FR-8.4 cycle, predicate semantics stated per carrier mechanism
- Next document: `execution-layers.md`
