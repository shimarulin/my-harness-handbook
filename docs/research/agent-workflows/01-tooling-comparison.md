# 01 — Tooling Comparison: OpenCode vs Pi vs Deep Agents Code

## Overview

Three candidates for open-source AI coding agents with different philosophies:
- **OpenCode** (Anomaly): mass-market, plug-and-play, config-driven
- **Pi** (Earendil Works): minimal harness, maximum hackability
- **Deep Agents Code** (LangChain): SDK + terminal wrapper, programmatic control

## Quick Comparison

| Criterion | OpenCode | Pi | Deep Agents Code |
|-----------|----------|-----|------------------|
| **License** | MIT | MIT | MIT |
| **GitHub stars** | ~172–200K | ~106K | ~29.9K (entire deepagents repo) |
| **Monthly users** | ~8M | N/A | N/A |
| **Providers** | 75+ via Models.dev | 15+ | OpenAI/Anthropic/Gemini + extras |
| **Context overhead** | ~6,900 tokens | <1,000 tokens | Not independently measured |
| **Customization model** | Config + plugins | TypeScript extensions | Python SDK |
| **Framework lock-in** | AI SDK ecosystem | None | LangChain/LangGraph |
| **Benchmark (DeepSeek V4 Pro)** | ~17/30 tasks | **21/30 (70%)** | Not tested |

## Pi — Minimal Agent Harness

