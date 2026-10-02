# Requirements for an Ideal Spec-Driven Development Tool

## Purpose

This document defines requirements for a hypothetical tool that combines the strengths of the researched spec-driven development (SDD) tools while avoiding their documented weaknesses. Each requirement traces to specific evidence from the [spec-tools research document](./spec-tools-research.md).

**Tools analyzed:** specs.md, OpenSpec, obra/superpowers, Spec Kitty, GitHub Spec Kit, BMAD, Kiro, Tessl, GSD.

**Document conventions:**
- Every functional requirement (FR) in this document carries acceptance criteria. No exceptions.
- "Non-trivial" is defined in P3. Enforcement precedence between ceremony levels and strictness profiles is defined in FR-1.4.
- Token budgets in FR-1.1 are **ceremony baselines** applying under the vibe and balanced strictness profiles; strictness-driven enforcement carries its own bounded allowance (FR-1.4).
- As of v2.0 this document is a frozen baseline; subsequent changes are made via dated change proposals (see Stabilization Note), not full-text revisions.

**Revision history:**
- v1 (2026-10-02): Initial requirements derived from spec-tools research.
- v1.1 (2026-10-02): Merged alternative requirements review r1. Added P6 (modular composition), FR-2.6–FR-2.9, FR-3.3 rule-inheritance clarification, FR-4.6, FR-5.5, FR-6.5–FR-6.6, FR-8.4–FR-8.5, Section 9 (project governance and maturity), NFR-5, strengthened NFR-2/NFR-3, expanded avoided-patterns table. Resolved Open Question 1 in favor of modular composition.
- v1.2 (2026-10-02): Applied machine review of v1.1. Fixed internal contradictions: FR-6.1 assistant count (expanded to 10 named), FR-4.2/FR-6.4 dashboard conditionality, FR-6.6/FR-9.1 unified deprecation policy, NFR-3/FR-4.3 per-integration opt-in, NFR-2/FR-4.2 local-vs-team dashboard split. Added FR-1.4 (strictness profiles), FR-2.10 (progressive elaboration), FR-2.11 (no pseudocode), FR-3.7 (systematic debugging), FR-6.7 (cloud-agnostic). Clarified FR-3.3 (enumerated inheritance list, minimal context package). Defined conflict classes (FR-2.5), non-trivial (P3), auto-trigger measurement (FR-3.1), validator regression suite (FR-2.8), review safety valve (FR-8.4), marketplace security (FR-9.3). Extended FR-6.2 to configuration-as-repo-artifact. Added acceptance criteria to all requirements introduced in v1.1.
- v1.3 (2026-10-02): Applied machine review of v1.2. Resolved ceremony-vs-strictness precedence conflict (FR-1.1, FR-1.4, FR-2.2): strictness profiles override ceremony enforcement defaults; minimal inline acceptance criteria generated at Trivial under strict profiles. Fixed FR-3.3 acceptance criterion (removed Open Question reference; made measurable). Added acceptance criteria to all remaining FRs (FR-1.2–1.3, FR-2.1–2.4, FR-3.1–3.6, FR-4.1, FR-4.3–4.5, FR-5.1–5.4, FR-6.3–6.4, FR-7.1–7.5, FR-8.1–8.3). Refined FR-6.7 (tool operations vs. assistant network needs). Replaced "where feasible" reversibility in migrations with defined classes. Restructured former Section 9: product-facing requirements moved to FR-6.8 (secure marketplace) and FR-8.6 (migration tooling); project-governance items relabeled as non-product commitments PG-1–PG-3. Updated all cross-references.
- v1.4 (2026-10-02): Applied machine review of v1.3. Resolved strict+Trivial token tension: FR-1.1 budgets redefined as ceremony baselines (balanced profile); FR-1.4 adds a bounded strict-enforcement allowance (≤5k tokens, itemized in cost reports). Added Class B arbitration fallback (FR-2.5: CODEOWNERS default, explicit blocking error as last resort). Bounded the subagent context package (FR-3.3: ≤15% of the task's ceremony budget) and clarified inheritance item 4 as interrupt-trigger configuration. Specified the FR-6.7 offline test mechanism (tool process network-isolated; assistant outside isolation). Defined kill-switch precedence over per-integration opt-ins (NFR-3, cross-referenced in FR-4.3). Fixed FR-7.4 wording ("where required by the effective strictness profile"). Specified the FR-2.10 silent-resolution detection mechanism (resolution flow with attributed decision record). Added third migration class to FR-8.6 (intentional loss: deprecation window + upgrade warning). Clarified FR-6.6/PG-1 division (per-release AC vs. longitudinal adherence). Qualified SC #2 by strictness profile. Added post-cycle-3 arbitration to FR-8.4 (per Spec Kitty #3925's documented "max 3 → arbiter"). Defined the drift-report pair format (FR-2.2). Added dashboard behavior above 50 missions (NFR-1). Delineated Open Questions 3 and 6.
- v2.0 (2026-10-02, stable baseline): Applied machine review of v1.4, folding the recommended v1.5 targeted edits into a single frozen revision. Mandatory items: FR-3.3 bound made feasible — total injected subagent context (governance inheritance plus context package) capped at the greater of 2,000 tokens or 15% of the effective budget, with digest-form inheritance permitted; FR-1.1 baselines explicitly cover vibe and balanced profiles; FR-1.4 gates vibe+Critical behind an acknowledgment-recorded warning and clarifies that ceremony process gates are not waived by vibe. Optional items also applied: FR-2.5 ownership fallback made platform-configurable (CODEOWNERS default, equivalent ownership file elsewhere) with the losing version archived per FR-2.3; FR-8.4 arbitration SLA (default 72h) with an observable escalation-pending state; NFR-1 dashboard bounds made testable (paginated render times); FR-6.7 offline harness specified cross-platform (Linux reference, equivalent mechanisms elsewhere); FR-8.6 intentional-loss example clarified; SC #2 "stock agent" baseline defined. Document frozen as the stable baseline for architectural design; subsequent changes via change proposals.

---

## Design Principles

An ideal tool must satisfy these non-negotiable principles:

### P1. Adaptive Ceremony

Process weight must scale with task complexity, not with tool defaults.

- **Evidence:** specs.md's FIRE flow adapts checkpoints (0 for simple, 1 for standard, 2 for critical); OpenSpec scores 5/5 for trivial modifications while Spec Kitty scores 2/5; Superpowers is documented as "overkill by design" for small tasks; BMAD's 21-agent workflow is called "malpractice" for production emergencies.
- **Requirement:** The tool must support at least three ceremony levels selectable per-task, not per-project.

### P2. Durable But Lightweight Artifacts

Artifacts must persist as reviewable, versioned records without becoming bureaucratic overhead.

- **Evidence:** OpenSpec's delta format (ADDED/MODIFIED/REMOVED) won independent comparison for specification quality; Spec Kitty's living wiki creates durable project memory but generates "46 markdown files after 20 min" (Dilger); SDD critical analysis notes "double review burden (specs + code)."
- **Requirement:** Every artifact must earn its existence by serving a specific downstream consumer (reviewer, future session, audit, or agent).

### P3. Enforcement, Not Just Existence

The tool must verify that code honors the spec, not merely that spec files exist.

- **Evidence:** OpenSpec's own documentation acknowledges "it only checks that artifacts exist, not that code honors them"; critical analysis across SDD tools finds "agents frequently ignore detailed specifications"; the spec-implementation gap is the most cited failure mode.
- **Requirement:** Automated spec-compliance verification must run on every non-trivial change. Throughout this document, **non-trivial** means a change executed at Standard or Critical ceremony level (FR-1.1); Trivial-level changes are exempt from mandatory enforcement **unless a strictness profile extends enforcement to them (FR-1.4)**.

### P4. Token Efficiency

The tool must minimize token consumption without sacrificing discipline.

- **Evidence:** Superpowers v6.0.0 achieved "up to 50% faster and up to 60% cheaper" by merging reviewers and pre-generating inputs; OpenSpec enforces a 50KB context limit; Superpowers users report "burned through all my max plan" on simple tasks; specs.md's FIRE flow uses adaptive checkpoints to reduce overhead.
- **Requirement:** The tool must measure and report token cost per phase, and provide mechanisms to reduce it without removing process value.

### P5. Team Observability Without Tool Lock-In

Teams must see agent activity across projects without abandoning their existing tools.

- **Evidence:** Spec Kitty's Teamspace provides cross-team observability; its tracker integration keeps Linear/Jira authoritative; Kiro's IDE lock-in is rated "high" risk; OpenSpec and specs.md have zero lock-in.
- **Requirement:** The tool must integrate with existing trackers, chat platforms, and code repositories without requiring migration.

### P6. Modular Composition Over Monolith

The ideal system is a composable ecosystem of layers — specification, planning, execution, orchestration, audit — not a single monolithic tool. Users enable only the components they need.

- **Evidence:** The `superpowers-bridge` schema demonstrates OpenSpec + Superpowers composition working in practice; spec-coding.dev's recommendation is "one planning tool (OpenSpec for fluid, brownfield changes, Spec Kit for a stricter lifecycle) plus Superpowers for execution"; the r1 requirements review argues the ideal tool is "not a replacement" for the researched tools "but a composition" — OpenSpec for lightweight change management, Superpowers for execution discipline, Spec Kitty for parallel orchestration, Spec Kit/specs.md for strict specifications — under a unified shell with shared configs, a common API, and git-native storage.
- **Requirement:** Each layer must be independently adoptable, individually disableable, and interoperable with the others via documented bridges or schemas. The core must be open-source, with transparent configuration and no hidden telemetry.

This principle resolves the former Open Question 1 ("single tool vs. combination?") in favor of composition.

---

## Functional Requirements

### 1. Adaptive Process Management

