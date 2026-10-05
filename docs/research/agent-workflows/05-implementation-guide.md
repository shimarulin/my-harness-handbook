# 05 — Implementation Guide: Pi + Deep Agents Code

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│         METHODOLOGY (portable, tool-agnostic)       │
│                                                     │
│  SDD artifacts + Evidence gates + CIV roles         │
│  + Phased pipeline + TDD enforcement                │
└─────────────────────────────────────────────────────┘
                    │
    ┌───────────────┼───────────────┐
    │               │               │
    ▼               ▼               ▼
┌─────────┐   ┌─────────┐   ┌─────────┐
│   Pi    │   │ Claude  │   │  dcode  │
│ Primary │   │  Code   │   │ Adapter │
│ Harness │   │ Adapter │   │(optional)│
└─────────┘   └─────────┘   └─────────┘
```

## Phase 1: Pi Foundation

### Install Pi

```bash
curl -fsSL https://pi.dev/install.sh | sh
```

### Install Sub-Agents Extension

```bash
pi install npm:@tintinweb/pi-subagents
```

This provides:
- `SubagentWorkflow` tool for deterministic JavaScript orchestration
- Nested subagents with `allowed_subagents`
- Agent mentions (`@handle`)
- Cross-extension RPC
- Fleet view, live widget, custom agent types

### Create Agent Roles (CIV)

#### `docs/research/agent-workflows/.pi/agents/coordinator.md`

```yaml
---
name: coordinator
tools: [planning, task_decomposition, web_search]
allowed_subagents: implementer, verifier, spec-writer
model: anthropic/claude-sonnet-4-5
thinking: high
---
# Coordinator

You decompose tasks into typed CIVMessage objects.

## Responsibilities
- Analyze requirements from spec.md
- Create task DAG with explicit dependencies
- Assign tasks to appropriate agents
- Monitor progress and handle escalations

## Constraints
- You do NOT write implementation code
- You do NOT run tests directly
- All task assignments must reference spec.md sections
```

#### `.pi/agents/implementer.md`

```yaml
---
name: implementer
tools: [write_file, edit_file, bash]
model: anthropic/claude-haiku-4-5
---
# Implementer

You execute tasks from the coordinator with limited tool access.

## Responsibilities
- Write implementation code per task specification
- Run build commands
- Report completion with list of changed files

## Constraints
- ONLY modify files listed in task allowlist
- Each change must reference the task ID
- Report changed files as structured JSON, not prose
```

#### `.pi/agents/verifier.md`

```yaml
---
name: verifier
tools: [bash, lint, test_runner, type_checker]
model: anthropic/claude-haiku-4-5
---
# Verifier

You run deterministic checks and return structured results.

## Responsibilities
- Run test suite
- Run linter
- Run type checker
- Compare git diff against claimed changes

## Output Format
Return JSON:
{
  "status": "pass" | "reject",
  "checks": [
    {"name": "tests", "passed": true, "output": "..."},
    {"name": "lint", "passed": true, "output": "..."}
  ],
  "unverified_claims": ["file.py claimed but not in git diff"]
}
```

#### `.pi/agents/spec-writer.md`

```yaml
---
name: spec-writer
tools: [write_file, read_file]
model: anthropic/claude-sonnet-4-5
---
# Spec Writer

You create specification documents following SDD methodology.

## Output Artifacts
- spec.md: what to build and acceptance criteria
- plan.md: how to build it
- tasks.md: ordered implementation steps

## Rules
- Every acceptance criterion must be mechanically verifiable
- Every task must reference a spec section
- No implementation details in spec.md
```

### Configure AGENTS.md

Create project-level `AGENTS.md`:

```markdown
# Project Agent Instructions

## Methodology: SDD + Evidence-Gated + CIV

### Mandatory Workflow
1. All features start with spec.md (created by spec-writer)
2. Human reviews spec before implementation
3. Coordinator decomposes into tasks
4. Implementer executes with tool restrictions
5. Verifier runs mechanical checks
6. No phase can be skipped

### Evidence Requirements
- "Done" means: tests pass + lint clean + type check passes
- Every claim must be verifiable via git diff
- Contradictions between claims and evidence → reject

### Role Boundaries
- Coordinator: planning only, no code
- Implementer: execution only, within allowlist
- Verifier: checking only, returns pass/reject
```

## Phase 2: SDD Integration

### Install GitHub Spec Kit

```bash
# Follow instructions at https://github.com/github/spec-kit
```

### Create SDD Workflow

Save as `.pi/workflows/sdd.js`:

```javascript
// SDD Workflow: Spec → Review → Plan → Tasks
const spec = await agent({
  type: "spec-writer",
  prompt: context.prompt,
  schema: {
    type: "object",
    properties: {
      specPath: { type: "string" },
      acceptanceCriteria: { type: "array", items: { type: "string" } }
    },
    required: ["specPath", "acceptanceCriteria"]
  }
});

