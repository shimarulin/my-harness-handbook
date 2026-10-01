# Артефакты процесса: шаблоны и правила (10 модулей)

| Параметр | Значение |
|---|---|
| Статус | draft |
| Обновлено | 2026-09-30 |

## Что это

Справочник по типам артефактов модульного пайплайна (`artifact-pipeline.md`): назначение, вход/выход, шаблон (скелет секций), анти-паттерны. Детали нотаций — в отдельных статьях: `adr.md`, `ears.md`, `prd.md`, `rfc-vs-sdd.md`, `../landscape/bdd-tools.md`.

## Problem Statement (core, всегда первый)

**Назначение**: формулировка проблемы на языке пользователя/бизнеса, без решения; north star для всех последующих решений. Отвечает: что не работает? почему это проблема? кто страдает? какова стоимость? что если не решить?

**Шаблон (базовый)**: `## Problem Statement → ### The Problem (текущее состояние) / ### The Impact (кто страдает, стоимость) / ### The Goal (желаемое состояние, НЕ как)`. Расширенный: + Context, Current State, Pain Points (с evidence), Impact (количественно), Success Criteria.

**Техники**: 5 Whys (до root cause, против XY problem); Problem-User-Impact Matrix (сегмент × боль × impact); Before/After Bridge; JTBD (`When [situation], I want to [motivation], so I can [outcome]`).

**Анти-паттерны**: solution in disguise («мигрировать на PostgreSQL» вместо проблемы); too vague («system is slow» — нужны числа); too broad; no impact; jumping to solution.

**Формы по размеру**: bug fix → commit message (`fix: … Problem: … Impact: … Goal: …`); small feature → начало spec-файла; major → секция PRD; решение → Context секция ADR.

## Requirements (core, EARS)

**Назначение**: контракт поведения системы — что система должна делать; source of truth для верификации; вход для AI-генерации кода. НЕ описание проблемы, НЕ дизайн, НЕ задачи, НЕ тесты.

**Ключевое**: 5 паттернов EARS + complex (≤1 While + ≤1 When); ID `REQ-<FEATURE>-<NNN>` (стабильные, не переиспользуются); паттерн-теги `[Ubiquitous]/[Event]/[State]/[Optional]/[Unwanted]/[Performance]/[Security]`; статусы Draft|In Review|Approved.

**Шаблон (lightweight)**: `# Feature: <Name>` → Problem Statement → Requirements (Functional по паттернам; Non-Functional) → Out of Scope → Open Questions. Full: + Metadata, Stakeholder Requirements (User/Business таблицы с Priority Must/Should/Could), Traceability Matrix (Req ID | Problem | Pattern | Design | Test | Code | Status), Acceptance Criteria Summary, Change Log.

**Правила качества**: однозначность, тестируемость (нетестируемое = плохое требование: запрещены «fast/easy/good/удобно» — только конкретные значения типа «200ms p95»), атомарность (нет «и» между разными вещами), ссылка на Problem Statement (необходимость), обязательны Unwanted Behaviour («всегда думайте: что может пойти не так?») и NFR (категории ISO/IEC 25010). Линтинг автоматизируем (`lint_ears.py`: паттерны, REQ-IDs, vague terms blacklist).

## Approach (core, при фичах > 1 дня / > 1 context window)

**Назначение**: технический план — как реализуем; принятое решение (debate — в RFC); source of truth для верификации реализации.

**Шаблон (lightweight)**: Overview → Architecture (Components, Data Flow mermaid) → Key Design Decisions (Choice/Why/Alternatives/Trade-offs) → Error Handling → Performance → Security → Testing Strategy → Out of Scope.

**Full (14 секций)**: Metadata → Overview → Architecture (C4 Context/Container/Component + Data Model SQL DDL) → API Contracts (REST + AsyncAPI) → Key Design Decisions (с Reference: ADR-NNN) → Data Flow (happy + error path sequence diagrams) → Error Handling (по подсистемам: стратегия retry/backoff/fail/alert) → Performance (объёмы, конкурентность, кэширование TTL) → Security (authn/authz/at rest/in transit/audit) → Testing Strategy (unit 80%, integration critical paths, E2E happy + top-3 errors, performance, security) → Deployment (staging → canary 5% → full; feature flags; rollback) → Monitoring (metrics p50/p95/p99, alerts с порогами, structured logging + correlation IDs) → Out of Scope → Open Questions → References.

**Принципы**: конкретность (технологии с ролями, не buzzwords); полнота (happy + error paths); traceability (REQ → секции; ADR → decisions; секции → Tasks); диаграммы как код; честные trade-offs. **Анти-паттерны**: без Requirements; too abstract; missing error handling; no trade-offs; approach as RFC.

## Tasks Breakdown (core, при проектах > 1 дня)

**Назначение**: мост Approach → Implementation; исполняемые единицы с проверяемым Definition of Done.

**Шаблон**: Overview → Estimation Summary (Phase|Tasks|Effort|Risk) → фазы (Setup & Infrastructure → Core Implementation → Testing → Deployment) → Dependency Graph (mermaid) → Parallelization → Risk Register (Task|Risk|Likelihood|Impact|Mitigation) → Open Questions.

**Задача (поля)**: Description, Acceptance Criteria (чекбоксы), Requirements covered (REQ-XXX), Approach reference (§N.N), Dependencies, Estimate, Risk, Assignee (@user / AI-agent), Status (⬜).

**Размеры**: XS <30 мин; S 2–4 ч; M 1–2 дня; L 3–5 дней; **XL обязательно разбить** (ни одна задача > 5 дней; норма ≤ 2 дней). Testing — отдельная фаза, не «после implementation».

