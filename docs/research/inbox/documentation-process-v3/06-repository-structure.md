# Структура репозитория: процессы v3

| Параметр | Значение |
|---|---|
| Дата | 2026-09-29 |
| Статус | Draft |
| Связан с | `02-process-design.md`, `04-tool-selection-and-migration.md` |

---

## 1. Принципы раскладки

| # | Принцип | Следствие |
|---|---|---|
| R1 | Один репозиторий — один source of truth | Все артефакты в git |
| R2 | Совместимость с обоими инструментами | Spec Kit и OpenSpec работают в одной структуре |
| R3 | Предсказуемость | Единая раскладка во всех проектах организации |
| R4 | Machine-readable | YAML front-matter в каждом артефакте |
| R5 | Сквозная трассировка | ID и связи между артефактами |
| R6 | Открытые форматы | Только Markdown, YAML, PlantUML, Gherkin |
| R7 | CI-friendly | Структура поддерживает lint, validate, build |

## 2. Зависимости от инструментов

### 2.1 Что требуют инструменты

| Инструмент | Каталог | Содержимое | Обязательно? |
|---|---|---|---|
| **Spec Kit** | `.specify/` | memory/constitution.md, templates/, scripts/ | Да (при использовании) |
| **Spec Kit** | `specs/` | Фича-артефакты (spec.md, plan.md, tasks.md) | Да (при использовании) |
| **OpenSpec** | `openspec/` | config.yaml, specs/, changes/ | Да (при использовании) |
| **MADR** | `docs/decisions/` | ADR-файлы | Да (всегда) |

### 2.2 Стратегия совместимости

**Подход**: оба инструмента работают в своих канонических каталогах,
а общие артефакты (ADR, PRD, RFC) живут в `docs/` — общей территории.

```
Специфика Spec Kit:  .specify/ + specs/
Специфика OpenSpec:  openspec/
Общая территория:    docs/ + tasks/ + tests/ + api/
Корневые файлы:      AGENTS.md, CONSTITUTION.md, README.md
```

---

## 3. Структура репозитория (Monorepo)

### 3.1 Полная раскладка

