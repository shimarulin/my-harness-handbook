# 02 — Multi-Agent Orchestration & Subagent Patterns

## Problem Statement

Standard terminal agents implement "hub-and-spoke": main agent calls subagent,
subagent returns summary, main agent calls next subagent. But what about:

1. Subagents communicating with each other (peer-to-peer)
2. Subagent A spawning its own subagent B that answers only to A

## Current Implementations

### Claude Code — Nested Subagents

Claude Code supports up to 20 parallel subagents and 3 levels of nesting
(tunable via environment variables).

**Source**: [Claude Code Agents and Subagents, Explained](https://www.notis.ai)

Stock Claude Code gates recursive delegation — subagents cannot spawn
subagents by default. A community patch
([claynicholson.com](https://claynicholson.com)) bypasses this gate.

### Pi — via @tintinweb/pi-subagents

**Repository**: [tintinweb/pi-subagents](https://github.com/tintinweb/pi-subagents)
**npm**: [@tintinweb/pi-subagents](https://www.npmjs.com/package/@tintinweb/pi-subagents)

This extension (1.2K stars, 593K downloads/mo) adds Claude Code-style
sub-agents and workflow orchestration to Pi:

#### Key Features

1. **Nested subagents** (default-off): custom agent with `allowed_subagents`
   gets ownership-scoped `Agent`, `get_subagent_result`, `steer_subagent` tools

2. **Depth cap**: default 2 (main → subagent → nested child), configurable
   via `maxSubagentDepth`

3. **Ownership-scoped**: nested children visible only to parent, stopped
   when parent finishes, token usage rolls up to parent

4. **No concurrency slot**: nested children don't occupy pool slots (parent
   already holds one)

5. **Agent mentions**: `@handle` syntax to address running/resumable/startable agents

6. **Scripted workflows**: `SubagentWorkflow` tool with `agent()`, `parallel()`,
   `pipeline()`, `phase()`, `log()`, `args()`

7. **Cross-extension RPC**: `subagents:rpc:spawn/stop/consume` via event bus

#### Configuration Example

```yaml
# .pi/agents/senior-architect.md
---
name: senior-architect
allowed_subagents: security-auditor, test-designer
model: anthropic/claude-sonnet-4-5
---
You are a senior architect. Delegate security and test work.
```

With this config, `senior-architect` can spawn `security-auditor` and
`test-designer` as its own children. They answer only to it, not to the
main session.

### Deep Agents / LangGraph

Deep Agents SDK supports hierarchical multi-agent graphs through LangGraph.

**Source**: [LangChain Forum: using a graph-based tool directly via createAgent](https://forum.langchain.com)

Approach: use `create_deep_agent` as outer orchestration layer, register
custom LangGraph subgraph (CompiledSubAgent) as subagent. Since LangGraph
is a state graph, you can programmatically set arbitrary edges, including
`subagent_A → subagent_B → subagent_A`.

### AutoGen — Conversation-Based Architecture

**Repository**: [microsoft/autogen](https://github.com/microsoft/autogen)

AutoGen is built around "Conversable Agents" that send and receive messages
to each other — architecturally peer-to-peer, not hub-and-spoke. Agents can
invoke each other directly without an orchestrator.

**Source**: [AutoGen: Powering Next Generation LLM Applications](https://www.unite.ai)

### A2A Protocol — Peer-to-Peer Between Agents

The Agent2Agent (A2A) protocol from Google enables horizontal communication
between autonomous AI agents, handling "macro" interactions (agent delegation
and orchestration), while MCP handles "micro" interactions (tool calls).

**Sources**:
- [What is the A2A Protocol?](https://tyk.io) — Tyk
- [MCP vs A2A Protocol](https://gingerlabs.ai) — Ginger Labs
- [The Two Protocols Behind Every Serious AI Agent System](https://dev.to)

## Why Hub-and-Spoke Dominates

### Research Findings

1. **The Illusion of Multi-Agent Advantage** ([arXiv](https://arxiv.org/abs/2607.14890)):
   "MAS gains depend critically on task structure, verification protocols,
   and capabilities of both orchestrator and sub-agents"

2. **Why Multi-Agent LLM Systems Fail** ([Creole Studios](https://www.creolestudios.com/why-multi-agent-llm-systems-fail)):
   Study of 5 frameworks, 150+ tasks, 14 failure modes. "More agents do not
   automatically improve accuracy: they increase latency, token use,
   communication overhead, and number of failure points"

3. **Anthropic's Building Effective Agents** ([anthropic.com](https://www.anthropic.com/engineering/building-effective-agents)):
   "Start with the simplest solution possible, and only increase complexity
   when needed"

### Specific Reasons

1. **Context isolation as a feature**: subagents fork context and return
   only results to parent, preventing context pollution
2. **Peer exchanges multiply cost, not benefit**: each agent-to-agent message
   is a separate LLM call adding overhead
3. **Cascading errors**: incorrect context from A propagates to B
4. **Debugging complexity**: peer-to-peer creates branching communication
   trees that are hard to trace

## Implementation on Pi

### Nested Subagents

```bash
pi install npm:@tintinweb/pi-subagents
```

Then in `.pi/agents/<name>.md`:

```yaml
---
name: team-lead
allowed_subagents: researcher, implementer, verifier
---
You are a team lead. Delegate to your team.
```

### Cross-Extension RPC (for peer-to-peer)

```javascript
// Extension code for agent-to-agent communication
pi.events.emit("subagents:rpc:spawn", {
  requestId: crypto.randomUUID(),
  type: "security-auditor",
  options: { isBackground: true }
});
```

## Summary

| Pattern | Claude Code | Pi + subagents | Deep Agents | AutoGen |
|---------|-------------|----------------|-------------|---------|
| Subagent ↔ subagent direct | No | Via RPC only | Programmable | Yes |
| A spawns B (nested) | Yes (3 levels) | Yes (`allowed_subagents`) | Yes | Yes |
| B answers only A | Yes | Yes (ownership-scoped) | Yes | Yes |
| Ready terminal agent | Yes | Yes | dcode | No (framework) |

**Conclusion**: For terminal coding, nested subagents (A→B, B answers A)
are available in Claude Code and Pi. Pure peer-to-peer between subagents
requires custom programming in all tools.

## Sources

- [tintinweb/pi-subagents](https://github.com/tintinweb/pi-subagents) — GitHub
- [Pi.dev Packages](https://pi.dev/packages) — Pi package catalog
- [Claude Code Agents and Subagents](https://www.notis.ai) — Notis
- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) — Anthropic
- [The Illusion of Multi-Agent Advantage](https://arxiv.org/abs/2607.14890) — arXiv
- [Why Multi-Agent LLM Systems Fail](https://www.creolestudios.com/why-multi-agent-llm-systems-fail) — Creole Studios
- [Multi-Agent AI Systems in Production](https://www.aimagicx.com) — AI MagicX
