# AGENTS.md

## Project Context

**My Harness Handbook** — research-driven project: building a practical handbook on designing AI harnesses for coding agents, while using the repository itself as a process playground.

**Role for AI agents:** You are a research and documentation assistant. You execute plans, conduct research, draft content, and maintain process artifacts. The human approves plans, ADRs, and promotes content to `content/`.

**Key documents (read in order):**
1. `docs/ABOUT.md` — what we're doing, for whom, methodology, current status
2. `docs/plans/_objects/PLAN-20261001-164751701-repository-structure.md` — repository structure, naming, rules
3. `docs/STATUS.md` — current state of the corpus (when it exists)
4. `tools/process-framework/conventions/` — frontmatter, naming, structure conventions (when they exist)

## Repository Structure

| Layer | Path | What it is | Your role |
|---|---|---|---|
| Content | `content/` | Reader-facing product: handbook, kb, guide | **Never create files here without research phase in `docs/`** |
| Workspace | `docs/` | Production workspace: research, drafts, plans, notes | Your primary working area |
| Process framework | `tools/process-framework/` | Process descriptions, conventions, templates, examples | Read for rules; write only when process evolves |

## Core Rules

### 1. Research first — always

Before any tool selection, any handbook chapter, any process change — create `docs/research/notes/YYYY-MM-DD-<slug>/` with:
- `question.md` — what we're deciding, criteria, constraints
- `findings/` — one file per source/alternative
- `comparison.md` — side-by-side matrix
- `decision.md` — recommendation with rationale

**Never skip research phase for non-trivial decisions.**

### 2. Content promotion = rewriting, not moving

- Files in `content/` are **written from scratch** based on `docs/` materials (absorption, not copying).
- `docs/` remains as attributed raw material; `content/` is the clean product.
- **Never `git mv` from `docs/` to `content/`.**

### 3. Immutable files, virtual structure

- Files in `docs/plans/_objects/`, `docs/notes/_objects/` **never move** — status changes in frontmatter only.
- Navigation via `docs/views/` (symlinks, materialized from frontmatter) — regenerate, don't edit manually.
- Symlinks: always relative paths, never symlink-to-symlink, only to `_objects/`.

### 4. Identifier format

All new objects: `TYPE-<YYYYMMDD>-<HHMMSSfff>-<slug>.md` (UTC, milliseconds).

- Generate UTC timestamp with milliseconds.
- Check for collision; if exists, wait for next millisecond.
- Example: `PLAN-20261001-164751701-repository-structure.md`.

### 5. Frontmatter — mandatory in all layers

```yaml
---
id: <type>-<YYYYMMDD>-<HHMMSSfff>
type: research-note | plan | draft | note | kb-article | handbook-chapter | guide-chapter | process-doc | adr
status: draft | active | review | final | archived
created: YYYY-MM-DD
updated: YYYY-MM-DD
topics: [<topic1>, <topic2>]
author: human:<name> | agent:<name>
---
```

### 6. Doubt as method — use `docs/notes/`

- `docs/notes/` — for doubts, questions, observations, unformed ideas.
- Low barrier: single file, minimal frontmatter (`created`, `topics`).
- Not "ideas" (that's already interpretation) — notes capture uncertainty before it becomes confidence.
- Promotion to research or ADR when doubt becomes verified understanding.

### 7. Avoid unnecessary friction

- Process should help, not ritualize.
- Before adding a rule, check: does it add value beyond friction?
- If a rule feels heavy, propose simplification in `docs/notes/` or `docs/adr/`.

## File Operations

| Operation | Path | Format |
|---|---|---|
| New plan | `docs/plans/_objects/PLAN-<YYYYMMDD>-<HHMMSSfff>-<slug>.md` | Template: `tools/process-framework/templates/plan.md` (when exists) |
| New note | `docs/notes/_objects/NOTE-<YYYYMMDD>-<HHMMSSfff>-<slug>.md` | Minimal frontmatter |
| New research | `docs/research/notes/YYYY-MM-DD-<slug>/` | question.md + findings/ + comparison.md + decision.md |
| New draft | `docs/drafts/<type>/` | Depends on type (handbook chapter, kb article) |
| New ADR | `docs/adr/ADR-<NNNN>-<slug>.md` | MADR format, project-specific decisions |
| Framework ADR | `tools/process-framework/adr/ADR-<NNNN>-<slug>.md` | MADR format, process-wide decisions |

## Commit Rules

- **Conventional Commits**: `docs(<scope>): <description>` or `content(<scope>): <description>`.
- Scope: `plans`, `about`, `agents`, `research`, `notes`, `kb`, `guide`, `handbook`, `process-framework`, `migration`.
- One logical change per commit; commit after each plan/ADR/research completion.
- **Never commit** files in `content/` without explicit user approval.

## What NOT to Do

- ❌ Create files in `content/` without research phase and user approval.
- ❌ Move files between `docs/` and `content/` (only rewrite).
- ❌ Edit files in `_objects/` after creation (only frontmatter status).
- ❌ Use sequential numbering (`000001`) for new objects — use UTC timestamp with milliseconds.
- ❌ Create symlinks to symlinks or absolute-path symlinks.
- ❌ Skip frontmatter in any markdown file.
- ❌ Write long philosophical passages in AGENTS.md — keep it prescriptive.

## Current Status (2026-10-01)

- ✅ Plan: repository structure accepted (PLAN-20261001-164751701).
- ✅ ABOUT.md: project description and methodology.
- ✅ AGENTS.md: this file.
- 🔄 Migration in progress: `research/kb/` → `content/kb/`, `guide/` → `content/guide/`, `ideas/` → `docs/notes/`.
- ⏳ Next: `tools/process-framework/conventions/`, `docs/STATUS.md`, migration completion.

## References

- Plan: `docs/plans/_objects/PLAN-20261001-164751701-repository-structure.md`
- About: `docs/ABOUT.md`
- KB format (when migrated): `tools/process-framework/conventions/kb-format.md`
- Research knowledge: `content/kb/methods/research-knowledge.md` (when migrated)
- Content-stays principle: `content/kb/principles/content-stays-virtual-structure.md` (when migrated)
