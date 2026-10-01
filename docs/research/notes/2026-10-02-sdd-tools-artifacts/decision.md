---
id: decision-20261002-000000001
type: research-note
status: final
created: 2026-10-02
updated: 2026-10-02
topics: [decision, adopt-adapt-build, specs-md, spec-kitty]
author: agent:omp
---

# Decision: adopt артефакты, avoid рантаймы

## Решение

**Не устанавливать ни specs.md, ни spec-kitty как рантаймы в наш репозиторий.** Вместо этого — **adopt ключевые артефакты и схемы** из обоих в нашу `tools/process-framework/` и `docs/research/`.

## Почему не рантаймы

| Проблема | specs.md | spec-kitty |
|---|---|---|
| **Root clutter** | 2+ директории (`.specsmd/`, `.specs-ideation/` или `specs/`, `memory-bank/`) | 4+ директории (`.kittify/`, `kitty-specs/`, `.worktrees/`, `.claude/`) |
| **Semantic clash** | `specs/` и `memory-bank/` рядом с `content/` и `docs/` — confusing для doc repo | `kitty-specs/` hardcoded, cannot relocate |
| **Frontmatter mismatch** | Simple flow — no frontmatter; partial в других | Bold-label headers, WP frontmatter — не наш schema |
| **Docs/ usage** | Не пишет в `docs/` (good) | Deliverables в `docs/research/` (conflict with our inbox/) |
| **Code-oriented** | Simple, FIRE, AI-DLC — для software features | software-dev, documentation missions — для code |
| **Oversized** | 90% markdown prompts + installer | Full runtime с worktrees, WP lanes, merge gates |

## Что adopt (немедленно)

| Артефакт | Откуда | Куда в нашем репо | Почему |
|---|---|---|---|
| `evidence-log.csv` schema | spec-kitty | `docs/research/notes/<slug>/evidence-log.csv` | Machine-readable evidence tracking; CI-проверяемо |
| `source-register.csv` schema | spec-kitty | `docs/research/notes/<slug>/source-register.csv` | Source status tracking; лучше inline URLs |
| Two-location model | spec-kitty | Уже есть (`docs/` vs `content/`) | Валидирует наш split |
| Research type taxonomy | spec-kitty | `tools/process-framework/conventions/frontmatter.md` + templates | Классификация research notes |
| Anti-bias protocols | specs.md | `tools/process-framework/templates/research-brainstorm.md` | Structured brainstorming |

## Что adapt (с изменениями)

| Артефакт | Откуда | Адаптация |
|---|---|---|
| Quality checklists | spec-kitty | Lint rules в `tools/process-framework/` |
| Template override chain | spec-kitty | `tools/process-framework/templates/` + project-local overrides |
| WP frontmatter `history` | spec-kitty | Наш `updated:` + optional `history[]` для agent work |
| Walkthrough pattern | specs.md | `docs/notes/` auto-documentation после agent sessions |
| Memory-bank.yaml schema | specs.md | Declarative pattern для conventions |

## Что avoid

| Что | Откуда | Почему |
|---|---|---|
| Full spec-kitty runtime | spec-kitty | Oversized; parallel metadata; code-oriented |
| specs.md Simple/AI-DLC flows | specs.md | Code-oriented; root clash |
| Charter/doctrine system | spec-kitty | Our conventions/ simpler |
| Documentation mission Divio layout | spec-kitty | Conflicts with our `docs/` workspace |

## Следующие шаги (приоритет)

1. **Создать шаблоны** в `tools/process-framework/templates/`:
   - `research-note.md` — frontmatter + research_type + ссылки на evidence-log и source-register
   - `evidence-log.csv` — spec-kitty schema (timestamp, source_type, citation, key_finding, confidence, notes)
   - `source-register.csv` — spec-kitty schema (source_id, citation, url, accessed_date, relevance, status)

2. **Обновить конвенцию** `tools/process-framework/conventions/frontmatter.md`:
   - Добавить `research_type: literature-review | empirical-study | case-study | meta-analysis` для `type: research-note`

3. **Создать пример** в `tools/process-framework/examples/`:
   - Заполненный research-note с evidence-log.csv и source-register.csv

4. **Первое research с новыми артефактами** — структура handbook'а (`docs/research/notes/2026-10-XX-handbook-structure/`).

## Риски

| Риск | Митигация |
|---|---|
| CSV файлы не интегрированы с frontmatter | CSV — отдельные артефакты; frontmatter ссылается на них |
| Ручное ведение CSV — friction | Шаблоны + будущий tooling (CLI для добавления записей) |
| Два формата (CSV + markdown) — cognitive load | CSV только для evidence/source; markdown для narrative |

## Источники

- Comparison: `comparison.md`
- specs.md findings: `findings/specs-md.md`
- spec-kitty findings: `findings/spec-kitty.md`
