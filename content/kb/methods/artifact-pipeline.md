# Пайплайн артефактов: модульная модель (синтез v2+v3)

| Параметр | Значение |
|---|---|
| Статус | draft |
| Обновлено | 2026-09-30 |

## Что это

Модель сквозного потока артефактов разработки: «не выбирайте pipeline — **соберите его** из нужных модулей». Есть обязательное ядро (core blocks, присутствует в любом процессе) и опциональные модули, подключаемые по явным критериям контекста. Каждый артефакт — файл открытого формата с уникальным ID, статусом, ссылкой на предшественника и approval-гейтом, где решение принимает человек.

Синтез: модульная модель v2 (6 core + 9 optional блоков, 5 правил композиции) + пайплайн v3 (IDEA→PRD→RFC→SPEC→ADR→CODE→RELEASE, трассировка через YAML front-matter). Выбор уровня набора артефактов — `process-levels.md`.

## Сквозная цепочка

```
Idea → Problem Statement → [PRD] → [discovery: Event Storming / Story Mapping] → [RFC]
     → Requirements (EARS) → Approach/Design → [API Specs] → [BDD] → Tasks
     → Implementation → ADR (по мере решений) → Tests → Release Notes
```

[…] — опциональные модули. Канонический порядок обязателен (Rule 4): нельзя Design до Requirements, нельзя Implementation до spec — иначе rework.

## Core blocks (обязательны всегда, Rule 1)

| # | Блок | Назначение | Вход → выход | Кто (человек / AI) | Хранение |
|---|---|---|---|---|---|
| 1 | **Problem Statement** | Проблема на языке бизнеса, 1–3 абзаца, без решения (Problem/Impact/Goal) | Боль/симптом → Goal + Success Criteria | Любой; AI — формулировка, 5 Whys | Начало spec/RFC/PRD; для bug fix — commit message |
| 2 | **Requirements** | Контракт поведения системы; EARS (5 паттернов), альтернативы User/Job Stories | Problem Statement → REQ-IDs | PM/Engineer; AI — генерация, проверка полноты | `specs/<feature>/requirements.md` |
| 3 | **Approach** | Технический план: как реализуем (компоненты, data flow, контракты, error handling); принятое решение, не debate | Requirements + ADR → секции дизайна | Engineer/Architect; AI — черновик | `specs/<feature>/approach.md` (или design.md) |
| 4 | **Tasks Breakdown** | Исполняемые единицы по фазам (Setup→Core→Testing→Deployment), каждая ≤ 2 дней, с acceptance criteria | Approach → план с зависимостями | Engineer; AI — разбиение | `specs/<feature>/tasks.md` |
| 5 | **Implementation** | Код + тесты; **код — производная от документации** | Tasks → PR | Engineer; AI — генерация по spec/tasks | `src/`, `tests/` |
| 6 | **ADR** | Одно решение — одна запись (Rule 2: при **каждом** архитектурном решении, независимо от pipeline) | Контекст решения → immutable запись | Engineer/Architect принимает; AI — MADR-черновик | `docs/adr/adr-NNNN-*.md` |

Триггер Approach/Tasks (v2 modules): задача больше одного context window AI-агента или одного рабочего дня.

## Optional modules (подключаются по критериям, Rule 3 / Rule 5 «skip what you don't need»)

| Модуль | Добавлять когда | НЕ добавлять | Хранение |
|---|---|---|---|
| **PRD** | Новая продуктовая линейка; multiple teams; budget > $100k; duration > 1 мес; нужен product alignment | Bug fix, small enhancement, одна команда | `docs/prd/` |
| **RFC** | Multiple viable alternatives; cross-team impact; high-risk; reversible vs irreversible choice | Решение очевидно, нет альтернатив, time pressure | `docs/rfc/` |
| **BDD Scenarios** | Business rules critical (финансы, здоровье, право); compliance (GDPR, HIPAA, SOX); complex workflows; stakeholder collaboration | Simple CRUD, internal tech features, нет business stakeholders | `features/*.feature` |
| **Event Storming** | Complex domain, greenfield, команда не понимает домен | Простой домен, time pressure | `docs/discovery/event-storming/` |
| **User Story Mapping** | Holistic view продукта, сложная приоритизация, release planning | Одна фича, ясные приоритеты | `docs/discovery/story-map/` |
| **Design-First** | Технические ограничения определяют решение; performance-critical; legacy modernization | Product-driven фича, UX первичен | `docs/design/` |
| **Formal Methods** | Correctness critical (auth, payments, consensus); distributed systems | Simple CRUD, нет экспертизы | `specs/formal/` (TLA+/FizzBee/Alloy) |
| **API Specs** | REST/event-driven/GraphQL API; external integration; multiple consumers | Внутренние функции, один потребитель | `specs/api/` (OpenAPI/AsyncAPI) |
| **Research Compendium** | Data science, ML, нужна воспроизводимость | Production code | `compendium/` |