**Анти-паттерны**: tasks too large; missing acceptance criteria; flat list без зависимостей; не покрывают requirements; no testing tasks.

## ADR (core, при каждом архитектурном решении)

7 категорий-триггеров: technology stack; архитектурные паттерны; data model; integration choices; deployment; security; performance trade-offs. Checklist «архитектурное ли это решение?»: влияет на multiple components? multiple viable options? сложно изменить? significant trade-offs? нужен consensus?

**Выбор формата** (decision matrix): много мелких → Y-Statements (`docs/decisions.md`); одно малое → Nygard; medium detailed → MADR full; quick → MADR minimal; automation → YADR. Рекомендация: начинать с MADR minimal, upgrade до full.

**Workflow**: checklist → формат → написание (Context → Options → Decision → Consequences → review коллегой → commit `docs(adr): add ADR-NNN …`) → supersession (новый `Supersedes ADR-003`; старый `Superseded by ADR-007` + причины). Index: `docs/adr/README.md` (Active/Superseded таблицы).

Шаблоны и детали: `adr.md`. Анти-паттерны: ADR для trivial; missing alternatives; only positive consequences; vague justification («popular and modern» — нужны причины, привязанные к контексту); not updating superseded; ADR without implementation (documentation debt).

## PRD (optional)

Статусы Draft|In Review|Approved; метаданные Author/Status/Last updated/Stakeholders/Related ADRs. Полный скелет: Overview → Problem (с evidence) → Goals (измеримые) → Non-goals → Requirements/User Stories (As a… + Prioritization Must/Should/Could + Effort S/M/L) → Success Metrics (метрика + target + owner) → User Experience → Constraints & Assumptions → Open Questions (владелец + дедлайн) → Out of Scope → Timeline & Milestones → References.

Анти-паттерны: PRD как технический дизайн (никаких «PostgreSQL и Celery»); нет метрик; нет non-goals; бесконечный черновик (time-box ревью 1–2 недели). Детали: `prd.md`.

## RFC (optional)

Статусный цикл: Draft → In Review → Changes Requested → Approved; Rejected / Blocked / Discarded. 6 принципов процесса (Attentive): консенсус, не бюрократия; рано, но не преждевременно; никаких вечных черновиков; time-box ревью (дефолт 1 неделя); автор владеет результатом; Staff+ менторят.

Скелет: Summary → Context and Problem → Motivation (почему сейчас; что если не сделать) → Proposal (Design, Architecture, API Changes, Migration Plan) → Alternatives Considered (каждая: Description/Pros/Cons/**Why rejected**; обязательна «Do Nothing») → Trade-offs and Risks (Risk|Likelihood|Impact|Mitigation) → Open Questions → Timeline → References. Обязательное поле Review deadline.

Переход: одобренный RFC → один или несколько ADR (RFC-004 → ADR-015 + ADR-016). Детали: `rfc-vs-sdd.md`.

## API Specs (optional)

Выбор формата: OpenAPI 3.x (REST), AsyncAPI (event-driven), GraphQL SDL, gRPC/Protobuf. Workflow: Requirements → Approach → Spec → {codegen (OpenAPI Generator, 40+ языков), mock server, docs, contract tests (Specmatic)}. Валидация: Spectral (400+ rules). Правила: спецификация ДО кода; версионирование breaking changes; ошибки + примеры для каждого endpoint; REQ-ID вшиваются в description схем (traceability до полей).

## BDD (optional)

Три практики: Discovery (example mapping, real-world примеры) → Formulation (Gherkin `.feature`) → Automation (step definitions, living documentation). Правило связи: каждое EARS-требование покрывается ≥ 1 BDD-сценарием; сценарии аннотируются `# REQ-XXX`.

Скелет: `Feature:` + `Background:` (общие предусловия) + `Rule: <бизнес-правило>` + `Scenario:` (Given/When/Then/And/But); теги @fast/@slow/@critical; Scenario Outline + Examples вместо раздувания сценариев. Анти-паттерны Cucumber: feature-coupled step definitions (шаги по доменным концепциям); conjunction steps (атомарность); BDD без collaboration («guaranteed to kill your test automation success»). Инструменты: `../landscape/bdd-tools.md`.

## Implementation (core, финальный)

Принцип: **код — производная от документации**. Этапы: Coding → Testing → Review (только человек) → Documentation update — **всё в одном PR**.

AI-паттерны execution: Task-by-Task (средние/крупные: читать task+AC+Approach sections → код+тесты → прогон → review); Requirement-by-Requirement (small); Approach-Driven (complex: весь Approach → component-by-component → verify against Requirements).

Верификация, 3 уровня: manual review (checklist: все REQ? архитектура = Approach? REQ-IDs в коде?) → automated (`verify_requirements.py`: REQ-IDs из requirements.md ищутся в src/ и tests/; CI workflow) → BDD (`behave --tags=@REQ-XXX`).

Кодовая конвенция: docstring/комментарии с REQ-ID («Requirements covered: REQ-EXP-005…») + assert на требование. PR Template: Description → Requirements Addressed → Documentation Updated (чекбоксы) → Tests → Verification.

## Источники

- Входные материалы inbox: `documentation-process-v2/modules/` (problem-statement.md, prd.md, rfc.md, approach.md, requirements.md, adr.md, tasks.md, implementation.md, api-specs.md, bdd.md), `documentation-process-v2/modular-process.md`
- Связанные KB: `artifact-pipeline.md`, `process-examples.md`
