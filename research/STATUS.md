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
| documentation-process-v2/goals.md | done | kb/principles/process-design-goals.md | полный (Vision, 5 принципов, Requirements, Constraints, Metrics, Risks) | 2026-09-30 |
| documentation-process-v2/knowledge-base.md | rejected | — | Каталог из 17 разделов, ~90% покрыт KB-статьями фаз 1–5; уникальные сущности (Structurizr, Volere/IREB, Zachman, 4+1, RFD, FitNesse/Concordion/JGiven/Spock, Alloy/Event-B, ISO 25010 перечень, ATAM/QAW, docToolchain, Read the Docs, Domain Storytelling, Event Modeling, Impact Mapping, Amazon PR/FAQ, Google Design Doc) — учтены в landscape-статьях как упоминания; отдельной ценности сверх KB не несёт | 2026-09-30 |
| documentation-process-v2/modular-process.md | done | kb/methods/artifact-pipeline.md, process-levels.md, artifact-templates.md | полный | 2026-09-30 |
| documentation-process-v2/process-variants.md | done | kb/methods/process-levels.md (фазовая эволюция), artifact-pipeline.md (композиции pipelines) | Навигационные артефакты поглощены (Decision Matrix, сравнительная таблица 7 pipelines, hybrid-рецепты); модель «7 named pipelines» замещена модульной сборкой + уровнями (формула KB: «не выбирайте pipeline — соберите его») | 2026-09-30 |
| documentation-process-v2/modules/README.md | done | kb/methods/artifact-pipeline.md, process-levels.md | полный | 2026-09-30 |
| documentation-process-v2/modules/problem-statement.md | done | kb/methods/artifact-templates.md | полный | 2026-09-30 |
| documentation-process-v2/modules/prd.md | done | kb/methods/artifact-templates.md | полный | 2026-09-30 |
| documentation-process-v2/modules/rfc.md | done | kb/methods/artifact-templates.md | полный | 2026-09-30 |
| documentation-process-v2/modules/approach.md | done | kb/methods/artifact-templates.md | полный | 2026-09-30 |
| documentation-process-v2/modules/requirements.md | done | kb/methods/artifact-templates.md | полный | 2026-09-30 |
| documentation-process-v2/modules/bdd.md | done | kb/methods/artifact-templates.md | полный | 2026-09-30 |
| documentation-process-v2/modules/adr.md | done | kb/methods/artifact-templates.md | полный | 2026-09-30 |
| documentation-process-v2/modules/api-specs.md | done | kb/methods/artifact-templates.md | полный | 2026-09-30 |
| documentation-process-v2/modules/tasks.md | done | kb/methods/artifact-templates.md | полный | 2026-09-30 |
| documentation-process-v2/modules/implementation.md | done | kb/methods/artifact-templates.md | полный | 2026-09-30 |
| documentation-process-v2/versioning-lifecycle/README.md | done | kb/methods/versioning-lifecycle.md | полный | 2026-09-30 |
| documentation-process-v2/storage-organization/README.md | done | kb/methods/repository-structure.md | полный | 2026-09-30 |
| documentation-process-v2/tools-automation/README.md | done | kb/landscape/toolchain-registry.md | полный | 2026-09-30 |
| documentation-process-v2/review-collaboration/README.md | done | kb/methods/review-collaboration.md | полный | 2026-09-30 |
| documentation-process-v2/scaling/README.md | done | kb/methods/process-levels.md | полный | 2026-09-30 |
| documentation-process-v2/metrics-dashboards/README.md | done | kb/methods/metrics-dashboards.md | полный | 2026-09-30 |
| documentation-process-v2/training-onboarding/README.md | done | kb/methods/training-onboarding.md | полный | 2026-09-30 |
| documentation-process-v2/ai-agent-workflows/README.md | done | kb/methods/ai-agent-workflows.md | полный | 2026-09-30 |
| documentation-process-v2/examples/export-service/ | partial | kb/methods/process-examples.md | README + все артефакты (specs/, docs/, features/) поглощены в разбор; каталог остаётся в inbox как копируемый эталон до фазы 7 (архивировать или перенести в guide/examples) | 2026-09-30 |

