# Requirements for an Ideal Spec-Driven Development Tool

## Purpose

This document defines requirements for a hypothetical tool that combines the strengths of the researched spec-driven development (SDD) tools while avoiding their documented weaknesses. Each requirement traces to specific evidence from the [spec-tools research document](./spec-tools-research.md).

**Tools analyzed:** specs.md, OpenSpec, obra/superpowers, Spec Kitty, GitHub Spec Kit, BMAD, Kiro, Tessl, GSD.

**Revision history:**
- v1 (2026-10-02): Initial requirements derived from spec-tools research.
- v1.1 (2026-10-02): Merged alternative requirements review r1. Added P6 (modular composition), FR-2.6–FR-2.9, FR-3.3 rule-inheritance clarification, FR-4.6, FR-5.5, FR-6.5–FR-6.6, FR-8.4–FR-8.5, Section 9 (project governance and maturity), NFR-5, strengthened NFR-2/NFR-3, expanded avoided-patterns table. Resolved Open Question 1 in favor of modular composition.

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
- **Requirement:** Automated spec-compliance verification must run on every non-trivial change.

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

| Level | Checkpoints | Use Cases | Token Budget Target |
|---|---|---|---|
| **Trivial** | 0 | Bug fixes with clear repro, config changes, typo fixes, documentation updates | <5k tokens overhead |
| **Standard** | 1-2 | Feature additions, refactors, API endpoints | <20k tokens overhead |
| **Critical** | Full | Security changes, data model changes, cross-service work | <50k tokens overhead |

**Acceptance criteria:**
- User can specify ceremony level via single flag or config
- Tool auto-detects complexity and suggests level (user can override)
- Trivial mode skips spec generation entirely for tasks under a configurable threshold
- Critical mode requires spec review before implementation begins

**Traces to:** specs.md FIRE flow adaptive checkpoints; OpenSpec's "skip it for a typo fix"; Superpowers' "bypass it explicitly for trivia."

#### FR-1.2: Iterative Refinement Without Restart

The tool must allow mid-feature course correction without discarding completed work.

- **Evidence:** BMAD scores 5/5 for "Mid-feature course correction" while Spec Kit scores 2/5; OpenSpec allows editing any artifact at any time with no phase gates; SDD critical analysis notes "agents over-apply or misinterpret instructions" requiring correction.
- **Requirement:** Modifying a spec mid-implementation must trigger delta propagation to affected tasks, not a full restart.

#### FR-1.3: Exploratory Mode

The tool must support exploratory/spike work without forcing premature specification.

- **Evidence:** Superpowers criticism notes "you're exploring, not building... spikes, prototypes, and 'what does this codebase even do' sessions fight the plan-first structure"; specs.md's Ideation Flow (Spark → Flame → Forge) exists specifically for this.
- **Requirement:** An exploratory mode must produce concept briefs, not implementation specs, and must not count toward project spec debt.

---

### 2. Specification Management

#### FR-2.1: Delta-Based Specs

Specifications must use delta format (ADDED, MODIFIED, REMOVED) rather than full rewrites.

- **Evidence:** OpenSpec's delta format is purpose-built for modifications and won independent comparison for specification quality (4/5) vs Spec Kit's 2/5; critical analysis notes "Spec-Kit requires `/speckit.clarify` workaround, not optimized for small changes."
- **Requirement:** Every spec change must express only what is changing, with automatic merge into the canonical spec tree upon archive.

#### FR-2.2: Spec Drift Detection

The tool must detect and alert when implementation diverges from specification.

- **Evidence:** Critical analysis identifies "spec drift over time" as an unresolved question; OpenSpec's `/opsx:verify` exists specifically for this but requires explicit invocation; the spec-implementation gap is "the most cited failure mode."
- **Requirement:** Automated drift detection must run on every PR, comparing implementation against spec acceptance criteria.

#### FR-2.3: Rejected-Proposal Memory

The tool must remember declined proposals to prevent re-proposing rejected ideas.

- **Evidence:** OpenSpec's documentation acknowledges `/opsx:archive` has "no dedicated status for a declined change, so nothing tells a future proposal that an idea was already investigated and turned down."
- **Requirement:** Declined changes must be archived with reasoning and be searchable by future proposals.

#### FR-2.4: Spec Verbosity Control

The tool must enforce spec length limits appropriate to change scope.