## Трассировка (единый механизм v3)

YAML front-matter каждого артефакта:

```yaml
---
id: spec-012
type: spec                    # idea|task|prd|rfc|adr|spec|change
status: approved              # draft|review|approved|rejected|superseded|archived
traces: prd-017               # предшественник(и)
adr: [adr-0007]               # решения по этой спеке
created: 2026-09-28
owner: @human
level: L2                     # уровень инициативы
tags: [...]
---
```

ID-схема: `idea-NNN`, `task-NNN`, `prd-NNN`, `spec-NNN` (3 знака); `rfc-NNNN`, `adr-NNNN` (4 знака); requirements внутри спек: `REQ-<FEATURE>-<NNN>` (стабильные, не переиспользуются). CI проверяет: все `traces` существуют; статусы валидны; `superseded` ADR имеет `superseded_by`. Инвариант G1: ни один значимый артефакт не существует только «в голове» или в чате.

Цепочка продвижения (promotion): Idea→Task→PRD→RFC→ADR; статусы `candidate → promoted`. ADR-0001 зарезервирован: `0001-record-architecture-decisions.md`.

## Approval-гейты и роли

| Этап | Человек | AI-агент |
|---|---|---|
| Idea/PRD | Формулирует, ревьюит, утверждает | Черновик из диалога; сбор open questions |
| RFC | Дебатирует, утверждает | Alternatives, trade-offs, risk-секции |
| Spec | Утверждает (gate: «Approved for implementation») | Черновик EARS из PRD/RFC |
| ADR | Принимает решение | MADR-черновик по итогу обсуждения |
| Tasks | Приоритизирует | Разбиение spec → tasks |
| Code | Ревьюит PR | Имплементация строго по spec+tasks; сверка code↔spec перед PR |

Жёсткие правила агентов (v3, закрепляются в AGENTS.md): (1) не имплементировать без approved-спеки (кроме L0); (2) перед имплементацией прочитать CONSTITUTION.md → PRD/RFC → spec → tasks → ADR; (3) любое отклонение от спеки — стоп и вопрос человеку; (4) принципиальные решения не принимать — оформлять draft ADR; (5) по завершении задачи обновить tasks.md и (при поведенческом изменении) scenarios.

## Анти-паттерны

- **Over-composition** — все модули «на всякий случай» → process paralysis, documentation debt.
- **Under-composition** — пропуск важного (RFC для архитектурного решения) → poor decisions, rework.
- **Wrong order** — design до requirements, implementation до spec.
- **Module without purpose** — BDD для simple CRUD.
- **Documentation without code** / **code without documentation** — документы и код меняются вместе, в одном PR.

## Пример прохода (композиции по размеру)

| Сценарий | Состав |
|---|---|
| Bug fix | Problem (commit message) → Implementation → Commit |
| Small feature (API endpoint) | Problem → Requirements (EARS) → Approach → Tasks → Implementation → ADR (если выбрана библиотека) |
| Major feature | PRD → Event Storming → RFC → Requirements → Design (C4) → API Specs → BDD → Tasks → Implementation → ADRs |
| Data science | Problem → Research Compendium → Implementation → Paper |
| Critical system | Problem → Formal Spec → Requirements (derived) → Design → Tasks → Implementation → ADR |

Полный нормативный пример: `process-examples.md`.

## Источники

- Входные материалы inbox: `documentation-process-v2/modular-process.md` (15 блоков, 5 правил, decision tree), `documentation-process-v2/modules/README.md` (интерфейсы модулей, 4 уровня сборки), `documentation-process-v3/02-process-design.md` (пайплайн, трассировка, роли, правила агентов), `documentation-process-v3/00-goals.md` (инварианты G1–G2)
- Связанные KB: `process-levels.md`, `artifact-templates.md`, `adr.md`, `ears.md`, `prd.md`, `rfc-vs-sdd.md`
