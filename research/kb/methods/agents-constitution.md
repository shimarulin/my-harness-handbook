# AGENTS.md и CONSTITUTION.md: durable context для AI-агентов

| Параметр | Значение |
|---|---|
| Статус | draft |
| Обновлено | 2026-09-30 |

## Что это

Два взаимодополняющих файла durable context — слой, который агент обязан прочитать до любой задачи:

- **AGENTS.md** — открытый кросс-инструментальный стандарт операционных правил «как работать в этом репо». Де-факто стандарт (agentsmd/agents.md): «README for agents — a dedicated, predictable place to provide context». Обновляется регулярно.
- **CONSTITUTION.md** — immutable high-level principles «почему так строим» (происхождение: GitHub Spec Kit, `/speckit.constitution`, `.specify/memory/constitution.md`). Меняется только через RFC/консенсус.

## Поддержка и размещение

| Инструмент | Поддержка AGENTS.md |
|---|---|
| Codex, Cursor, Sourcegraph Amp, Aider, Jules | Native (primary) |
| Claude Code | Читает как fallback (CLAUDE.md primary) |
| GitHub Copilot | Через `.github/copilot-instructions.md` |

Размещение: строго `AGENTS.md` в корне репо, UTF-8, plain Markdown. **Hierarchical loading**: в monorepo агент использует ближайший AGENTS.md в дереве (`src/module-a/AGENTS.md`).

Layered setup (best practice 2026): tool-specific файлы импортируют из canonical AGENTS.md, не дублируют — `# CLAUDE.md` → `@AGENTS.md` + секция Claude-specific. Альтернативы по переносимости: CLAUDE.md / .cursorrules / copilot-instructions — single tool; SKILL.md (Agent Skills spec) — cross-tool, но для on-demand capabilities, не для контекста.

## AGENTS.md vs CONSTITUTION.md

| Аспект | AGENTS.md | CONSTITUTION.md |
|---|---|---|
| Назначение | Операционные правила «как работать» | Принципы «почему так строим» |
| Изменяемость | Регулярно | Immutable, через RFC |
| Пример | «Run `npm test` before commit» | «Test-first development is mandatory» |
| Аудитория | Агенты + разработчики | Все участники + агенты |

Порядок чтения агентом: **CONSTITUTION.md** (inviolable principles) → **AGENTS.md** (operational rules) → **specs/\<feature\>/** (что строим сейчас). Закрепляется секцией `## Mandatory Context (read before any task)` в AGENTS.md.

## Скелет AGENTS.md

```markdown
# [Project Name]
One-line description.

## Stack                — Framework / Language / Database (конкретные версии!)
## Setup Commands       — install / dev / build / test / lint / typecheck (полные флаги)
## Project Structure    — дерево src/ с назначением директорий
## Code Style           — language rules, naming, imports, formatting, linting
## Testing              — фреймворки, расположение, coverage philosophy (behavior, not implementation)
## Security             — secrets (.env + .env.example), input validation, server-side auth, no new deps без approval
## Pull Requests & Commits — Conventional Commits, PR < 400 lines, new behavior = new tests в том же PR
## Domain Context       — бизнес-правила, ключевые архитектурные решения
## Known Issues & Gotchas — ловушки, workarounds
```

DO: точные команды с полными флагами; конкретные версии («Next.js 14.2.3», не «Next.js»); стабильный контекст; позитивные инструкции («Do X», не «Don't do Y» — кроме security); примеры expected output; обновлять при смене конвенций («устаревший AGENTS.md хуже отсутствующего»). DON'T: копировать README (README — для людей); volatile-информация (текущие таски, sprint status); > 500 строк (агент теряет контекст); абстрактные принципы без примеров; security rules в конце (должны быть prominent).

## Скелет CONSTITUTION.md

```markdown
# [PROJECT_NAME] Constitution

## Core Principles
### I. [Principle Name]              — с specific, actionable rules
### III. [Principle Name] (NON-NEGOTIABLE)

## [Technology stack / compliance]
## [Development Workflow: review requirements, testing gates]
## Governance                        — как конституция supersede другие практики; amendment process
```

Что включать (immutable): architecture principles («Event-driven»); quality gates («TDD mandatory», «100% coverage on critical paths»); security baselines («No secrets in code»); technology constraints («PostgreSQL only»); team conventions («PR < 400 lines»); domain rules («Financial calculations: integer cents only»). НЕ включать: текущие фичи, specific API designs, workarounds, team roster, sprint planning — всё volatile.

Роли конституции: архитектурный контракт (consistency across features/teams/AI output); baseline для QA; steering для агентов («how we build here»); decision filter. Связь с критикой: «конституция — не конфиг-файл» — каждый запрет с rationale (см. `../principles/invariants-and-gates.md`, кейс EPAM).

## Метрики успеха

| AGENTS.md | Target | CONSTITUTION.md | Target |
|---|---|---|---|
| Agent onboarding time (до первого корректного PR) | < 15 min | Compliance rate (PR по принципам) | > 95% |
| Context accuracy (задач без уточнений) | > 80% | Drift incidents (vibe-coding/мес) | < 2 |
| Convention violations per PR | < 1 | Principle violations caught в review | 100% |
| Agent iteration count | < 3 | Time to decision | Снижается |

Генераторы initial draft (затем кастомизация): design.dev AGENTS.md Generator, AgentsMDGenerator (VS Code), agents-md-creator (CLI, project analysis).

## Источники

- AGENTS.md spec: https://github.com/agentsmd/agents.md
- Constitution (Spec Kit): https://github.com/github/spec-kit; deep dive: https://daita.io/en/blog/spec_kit_constitution_first_principles
- Входные материалы inbox: `documentation-process-v3/05-agents-and-constitution-guide.md`, `documentation-process-v3/03-open-questions-analysis.md` (прототипы)
- Связанные KB: `ai-agent-workflows.md`, `../principles/invariants-and-gates.md`
