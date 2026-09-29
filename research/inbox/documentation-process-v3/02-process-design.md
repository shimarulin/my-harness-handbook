# Модель процессов разработки ПО v3 (черновик)

| Параметр | Значение |
|---|---|
| Дата | 2026-09-28 |
| Статус | Draft v0.1 |
| Связан с | `00-goals.md`, `01-knowledge-summary.md` |

---

## 1. Общая модель

Процесс — это **пайплайн артефактов** в git. Каждый артефакт:

- файл открытого формата (Markdown/YAML/PlantUML/Gherkin);
- имеет уникальный ID и статус (draft → approved / superseded);
- ссылается на артефакт-предшественник (трассировка);
- проходит через **approval-гейт**, где решение принимает человек.

```
┌──────┐   ┌───────┐   ┌────────────┐   ┌───────┐   ┌──────┐   ┌──────┐   ┌─────────┐
│ IDEA │ → │ PRD / │ → │ RFC /      │ → │ SPEC  │ → │ ADR  │ → │ CODE │ → │ RELEASE │
│      │   │ JOB   │   │ DESIGN DOC │   │ EARS/ │   │(MADR)│   │+TESTS│   │ NOTES   │
│      │   │ STORY │   │            │   │ GHERK │   │      │   │      │   │         │
└──────┘   └───────┘   └────────────┘   └───────┘   └──────┘   └──────┘   └─────────┘
  human       human        human +          human        human      AI +        AI +
  capture     authored     AI draft         approves     approves   human       human
```

**Docs-first правило**: переход на следующий этап возможен только когда
артефакт предыдущего этапа имеет статус `approved` (кроме L0).

## 2. Уровни масштаба (Scale Levels)

Уровень выбирается автором инициативы при создании артефакта идеи.
Уровень можно **повышать** в процессе (артефакты не выбрасываются).

### L0 — Trivial (typo, hotfix, рефакторинг без поведенческих изменений)

Обязательные артефакты: **нет**.
В коммит-сообщении: `trivial: <описание>`.
AI-агент может выполнять без спеки, но человек ревьюит PR.

### L1 — Small (локальное изменение, один контекст)

| Этап | Артефакт | Формат |
|---|---|---|
| Idea+Spec | `tasks/NNN-task.md` | Markdown: Job Story + tasks-чеклист |
| Реализация | PR, связанный с задачей | Git |

Overhead: ~10–15 минут. Подходит для AI-агента в одном context window.

### L2 — Feature (фича, несколько сессий/людей)

| Этап | Артефакт | Формат |
|---|---|---|
| Product | `docs/prd/NNN-*.md` (PRD-lite) | Markdown |
| Spec | `docs/specs/NNN-*/spec.md` | EARS-требования |
| Tasks | `docs/specs/NNN-*/tasks.md` | Markdown-чеклист |
| Design | `docs/specs/NNN-*/design.md` (notes) | Markdown |
| Реализация | PR-ы, каждый ссылается на spec | Git |

### L3 — Major (крупная фича, архитектурные последствия)

Всё из L2, плюс:

| Этап | Артефакт | Формат |
|---|---|---|
| Debate | `docs/rfq/NNNN-*.md` (RFC/Design Doc) | Markdown (Google DD-структура) |
| Decisions | `docs/adr/NNNN-*.md` (MADR) | Markdown |
| Behavior | `docs/specs/NNN-*/scenarios/*.feature` | Gherkin |
| Architecture | `docs/architecture/` (C4-диаграммы) | PlantUML/Mermaid |

### L4 — Platform/Product (новая платформа, продукт)

Всё из L3, плюс:

| Этап | Артефакт | Формат |
|---|---|---|
| Product | PRD полный + Amazon PR/FAQ | Markdown |
| Architecture | arc42-документ (12 секций) + C4 все уровни | Markdown + PlantUML |
| Enterprise | ArchiMate/TOGAF — только если требуется | ArchiMate-XML |
| Quality | Quality scenarios (arc42 quality model) | Markdown |
| Repro | Research Compendium (для R&D-частей) | Markdown+Docker |

### Правила продвижения уровней

- L1→L2: task.md разворачивается в PRD (та же история, больше деталей).
- L2→L3: design notes оформляются в RFC; если принято новое архитектурное
  решение — обязательно ADR.
- L3→L4: RFC-серия консолидируется в arc42-документ.

## 3. Структура репозитория (один репо — source of truth)

```
project/
├── README.md                     # входная точка: что, зачем, статус
├── AGENTS.md                     # правила для AI-агентов (durable context)
├── CONSTITUTION.md               # постоянные принципы проекта (spec-kit style)
├── docs/
│   ├── prd/                      # PRD / PR-FAQ (L2+)
│   │   ├── NNN-slug.md
│   │   └── _index.md
│   ├── rfc/                      # RFC / Design Docs (L3+)
│   │   └── NNNN-slug.md
│   ├── adr/                      # Architecture/Any Decision Records (MADR)
│   │   ├── 0001-record-decisions.md
│   │   └── NNNN-slug.md
│   ├── specs/                    # фича-спецификации
│   │   └── NNN-slug/
│   │       ├── spec.md           # EARS-требования
│   │       ├── design.md         # дизайн (notes или полный)
│   │       ├── tasks.md          # задачный чеклист
│   │       └── scenarios/        # Gherkin (L3+)
│   ├── architecture/             # архитектура (L3+)
│   │   ├── c4/                   # .puml / .mmd диаграммы
│   │   └── arc42/                # 12 секций (L4)
│   ├── quality/                  # quality scenarios (L4)
│   └── research/                 # research compendia, эксперименты
├── tasks/                        # L1-задачи (лёгкий трек)
│   └── NNN-slug.md
├── tests/
│   └── features/                 # Gherkin-фичи (исполняемые)
├── api/                          # контракты
│   ├── openapi.yaml
│   └── asyncapi.yaml
├── .ai/
│   ├── rules.md                  # дополнительные правила агентов
│   └── workflows/                # агентские workflow (optional)
└── mkdocs.yml                    # сборка сайта документации
```