// HITL gate: human must approve spec
const review = await agent({
  type: "human-reviewer",
  prompt: `Review spec at ${spec.specPath}. 
           Acceptance criteria: ${spec.acceptanceCriteria.join(", ")}`,
  gate: "human-approval"
});

if (!review.approved) {
  return { 
    status: "spec-rejected",
    feedback: review.feedback 
  };
}

const plan = await agent({
  type: "spec-writer",
  prompt: `Create plan.md based on ${spec.specPath}`,
  schema: { planPath: { type: "string" } }
});

const tasks = await agent({
  type: "coordinator",
  prompt: `Decompose ${plan.planPath} into tasks.md`,
  schema: { 
    tasksPath: { type: "string" },
    taskCount: { type: "number" } 
  }
});

return {
  spec: spec.specPath,
  plan: plan.planPath,
  tasks: tasks.tasksPath,
  taskCount: tasks.taskCount
};
```

## Phase 3: Evidence-Gated Execution

### Create Verification Extension

Save as `.pi/extensions/evidence-gate.ts`:

```typescript
// Evidence gate: verify agent claims against git diff
import { exec } from "child_process";

pi.events.on("subagents:completed", async (event) => {
  if (event.type === "implementer") {
    // Get actual changes
    const gitDiff = exec("git diff --name-only").toString();
    const changedFiles = gitDiff.split("\n").filter(Boolean);
    
    // Get claimed changes from result
    const claimed = event.result?.changedFiles || [];
    
    // Find unverified claims
    const unverified = claimed.filter(
      (f: string) => !changedFiles.includes(f)
    );
    
    // Find unclaimed changes
    const unclaimed = changedFiles.filter(
      (f: string) => !claimed.includes(f)
    );
    
    if (unverified.length > 0) {
      // Agent claimed changes that don't exist
      pi.events.emit("evidence:violation", {
        agentId: event.id,
        type: "false-claim",
        files: unverified
      });
    }
    
    if (unclaimed.length > 0) {
      // Agent made changes it didn't report
      pi.events.emit("evidence:violation", {
        agentId: event.id,
        type: "unreported-changes",
        files: unclaimed
      });
    }
  }
});
```

### Wire into Workflow

```javascript
// Implementation with evidence gate
const result = await agent({
  type: "implementer",
  prompt: `Implement tasks from tasks.md`,
  gate: "npm test && npm run lint", // mechanical verification
  schema: {
    changedFiles: { type: "array", items: { type: "string" } },
    testsPassed: { type: "boolean" }
  }
});

// Evidence gate fires via extension
// If verification fails, result marked as partial
```

## Phase 4: TDD Enforcement

### Create TDD Workflow

Save as `.pi/workflows/tdd.js`:

```javascript
// TDD: RED → validate → GREEN
async function tddCycle(task) {
  // Phase 1: Write failing test (RED)
  const test = await agent({
    type: "test-writer",
    prompt: `Write failing test for: ${task.description}`,
    model: "anthropic/claude-haiku-4-5", // cheap model for test writing
    schema: { testPath: { type: "string" } }
  });
  
  // Validate: test must fail
  const testResult = exec(`npm test -- ${test.testPath}`);
  if (testResult.exitCode === 0) {
    return { 
      status: "invalid-red", 
      reason: "test passes without implementation" 
    };
  }
  
  // Phase 2: Implement (GREEN)
  const impl = await agent({
    type: "implementer",
    prompt: `Make test pass: ${test.testPath}`,
    model: "anthropic/claude-sonnet-4-5", // expensive model for implementation
    gate: `npm test -- ${test.testPath}` // must pass now
  });
  
  if (!impl.passed) {
    return { status: "green-failed", task };
  }
  
  return { status: "complete", task, test: test.testPath };
}

// Run TDD for all tasks
const results = await pipeline(
  tasks.map(task => tddCycle(task))
);

// Summary
const passed = results.filter(r => r.status === "complete");
const failed = results.filter(r => r.status !== "complete");

