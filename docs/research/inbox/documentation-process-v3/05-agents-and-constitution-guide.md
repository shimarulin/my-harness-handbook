# Руководство: AGENTS.md и CONSTITUTION.md

| Параметр | Значение |
|---|---|
| Дата | 2026-09-29 |
| Статус | Draft |
| Связан с | `04-tool-selection-and-migration.md` |

---

## 1. AGENTS.md

### 1.1 Что это

**AGENTS.md** — открытый стандарт для инструкций AI-агентам. Представляет
собой Markdown-файл, расположенный в корне репозитория, который читают
все основные AI-агенты перед началом работы【turn1fetch0】【turn3fetch0】.

> «AGENTS.md is a simple, open format for guiding coding agents. Think of
> AGENTS.md as a README for agents: a dedicated, predictable place to
> provide context»【turn1fetch0】

### 1.2 Поддержка инструментами

| Инструмент | Поддержка | Приоритет |
|---|---|---|
| **OpenAI Codex** | ✅ Native | Primary |
| **Cursor** | ✅ Native | Primary |
| **Sourcegraph Amp** | ✅ Native | Primary |
| **Aider** | ✅ Native | Primary |
| **Jules (Google)** | ✅ Native | Primary |
| **Claude Code** | ✅ Читает как fallback | Secondary (CLAUDE.md primary) |
| **GitHub Copilot** | ✅ Через .github/copilot-instructions.md | Supplement |
| **RooCode** | ✅ | |

**Ключевое преимущество**: «AGENTS.md is the de-facto standard»【turn3fetch0】.
В отличие от `.cursorrules` или `CLAUDE.md`, которые работают только в одном
инструменте, AGENTS.md — кросс-инструментальный стандарт.

### 1.3 Структура файла

Согласно best practices【turn3fetch0】【turn3search2】, типичная структура:

```markdown
# [Project Name]

One-line description of the project.

This file gives AI coding agents the context they need to work
effectively in this repository.

## Stack
- **Framework**: [e.g., Next.js, Django, Spring]
- **Language**: [e.g., TypeScript, Python, Java]
- **Database**: [e.g., PostgreSQL, MongoDB]

## Setup Commands
- **install**: `npm install` / `pip install -r requirements.txt`
- **dev**: `npm run dev` / `python manage.py runserver`
- **build**: `npm run build` / `python -m build`
- **test**: `npm test` / `pytest`
- **lint**: `npm run lint` / `ruff check .`
- **typecheck**: `npx tsc --noEmit` / `mypy .`

## Project Structure
```
src/
├── components/     # UI components
├── api/           # API routes/handlers
├── lib/           # Shared utilities
├── models/        # Data models
└── tests/         # Test files
```

## Code Style
- **Language**: TypeScript everywhere, avoid `any`
- **Naming**: kebab-case files, PascalCase components, camelCase variables
- **Imports**: External → Internal → Relative; path aliases preferred
- **Formatting**: Prettier auto-format, no hand-formatting
- **Linting**: ESLint enforced, run `lint --fix` before commit

## Testing
- **Unit tests**: [Framework], co-located with source
- **E2E tests**: [Framework], in `tests/e2e/`
- **Coverage**: Happy path + at least one edge case per function
- **Philosophy**: Test behavior, not implementation

## Security
- **Secrets**: Never commit; use `.env` + `.env.example`
- **Input validation**: Schema-validate all external input
- **Auth checks**: Server-side, never rely on client guards
- **Dependencies**: No new packages without explicit approval

## Pull Requests & Commits
- **Commit format**: Conventional Commits (`feat:`, `fix:`, `chore:`)
- **PR size**: < 400 lines diff, one logical change
- **Tests**: New behavior = new tests in same PR
- **Review**: All changes via PR, no direct commits to main

## Domain Context
[Project-specific domain knowledge, business rules,
key architectural decisions]

## Known Issues & Gotchas
[Common pitfalls, workarounds, things that look wrong but aren't]
```

### 1.4 Размещение в репозитории

```
your-project/
├── AGENTS.md          ← Root of repo (universal)
├── DESIGN.md          ← Optional, for UI work
├── package.json
└── src/
    ├── module-a/
    │   └── AGENTS.md  ← Module-specific (optional)
    └── module-b/
        └── AGENTS.md  ← Module-specific (optional)
```

