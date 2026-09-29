# Modules: Полная картина

Все строительные блоки для процессов разработки ПО — от идеи до конечного результата.

---

## Архитектура модулей

```
┌─────────────────────────────────────────────────────────────────────┐
│                        OPTIONAL MODULES                              │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌──────────┐ ┌────────────┐ ┌────────┐  │
│  │ PRD │ │ RFC │ │ BDD │ │ API Specs │ │ Design-First│ │ Formal │  │
│  └──┬──┘ └──┬──┘ └──┬──┘ └────┬─────┘ └─────┬──────┘ └───┬────┘  │
│     │       │       │         │              │             │        │
├─────┼───────┼───────┼─────────┼──────────────┼─────────────┼────────┤
│     ▼       ▼       ▼         ▼              ▼             ▼        │
│              EXECUTION FLOW (Phase 2)                              │
│  ┌──────────────┐  ┌───────────────┐  ┌────────────────┐          │
│  │   APPROACH   │→ │    TASKS      │→ │ IMPLEMENTATION │          │
│  │ (Design)     │  │  (Breakdown)  │  │  (Code)        │          │
│  └──────┬───────┘  └───────┬───────┘  └───────┬────────┘          │
│         │                  │                   │                    │
├─────────┼──────────────────┼───────────────────┼────────────────────┤
│         ▼                  ▼                   ▼                    │
│              CORE FOUNDATION (Phase 1)                              │
│  ┌────────────────┐  ┌──────────────┐  ┌─────────────┐            │
│  │   PROBLEM      │→ │ REQUIREMENTS │→ │     ADR     │            │
│  │   STATEMENT    │  │   (EARS)     │  │  (Decision  │            │
│  │                │  │              │  │   Record)   │            │
│  └────────────────┘  └──────────────┘  └─────────────┘            │
│                                                                      │
│  Используются ВСЕГДА. Минимальный набор для любого проекта.        │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Core Foundation (Phase 1) — Обязательные модули

Присутствуют в **любом** проекте, независимо от размера и сложности.

### 1. Problem Statement
**Файл**: [`problem-statement.md`](./problem-statement.md)

| Атрибут | Значение |
|---------|----------|
| **Что** | Краткое описание проблемы (1-3 абзаца) |
| **Когда** | Всегда в начале любой работы |
| **Кто** | Любой участник |
| **Формат** | Markdown |
| **Хранение** | В начале spec/RFC/PRD или отдельным файлом |

**Техники**: 5 Whys, Problem-User-Impact Matrix, Before/After Bridge, JTBD

**Связь**: → Requirements, → RFC, → ADR

---

### 2. Requirements (EARS)
**Файл**: [`requirements.md`](./requirements.md)

| Атрибут | Значение |
|---------|----------|
| **Что** | Структурированные требования в EARS нотации |
| **Когда** | После Problem Statement, перед Approach |
| **Кто** | Engineer + PM + AI |
| **Формат** | Markdown с 5 паттернами EARS |
| **Хранение** | `specs/requirements.md` |

**5 паттернов**: Ubiquitous, State-driven, Event-driven, Optional, Unwanted

**Связь**: ← Problem Statement, → Approach, → BDD, → Tests

---

### 3. ADR (Architecture Decision Record)
**Файл**: [`adr.md`](./adr.md)

| Атрибут | Значение |
|---------|----------|
| **Что** | Запись архитектурного решения |
| **Когда** | При принятии значимого решения |
| **Кто** | Engineer / Architect |
| **Формат** | MADR / Nygard / Y-Statements |
| **Хранение** | `docs/adr/adr-NNN.md` |

**Форматы**: Nygard (простой), MADR (структурированный), Y-Statements (легковесный)

**Связь**: ← Problem Statement, ← Requirements, → Implementation

---

## Execution Flow (Phase 2) — Модули реализации

Связывают документацию с кодом. Используются для проектов > 1 дня.

### 4. Approach (Technical Design)
**Файл**: [`approach.md`](./approach.md)

| Атрибут | Значение |
|---------|----------|
| **Что** | Технический план реализации |
| **Когда** | Для фич > 1 недели |
| **Кто** | Engineer / Architect |
| **Формат** | Markdown + PlantUML/Mermaid |
| **Хранение** | `specs/approach.md` |

**Содержит**: Architecture, Data Flow, API Contracts, Design Decisions, Error Handling, Performance, Security, Testing

**Связь**: ← Requirements, ← ADR, → Tasks, → Implementation

---

### 5. Tasks Breakdown
**Файл**: [`tasks.md`](./tasks.md)

| Атрибут | Значение |
|---------|----------|
| **Что** | Список implementable задач |
| **Когда** | После Approach, перед Implementation |
| **Кто** | Engineer / AI |
| **Формат** | Markdown с чекбоксами |
| **Хранение** | `specs/tasks.md` |

**Структура**: Phases → Tasks → Acceptance Criteria → Dependencies → Estimates

**Связь**: ← Approach, ← Requirements, → Implementation

---

### 6. Implementation
**Файл**: [`implementation.md`](./implementation.md)

| Атрибут | Значение |
|---------|----------|
| **Что** | Связь документации с кодом |
| **Когда** | После Tasks |
| **Кто** | Engineer / AI |
| **Формат** | Source code + tests |
| **Хранение** | `src/`, `tests/` |

**Принципы**: Код = производная от документации, верификация, прослеживаемость

**Связь**: ← Tasks, ← Approach, ← Requirements, → Verification

---

## Optional Modules — Добавляются по необходимости

### 7. PRD (Product Requirements Document)
**Файл**: [`prd.md`](./prd.md)

| Атрибут | Значение |
|---------|----------|
| **Что** | Продуктовые требования (what & why) |
| **Когда** | Новая продуктовая линейка, major feature |
| **Кто** | Product Manager |
| **Формат** | Markdown |
| **Хранение** | `docs/prd/` |

**Добавлять когда**:
- Новая продуктовая линейка
- Multiple teams involved
- Budget > $100k
- Duration > 1 month

**Не добавлять когда**:
- Bug fix
- Small enhancement
- Одна команда

**Связь**: → Requirements, → RFC, → ADR

---

### 8. RFC (Request for Comments)
**Файл**: [`rfc.md`](./rfc.md)

| Атрибут | Значение |
|---------|----------|
| **Что** | Техническое предложение с альтернативами |
| **Когда** | Нужен consensus, архитектурные дебаты |
| **Кто** | Engineer |
| **Формат** | Markdown |
| **Хранение** | `docs/rfc/` |

**Добавлять когда**:
- Multiple viable alternatives
- Cross-team impact
- High-risk decision
- Reversible vs irreversible choice

**Не добавлять когда**:
- Решение очевидно
- Нет альтернатив
- Time pressure

**Связь**: ← Problem Statement, → ADR, → Approach

---

### 9. BDD (Behavior-Driven Development)
**Файл**: [`bdd.md`](./bdd.md)

| Атрибут | Значение |
|---------|----------|
| **Что** | Исполняемые спецификации (Given-When-Then) |
| **Когда** | Business rules критичны, нужен compliance |
| **Кто** | Team (Product + Dev + QA) |
| **Формат** | Gherkin (.feature files) |
| **Хранение** | `features/*.feature` |

**Добавлять когда**:
- Business rules критичны (финансы, здоровье, право)
- Нужен compliance (GDPR, HIPAA)
- Complex user workflows
- Stakeholder collaboration важна

**Не добавлять когда**:
- Simple CRUD
- Internal technical features
- Нет business stakeholders

**Связь**: ← Requirements, → Implementation, → Tests

---

### 10. API Specifications
**Файл**: [`api-specs.md`](./api-specs.md)

| Атрибут | Значение |
|---------|----------|
| **Что** | Формальные контракты для APIs |
| **Когда** | API development, интеграции |
| **Кто** | Engineer |
| **Формат** | YAML / JSON / SDL |
| **Хранение** | `specs/api/` |

**Форматы**:
- **OpenAPI 3.x** — REST APIs
- **AsyncAPI** — Event-driven APIs
- **GraphQL SDL** — GraphQL APIs
- **gRPC/Protobuf** — RPC APIs

**Добавлять когда**:
- Разработка нового API
- Интеграция с внешними системами
- Микросервисная архитектура
- Множественные потребители (clients)

**Не добавлять когда**:
- Внутренние функции
- Нет API
- Один потребитель

**Связь**: ← Requirements, → Approach, → Implementation

---

## Как собирать процесс

### Уровень 1: Минимальный (любой проект)

```
Problem Statement → Requirements → Implementation → ADR
```

**Когда**: Любая задача, даже простая

### Уровень 2: Стандартный (фича 1-4 недели)

```
Problem Statement → Requirements → Approach → Tasks → Implementation → ADR
```

**Когда**: Средняя фича, одна команда

### Уровень 3: Расширенный (крупная фича 1-3 месяца)

```
PRD → Problem Statement → RFC → Requirements → Approach → 
API Specs → BDD → Tasks → Implementation → ADRs
```

**Когда**: Major feature, multiple teams

### Уровень 4: Полный (новый продукт 3+ месяца)

```
PRD → Event Storming → Problem Statement → RFC → Requirements →
Approach → API Specs → BDD → Tasks → Implementation → ADRs → 
Formal Methods (если нужно)
```

**Когда**: Новая продуктовая линейка, критическая система

---

## Матрица: Когда какой модуль

| Модуль | Всегда | Малый проект | Средний | Крупный |
|--------|--------|-------------|---------|---------|
| **Problem Statement** | ✅ | ✅ | ✅ | ✅ |
| **Requirements** | ✅ | ✅ | ✅ | ✅ |
| **ADR** | При решении | ✅ | ✅ | ✅ |
| **Approach** | — | — | ✅ | ✅ |
| **Tasks** | — | — | ✅ | ✅ |
| **Implementation** | ✅ | ✅ | ✅ | ✅ |
| **PRD** | — | — | Опционально | ✅ |
| **RFC** | — | — | Опционально | ✅ |
| **BDD** | — | — | Опционально | ✅ |
| **API Specs** | — | — | ✅ (если API) | ✅ |
| **Formal Methods** | — | — | — | Опционально |

---

## Хранение в репозитории

```
project/
├── docs/
│   ├── prd/                      ← PRD (optional)
│   │   └── feature-name.md
│   ├── rfc/                      ← RFC (optional)
│   │   └── rfc-001-title.md
│   ├── adr/                      ← ADR (обязательно)
│   │   ├── README.md
│   │   ├── adr-001.md
│   │   └── adr-002.md
│   └── architecture/             ← Arc42 (optional, крупные проекты)
│       ├── 01-introduction.md
│       └── ...
├── specs/                        ← Feature specifications
│   ├── feature-name/
│   │   ├── problem-statement.md  ← Phase 1
│   │   ├── requirements.md       ← Phase 1 (EARS)
│   │   ├── approach.md           ← Phase 2
│   │   ├── tasks.md              ← Phase 2
│   │   └── adr/                  ← Feature-specific ADRs
│   └── ...
├── features/                     ← BDD scenarios (optional)
│   └── feature.feature
├── src/                          ← Implementation
├── tests/                        ← Tests
│   ├── unit/
│   ├── integration/
│   └── e2e/
└── README.md
```

---

## AI-Agent Integration Overview

| Модуль | Что может делать AI | Что остаётся человеку |
|--------|--------------------|-----------------------|
| **Problem Statement** | Формулировка, 5 Whys | Финальный выбор проблемы |
| **Requirements** | Генерация, проверка полноты | Приоритизация, валидация |
| **ADR** | Генерация черновика | Принятие решения |
| **Approach** | Генерация, ревью | Выбор архитектуры |
| **Tasks** | Генерация, разбиение | Оценка, планирование |
| **Implementation** | Генерация кода, тесты | Финальный ревью |
| **PRD** | Генерация черновика | Продуктовые решения |
| **RFC** | Альтернативы, анализ | Принятие решения |
| **BDD** | Генерация сценариев | Валидация с бизнесом |
| **API Specs** | Генерация из requirements | Финальная валидация |

---

## Progression Guide

### Level 1: Новичок
**Используете**: Problem Statement, Requirements, ADR (при решениях)

**Характерно**:
- Commit message вместо отдельного Problem Statement
- Requirements в EARS (хотя бы базовые)
- ADR только для major decisions

**Когда переходить**: Когда теряете контекст или повторяете решения

### Level 2: Практик
**Используете**: Все 6 модулей (2 фазы)

**Характерно**:
- Полная документация для каждой фичи
- Approach с диаграммами
- Tasks с acceptance criteria

**Когда переходить**: Когда команда растёт или проект усложняется

### Level 3: Эксперт
**Используете**: Все модули + опциональные по необходимости

**Характерно**:
- PRD для продуктовых решений
- RFC для архитектурных дебатов
- BDD для критических правил
- API Specs для интеграций

**Когда переходить**: Когда процессы становятся bottleneck

### Level 4: Enterprise
**Используете**: Всё + формальные методы + Arc42 + TOGAF

**Характерно**:
- Полная документация
- Compliance и аудиторские требования
- Cross-team governance

---

## Инструменты и автоматизация

### Обязательные (все уровни)

| Назначение | Инструмент | Формат |
|-----------|------------|--------|
| Редактирование | Любой text editor | Markdown |
| Версионирование | Git | — |
| Диаграммы | Mermaid (GitHub native) | Mermaid |
| Валидация | Custom scripts / AI | — |

### Рекомендуемые (уровень 2+)

| Назначение | Инструмент | Формат |
|-----------|------------|--------|
| Диаграммы | PlantUML | PlantUML |
| ADR management | [adr-tools](https://github.com/npryce/adr-tools) | Markdown |
| ADR publishing | [Log4brains](https://github.com/thomvaill/log4brains) | HTML |
| API Specs | [Stoplight](https://stoplight.io) | OpenAPI/AsyncAPI |
| BDD | [Cucumber](https://cucumber.io) / [Behave](https://behave.readthedocs.io) | Gherkin |
| Documentation | [MkDocs](https://www.mkdocs.org) / [Docusaurus](https://docusaurus.io) | Markdown |

### Опциональные (уровень 3+)

| Назначение | Инструмент | Формат |
|-----------|------------|--------|
| C4 Model | [Structurizr](https://structurizr.com) | DSL |
| Arc42 | [arc42 templates](https://github.com/arc42) | Markdown/AsciiDoc |
| Event Storming | [Miro](https://miro.com) / [EventModeling](https://eventmodeling.org) | Visual |
| Formal Methods | [TLA+](https://lamport.azurewebsites.net/tla/tla.html) / [FizzBee](https://fizzbee.io) | TLA+/Python |
| SDD Tools | [GitHub Spec Kit](https://github.com/github/spec-kit) / [OpenSpec](https://openspec.dev) | Markdown |

---

## Анти-паттерны (общие)

### ❌ Over-documentation
**Проблема**: Все модули для каждой мелочи
**Решение**: Используйте только нужные модули. Bug fix не требует PRD.

### ❌ Under-documentation
**Проблема**: Ничего не документировано
**Решение**: Как минимум Problem Statement + Requirements + ADR.

### ❌ Documentation Without Code
**Проблема**: Документы пишутся, но не реализуются
**Решение**: Каждый документ должен приводить к коду.

### ❌ Code Without Documentation
**Проблема**: Код пишется без спецификаций
**Решение**: Документация в одном PR с кодом.

### ❌ One-size-fits-all
**Проблема**: Одинаковый процесс для всего
**Решение**: Модульный подход — собирайте под контекст.

---

## Ссылки на документы

### Внутренние документы
- [Goals](../goals.md) — цели процессов
- [Knowledge Base](../knowledge-base.md) — все инструменты и подходы
- [Process Variants](../process-variants.md) — готовые pipelines
- [Modular Process](../modular-process.md) — модульный подход

### Модули
- [Problem Statement](./problem-statement.md) — Phase 1
- [Requirements (EARS)](./requirements.md) — Phase 1
- [ADR](./adr.md) — Phase 1
- [Approach](./approach.md) — Phase 2
- [Tasks](./tasks.md) — Phase 2
- [Implementation](./implementation.md) — Phase 2
- [PRD](./prd.md) — Optional
- [RFC](./rfc.md) — Optional
- [BDD](./bdd.md) — Optional
- [API Specs](./api-specs.md) — Optional