return {
  total: tasks.length,
  passed: passed.length,
  failed: failed.length,
  failedTasks: failed.map(f => f.task.id)
};
```

## Phase 5: Full Pipeline

### Combining All Methodologies

```javascript
// Full pipeline: SDD + Evidence-Gated + CIV + TDD
const workflow = async () => {
  // 1. SDD: Create specification
  const spec = await agent({
    type: "spec-writer",
    prompt: context.prompt
  });
  
  // 2. HITL: Human approves spec
  const review = await agent({
    type: "human-reviewer",
    prompt: `Review: ${spec.specPath}`,
    gate: "human-approval"
  });
  if (!review.approved) return { status: "spec-rejected" };
  
  // 3. CIV: Coordinator decomposes
  const plan = await agent({
    type: "coordinator",
    prompt: `Plan from: ${spec.specPath}`
  });
  
  // 4. TDD: Implement with test-first
  const results = await pipeline(
    plan.tasks.map(task => tddCycle(task))
  );
  
  // 5. Evidence-Gated: Verify all claims
  const verification = await agent({
    type: "verifier",
    prompt: "Run full verification suite",
    gate: "npm test && npm run lint && npm run typecheck"
  });
  
  // 6. Final HITL: Human approves merge
  const mergeApproval = await agent({
    type: "human-reviewer",
    prompt: "Final review before merge",
    gate: "human-approval"
  });
  
  return {
    status: mergeApproval.approved ? "ready-to-merge" : "needs-revision",
    spec: spec.specPath,
    testResults: results,
    verification: verification
  };
};
```

## Phase 6: Deep Agents Code Integration (Optional)

### When to Use dcode

- You need LangGraph's state graph for complex conditional logic
- You want remote sandboxes (LangSmith, Daytona, Modal)
- You need persistent memory across sessions
- You want LangSmith tracing/observability

### Python Implementation

```python
from deepagents import create_deep_agent
from langgraph import StateGraph, END

# Create CIV roles
coordinator = create_deep_agent(
    model="anthropic/claude-sonnet-4-5",
    tools=[planning_tool, decomposition_tool],
    system_prompt="Coordinator: decompose into typed tasks"
)

implementer = create_deep_agent(
    model="anthropic/claude-haiku-4-5",
    tools=[write_file_tool, edit_file_tool, bash_tool],
    system_prompt="Implementer: execute within allowlist"
)

verifier = create_deep_agent(
    model="anthropic/claude-haiku-4-5",
    tools=[test_runner_tool, lint_tool, type_check_tool],
    system_prompt="Verifier: return pass/reject, not text"
)

# Build state graph
workflow = StateGraph(AgentState)
workflow.add_node("spec", spec_agent)
workflow.add_node("plan", coordinator)
workflow.add_node("implement", implementer)
workflow.add_node("verify", verifier)
workflow.add_node("human_gate", human_approval)

workflow.add_edge("spec", "human_gate")  # HITL after spec
workflow.add_conditional_edges(
    "human_gate",
    lambda s: "plan" if s["approved"] else "spec"
)
workflow.add_edge("plan", "implement")
workflow.add_conditional_edges(
    "implement",
    lambda s: "verify" if s["complete"] else "implement"
)
workflow.add_conditional_edges(
    "verify",
    lambda s: "human_gate" if s["passed"] else "implement"
)
workflow.add_edge("human_gate", END)
```

## Configuration Summary

### Pi Configuration Files

```
.pi/
├── agents/
│   ├── coordinator.md
│   ├── implementer.md
│   ├── verifier.md
│   ├── spec-writer.md
│   └── human-reviewer.md
├── extensions/
│   └── evidence-gate.ts
├── workflows/
│   ├── sdd.js
│   └── tdd.js
└── settings.json
```

### AGENTS.md (Project Root)

Contains methodology rules that work across all tools.

### Subagents Settings

```json
// .pi/subagents.json
{
  "maxConcurrent": 10,
  "maxConcurrentForeground": 0,
  "maxSubagentDepth": 2,
  "backgroundByDefault": true,
  "rememberAgents": true,
  "workflowsEnabled": true
}
```

## Troubleshooting

### Common Issues

1. **Workflow scripts fail with TypeScript syntax**: Remove type
   annotations; runtime is JavaScript-only

2. **Nested subagents don't appear**: Check `allowed_subagents` in agent
   frontmatter; verify `maxSubagentDepth` > 1

3. **Evidence gate not firing**: Ensure extension is in `.pi/extensions/`
   and event listener is registered

4. **Model routing not working**: Verify model names in frontmatter match
   Pi's registry exactly

## Sources

- [tintinweb/pi-subagents](https://github.com/tintinweb/pi-subagents) — GitHub
- [Pi.dev Documentation](https://pi.dev) — Official docs
- [ray-amjad/claude-code-workflow-creator](https://github.com/ray-amjad/claude-code-workflow-creator) — Workflow patterns
- [Deep Agents SDK](https://docs.langchain.com/oss/deepagents/code/overview) — LangChain docs
- [GitHub Spec Kit](https://github.com/github/spec-kit) — SDD toolkit
- [Proof-or-Stop](https://github.com/Proof-or-Stop) — Evidence-gated lifecycle
- [no-slop-harness](https://pypi.org/project/no-slop-harness) — CIV framework
- [ByteDigger](https://github.com/shtofadhor/bytedigger) — Phased pipeline