**Hierarchical loading**: В monorepo можно размещать дополнительные
AGENTS.md в поддиректориях — агент использует ближайший в дереве【turn3fetch0】.

### 1.5 AGENTS.md vs другие форматы

| Формат | Инструмент | Portability | Use Case |
|---|---|---|---|
| **AGENTS.md** | Все (open standard) | ✅ Cross-tool | Universal project context |
| **CLAUDE.md** | Claude Code only | ❌ Single tool | Claude-specific instructions |
| **.cursorrules** | Cursor only | ❌ Single tool | Cursor-specific rules |
| **.github/copilot-instructions.md** | Copilot only | ❌ Single tool | Copilot instructions |
| **SKILL.md** | Agent Skills spec | ✅ Cross-tool | Reusable on-demand capabilities |

**Best practice (2026)**: Layered setup — AGENTS.md как cross-tool standard,
с tool-specific files, импортирующими из него【turn4search6】.

```markdown
# CLAUDE.md (example)
@AGENTS.md

## Claude-specific additions
[Only Claude Code relevant instructions]
```

### 1.6 Инструменты для генерации AGENTS.md

| Инструмент | Тип | Источник |
|---|---|---|
| **design.dev AGENTS.md Generator** | Web, stack-aware defaults | [design.dev/ai/agents-md-generator](https://design.dev/ai/agents-md-generator) |
| **AgentsMDGenerator (VS Code)** | VS Code extension | [github.com/freelich-du/AgentsMDGenerator](https://github.com/freelich-du/AgentsMDGenerator) |
| **agents-md-creator** | CLI, project analysis | [github.com/goncalovelosa/agents-md-creator](https://github.com/goncalovelosa/agents-md-creator) |
| **Caliber AGENTS.md Generator** | Web, codebase scanning | [trycaliber.ai/agents-md-generator](https://trycaliber.ai/agents-md-generator) |
| **CursorGenerator** | Web, multiple formats | [cursorgenerator.dev/agents-md-generator](https://www.cursorgenerator.dev/agents-md-generator) |

**Рекомендация**: Использовать генератор для initial draft, затем
кастомизировать под конкретный проект.

### 1.7 Лучшие практики

#### DO:

| # | Практика | Почему |
|---|---|---|
| 1 | **Точные команды** с полными флагами | Агент не будет угадывать【turn3search3】 |
| 2 | **Конкретные версии стека** | «Next.js 14.2.3», не «Next.js»【turn3search3】 |
| 3 | **Стабильный контекст** | Не volatile информация, которая устареет【turn3search2】 |
| 4 | **Иерархическая структура** | Заголовки помогают агенту navigate【turn3fetch0】 |
| 5 | **Позитивные инструкции** | «Do X», не «Don't do Y» (кроме security) |
| 6 | **Примеры для неочевидных случаев** | Показать expected output |
| 7 | **Обновлять при изменении conventions** | Устаревший AGENTS.md хуже отсутствующего |
| 8 | **Module-specific AGENTS.md** в monorepo | Контекст ближе к коду【turn3fetch0】 |

#### DON'T:

| # | Анти-паттерн | Почему плохо |
|---|---|---|
| 1 | **Копировать README.md** | README — для людей, AGENTS.md — для агентов |
| 2 | **Дублировать tool-specific files полностью** | Maintenance overhead |
| 3 | **Volatile информация** (текущие таски, sprint status) | Быстро устаревает |
| 4 | **Слишком длинный файл** | Агент теряет контекст; держать < 500 строк |
| 5 | **Абстрактные принципы без примеров** | «Follow best practices» — бесполезно |
| 6 | **Security rules в конце** | Должны быть prominent |

---

## 2. CONSTITUTION.md

### 2.1 Что это

**CONSTITUTION.md** — файл, содержащий **immutable principles** проекта.
Это «rules of the road», которые применяются к каждому решению, каждой
спеке, каждой имплементации【turn1fetch1】【turn0search10】.

> «The constitution is supposed to contain the high level principles
> that are "immutable" and should always be applied, to every change»【turn0search7】

### 2.2 Происхождение

Концепция введена **GitHub Spec Kit**【turn0search10】, где constitution
создаётся командой `/speckit.constitution` и хранится в
`.specify/memory/constitution.md`. Впоследствии концепция была принята
шире как общий паттерн для SDD-workflows.

### 2.3 Назначение

| Роль | Что даёт |
|---|---|
| **Архитектурный контракт** | Consistency across features, teams, AI output【turn1fetch1】 |
| **Baseline для QA** | «No silent failures», «test critical paths» — проверяемые ожидания【turn1fetch1】 |
| **Steering для AI-агентов** | Агент знает «how we build here»【turn1fetch1】 |
| **Decision filter** | Каждое решение проходит через принципы |

### 2.4 Структура

Согласно шаблону【turn1fetch1】:

```markdown
# [PROJECT_NAME] Constitution

## Core Principles

### I. [Principle Name]
[Description with specific, actionable rules]

### II. [Principle Name]
[Description]

### III. [Principle Name] (NON-NEGOTIABLE)
[Description]

...

## [Additional Section]
[Technology stack requirements, compliance standards, etc.]

## [Development Workflow]
[Code review requirements, testing gates, etc.]

## Governance
[How constitution supersedes other practices; amendment process]
```

### 2.5 Примеры принципов

#### Из реальных проектов【turn0search14】:

```
1. Prototype-First Development
   - Work on test datasets before scaling
   - Validate approach before full implementation

2. Fail Fast, Never Silently
   - No silent defaults or error swallowing
   - Every failure must be explicit and logged

3. Test-First (NON-NEGOTIABLE)
   - TDD mandatory: Tests written → User approved → Tests fail → Then implement
   - Red-Green-Refactor cycle strictly enforced

4. Integration Testing
   - Focus: New library contract tests, Contract changes,
     Inter-service communication, Shared schemas

5. Observability
   - Text I/O ensures debuggability
   - Structured logging required
```

#### Из Daita.io (distributed systems)【turn0search6】:

```
- Idempotency: All operations must be idempotent
- Exactly-once semantics where possible
- Event sourcing over CRUD for audit trails
- Backpressure handling mandatory
- Circuit breakers on all external calls
```

### 2.6 Что включать vs НЕ включать

#### Включать (immutable principles):

| Тип | Пример |
|---|---|
| **Architecture principles** | «Microservices over monolith», «Event-driven» |
| **Quality gates** | «TDD mandatory», «100% coverage on critical paths» |
| **Security baselines** | «No secrets in code», «Server-side auth always» |
| **Technology constraints** | «PostgreSQL only for persistence», «No NoSQL» |
| **Team conventions** | «Conventional Commits», «PR < 400 lines» |
| **Domain rules** | «Financial calculations: integer cents only» |

#### НЕ включать (feature-specific):

| Тип | Почему |
|---|---|
| Текущие фичи | Меняются каждый sprint |
| Specific API designs | Детали, не принципы |
| Временные workarounds | Не immutable |
| Team roster | Изменяется |
| Sprint planning | Volatile |

### 2.7 AGENTS.md vs CONSTITUTION.md

| Аспект | AGENTS.md | CONSTITUTION.md |
|---|---|---|
| **Назначение** | Операционные правила «как работать» | Принципы «почему так строим» |
| **Изменяемость** | Обновляется регулярно | Immutable, изменение через RFC |
| **Аудитория** | AI-агенты + разработчики | Все участники + агенты |
| **Scope** | Repository-wide | Project-wide (cross-repo возможно) |
| **Пример** | «Run `npm test` before commit» | «Test-first development is mandatory» |
| **Расположение** | Root of repo | Root of repo (или .specify/memory/) |

### 2.8 Совместное использование

```
AI Agent reads:
1. CONSTITUTION.md  → «What are the inviolable principles?»
2. AGENTS.md        → «How do I work in this repo?»
3. specs/<feature>/ → «What am I building now?»
```

**В AGENTS.md:**

```markdown
## Mandatory Context (read before any task)

1. **CONSTITUTION.md** — project principles (immutable)
2. **This file (AGENTS.md)** — operational rules
3. **Related specification** — `docs/specs/<NNN-slug>/spec.md`
4. **Relevant ADRs** — `docs/adr/`
```

---

## 3. Спецификация AGENTS.md (agents.md)

### 3.1 Open Standard

AGENTS.md — **open specification**, размещённая на GitHub:
[github.com/agentsmd/agents.md](https://github.com/agentsmd/agents.md)【turn1fetch0】

### 3.2 Ключевые аспекты стандарта

| Аспект | Описание |
|---|---|
| **Format** | Plain Markdown |
| **Location** | Root of repository, named exactly `AGENTS.md` |
| **Encoding** | UTF-8 |
| **Hierarchy** | Agents use closest AGENTS.md in directory tree |
| **Fallback** | Tool-specific files may supplement, not replace |

### 3.3 Adoption

> «Adoption is now broad enough that AGENTS.md is the de-facto
> standard»【turn3fetch0】

---

## 4. Шаблоны для немедленного использования

### 4.1 Minimal AGENTS.md (для маленьких проектов)

```markdown
# [Project Name]

[One-line description]

## Setup
- `npm install` — install dependencies
- `npm run dev` — start dev server
- `npm test` — run tests
- `npm run lint` — lint code

## Rules
1. TypeScript strict mode, no `any`
2. Write tests for new features
3. Conventional Commits (`feat:`, `fix:`, `chore:`)
4. No direct commits to main; PR required

## Structure
```
src/
├── api/         # API endpoints
├── components/  # UI components
├── lib/         # Utilities
└── tests/       # Tests
```
```

### 4.2 Full AGENTS.md (для production проектов)

(см. §1.3 для полной структуры)

### 4.3 Minimal CONSTITUTION.md

```markdown
# [Project] Constitution

## Principles

1. **Security first**: No secrets in code. Server-side auth mandatory.
2. **Test-driven**: New features require tests before implementation.
3. **Simplicity**: YAGNI. Start simple, add complexity only when needed.
4. **Explicit failure**: No silent errors. Fail fast, fail loudly.

## Governance
- Changes to this file require team consensus
- All PRs must comply with these principles
```

---

## 5. Метрики успеха

### 5.1 Для AGENTS.md

| Метрика | Как измерить | Target |
|---|---|---|
| **Agent onboarding time** | Время до первого корректного PR | < 15 min |
| **Context accuracy** | Процент задач без уточнений | > 80% |
| **Convention violations** | Нарушений per PR | < 1 |
| **Agent iteration count** | Итераций до корректного кода | < 3 |

### 5.2 Для CONSTITUTION.md

| Метрика | Как измерить | Target |
|---|---|---|
| **Compliance rate** | PR, соответствующие принципам | > 95% |
| **Drift incidents** | Случаев vibe-coding per month | < 2 |
| **Principle violations caught** | Нарушений, пойманных в review | 100% |
| **Time to decision** | Время на architectural decision | Снижение со временем |

---

## 6. Источники

| Ресурс | Тип | Ссылка |
|---|---|---|
| AGENTS.md Spec | Open standard | [github.com/agentsmd/agents.md](https://github.com/agentsmd/agents.md) |
| Complete Guide (AI Hero) | Tutorial | [aihero.dev](https://www.aihero.dev) |
| Design.dev Generator | Tool | [design.dev/ai/agents-md-generator](https://design.dev/ai/agents-md-generator) |
| AgentsMDGenerator (VS Code) | Tool | [github.com/freelich-du/AgentsMDGenerator](https://github.com/freelich-du/AgentsMDGenerator) |
| agents-md-creator | Tool | [github.com/goncalovelosa/agents-md-creator](https://github.com/goncalovelosa/agents-md-creator) |
| Spec Kit Constitution | Template | [github.com/github/spec-kit](https://github.com/github/spec-kit) |
| Constitution Deep Dive | Article | [daita.io](https://daita.io/en/blog/spec_kit_constitution_first_principles) |
| Millan Kaul Guide | Article | [qualitywithmillan.github.io](https://qualitywithmillan.github.io/blog/ai/constitution-md-spec-driven-development.html) |
| BuildBetter Comparison | Guide | [blog.buildbetter.ai](https://blog.buildbetter.ai) |
| Augment Code Guide | Tutorial | [augmentcode.com](https://www.augmentcode.com) |