#### FR-1.1: Ceremony-Level Selection

The tool must support selecting ceremony level per task, not per project.

| Level | Checkpoints | Use Cases | Ceremony Baseline (vibe & balanced profiles) |
|---|---|---|---|
| **Trivial** | 0 | Bug fixes with clear repro, config changes, typo fixes, documentation updates | <5k tokens overhead |
| **Standard** | 1-2 | Feature additions, refactors, API endpoints | <20k tokens overhead |
| **Critical** | Full | Security changes, data model changes, cross-service work | <50k tokens overhead |

Ceremony baselines cover artifact and process overhead and are independent of enforcement intensity: they apply under the **vibe** and **balanced** strictness profiles alike (vibe differs only in rendering discipline enforcement advisory, per FR-1.4). The **strict** profile adds the bounded enforcement allowance defined in FR-1.4, so that ceremony cost and strictness cost remain independently attributable.

**Acceptance criteria:**
- User can specify ceremony level via single flag or config
- Tool auto-detects complexity and suggests level (user can override)
- Trivial mode skips spec generation by default for tasks under a configurable threshold; **exception:** where a strictness profile (FR-1.4) enforces spec-dependent disciplines at Trivial ceremony, a minimal inline acceptance-criteria artifact is generated instead, within the Trivial baseline plus the strict enforcement allowance
- Critical mode requires spec review before implementation begins

**Traces to:** specs.md FIRE flow adaptive checkpoints; OpenSpec's "skip it for a typo fix"; Superpowers' "bypass it explicitly for trivia."

#### FR-1.2: Iterative Refinement Without Restart

The tool must allow mid-feature course correction without discarding completed work.

- **Evidence:** BMAD scores 5/5 for "Mid-feature course correction" while Spec Kit scores 2/5; OpenSpec allows editing any artifact at any time with no phase gates; SDD critical analysis notes "agents over-apply or misinterpret instructions" requiring correction.
- **Requirement:** Modifying a spec mid-implementation must trigger delta propagation to affected tasks, not a full restart.

**Acceptance criteria:**
- A mid-implementation spec edit propagates only to tasks whose acceptance criteria it touches; unaffected tasks and their results survive unchanged
- Affected tasks are flagged for re-verification rather than regenerated from scratch
- The propagation is logged, listing each affected task and the spec clause that changed

#### FR-1.3: Exploratory Mode

The tool must support exploratory/spike work without forcing premature specification.

- **Evidence:** Superpowers criticism notes "you're exploring, not building... spikes, prototypes, and 'what does this codebase even do' sessions fight the plan-first structure"; specs.md's Ideation Flow (Spark → Flame → Forge) exists specifically for this.
- **Requirement:** An exploratory mode must produce concept briefs, not implementation specs, and must not count toward project spec debt.

**Acceptance criteria:**
- Exploratory sessions produce concept briefs only; no implementation specs, plans, or task lists are generated
- Concept briefs are excluded from canonical spec-tree validation and from spec-debt metrics
- Transitioning from exploration to implementation routes through the spec phase; briefs can seed but do not substitute for specs

#### FR-1.4: Strictness Profiles

Enforcement intensity of individual disciplines must be configurable independently of process weight, via named strictness profiles with per-setting overrides.

