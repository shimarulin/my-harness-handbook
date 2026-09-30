# STATUS — трекинг обработки research/inbox

Метод: см. `research/PLAN.md` §5. Обновляется в конце каждой рабочей сессии.

**Текущая фаза:** 0 → готовность к фазе 1 (сессия 2026-09-30)

## Легенда статусов

| Статус | Значение |
|---|---|
| `new` | Не тронут |
| `triaged` | Прочитан, определено назначение (куда пойдёт) |
| `partial` | Частично выгружен — см. колонку «охват / остаток» |
| `done` | Выгружен полностью в KB/guide/ideas |
| `archived` | done + источник закрыт (можно убирать из inbox) |
| `deferred` | Сознательно отложен (причина в «остатке») |
| `rejected` | Не несёт ценности (причина обязательна) |

## Источники

### Группа A — референс-справочники (`inbox/documentation-process/`)

| source | статус | куда выгружено | охват / остаток | сессия |
|---|---|---|---|---|
| documentation-process/index.md | rejected | — | Индексная функция поглощена: формат статьи (5 пунктов) → kb/README.md, матрица выбора → разделы «Сравнение / выбор» KB-статей и guide гл.3 (фаза 7), реестр → kb/meta.yaml. Отдельной ценности сверх этого не несёт | 2026-09-30 |
| documentation-process/reference/sdd-landscape.md | done | kb/landscape/sdd-tools-overview.md | полный | 2026-09-30 |
| documentation-process/reference/prd.md | done | kb/methods/prd.md | полный | 2026-09-30 |
| documentation-process/reference/rfc-vs-sdd.md | done | kb/methods/rfc-vs-sdd.md | полный | 2026-09-30 |
| documentation-process/reference/adr-standards.md | done | kb/methods/adr.md | полный | 2026-09-30 |
| documentation-process/reference/architecture-c4-arc42.md | done | kb/methods/c4-arc42.md | полный | 2026-09-30 |
| documentation-process/reference/bdd-alternatives.md | done | kb/landscape/bdd-tools.md | полный | 2026-09-30 |
| documentation-process/reference/ears-notation.md | done | kb/methods/ears.md | полный | 2026-09-30 |
| documentation-process/reference/research-compendium.md | done | kb/methods/research-compendium.md | полный | 2026-09-30 |

### Группа B — процессы v2 (`inbox/documentation-process-v2/`)

| source | статус | куда выгружено | охват / остаток | сессия |
|---|---|---|---|---|
| documentation-process-v2/goals.md | triaged | guide гл.2 (принципы) | Сырьё для синтеза (Q3) | 2026-09-30 |
| documentation-process-v2/knowledge-base.md | new | → kb/landscape/ (по темам) | | |
| documentation-process-v2/modular-process.md | new | → синтез гл.5 | | |
| documentation-process-v2/process-variants.md | new | → синтез гл.5 | | |
| documentation-process-v2/modules/README.md | new | → синтез гл.5 | | |
| documentation-process-v2/modules/problem-statement.md | new | → kb/methods/ + гл.5 | | |
| documentation-process-v2/modules/prd.md | new | → kb/methods/ + гл.5 | | |
| documentation-process-v2/modules/rfc.md | new | → kb/methods/ + гл.5 | | |
| documentation-process-v2/modules/approach.md | new | → kb/methods/ + гл.5 | | |
| documentation-process-v2/modules/requirements.md | new | → kb/methods/ + гл.5 | | |
| documentation-process-v2/modules/bdd.md | new | → kb/methods/ + гл.5 | | |
| documentation-process-v2/modules/adr.md | new | → kb/methods/ + гл.5 | | |
| documentation-process-v2/modules/api-specs.md | new | → kb/methods/ + гл.5 | | |
| documentation-process-v2/modules/tasks.md | new | → kb/methods/ + гл.5 | | |
| documentation-process-v2/modules/implementation.md | new | → kb/methods/ + гл.5 | | |
| documentation-process-v2/versioning-lifecycle/README.md | new | → guide гл.9 | | |
| documentation-process-v2/storage-organization/README.md | new | → guide гл.6 | | |
| documentation-process-v2/tools-automation/README.md | new | → guide гл.6 | | |
| documentation-process-v2/review-collaboration/README.md | new | → guide гл.9 | | |
| documentation-process-v2/scaling/README.md | new | → guide гл.5 | | |
| documentation-process-v2/metrics-dashboards/README.md | new | → guide гл.9 | | |
| documentation-process-v2/training-onboarding/README.md | new | → guide гл.9 | | |
| documentation-process-v2/ai-agent-workflows/README.md | new | → guide гл.7 | | |
| documentation-process-v2/examples/export-service/ | new | → guide гл.5 (сквозной пример) | целиком, со src/specs/docs | |

### Группа C — процессы v3 (`inbox/documentation-process-v3/`)

| source | статус | куда выгружено | охват / остаток | сессия |
|---|---|---|---|---|
| documentation-process-v3/00-goals.md | triaged | guide гл.1–2 | Принципы P1–P10, уровни L0–L4 — сырьё для синтеза (Q3) | 2026-09-30 |
| documentation-process-v3/01-knowledge-summary.md | new | → kb/landscape/, kb/methods/ (по разделам 1–11) | | |
| documentation-process-v3/02-process-design.md | new | → синтез гл.5 | | |
| documentation-process-v3/03-open-questions-analysis.md | new | → guide гл.10, ideas/ | | |
| documentation-process-v3/04-tool-selection-and-migration.md | new | → guide гл.6, kb/landscape/ | | |
| documentation-process-v3/05-agents-and-constitution-guide.md | new | → guide гл.7 | | |
| documentation-process-v3/06-repository-structure.md | new | → guide гл.6 | | |
| documentation-process-v3/07-cicd-docs-pipeline.md | new | → guide гл.9 | | |
| documentation-process-v3/09-toolchain-registry.md | new | → kb/landscape/toolchain-registry.md | | |
| documentation-process-v3/08-examples/ | new | → guide гл.5 (примеры L1/L2/L3) | | |