```
project/
│
├── AGENTS.md                          # Cross-tool правила для AI-агентов
├── CONSTITUTION.md                    # Immutable principles проекта
├── README.md                          # Входная точка для людей
├── mkdocs.yml                         # Конфигурация сайта документации
├── .markdownlint-cli2.jsonc          # Конфигурация markdownlint
├── .pre-commit-config.yaml           # Pre-commit hooks
│
├── docs/                              # Общая документация
│   ├── process/                       # Документация процессов (этот документ)
│   │   ├── 00-goals.md
│   │   ├── 01-knowledge-summary.md
│   │   ├── 02-process-design.md
│   │   ├── 03-open-questions-analysis.md
│   │   ├── 04-tool-selection-and-migration.md
│   │   ├── 05-agents-and-constitution-guide.md
│   │   ├── 06-repository-structure.md     # Этот файл
│   │   └── templates/                     # Шаблоны артефактов
│   │       ├── idea-template.md
│   │       ├── task-template.md
│   │       ├── prd-template.md
│   │       ├── rfc-template.md
│   │       ├── adr-template.md            # MADR 4.0.0
│   │       └── spec-template.md
│   │
│   ├── decisions/                     # ADR (MADR format)
│   │   ├── 0001-record-architecture-decisions.md
│   │   ├── 0002-choose-spec-driven-development.md
│   │   ├── 0003-select-primary-sdd-tool.md
│   │   └── NNNN-slug.md
│   │
│   ├── prd/                           # Product Requirements Documents
│   │   ├── _index.md                  # Auto-generated список
│   │   └── NNN-slug.md
│   │
│   ├── rfc/                           # Request for Comments / Design Docs
│   │   ├── _index.md
│   │   └── NNNN-slug.md
│   │
│   ├── ideas/                         # Кандидаты-идеи
│   │   ├── _index.md                  # Auto-generated, фильтр по статусу
│   │   └── NNN-slug.md
│   │
│   ├── architecture/                  # Архитектурная документация
│   │   ├── c4/                        # C4-диаграммы
│   │   │   ├── context.puml
│   │   │   ├── container.puml
│   │   │   ├── component.puml
│   │   │   └── dynamic.puml
│   │   └── arc42/                     # arc42 (для L4 проектов)
│   │       ├── 01-introduction-and-goals.md
│   │       ├── 02-architecture-constraints.md
│   │       └── ...
│   │
│   ├── quality/                       # Quality scenarios
│   │   └── NNN-slug.md
│   │
│   └── research/                      # Research compendia
│       └── NNN-slug/
│           ├── README.md
│           ├── data/
│           ├── analysis/
│           └── Dockerfile
│
├── tasks/                             # L1-задачи (лёгкий трек)
│   ├── _index.md
│   └── NNN-slug.md
│
├── tests/
│   ├── specs/                         # Gauge Markdown-спецификации
│   │   └── NNN-slug/
│   │       └── spec.md
│   └── features/                      # Gherkin (опционально)
│       └── NNN-slug.feature
│
├── api/                               # API-контракты
│   ├── openapi.yaml
│   └── asyncapi.yaml
│
├── .ai/                               # AI-специфичные конфигурации
│   ├── rules.md                       # Дополнительные правила агентов
│   └── workflows/                     # Агентские workflow (optional)
│
├── .github/                           # CI/CD
│   └── workflows/
│       ├── docs.yml                   # Docs pipeline
│       └── trace-check.yml            # Traceability validation
│
├── openspec/                          # OpenSpec (если используется)
│   ├── config.yaml                    # Проектная конфигурация
│   ├── specs/                         # Canonical specs (source of truth)
│   │   ├── auth/
│   │   │   └── spec.md
│   │   └── payments/
│   │       └── spec.md
│   └── changes/                       # Активные изменения
│       ├── add-user-auth/
│       │   ├── .openspec.yaml
│       │   ├── proposal.md
│       │   ├── specs/
│       │   │   └── user-auth/
│       │   │       └── spec.md        # Delta spec
│       │   ├── design.md
│       │   └── tasks.md
│       └── archive/                   # Завершённые изменения
│           └── 2026-01-15-add-oauth/
│
├── .specify/                          # Spec Kit (если используется)
│   ├── memory/
│   │   └── constitution.md            # Constitution Spec Kit
│   ├── templates/
│   │   ├── spec-template.md
│   │   ├── plan-template.md
│   │   ├── tasks-template.md
│   │   └── constitution-template.md
│   └── scripts/                       # Workflow scripts
│
├── specs/                             # Spec Kit фича-артефакты
│   └── <feature-name>/
│       ├── spec.md
│       ├── plan.md
│       └── tasks.md
│
└── src/                               # Исходный код
    ├── ...
    └── ...
```

### 3.2 Минимальная структура (L1–L2 проекты)

Для малых проектов, где не нужны оба SDD-инструмента:

```
project/
├── AGENTS.md
├── CONSTITUTION.md
├── README.md
├── docs/
│   ├── decisions/                     # ADR (обязательно)
│   │   └── 0001-record-architecture-decisions.md
│   ├── ideas/
│   │   └── _index.md
│   └── process/
│       └── templates/
│           ├── task-template.md
│           └── adr-template.md
├── tasks/
│   └── _index.md
├── tests/
│   └── specs/
└── openspec/                          # ИЛИ .specify/ (один из них)
    ├── config.yaml
    ├── specs/
    └── changes/
```

---

## 4. Идентификация и трассировка

### 4.1 ID-система

| Артефакт | Формат ID | Пример | Каталог |
|---|---|---|---|
| **Idea** | `idea-NNN` | `idea-042` | `docs/ideas/` |
| **Task (L1)** | `task-NNN` | `task-017` | `tasks/` |
| **PRD** | `prd-NNN` | `prd-005` | `docs/prd/` |
| **RFC** | `rfc-NNNN` | `rfc-0031` | `docs/rfc/` |
| **ADR** | `adr-NNNN` | `adr-0007` | `docs/decisions/` |
| **Spec (OpenSpec)** | `<capability-path>` | `user-auth` | `openspec/specs/` |
| **Change (OpenSpec)** | `<change-name>` | `add-user-auth` | `openspec/changes/` |
| **Feature (Spec Kit)** | `<feature-name>` | `user-authentication` | `specs/` |
| **Quality scenario** | `quality-NNN` | `quality-003` | `docs/quality/` |
| **Research** | `research-NNN` | `research-001` | `docs/research/` |

### 4.2 Front-matter Schema (общий)

Каждый Markdown-артефакт начинается с YAML front-matter:

```yaml
---
# Обязательные поля
id: <artifact-id>           # Уникальный ID (см. §4.1)
type: <artifact-type>       # idea | task | prd | rfc | adr | spec | change
status: <status>            # draft | review | approved | rejected | superseded | archived
created: YYYY-MM-DD         # Дата создания
title: <human-readable>     # Заголовок

# Опциональные поля (трассировка)
traces: []                  # ID артефактов-предшественников
relates_to: []              # ID связанных артефактов
deciders: []                # Кто принял решение (для ADR)
consulted: []               # Кого консультировали
informed: []                # Кого информировали
tags: []                    # Теги для фильтрации
priority: P0|P1|P2|P3      # Приоритет (для ideas, tasks)
level: L0|L1|L2|L3|L4      # Уровень масштаба
---
```

### 4.3 Правила трассировки

| Правило | Пример |
|---|---|
| **Idea → Task**: при promotion | `traces: [idea-042]` в task-017 |
| **Task → PRD**: при развитии | `traces: [task-017]` в prd-005 |
| **PRD → RFC**: при необходимости дебатов | `traces: [prd-005]` в rfc-0031 |
| **RFC → ADR**: при принятии решения | `traces: [rfc-0031]` в adr-0007 |
| **Spec ↔ ADR**: двусторонняя связь | `relates_to: [adr-0007]` в spec |
| **Change → Spec**: в OpenSpec | Proposal ссылается на capability paths |

### 4.4 Статусы

| Статус | Описание | Переход |
|---|---|---|
| `draft` | Черновик, в работе | → `review` |
| `review` | На ревью | → `approved` или `rejected` |
| `approved` | Принят к работе | → `archived` (для changes) |
| `rejected` | Отклонён | Финальный |
| `superseded` | Заменён другим | Финальный, нужен `superseded_by` |
| `archived` | Завершён (OpenSpec changes) | Финальный |
| `promoted` | Idea→Task, Task→PRD | Промежуточный |
| `candidate` | Idea на рассмотрении | → `promoted` или `rejected` |

---

## 5. Шаблоны артефактов

### 5.1 Idea Template (`docs/process/templates/idea-template.md`)

```markdown
---
id: idea-NNN
type: idea
status: candidate
created: YYYY-MM-DD
title: <Идея в одну строку>
priority: P1
tags: []
---

# Идея: <title>

## Проблема / Возможность

<1–3 предложения: какую проблему решаем или какую возможность видим>

## Предлагаемое решение

<1–2 предложения: что предлагаем сделать>

## Почему сейчас

<Почему это важно сейчас, а не потом>

## Оценка

| Критерий | Оценка |
|---|---|
| Влияние | High / Medium / Low |
| Усилия | High / Medium / Low |
| Риск | High / Medium / Low |
| Зависимости | <список или "нет"> |

## Открытые вопросы

- <вопрос 1>
- <вопрос 2>
```

### 5.2 Task Template (`docs/process/templates/task-template.md`)

```markdown
---
id: task-NNN
type: task
status: draft
created: YYYY-MM-DD
title: <Задача в одну строку>
traces: []              # idea-NNN если promoted
level: L1
tags: []
---

# Задача: <title>

## Job Story

```
When <situation>
I want <motivation>
So I can <expected outcome>
```

## Критерии готовности

- [ ] <критерий 1>
- [ ] <критерий 2>
- [ ] Тесты написаны и проходят
- [ ] Документация обновлена

## Контекст

<Ссылки на related ADR, specs, другие задачи>

## Заметки

<Дополнительная информация, discovered during work>
```

### 5.3 PRD Template (`docs/process/templates/prd-template.md`)

```markdown
---
id: prd-NNN
type: prd
status: draft
created: YYYY-MM-DD
title: <Feature/product name>
traces: []              # task-NNN если развилась из задачи
level: L2
tags: []
---

# PRD: <title>

## Overview

<1 paragraph: что это и для кого>

## Problem

<User pain или business opportunity. Include evidence.>

## Goals

- <Measurable outcome 1>
- <Measurable outcome 2>

## Non-goals

- <What we are explicitly NOT doing>

## Requirements / User Stories

- As a <user>, I want <capability> so that <benefit>.
- Priority: Must / Should / Could

## Success Metrics

| Metric | Target | How to measure |
|---|---|---|
| <metric> | <target> | <method> |

## Constraints & Assumptions

- <Deadlines, dependencies, platform limits>

## Open Questions

| Question | Status | Answer |
|---|---|---|
| <question> | open / resolved | <answer> |
```