- **Evidence:** OpenSpec's most-cited complaint: "The AI generates way more spec than I need... an agent can turn a thirty-minute feature into an 800-line spec"; the 50KB context limit forces some discipline but "delta specs themselves have no hard limit."
- **Requirement:** Configurable spec size limits per ceremony level; automatic flagging when specs exceed thresholds; agent must justify why a spec exceeds the limit.

#### FR-2.5: Parallel-Change Conflict Resolution

The tool must handle multiple in-flight changes touching the same requirement or the same shared state.

- **Evidence:** OpenSpec documented edge case: "Two changes touched the same requirement and one silently dropped the other's scenario... archiving applies a MODIFIED delta as a whole-block replace keyed by requirement name." The r1 review additionally flags conflicts in shared state files (e.g., `state.yaml`) when parallel agents run in separate worktrees; Spec Kitty's original worktree-per-work-package strategy was itself unstable enough to be replaced in v3.1.0.
- **Requirement:** Concurrent modifications — whether to the same requirement or to shared state files across parallel worktrees — must be detected before merge/archive, with an explicit conflict-resolution workflow: automatic where safe, semi-automatic with human confirmation otherwise.

#### FR-2.6: Greenfield Spec Generation

The tool must support full-spec generation for new systems, not only delta changes to existing ones.

- **Evidence:** Spec Kit is rated 5/5 for greenfield work ("Constitution-driven governance... purpose-built for greenfield") while OpenSpec scores 3/5 ("lightweight, better suited for modifications than greenfield"); specs.md targets both greenfield and brownfield across its flows; the r1 review requires explicit support for both.
- **Requirement:** A greenfield mode must produce complete requirement, design, and task specifications from a project brief, while reusing the same artifact formats as brownfield delta specs so projects can transition between modes without migration.

#### FR-2.7: Spec Formality Spectrum

Specifications must support a spectrum of formality, from lightweight notes to formal requirement language, within a single source of truth.

- **Evidence:** OpenSpec delta specs use formal SHALL-language scenarios ("The app SHALL let users switch between light and dark themes"); SDD critical analysis notes ongoing confusion about "where functional specs end and technical implementation begins" and inconsistent interpretation across tools; the r1 review requires "levels of detail: from light notes to formal SHALL/MUST requirements."
- **Requirement:** Spec templates must support at least three formality levels — note-style, structured scenario, formal SHALL/MUST with testable acceptance criteria — selectable per requirement and upgradeable in place without rewriting.

#### FR-2.8: Reliable Spec Validation

Spec validation commands must be deterministic and robust; validator failures must never silently pass or produce spurious errors.

- **Evidence:** The r1 requirements review reports validation bugs of the "no requirement entries parsed" class in existing tools; OpenSpec ships `openspec validate` as a core command, making the validator a single point of failure for CI integration.
- **Requirement:** Validation must produce unambiguous pass/fail results with error locations pointing at the offending lines; validation failures must block archive/merge; the validator itself must have a test suite with ≥90% coverage.

#### FR-2.9: Monorepo and Hierarchical Standards

The tool must support monorepositories with nested projects, independent per-module configuration, and no instruction bloat.

- **Evidence:** specs.md's FIRE flow provides "hierarchical standards with module-specific overrides. One project, multiple tech stacks"; OpenSpec's 50KB context cap is a partial mitigation but not a monorepo design; the r1 review explicitly requires nested projects with independent configurations and no "instruction growth."
- **Requirement:** Sub-project configuration must inherit and override repository-level standards; context injected into agents must be scoped to the affected module; adding modules must not increase per-module context cost.

---

### 3. Execution & Quality Enforcement

#### FR-3.1: Contextual Skill Triggering

Discipline skills must trigger automatically based on context, not require explicit invocation.

- **Evidence:** Superpowers' auto-trigger model is praised: "The agent doesn't *decide* to brainstorm; the brainstorming skill triggers because the user mentioned a vague idea"; contrasted with Spec Kit's "human types `/speckit.plan`. Explicit, deterministic."
- **Requirement:** At least 80% of discipline skills must auto-trigger; users must be able to force-trigger any skill explicitly.

#### FR-3.2: Mandatory TDD (Configurable)

Test-Driven Development must be enforced by default for standard and critical ceremony levels, with opt-out for trivial.

- **Evidence:** Superpowers' "Iron Law" of TDD is its defining characteristic: "No production code without a failing test first"; a controlled comparison found better output quality on non-trivial tasks with TDD enforcement.
- **Requirement:** TDD enforcement must be on by default, configurable per-project and per-task, with automatic deletion of implementation code written before tests.

