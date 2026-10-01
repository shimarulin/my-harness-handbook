---
id: comparison-20261002-000000001
type: research-note
status: final
created: 2026-10-02
updated: 2026-10-02
topics: [comparison, specs-md, spec-kitty, adopt-adapt-build]
author: agent:omp
---

# Comparison: specs.md vs spec-kitty vs наша process-framework

## Матрица критериев

| Критерий | specs.md | spec-kitty | Наша process-framework |
|---|---|---|---|
| **Язык** | TypeScript/Node.js | Python 3.11+ | TypeScript (будущее) |
| **Установка** | `npx specsmd@latest install` | `pipx install spec-kitty-cli` | — |
| **Архитектура** | Pluggable flows (4) | Mission types (4) | Conventions + templates |
| **Research support** | ⚠️ Ideation only | ✅ Full research mission | ✅ Research as first phase |
| **Evidence tracking** | ❌ | ✅ CSV (evidence-log, source-register) | ❌ (gap) |
| **State machine** | ⚠️ Per-flow | ✅ Evidence-gated | ❌ Frontmatter status |
| **Frontmatter** | ⚠️ Partial (no frontmatter in simple) | ⚠️ Bold-label headers, WP frontmatter | ✅ Mandatory, strict schema |
| **Docs/ usage** | ✅ Never touches docs/ | ⚠️ Deliverables to docs/research/ | ✅ docs/ is workspace |
| **Root clutter** | 🟡 2+ dirs (.specsmd/, .specs-ideation/ or specs/, memory-bank/) | 🔴 4+ dirs (.kittify/, kitty-specs/, .worktrees/, .claude/) | ✅ Minimal (content/, docs/, tools/) |
| **Extensibility** | ✅ Markdown agents, .hbs templates, memory-bank.yaml | ✅ Template overrides, custom missions, validators | ✅ Conventions, templates (planned) |
| **Fit for doc repo** | 🟡 Ideation only | 🟡 Research mission only | ✅ Native |

## Уникальные сильные стороны

### specs.md

1. **12 tool installers** — самая широкая поддержка AI-инструментов (Claude, Cursor, Copilot, Antigravity, Cline, Codex, Gemini, Kiro, OpenCode, Roo, Windsurf).
2. **Ideation Flow** — уникальный pre-research brainstorming (Spark → Flame → Forge) с anti-bias engine (12-domain wheel), deep thinking, resumable sessions.
3. **Memory-bank.yaml** — declarative schema для artifacts (paths, naming, ownership, execution modes) — agent-readable process schema.
4. **Walkthrough generation** (FIRE) — auto-generated change documentation после каждого run.
5. **Handlebars templates** — полностью overridable форматы артефактов.

### spec-kitty

1. **Evidence-gated state machine** — переходы блокируются условиями (≥3 источника для synthesis), не advisory.
2. **CSV evidence tracking** — `evidence-log.csv` (timestamp, source_type, citation, key_finding, confidence, notes) и `source-register.csv` (source_id, citation, url, accessed_date, relevance, status) — machine-readable, CI-проверяемо.
3. **Two-location model** — planning evidence в `kitty-specs/`, deliverables в `docs/research/` — зеркалит наш `docs/` vs `content/` split.
4. **Work Packages с lanes** — `planned → claimed → in_progress → for_review → in_review → approved → done`, append-only `status.events.jsonl`.
5. **Template override chain** — project > user > package, 3-tier resolution.

### Наша process-framework