### 5.4 RFC Template (`docs/process/templates/rfc-template.md`)

```markdown
---
id: rfc-NNNN
type: rfc
status: draft
created: YYYY-MM-DD
title: <RFC title>
traces: []              # prd-NNN обычно
level: L3
reviewers: []
tags: []
---

# RFC: <title>

## Status

Draft | In Review | Approved | Rejected | Superseded

## Context and Scope

<Current state, why this RFC exists. Link to PRD/Spec.>

## Goals and Non-goals

**Goals:**
- <what this RFC achieves>

**Non-goals:**
- <what is explicitly out of scope>

## Proposal

<Detailed design proposal. Include diagrams if helpful.>

## Alternatives Considered

### Alternative 1: <name>

- **Description**: <what>
- **Pros**: <advantages>
- **Cons**: <disadvantages>
- **Why not chosen**: <reason>

### Alternative 2: <name>

<...>

## Trade-offs and Risks

| Risk | Impact | Mitigation |
|---|---|---|
| <risk> | <high/medium/low> | <mitigation> |

## Open Questions

- <question for reviewers>

## References

- <links to related ADRs, specs, external resources>
```

### 5.5 ADR Template — MADR 4.0.0 (`docs/process/templates/adr-template.md`)

```markdown
---
id: adr-NNNN
type: adr
status: proposed         # proposed | accepted | deprecated | superseded
created: YYYY-MM-DD
title: <Decision title>
deciders: []             # Who made the decision
consulted: []            # Who was consulted
informed: []             # Who was informed
traces: []               # rfc-NNNN if came from RFC
tags: []
superseded_by: null      # adr-NNNN if superseded
---

# <NNNN.> <Title>

## Context and Problem Statement

<What is the issue that we're seeing that is motivating this decision or change?>

## Decision Drivers

- <driver 1>
- <driver 2>

## Considered Options

- <option 1>
- <option 2>
- <option 3>

## Decision Outcome

Chosen option: "<option>", because
<justification. e.g., only option which meets k.o. criterion>
<!-- optional: other reasons -->

### Consequences

- Good, because <positive consequence>
- Bad, because <negative consequence>
- Neutral, because <consequence>

### Confirmation

<How will we know the decision was implemented correctly?>

## Pros and Cons of the Options

### <option 1>

- Good, because <pro>
- Bad, because <con>
- Neutral, because <con>

### <option 2>

- Good, because <pro>
- Bad, because <con>

## More Information

<links to related ADRs, RFCs, external resources>
```

### 5.6 Spec Template — для OpenSpec delta specs

```markdown
# Spec Delta: <capability-path>

## Purpose
<One-two sentences (50+ chars) on what this capability is for. 
Delete for existing capabilities.>

## ADDED Requirements

### Requirement: <name>
<requirement text using SHALL/MUST>

#### Scenario: <name>
- **WHEN** <condition>
- **THEN** <expected outcome>

## MODIFIED Requirements

### Requirement: <existing name>
<full updated content — copy ENTIRE requirement block>

#### Scenario: <existing scenario name>
- **WHEN** <updated condition>
- **THEN** <updated outcome>

## REMOVED Requirements

### Requirement: <name>
**Reason**: <why removed>
**Migration**: <how to migrate>
```

---

## 6. Вариант: Split Repository (два репо)

### 6.1 Когда использовать

| Ситуация | Почему |
|---|---|
| Публичная документация, приватный код | OSS-проект с закрытыми internal specs |
| Мультипроектная документация | Один docs-repo на несколько продуктов |
| Разные access levels | Docs для всех, код для команды |

### 6.2 Структура

```
# Репозиторий 1: project-docs
docs-repo/
├── AGENTS.md                       # Для AI-агентов docs
├── CONSTITUTION.md                 # Общие принципы
├── README.md
├── docs/
│   ├── decisions/                  # ADR (все)
│   ├── prd/
│   ├── rfc/
│   ├── ideas/
│   ├── architecture/
│   └── process/
├── openspec/                       # Canonical specs (если OpenSpec)
│   ├── config.yaml
│   └── specs/
└── mkdocs.yml

# Репозиторий 2: project-code  
code-repo/
├── AGENTS.md                       # Для AI-агентов кода (ссылается на docs-repo)
├── CONSTITUTION.md                 # Симлинк или copy из docs-repo
├── README.md
├── specs/                          # Spec Kit фичи (если Spec Kit)
├── .specify/
├── openspec/
│   └── changes/                    # Активные изменения
├── tasks/
├── tests/
├── api/
└── src/
```

