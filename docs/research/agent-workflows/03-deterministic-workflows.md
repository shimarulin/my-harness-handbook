# 03 — Deterministic Workflows vs Agent Loops

## The Fundamental Distinction

Anthropic's "Building Effective Agents" ([anthropic.com](https://www.anthropic.com/engineering/building-effective-agents))
draws a critical architectural distinction:

> **Workflows** are systems where LLMs and tools are orchestrated through
> predefined code paths.
>
> **Agents** are systems where LLMs dynamically direct their own processes
> and tool usage, maintaining control over how they accomplish tasks.

This is not "simple vs complex" — it's "who decides: code or model".

## Why Deterministic Workflows Often Win

### 1. Token Economics

Multiple agents with smaller contexts can be cheaper than one with a
saturated context window:

> "Each `agent()` call runs in its own clean context window. The result
> is multi-agent work that behaves the same way every run."
> — [claude-code-workflow-creator](https://github.com/ray-amjad/claude-code-workflow-creator)

Source: [Context Engineering: What It Is + How to Do It](https://www.taskade.com) — Taskade

### 2. Model Routing

> "An LLM router that sends routine work to cheaper models and reserves
> frontier models for hard tasks is one way teams stop that pattern."
> — [TrueFoundry](https://www.truefoundry.com/blog/opencode-token-usage-how-it-works-and-how-to-optimize-it)

In workflows, you explicitly choose the model for each `agent()` call —
no reliance on the harness's routing logic.

### 3. Mandatory Steps

In agent loops, the model can skip steps. In workflows, steps are hardcoded:

```javascript
// Workflow: security audit is MANDATORY before implementation
const audit = await agent({
  type: "security-auditor",
  model: "anthropic/claude-haiku-4-5", // cheap model for routine audit
  prompt: "Audit for vulnerabilities"
});

if (audit.criticalFindings.length > 0) {
  return { status: "blocked", reason: "security" };
}

// This code CANNOT be skipped by the model
const impl = await agent({
  type: "implementer",
  model: "anthropic/claude-sonnet-4-5", // expensive model for implementation
  prompt: `Implement with security constraints: ${audit.constraints}`
});
```

### 4. Reduced Cognitive Load

Not every step needs human review. Workflows allow targeted HITL gates
(after spec, before merge) without forcing human attention on every
intermediate step.

## Claude Code Workflow Tool

**Released**: May 2026 (research preview)

**Documentation**: [Claude Code Workflows: Deterministic Multi-Agent Orchestration](https://alexop.dev/posts/claude-code-workflows-deterministic-orchestration) — Alex Op

### Key Properties

1. **JavaScript, not TypeScript**: "Workflow scripts are JavaScript, not
   TypeScript. The runtime has no TypeScript transpilation layer."
   — [buildthisnow.com](https://www.buildthisnow.com)

2. **API**: `agent()`, `parallel()` (barrier), `pipeline()` (streaming,
   no barrier), `phase()`, `log()`, `args()`

3. **Fresh context per leaf**: each `agent()` call runs in its own clean
   context window

4. **Deterministic**: "behaves the same way every run"

5. **Resumable**: can be resumed if stopped partway

### Example: Multi-Source Research Workflow

Source: [alexanderop/claude-code-workflows-example](https://github.com/alexanderop/claude-code-workflows-example)

```javascript
// 9 research agents in parallel, then curate, then write
const sources = ["github", "blogs", "hackernews", "reddit", "devto", "key-people", "podcasts"];

const findings = await parallel(
  sources.map(source =>
    agent({
      type: "researcher",
      prompt: `Find recent developments from ${source}`,
      schema: { items: [{ title: "string", url: "string", impact: "number" }] }
    })
  )
);

const curated = await agent({
  type: "curator",
  prompt: `Deduplicate and rank by impact: ${JSON.stringify(findings)}`,
  schema: { ranked: [{ title: "string", url: "string", score: "number" }] }
});

const newsletter = await agent({
  type: "writer",
  prompt: `Write weekly newsletter from: ${JSON.stringify(curated.ranked)}`
});

return newsletter;
```

### Workflow-Creator Skill

**Repository**: [ray-amjad/claude-code-workflow-creator](https://github.com/ray-amjad/claude-code-workflow-creator)

A Claude Code skill that teaches Claude to author workflows. Ask "create a
workflow for X" and Claude generates a correct, runnable JavaScript file.

## Pi SubagentWorkflow

The `@tintinweb/pi-subagents` extension provides the same API:

> "When the orchestration shouldn't be improvised, hand a deterministic
> JavaScript script to the `SubagentWorkflow` tool — `agent()`, `parallel()`,
> `pipeline()` — and scripts written for Claude Code's Workflow tool run
> here unchanged."
> — [tintinweb/pi-subagents](https://github.com/tintinweb/pi-subagents)

### Key Features

- **`parallel()`**: barrier — all agents finish before next stage
- **`pipeline()`**: no barrier — one item can be in later stage while
  another is still in first
- **`gate` parameter**: verify child by running command (e.g., `npm test`)
  rather than asking another model
- **`resume` parameter**: continue a child instead of re-paying its context
- **Sandboxed execution**: scripts run in `node:vm` sandbox where
  `Date.now()`, `Math.random()`, and `eval` throw
- **Budget**: always reports no token target (Pi has no such directive)

### Compatibility

Scripts written for Claude Code's Workflow tool run in Pi's SubagentWorkflow
unchanged: same globals, same `schema` behavior, `budget` present.

## LangGraph — Programmatic Workflows

LangGraph allows building `StateGraph` with explicit nodes-phases and
conditional edges:

- `interrupt()` for HITL gates
- `Command(resume=...)` for human approval
- State can store append-only log with hash chain for audit

**Source**: [LangGraph Supervisor Pattern](https://callsphere.ai)

## TypeScript vs JavaScript

**Workflows must be JavaScript, not TypeScript**:

> "Workflow scripts are JavaScript, not TypeScript. The runtime has no
> TypeScript transpilation layer. Adding type annotations to a workflow
> script causes a parse error."
> — [buildthisnow.com](https://www.buildthisnow.com)

**Reason**: workflow scripts execute in `node:vm` sandbox without
pre-compilation. This is a security and predictability design decision.

**Workaround**: Write TypeScript, compile to JavaScript (`tsc` or `esbuild`),
use the generated `.js` file.

## When to Use What

| Situation | Recommended |
|-----------|-------------|
| Known repeating procedure (PR review, report generation) | **Workflow** |
| Open-ended task with unknown decomposition | **Agent** (orchestrator-workers) |
| Simple task with clear prompt | **Single LLM call** |
| Need targeted HITL | Workflow with approval gate |

## Sources

- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) — Anthropic
- [Claude Code Workflows: Deterministic Multi-Agent Orchestration](https://alexop.dev/posts/claude-code-workflows-deterministic-orchestration) — Alex Op
- [ray-amjad/claude-code-workflow-creator](https://github.com/ray-amjad/claude-code-workflow-creator) — GitHub
- [alexanderop/claude-code-workflows-example](https://github.com/alexanderop/claude-code-workflows-example) — GitHub
- [tintinweb/pi-subagents](https://github.com/tintinweb/pi-subagents) — GitHub
- [Claude Code Dynamic Workflows](https://www.buildthisnow.com) — BuildThisNow
- [AI Agents vs Workflows: When to Use Each](https://agnt.gg) — Agnt
- [Context Engineering](https://www.taskade.com) — Taskade
- [Model routing for AI agents](https://caveman.so) — Caveman