- **Evidence:** The r1 review requires profiles "from vibe coding to a militarized process," noting that hard gates must not be mandatory for all tasks. Ceremony levels (FR-1.1) control process weight; they do not by themselves permit, e.g., a heavyweight process with relaxed TDD or a lightweight one with strict drift detection. Superpowers' single fixed discipline bundle is the counter-example: "bypass it explicitly for trivia" is the documented escape hatch.
- **Requirement:** The tool must provide named strictness presets — at minimum **vibe** (all discipline enforcement advisory), **balanced** (ceremony-level defaults; FR-1.1 baselines apply as stated), and **strict** (TDD and drift detection enforced even at Trivial ceremony, via the minimal inline acceptance criteria of FR-1.1; adversarial review on all changes, performed as a lightweight merge-time gate at Trivial) — and every discipline toggle (TDD enforcement, review depth, drift detection, verbosity limits) must be individually configurable, overriding any preset.

  **Precedence rule:** Strictness profiles override ceremony-level enforcement defaults (including FR-2.2 and FR-3.2). The ceremony level governs artifact volume and process weight; the effective strictness profile governs enforcement intensity. A profile never changes ceremony-level artifact volume beyond the minimal inline artifact required to give enforcement a referent. Note that ceremony-level **process gates** (e.g., Critical's mandatory spec review, FR-1.1) are process checkpoints, not discipline enforcement, and are **not** waived by any profile: vibe renders *discipline enforcement* (TDD, drift detection, adversarial review) advisory only.

  **Critical-ceremony safety:** selecting the vibe profile for a change classified Critical is permitted (full configurability is intentional) but gated by an explicit warning: the tool names the disciplines that will be advisory against the change's Critical classification, and the warning must be acknowledged once per project; the acknowledgment is recorded in configuration (FR-6.2) and surfaced in the effective-config inspection and mission reports.

  **Strict enforcement allowance:** strict-profile enforcement at Trivial ceremony operates within an explicit allowance of **≤5k tokens on top of the Trivial ceremony baseline**, itemized separately in cost reports (FR-5.4). This keeps strict+Trivial feasible (drift check, merge-time gate, and criteria generation share the allowance) while keeping ceremony and strictness costs separately attributable; vibe and balanced profiles are unaffected.

**Acceptance criteria:**
- Switching profiles changes only enforcement behavior; no project state or artifacts are lost or regenerated
- Every discipline toggle is individually settable at project and task level
- The effective configuration (profile plus overrides) is inspectable via a single command and stored per FR-6.2
- Selecting vibe for a Critical-classified change triggers the warning; proceeding requires the recorded acknowledgment, visible in the effective-config inspection
- Under the strict profile at Trivial ceremony: a minimal inline acceptance-criteria artifact exists, drift detection runs against it, and a merge-time review gate executes — while ceremony-baseline overhead stays within the FR-1.1 budget and enforcement overhead stays within the ≤5k allowance, both itemized in the cost report (FR-5.4)

---

### 2. Specification Management

#### FR-2.1: Delta-Based Specs

Specifications must use delta format (ADDED, MODIFIED, REMOVED) rather than full rewrites.

- **Evidence:** OpenSpec's delta format is purpose-built for modifications and won independent comparison for specification quality (4/5) vs Spec Kit's 2/5; critical analysis notes "Spec-Kit requires `/speckit.clarify` workaround, not optimized for small changes."
- **Requirement:** Every spec change must express only what is changing, with automatic merge into the canonical spec tree upon archive.

**Acceptance criteria:**
- A one-field change produces a delta referencing only that field and its requirement
- Archiving merges the delta into the canonical tree without rewriting untouched requirements
- The canonical spec is reconstructible from the archive history alone

#### FR-2.2: Spec Drift Detection

The tool must detect and alert when implementation diverges from specification.

- **Evidence:** Critical analysis identifies "spec drift over time" as an unresolved question; OpenSpec's `/opsx:verify` exists specifically for this but requires explicit invocation; the spec-implementation gap is "the most cited failure mode."
- **Requirement:** Automated drift detection must run on every PR for non-trivial changes (per P3). A strictness profile may extend enforcement to Trivial-level changes per the precedence rule in FR-1.4; the ceremony-level default alone never disables an explicitly enforced discipline.

**Acceptance criteria:**
- Drift detection runs on every PR for Standard and Critical changes without manual invocation
- Under a strict profile, it also runs for Trivial changes against their minimal inline acceptance criteria
- Divergences are reported as spec-clause ↔ code-location pairs — spec clause reference plus code location as file with line-range or symbol reference — in a machine-readable report, and gate the merge

#### FR-2.3: Rejected-Proposal Memory

The tool must remember declined proposals to prevent re-proposing rejected ideas.

- **Evidence:** OpenSpec's documentation acknowledges `/opsx:archive` has "no dedicated status for a declined change, so nothing tells a future proposal that an idea was already investigated and turned down."
- **Requirement:** Declined changes must be archived with reasoning and be searchable by future proposals.

**Acceptance criteria:**
- A declined change archives with a machine-readable decision record including the reason
- A new proposal touching the same area surfaces the prior rejection and its reasoning
- Rejections are searchable via a single command by requirement, date, and reason

#### FR-2.4: Spec Verbosity Control

The tool must enforce spec length limits appropriate to change scope.

- **Evidence:** OpenSpec's most-cited complaint: "The AI generates way more spec than I need... an agent can turn a thirty-minute feature into an 800-line spec"; the 50KB context limit forces some discipline but "delta specs themselves have no hard limit."
- **Requirement:** Configurable spec size limits per ceremony level; automatic flagging when specs exceed thresholds; agent must justify why a spec exceeds the limit.

**Acceptance criteria:**
- Size limits are configurable per ceremony level and enforced at generation time
- An over-limit spec is flagged and cannot be finalized without an explicit justification entry
- Default limits keep a Standard-ceremony spec within the token budget of FR-1.1

#### FR-2.5: Parallel-Change Conflict Resolution

The tool must handle multiple in-flight changes touching the same requirement or the same shared state, with resolution rules defined per conflict class.

- **Evidence:** OpenSpec documented edge case: "Two changes touched the same requirement and one silently dropped the other's scenario... archiving applies a MODIFIED delta as a whole-block replace keyed by requirement name." The r1 review additionally flags conflicts in shared state files (e.g., `state.yaml`) when parallel agents run in separate worktrees; Spec Kitty's original worktree-per-work-package strategy was itself unstable enough to be replaced in v3.1.0.
- **Requirement:** Concurrent modifications must be detected before merge/archive and resolved according to conflict class:
  - **Class A — independent** (different requirements, different files): auto-merge; never blocks
  - **Class B — same-requirement** (two in-flight changes modify the same requirement): human arbitration required before archive; both versions presented with their scenarios. The arbitrator is the **accountable owner** for the affected area, routed via the decision mechanism of FR-4.1; the verdict is recorded as a decision record per FR-4.4, and the **non-chosen version is archived with its rejection rationale** (per FR-2.3) so that neither version is lost. **Fallback chain:** if no accountable owner is configured for the affected area, arbitration falls back to repository maintainers via a **configurable ownership declaration** (stored per FR-6.2): CODEOWNERS where the hosting platform supports it, or a configured equivalent ownership file on platforms without one; if no ownership declaration resolves, archive remains blocked with an explicit error naming the missing configuration and how to set it — never a silent drop or an indefinite unexplained block
  - **Class C — shared state files** (e.g., worktree coordination state such as `state.yaml`): three-way merge attempted automatically; unresolved conflicts escalate to human review
- **Acceptance criteria:**
  - Class A changes merge without interaction
  - Class B changes always block archive until arbitration; neither version is silently dropped; the arbitration verdict is a linked, versioned artifact, and the losing version is preserved with its rationale, retrievable per FR-2.3
  - When no owner is configured, the configured ownership fallback engages (CODEOWNERS by default, an equivalent ownership file on other platforms); when no declaration resolves, the block is accompanied by a configuration error
  - Class C merge attempts are logged; failures present a readable conflict for resolution

#### FR-2.6: Greenfield Spec Generation

The tool must support full-spec generation for new systems, not only delta changes to existing ones.

- **Evidence:** Spec Kit is rated 5/5 for greenfield work ("Constitution-driven governance... purpose-built for greenfield") while OpenSpec scores 3/5 ("lightweight, better suited for modifications than greenfield"); specs.md targets both greenfield and brownfield across its flows; the r1 review requires explicit support for both.
- **Requirement:** A greenfield mode must produce complete requirement, design, and task specifications from a project brief, while reusing the same artifact formats as brownfield delta specs so projects can transition between modes without migration.

**Acceptance criteria:**
- Greenfield mode produces requirement, design, and task specs from a project brief in one session
- Greenfield artifacts use the same formats as brownfield delta specs; no format migration is needed when the project becomes brownfield
- Transitioning a repository from greenfield to brownfield requires no artifact conversion

#### FR-2.7: Spec Formality Spectrum

Specifications must support a spectrum of formality, from lightweight notes to formal requirement language, within a single source of truth.

- **Evidence:** OpenSpec delta specs use formal SHALL-language scenarios ("The app SHALL let users switch between light and dark themes"); SDD critical analysis notes ongoing confusion about "where functional specs end and technical implementation begins" and inconsistent interpretation across tools; the r1 review requires "levels of detail: from light notes to formal SHALL/MUST requirements."
- **Requirement:** Spec templates must support at least three formality levels — note-style, structured scenario, formal SHALL/MUST with testable acceptance criteria — selectable per requirement and upgradeable in place without rewriting.

**Acceptance criteria:**
- Any requirement can be expressed at any formality level
- A requirement upgrades in place (note → scenario → SHALL/MUST) without rewriting sibling requirements
- Formal-level requirements carry testable acceptance criteria; note-level requirements are valid without them

#### FR-2.8: Reliable Spec Validation

Spec validation commands must be deterministic and robust; validator failures must never silently pass or produce spurious errors.

- **Evidence:** The r1 requirements review reports validation bugs of the "no requirement entries parsed" class in existing tools; OpenSpec ships `openspec validate` as a core command, making the validator a single point of failure for CI integration.
- **Requirement:** Validation must produce unambiguous pass/fail results with error locations pointing at the offending lines; validation failures must block archive/merge. The validator must ship with a regression suite covering **every documented failure class** (including parse failures of the "no requirement entries parsed" kind), with at least one test per class; failure classes discovered in the wild must be added to the suite before the next release.

**Acceptance criteria:**
- CI runs the validator regression suite on every release
- No documented failure class lacks a regression test
- Validator errors identify file and line; a spec that fails to parse can never validate as true

#### FR-2.9: Monorepo and Hierarchical Standards

The tool must support monorepositories with nested projects, independent per-module configuration, and no instruction bloat.

- **Evidence:** specs.md's FIRE flow provides "hierarchical standards with module-specific overrides. One project, multiple tech stacks"; OpenSpec's 50KB context cap is a partial mitigation but not a monorepo design; the r1 review explicitly requires nested projects with independent configurations and no "instruction growth."
- **Requirement:** Sub-project configuration must inherit and override repository-level standards; context injected into agents must be scoped to the affected module and its ancestors; unrelated sibling modules must not inflate the context of work on a given module.

**Acceptance criteria:**
- A module's context contains its own standards plus inherited repository standards, and no sibling-module standards
- Adding a sibling module does not change the context payload of work on an existing module
- Per-module overrides are expressible without editing repository-level defaults

#### FR-2.10: Progressive Elaboration

Specifications must be allowed to start incomplete and be elaborated iteratively; unknowns must be explicitly marked, never guessed.

- **Evidence:** Spec Kit's templates "flag unknowns as NEEDS CLARIFICATION rather than guessing" — the strongest existing implementation of this pattern; the r1 review requires that the tool "not demand exhaustive data at the start — context must be built up iteratively." Contrast with elicitation flows that force completeness before any work begins.
- **Requirement:** A spec containing explicitly marked unknowns must be valid, and its known portions implementable. Unknowns must use a standard, searchable marker; agents must never silently resolve them. Implementation tasks depending on unresolved unknowns must be blocked until resolution. **Resolution mechanism:** a marked unknown may only be resolved through the tool's resolution flow, which requires user attribution and records a decision entry (who resolved it, when, and the source of the answer, per FR-4.4).

**Acceptance criteria:**
- A spec with marked unknowns passes validation and is implementable for known requirements
- Resolving an unknown via the resolution flow updates the spec in place via delta and records an attributed decision entry
- Tasks blocked on unknowns report the blocking marker
- A delta that removes an unknown marker without a corresponding attributed decision record fails validation (silent resolution is detectable and rejected)

#### FR-2.11: No Pseudocode in Business-Facing Specs

Business-facing spec layers must contain no pseudocode or implementation-like notation.

- **Evidence:** The r1 review requires "Markdown + schemas, but without sliding into pseudocode"; Dilger's critique documents business stakeholders unable to engage with tool output. In practice, agents frequently turn requirement specs into pseudocode, which defeats FR-7.3's plain-language review.
- **Requirement:** The business-facing layers of a spec (requirements, scenarios, acceptance criteria) must not contain pseudocode, code-like notation, or implementation language. Implementation detail belongs exclusively to the plan and task layers.

**Acceptance criteria:**
- Spec linting flags pseudocode-like constructs in business-facing layers
- Plain-language summaries are generated without code notation
- Business-facing and technical artifacts are structurally separated (distinct files or sections)

---

### 3. Execution & Quality Enforcement

#### FR-3.1: Contextual Skill Triggering

Discipline skills must trigger automatically based on context, not require explicit invocation.

- **Evidence:** Superpowers' auto-trigger model is praised: "The agent doesn't *decide* to brainstorm; the brainstorming skill triggers because the user mentioned a vague idea"; contrasted with Spec Kit's "human types `/speckit.plan`. Explicit, deterministic."
- **Requirement:** At least 80% of discipline skills must auto-trigger; users must be able to force-trigger any skill explicitly. The auto-trigger rate is measured over a reference corpus of representative tasks as the fraction of applicable skill invocations that occur without an explicit user command.

**Acceptance criteria:**
- Over the reference corpus, ≥80% of applicable skill invocations occur without an explicit user command
- Every discipline skill is force-triggerable by explicit command
- Trigger decisions are logged so the rate is auditable

#### FR-3.2: Mandatory TDD (Configurable)

Test-Driven Development must be enforced by default for standard and critical ceremony levels, with opt-out for trivial.

- **Evidence:** Superpowers' "Iron Law" of TDD is its defining characteristic: "No production code without a failing test first"; a controlled comparison found better output quality on non-trivial tasks with TDD enforcement.
- **Requirement:** TDD enforcement must be on by default, configurable per-project and per-task (including via strictness profiles, FR-1.4), with automatic deletion of implementation code written before tests.

**Acceptance criteria:**
- Under an enforcing profile and ceremony level, implementation code written before a failing test is deleted or blocked from merging
- Per-task opt-outs are recorded in the mission log with the opting user
- Under the vibe profile, enforcement is advisory: violations warn but do not block

#### FR-3.3: Subagent Isolation with Rule Inheritance

Each implementation task must execute in an isolated context, but subagents must inherit the governance rules and a defined minimal context package from the parent session.

- **Evidence:** Superpowers' subagent-driven development is called "a brilliant solution to context collapse. Each subagent only knows about its specific task, preventing it from getting confused by previous steps or unrelated code." However, Superpowers' own `using-superpowers` bootstrap instructs: "If you were dispatched as a subagent to execute a specific task, ignore this skill" — subagents are explicitly exempted from the discipline bootstrap, creating exactly the gap the r1 review identifies (subagents ignoring TDD and other constraints).
- **Requirement:** Tasks must execute in isolated subagents; subagent results must be reviewed before merging into main context. **Isolation applies to accumulated session context, not to governance.** Each subagent must inherit, at minimum:
  1. The project constitution/doctrine
  2. Discipline enforcement settings (TDD and the effective strictness profile, FR-1.4)
  3. Scope boundaries and the task definition
  4. Interrupt-trigger configuration (FR-3.6), so that deviations inside a subagent pause it identically to the parent session
  5. Coding and security standards
  6. The spec deltas relevant to the task

  Each subagent must receive a **minimal context package**: the task definition, affected spec deltas, and interface contracts of the modules the task touches. Accumulated session history and unrelated task context must be excluded. Governance inheritance may be delivered in a compact **digest form** (full constitution and standards texts remaining available on demand) to keep injected context within bounds.
- **Acceptance criteria:**
  - Subagent prompts verifiably contain the constitution (or its digest) and effective enforcement settings
  - A subagent attempting to skip TDD under an enforcing profile is blocked
  - Total injected subagent context — governance inheritance plus the minimal context package — is bounded: it must not exceed the **greater of 2,000 tokens or 15% of the task's effective token budget** (the applicable ceremony baseline per FR-1.1 plus any active strictness allowance per FR-1.4), counted within that budget rather than in addition to it; its token cost is reported per FR-5.4
  - No always-loaded bootstrap is injected into subagent context: governance rules are attached per-task to the context package, and the per-task inheritance overhead is measured and reported under FR-5.4 (the question of minimizing that overhead remains Open Question 6)

#### FR-3.4: Adversarial Review (Not Confirmatory)

Plan and spec review must attempt to break the plan, not merely confirm completeness.

- **Evidence:** GitHub issue #1803 on Superpowers: "The built-in writing-plans self-review is confirmatory — it checks coverage, types, and placeholders. It does not attempt to break the plan... Claude in 'completion state' produces plans that look correct but contain silent failures."
- **Requirement:** Review phase must explicitly instruct the reviewer to trace intermediate states, run commands mentally, and verify assumptions against the actual codebase.

**Acceptance criteria:**
- Review prompts instruct the reviewer to attempt to break the plan, not merely confirm coverage
- Unverified shell commands and environment assumptions are surfaced as findings
- Findings are categorized by fix type (surface fix, architectural issue, wrong problem)

#### FR-3.5: Context-Clearing Guidance

The tool must indicate when context can safely be cleared between phases.

- **Evidence:** Superpowers issue #655: "It provides no guidance as to when context can safely be cleared (/clear) between phases. From start to finish, it stayed on the same context... 80k tokens of baggage that will degrade the accuracy of future generation?"
- **Requirement:** After each phase completion, the tool must indicate whether context can be cleared and what minimal state must be preserved.

**Acceptance criteria:**
- On each phase completion, the tool states whether context may be cleared, without being asked
- The preserved minimal state (file paths, mission pointer, active deltas) is enumerated in the guidance
- Resuming from cleared context loses no mission state

#### FR-3.6: Human-in-the-Loop Interrupts

The agent must pause and ask when implementation deviates from plan or encounters unexpected constraints.

- **Evidence:** Superpowers issue #655: "Claude Code seems to generally be blazing through on its own without ever stopping to ask me stuff if things aren't going according to plan... Claude kept trying to YOLO it by playing around with critical arguments."
- **Requirement:** Configurable interrupt triggers for: plan deviation, external tool errors, assumption invalidation, and scope expansion.

**Acceptance criteria:**
- Each trigger condition (plan deviation, external tool error, assumption invalidation, scope expansion) pauses the agent with a question rather than an autonomous workaround
- Resumption requires a user response; the exchange is logged
- Triggers are individually enabled/disabled per project and per task

#### FR-3.7: Systematic Debugging Skill

A systematic-debugging skill must auto-trigger on errors and enforce root-cause analysis before fix attempts.

- **Evidence:** Superpowers ships `systematic-debugging` and `verification-before-completion` among its core skills; the r1 review lists systematic debugging among the required engineering disciplines alongside TDD, verification, and review.
- **Requirement:** The debugging skill must trigger automatically when the agent encounters an error or failing test, and must enforce the sequence: reproduce → isolate → hypothesize → test hypothesis → fix → verify. Fixes attempted without a reproduction must be rejected.

**Acceptance criteria:**
- The skill triggers on error detection without user invocation
- Fix proposals without a reproduction step are rejected by the workflow
- Invocations produce a debug-log artifact linked to the task (FR-4.6)

---

### 4. Team Collaboration & Governance

#### FR-4.1: Decision Moments with Stakeholder Routing

Important decisions must be surfaced to relevant stakeholders before agent continues.

- **Evidence:** Spec Kitty's Decision Moments "widen those moments by moving the question into a Slack or Teams thread, so the people who need to participate can weigh in before the agent continues."
- **Requirement:** Decisions affecting deployment policy, domain language, architecture, customer impact, or migration strategy must be routable to accountable/consulted/informed parties.

**Acceptance criteria:**
- Decisions in the listed categories route to designated stakeholders (via chat thread or equivalent) before the agent proceeds
- Routing targets are configurable per decision category
- An unresolved decision blocks the agent; the block and its resolution are logged

#### FR-4.2: Cross-Team Observability (Conditional Dashboard)

Where the dashboard is enabled, it must show agent mission activity; the same data must be accessible via CLI and API regardless of dashboard use.

- **Evidence:** Spec Kitty's Teamspace: "shows which Spec Kitty missions are running in which builds of which projects, what state they are in, and how that work relates back to the team's canonical tracker and repository."
- **Requirement:** Where enabled, the dashboard must show active missions, their state, owner, blockers, and relationship to tracker tickets. All observability data must be equally accessible via CLI commands and a query API, independent of the dashboard (per FR-6.4). Two components are distinguished: a **local dashboard** (single-repo, offline-capable, reads repository state) and an optional **team dashboard** (cross-repo aggregation, networked; its unavailability must not affect local operation, per NFR-2).
- **Acceptance criteria:**
  - A CLI command lists all missions with state, owner, and blockers
  - The local dashboard functions with no network connectivity
  - Disabling the dashboard removes no capability: all data remains reachable via CLI/API
  - Distinct workflow states — including arbitration-pending and escalation-pending (FR-2.5, FR-8.4) — are individually visible and filterable

#### FR-4.3: Tracker Authority Preservation

External trackers (Linear, Jira, GitHub Issues) must remain the source of truth for work status.

- **Evidence:** Spec Kitty's design: "a developer can pull a ticket from Linear or Jira into the Spec Kitty CLI and turn it into a full mission... While the work is being implemented, Spec Kitty keeps the ticket updated so the team's normal tracker remains useful."
- **Requirement:** Two-way sync with at least Linear, Jira, and GitHub Issues; tracker status must update automatically as agent work progresses. Tracker sync is **opt-in per integration**: consent is recorded as a versioned repository file (NFR-3), sync actions are logged, and consent is revocable at any time — revocation halts sync without data loss. The global network kill switch (NFR-3) overrides all per-integration consent while active; consent configurations survive and take effect again when the kill switch is lifted.

**Acceptance criteria:**
- Tracker ticket status reflects mission state without manual edits, in both directions (ticket → mission, mission → ticket)
- Each integration's consent is a separate, versioned, reviewable file; revoking it halts that integration's sync without losing repository state
- Activating the kill switch halts all opted-in sync while preserving consent files for re-enable
- Every sync action is logged with timestamp and direction

#### FR-4.4: Living Project Memory

The tool must maintain a searchable, durable record of decisions, specs, and evidence.

- **Evidence:** Spec Kitty's `kitty-specs` wiki: "specs, plans, evidence, review trails, and Decision Moment ADRs... not just ceremony. They are a living wiki of how the software is being changed"; compared to Karpathy's advocacy for "LLM-maintained Markdown knowledge bases."
- **Requirement:** All decisions, specs, plans, and review results must be stored as versioned, searchable, linked artifacts in the repository.

**Acceptance criteria:**
- Every decision, spec, plan, and review result exists as a versioned, linked artifact in the repository
- Artifacts are searchable by content and navigable via their link graph
- No decision or review outcome exists only in chat history or ephemeral state

#### FR-4.5: Onboarding and Context Recovery

New team members and fresh sessions must be able to recover project context from artifacts.

- **Evidence:** SDD critical analysis notes "long-term maintenance: unclear maintenance story, risk of spec drift, may abandon specs after initial development"; OpenSpec's archive mechanism creates durable current-state description.
- **Requirement:** A single command must generate a comprehensive project context summary from stored artifacts, sufficient for a new session or team member to understand current state.

**Acceptance criteria:**
- A single command produces a context summary covering active missions, current specs, open decisions, and recent changes
- The summary is generated entirely from stored artifacts — no session history required
- A fresh session resumed from the summary alone can continue an in-flight mission

#### FR-4.6: Traceability Reporting

The tool must provide queryable traceability: what was built, by whom (which agent or human), and on the basis of which requirements and decisions.

- **Evidence:** Spec Kitty positions itself as providing "an auditable delivery record from first decision to merge"; the SDD critical analysis lists "who maintains specifications during bug fixes?" among unresolved questions; the r1 review requires visible "who/what/why" metrics.
- **Requirement:** Every merged change must link to the originating requirement(s), the decision records that shaped it, the implementing agent/session, and the review verdicts. A single command must produce a traceability report for any artifact or requirement.

**Acceptance criteria:**
- Every merged change links to originating requirement(s), decision records, implementing session, and review verdicts
- A single command produces a traceability report in both directions (requirement → changes → code; code → change → requirement)
- Broken links fail CI

---

### 5. Token & Context Efficiency

#### FR-5.1: Phase-Based Token Budgets

Each phase must have configurable token budgets with alerts on overrun.

- **Evidence:** Superpowers' optimization history: v5.0.6 removed subagent review loops after "~25 minutes of overhead with no measurable quality gain"; v6.0.0 achieved "up to 50% faster and up to 60% cheaper"; yet "no amount of optimization makes a design interview free."
- **Requirement:** Token usage must be tracked per phase; alerts must fire when budget exceeded; tool must suggest which phase to simplify.

**Acceptance criteria:**
- Per-phase budgets are configurable and actual usage is recorded per phase
- Budget overrun raises an alert naming the exceeded phase
- The alert includes a suggestion of which phase to simplify or skip

#### FR-5.2: Progressive Disclosure

Only relevant context should be loaded at each phase, not the full project state.

- **Evidence:** Superpowers' progressive disclosure: "~100 tokens per skill for always-loaded metadata, skill bodies under 5k tokens loaded only on trigger"; Anthropic's documented approach.
- **Requirement:** Context injection must be scoped to current task; irrelevant project state must not consume context window.

**Acceptance criteria:**
- The context payload for a task contains only task-relevant spec deltas, plans, and standards
- Dormant skills cost only their always-loaded metadata (bounded, per-skill)
- Injected context for unrelated modules or missions is measurable as zero

#### FR-5.3: Worktree Isolation with Cleanup

Parallel work must use isolated worktrees with automatic cleanup on merge.

- **Evidence:** Spec Kitty pioneered "built-in git worktree support among SDD tools... Automatic worktree creation per feature, Parallel feature isolation without branch switching, Automated cleanup on merge"; Superpowers' "Using Git Worktrees: Isolated branches with verified test baselines."
- **Requirement:** Worktree management must be automatic, with configurable strategy (per-feature or per-swim-lane) and cleanup on completion.

**Acceptance criteria:**
- Parallel tasks receive isolated worktrees and branches without manual git commands
- Merge (or rejection) triggers worktree and branch cleanup automatically
- Strategy is configurable per project; no orphaned worktrees remain after mission completion

#### FR-5.4: Cost Reporting

The tool must report token and time cost per mission, phase, and task.

- **Evidence:** The "hidden costs of spec-driven development" analysis identifies six cost types teams forget to track; MCP.Directory's controlled comparison found "runs 9% cheaper with 14% fewer tokens" on non-trivial tasks.
- **Requirement:** Post-mission reports must include: total tokens, tokens per phase, time elapsed, and comparison to project baseline.

**Acceptance criteria:**
- Every completed mission produces a report with total tokens, per-phase tokens, and elapsed time
- The report includes comparison against the project's running baseline
- Subagent context-package overhead (FR-3.3) is itemized in the report
- Where a strictness profile is active, strictness-driven enforcement overhead (e.g., the Trivial allowance of FR-1.4) is itemized separately from ceremony-baseline overhead

#### FR-5.5: Context Caching and Summarization

The tool must reduce token consumption through caching and summarization of previously established context.

- **Evidence:** Superpowers v6.0.0 achieved "up to 50% faster and up to 60% cheaper" partly by pre-generating review inputs; progressive disclosure keeps dormant skills cheap; the r1 review explicitly requires "selective context loading, caching, summarization."
- **Requirement:** Phase outputs must be cached and reused across sessions where unchanged; long-running context must be summarizable into compact form for downstream phases; cache invalidation must be automatic on spec or plan change.

**Acceptance criteria:**
- Re-running an unchanged phase consumes <10% of the original generation tokens
- Cache invalidates automatically when spec or plan inputs change
- Summarized context is explicitly flagged and distinguishable from primary artifacts

---

### 6. Integration & Portability

#### FR-6.1: Multi-Agent Support

The tool must work with at least 10 AI coding assistants without lock-in.

- **Evidence:** OpenSpec supports "30+ assistants including Claude Code, Cursor, GitHub Copilot, Gemini CLI, Codex, Kiro, and OpenCode"; Superpowers has first-class plugin packages for multiple harnesses (Antigravity, Codex, Cursor, Devin CLI, Gemini CLI, GitHub Copilot CLI, OpenCode, Qwen Code, and others); Kiro's lock-in is rated "high" risk.
- **Requirement:** Support for Claude Code, Cursor, GitHub Copilot, Gemini CLI, Codex, OpenCode, Windsurf, Antigravity, Devin CLI, and Qwen Code — at least 10 named assistants — plus an extensible plugin architecture for others.

**Acceptance criteria:**
- Each named assistant is supported via a documented integration
- Adding a new assistant requires no core changes, only a plugin
- No capability is exclusive to a single assistant

#### FR-6.2: Repository-Native Storage and Configuration

All artifacts and all configuration must live in the repository as version-controlled files.

- **Evidence:** Spec Kitty: "specs, plans, work packages, acceptance criteria, decision records, review state, and merge status become repo-native artifacts, not ephemeral chat"; OpenSpec: "commit the whole `openspec/` folder to git"; the r1 review requires that configuration be versioned and reviewable, with no hidden global state.
- **Requirement:** No external database or service required for core functionality; all state recoverable from git. **All configuration** — ceremony defaults, strictness profiles, integration settings, telemetry consent, ownership declarations (FR-2.5) — must likewise be stored as versioned files in the repository; no hidden global state outside the repository may affect project behavior.
- **Acceptance criteria:**
  - Cloning a repository reproduces complete tool behavior
  - Configuration changes go through code review like any other change
  - No tool state outside the repository and git caches affects semantics

#### FR-6.3: Bridge/Combination Support

The tool must support combination with complementary tools via documented schemas or bridges.

- **Evidence:** The `superpowers-bridge` schema for OpenSpec redirects Superpowers output into OpenSpec change folders; spec-coding.dev recommends "one planning tool (OpenSpec for fluid, brownfield changes, Spec Kit for a stricter lifecycle) plus Superpowers for execution."
- **Requirement:** Export/import mechanisms for spec artifacts; documented combination patterns with at least Superpowers and OpenSpec.

**Acceptance criteria:**
- Spec artifacts export and re-import losslessly (round-trip preserves semantics)
- A documented, tested combination exists with at least OpenSpec and with Superpowers
- Combination avoids duplicate artifacts: one designated home per artifact type

#### FR-6.4: CLI-First with Optional Dashboard

Core functionality must work entirely from CLI; dashboards are optional enhancements.

- **Evidence:** OpenSpec is "a free, open-source CLI... does not write code by itself or replace Claude Code, Codex, Cursor, or GitHub Copilot"; Spec Kitty's dashboard is "visual kanban boards tracking work progress" but CLI-first.
- **Requirement:** All operations must be scriptable; the dashboard must be an optional layer, not a dependency.

**Acceptance criteria:**
- Every operation is expressible as a CLI command (including in CI)
- Removing or never installing the dashboard loses no capability
- Dashboard state is derived from repository state, not held only in the dashboard

#### FR-6.5: IDE-Agnostic Operation

The tool must work from any editor or no editor at all; no functionality may require a specialized IDE.

- **Evidence:** specs.md's comparison matrix rates Kiro's IDE lock-in as "High — Kiro IDE + Claude Sonnet only" while rating all CLI-based tools "None (any IDE)"; the r1 review requires IDE-agnostic operation explicitly.
- **Requirement:** All features must be accessible via CLI and standard file formats; IDE extensions, where offered, must be additive conveniences and never the only path to a capability.
- **Acceptance criteria:**
  - Every feature is accessible via CLI and files
  - IDE extensions add convenience only; removing an extension loses no capability
  - A documented feature × access-path matrix shows no IDE-only cells

#### FR-6.6: Documentation and Command Naming Discipline

Documentation must include examples and migration guides; command names must be unambiguous and conflict-free, with a single unified deprecation policy.

- **Evidence:** OpenSpec's most-cited namespace criticism: "Why `/opsx:*`? This is awkward, hard to remember because 'opsx' is not 'openspec', so I have to take a minute to think about what I'm writing"; spec-coding.dev warns that tracked tools "ship new releases every few weeks, so treat the command names as current rather than permanent."
- **Requirement:** Command namespaces must be consistent with the tool name; every command must have `--help` documentation. **Unified deprecation policy (adherence is a project commitment, PG-1):** deprecation notices must appear at least one minor version before removal, and deprecated commands/aliases must remain functional through at least one major version. Every breaking change must ship with a migration guide.

  Division of verification: the acceptance criteria below verify **per-release product behavior** (an old name remains functional in the release following a rename). Longitudinal adherence across the project's release history is a project commitment verified under PG-1.
- **Acceptance criteria:**
  - Renamed commands keep old names functional through one major version, emitting deprecation warnings
  - Every command documents usage and examples via `--help`
  - Release notes for breaking changes link a migration guide

#### FR-6.7: Cloud and SaaS Agnostic

The tool itself must not require any specific cloud, SaaS, or hosting; the tool's own operations must be network-independent. Network needs of the AI assistant are the assistant's concern, not a tool lock-in.

- **Evidence:** Kiro's lock-in is rated "high — Kiro IDE + Claude Sonnet only"; the r1 review extends vendor-independence beyond AI agent and IDE to cloud: "the tool must not dictate a specific AI agent, IDE, or cloud." The v1.2 review notes the original formulation ("full workflow with zero network dependency") was unachievable because implementation is typically performed by cloud-based assistants.
- **Requirement:** All tool-native operations (spec authoring, validation, archive, orchestration bookkeeping, local dashboard, drift detection) must complete with no outbound network from the tool itself. The tool must function with any assistant, local or cloud; no feature may require a specific cloud provider account or hosted service. Any hosted features (team dashboard, cross-repo sync) must be optional add-ons with local alternatives or graceful degradation.
- **Acceptance criteria:**
  - **Offline test setup:** a test harness blocks the tool process's egress while permitting the assistant's. On Linux (the reference CI environment) this is a dedicated network namespace or egress-blocking policy applied to the tool process; on other platforms, equivalent mechanisms (e.g., pf rules on macOS, Windows Firewall rules) are acceptable — the invariant is "tool egress blocked, assistant egress permitted." All tool-native operations must complete under this harness
  - The tool works identically with a local assistant and a cloud assistant
  - No feature requires a specific cloud provider account; hosted features degrade cleanly with notice

#### FR-6.8: Secure Community Marketplace

The community schema/skill marketplace must enforce signing, verification, permission disclosure, and sandboxed execution.

- **Evidence:** OpenSpec's community schema catalog (which lists `superpowers-bridge`) demonstrates the marketplace pattern; the v1.1 review flags that community skills/schemas are executable content (code and prompts) and require signing, verification, sandboxing, and a review policy.
- **Requirement:** Marketplace items must be cryptographically signed and verified at install (unsigned items refuse to install by default); installs must disclose requested permissions; skills must execute sandboxed with least privilege — no network or filesystem access beyond declared scopes — and scope violations must be blocked and logged; a review policy gates listings.
- **Acceptance criteria:**
  - Unsigned marketplace items cannot be installed under default settings
  - Install-time permission disclosure precedes any grant
  - Sandbox scope violations are blocked and logged
  - Listings carry review status; unreviewed items are labeled as such

---

### 7. Developer Experience

#### FR-7.1: Problem-First Elicitation

The specification interview must understand the problem before proposing technical solutions.

- **Evidence:** Martin Dilger's critique of Spec Kitty: "The third question was already about the tech stack. That confused me. Shouldn't we spend some more time understanding the problem first? Then it came up with a 'domain model' almost immediately... before it had any real grasp of the problem."
- **Requirement:** Elicitation must follow a structured sequence: problem understanding → domain modeling → constraint identification → technical approach. Tech stack questions must not appear before problem understanding is confirmed.

**Acceptance criteria:**
- The elicitation sequence is enforced: technical-approach questions are blocked until problem understanding is recorded
- The session transcript shows the phase of each question
- Attempting to skip ahead (e.g., to tech stack) before confirmation is refused or flagged

#### FR-7.2: Structured Question Flow

Questions must follow logical domain boundaries, not jump arbitrarily between features.

- **Evidence:** Dilger: "The requirements covered a few different functionalities, and the questions came back in arbitrary order, jumping between features with no structure... A business stakeholder would have no idea if they're supposed to answer feature by feature or think about the whole system at once."
- **Requirement:** Questions must be grouped by feature or domain concept; the tool must indicate which feature/domain is being discussed.

**Acceptance criteria:**
- Every question is labeled with the feature or domain it addresses
- The flow completes one feature's questions before opening another, unless the user explicitly switches
- Arbitrary interleaving of features within a single question thread does not occur

#### FR-7.3: Business-Stakeholder Comprehensible Output

Non-technical stakeholders must be able to participate in spec review.

- **Evidence:** Dilger's critique that "a business stakeholder on the other end of that conversation would have no idea" how to engage; SDD positioning for enterprise requires cross-functional participation.
- **Requirement:** Spec output must include a plain-language summary comprehensible to non-technical reviewers; technical details must be clearly separated from business requirements.

**Acceptance criteria:**
- Every spec generates a plain-language summary alongside the technical artifacts
- Business-facing content contains no implementation notation (enforced with FR-2.11)
- A non-technical reviewer can approve or reject requirements from the summary alone

#### FR-7.4: Artifact Volume Control

The tool must not generate excessive markdown files for simple features.

- **Evidence:** Dilger: "We ended up with 46 markdown files after 20 min... Twenty minutes in, you have fifty markdown files. Who is reading all of that? Who is maintaining it?"
- **Requirement:** Maximum artifact count per ceremony level; automatic consolidation when possible; explicit warning when artifact count exceeds threshold.

**Acceptance criteria:**
- Artifact-count limits are defined per ceremony level and enforced
- Exceeding a threshold triggers a warning and a consolidation offer
- A Trivial-ceremony change produces at most the minimal artifact set: one change record, plus inline acceptance criteria where required by the effective strictness profile (FR-1.1, FR-1.4)

#### FR-7.5: Failed-Experiment Recovery

When spec-driven approach fails to produce better results, the tool must support graceful fallback.

- **Evidence:** The dev.to OpenSpec experiment: "The new front-end looked almost identical to the original. Not exactly the premium UI redesign I was hoping for... I removed OpenSpec entirely and created a file called Instructions.md."
- **Requirement:** A "simplified mode" must extract core instructions from failed spec attempts into a minimal format for direct agent execution.

**Acceptance criteria:**
- A single command extracts core instructions from existing spec artifacts into a minimal instruction file
- The extracted file is directly executable by an agent without the tool's workflow
- Extraction preserves the original artifacts for later retrospective (nothing is destroyed)

---

### 8. Maintenance & Evolution

#### FR-8.1: Spec Synchronization on Code Changes

When code changes outside the spec workflow (hotfix, manual edit), specs must be flagged for update.

- **Evidence:** Critical analysis: "What happens when specs and code diverge?... Spec-First Tools: unclear maintenance story, risk of spec drift, may abandon specs after initial development."
- **Requirement:** Git hooks or CI checks must detect code changes without corresponding spec updates and flag for synchronization.

**Acceptance criteria:**
- A code change touching a specced area without a spec delta is flagged by hook or CI
- The flag persists until the spec is synchronized or explicitly waived (with recorded reason)
- Hotfix paths can defer, but not silently skip, synchronization

#### FR-8.2: Retroactive Spec Generation

For existing codebases without specs, the tool must support generating specs from code.

- **Evidence:** OpenSpec's brownfield guidance: "pick something small and real that you were already going to build this week, run `/opsx:explore` on the area you are about to touch so the agent maps how things actually work first."
- **Requirement:** A command to analyze existing code and generate delta specs for the affected area, not the entire codebase.

**Acceptance criteria:**
- The command generates delta specs scoped to the named area/files only
- Generation time and output size scale with the affected area, not the whole repository
- Generated specs are valid per FR-2.8 without manual repair

#### FR-8.3: Ceremony-Level Migration

Projects must be able to change ceremony level without losing history.

- **Evidence:** specs.md's "start where you are" philosophy: "Use Simple for quick specs, FIRE for rapid execution, or AI-DLC for full methodology. No upgrade path required—each flow is designed for different needs."
- **Requirement:** Switching from trivial to standard to critical ceremony must preserve all existing artifacts and add only what the new level requires.

**Acceptance criteria:**
- Changing ceremony level preserves every existing artifact verbatim
- Only the additional artifacts required by the new level are created
- No regeneration or rewriting of prior work occurs

#### FR-8.4: Review-Cycle Narrowing on Rejection

When a work package is rejected and reworked, subsequent review cycles must narrow to the delta, not re-run the full acceptance contract — with a safety valve for newly discovered critical defects, arbitration on non-convergence, and an observable escalation state when arbitration stalls.

- **Evidence:** Spec Kitty issue #3925 (from the project's own dogfooding): "each review pass took 12–22 minutes of wall-clock, most of it re-verifying settled items. By the third pass the marginal signal is close to zero... successive review cycles must narrow, not repeat." The same issue documents the original implement-review skill's cycle counter with escalation to an arbiter after a maximum of three reviews ("max 3 → arbiter").
- **Requirement:** Cycle 1 review covers the full contract; cycle 2 covers feedback items plus the diff since the prior review; cycle 3 covers feedback items only. Prior verified items must be treated as settled unless the delta touches them. **Safety valve:** if any cycle discovers a new critical defect outside the current narrowed scope, the review resets to full-contract coverage of the affected area for one cycle, then re-narrows; the escalation is logged. **Non-convergence:** if feedback items remain unresolved after cycle 3, the mission escalates to arbitration by the accountable owner (routed per FR-2.5 Class B, including its fallback chain) rather than continuing review cycles. **Arbitration SLA:** arbitration carries a configurable response SLA (default: 72 hours). If the arbitrator does not respond within the SLA, the mission enters an **escalation-pending** state: work remains blocked (no unsafe auto-resolution), the state is distinctly flagged and surfaced in observability (FR-4.2, dashboard and CLI), and the arbitration route — including its fallback chain — is re-notified on a configurable cadence until resolved.
- **Acceptance criteria:**
  - Cycle 2+ review prompts contain only the delta, prior feedback, and unresolved items
  - Settled items are listed as treated-as-settled without re-verification
  - Safety-valve escalations appear in the mission log with the triggering defect
  - Unresolved feedback after cycle 3 triggers arbitration, not a fourth full review cycle
  - An arbitration unanswered past its SLA surfaces as escalation-pending in the dashboard and CLI, with re-notification of the arbitration route

#### FR-8.5: Automatic Archive of Completed Changes

Completed and merged changes must be archived automatically, with delta specs merged into the canonical spec tree without manual steps.

- **Evidence:** OpenSpec requires an explicit `/opsx:archive` step, creating a risk that completed changes linger unarchived; Spec Kitty's merge command includes cleanup; the r1 review requires automatic archiving of completed changes.
- **Requirement:** Upon merge (or a configurable post-merge trigger), the change folder must be archived, delta specs merged, and the tracker ticket updated — without additional manual invocation. Rejected changes must be archived with reasoning per FR-2.3.
- **Acceptance criteria:**
  - Merge triggers archive, spec merge, and tracker update with no further commands
  - Rejected changes archive with a decision record per FR-2.3
  - Archive is idempotent; re-invocation causes no duplication

#### FR-8.6: Migration Tooling and Pre-Upgrade Checks

Artifact-format changes must ship with automated migrations, and upgrades must be checkable before application.

- **Evidence:** The `superpowers-bridge` documentation warns of version drift: "compatibility baselines of OpenSpec 1.4.1 and Superpowers v5.1.0, while current releases are 1.13.2 and 6.4.1" — combination workflows break silently when components drift; the r1 review requires "predictable updates without breaking changes." (The project-level semantic-versioning commitment is PG-2.)
- **Requirement:** The tool must provide migration scripts for artifact format changes and a pre-upgrade compatibility check that reports required migrations before they are applied. **Migration classes:**
  - **Data-losing migrations** (format changes that drop or transform content): must be reversible, with reversibility verified by a down-migration test before release
  - **Add-only migrations** (introducing new fields/sections): must be idempotent and non-destructive by construction
  - **Intentional-loss migrations** (removal of content whose semantics cannot be reconstructed from any remaining source of truth — e.g., deleting a schema section with no archived representation): irreversible by design; must ship with a deprecation window — the removal lands at least one major version after the deprecation notice, consistent with FR-6.6/PG-1 — and an upgrade warning naming exactly what will be lost and how to back it up; the pre-upgrade check must flag every intentional-loss migration before application
- **Acceptance criteria:**
  - The pre-upgrade check reports required migrations before applying anything
  - Data-losing migrations pass a down-migration test before release; add-only migrations are verified idempotent
  - Intentional-loss migrations are flagged by the pre-upgrade check and carry an upgrade warning naming the loss and a backup path
  - No artifact format change requires manual file editing

---

### 9. Project Governance Commitments (Non-Product Requirements)

The following are commitments about how the project producing the tool is run. They are **not functional requirements of the tool itself** and are labeled separately (PG-*) to avoid mixing product and project levels. Product-facing items formerly in this section now live in FR-6.8 (secure marketplace) and FR-8.6 (migration tooling).

#### PG-1: Transparent Roadmap, Issue Triage, and Deprecation Adherence

- **Evidence:** The r1 review requires a transparent roadmap, regular audits, issue responsiveness, and backward compatibility; the SDD landscape's velocity ("treat the command names as current rather than permanent") makes compatibility guarantees a differentiator for adoption.
- **Commitment:** Publish a public, versioned roadmap; document an issue triage policy with response-time targets; adhere to the unified deprecation policy defined in FR-6.6 (notice at least one minor version ahead, aliases functional through one major version).
- **How verified:** Roadmap and triage policy are publicly accessible; release history demonstrably follows the deprecation policy. (FR-6.6's acceptance criteria verify the per-release behavior; this commitment verifies longitudinal adherence across the release history.)

#### PG-2: Semantic Versioning

- **Evidence:** The r1 review requires "predictable updates without breaking changes"; FR-8.6's migration tooling depends on a versioning contract to know when migrations apply.
- **Commitment:** Follow semantic versioning; breaking changes occur only in major versions and always ship with migrations (FR-8.6) and a migration guide (FR-6.6).
- **How verified:** Release history conforms to semver; no breaking change appears in a minor or patch release.

#### PG-3: Community Contribution and Real-World Evidence

- **Evidence:** Spec Kitty's ~1.7k-star adoption with sparse independent review illustrates the cost of weak community evidence; the v1 review requires community influence on development and examples of real implementations.
- **Commitment:** Maintain public contribution guidelines; curate a list of documented production adoptions; provide channels for community influence on the roadmap.
- **How verified:** Contribution guidelines exist and are followed; the adoption list contains verifiable cases; roadmap changes reference community input.

---

## Non-Functional Requirements

### NFR-1: Performance
- Spec generation for standard ceremony level must complete in <2 minutes
- Drift detection on PR must complete in <30 seconds
- Local dashboard: the default (paginated) view must render in <2 seconds and per-page navigation in <1 second, for any number of active missions; listing cost is bounded by page size, not mission count

### NFR-2: Reliability
- No data loss on session interruption; all state recoverable from git
- Graceful degradation when AI assistant is unavailable (manual spec editing)
- Offline mode: core operations (spec authoring, validation, archive, and the **local** dashboard) must function with no network connectivity. The **team** dashboard (cross-repo aggregation, FR-4.2) is networked and optional; its unavailability must not affect local operation. Network-dependent features (tracker sync, telemetry) must fail soft and queue

### NFR-3: Security and Privacy
- No secrets in spec files (automatic scanning)
- Local-first: no data leaves the repository without explicit opt-in
- Audit trail for all agent actions
- Opt-in consent for telemetry and sync must be **per integration** (see FR-4.3), stored as a reviewable file in the repository, visible in code review, and revocable
- A published privacy policy must document every network call the tool can make
- A configuration switch must disable all network activity ("network kill switch") without degrading local functionality. **Precedence:** the kill switch overrides all per-integration opt-ins (FR-4.3), halting opted-in sync as well; consent configurations are preserved unchanged and take effect again when the kill switch is lifted

### NFR-4: Extensibility
- Plugin architecture for custom skills, schemas, and integrations
- Documented API for programmatic interaction
- Community schema marketplace (per FR-6.8 security requirements)

### NFR-5: Lightweight Installation and Startup
- Installation must not require heavyweight runtimes beyond a single standard package manager
- CLI cold start must be <1 second for `--version` and <3 seconds for `init`
- No daemon or background service required for core operation

**Evidence:** spec-compare lists Spec Kitty's "Python dependency (pip install) vs. Node-based alternatives" as a limitation; the r1 review requires "installation without heavy runtimes, fast startup."

---

## What This Tool Explicitly Avoids

Based on documented weaknesses across all researched tools and the requirements reviews (r1, v1.1–v1.4 reviews):

| Avoided Pattern | Source Evidence | Mitigation |
|---|---|---|
| Fixed process weight regardless of task size | BMAD "30+ minute workflow for button color"; Spec Kitty "worktree overhead excessive for one-line change" | FR-1.1 ceremony levels |
| Fixed discipline bundle regardless of task style | Superpowers: "bypass it explicitly for trivia" as the only escape hatch; r1 review requires profiles from vibe to strict | FR-1.4 strictness profiles |
| Enforcement-vs-ceremony ambiguity | v1.2 review: strict profile demanded drift detection where Trivial skips spec generation — undefined referent, checkpoint contradiction | FR-1.4 precedence rule; FR-1.1 minimal inline artifact |
| Unbounded strict-enforcement overhead at Trivial ceremony | v1.3 review: strict+Trivial demanded drift detection, review gate, and criteria generation inside the <5k Trivial budget with no justification or fallback | FR-1.4 strict enforcement allowance (≤5k, itemized per FR-5.4) |
| Infeasible bounds at ceremony extremes | v1.4 review: 15% of the Trivial budget = 750 tokens — below any feasible context package; governance inheritance left unbounded entirely | FR-3.3 total-injection cap: max(2k tokens, 15% of effective budget); digest-form inheritance |
| Ceremony baselines undefined for non-default profiles | v1.4 review: FR-1.1 column covered balanced only; vibe unspecified | FR-1.1 baselines apply to vibe & balanced; strict adds the allowance |
| Silently unsafe profile combinations | v1.4 review: vibe + Critical permitted with all disciplines advisory and no warning | FR-1.4 acknowledgment-gated warning; ceremony process gates retained under vibe |
| Spec generation without problem understanding | Spec Kitty asking about tech stack before understanding problem (Dilger) | FR-7.1 problem-first elicitation |
| Markdown file explosion | Spec Kitty "46 markdown files after 20 min" (Dilger) | FR-7.4 artifact volume control |
| Upfront-completeness demands blocking all work | r1 review: context must build iteratively; Spec Kit's NEEDS CLARIFICATION as the positive pattern | FR-2.10 progressive elaboration |
| Pseudocode-laden specs unreadable by stakeholders | r1 review: "Markdown + schemas, but without sliding into pseudocode"; Dilger's stakeholder critique | FR-2.11 no pseudocode in business-facing specs |
| Confirmatory-only review | Superpowers "self-review is confirmatory... does not attempt to break the plan" | FR-3.4 adversarial review |
| Token burn on simple tasks | Superpowers "burned through all my max plan"; "simple fixes take literally an hour" | FR-5.1 phase budgets, FR-1.1 trivial mode |
| IDE or vendor lock-in | Kiro "high lock-in risk - Kiro IDE + Claude Sonnet only" | FR-6.1 multi-agent, FR-6.2 repo-native, FR-6.5 IDE-agnostic |
| Cloud/SaaS lock-in or unachievable offline claims | r1 review: the tool must not dictate a specific cloud; v1.2 review: "zero network for full workflow" ignores cloud assistants | FR-6.7 cloud-agnostic (tool ops vs. assistant needs; cross-platform harness) |
| Spec-implementation gap | OpenSpec "only checks that artifacts exist, not that code honors them" | FR-2.2 drift detection, FR-3.4 adversarial review |
| Parallel-change silent conflicts | OpenSpec "one silently dropped the other's scenario" | FR-2.5 conflict classes |
| Deadlocked arbitration when no owner is configured | v1.3 review: FR-2.5 Class B routed to an owner via FR-4.1 with no fallback — archive could block indefinitely | FR-2.5 configurable ownership fallback + explicit blocking error |
| Platform-specific fallbacks | v1.4 review: CODEOWNERS is GitHub/GitLab-specific; absent or different on Bitbucket, Gerrit, self-hosted | FR-2.5 configurable ownership declaration (CODEOWNERS default, equivalent file elsewhere) |
| Lost losing versions in conflicts | v1.4 review: fate of the non-chosen Class B version unspecified | FR-2.5 losing version archived with rationale per FR-2.3 |
| No memory of rejected proposals | OpenSpec "nothing tells a future proposal that an idea was already investigated and turned down" | FR-2.3 rejected-proposal memory |
| Agent YOLO-mode on deviation | Superpowers "blazing through on its own without ever stopping to ask" | FR-3.6 human-in-the-loop interrupts |
| Monolithic all-or-nothing architecture | r1 review: ideal system is a modular ecosystem, not a monolith; each researched tool covers only one layer | P6 modular composition, FR-6.3 bridge support |
| Greenfield-only or brownfield-only support | OpenSpec 3/5 for greenfield ("better suited for modifications"); Spec Kit heavier for trivial modifications | FR-2.1 delta specs + FR-2.6 greenfield mode |
| Unreliable or ambiguous spec validation | r1 review: "no requirement entries parsed" bug class; `openspec validate` is a single point of failure for CI | FR-2.8 regression suite per failure class |
| Shared-state conflicts between parallel worktrees | r1 review: `state.yaml` conflicts across parallel agents; Spec Kitty's worktree-per-work-package instability | FR-2.5 Class C conflict handling |
| Subagents exempt from governance rules | Superpowers bootstrap: "If you were dispatched as a subagent... ignore this skill" | FR-3.3 rule inheritance |
| Untestable acceptance criteria (design goals posing as AC) | v1.2 review: FR-3.3 AC referenced an Open Question | FR-3.3 measurable AC; document convention "every FR carries AC" |
| Unimplementable detection mechanisms | v1.3 review: FR-2.10's "silent resolution is detectable" specified no mechanism for the validator to attribute resolution | FR-2.10 resolution flow with attributed decision record |
| Full-contract re-review on every rejection cycle | Spec Kitty #3925: "each review pass took 12–22 minutes... marginal signal is close to zero" | FR-8.4 review-cycle narrowing with safety valve |
| Unbounded review loops on non-convergence | Spec Kitty #3925 documents the original skill's "max 3 → arbiter" escalation; v1.3 review flags feedback-item ballooning | FR-8.4 post-cycle-3 arbitration |
| Unobservable arbitration delays | v1.4 review: FR-8.4 arbitration had no timeout — indefinite silent block possible | FR-8.4 arbitration SLA + escalation-pending state (FR-4.2) |
| Ambiguous command namespaces | OpenSpec: "Why `/opsx:*`?... awkward, hard to remember" | FR-6.6 naming discipline |
| Inconsistent deprecation policy | v1.1 review: FR-6.6 (one major version) vs FR-9.1 (one minor version) contradiction | FR-6.6 unified policy; adherence via PG-1 |
| Silent breakage on component version drift | superpowers-bridge: baselines OpenSpec 1.4.1 / Superpowers v5.1.0 vs. current 1.13.2 / 6.4.1 | FR-8.6 migration tooling and pre-upgrade checks |
| Untestable migration reversibility ("where feasible") | v1.2 review: "where feasible, reversible" is not an AC | FR-8.6 migration classes |
| Irreversible removals without warning | v1.3 review: intentional data loss uncovered by the two reversibility classes; v1.4 review: deprecated-field example ambiguous | FR-8.6 intentional-loss class (deprecation window + upgrade warning + clarified example) |
| Hidden telemetry or non-reviewable consent | r1 review: consent must be explicit, stored in repo, visible in review | NFR-3 per-integration opt-in consent |
| Kill switch ambiguous against opt-in consent | v1.3 review: unclear whether the kill switch disables only non-opted-in functions | NFR-3 precedence: kill switch overrides all opt-ins, configs preserved |
| Untestable performance claims | v1.4 review: "no unbounded refresh time" is not an AC | NFR-1 paginated render-time bounds |
| Unsecured community marketplace | v1.1 review: community skills/schemas are executable content requiring signing and sandboxing | FR-6.8 marketplace security |
| Mixing product requirements with project governance | v1.2 review: former Section 9 conflated tool features with project practices | Section 9 relabeled non-product (PG-1–PG-3); product items moved to FR-6.8, FR-8.6 |

---

## Success Criteria

An implementation of these requirements would be successful if:

1. **Independent comparison win:** It scores ≥4/5 across all use cases in a comparison like [ranthebuilder.cloud's methodology](https://ranthebuilder.cloud/blog/i-tested-three-spec-driven-ai-tools-here-s-my-honest-take), with no use case scoring below 3/5.

2. **Token efficiency:** Controlled comparison shows ≥10% token reduction vs. Superpowers on non-trivial tasks, with trivial tasks costing no more than stock agent without the tool **under the balanced or vibe strictness profile**. (The strict profile at Trivial deliberately purchases enforcement within its bounded allowance, FR-1.4, and is exempt from the stock-agent parity bound. **"Stock agent" baseline:** the same assistant executing the same task from the issue or prompt alone, with no spec-workflow artifacts — the control condition used in controlled comparisons such as MCP.Directory's Superpowers evaluation.)

3. **Longitudinal validation:** A 4+ month study with multiple engineers (like the [OpenSpec simulation study](https://medium.com/@vinodh.thiagarajan/simulating-a-software-team-to-study-spec-driven-development-using-openspec-5d2195fb2a37)) shows spec-implementation gap <10% and no spec drift on actively developed areas.

4. **Adoption friction:** New team onboarding to productive use in <1 day (like specs.md's "Establish an SDD Workflow in One Day" claim, but validated).

5. **Community validation:** ≥1k GitHub stars within 6 months with substantive independent reviews (not just vendor documentation), and a verifiable adoption list per PG-3.

6. **Modular adoption:** Individual layers can be adopted independently and combined with existing tools (OpenSpec, Superpowers) via bridges without duplicate artifacts — validated by at least two documented production combinations.

---

## Open Questions

These requirements leave several questions unresolved that would need design decisions:

1. ~~**Single tool vs. combination?**~~ **Resolved in v1.1:** P6 adopts modular composition as the primary architecture. The remaining boundary question is covered by Q2.

2. **Governance layer ownership?** Spec Kitty's governance (Charter, Decision Moments) is tightly coupled to its workflow. Can governance be a standalone layer applicable to any SDD tool?

3. **Auto-trigger reliability?** Superpowers' auto-triggering works because of its bootstrap enforcement ("IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE"). Can this be achieved without the token cost of the bootstrap? **Scope:** this question concerns the *enforcement mechanism for skill triggering in the main session*; measurement of the trigger rate is defined in FR-3.1. (See Q6 for the parallel subagent-side question.)

4. **Spec-as-source viability?** Tessl's "spec-as-source" approach (specs ARE the source, code auto-generates) is unproven with non-deterministic LLMs. Should the ideal tool support this as an optional mode?

5. **Cross-repo planning?** OpenSpec's "Stores" feature (beta) addresses planning that spans multiple repos. How essential is this for the ideal tool's initial release?

6. **Rule inheritance without bootstrap cost?** FR-3.3 requires subagents to inherit governance rules, but Superpowers' enforcement mechanism (the always-loaded bootstrap) is exactly what its documentation tells subagents to skip. Can rules be injected into subagent prompts without the recurring token cost of a full bootstrap? **Scope:** this question concerns the *injection mechanism for the subagent context package*, including how far the digest-form inheritance of FR-3.3 can be compressed. Q3 and Q6 are parallel applications of the same underlying problem — cheap enforcement without an always-loaded bootstrap — to two contexts with different constraints (main-session skill triggering vs. subagent rule inheritance); they are kept separate because the solutions may differ.

---

## Relationship to Existing Tools

| Existing Tool | What the Ideal Tool Inherits | What It Improves Upon |
|---|---|---|
| **OpenSpec** | Delta specs, brownfield-first, archive mechanism, multi-tool support | Adds drift detection, conflict classes with platform-configurable arbitration fallback, rejected-proposal memory, spec-implementation verification, progressive elaboration |
| **Superpowers** | Auto-triggered skills, subagent isolation, TDD enforcement, adversarial review direction, systematic debugging | Adds ceremony levels, strictness profiles with bounded enforcement allowance, token budgets, context-clearing guidance, trivial-task bypass, rule inheritance for subagents |
| **Spec Kitty** | Governance layer, Teamspace observability, tracker integration, Decision Moments | Adds problem-first elicitation, artifact volume control, review-cycle narrowing with observable arbitration; avoids markdown explosion |
| **specs.md** | Pluggable flows, adaptive ceremony, Ideation phase, monorepo support | Adds independent validation, longitudinal evidence, community adoption |
| **GitHub Spec Kit** | Constitution framework, spec-to-code traceability, NEEDS CLARIFICATION unknowns pattern | Adds fluid iteration, delta format, brownfield optimization |
| **BMAD** | Elicitation quality, course-correction workflows | Reduces ceremony for non-enterprise use, eliminates 21-agent overhead for standard tasks |

**Composition mapping (per r1 review and P6):** the ideal system composes rather than replaces — OpenSpec as the lightweight change-management layer, Superpowers as the execution-discipline layer, Spec Kitty as the parallel-orchestration and governance layer, and Spec Kit/specs.md as the strict-specification layer for complex projects — unified by shared configuration, a common API, and git-native storage.

---

## Stabilization Note (v2.0)

Per the v1.4 review's recommendation, this revision folds the targeted v1.5 edits into a single frozen baseline. The document is now designated the **stable baseline for architectural design and MVP decomposition**. Subsequent changes are made via **change proposals** — dated, scoped entries stating the motivation, the affected FR/NFR/PG identifiers, and the impact on acceptance criteria and cross-references — rather than through further full-text revisions. Open Questions 2–6 remain the designated mechanism for deferring design decisions without destabilizing the baseline.

---

*Document created: 2026-10-02 (v1)*
*Revised: 2026-10-02 (v1.1) — merged alternative requirements review r1*
*Revised: 2026-10-02 (v1.2) — applied machine review of v1.1*
*Revised: 2026-10-02 (v1.3) — applied machine review of v1.2*
*Revised: 2026-10-02 (v1.4) — applied machine review of v1.3*
*Revised: 2026-10-02 (v2.0, stable baseline) — applied machine review of v1.4; v1.5 targeted edits folded in; document frozen*
*Derived from: [spec-tools-research.md](./spec-tools-research.md), requirements review r1, and machine reviews of v1.1–v1.4*
*Status: Stable baseline (v2.0) — requirements specification for hypothetical ideal tool; not implemented; changes via change proposals*