1. **Единый frontmatter** — обязателен во всех слоях, strict schema (id, type, status, created, updated, topics, author).
2. **Три слоя** — чёткое разделение `content/` (product), `docs/` (workspace), `tools/` (process).
3. **Research as first phase** — не отдельный flow/mission, а принцип всей работы.
4. **Неперемещаемые объекты + views/** — content stays, structure virtual; чистый diff.
5. **Минимальный root** — только `content/`, `docs/`, `tools/`, `config/`.

## GAP-анализ: чего нет у нас

| GAP | Где у конкурентов | Приоритет | Действие |
|---|---|---|---|
| **Evidence-log CSV** | spec-kitty: `research/evidence-log.csv` | 🔴 High | Adopt schema в `docs/research/notes/<slug>/evidence-log.csv` |
| **Source-register CSV** | spec-kitty: `research/source-register.csv` | 🔴 High | Adopt schema в `docs/research/notes/<slug>/source-register.csv` |
| **Research type taxonomy** | spec-kitty: Literature Review \| Empirical Study \| Case Study \| Meta-Analysis | 🟡 Medium | Adopt в frontmatter research-note |
| **Quality checklists** | spec-kitty: `checklists/requirements.md` | 🟡 Medium | Adapt как per-research checklists |
| **Template override chain** | spec-kitty: project > user > package | 🟡 Medium | Adapt для `tools/process-framework/templates/` |
| **Anti-bias protocols** | specs.md: ideation shared protocols (anti-bias.md, deep-thinking.md) | 🟢 Low | Adopt как research/brainstorming prompts |
| **Walkthrough generation** | specs.md: FIRE walkthrough.md | 🟢 Low | Adapt для `docs/notes/` (auto-documenting agent sessions) |
| **Memory-bank.yaml schema** | specs.md: declarative artifact schema | 🟢 Low | Adapt pattern для conventions |

## Рекомендация: adopt / adapt / avoid

| Решение | Что | Откуда | Почему |
|---|---|---|---|
| **Adopt outright** | `evidence-log.csv` schema | spec-kitty | Немедленно usable; machine-readable; CI-проверяемо |
| **Adopt outright** | `source-register.csv` schema | spec-kitty | Лучше, чем inline URLs; status tracking |
| **Adopt outright** | Two-location model (planning evidence vs deliverables) | spec-kitty | Валидирует наш `docs/` vs `content/` split |
| **Adopt outright** | Research type taxonomy (Literature Review, Empirical Study, Case Study, Meta-Analysis) | spec-kitty | Полезно для классификации research notes |
| **Adapt** | Quality checklists → lint rules | spec-kitty | `tools/process-framework/` linting |
| **Adapt** | Template override chain → project-local templates | spec-kitty | `tools/process-framework/templates/` + project overrides |
| **Adapt** | WP frontmatter `history` → наш `updated:` + history array | spec-kitty | Richer tracking for agent work |
| **Adapt** | Anti-bias protocols → research prompts | specs.md | `docs/research/` brainstorming |
| **Adapt** | Walkthrough pattern → session documentation | specs.md | `docs/notes/` auto-documentation |
| **Avoid** | Full spec-kitty runtime (kitty-specs/, worktrees, WP lanes, merge gates) | — | Oversized for doc repo; 4 root dirs; parallel metadata |
| **Avoid** | specs.md Simple/AI-DLC flows | — | Code-oriented; `specs/` и `memory-bank/` root clash |
| **Avoid** | Charter/doctrine system | spec-kitty | Our conventions/ simpler |
| **Avoid** | Documentation mission Divio layout | spec-kitty | Conflicts with our `docs/` workspace |

## Следующие шаги

1. **Создать шаблоны** в `tools/process-framework/templates/`:
   - `research-note.md` — с frontmatter + research type taxonomy
   - `evidence-log.csv` — spec-kitty schema
   - `source-register.csv` — spec-kitty schema
2. **Обновить конвенцию** `tools/process-framework/conventions/frontmatter.md` — добавить `research_type` для research-note.
3. **Создать пример** в `tools/process-framework/examples/` — заполненный research-note с evidence-log.
4. **Первое research** — структура handbook'а с использованием новых артефактов.

## Источники

- specs.md findings: `findings/specs-md.md`
- spec-kitty findings: `findings/spec-kitty.md`
- Research agents: SpecsMdResearch, SpecKittyResearch