**Два репозитория — когда**: если документация открытая (public docs repo),
а код закрытый, либо документация мультипроектная. Тогда:
`project-docs/` (arc42, ADR, RFC) + `project-code/` (specs рядом с кодом,
ссылки на docs-repo по ID). Формат и ID одинаковы.

## 4. Идентификация и трассировка

Каждый артефакт получает ID при создании:

| Артефакт | Формат ID | Пример |
|---|---|---|
| Задача L1 | `task-NNN` | `task-042` |
| PRD | `prd-NNN` | `prd-017` |
| RFC | `rfc-NNNN` | `rfc-0031` |
| ADR | `adr-NNNN` | `adr-0007` |
| Spec | `spec-NNN` | `spec-012` |
| Idea | `idea-NNN` (опционально, в backlog.md) | `idea-003` |

Трассировка — через YAML front-matter каждого артефакта:

```yaml
---
id: spec-012
status: approved        # draft | review | approved | superseded | rejected
traces: prd-017         # предшественник
rfc: rfc-0031           # связанный RFC (если есть)
adr: [adr-0007]         # решения, принятые по этой спеке
created: 2026-09-28
owner: @human
---
```

CI проверяет: все `traces` существуют; статусы валидны; ADR, помеченные
`superseded`, имеют ссылку на superseding ADR.

## 5. Роли человека и AI-агента

| Этап | Человек | AI-агент |
|---|---|---|
| Idea | Формулирует (или просит агента зафиксировать из обсуждения) | Черновик `idea-*.md` из диалога/митинга |
| PRD | Ревьюит, утверждает | Черновик PRD по шаблону; собирает open questions |
| RFC | Дебатирует, утверждает | Генерирует alternatives, trade-offs, risk-секции |
| Spec (EARS) | Утверждает | Черновик EARS-требований из PRD/RFC |
| ADR | Принимает решение | Формулирует MADR-черновик по итогу обсуждения |
| Tasks | Приоритизирует | Разбиение spec → tasks.md |
| Code | Ревьюит PR | Имплементация строго по spec+tasks; сверка code↔spec перед PR |
| Tests | Ревьюит | Генерация step definitions, исполнение |
| Docs | Утверждает | Автогенерация changelog, обновление диаграмм |

**Жёсткие правила для агентов** (закрепляются в `AGENTS.md`):

1. Не имплементировать без `approved` спеки (кроме L0).
2. Перед имплементацией прочитать: CONSTITUTION.md → связанный PRD/RFC →
   spec → tasks → релевантные ADR.
3. Любое отклонение от спеки — стоп и вопрос человеку (или RFC-предложение).
4. Принципиальные решения (выбор технологии, паттерна) — не принимать,
   оформлять как draft ADR для человека.
5. Каждое завершение задачи — обновить tasks.md (чеклист) и, при
   поведенческом изменении, — scenarios.

## 6. CI/CD для документации (docs pipeline)

```yaml
# .github/workflows/docs.yml (концепция)
name: docs
on: [pull_request, push]
jobs:
  lint:
    # markdownlint, yamllint
    # madr-lint (валидация структуры ADR)
  diagrams:
    # рендер .puml / .mmd / .d2 → артефакты
  trace:
    # проверка ID, статусов, ссылок traces
  build:
    # mkdocs build (или antora)
  executable-specs:
    # запуск Gherkin-сценариев (если есть)
```

## 7. Соответствие целям (G1–G6)

| Цель | Как обеспечена |
|---|---|
| G1 Сквозной пайплайн | §1 модель + §4 трассировка ID |
| G2 Docs-first | Approval-гейты; правила агентов №1 |
| G3 Открытые форматы | Только Markdown/YAML/Gherkin/PlantUML; инструменты заменяемы |
| G4 Human+AI | §5 роли; AGENTS.md как durable context |
| G5 Масштабируемость | §2 уровни L0–L4 + правила продвижения |
| G6 Воспроизводимость | §6 docs-CI; research/ compendia; Gherkin в tests |

## 8. Открытые вопросы (для следующей итерации)

1. Выбрать primary BDD-инструмент per-стек (Cucumber vs Reqnroll vs Behave
   vs Gauge) — критерий: Gherkin-переносимость.
2. Формат PRD-шаблона: Atlassian-стиль vs Amazon PR/FAQ vs Job-Story-микс.
3. Нужен ли отдельный `backlog.md` для ideas или идеи сразу в tasks/?
4. Прототип `AGENTS.md` и `CONSTITUTION.md` — написать примеры.
5. Автоматизация создания артефактов: `specify` CLI (spec-kit) vs
   собственные скрипты vs `npx openspec`.
6. Как хранить EARS: внутри spec.md (раздел Requirements) или отдельным
   `requirements.yaml` (YADR-стиль)?

## 9. Следующие документы

- `03-repository-structure.md` — полная спецификация раскладки + шаблоны
  всех артефактов.
- `04-toolchain.md` — реестр инструментов: primary + альтернативы + критерии
  замены.
- `05-ai-collaboration.md` — полный протокол Human↔AI, шаблоны AGENTS.md,
  CONSTITUTION.md.
- `06-examples/` — заполненный пример инициативы L2 и L3 от идеи до PR.