### 6.3 Cross-repo трассировка

В docs-repo ADR может ссылаться на code-repo:

```yaml
---
id: adr-0007
type: adr
traces: [rfc-0031]
relates_to: [repo:project-code:spec:user-auth]
---
```

В code-repo артефакты ссылаются на docs-repo:

```yaml
---
id: spec-user-auth
type: spec
traces: [repo:project-docs:adr-0007]
---
```

---

## 7. Совместимость с инструментами

### 7.1 Spec Kit работает

| Функция Spec Kit | Каталог | Совместимость |
|---|---|---|
| `/speckit.constitution` | `.specify/memory/constitution.md` | ✅ Собственный |
| `/speckit.specify` | `specs/<feature>/spec.md` | ✅ Собственный |
| `/speckit.plan` | `specs/<feature>/plan.md` | ✅ Собственный |
| `/speckit.tasks` | `specs/<feature>/tasks.md` | ✅ Собственный |
| `/speckit.implement` | Работает с specs/ | ✅ Собственный |

### 7.2 OpenSpec работает

| Функция OpenSpec | Каталог | Совместимость |
|---|---|---|
| `openspec init` | Создаёт `openspec/` | ✅ Собственный |
| `/opsx:propose` | `openspec/changes/<name>/` | ✅ Собственный |
| `/opsx:apply` | Работает с changes/ | ✅ Собственный |
| `openspec archive` | Перемещает в `changes/archive/` | ✅ Собственный |
| Canonical specs | `openspec/specs/` | ✅ Собственный |

### 7.3 Общие артефакты (работают в обоих)

| Артефакт | Каталог | Использование |
|---|---|---|
| ADR | `docs/decisions/` | Оба инструмента могут ссылаться |
| PRD | `docs/prd/` | Источник для обоих |
| RFC | `docs/rfc/` | Дебаты до выбора инструмента |
| Ideas | `docs/ideas/` | Pipeline до SDD |
| Constitution | `CONSTITUTION.md` | Общий (Spec Kit может symlink) |
| AGENTS.md | `AGENTS.md` | Cross-tool правила |

### 7.4 Конфигурация для обоих

**AGENTS.md описывает оба workflow:**

```markdown
## Workflow Selection

- **Read CONSTITUTION.md first** — applies to all work
- **Feature development**: Use OpenSpec (/opsx:* commands)
  - Creates: openspec/changes/<name>/
  - Or: Use Spec Kit (/speckit.* commands)
  - Creates: specs/<feature>/
- **Architectural decisions**: Always create ADR in docs/decisions/
- **Product requirements**: Create PRD in docs/prd/
```

---

## 8. Naming Conventions

### 8.1 Файлы

| Артефакт | Pattern | Пример |
|---|---|---|
| ADR | `NNNN-title-with-dashes.md` | `0007-use-postgresql.md` |
| PRD | `NNN-slug.md` | `005-user-authentication.md` |
| RFC | `NNNN-slug.md` | `0031-api-redesign.md` |
| Idea | `NNN-slug.md` | `042-dark-mode.md` |
| Task | `NNN-slug.md` | `017-fix-login-bug.md` |
| OpenSpec change | `<kebab-case-name>/` | `add-user-auth/` |
| OpenSpec capability | `<kebab-case-path>/` | `user-auth/`, `identity/user-auth/` |
| Spec Kit feature | `<kebab-case-name>/` | `user-authentication/` |

### 8.2 Правила

| Правило | Пример |
|---|---|
| Все lowercase | `use-postgresql` ✅, `Use-PostgreSQL` ❌ |
| Слова через дефис | `api-redesign` ✅, `api_redesign` ❌ |
| ADR: 4-значная нумерация | `0001`, `0042`, `0999` |
| PRD/RFC/Idea/Task: 3-значная | `001`, `042`, `999` |
| OpenSpec capabilities: kebab-case | `user-auth` ✅, `UserAuth` ❌ |
| Заголовок ADR: полные предложения | `Use PostgreSQL for primary database` |

