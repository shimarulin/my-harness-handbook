# Сквозные примеры процесса: L1, L2, L3 и полный модульный проход

| Параметр | Значение |
|---|---|
| Статус | draft |
| Обновлено | 2026-09-30 |

## Что это

Нормативные заполненные эталоны процесса на одном сквозном домене (экспорт данных / уведомления): что создаётся на каждом уровне, что сознательно пропускается и почему, сколько времени занимает документация. Применения: изучение процесса, копирование как шаблоны, валидация своих артефактов, few-shot examples для AI-агентов.

## Сравнение уровней на примерах

| Аспект | L1: task-042 (timeout message) | L2: spec-012 (CSV export) | L3: rfc-0031 (Kafka notifications) | v2: export-service (все модули) |
|---|---|---|---|---|
| Документация | ~15 мин | ~3 ч | ~1–2 дня | ~2–4 недели фичи |
| Артефакты | 1 (task.md) | 3 (prd, spec, tasks) | 5 (rfc, adr, spec, tasks, PR) | 10 (все core + PRD, RFC, BDD, API, ADR×2) |
| AI-сессии | 1 | 2–3 | Много | Много |
| Цепочка traces | bug report → task-042 → PR | idea-023 → prd-005 → spec-012 → tasks → PR | prd-012 → rfc-0031 → adr-0007 → spec-015 → tasks → PR | PS → PRD → REQ(31) → RFC-001 → Approach → API/BDD → Tasks(14) → ADR-001/002 → код |

## Пример L1: task-042 «Fix unclear timeout error message on login»

**Поток**: Observe bug (5 мин) → task с Job Story (10 мин) → AI implements (15 мин) → PR (5 мин) → review+merge (10 мин).

**Создано**: `task-042.md` — frontmatter {id, type: task, status, traces: [], level: L1, tags} + Job Story + Критерии готовности (чекбоксы) + Контекст + Implementation Notes для AI (constraints: не менять архитектуру, не добавлять dependencies, i18n keys; файлы для чтения: errorHandler.ts, sessionManager.ts, errors.ts) + `PR_DESCRIPTION.md` (скриншоты Before/After, How to Test).

**Пропущено и почему**: ADR — «не архитектурное решение»; PRD/Spec — задача из bug report, не из idea; документация — «не требуется (bug fix)».

**Чему учит**: task-файл как самодостаточный контекст для AI-агента; Job Story как формат постановки; минимальный overhead по Scale-тесту (≤ 15 мин).

## Пример L2: spec-012 «Data Export to CSV»

**Поток**: Idea (5 мин) → PRD (45 мин) → Spec EARS (60 мин) → Tasks (30 мин) → AI 2–3 сессии (90 мин) → PR (15 мин) → review (30 мин).

**Создано**: `prd-005` (traces: idea-023; PM + AI draft → ревью PM + Eng lead) → `spec-012/spec.md` (EARS R1–R8 + acceptance-сценарии GIVEN/WHEN/THEN; Engineer + AI → ревью team; статус «Approved for implementation» — gate) → `spec-012/tasks.md` (5 фаз по AI-сессиям, каждая с Verification Checklist против EARS) → PR.

**Пропущено и почему**: RFC/ADR — нет архитектурных альтернатив (используется existing email/auth/S3); JSON/scheduled exports/import — Non-goals. Один open question (file naming) сознательно отложен «TBD in spec phase» — демонстрация передачи вопросов между артефактами.

**Чему учит**: разделение «кто пишет / кто ревьюит» по артефактам; approval gate перед implementation; tasks разбиты по AI-сессиям с проверкой против требований.

## Пример L3: rfc-0031 «Event-driven notifications (Kafka)»

**Поток**: Problem (30 мин) → RFC с альтернативами (4 ч) → Debate (2 ч) → ADR (1 ч) → Spec (2 ч) → Design (1 ч) → Tasks (1 ч) → Implementation (дни).

**Создано**: `rfc-0031` (traces: prd-012; reviewers: arch/backend/sre leads; sync p95 200ms→3s, 3 инцидента/квартал → event-driven; 4 альтернативы с «Why not chosen»; 4 фазы внедрения) → `adr-0007` (MADR, deciders 4 включая CTO; replay capability как hard requirement от compliance — отсекает RabbitMQ/SQS; adr-0003 → superseded; статус RFC: «Approved — Decision recorded in adr-0007») → `spec-015/spec.md` (EARS R1–R10) → `tasks.md` (5 фаз по неделям, Avro-схема) → PR (deployment plan + rollback через feature flag).

**Ключевые механики**: dual-write фаза; gradual rollout 10%→50%→100%; rollback criteria («error rate > 5%»); sync-код хранится 1 неделю после cutover; DLQ replay + admin interface + runbooks — часть Definition of Done.

**Чему учит**: RFC-процесс с reviewers и debate-фазой; ADR как результат RFC; supersede-связь; compliance-требование (replay) как отсекающий критерий альтернатив.

## Пример v2 (все модули): export-service

**Контекст**: средняя фича 2–4 недели, одна команда; GDPR Article 20, 3 enterprise-сделки заблокированы ($2M ARR), 23% surveys.

**Проход всех 10 модулей**: Problem Statement (5 Whys до root cause «Product strategy gap»; impact по осям Users/Business/Engineering; Why Now с дедлайнами) → PRD (US-1..US-6, MoSCoW, success metrics с owners) → Requirements (31 REQ-EXP-001..031 по всем 5 паттернам EARS + NFR) → RFC-001 (4 альтернативы с «Why rejected», включая обязательную «Do Nothing») → Approach (C4 PlantUML, sequence mermaid, SQL data model, API contracts, design decisions со ссылками на ADR) → OpenAPI 3.0.3 (REQ-ID вшиты в description схем) → Gherkin (8 Rules, каждая с `# REQ-EXP-xxx`) → Tasks (14 задач в 4 фазах, 11.5 дней, dependency graph) → ADR-001 (Celery+Redis, MADR) + ADR-002 (S3, lifecycle 7 дней, AES-256) → код FastAPI (`exports.py`, docstring «Requirements covered: REQ-EXP-005…»).

**Чему учит**: (1) каждый артефакт начинается со ссылок на входы; (2) трейсинг требований до кода: REQ-EXP-xxx фигурирует в requirements → tasks → openapi descriptions → gherkin → docstring кода; (3) RFC отвергает альтернативы с обоснованиями; (4) ADR фиксируют решения «по ходу» и линкуются из Approach.

**Замеченные пропуски в самом примере**: из src/ присутствует только `api/exports.py` (services/models/tests заявлены, но отсутствуют); adr/README.md (index) заявлен, но не создан. Полные исходники: `research/inbox/documentation-process-v2/examples/export-service/` (статус: не архивирован, доступен как эталон для копирования).

## Расхождения v2 ↔ v3 на одном домене (нормативно, не ошибка)

| Параметр | v2 export-service | v3 spec-012 (L2) |
|---|---|---|
| Expiry download link | 7 дней | 24 часа |
| Rate limit | 10/час | 3/24 ч |
| Форматы | CSV + JSON | Только CSV (JSON — non-goal) |

Разные нормативные примеры, а не эволюция одного артефакта: иллюстрация, что конкретные значения — предмет spec, а не процесса.

## Источники

- Входные материалы inbox: `documentation-process-v3/08-examples/` (README + 01-task-l1 + 02-feature-l2 + 03-major-l3), `documentation-process-v2/examples/export-service/` (README + specs/ + docs/ + features/ + src/)
- Связанные KB: `process-levels.md`, `artifact-pipeline.md`, `artifact-templates.md`
