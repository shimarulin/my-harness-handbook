# AI Coding Agents & Deterministic Workflows — Research

This directory contains comprehensive research on AI coding agents, multi-agent
orchestration patterns, deterministic workflow engines, and portable methodologies
for building reliable agent-based development systems.

## Document Index

| Document | Topic |
|----------|-------|
| [01-tooling-comparison.md](01-tooling-comparison.md) | OpenCode vs Pi vs Deep Agents Code — architecture, features, trade-offs |
| [02-multi-agent-orchestration.md](02-multi-agent-orchestration.md) | Subagent patterns, nested architectures, peer-to-peer vs hierarchical |
| [03-deterministic-workflows.md](03-deterministic-workflows.md) | Workflows vs agents, deterministic orchestration, token economics |
| [04-methodologies.md](04-methodologies.md) | SDD, Proof-or-Stop, CIV, TDD-first — portable methodology layer |
| [05-implementation-guide.md](05-implementation-guide.md) | Practical implementation on Pi + Deep Agents Code |

## Executive Summary

**Core thesis**: The optimal open-source stack for vendor-lock-free AI coding
is **Pi** (minimal harness, maximum control) as primary agent, supplemented
optionally by **Deep Agents Code** for programmatic LangGraph-based
orchestration. The methodology layer (SDD + Evidence-Gated Lifecycle + CIV +
TDD) is portable across harnesses through AGENTS.md, workflow scripts, and
adapter patterns.

**Key findings**:

1. Pi is the most vendor-lock-free option: MIT license, 15+ providers,
   TypeScript extensions, no framework dependencies
2. Deep Agents Code has LangChain framework lock-in but offers rich
   programmatic control via LangGraph
3. Workflows (deterministic JavaScript orchestration) are the enforcement
   mechanism that turns methodology from "prompt recommendations" into
   "code invariants"
4. The methodology layer is already tool-agnostic: GitHub Spec Kit has 38+
   integrations, Proof-or-Stop is an open standard
5. Workflow scripts are JavaScript (not TypeScript) — the runtime has no
   TS transpilation layer

**Date**: 2026-10-05
**Status**: Active research, evolving