### Группа C — процессы v3 (`inbox/documentation-process-v3/`)

| source | статус | куда выгружено | охват / остаток | сессия |
|---|---|---|---|---|
| documentation-process-v3/00-goals.md | done | kb/methods/process-levels.md, artifact-pipeline.md | полный (P1–P10, G1–G6, критерии успеха поглощены) | 2026-09-30 |
| documentation-process-v3/01-knowledge-summary.md | rejected | — | Каталог из 11 разделов, ~90% покрыт KB фаз 1–5; уникальное (Any Decision Records, docToolchain, pyadr, Concordion/JGiven/FitNesse/Spock, Domain Story Telling, Event Modeling, Impact Mapping, Example Mapping, Amazon PR/FAQ, Google Design Doc, Read the Docs) — учтено в landscape-статьях; пробелы №2 (Human↔AI approval-гейты) и №3 (CI-пайплайн) закрыты статьями ai-agent-workflows.md и docs-cicd.md | 2026-09-30 |
| documentation-process-v3/02-process-design.md | done | kb/methods/artifact-pipeline.md, process-levels.md | полный | 2026-09-30 |
| documentation-process-v3/03-open-questions-analysis.md | done | kb/methods/agents-constitution.md (прототипы), kb/landscape/toolchain-registry.md (Spec Kit vs OpenSpec, EARS storage вариант A), repository-structure.md (ideas/) | полный; 6 открытых вопросов с рекомендациями поглощены | 2026-09-30 |
| documentation-process-v3/04-tool-selection-and-migration.md | done | kb/landscape/toolchain-registry.md | полный | 2026-09-30 |
| documentation-process-v3/05-agents-and-constitution-guide.md | done | kb/methods/agents-constitution.md | полный | 2026-09-30 |
| documentation-process-v3/06-repository-structure.md | done | kb/methods/repository-structure.md | полный | 2026-09-30 |
| documentation-process-v3/07-cicd-docs-pipeline.md | done | kb/methods/docs-cicd.md | полный | 2026-09-30 |
| documentation-process-v3/09-toolchain-registry.md | done | kb/landscape/toolchain-registry.md | полный | 2026-09-30 |
| documentation-process-v3/08-examples/ | partial | kb/methods/process-examples.md | README + 3 примера (L1/L2/L3) разобраны; каталог остаётся в inbox как копируемый эталон до фазы 7 | 2026-09-30 |

### Группа D — критика SDD (`inbox/documentation-process-criticism/`)

| source | статус | куда выгружено | охват / остаток | сессия |
|---|---|---|---|---|
| documentation-process-criticism/q1/README.md | done | kb/landscape/sdd-criticism.md (реестр источников) | Реестр ссылок поглощён в раздел «Источники» статей фазы 2; 18+ внешних ссылок — также вход для фазы 6 | 2026-09-30 |
| documentation-process-criticism/q1/ai-development-processes-analysis.md | done | kb/principles/ (все 5), kb/landscape/sdd-criticism.md | полный; фреймворковые детали → доп. вход для фазы 6 | 2026-09-30 |
| documentation-process-criticism/q1/sdd-frameworks-analysis.md | done | kb/principles/process-over-tool.md, kb/landscape/sdd-criticism.md | полный; сценарные рекомендации и чек-листы vendor-lock — доп. вход для фазы 6 | 2026-09-30 |
| documentation-process-criticism/g1/openspec-sdd-process-criticism.md | done | kb/principles/ (все 5), kb/landscape/sdd-criticism.md | полный | 2026-09-30 |
| documentation-process-criticism/g1/open-sdd-frameworks-comparison.md | done | kb/landscape/sdd-criticism.md | Принципы и вердикты поглощены; детальный ландшафт (project health, контекст-модели, новые альтернативы) — вход для фазы 6 | 2026-09-30 |
| documentation-process-criticism/d1/openspec-sdd-criticism-and-principles.md | done | kb/principles/ (все 5), kb/landscape/sdd-criticism.md | полный | 2026-09-30 |
| documentation-process-criticism/d1/open-source-sdd-frameworks-review.md | done | kb/landscape/sdd-criticism.md | Принципы и вердикты поглощены; обзор 18+ фреймворков — вход для фазы 6 | 2026-09-30 |

