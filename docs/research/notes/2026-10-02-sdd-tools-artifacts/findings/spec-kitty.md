---
id: findings-spec-kitty-20261002
type: research-note
status: final
created: 2026-10-02
updated: 2026-10-02
topics: [spec-kitty, artifacts, missions, integration]
author: agent:SpecKittyResearch
---

# Findings: spec-kitty (spec-kitty/spec-kitty)

## Что это

Python 3.11+ CLI (`pipx/uv install spec-kitty-cli`) для spec-driven development с repo-native governance. Эволюционировал из форка Spec Kit: workflow `spec → plan → tasks → next → review → accept → merge`, 4 mission types, git-worktree isolation, charter governance.

## Установка и команды

```bash
pipx install spec-kitty-cli          # или uv tool install
spec-kitty init . --ai claude        # в существующем репозитории
spec-kitty verify-setup
spec-kitty upgrade                   # после CLI upgrades
```

Slash-команды в AI-агенте: `/spec-kitty.charter → /spec-kitty.specify → /spec-kitty.plan → /spec-kitty.tasks → (runtime next) → /spec-kitty.review → /spec-kitty.accept → /spec-kitty.merge --push → /spec-kitty-mission-review`.

CLI: `spec-kitty mission list`, `spec-kitty specify --mission research "question"`, `spec-kitty next --agent claude --mission <slug>`, `spec-kitty agent tasks status [--json]`, `spec-kitty dispatch "<request>"`.

## Артефакты при установке

| Путь | Что |
|---|---|
| `.kittify/` | Все config/memory: templates/, missions/<type>/mission.yaml, charter/, config.yaml, doctrine/, evidence/, overrides/, curation/ |
| `.claude/commands/` (или .cursor/, .gemini/, ...) | ~13 slash-command .md файлов: spec-kitty.specify.md, plan, tasks, implement, review, accept, merge, status, charter, research, analyze |
| `.worktrees/` | Git worktrees per execution lane: `.worktrees/<slug>-lane-a/` |

## Артефакты per mission

```
kitty-specs/<NNN>-<slug>/
├── meta.json           # {feature_number, slug, friendly_name, mission, target_branch, vcs, created_at}
├── spec.md             # from mission-type spec-template
├── plan.md             # from mission-type plan-template
├── tasks.md            # WP breakdown
├── wps.yaml            # machine-readable WP manifest with plan_concern_refs -> IC-## traceability
├── research.md         # optional (from /spec-kitty.research)
├── data-model.md       # software-dev only
├── contracts/          # optional API specs
├── checklists/requirements.md
└── tasks/WP01-<name>.md ...   # WP prompt files with YAML frontmatter
```

### Research Mission (best fit для нас)

```
kitty-specs/<slug>/research/
├── evidence-log.csv        # timestamp, source_type, citation, key_finding, confidence, notes
├── source-register.csv     # source_id, citation, url, accessed_date, relevance, status
├── methodology.md          # optional
└── deliverables_path/      # declared in plan.md + meta.json, e.g. docs/research/<NNN>-<slug>/
    ├── findings.md
    ├── report.md
    ├── bibliography.md
    ├── data/analysis.csv
    └── presentation/
```

**Two-location model**: planning evidence (during planning) в `kitty-specs/<slug>/research/`; research OUTPUT deliverables в declared `deliverables_path` (convention: `docs/research/<slug>/`), merged to main like code. **Explicitly forbidden**: `kitty-specs/` for deliverables, bare `research/` at root.

### Mission types

| Mission | Steps | Required | Special |
|---|---|---|---|
| `software-dev` | discovery → specify → plan → tasks_outline → tasks_packages → tasks_finalize → implement → review → accept | spec.md, plan.md, tasks.md | WP lanes: planned → claimed → in_progress → for_review → in_review → approved → done |
| `research` | scoping → methodology → gathering ↔ synthesis → output → accept | spec.md, plan.md, tasks.md, findings.md | source-count guard (≥3 sources for synthesis); research/source-register.csv, research/evidence-log.csv |
| `plan` | specify → research → plan → review (v1: goals → research → structure → draft → review → done) | goals.md, plan.md | artifact-exists guards per step; plan_approved gate |
| `documentation` | discover → audit → design → generate → validate → publish (Divio 4-type) | spec.md, plan.md, tasks.md, gap-analysis.md | quality checks at acceptance (no [TODO], gap analysis complete) |