#### FR-3.3: Subagent Isolation with Rule Inheritance

Each implementation task must execute in an isolated context, but subagents must inherit the governance rules and engineering constraints of the parent session.

- **Evidence:** Superpowers' subagent-driven development is called "a brilliant solution to context collapse. Each subagent only knows about its specific task, preventing it from getting confused by previous steps or unrelated code." However, Superpowers' own `using-superpowers` bootstrap instructs: "If you were dispatched as a subagent to execute a specific task, ignore this skill" — subagents are explicitly exempted from the discipline bootstrap, creating exactly the gap the r1 review identifies (subagents ignoring TDD and other constraints).
- **Requirement:** Tasks must execute in isolated subagents with task-specific context, and subagent results must be reviewed before merging into main context. Subagents must, however, inherit: the project constitution/doctrine, TDD enforcement, scope boundaries, and interrupt triggers. Isolation applies to task context, not to governance rules.

#### FR-3.4: Adversarial Review (Not Confirmatory)

Plan and spec review must attempt to break the plan, not merely confirm completeness.

- **Evidence:** GitHub issue #1803 on Superpowers: "The built-in writing-plans self-review is confirmatory — it checks coverage, types, and placeholders. It does not attempt to break the plan... Claude in 'completion state' produces plans that look correct but contain silent failures."
- **Requirement:** Review phase must explicitly instruct the reviewer to trace intermediate states, run commands mentally, and verify assumptions against the actual codebase.

#### FR-3.5: Context-Clearing Guidance

The tool must indicate when context can safely be cleared between phases.

- **Evidence:** Superpowers issue #655: "It provides no guidance as to when context can safely be cleared (/clear) between phases. From start to finish, it stayed on the same context... 80k tokens of baggage that will degrade the accuracy of future generation?"
- **Requirement:** After each phase completion, the tool must indicate whether context can be cleared and what minimal state must be preserved.

#### FR-3.6: Human-in-the-Loop Interrupts

The agent must pause and ask when implementation deviates from plan or encounters unexpected constraints.

- **Evidence:** Superpowers issue #655: "Claude Code seems to generally be blazing through on its own without ever stopping to ask me stuff if things aren't going according to plan... Claude kept trying to YOLO it by playing around with critical arguments."
- **Requirement:** Configurable interrupt triggers for: plan deviation, external tool errors, assumption invalidation, and scope expansion.

---

### 4. Team Collaboration & Governance

#### FR-4.1: Decision Moments with Stakeholder Routing

Important decisions must be surfaced to relevant stakeholders before agent continues.

- **Evidence:** Spec Kitty's Decision Moments "widen those moments by moving the question into a Slack or Teams thread, so the people who need to participate can weigh in before the agent continues."
- **Requirement:** Decisions affecting deployment policy, domain language, architecture, customer impact, or migration strategy must be routable to accountable/consulted/informed parties.

#### FR-4.2: Cross-Team Observability

Teams must see which agent missions are active across projects, builds, and checkouts.

- **Evidence:** Spec Kitty's Teamspace: "shows which Spec Kitty missions are running in which builds of which projects, what state they are in, and how that work relates back to the team's canonical tracker and repository."
- **Requirement:** A dashboard must show active missions, their state, owner, blockers, and relationship to tracker tickets.

#### FR-4.3: Tracker Authority Preservation

External trackers (Linear, Jira, GitHub Issues) must remain the source of truth for work status.

- **Evidence:** Spec Kitty's design: "a developer can pull a ticket from Linear or Jira into the Spec Kitty CLI and turn it into a full mission... While the work is being implemented, Spec Kitty keeps the ticket updated so the team's normal tracker remains useful."
- **Requirement:** Two-way sync with at least Linear, Jira, and GitHub Issues; tracker status must update automatically as agent work progresses.

#### FR-4.4: Living Project Memory

The tool must maintain a searchable, durable record of decisions, specs, and evidence.

- **Evidence:** Spec Kitty's `kitty-specs` wiki: "specs, plans, evidence, review trails, and Decision Moment ADRs... not just ceremony. They are a living wiki of how the software is being changed"; compared to Karpathy's advocacy for "LLM-maintained Markdown knowledge bases."
- **Requirement:** All decisions, specs, plans, and review results must be stored as versioned, searchable, linked artifacts in the repository.

#### FR-4.5: Onboarding and Context Recovery

New team members and fresh sessions must be able to recover project context from artifacts.

