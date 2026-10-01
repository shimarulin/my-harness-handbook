# AI-агенты в процессе: роли, HITL-паттерны, промпт-паттерны

| Параметр | Значение |
|---|---|
| Статус | draft |
| Обновлено | 2026-09-30 |

## Что это

Модель интеграции AI-агентов в модульный пайплайн (`artifact-pipeline.md`): что агент делает на каждом из 10 модулей, что остаётся человеку, паттерны Human-in-the-Loop, уровни верификации, промпт-паттерны. Центральная идея: **AI — collaborator, не authority**; агент генерирует черновики и ускоряет повторяющееся, человек принимает все критические решения через HITL-gates.

## 5 принципов работы с агентами

1. **AI как collaborator, не authority** — агент черновики, человек решения.
2. **Context is King** — полный контекст (проблема → требования → дизайн), формат вывода, ссылки на предыдущие артефакты.
3. **Verification is Mandatory** — «trust but verify»; автоматические проверки дополняют, не заменяют ревью.
4. **Iteration over Perfection** — первый вывод = черновик; уточнение через дополнительные промпты.
5. **Human-in-the-Loop Gates** — критические решения ВСЕГДА за человеком: архитектурные (→ ADR), продуктовые приоритеты (→ PRD), выбор альтернатив (→ RFC), финальный ревью кода.

## Матрица интеграции по модулям (агент / человек / gate)

| Модуль | Агент | Человек | Quality Gate |
|---|---|---|---|
| Problem Statement | Формулировка, 5 Whys | Финальный выбор проблемы | Human review (ясность, конкретность) |
| Requirements (EARS) | Генерация, проверка полноты, конвертация | Приоритизация, валидация | AI + Human (полнота, тестируемость) |
| ADR | MADR-черновик, альтернативы | Принятие решения | Human approval |
| Approach | Генерация, диаграммы, ревью | Выбор архитектуры | Peer review |
| Tasks | Разбиение, оценка, зависимости | Планирование, назначение | Team planning |
| Implementation | Код, тесты | Финальный ревью, merge | Code review + tests |
| PRD | Черновик, метрики | Продуктовые решения | Stakeholder approval |
| RFC | Альтернативы, анализ, резюме | Принятие решения | Team consensus |
| BDD | Сценарии, step definitions | Валидация с бизнесом | Business validation |
| API Specs | Генерация из требований | Финальная валидация | Automated + Human |

## 4 уровня верификации

1. **Automated** (CI/CD): формат, синтаксис, линтеры — при каждом коммите.
2. **AI Review**: логика, полнота, соответствие — после генерации.
3. **Peer Review**: корректность, целесообразность — перед merge.
4. **Human Decision**: архитектурные/продуктовые решения — в критических точках.

## 4 HITL-паттерна

1. **AI Drafts, Human Decides** (ADR, RFC, PRD): агент черновик → человек ревьюит → человек решает → уточнение → финал.
2. **AI Generates, Human Validates** (Requirements, Tasks, API Specs): агент → автоматические проверки → человек валидирует → принятие/отклонение.
3. **AI Assists, Human Executes** (Implementation, Testing): человек описывает задачу → агент подсказывает → человек реализует и коммитит.
4. **Human Defines, AI Implements** (Implementation после approval): человек спецификация → агент код → автотесты → человек ревьюит → merge.

## Промпт-паттерны (скелеты по модулям)

- **Problem Statement**: 5 Whys facilitation (агент задаёт «why» 5 раз, ждёт ответа, в конце root cause + 2–3 решения); Generation (The Problem / The Impact quantified / The Goal / Non-goals / Success criteria); Review по 5 критериям (Clarity, Specificity, Completeness, Solution-free, Testability).
- **Requirements**: генерация из Problem Statement (все 5 EARS-паттернов с тегами, `REQ-<PREFIX>-<NNN>`, конкретные значения, NFR + выявление missing/edge cases/open questions); проверка полноты (6 проверок + **Completeness score 0–100%**); конвертация в BDD (REQ → Feature/Rule/Scenario + test data + tags); конвертация из User Stories.
- **ADR**: генерация из обсуждения (MADR; все опции включая rejected с причинами; honest trade-offs — «not 'because it's better'»); ревью по 6 критериям + **Approval recommendation**; supersession (старый «superseded by ADR-XXX» + новый с reference и migration considerations).
- **Approach**: генерация (11 секций от Overview до Out of Scope; Mermaid-диаграммы; ссылки на REQ-IDs); ревью по 7 критериям с severity (critical/major/minor).
- **Tasks**: генерация (4 фазы; поля задачи включая **Estimate S=2–4h / M=1–2d / L=3–5d** и **Suitable for AI-agent? (yes/no)**; dependency graph; critical path; **ни одна задача > 2 дней**).
- **Implementation**: Task-by-Task промпт (Task ID + AC + REQ-IDs + Approach reference + dependencies + stack → код + тесты; REQ-IDs в комментариях; тесты до или вместе с кодом); генерация тестов (Given-When-Then комментарии в каждом тесте).
- **PRD/RFC/BDD/API Specs**: генерация по шаблонам (`artifact-templates.md`); RFC — ≥ 3 альтернативы включая «do nothing»; BDD — один сценарий на поведение, переиспользуемые атомарные шаги; OpenAPI — REQ-IDs в descriptions, все error codes, примеры.

## Анти-паттерны

| ❌ | Решение |
|---|---|
| AI как «чёрный ящик» (вывод без проверки) | Всегда верифицируем, особенно критические решения |
| Слишком широкий промпт («сделай всё») | Конкретные промпты с контекстом и форматом вывода |
| Нет итерации (первый вывод как финал) | Итерируем, уточняем |
| Пропуск human gates (агент принимает архитектурные решения) | Критические решения всегда за человеком |
| Нет контекста (генерация без предыдущих артефактов) | Всегда передаём Problem → Requirements → Approach |

## Эталонный 10-шаговый workflow (фича)

1. Problem Statement: человек 1–2 предложения → агент 5 Whys + генерация → ревью. 2. Requirements: агент EARS + полнота → человек проверяет. 3. RFC (опц.): агент с альтернативами → команда обсуждает → человек решает. 4. ADR: агент MADR → человек коммитит. 5. Approach: Requirements + ADR → агент с диаграммами. 6. API Spec: агент OpenAPI → Spectral lint → валидация. 7. BDD (опц.): агент Gherkin → бизнес валидирует. 8. Tasks: агент с зависимостями/оценками → планирование. 9. Implementation: для каждого таска — человек выбирает → агент код+тесты → автотесты → ревью и merge. 10. Verification: все тесты + requirements coverage check → финальный ревью.

## Источники

- Входные материалы inbox: `documentation-process-v2/ai-agent-workflows/README.md`
- Связанные KB: `agents-constitution.md` (дurable context), `artifact-pipeline.md` (роли по этапам v3), `../principles/attention-economy.md`, `../principles/invariants-and-gates.md`
