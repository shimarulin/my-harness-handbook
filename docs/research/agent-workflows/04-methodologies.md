# 04 — Methodologies: Portable Deterministic Development

## Overview

The methodology layer sits between the LLM and the harness. It defines
**what must happen** (phases, gates, roles) independent of **how it's
executed** (which agent, which tool). The same methodology can run on
Claude Code, Pi, OpenCode, or Deep Agents Code through adapters.

## 1. Spec-Driven Development (SDD)

### Core Idea

Before the agent writes code, create a chain of artifacts:
**specification → plan → task list → implementation**. Each stage produces
a Markdown artifact that feeds the next, eliminating ad-hoc prompts.

### GitHub Spec Kit

**Repository**: [github/spec-kit](https://github.com/github/spec-kit)
**Documentation**: [Microsoft Learn: Spec-Driven Development](https://learn.microsoft.com)

GitHub's open-source toolkit for SDD with **38+ integrations** including
Claude Code, Cursor, Copilot, Gemini, Codex, Zed, Kiro.

**Key artifacts**:
- `constitution.md` — project mission, tech stack, roadmap
- `spec.md` — what to build and acceptance criteria
- `plan.md` — how to build it
- `tasks.md` — ordered implementation steps

**How it provides determinism**: SDD doesn't make execution deterministic,
but makes **intent** explicit and verifiable. The agent works with a
contract, not with "understood, will do".

### tiny-spec

**Repository**: [matheusbuniotto/tiny-spec](https://github.com/matheusbuniotto/tiny-spec)

Minimalist alternative: four steps, two agents, no config. A spec is a
short markdown file capturing:
- **What** you're building and why
- **Acceptance criteria** (the gate)
- **Context** your agent needs

### OpenSpec

**Documentation**: [Getting started with OpenSpec](https://sgryphon.gamertheory.net)

Light-weight SDD framework using spec changes (deltas) merged into a central
spec repository. Good for existing code bases.

### Implementation in Workflows

```javascript
// SDD workflow
const spec = await agent({
  type: "spec-writer",
  prompt: "Write spec.md for feature: rate limiting",
  schema: { specPath: "string" }
});

// HITL gate: human reviews spec
const approved = await agent({
  type: "human-reviewer",
  prompt: `Review spec: ${spec.specPath}`,
  gate: "human-approval"
});

if (!approved.passed) return { status: "spec-rejected" };

const plan = await agent({
  type: "planner",
  prompt: `Create plan.md from ${spec.specPath}`
});

const tasks = await agent({
  type: "task-decomposer",
  prompt: `Break plan into tasks.md`
});
```

## 2. Evidence-Gated Lifecycle (Proof-or-Stop)

### Core Idea

Lifecycle states like "tested", "reviewed", "done" are **claims** until
verified by mechanically checkable evidence. The agent can *propose* a
claim but cannot *set* lifecycle state. Transitions require fresh,
code-state-bound, verifiable evidence.

### Proof-or-Stop

**Paper**: [arXiv:2607.14890](https://arxiv.org/abs/2607.14890)
**Repository**: [Proof-or-Stop](https://github.com/Proof-or-Stop)

> "Don't trust the agent — trust the evidence. Lifecycle states like
> *reviewed*, *tested*, and *done* are claims — Proof-or-Stop admits them
> only when fresh, tracked-source-state-bound, mechanically verifiable
> evidence satisfies the gate. No qualifying evidence → repair, degrade
> honestly, or stop. Never advance on the agent's word."

**Key results** (from paper):
- Unattended-loop engine passed 10/10 scenarios with zero false-DONE
- Local-key receipt bundles rejected 18 tamper classes with zero false accepts

### phionyx-pipeline-mcp

**Repository**: [halvrenofviryel/phionyx-pipeline-mcp](https://github.com/halvrenofviryel/phionyx-pipeline-mcp)
**PyPI**: [phionyx-pipeline-mcp](https://pypi.org/project/phionyx-pipeline-mcp)

MCP server implementing three-layer verification:
1. **LLM Declaration** (stochastic): agent says what it changed
2. **Repo Truth** (deterministic): `git diff --name-only` + `git diff -U0`
3. **Deterministic Gate** (decision): produces `pass | regenerate | reject`

**Architecture**: [phionyx.ai/agentic-development/architecture](https://phionyx.ai/agentic-development/architecture)

### Custos Code

**Repository**: [Olivesz/custos-code](https://github.com/Olivesz/custos-code)

Reads the harness-written action log, splits agent report into claims,
and marks each as **confirmed**, **contradicted**, **unwitnessed**,
**unrecorded**, or **qualified**. Contradictions go back to the agent
before it's allowed to stop.

### Implementation in Workflows

```javascript
// Evidence-gated execution
pi.events.on("subagents:completed", async (event) => {
  if (event.type === "implementer") {
    const gitDiff = exec("git diff --name-only");
    const claimedFiles = event.result.changedFiles;
    const unverified = claimedFiles.filter(f => !gitDiff.includes(f));
    
    if (unverified.length > 0) {
      return { status: "evidence-failed", unverified };
    }
  }
});
```

## 3. CIV (Coordinator-Implementor-Verifier)

### Core Idea

Task decomposed by Coordinator into DAG of typed tasks. Implementor executes
with limited toolset. Verifier checks result via tests, linting, type-checking.
Connection between phases is strictly typed (`CIVMessage` schema).

### no-slop-harness

**PyPI**: [no-slop-harness](https://pypi.org/project/no-slop-harness)

> "Deterministic, local-first LLM orchestration framework implementing
> the CIV (Coordinator-Implementor-Verifier) pattern for zero-slop,
> high-fidelity software engineering."

### Key Properties

- **Coordinator**: planning and decomposition tools
- **Implementor**: only `write_file`, `edit_file_ast`, `bash_execute` with
  allowlist
- **Verifier**: tests, linters, type-checkers — returns pass/reject,
  not text
- **Feedback loop**: limited iterations (e.g., 3), then flags for human

### harnessie

**Repository**: [snapsynapse/harnessie](https://github.com/snapsynapse/harnessie)
**Website**: [harnessie.com](https://harnessie.com)

> "Brain-agnostic multi-agent harness" — orchestrator decomposes into task
> packets, workers execute in jailed workspace with allowlisted tools,
> every phase exits through a gate with deterministic checks + independent
> fresh-context verifier.

**Key features**:
- Eight-layer prompt-injection defense
- Hash-chained audit log
- Enforced file ownership
- Contested decisions fan out to adversarial panel

### Implementation in Pi

```yaml
# .pi/agents/coordinator.md
---
name: coordinator
tools: [planning, task_decomposition]
allowed_subagents: implementer, verifier
model: anthropic/claude-sonnet-4-5
---
Decompose tasks into typed CIVMessage objects.
```

```yaml
# .pi/agents/implementer.md
---
name: implementer
tools: [write_file, edit_file, bash]
model: anthropic/claude-haiku-4-5
---
Execute tasks with limited tool access.
```

```yaml
# .pi/agents/verifier.md
---
name: verifier
tools: [bash, lint, test_runner]
model: anthropic/claude-haiku-4-5
---
Run tests, check lint. Return structured pass/reject, not text.
```

## 4. Phased Pipeline with HITL Gates

### Core Idea

Work structured in sequential phases (Spec → Design → Implement → Test →
Review → Security → Release). Each phase has **hard invariants**: phase n
cannot start until phase n-1 recorded end timestamp. Gates are hardcoded
in control plane and cannot be bypassed by prompting.

### ByteDigger

**Repository**: [shtofadhor/bytedigger](https://github.com/shtofadhor/bytedigger)
**Alternative**: [guy-lifshitz/bytedigger](https://github.com/guy-lifshitz/bytedigger)

> "A software factory: a CI that drives a Python state machine through
> the whole SDLC — research, spec, failing tests, implementation, review —
> with TDD at the core and agents as replaceable workers inside. The spec
> compiles into machine-runnable checks, so 'done' is a table of checks
> passing, not anyone's judgment."

**8 phases**: research → spec → failing-tests → implementation →
review → security → release → done

**Anti-gaming lints**:
- `stub-passability`: rejects RED that mocks its own unit under test
- `test-integrity diff guard`: fails on assertion gaming

### Implementation in Workflows

```javascript
const phases = ["research", "spec", "failing-tests", "implementation",
                "review", "security", "release"];
let completed = [];

for (const phase of phases) {
  if (!completed.includes(prev(phase))) {
    throw new Error(`Phase ${phase} blocked: previous incomplete`);
  }
  
  const result = await agent({
    type: phase,
    gate: getPhaseGate(phase)
  });
  
  if (result.status === "passed") completed.push(phase);
  else return { status: "stopped", failedPhase: phase };
}
```

## 5. TDD as Deterministic Anchor

### Core Idea

Failing test is written and independently verified **before** implementation.
The agent cannot declare "done" until the test passes. This creates a
mechanical anchor.

**Source**: [TDD inside the agent loop - theater or actual value?](https://martinfowler.com/articles/exploring-gen-ai/tdd-in-the-agent-loop.html) — Martin Fowler

### Implementation

```javascript
// TDD workflow: RED → validate → GREEN
const redTest = await agent({
  type: "test-writer",
  prompt: "Write failing test for feature",
  // Middleware blocks write_file for implementation
  // until test is written and run (and failed)
});

const testFailed = exec("npm test"); // must fail
if (testFailed.exitCode === 0) {
  return { status: "invalid-red", reason: "test passes without implementation" };
}

const implementation = await agent({
  type: "implementer",
  prompt: "Make the failing test pass",
  gate: "npm test" // must pass now
});
```

## Composition: The Full Methodology Stack

A production methodology combines all five:

```
┌─────────────────────────────────────────────────┐
│           METHODOLOGY (portable layer)           │
├─────────────────────────────────────────────────┤
│ 1. SDD — spec.md → plan.md → tasks.md           │
│    (GitHub Spec Kit / tiny-spec / OpenSpec)     │
├─────────────────────────────────────────────────┤
│ 2. Evidence-Gated — proof-or-stop lifecycle     │
│    (Proof-or-Stop / phionyx / Custos Code)      │
├─────────────────────────────────────────────────┤
│ 3. CIV — Coordinator → Implementor → Verifier   │
│    (no-slop-harness / harnessie)                │
├─────────────────────────────────────────────────┤
│ 4. Phased Pipeline — 8 phases with hard gates   │
│    (ByteDigger pattern)                         │
├─────────────────────────────────────────────────┤
│ 5. TDD — RED → validate → GREEN as anchor       │
│    (mandatory, not optional)                    │
└─────────────────────────────────────────────────┘
```

## Portability Matrix

| Methodology | Claude Code | Pi | OpenCode | Deep Agents |
|-------------|-------------|-----|----------|-------------|
| SDD (Spec Kit) | ✅ Native | ✅ Via CLI | ✅ Via CLI | ✅ Via CLI |
| Evidence-Gated | ✅ MCP | ✅ Extension | ⚠️ Plugin | ✅ Middleware |
| CIV | ⚠️ Config | ✅ Agent types | ⚠️ Config | ✅ Subagents |
| Phased Pipeline | ✅ Workflow | ✅ SubagentWorkflow | ⚠️ Plugin | ✅ LangGraph |
| TDD | ✅ Workflow | ✅ SubagentWorkflow | ⚠️ | ✅ LangGraph |

## Sources

### SDD
- [GitHub Spec Kit](https://github.com/github/spec-kit) — GitHub
- [Microsoft Learn: Spec-Driven Development](https://learn.microsoft.com)
- [tiny-spec](https://github.com/matheusbuniotto/tiny-spec) — GitHub
- [OpenSpec](https://sgryphon.gamertheory.net) — Getting started guide
- [Spec-Driven Development: From Code to Contract](https://arxiv.org/html/2602.00180v1) — arXiv
- [What Is Spec-Driven Development?](https://www.augmentcode.com/guides/what-is-spec-driven-development) — Augment Code

### Evidence-Gated
- [Proof-or-Stop](https://arxiv.org/abs/2607.14890) — arXiv paper
- [Proof-or-Stop GitHub](https://github.com/Proof-or-Stop) — Implementation
- [phionyx-pipeline-mcp](https://github.com/halvrenofviryel/phionyx-pipeline-mcp) — GitHub
- [Custos Code](https://github.com/Olivesz/custos-code) — GitHub

### CIV
- [no-slop-harness](https://pypi.org/project/no-slop-harness) — PyPI
- [harnessie](https://github.com/snapsynapse/harnessie) — GitHub
- [harnessie.com](https://harnessie.com) — Website

### Phased Pipeline / TDD
- [ByteDigger (shtofadhor)](https://github.com/shtofadhor/bytedigger) — GitHub
- [ByteDigger (guy-lifshitz)](https://github.com/guy-lifshitz/bytedigger) — GitHub
- [TDD inside the agent loop](https://martinfowler.com/articles/exploring-gen-ai/tdd-in-the-agent-loop.html) — Martin Fowler