- **Evidence:** SDD critical analysis notes "long-term maintenance: unclear maintenance story, risk of spec drift, may abandon specs after initial development"; OpenSpec's archive mechanism creates durable current-state description.
- **Requirement:** A single command must generate a comprehensive project context summary from stored artifacts, sufficient for a new session or team member to understand current state.

#### FR-4.6: Traceability Reporting

The tool must provide queryable traceability: what was built, by whom (which agent or human), and on the basis of which requirements and decisions.

- **Evidence:** Spec Kitty positions itself as providing "an auditable delivery record from first decision to merge"; the SDD critical analysis lists "who maintains specifications during bug fixes?" among unresolved questions; the r1 review requires visible "who/what/why" metrics.
- **Requirement:** Every merged change must link to the originating requirement(s), the decision records that shaped it, the implementing agent/session, and the review verdicts. A single command must produce a traceability report for any artifact or requirement.

---

### 5. Token & Context Efficiency

#### FR-5.1: Phase-Based Token Budgets

Each phase must have configurable token budgets with alerts on overrun.

- **Evidence:** Superpowers' optimization history: v5.0.6 removed subagent review loops after "~25 minutes of overhead with no measurable quality gain"; v6.0.0 achieved "up to 50% faster and up to 60% cheaper"; yet "no amount of optimization makes a design interview free."
- **Requirement:** Token usage must be tracked per phase; alerts must fire when budget exceeded; tool must suggest which phase to simplify.

#### FR-5.2: Progressive Disclosure

Only relevant context should be loaded at each phase, not the full project state.

- **Evidence:** Superpowers' progressive disclosure: "~100 tokens per skill for always-loaded metadata, skill bodies under 5k tokens loaded only on trigger"; Anthropic's documented approach.
- **Requirement:** Context injection must be scoped to current task; irrelevant project state must not consume context window.

#### FR-5.3: Worktree Isolation with Cleanup

Parallel work must use isolated worktrees with automatic cleanup on merge.

- **Evidence:** Spec Kitty pioneered "built-in git worktree support among SDD tools... Automatic worktree creation per feature, Parallel feature isolation without branch switching, Automated cleanup on merge"; Superpowers' "Using Git Worktrees: Isolated branches with verified test baselines."
- **Requirement:** Worktree management must be automatic, with configurable strategy (per-feature or per-swim-lane) and cleanup on completion.

#### FR-5.4: Cost Reporting

The tool must report token and time cost per mission, phase, and task.

- **Evidence:** The "hidden costs of spec-driven development" analysis identifies six cost types teams forget to track; MCP.Directory's controlled comparison found "runs 9% cheaper with 14% fewer tokens" on non-trivial tasks.
- **Requirement:** Post-mission reports must include: total tokens, tokens per phase, time elapsed, and comparison to project baseline.

#### FR-5.5: Context Caching and Summarization

The tool must reduce token consumption through caching and summarization of previously established context.

- **Evidence:** Superpowers v6.0.0 achieved "up to 50% faster and up to 60% cheaper" partly by pre-generating review inputs; progressive disclosure keeps dormant skills cheap; the r1 review explicitly requires "selective context loading, caching, summarization."
- **Requirement:** Phase outputs must be cached and reused across sessions where unchanged; long-running context must be summarizable into compact form for downstream phases; cache invalidation must be automatic on spec or plan change.

---

### 6. Integration & Portability

#### FR-6.1: Multi-Agent Support

The tool must work with at least 10 AI coding assistants without lock-in.

- **Evidence:** OpenSpec supports "30+ assistants including Claude Code, Cursor, GitHub Copilot, Gemini CLI, Codex, Kiro, and OpenCode"; Superpowers has first-class plugin packages for multiple harnesses; Kiro's lock-in is rated "high" risk.
- **Requirement:** Support for Claude Code, Cursor, GitHub Copilot, Gemini CLI, Codex, OpenCode, Windsurf, and extensible plugin architecture for others.

#### FR-6.2: Repository-Native Storage

All artifacts must live in the repository as version-controlled files.

- **Evidence:** Spec Kitty: "specs, plans, work packages, acceptance criteria, decision records, review state, and merge status become repo-native artifacts, not ephemeral chat"; OpenSpec: "commit the whole `openspec/` folder to git."
- **Requirement:** No external database or service required for core functionality; all state recoverable from git.

#### FR-6.3: Bridge/Combination Support

The tool must support combination with complementary tools via documented schemas or bridges.