---

## 9. CI/CD Integration Points

### 9.1 Что проверяет CI

```yaml
# .github/workflows/docs.yml (концепция)
name: docs
on: [pull_request, push]
jobs:
  lint:
    # markdownlint на все .md
    # yamllint на front-matter
  trace:
    # Валидация ID, статусов, связей traces
    # Проверка: superseded ADR имеет superseded_by
  adr-lint:
    # MADR format validation
  structure:
    # Проверка раскладки каталогов
    # Все ADR в docs/decisions/ с правильной нумерацией
  build:
    # mkdocs build
  openspec-validate:
    # openspec validate (если есть openspec/)
  spec-kit-check:
    # specify check (если есть .specify/)
```

### 9.2 Pre-commit hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/igorshubovych/markdownlint-cli
    rev: v0.40.0
    hooks:
      - id: markdownlint-cli2
  - repo: https://github.com/adrienverhall/yamllint
    rev: v1.35.1
    hooks:
      - id: yamllint
        args: [-d, relaxed]
```

---

## 10. Migration Notes

### 10.1 Из существующего проекта без SDD

```
Phase 1: Создать минимальную структуру
├── CONSTITUTION.md (new)
├── AGENTS.md (new)
├── docs/decisions/0001-record-architecture-decisions.md (new)
└── docs/process/templates/ (copy from this document)

Phase 2: Выбрать SDD-инструмент
├── OpenSpec: openspec init
└── Spec Kit: specify init --agent <agent>

Phase 3: Мигрировать существующую документацию
├── Design docs → docs/rfc/
├── Wiki pages → docs/ (по типу)
└── Решения из чатов → docs/decisions/
```

### 10.2 Смена SDD-инструмента

(детали в `04-tool-selection-and-migration.md` §3)

```
Spec Kit → OpenSpec:
1. npm install -g @fission-ai/openspec
2. openspec init
3. Мигрировать specs/<feature>/ → openspec/changes/<name>/
4. cp .specify/memory/constitution.md CONSTITUTION.md
5. Обновить AGENTS.md

OpenSpec → Spec Kit:
1. uv tool install specify-cli
2. specify init --agent <agent>
3. Мигрировать openspec/changes/<id>/ → specs/<feature>/
4. cp CONSTITUTION.md .specify/memory/constitution.md
5. Обновить AGENTS.md
```

---

## 11. Checklist: новый проект

- [ ] Создать `CONSTITUTION.md` (см. `05-agents-and-constitution-guide.md` §2)
- [ ] Создать `AGENTS.md` (см. `05-agents-and-constitution-guide.md` §1)
- [ ] Создать `README.md` с обзором проекта
- [ ] Создать `docs/decisions/0001-record-architecture-decisions.md`
- [ ] Скопировать шаблоны в `docs/process/templates/`
- [ ] Создать `docs/ideas/_index.md`
- [ ] Создать `tasks/_index.md`
- [ ] Инициализировать SDD-инструмент (OpenSpec ИЛИ Spec Kit)
- [ ] Настроить `mkdocs.yml` для публикации документации
- [ ] Настроить `.markdownlint-cli2.jsonc`
- [ ] Настроить `.pre-commit-config.yaml`
- [ ] Создать `.github/workflows/docs.yml`
- [ ] Настроить CI для traceability-проверок

---

## 12. Источники

| Ресурс | Что даёт | Ссылка |
|---|---|---|
| OpenSpec Directory Structure | Каноническая раскладка openspec/ | [deepwiki.com/Fission-AI/OpenSpec](https://deepwiki.com/Fission-AI/OpenSpec/4.1-directory-structure) |
| OpenSpec spec-driven schema | Артефакты и workflow | [openspec.dev/docs/schemas/spec-driven](https://openspec.dev/docs/schemas/spec-driven) |
| Spec Kit Templates | Шаблоны spec/plan/tasks | [github.com/github/spec-kit/tree/main/templates](https://github.com/github/spec-kit/tree/main/templates) |
| Spec Kit Documentation | Обзор процессов | [github.github.com/spec-kit](https://github.github.com/spec-kit) |
| MADR | Формат ADR + шаблон | [adr.github.io/madr](https://adr.github.io/madr) |
| MADR Template | Полный шаблон 4.0.0 | [github.com/adr/madr](https://github.com/adr/madr) |