**Repository**: [earendil-works/pi](https://github.com/earendil-works/pi)
**Website**: [pi.dev](https://pi.dev)

### Architecture

Pi is a "minimal agent harness" designed to be adapted to your workflows,
not the other way around:

- **Four default tools**: `read`, `write`, `edit`, `bash`
- **System prompt**: under 1,000 tokens
- **Extensions**: TypeScript files running in the same process as the agent loop
- **Self-modification**: Pi can read its own source code and build extensions on demand

### Key Features

- **Tree-structured sessions**: branch from any point, share as HTML/gist
- **Context engineering**: AGENTS.md, SYSTEM.md, compaction, skills, prompt templates
- **Four modes**: interactive, print/JSON, RPC, SDK
- **Session trees**: `/tree` navigation, `/export`, `/share`
- **Steering**: `Enter` to steer running agent, `Alt+Enter` for follow-up

### Extension Ecosystem

Pi has a rich package ecosystem ([pi.dev/packages](https://pi.dev/packages)):

| Package | Downloads/mo | Purpose |
|---------|-------------|---------|
| `@tintinweb/pi-subagents` | 593K | Claude Code-style sub-agents + workflows |
| `pi-mcp-adapter` | 1.5M | MCP protocol adapter |
| `pi-web-access` | 590K | Web search, URL fetching, GitHub clone |
| `billion-context` | 552K | Context compression plugin |
| `pi-subagents` (nicopreme) | 593K | Single-agent delegation, scripted workflows |

### Token Efficiency

In independent benchmarking by [Composio](https://composio.dev/content/pi-vs-opencode):

| Metric | Pi | OpenCode |
|--------|-----|----------|
| Context overhead (prompt + tools) | <1,000 tokens | ~6,900 tokens |
| Tasks passed (DeepSeek V4 Pro, hard 30) | 21/30 (70%) | ~17/30 |
| Cost per success | $0.078 | Higher (more failures) |
| Cost per shared success | $0.031 | $0.032 |

Pi's efficiency comes from minimal fixed overhead: the prefix barely changes
between turns, making much of the context land as cache hits.

## Deep Agents Code (dcode)

**Repository**: [langchain-ai/deepagents](https://github.com/langchain-ai/deepagents/tree/main/libs/code)
**Documentation**: [docs.langchain.com/oss/deepagents/code](https://docs.langchain.com/oss/deepagents/code/overview)

### Architecture

`dcode` is a pre-built coding agent built on Deep Agents SDK:

- **Interactive TUI** with streaming responses
- **Conversation resume** across sessions
- **Remote sandboxes**: LangSmith, AgentCore, Daytona, Modal, Runloop
- **Persistent memory** across conversations
- **Custom skills** as slash commands
- **Headless mode** for scripting and CI
- **Human-in-the-loop** approval gates

### Framework Lock-in

Deep Agents Code is built on the LangChain ecosystem:

- **LangGraph** for state graphs and durable execution
- **Deep Agents SDK** as abstraction layer
- **LangSmith** as default sandbox/tracing (configurable)
- Integration with **AgentCore, Daytona, Modal, Runloop**

This is not vendor lock to an LLM provider, but **framework lock**: if
LangChain changes LangGraph or Deep Agents SDK API, your code breaks.

### Relationship to Open SWE

**Open SWE** ([langchain-ai/open-swe](https://github.com/langchain-ai/open-swe)) is a
separate project from the same team — an asynchronous "software factory":

- Reads GitHub issues, plans tasks, writes code, creates PRs
- Reviews PRs, learns repository-specific preferences
- Monitors CI, responds to feedback
- Runs through dashboard, GitHub/Slack/Linear integration
- Requires backend + dashboard + database deployment

**Key distinction**: `dcode` is for interactive local development; `open-swe`
is for team automation from issue to PR. They share the Deep Agents SDK foundation.

## OpenCode

**Repository**: [anomalyco/opencode](https://github.com/anomalyco/opencode)

### Architecture

- Terminal agent with bring-your-own-key model
- 75+ LLM providers via AI SDK and Models.dev catalog
- Plan mode, MCP, LSP diagnostics, sub-agents, permissions
- Config-driven customization via `opencode.json`

### Strengths

- Most feature-rich out of the box
- Widest provider support
- Largest community (~8M monthly users)
- MIT license, fully open

### Criticisms

1. **Token consumption**: ~6,900 tokens per request overhead; documented
   cases of 13,000+ tokens for simple questions
   ([GitHub issue #8234](https://github.com/anomalyco/opencode/issues/8234))
2. **Customization model**: mostly config-driven, harder to modify core
   than Pi's TypeScript extensions
3. **Token efficiency**: in Composio's benchmark, more failed tasks that
   still burn tokens

## Vendor Lock Analysis

| Lock Type | OpenCode | Pi | Deep Agents Code |
|-----------|----------|-----|------------------|
| **To LLM provider** | None (75+ providers) | None (15+ providers) | None (any tool-calling LLM) |
| **To framework** | AI SDK ecosystem | **None** | **LangChain/LangGraph** |
| **To infrastructure** | Models.dev catalog | None (npm only) | LangSmith (default), configurable |
| **Control over core** | Config-level | **Full source access** | Full source, but LangChain abstractions |

**Pi wins for vendor-lock freedom**: no framework dependency, minimal core,
TypeScript extensions without framework abstractions.

## Recommendations

1. **For maximum independence**: Pi as primary harness
2. **For LangChain ecosystem integration**: Deep Agents Code
3. **For quick setup with many features**: OpenCode
4. **Hybrid approach**: Pi primary + Deep Agents SDK for special cases

## Sources

- [Pi vs OpenCode: After 100 Hours](https://composio.dev/content/pi-vs-opencode) — Composio, Aug 2026
- [Pi.dev Package Catalog](https://pi.dev/packages)
- [langchain-ai/deepagents](https://github.com/langchain-ai/deepagents) — GitHub
- [langchain-ai/open-swe](https://github.com/langchain-ai/open-swe) — GitHub
- [OpenCode: 8M Users, 172K Stars](https://stackfutures.com/blog/opencode-8m-users-172k-stars-coding-agents) — StackFutures, Jun 2026
- [Pi Agent Harness: Mario Zechner's Minimal Coding Agent](https://explainx.ai) — ExplainX
- [The New Agent Harnesses, Compared (2024–2026)](https://phoson.lat) — Phoson
- [OpenCode Token Usage: How It Works](https://www.truefoundry.com/blog/opencode-token-usage-how-it-works-and-how-to-optimize-it) — TrueFoundry