## Frontmatter и метаданные

| Артефакт | Формат | Наше соответствие |
|---|---|---|
| WP files (`tasks/WP##-*.md`) | YAML frontmatter: `work_package_id`, `title`, `lane`, `dependencies`, `subtasks`, `phase`, `assignee`, `agent`, `shell_pid`, `review_status`, `history[]` | ❌ Нет (наш: id, type, status, created, updated, topics, author) |
| `meta.json` | JSON, no frontmatter. `mission` selects type. | ⚠️ JSON, не frontmatter |
| `spec.md` / `plan.md` | **Bold-label headers**, не YAML: `**Mission Branch**: [###-name]`, `**Created**: [DATE]`, `**Status**: Draft`, `**Research Type**: Literature Review \| Empirical Study \| Case Study \| Meta-Analysis` | ❌ Не frontmatter |
| `status.events.jsonl` | Append-only JSONL event log — source of truth for WP lane state | ❌ Не frontmatter |
| Their docs | Frontmatter (title, description, doc_status, updated, audience, related) — for THEIR docs site (DocFX), not imposed on mission artifacts | ⚠️ Их docs, не наши |

## Source code structure

- `src/` — 6 packages: `charter/` (governance), `kernel/` (env, bootstrap), `mission_runtime/`, `runtime/`, `glossary/`, `specify_cli/` (bulk CLI, 60+ submodules).
- Mission definitions: `packs/built-in/missions/<type>/` (mission.yaml + mission-runtime.yaml + templates/ + step contracts).
- `src/specify_cli/missions/<type>/` — derived copies (deprecation path #883).
- Step contracts: `src/charter/offering/missions/built_in_step_contracts/research-*.step-contract.yaml`.

**Extensibility**: template override chain (project `.kittify/overrides/` > user `~/.kittify/` > package), custom missions (`.kittify/missions/<key>/mission.yaml`), org packs, charter governance (charter.md + charter.yaml + graph.yml), custom validators (`validators.py`).

## Интеграция с нашим репозиторием

### Конфликты

| Конфликт | Severity | Разрешение |
|---|---|---|
| `docs/research/` collision: spec-kitty deliverables default `docs/research/<NNN>-<slug>/` vs our `docs/research/inbox/<topic>/` | 🟡 Low-Medium | Different subdirs, no file clash. Two naming conventions (NNN-slug vs topic-name), two lifecycles (merged-from-worktree vs inbox-curation). Разрешение: `deliverables_path` configurable per-mission — set to `docs/research/inbox/<slug>/` or distinct tree. |
| `docs/` Divio assumption: documentation mission assumes `docs/` as tutorials/how-to/reference/explanation with docfx.json + toc.yml | 🟡 Low | Our `docs/` is workspace layer, not published docs. Point documentation missions at `content/` or skip. |
| Frontmatter schema mismatch | 🟡 Medium | Our mandatory schema vs spec-kitty's WP frontmatter and bold-label headers. Разрешение: override content templates via `.kittify/overrides/`; `kitty-specs/` arguably tooling state exempt from content conventions. |
| Root clutter: `.kittify/`, `kitty-specs/`, `.worktrees/`, `.claude/` — 4 new top-level entries | 🟡 Low | `kitty-specs/` cannot be relocated (hardcoded). Acceptable; gitignore `.worktrees/`. |
| `tools/process-framework/` — no collision | ✅ None | spec-kitty never touches `tools/`. Its conventions live in `.kittify/`. Our process-framework could host override templates. |

### Fit assessment

| Mission | Fit | Почему |
|---|---|---|
| **research** | ✅ Best | `source-register.csv` + `evidence-log.csv` + `findings.md` map directly to our `docs/research/inbox/` practice + add confidence levels, source status, ≥3-source guards. Two-location model mirrors our `docs/` (workspace) vs `content/` (published) split. |
| `plan` | 🟡 Moderate | `goals.md`, `plan.md`, `research.md` map to our `docs/plans/_objects/`. But heavyweight (worktrees, WP lanes) for doc repo. |
| `documentation` | ❌ Poor | Divio docs/ layout conflicts with our `docs/` workspace semantics. Our `content/` already covers Divio. |
| `software-dev` | ❌ Poor | Code implementation coordination we don't have. |

### Рекомендация

**Adopt артефакты, avoid runtime.** Research mission's CSV schemas и two-location model — immediately usable. Full runtime (kitty-specs/ + worktrees + WP lanes + merge gates) — oversized for documentation repo unless parallel doc-writing agents.

## Adopt / Adapt / Avoid

| Решение | Что | Почему |
|---|---|---|
| **Adopt outright** | `evidence-log.csv` schema (timestamp, source_type, citation, key_finding, confidence, notes) | Immediately usable for our research notes |
| **Adopt outright** | `source-register.csv` schema (source_id, citation, url, accessed_date, relevance, status) | Better than our current undifferentiated inbox notes |
| **Adopt outright** | Two-location model: planning evidence separate from published deliverables | Mirrors our `docs/research/inbox/` vs `content/` split, validates it |
| **Adopt outright** | Research type taxonomy in spec header (Literature Review \| Empirical Study \| Case Study \| Meta-Analysis) | Useful for our research notes |
| **Adopt outright** | Quality checklists as quality gates | Adapt as lint rules in `tools/process-framework/` |
| **Adapt** | Mission-type concept → our doc `type` taxonomy | Their research/plan/documentation parallel our research-note/plan/kb-article; borrow per-type required-artifact lists as validation rules |
| **Adapt** | WP frontmatter `history` append-only log → our `updated:` field | Their full history array richer for agent-authored work |
| **Adapt** | Template override chain (project > user > package) | Good model for `tools/process-framework/templates/` if we add per-project overrides |
| **Adapt** | `plan-field-declaration.yaml` (machine-checkable declaration of substantive template fields) | Could become frontmatter/template linter for our corpus |
| **Avoid** | Full runtime adoption: `kitty-specs/` + `.worktrees/` + WP lanes + merge gates | Solve code-implementation coordination we don't have; 4 root dirs + parallel metadata duplicating our frontmatter |
| **Avoid** | Charter/doctrine system (DIRECTIVE_/PROCEDURE_/TACTIC_ with provenance) | Our `tools/process-framework/conventions/` already plays this role, simpler |
| **Avoid** | Documentation mission's DocFX/Divio `docs/` layout | Conflicts with our `docs/` workspace; our `content/` already covers Divio |

## Artifact mapping vs our repo

| spec-kitty | Ours | Verdict |
|---|---|---|
| `kitty-specs/<slug>/spec.md` | `docs/research/inbox/<topic>/00-goals.md` | Equivalent intent; theirs template-driven |
| `kitty-specs/<slug>/plan.md` | `docs/plans/_objects/PLAN-*.md` | Equivalent |
| `research/evidence-log.csv` | (none — scattered in note bodies) | **GAP in ours; adopt** |
| `research/source-register.csv` | (none — URLs inline) | **GAP in ours; adopt** |
| `findings.md` / `report.md` in deliverables_path | `content/kb/` articles | Equivalent split (deliverable vs corpus) |
| `.kittify/charter/charter.md` | `tools/process-framework/conventions/*.md` | Equivalent; ours simpler |
| `tasks/WP*.md` + `status.events.jsonl` | (none) | N/A — no multi-agent code workflow |
| `kitty-specs/<slug>/checklists/requirements.md` | (none) | Adoptable as per-research checklists |

## Ключевые цитаты

- Mission system: `docs/architecture/mission-system.md`
- Config reference: `docs/api/configuration.md` — meta.json + WP frontmatter fields
- File structure: `docs/api/file-structure.md` — full `.kittify/`/`kitty-specs/`/`.worktrees/` layout
- Research templates: `src/specify_cli/missions/research/templates/{spec,plan,task-prompt}-template.md` — CSV schemas verbatim

## Источники

- GitHub: https://github.com/spec-kitty/spec-kitty
- Docs: https://docs.spec-kitty.ai
- Research agent: SpecKittyResearch (task, 4m11s)