- **Evidence:** The `superpowers-bridge` schema for OpenSpec redirects Superpowers output into OpenSpec change folders; spec-coding.dev recommends "one planning tool (OpenSpec for fluid, brownfield changes, Spec Kit for a stricter lifecycle) plus Superpowers for execution."
- **Requirement:** Export/import mechanisms for spec artifacts; documented combination patterns with at least Superpowers and OpenSpec.

#### FR-6.4: CLI-First with Optional Dashboard

Core functionality must work entirely from CLI; dashboards are optional enhancements.

- **Evidence:** OpenSpec is "a free, open-source CLI... does not write code by itself or replace Claude Code, Codex, Cursor, or GitHub Copilot"; Spec Kitty's dashboard is "visual kanban boards tracking work progress" but CLI-first.
- **Requirement:** All operations must be scriptable; dashboard must be an optional layer, not a dependency.

#### FR-6.5: IDE-Agnostic Operation

The tool must work from any editor or no editor at all; no functionality may require a specialized IDE.

- **Evidence:** specs.md's comparison matrix rates Kiro's IDE lock-in as "High — Kiro IDE + Claude Sonnet only" while rating all CLI-based tools "None (any IDE)"; the r1 review requires IDE-agnostic operation explicitly.
- **Requirement:** All features must be accessible via CLI and standard file formats; IDE extensions, where offered, must be additive conveniences and never the only path to a capability.

#### FR-6.6: Documentation and Command Naming Discipline

Documentation must include examples and migration guides; command names must be unambiguous and conflict-free.

- **Evidence:** OpenSpec's most-cited namespace criticism: "Why `/opsx:*`? This is awkward, hard to remember because 'opsx' is not 'openspec', so I have to take a minute to think about what I'm writing"; spec-coding.dev warns that tracked tools "ship new releases every few weeks, so treat the command names as current rather than permanent."
- **Requirement:** Command namespaces must be consistent with the tool name; every command must have `--help` documentation; every breaking change must ship with a migration guide; command renames must maintain deprecated aliases for at least one major version.

---

### 7. Developer Experience

#### FR-7.1: Problem-First Elicitation

The specification interview must understand the problem before proposing technical solutions.

- **Evidence:** Martin Dilger's critique of Spec Kitty: "The third question was already about the tech stack. That confused me. Shouldn't we spend some more time understanding the problem first? Then it came up with a 'domain model' almost immediately... before it had any real grasp of the problem."
- **Requirement:** Elicitation must follow a structured sequence: problem understanding → domain modeling → constraint identification → technical approach. Tech stack questions must not appear before problem understanding is confirmed.

#### FR-7.2: Structured Question Flow

Questions must follow logical domain boundaries, not jump arbitrarily between features.

- **Evidence:** Dilger: "The requirements covered a few different functionalities, and the questions came back in arbitrary order, jumping between features with no structure... A business stakeholder would have no idea if they're supposed to answer feature by feature or think about the whole system at once."
- **Requirement:** Questions must be grouped by feature or domain concept; the tool must indicate which feature/domain is being discussed.

#### FR-7.3: Business-Stakeholder Comprehensible Output

Non-technical stakeholders must be able to participate in spec review.

- **Evidence:** Dilger's critique that "a business stakeholder on the other end of that conversation would have no idea" how to engage; SDD positioning for enterprise requires cross-functional participation.
- **Requirement:** Spec output must include a plain-language summary comprehensible to non-technical reviewers; technical details must be clearly separated from business requirements.

#### FR-7.4: Artifact Volume Control

The tool must not generate excessive markdown files for simple features.

- **Evidence:** Dilger: "We ended up with 46 markdown files after 20 min... Twenty minutes in, you have fifty markdown files. Who is reading all of that? Who is maintaining it?"
- **Requirement:** Maximum artifact count per ceremony level; automatic consolidation when possible; explicit warning when artifact count exceeds threshold.

#### FR-7.5: Failed-Experiment Recovery

When spec-driven approach fails to produce better results, the tool must support graceful fallback.

- **Evidence:** The dev.to OpenSpec experiment: "The new front-end looked almost identical to the original. Not exactly the premium UI redesign I was hoping for... I removed OpenSpec entirely and created a file called Instructions.md."
- **Requirement:** A "simplified mode" must extract core instructions from failed spec attempts into a minimal format for direct agent execution.

---

### 8. Maintenance & Evolution

#### FR-8.1: Spec Synchronization on Code Changes