### Группа D — критика SDD (`inbox/documentation-process-criticism/`)

| source | статус | куда выгружено | охват / остаток | сессия |
|---|---|---|---|---|
| documentation-process-criticism/q1/README.md | triaged | — | Индекс источников: 18+ ссылок — вход для фазы 6 | 2026-09-30 |
| documentation-process-criticism/q1/ai-development-processes-analysis.md | new | → kb/principles/ + guide гл.4 | | |
| documentation-process-criticism/q1/sdd-frameworks-analysis.md | new | → kb/principles/ + guide гл.4 | | |
| documentation-process-criticism/g1/openspec-sdd-process-criticism.md | new | → kb/principles/ + guide гл.4 | | |
| documentation-process-criticism/g1/open-sdd-frameworks-comparison.md | new | → kb/landscape/sdd-tools-* | | |
| documentation-process-criticism/d1/openspec-sdd-criticism-and-principles.md | new | → kb/principles/ + guide гл.4 | | |
| documentation-process-criticism/d1/open-source-sdd-frameworks-review.md | new | → kb/landscape/sdd-tools-* | | |

### Группа E — исследовательские процессы (`inbox/research-and-notes/`)

| source | статус | куда выгружено | охват / остаток | сессия |
|---|---|---|---|---|
| research-and-notes/research-process.md | triaged | → kb/methods/research-knowledge.md + guide гл.8 | 302 заголовка, ~5 логических частей; обрабатывать по секциям | 2026-09-30 |

### Группа F — бэклог внешних источников (`inbox/README.md`)

| source | статус | куда выгружено | охват / остаток | сессия |
|---|---|---|---|---|
| inbox/README.md (spec-weave, Spec Kitty, specs.md, Spec Kit) | deferred | → kb/landscape/sdd-tools-* (фаза 6) | Ждёт фазы 6: исследование + свежий поиск | 2026-09-30 |

## Журнал идей-кандидатов (вход для ideas/, фаза 8)

Пополняется по ходу фаз 1–5. Формат: идея → где встретилась → почему ценна.

| Идея | Источник | Потенциальная ценность |
|---|---|---|
| Уровни масштаба процесса (L0–L4) с продвижением артефактов вверх | C/00-goals | Overhead пропорционален риску; ядро собственной системы |
| Durable context: артефакты как долговременная память агентов | C/00, E | Снимает переобъяснение контекста; принцип для harness-дизайна |
| «Формат первичен, инструмент вторичен» | C/00 (P2, P10) | Vendor-exit как тестируемый критерий |
| Approval-гейты: человек утверждает, агент исполняет | C/00 (P8), D | Разделение ответственности human/AI |
| Предсказуемая структура важнее графа для AI-retrieval | E | Принцип организации KB под агентов |
| «Content stays, structure is virtual»: файлы не перемещаются, статус в frontmatter, навигация через views | E, инсайты #3–#7 (стр. 618–628, 704–751) | Чистый diff, дешёвые операции агента; основа архитектуры KB |
| Симлинки как primary-навигация (views/), MOC — опционально для аннотированных обзоров | E, «Симлинки против MOC» (стр. 1096–1562) | Нативная навигация (tree/IDE/ls) для человека и агента; риски купированы: относительные пути + sync-скрипт + запрет перемещений |
| Инсайт → практическая проверка → правило в CONVENTIONS.md | E (стр. 634–641) | Pipeline промоции знаний о самом процессе; механизм эволюции системы |
| Vision + Core Principles v2: docs-first, open formats, git-native, human+AI, scalability | B/goals.md | Проверенный набор принципов — сырьё для конституции новой системы |
| Модульность процесса: артефакты как компонуемые модули с явными интерфейсами | B/modular-process.md | Процесс собирается под задачу, а не монолитен; сочетается с уровнями масштаба |
| G4 human+AI collaboration, G5 масштабируемость, G2 docs-first, принципы P1–P10 | C/00-goals.md | Целевые свойства системы + критерии успеха (traceability/onboarding/vendor-exit/scale/AI тесты) |
| Избегать ненужного трения | Сквозной принцип (пользователь, 2026-09-30) | Каждое решение проверяется: не добавляет ли friction сверх ценности |

## Протокол сессии

1. **Старт:** прочитать `research/PLAN.md` + этот файл → выбрать фазу/строки.
2. **Работа:** обработка источников → запись в `research/kb/`, `guide/`, журнал выше.
3. **Конец:** обновить статусы и «охват / остаток»; обновить `research/kb/meta.yaml`; коммит.

## История сессий

| Дата | Фаза | Что сделано |
|---|---|---|
| 2026-09-30 | 0 | Инвентаризация inbox (74 файла, 6 групп A–F), PLAN.md accepted (Q1–Q3, Q5), STATUS.md создан, журнал идей начат. Пользователь указал входы ideas (инсайты E #1–7, «Симлинки против MOC», B/goals, B/modular-process, C/00) + принцип «избегать ненужного трения»; добавлен протокол отклонений от пути (PLAN §5.4); правило: коммит после каждой фазы |
| 2026-09-30 | 1 | Группа A поглощена: 8 KB-статей (methods: adr, ears, rfc-vs-sdd, prd, c4-arc42, research-compendium; landscape: bdd-tools, sdd-tools-overview) + kb/README.md (формат статьи) + meta.yaml (8 записей). Все 9 источников A → done |