### Группа E — исследовательские процессы (`inbox/research-and-notes/`)

| source | статус | куда выгружено | охват / остаток | сессия |
|---|---|---|---|---|
| research-and-notes/research-process.md | done | kb/methods/research-knowledge.md (ч.1, стр. 1–629), kb/principles/content-stays-virtual-structure.md (ч.2, стр. 630–1567), kb/methods/research-tooling.md (ч.3, стр. 1568–2229), kb/landscape/spec-kitty-research.md (ч.4, стр. 2230–3019) | полный; все 4 части поглощены | 2026-09-30 |

### Группа F — бэклог внешних источников (`inbox/README.md`)

| source | статус | куда выгружено | охват / остаток | сессия |
|---|---|---|---|---|
| inbox/README.md (spec-weave, Spec Kitty, specs.md, Spec Kit) | done | kb/landscape/spec-weave.md, spec-kitty-research.md (фаза 4+fix), sdd-tools-overview.md (обновление), sdd-criticism.md (приложение) | Spec-weave исследован (сайт + GitHub README v3.0.0); Spec Kitty/specs.md покрыты в фазе 4; Spec Kit — источник решений (toolchain-registry); свежий поиск: OpenSpec 126K (08.2026), Kiro GA free tier, BMAD/Spec Kit статус | 2026-09-30 |

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
| Дешевая форма требования: тип/контракт/PBT/пример/ADR, проза — только для дорогоформализуемого | D (kb/principles/cheapest-form.md; Dhwtj, Шапиро, Бём) | Ядро собственной системы: артефакты выбираются по цене удержания, не по шаблону |
| Явные инварианты с rationale + блокирующие машинные gate вне досягаемости агента | D (kb/principles/invariants-and-gates.md; Gromilo, EPAM, issue #194) | Прямо ложится на дизайн harness: hooks/CI > промпты |
| Экономика внимания: машина фильтрует, человек решает только по квалифицированным расхождениям; масштаб процесса = f(сложность, цена ошибки) | D (kb/principles/attention-economy.md; Шапиро, Nadeem) | Соединяется с уровнями L0–L4 (C/00): уровни как механизм экономики внимания |
| Молчание ≠ согласие; явная приёмка + фриз; ведомость допущений (удача оставляет след) | D (kb/principles/ai-degradation-phenomena.md; Шапиро) | Уникальный протокол приёмки AI-изменений; дифференциатор собственной системы |
| Сжатые представления как индексы к коду (6 типов), не вторая спека | D (kb/principles/ai-degradation-phenomena.md; Шапиро) | Кандидат на механизм durable context для агентов |
| Процесс проектируется владельцем; инструмент оборачивается в свою абстракцию; план миграции | D (kb/principles/process-over-tool.md; Isenberg) | Принцип для собственной системы: она и есть «своя абстракция» поверх готовых частей |
| Место артефактов определяет доступность процесса (upstream-работа — не обязательно репо) | D (Talk Think Do кейс) | Граница git-native принципа: требования upstream — вне репо, с зеркалированием |
| Две оси масштаба: инициатива (L0–L4, per-изменение) × организация (S1–S5, per-команда) | Синтез фазы 3 (kb/methods/process-levels.md) | Разделяет «сколько документов на изменение» и «сколько governance»; кандидат в архитектуру новой системы |
| Promotion-цепочка артефактов: idea→task→prd→rfc→adr со статусом promoted | v3 (kb/methods/artifact-pipeline.md) | Артефакты не рождаются «правильного уровня», а растут; сочетается с «content stays, structure is virtual» |
| Трассировка через YAML front-matter (id/type/status/traces) + CI-проверка ссылок | v3 02/06 | Машинно-проверяемый след решений; механизм для собственной системы |
| Реестр инструментов с exit strategies и quarterly health check (любой инструмент заменим ≤ 1 sprint) | v3 09 (kb/landscape/toolchain-registry.md) | Vendor-exit как операционная практика, не лозунг; прямое применение к собственному тулчейну |
| Эталоны как few-shot examples для AI-агентов (нормативные заполненные примеры L1/L2/L3) | v3 08-examples | Канонические примеры против наплыва (Шапиро): агент получает образец, а не только правила |
| Инсайты #1–7 как основание архитектуры KB (иерархия = оглавление; статус в frontmatter + структуре; не перемещать; скрипт вместо агента; много тем; симлинки; ссылка дешевле файла) | E ч.2 (kb/principles/content-stays-virtual-structure.md; пользователь) | Сформулированы пользователем, развиты в полную архитектуру — претендент на ядро новой системы |
| Симлинки как primary-навигация + frontmatter как source of truth + MOC опционально (вердикт после честного разбора рисков) | E ч.2 | Конкретное архитектурное решение для KB системы; риски купированы (относительные пути, sync-скрипт, CI verify) |
| Двухрежимный CLI (dual-mode): интерактив для человека, флаги+JSON для агента | E ч.3 (kb/methods/research-tooling.md; прецедент uvtemplate) | Принцип дизайна всех инструментов собственной системы |
| Ядро + project-local кастомизация (.research/: templates/config/hooks/extensions с fallback chain) | E ч.3 (паттерн Spec Kit/pre-commit/Husky) | Архитектура распространения собственного tooling без vendor-lock |
| Research как фаза delivery pipeline (Ideation → Research → Spec → Plan → Implement), не отдельная ниша | E ч.4 (пересмотр позиции) | Меняет границы собственной системы: research-функцию можно adopt (Spec Kitty), не строить |
| Evidence-gated state machine для research (guards: минимум 3 источника, findings.md обязателен) + evidence-log.csv | E ч.4 (Spec Kitty) | Конкретный механизм блокирующих gate для research-процесса; соответствует принципу invariants-and-gates |
| AGENTS.md как canonical cross-tool standard + tool-specific файлы импортируют (@AGENTS.md); hierarchical loading (ближайший в дереве) | v3 05 (kb/methods/agents-constitution.md) | Решает durable context без vendor-lock на harness; прямой паттерн для собственной системы |
| CONSTITUTION.md immutable + amendment через RFC + Governance-секция | v3 05/03 | Механизм «конституции» собственной системы: принципы с явным процессом изменения |
| HITL-паттерны (AI Drafts Human Decides / Generates Validates / Assists Executes / Human Defines AI Implements) как именованные протоколы | v2 ai-agent-workflows | Каталог протоколов human↔AI handoff — операционный слой системы |
| Quality gates как серия блокирующих CI-проверок для документации (EARS → coverage → architecture → tests → AI metrics) | v3 07 + v2 metrics | Docs-as-Code gate — реализация принципа invariants-and-gates для артефактов |
| Error Pattern Dashboard + prevention (prompt templates с anti-patterns, checklists) как механизм обучения процесса | v2 metrics | Замыкает feedback loop: ошибка → pattern → защита в tooling, а не в инструкциях |
| Ленивая консенсусность (lazy consensus) конфликтует с «молчание ≠ согласие» — зона напряжения | v2 review vs Шапиро | Кандидат на разбор в ideas/: где молчание допустимо (minor), где — нет (accepted) |
| Cross-tool handoff (hand off / pick up) + project memory, переносимая с кодом (.specweave/memory/) | F (SpecWeave) | Решает «AI forgets everything between sessions» на уровне delivery и переносит durable context между вендорами/аккаунтами — уникальный механизм, кандидат для собственной системы |
| Блокирующий evidence-gate `task done --run` (отказ при падающем тесте) + append-only ledger (claims, evidence) | F (SpecWeave) | Конкретная реализация invariants-and-gates на уровне задач; ledger — аудируемый след работы агентов |
| Enforcement/handoff/evidence как конкурентное преимущество SDD-инструментов (подтверждение тезиса критики рынком) | Фаза 6 (свежий поиск) | Тезис «дешёвый машинный enforcement решает судьбу SDD» подтверждён появлением инструментов с блокирующими gate — сигнал для приоритетов собственной системы |

## Протокол сессии

1. **Старт:** прочитать `research/PLAN.md` + этот файл → выбрать фазу/строки.
2. **Работа:** обработка источников → запись в `research/kb/`, `guide/`, журнал выше.
3. **Конец:** обновить статусы и «охват / остаток»; обновить `research/kb/meta.yaml`; коммит.

## История сессий

| Дата | Фаза | Что сделано |
|---|---|---|
| 2026-09-30 | 0 | Инвентаризация inbox (74 файла, 6 групп A–F), PLAN.md accepted (Q1–Q3, Q5), STATUS.md создан, журнал идей начат. Пользователь указал входы ideas (инсайты E #1–7, «Симлинки против MOC», B/goals, B/modular-process, C/00) + принцип «избегать ненужного трения»; добавлен протокол отклонений от пути (PLAN §5.4); правило: коммит после каждой фазы |
| 2026-09-30 | 1 | Группа A поглощена: 8 KB-статей (methods: adr, ears, rfc-vs-sdd, prd, c4-arc42, research-compendium; landscape: bdd-tools, sdd-tools-overview) + kb/README.md (формат статьи) + meta.yaml (8 записей). Все 9 источников A → done |
| 2026-09-30 | 2 | Группа D поглощена: 5 статей kb/principles/ (ai-degradation-phenomena, cheapest-form, invariants-and-gates, attention-economy, process-over-tool) + kb/landscape/sdd-criticism.md (синтез критики, основа главы 4). Все 7 источников D → done; журнал идей +7 записей. При правке meta.yaml сломал YAML — починен, инвариант перепроверен |
| 2026-09-30 | 3 | Процессное ядро (синтез v2+v3 с нуля): 6 статей — methods/process-levels (две оси L0–L4 × S1–S5), artifact-pipeline (6 core + 9 optional, трассировка), artifact-templates (10 модулей), repository-structure (синтез v3/06 + v2/storage), process-examples (L1/L2/L3 + export-service); landscape/toolchain-registry (скоринг, exit strategies, health check). 22 источника → done, 2 эталона → partial (остаются как копируемые примеры до фазы 7). Журнал идей +5 |
| 2026-09-30 | 4 | Группа E поглощена по 4 частям: kb/methods/research-knowledge.md (ч.1), kb/principles/content-stays-virtual-structure.md (ч.2 — инсайты #1–7 + симлинки vs MOC, ядро кандидата в систему), kb/methods/research-tooling.md (ч.3), kb/landscape/spec-kitty-research.md (ч.4). E → done; журнал идей +6 |
| 2026-09-30 | 5 | Остаток B/C поглощён: 8 статей — methods/agents-constitution, ai-agent-workflows, docs-cicd, review-collaboration, versioning-lifecycle, metrics-dashboards, training-onboarding; principles/process-design-goals. 11 источников → done, 2 корпуса (v2 knowledge-base, v3 01) → rejected (~90% покрытия KB, уникальное учтено). Журнал идей +6. Весь корпус inbox обработан (кроме F — фаза 6) |
| 2026-09-30 | 4-fix | Восстановление выжимки E4 (была усечена на 264 строках): перезапуск скаута с явным требованием всех 8 секций. Восстановлено: варианты A–D с содержанием, 3 итерации пересмотра позиции («ниша уникальна» → «specs.md покрывает research» → «Spec Kitty — наиболее полный инструмент»), таблицы Spec Kit/Kitty/specs.md + research-поддержка + сопоставление с notes/+views/, команды, 12 URL. kb/landscape/spec-kitty-research.md дополнена (224 строки), статус → reviewed |
| 2026-09-30 | 6 | Группа F закрыта: spec-weave исследован (сайт + GitHub README v3.0.0 от 2026-09-25) → kb/landscape/spec-weave.md (cross-tool handoff, evidence-gate, ledger, memory). Свежий поиск: OpenSpec 126K (08.2026), Kiro GA free tier, BMAD/Spec Kit статус — обновлены sdd-tools-overview.md и sdd-criticism.md (приложение «тезис enforcement подтверждён рынком»). Журнал идей +3. **Весь корпус inbox обработан (74 файла + F)** |