When code changes outside the spec workflow (hotfix, manual edit), specs must be flagged for update.

- **Evidence:** Critical analysis: "What happens when specs and code diverge?... Spec-First Tools: unclear maintenance story, risk of spec drift, may abandon specs after initial development."
- **Requirement:** Git hooks or CI checks must detect code changes without corresponding spec updates and flag for synchronization.

#### FR-8.2: Retroactive Spec Generation

For existing codebases without specs, the tool must support generating specs from code.

- **Evidence:** OpenSpec's brownfield guidance: "pick something small and real that you were already going to build this week, run `/opsx:explore` on the area you are about to touch so the agent maps how things actually work first."
- **Requirement:** A command to analyze existing code and generate delta specs for the affected area, not the entire codebase.

#### FR-8.3: Ceremony-Level Migration

Projects must be able to change ceremony level without losing history.

- **Evidence:** specs.md's "start where you are" philosophy: "Use Simple for quick specs, FIRE for rapid execution, or AI-DLC for full methodology. No upgrade path required—each flow is designed for different needs."
- **Requirement:** Switching from trivial to standard to critical ceremony must preserve all existing artifacts and add only what the new level requires.

#### FR-8.4: Review-Cycle Narrowing on Rejection

When a work package is rejected and reworked, subsequent review cycles must narrow to the delta, not re-run the full acceptance contract.

- **Evidence:** Spec Kitty issue #3925 (from the project's own dogfooding): "each review pass took 12–22 minutes of wall-clock, most of it re-verifying settled items. By the third pass the marginal signal is close to zero... successive review cycles must narrow, not repeat."
- **Requirement:** Cycle 1 review covers the full contract; cycle 2 covers feedback items plus the diff since the prior review; cycle 3 covers feedback items only. Prior verified items must be treated as settled unless the delta touches them.

#### FR-8.5: Automatic Archive of Completed Changes

Completed and merged changes must be archived automatically, with delta specs merged into the canonical spec tree without manual steps.

- **Evidence:** OpenSpec requires an explicit `/opsx:archive` step, creating a risk that completed changes linger unarchived; Spec Kitty's merge command includes cleanup; the r1 review requires automatic archiving of completed changes.
- **Requirement:** Upon merge (or a configurable post-merge trigger), the change folder must be archived, delta specs merged, and the tracker ticket updated — without additional manual invocation. Rejected changes must be archived with reasoning per FR-2.3.

---

### 9. Project Governance and Maturity

#### FR-9.1: Transparent Roadmap and Backward Compatibility

The project must publish a roadmap, respond to issues, and maintain backward compatibility within major versions.

- **Evidence:** The r1 review requires a transparent roadmap, regular audits, issue responsiveness, and backward compatibility; the SDD landscape's velocity ("treat the command names as current rather than permanent") makes compatibility guarantees a differentiator for adoption.
- **Requirement:** Public roadmap; documented issue triage policy; deprecation notices at least one minor version before removal.

#### FR-9.2: Versioned Migrations Without Breaking Changes

Upgrades must be predictable, with automated migrations where formats change.

- **Evidence:** The `superpowers-bridge` documentation warns of version drift: "compatibility baselines of OpenSpec 1.4.1 and Superpowers v5.1.0, while current releases are 1.13.2 and 6.4.1" — combination workflows break silently when components drift; the r1 review requires "predictable updates without breaking changes."
- **Requirement:** Semantic versioning; migration scripts for artifact format changes; a pre-upgrade compatibility check that reports required migrations before they are applied.

#### FR-9.3: Community Contribution and Real-World Evidence

The project must support community contribution, maintain a schema/skill marketplace, and surface real-world adoption examples.

- **Evidence:** OpenSpec's community schema catalog (which lists `superpowers-bridge`) demonstrates the pattern; Spec Kitty's ~1.7k-star adoption with sparse independent review illustrates the cost of weak community evidence.
- **Requirement:** Public contribution guidelines; a browsable marketplace or registry for community schemas/skills; a curated list of documented production adoptions.

---

## Non-Functional Requirements

### NFR-1: Performance
- Spec generation for standard ceremony level must complete in <2 minutes
- Drift detection on PR must complete in <30 seconds
- Dashboard refresh must be <1 second for teams with <50 active missions

### NFR-2: Reliability
- No data loss on session interruption; all state recoverable from git
- Graceful degradation when AI assistant is unavailable (manual spec editing)
- Offline mode: core operations (spec authoring, validation, archive, dashboard) must function with no network connectivity; network-dependent features (tracker sync, telemetry) must fail soft and queue

