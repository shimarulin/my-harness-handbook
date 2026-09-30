# Уровни масштаба процесса (синтез v2+v3)

| Параметр | Значение |
|---|---|
| Статус | draft |
| Обновлено | 2026-09-30 |

## Что это

Модель масштабирования процесса разработки: набор обязательных артефактов и глубина ревью определяются **размером и ценой ошибки инициативы**, а не являются константой. Синтезирована из двух линеек: уровни инициативы **L0–L4** (v3, per-инициатива) и уровни организации **S1–S5** (v2 scaling, per-проект/команда). Ключевая идея обеих: «меняется количество артефактов, не подход» и «процесс меняется под масштаб, а не наоборот».

Принцип-основание из критики SDD: сложность процесса должна соответствовать сложности задачи и цене ошибки — экономика внимания (`../principles/attention-economy.md`). Уровни — механизм этой экономики.

## Две оси масштаба

| Ось | Что определяет | Источник | Диапазон |
|---|---|---|---|
| **Инициатива (L0–L4)** | Набор артефактов и gates для одного изменения | v3 | Выбирается автором при создании артефакта идеи |
| **Организация (S1–S5)** | Процессный контекст проекта/команды (governance, координация) | v2 scaling | Определяется размером команды/кодовой базы |

Оси независимы: L3-инициатива возможна в S2-команде (solo с архитектурным решением), L1-задача — в S5-enterprise (hotfix с compliance-контекстом).

## Уровни инициативы L0–L4

| Уровень | Размер | Обязательные артефакты | Overhead на доки | AI-сессии | Ревью |
|---|---|---|---|---|---|
| **L0** Trivial | Typo, hotfix, рефакторинг без поведенческих изменений | Нет; коммит `trivial: <описание>` | ~0 | Опционально | Code review |
| **L1** Small | Локальное изменение, один контекст | `tasks/NNN-*.md` (Job Story + чеклист) + связанный PR | ~10–15 мин | 1 сессия | Code review |
| **L2** Feature | Фича, несколько сессий/людей | PRD-lite `docs/prd/NNN-*.md` + `docs/specs/NNN-*/{spec.md (EARS), design.md (notes), tasks.md}` | ~2–4 ч | 2–3 сессии | Spec review + code review |
| **L3** Major | Крупная фича, архитектурные последствия | L2 + RFC `docs/rfc/NNNN-*.md` + ADR (MADR) `docs/adr/NNNN-*.md` + Gherkin `scenarios/*.feature` + C4-диаграммы | ~1–2 дня | Много | RFC review + ADR + spec + code |
| **L4** Platform | Новая платформа/продукт | L3 + PRD полный (+Amazon PR/FAQ) + arc42 (12 секций) + C4 все уровни + quality scenarios (+ ArchiMate/TOGAF только если требуется; Research Compendium для R&D-частей) | дни | Много | Полное |

Правила:
- **Docs-first**: переход на следующий этап — только при `approved` артефакте предыдущего (кроме L0). PR без связанного артефакта не принимается (кроме `trivial`).
- **AI-агент** не имплементирует без approved-спеки (кроме L0); на L1 задача укладывается в одно context window.
- L0/L1: SDD-инструменты (Spec Kit/OpenSpec) — overkill; прямой коммит / лёгкий task-файл.

## Продвижение между уровнями (только вверх)

Артефакты не выбрасываются, а **разворачиваются** (принцип P9: обратная совместимость масштаба):

| Переход | Механика |
|---|---|
| L1→L2 | task.md (Job Story) разворачивается в PRD (та же история, больше деталей) |
| L2→L3 | design notes оформляются в RFC; новое архитектурное решение → обязательно ADR |
| L3→L4 | RFC-серия консолидируется в arc42-документ |

Понижение уровня не описано ни в одном источнике — открытый вопрос (на практике: если инициатива сдулась, артефакты остаются как есть, уровень не пересматривается задним числом).

## Уровни организации S1–S5 (v2 scaling)

| Уровень | Команда | Длительность | LOC | Процесс (добавки к L-уровням) |
|---|---|---|---|---|
| **S1** Solo | 1–2 | < 3 мес | < 10k | Problem Statement в commit message; ADR только для major (Y-Statements в `docs/decisions.md`) |
| **S2** Small Team | 3–5 | 3–6 мес | 10k–50k | Requirements (EARS, lightweight) + ADR для всех архитектурных решений |
| **S3** Growing | 5–15 | 6–18 мес | 50k–200k | + Approach + Tasks + BDD; RFC для дебатов; C4 |
| **S4** Large | 15–50 | 1–3 года | 200k–1M | + PRD + API Specs; monorepo/multi-service; cross-team RFC/ADR |
| **S5** Enterprise | 50+ | 3+ лет | 1M+ | + ARB gate после RFC, security review, compliance audit (GDPR/HIPAA/SOX) |

Триггеры upgrade: team size > порога; длительность > порога; накопление техдолга; coordination overhead; compliance. Паттерны роста: vertical (проект растёт S1→S5), horizontal (много проектов на разных S + shared standards), federation (независимые команды, стандартизированы только inter-team контракты).

## Соответствие модульной сборке (v2 modules)

L-уровни и модули — две проекции одной модели:

| Уровень | В терминах модулей (`artifact-pipeline.md`) |
|---|---|
| L0 | Только Implementation (+ commit) |
| L1 | Problem Statement (Job Story форма) + Tasks-lite + Implementation |
| L2 | Core: Problem Statement → Requirements → Approach → Tasks → Implementation (+ PRD-lite как product-обёртка) |
| L3 | Core + RFC + ADR + BDD + API Specs (по критериям) |
| L4 | Все модули: + PRD полный + arc42 + Formal Methods (по критериям) + Research Compendium |

## Критерии успеха масштабирования (v3)

- **Scale-тест**: L1-задача — overhead ≤ 15 минут на документацию; L4 — полный набор артефактов.
- **Анти-паттерны** (v2 scaling): premature scaling (enterprise-процессы для small team), inconsistent scaling (команды на разных уровнях без shared standards), tooling without process (shelfware), manual at scale, governance without value (bureaucracy без clear value).

## Сильные и слабые стороны

Сильные: overhead пропорционален риску (закрывает главную критику SDD — «хирургия вилочным погрузчиком»); продвижение вверх без переписывания сохраняет след решений; две оси разделяют «сколько документов на изменение» и «сколько governance на организацию».

Слабые / риски: уровень выбирает автор инициативы — риск систематического занижения (лечится review и метриками: rework rate, spec-code alignment); границы L1/L2 размыты (когда «малое изменение» становится «фичей» — на практике: выходит за одно context window / один день); понижение уровня не определено; S-пороги (team/duration/LOC) — эвристики, не законы.

## Источники

- Входные материалы inbox: `documentation-process-v3/00-goals.md` (уровни L0–L4, принципы P1–P10, критерии успеха), `documentation-process-v3/02-process-design.md` (механика уровней, продвижение, правила агентов), `documentation-process-v2/scaling/README.md` (уровни S1–S5, паттерны роста, метрики, анти-паттерны), `documentation-process-v2/modular-process.md`, `documentation-process-v2/modules/README.md` (уровни сборки 1–4), `documentation-process-v3/08-examples/README.md` (overhead-бюджеты)
- Связанные KB: `artifact-pipeline.md`, `../principles/attention-economy.md`
