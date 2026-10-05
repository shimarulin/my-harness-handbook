# 06 — Additional Tools & Frameworks

Tools and frameworks that complement the core Pi + Deep Agents Code stack.

## pydantic-deep — Self-Hosted Claude Code Alternative

**Repository**: [vstorm-co/pydantic-deepagents](https://github.com/vstorm-co/pydantic-deepagents)
**PyPI**: [pydantic-deep](https://pypi.org/project/pydantic-deep)
**Documentation**: [vstorm-co.github.io/pydantic-deepagents](https://vstorm-co.github.io/pydantic-deepagents)

### What It Is

A self-hosted terminal AI assistant and Python framework built on Pydantic AI
by Vstorm. Described as "the open-source Claude Code alternative & Python
agent framework."

### Key Features

- `create_deep_agent()` — one function to create an agent with planning,
  file editing, command execution, search, memory, subagents, MCP
- **Live Run Forking** — unique feature not found in other frameworks
- Copy-on-write file overlay for branch isolation
- Docker sandboxing, per-tool approval gates
- 100% type-safe (strict Pyright + MyPy), MIT license
- Unlimited context (long conversations summarized, large tool outputs
  evicted to files automatically)

### Live Run Forking

**Documentation**: [Live Run Forking](https://vstorm-co.github.io/pydantic-deepagents/advanced/forking)

From the docs:
> "Live Run Forking splits a running agent into multiple parallel branches
> that share the same conversation history up to the fork point, then explore
> different approaches in isolation. The branches run concurrently as
> asyncio.Tasks with their own DeepAgentDeps (separate backends, todos,
> message queues). When branches finish, you pick a winner — manually via
> merge_or_select (action='pick:<id>') or automatically via an AI judge."

```python
from pydantic_deep import create_deep_agent, LiveForkCapability

agent = create_deep_agent(
    forking=LiveForkCapability(max_branches=4, max_depth=2),
    # ... other config
)
```

**Why it matters**: No other agent framework has this. It enables
architectural exploration — fork a run, try different approaches in parallel,
let an AI judge pick the best.

### When to Use

- You want a self-hosted alternative to Claude Code
- You need Live Run Forking for architectural exploration
- You prefer Python + Pydantic type safety over TypeScript
- You want batteries-included (planning, memory, subagents out of the box)

## DeterminAgent — Zero-Cost Multi-Agent Orchestration

**Repository**: [Experto-AI/determinagent](https://github.com/Experto-AI/determinagent)
**PyPI**: [determinagent](https://pypi.org/project/determinagent)

### What It Is

A Python library for orchestrating AI CLI tools (Claude Code, Copilot CLI,
Gemini CLI, OpenAI Codex) using LangGraph to create deterministic pipelines
powered by existing flat-rate subscriptions.

### Key Features

- **Zero variable cost**: Uses CLI subscriptions you already pay for
- **Library-only**: Full control in pure Python, no proprietary YAML DSL
- **LangGraph state machines**: Deterministic pipelines
- `leaf_agent()` — delegating tasks in isolated context
- Zero-latency local tool control via subprocess

### Architecture

```
┌─────────────────────────────────────┐
│         DeterminAgent (Python)      │
│  ┌───────────────────────────────┐  │
│  │     LangGraph State Machine   │  │
│  │  ┌─────┐  ┌─────┐  ┌─────┐  │  │
│  │  │Node1│→ │Node2│→ │Node3│  │  │
│  │  └─────┘  └─────┘  └─────┘  │  │
│  └───────────────────────────────┘  │
└──────────┬──────────────────────────┘
           │
    ┌──────┼──────┬──────┐
    ▼      ▼      ▼      ▼
┌──────┐┌──────┐┌──────┐┌──────┐
│Claude││Copilot││Gemini││Codex │
│ Code ││ CLI  ││ CLI ││ CLI  │
└──────┘└──────┘└──────┘└──────┘
```

### When to Use

- You already pay for Claude Code / Copilot / Gemini CLI subscriptions
- You want to build multi-agent workflows without additional API costs
- You need deterministic orchestration of multiple CLI agents

## owenloop — Deterministic Rails for Agentic Workflows

**npm**: [owenloop](https://www.npmjs.com/package/owenloop)

### What It Is

From the npm description:
> "Deterministic rails for agentic workflows. Declare steps and dependencies;
> the engine guarantees order, redoes what changes invalidate, and stops what
> keeps failing — instead of hoping the agent follows through."

### Key Features

- **Declarative YAML**: Describe steps and dependencies
- **Ordering guarantee**: Step runs only when all dependencies are complete
- **Invalidation on change**: If a result changes, everything dependent is
  invalidated and redone
- **Failure handling**: Failed step stops and flags for human
- **Artifact judges**: Independent quality assessors
- **Append-only audit**: SHA-256 hash chain

### When to Use

- You need deterministic execution guarantees for agent workflows
- You want automatic invalidation when inputs change
- You need audit trails with tamper evidence

## ACP (Agent Client Protocol)

**Repository**: [zed-industries/agent-client-protocol](https://github.com/zed-industries/agent-client-protocol)

### What It Is

A JSON-RPC-based interface over stdio (local agents) or HTTP, originated by
Zed Industries and now jointly maintained with JetBrains. Defines how coding
agents communicate with editors and IDEs.

### dcode Integration

From [Deep Agents Code docs](https://docs.langchain.com/oss/deepagents/code/subagents):
> "You can also use dynamic subagents in the coding agent of your choice
> over ACP (for example, Zed)."

Enable with: `dcode --acp`

### Supported Editors

- Zed (native)
- JetBrains (via plugin)
- VS Code (via extension)
- Neovim (via adapter)

### Sources

- [ACP — VS Code Extension](https://marketplace.visualstudio.com) — VS Code Marketplace
- [Agent Client Protocol concepts](https://blog.dsalathe.dev) — Blog post
- [ACP discussion on Hacker News](https://news.ycombinator.com) — Community

## Comparison: When to Use What

| Tool | Primary Use | Language | Cost Model | Unique Feature |
|------|-------------|----------|------------|----------------|
| **pydantic-deep** | Self-hosted Claude Code alternative | Python | API costs | Live Run Forking |
| **DeterminAgent** | Orchestrate CLI subscriptions | Python | $0 (uses subscriptions) | Zero variable cost |
| **owenloop** | Deterministic workflow rails | TypeScript/JS (npm) | N/A (library) | Invalidation on change |
| **ACP** | Editor-protocol standard | Protocol | N/A | Editor integration |

## Integration with Core Stack

These tools complement the Pi + Deep Agents Code stack:

1. **Pi** remains the primary terminal harness
2. **Deep Agents Code** for programmatic LangGraph orchestration
3. **pydantic-deep** if you need Live Run Forking (not available elsewhere)
4. **DeterminAgent** if you want zero-cost orchestration via CLI subscriptions
5. **owenloop** if you need YAML-based deterministic rails
6. **ACP** for editor integration (Zed, JetBrains, VS Code)

## Sources

### pydantic-deep
- [PyPI package](https://pypi.org/project/pydantic-deep)
- [GitHub repository](https://github.com/vstorm-co/pydantic-deepagents)
- [Live Run Forking docs](https://vstorm-co.github.io/pydantic-deepagents/advanced/forking)
- [Vstorm announcement](https://pydantic.dev/articles/pydantic-deep-agents)
- [MCP Agents Market listing](https://mcpagentsmarket.com)

### DeterminAgent
- [GitHub repository](https://github.com/Experto-AI/determinagent)
- [PyPI package](https://pypi.org/project/determinagent)
- [Medium article](https://medium.com/@Experto_AI/determinagent-the-zero-cost-multi-agent-framework-you-already-paid-for-c36210e8cee5)

### owenloop
- [npm package](https://www.npmjs.com/package/owenloop)

### ACP
- [zed-industries/agent-client-protocol](https://github.com/zed-industries/agent-client-protocol)
- [ACP VS Code Extension](https://marketplace.visualstudio.com)
- [ACP concepts blog](https://blog.dsalathe.dev)