### NFR-3: Security and Privacy
- No secrets in spec files (automatic scanning)
- Local-first: no data leaves the repository without explicit opt-in
- Audit trail for all agent actions
- Opt-in consent for telemetry and sync must be stored as a reviewable file in the repository, visible in code review
- A published privacy policy must document every network call the tool can make
- A configuration switch must disable all network activity ("network kill switch") without degrading local functionality

### NFR-4: Extensibility
- Plugin architecture for custom skills, schemas, and integrations
- Documented API for programmatic interaction
- Community schema marketplace (like OpenSpec's community catalog)

### NFR-5: Lightweight Installation and Startup
- Installation must not require heavyweight runtimes beyond a single standard package manager
- CLI cold start must be <1 second for `--version` and <3 seconds for `init`
- No daemon or background service required for core operation

**Evidence:** spec-compare lists Spec Kitty's "Python dependency (pip install) vs. Node-based alternatives" as a limitation; the r1 review requires "installation without heavy runtimes, fast startup."

---

## What This Tool Explicitly Avoids

Based on documented weaknesses across all researched tools and the r1 requirements review:

| Avoided Pattern | Source Evidence | Mitigation |
|---|---|---|
| Fixed process weight regardless of task size | BMAD "30+ minute workflow for button color"; Spec Kitty "worktree overhead excessive for one-line change" | FR-1.1 ceremony levels |
| Spec generation without problem understanding | Spec Kitty asking about tech stack before understanding problem (Dilger) | FR-7.1 problem-first elicitation |
| Markdown file explosion | Spec Kitty "46 markdown files after 20 min" (Dilger) | FR-7.4 artifact volume control |
| Confirmatory-only review | Superpowers "self-review is confirmatory... does not attempt to break the plan" | FR-3.4 adversarial review |
| Token burn on simple tasks | Superpowers "burned through all my max plan"; "simple fixes take literally an hour" | FR-5.1 phase budgets, FR-1.1 trivial mode |
| IDE or vendor lock-in | Kiro "high lock-in risk - Kiro IDE + Claude Sonnet only" | FR-6.1 multi-agent, FR-6.2 repo-native, FR-6.5 IDE-agnostic |
| Spec-implementation gap | OpenSpec "only checks that artifacts exist, not that code honors them" | FR-2.2 drift detection, FR-3.4 adversarial review |
| Parallel-change silent conflicts | OpenSpec "one silently dropped the other's scenario" | FR-2.5 conflict resolution |
| No memory of rejected proposals | OpenSpec "nothing tells a future proposal that an idea was already investigated and turned down" | FR-2.3 rejected-proposal memory |
| Agent YOLO-mode on deviation | Superpowers "blazing through on its own without ever stopping to ask" | FR-3.6 human-in-the-loop interrupts |
| Monolithic all-or-nothing architecture | r1 review: ideal system is a modular ecosystem, not a monolith; each researched tool covers only one layer | P6 modular composition, FR-6.3 bridge support |
| Greenfield-only or brownfield-only support | OpenSpec 3/5 for greenfield ("better suited for modifications"); Spec Kit heavier for trivial modifications | FR-2.1 delta specs + FR-2.6 greenfield mode |
| Unreliable or ambiguous spec validation | r1 review: "no requirement entries parsed" bug class; `openspec validate` is a single point of failure for CI | FR-2.8 reliable validation |
| Shared-state conflicts between parallel worktrees | r1 review: `state.yaml` conflicts across parallel agents; Spec Kitty's worktree-per-work-package instability | FR-2.5 conflict resolution |
| Subagents exempt from governance rules | Superpowers bootstrap: "If you were dispatched as a subagent... ignore this skill" | FR-3.3 rule inheritance |
| Full-contract re-review on every rejection cycle | Spec Kitty #3925: "each review pass took 12–22 minutes... marginal signal is close to zero" | FR-8.4 review-cycle narrowing |
| Ambiguous command namespaces | OpenSpec: "Why `/opsx:*`?... awkward, hard to remember" | FR-6.6 naming discipline |
| Silent breakage on component version drift | superpowers-bridge: baselines OpenSpec 1.4.1 / Superpowers v5.1.0 vs. current 1.13.2 / 6.4.1 | FR-9.2 versioned migrations |
| Hidden telemetry or non-reviewable consent | r1 review: consent must be explicit, stored in repo, visible in review | NFR-3 privacy requirements |

---

## Success Criteria

An implementation of these requirements would be successful if:

1. **Independent comparison win:** It scores ≥4/5 across all use cases in a comparison like [ranthebuilder.cloud's methodology](https://ranthebuilder.cloud/blog/i-tested-three-spec-driven-ai-tools-here-s-my-honest-take), with no use case scoring below 3/5.

2. **Token efficiency:** Controlled comparison shows ≥10% token reduction vs. Superpowers on non-trivial tasks, with trivial tasks costing no more than stock agent without the tool.

3. **Longitudinal validation:** A 4+ month study with multiple engineers (like the [OpenSpec simulation study](https://medium.com/@vinodh.thiagarajan/simulating-a-software-team-to-study-spec-driven-development-using-openspec-5d2195fb2a37)) shows spec-implementation gap <10% and no spec drift on actively developed areas.

4. **Adoption friction:** New team onboarding to productive use in <1 day (like specs.md's "Establish an SDD Workflow in One Day" claim, but validated).

5. **Community validation:** ≥1k GitHub stars within 6 months with substantive independent reviews (not just vendor documentation).

6. **Modular adoption:** Individual layers can be adopted independently and combined with existing tools (OpenSpec, Superpowers) via bridges without duplicate artifacts — validated by at least two documented production combinations.

---

## Open Questions

These requirements leave several questions unresolved that would need design decisions:

1. ~~**Single tool vs. combination?**~~ **Resolved in v1.1:** P6 adopts modular composition as the primary architecture. The remaining boundary question is covered by Q2.

2. **Governance layer ownership?** Spec Kitty's governance (Charter, Decision Moments) is tightly coupled to its workflow. Can governance be a standalone layer applicable to any SDD tool?

3. **Auto-trigger reliability?** Superpowers' auto-triggering works because of its bootstrap enforcement ("IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE"). Can this be achieved without the token cost of the bootstrap?

4. **Spec-as-source viability?** Tessl's "spec-as-source" approach (specs ARE the source, code auto-generates) is unproven with non-deterministic LLMs. Should the ideal tool support this as an optional mode?

5. **Cross-repo planning?** OpenSpec's "Stores" feature (beta) addresses planning that spans multiple repos. How essential is this for the ideal tool's initial release?

6. **Rule inheritance without bootstrap cost?** FR-3.3 requires subagents to inherit governance rules, but Superpowers' enforcement mechanism (the always-loaded bootstrap) is exactly what its documentation tells subagents to skip. Can rules be injected into subagent prompts without the recurring token cost of a full bootstrap?

---

## Relationship to Existing Tools

| Existing Tool | What the Ideal Tool Inherits | What It Improves Upon |
|---|---|---|
| **OpenSpec** | Delta specs, brownfield-first, archive mechanism, multi-tool support | Adds drift detection, conflict resolution, rejected-proposal memory, spec-implementation verification |
| **Superpowers** | Auto-triggered skills, subagent isolation, TDD enforcement, adversarial review direction | Adds ceremony levels, token budgets, context-clearing guidance, trivial-task bypass, rule inheritance for subagents |
| **Spec Kitty** | Governance layer, Teamspace observability, tracker integration, Decision Moments | Adds problem-first elicitation, artifact volume control, review-cycle narrowing; avoids markdown explosion |
| **specs.md** | Pluggable flows, adaptive ceremony, Ideation phase, monorepo support | Adds independent validation, longitudinal evidence, community adoption |
| **GitHub Spec Kit** | Constitution framework, spec-to-code traceability | Adds fluid iteration, delta format, brownfield optimization |
| **BMAD** | Elicitation quality, course-correction workflows | Reduces ceremony for non-enterprise use, eliminates 21-agent overhead for standard tasks |

**Composition mapping (per r1 review and P6):** the ideal system composes rather than replaces — OpenSpec as the lightweight change-management layer, Superpowers as the execution-discipline layer, Spec Kitty as the parallel-orchestration and governance layer, and Spec Kit/specs.md as the strict-specification layer for complex projects — unified by shared configuration, a common API, and git-native storage.

---

*Document created: 2026-10-02 (v1)*
*Revised: 2026-10-02 (v1.1) — merged alternative requirements review r1*
*Derived from: [spec-tools-research.md](./spec-tools-research.md) and requirements review r1*
*Status: Requirements specification for hypothetical ideal tool; not implemented*
