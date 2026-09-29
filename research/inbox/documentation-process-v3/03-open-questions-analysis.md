# Анализ открытых вопросов: процессы v3

| Параметр | Значение |
|---|---|
| Дата | 2026-09-29 |
| Статус | Draft |
| Связан с | `02-process-design.md` §8 |
| Следующий шаг | Эксперименты (см. §7) |

---

## 1. BDD-инструмент: важна ли Gherkin-переносимость?

### Постановка

Исходный вопрос предполагал выбор primary BDD-инструмента per-стек
(Cucumber vs Reqnroll vs Behave vs Gauge) с критерием Gherkin-переносимости.
Пользователь предлагает: **стек неважен, инструмент должен работать на любом
проекте**.

### Анализ

**Так ли важна Gherkin-переносимость?**

Gherkin — межинструментный формат сценариев (Given-When-Then), поддерживаемый
Cucumber (Java/JS/Ruby), Reqnroll (.NET), Behave (Python), Behat (PHP).
Если Gherkin-файлы хранятся в `tests/features/`, их можно запускать разными
инструментами — это снижает switching cost【turn0search5】.

**Но**: переносимость важна только если:
- есть реальный риск смены стека/инструмента;
- Gherkin-файлы — единственный носитель поведения.

Если поведение зафиксировано в **спецификации** (EARS/Markdown), а Gherkin —
только исполняемая проекция, то смена инструмента = перегенерация step
definitions, не переписывание спек.

**Нужен ли инструмент per-стек?**

Нет. Пользователь прав: **Gauge** — мультиязычный framework, использующий
Markdown (не Gherkin) для спецификаций и language runners для исполнения
кода【turn2search6】【turn2search9】:

| Runner | Язык |
|---|---|
| Java | Java |
| JS/TS | JavaScript/TypeScript |
| Python | Python |
| .NET | C#/F# |
| Ruby | Ruby |

Один инструмент, один формат спек (Markdown), разные language runners.
**Markdown-спеки Gauge лучше для AI-агентов**, чем Gherkin — агенты уже
обучены на Markdown, и формат спек совпадает с остальной документацией.

### Варианты

| Вариант | Плюсы | Минусы |
|---|---|---|
| **A: Gauge как primary** | Единый инструмент для всех стеков; Markdown-спеки (AI-friendly); language runners | Меньше сообщество, чем Cucumber; Gherkin-экосистема (step libraries) недоступна |
| **B: Cucumber-family per-стек** | Зрелая экосистема; Gherkin-переносимость между Cucumber/Reqnroll/Behave | Разные инструменты для разных стеков; Gherkin — ещё один формат для агентов |
| **C: Смешанный** | Gauge для acceptance specs (Markdown), Cucumber для legacy | Две системы, cognitive overhead |

### Рекомендация

**Вариант A: Gauge как primary**, с оговоркой:

- Gauge Markdown-спеки хранятся в `tests/specs/` и являются частью
  документации (AI-агенты читают их как обычный Markdown).
- Gherkin — **опциональный** формат экспорта для integration со сторонними
  инструментами (если понадобится).
- Для API-тестов дополнительно: **Karate** (Gherkin-подобный DSL,
  self-contained, не требует step definitions)【turn1search19】.

**Решение не окончательное** — pilot на реальном проекте до commit.

---

## 2. Формат PRD-шаблона

### Постановка

Atlassian-стиль vs Amazon PR/FAQ vs Job-Story-микс. Пользователь предлагает:
**использовать готовое из фреймворков, своё только при необходимости.
Нельзя принять решение, не попробовав**.

### Анализ

Пользователь прав — **преждевременная оптимизация** выбирать PRD-шаблон до
выбора SDD-фреймворка. Оба leading-инструмента (Spec Kit, OpenSpec)
уже включают PRD-подобные артефакты:

| Фреймворк | PRD-подобный артефакт | Формат |
|---|---|---|
| **Spec Kit** | `specs/<feature>/spec.md` (constitution → specify) | Структурированный Markdown с user stories |
| **OpenSpec** | `proposal.md` + `specs/` + `design.md` | Markdown, delta-oriented |
| **BMAD** | PRD-шаблон в product-агенте | Markdown |

**Иерархия выбора:**

1. **Выбрать SDD-фреймворк** (вопрос 5) → использовать его PRD-шаблон.
2. Если шаблон не подходит (например, нужна Amazon PR/FAQ-жёсткость) —
   кастомизировать.
3. Свой шаблон — только если ни один не подходит после pilot.

### Рекомендация

**Отложить решение** до pilot SDD-фреймворка (вопрос 5). В pilot-проекте
попробовать PRD-шаблоны Spec Kit и OpenSpec на одной фиче, сравнить.

**Принцип зафиксировать**: PRD-шаблон — производная от выбранного
SDD-инструмента, не наоборот.

---

## 3. backlog.md для идей vs идеи сразу в tasks/

### Постановка

Нужен ли отдельный `backlog.md` для сырых идей, или идеи сразу оформлять
как задачи в `tasks/`?

### Анализ

**Разница между «идеей» и «задачей»:**

| Аспект | Идея | Задача |
|---|---|---|
| Зрелость | Сырая, может быть отклонена | Сформулирована, принята к работе |
| Формат | 1–3 предложения | Job Story + критерии |
| Статус | proposal / candidate | ready / in-progress / done |
| Обязательства | Нет | Есть (взяли в sprint) |

**Проблема смешения**: если идеи сразу в `tasks/`, то:
- `tasks/` захламляется отклонёнными идеями;
- AI-агент не отличает «ready to work» от «maybe someday»;
- невозможно приоритизировать параллельно (backlog grooming).

**Проблема отдельного backlog**: если `backlog.md`:
- ещё один файл для синхронизации;
- риск, что backlog живёт отдельно от кода и устаревает;
- дублирование с внешним трекером (Jira/Linear).

### Варианты

| Вариант | Плюсы | Минусы |
|---|---|---|
| **A: `docs/backlog.md` (единый файл)** | Просто; один взгляд на все идеи; AI-агент может читать как контекст | Файл растёт; merge-конфликты при параллельной работе; нет per-idea статуса |
| **B: `docs/ideas/` (директория с файлами)** | Каждая идея — файл с front-matter (статус, приоритет); масштабируемо; git-friendly | Больше файлов; нужен `_index.md` для навигации |
| **C: Идеи сразу в `tasks/` с статусом `idea`** | Нет лишней директории; одна система | `tasks/` захламляется; агент не отличает ready от idea |
| **D: Внешний трекер (Jira/Linear) + зеркало** | Богатые возможности трекинга | Vendor-lock; двойной ввод; артефакт вне git |

### Рекомендация

**Вариант B: `docs/ideas/` как директория**, с правилами:

```yaml
---
id: idea-042
status: candidate   # candidate | accepted | rejected | promoted
priority: P2
promoted_to: task-017  # если accepted → задача в tasks/
created: 2026-09-29
---
# Идея: <краткое описание>
```

- **Promotion flow**: `idea → (обсуждение) → task` — это L0→L1 переход
  из `02-process-design.md` §2.
- `docs/ideas/_index.md` — autogenerated список с фильтром по статусу.
- AI-агент читает `docs/ideas/` только с `status: accepted` для планирования.

**Почему не A (единый файл)**: не масштабируется, merge-конфликты.
**Почему не C**: захламляет `tasks/`, агент путается.
**Почему не D**: нарушает принцип P1 (git — source of truth).

---

## 4. Прототипы AGENTS.md и CONSTITUTION.md

### Постановка

Пользователь не готов предоставить, но предлагает попробовать сделать.

### Анализ

**Разделение ответственности:**

| Файл | Что содержит | Кто читает |
|---|---|---|
| **AGENTS.md** | Операционные правила: как работать с репо, что читать перед задачей, ограничения | AI-агенты (все) + новые разработчики |
| **CONSTITUTION.md** | Неизменяемые принципы проекта: ценности, красные линии | AI-агенты + все участники |

**Стандарт де-факто**: AGENTS.md — cross-tool стандарт (Codex, Cursor,
Cline, Copilot, OpenCode)【turn2search11】. CLAUDE.md — Claude-специфичный.
Для мультиагентных репозиториев — **AGENTS.md как canonical**, CLAUDE.md —
симлинк или include【turn1search15】.

### Прототипы

#### AGENTS.md (prototype)

```markdown
# AGENTS.md — Правила для AI-агентов

## Обязательный контекст (читать перед любой задачей)

1. `CONSTITUTION.md` — принципы проекта
2. Связанная спецификация: `docs/specs/<NNN-slug>/spec.md`
3. Задачи: `docs/specs/<NNN-slug>/tasks.md`
4. Релевантные ADR: `docs/adr/` (фильтр по затронутым технологиям)

## Жёсткие правила

1. **Не имплементировать без approved-спеки** (статус `approved`
   в front-matter). Исключение: `trivial`-изменения (typo, hotfix).
2. **Прочитать перед кодом**: constitution → spec → tasks → ADR.
3. **Отклонение от спеки** → стоп + вопрос человеку или RFC-предложение.
4. **Архитектурные решения** — не принимать самостоятельно. Оформить
   как draft ADR (`docs/adr/draft-*.md`) для человека.
5. **Обновить после имплементации**: tasks.md (чеклист), scenarios
   (если поведение изменилось), changelog.

## Формат артефактов

- Все документы: Markdown с YAML front-matter
- Требования: EARS-нотация
- Сценарии: Gauge Markdown (`tests/specs/`)
- Диаграммы: PlantUML (`.puml`) или Mermaid (`.mmd`)
- ID: `idea-NNN`, `task-NNN`, `prd-NNN`, `rfc-NNNN`, `adr-NNNN`, `spec-NNN`

## Директории

| Каталог | Что там |
|---|---|
| `docs/` | Вся документация (PRD, RFC, ADR, specs) |
| `docs/specs/` | Фича-спецификации |
| `docs/adr/` | Decision records (MADR) |
| `docs/ideas/` | Кандидаты-идеи (статус: candidate) |
| `tasks/` | L1-задачи (готовые к работе) |
| `tests/specs/` | Gauge Markdown-спеки |

## CI проверки (не нарушать)

- `markdownlint`: Markdown валиден
- `trace-check`: все `traces`-ссылки существуют
- `adr-lint`: ADR соответствуют MADR-формату
- `gauge`: исполняемые спецификации проходят
```

#### CONSTITUTION.md (prototype)

```markdown
# CONSTITUTION.md — Принципы проекта

> Неизменяемые правила. Изменение — только через RFC с одобрением
> всех мейнтейнеров.

## Ценности

1. **Docs-first**: документ опережает код. PR без артефакта — отклонён
   (кроме trivial).
2. **Git — source of truth**: все значимые артефакты — файлы в репо.
   Внешние системы — зеркало.
3. **Человек решает, агент исполняет**: approval-гейты у людей.
   AI-агент не принимает архитектурных решений.
4. **Открытые форматы**: Markdown/YAML/Gherkin/PlantUML. Бинарные
   форматы как единственный носитель — запрещены.

## Красные линии

1. Не пушить в `main` без ревью (даже AI-агенту).
2. Не менять `CONSTITUTION.md` без RFC.
3. Не удалять ADR — только `superseded` с ссылкой на новый.
4. Не генерировать код вне approved-спеки (кроме trivial).
5. Не коммитить секреты (использовать `.env` + `.gitignore`).

## Качество

1. Тесты обязательны для поведенческих изменений.
2. Исполняемые спецификации (Gauge) должны проходить в CI.
3. Документация обновляется в том же PR, что и код.

## Масштаб

- L0 (trivial): без артефактов, `trivial:` префикс в коммите.
- L1–L4: см. `docs/process/levels.md` (TBD).
- Уровень повышается, артефакты не выбрасываются.
```

### Статус

**Черновики для обсуждения.** Пользователь ревьюит и корректирует под
свой проект. Это стартовая точка, не финальная версия.

---

## 5. Автоматизация создания артефактов: Spec Kit vs OpenSpec

### Постановка

Пользователь: «лучше использовать готовое, своё только при необходимости.
Есть ли такая необходимость? Плюсы/минусы spec-kit и openspec?»

### Анализ: нужна ли собственная разработка?

**Нет.** Оба инструмента (Spec Kit, OpenSpec) покрывают весь lifecycle
артефактов: создание шаблонов, slash-команды для агентов, структура
директорий. Своя разработка нужна только если:

- требуется нестандартный пайплайн артефактов (например, Event Modeling-
  oriented вместо user-story);
- vendor-lock неприемлем даже для OSS-инструмента.

Ни то, ни другое не подтверждено. **Используем готовое.**

### Сравнение Spec Kit vs OpenSpec

| Аспект | GitHub Spec Kit | OpenSpec (Fission-AI) |
|---|---|---|
| **Maintainer** | GitHub | Fission AI |
| **Runtime** | Python (`uv`/`pipx`) | TypeScript (`npm`) |
| **Workflow** | Линейные фазы: constitution→specify→plan→tasks→implement | Fluid actions: explore→propose→apply→verify→archive |
| **Спецификации** | Фрагментированы: несколько файлов per feature | Unified: единый документ + delta specs |
| **Greenfield** | Excellent | Good |
| **Brownfield** | Workable (needs adaptation) | **Excellent** (delta-first) |
| **Delta specs** | Нет | **Да**: ADDED/MODIFIED/REMOVED маркеры【turn4search0】【turn4search3】 |
| **Customization** | Extensions + presets + overrides | Schemas + project config |
| **Footprint** | Тяжелее (~800 lines typical)【turn1search5】 | Легче (~250 lines typical)【turn1search5】 |
| **Guardrails** | Сильные (phase gates) | Слабые (свобода итерации) |
| **Best for** | Structured teams, 0→1, enterprise | Iterative work, brownfield, parallel changes |

**Ключевое различие**【turn3fetch0】:

- **Spec Kit**: «guided workflow, strong guardrails, big extension catalog».
  Фазы обязательны, агент не может пропустить specify перед implement.
- **OpenSpec**: «fluid actions on a DAG of artifacts». Нет жёстких фаз,
  можно итерировать свободно. **Delta specs** — killer feature для
  brownfield: описывают что меняется, не переписывая весь spec.

### Применимость к нашим процессам

| Сценарий | Лучший выбор | Почему |
|---|---|---|
| **Новый проект (L4)** | Spec Kit | Guardrails для enterprise-уровня, constitution-фаза |
| **Существующий проект + AI** | OpenSpec | Delta specs для изменений, не переписывая legacy |
| **Малый проект (L1–L2)** | OpenSpec | Легче, меньше overhead |
| **Команда с жёстким процессом** | Spec Kit | Phase gates предотвращают vibe-coding |
| **Solo + AI-агент** | OpenSpec | Быстрее iterate, меньше бюрократии |

### Рекомендация

**Не выбирать сейчас — pilot оба.**

**Пилот-план:**

1. **Неделя 1**: Одна фича L2 через **Spec Kit** (`specify init --agent claude`).
2. **Неделя 2**: Та же фича (или похожая) через **OpenSpec**
   (`npm install -g @fission-ai/openspec@latest`).
3. **Сравнить**: overhead, качество спек, опыт AI-агента, brownfield-fit.
4. **Выбрать primary** по результатам, второй — как fallback.

**Принцип**: оба MIT-licensed, оба поддерживают 30+ AI-ассистентов.
Формат артефактов (Markdown) совместим — смена инструмента не потеряет
данные【turn3fetch0】.

---

## 6. EARS: внутри spec.md vs отдельный requirements.yaml

### Постановка

Как хранить EARS-требования: внутри `spec.md` (раздел Requirements) или
отдельным `requirements.yaml` (YADR-стиль)?

### Анализ

**EARS** — текстовая нотация требований:
```
WHEN <condition>
THE SYSTEM SHALL <expected behavior>
```

**Два формата хранения:**

#### Вариант A: внутри spec.md

```markdown
# Spec: User Authentication

## Requirements (EARS)

### R1: Login
WHEN a user submits valid credentials
THE SYSTEM SHALL create an authenticated session

### R2: Invalid login
WHEN a user submits invalid credentials
THE SYSTEM SHALL display "Invalid username or password"
AND THE SYSTEM SHALL NOT create a session

## Acceptance Criteria
...
```

**Плюсы:**
- Всё в одном файле — контекст не фрагментирован.
- AI-агент читает один файл, не ищет по репо.
- Markdown-структура естественна для секций.
- Diff-читаемость: изменение требования видно в контексте спеки.

**Минусы:**
- Не machine-parseable без доп. инструментов (нужен regex-парсер EARS).
- Нет schema-валидации (опечатки в THE SYSTEM SHALL не ловятся).
- Сложно делать coverage-отчёты (какие требования покрыты тестами).

#### Вариант B: отдельный requirements.yaml

```yaml
# requirements.yaml
id: spec-012
requirements:
  - id: R1
    text: "Login with valid credentials"
    ears: |
      WHEN a user submits valid credentials
      THE SYSTEM SHALL create an authenticated session
    priority: must
    traces: [prd-017]
  - id: R2
    text: "Reject invalid credentials"
    ears: |
      WHEN a user submits invalid credentials
      THE SYSTEM SHALL display "Invalid username or password"
      AND THE SYSTEM SHALL NOT create a session
    priority: must
```

**Плюсы:**
- Machine-readable: YAML-парсер → валидация структуры.
- Schema-валидация через JSON Schema.
- Coverage-трекинг: автоматическая связь requirement → test.
- CI может проверять: все требования имеют ID, приоритет, trace.

**Минусы:**
- Фрагментация: спека в одном файле, требования в другом.
- AI-агенту нужно читать два файла (или tooling должно мержить).
- YAML менее читаем для не-технических стейкхолдеров.
- Ещё один формат для синхронизации.

#### Вариант C: гибрид

`spec.md` содержит требования в Markdown с EARS-блоками,
CI-скрипт парсит EARS-паттерны и генерирует `requirements.yaml` для
машинной обработки.

**Плюсы:**
- Человек читает spec.md (один файл).
- Машина получает requirements.yaml (auto-generated).
- Нет ручной синхронизации.

**Минусы:**
- Требуется parser (custom tooling).
- Generated file в репо или только в CI-artifacts?

### Сравнение

| Критерий | A: внутри spec.md | B: requirements.yaml | C: гибрид |
|---|---|---|---|
| Читаемость (human) | ✅ Отлично | ⚠️ Приемлемо | ✅ Отлично |
| Machine-readability | ⚠️ Regex-парсер | ✅ YAML-парсер | ✅ Генерация YAML |
| AI-agent friendly | ✅ Один файл | ⚠️ Два файла | ✅ Один файл |
| CI-валидация | ⚠️ Ограничена | ✅ Schema | ✅ Через generated |
| Coverage-tracking | ❌ Нет | ✅ Да | ✅ Да |
| Overhead | ✅ Минимальный | ⚠️ Средний | ⚠️ Нужен parser |

### Рекомендация

**Вариант A (внутри spec.md) для старта**, с планом миграции на C:

1. **Фаза 1 (теперь)**: EARS-требования внутри `spec.md` в разделе
   `## Requirements (EARS)`. Формат — markdown-совместимый, agent-friendly.
2. **Фаза 2 (когда появится потребность)**: CI-скрипт
   (`tools/ears-parser.py`) извлекает EARS-блоки из spec.md → генерирует
   `requirements.json` (machine-readable, не в репо, только CI-artifact)
   для coverage-отчётов и валидации.

**Почему не B сразу**: фрагментация противоречит принципу «один артефакт —
одна сущность». AI-агенту удобнее один файл. YAML-валидация — преждевременная
оптимизация, пока нет доказанной потребности.

**Триггер для миграции на C**: когда появится потребность в automated
requirement-to-test coverage tracking (например, для compliance-проектов).

---

## 7. Сводка рекомендаций и план экспериментов

| # | Вопрос | Рекомендация | Статус |
|---|---|---|---|
| 1 | BDD-инструмент | **Gauge** как primary (Markdown, multi-language) | Pilot на L2-фиче |
| 2 | PRD-шаблон | **Отложено** до выбора SDD-фреймворка | Зависит от №5 |
| 3 | Ideas storage | **`docs/ideas/`** директория с front-matter | Принято (условное) |
| 4 | AGENTS.md / CONSTITUTION.md | **Черновики** в §4 — на ревью пользователя | Draft |
| 5 | SDD-фреймворк | **Pilot оба** (Spec Kit + OpenSpec) на 2 недели | Pilot |
| 6 | EARS storage | **Внутри spec.md** (вариант A) | Принято (условно) |

### План экспериментов (2 недели)

```
Неделя 1:
├── Day 1-2: Pilot Spec Kit
│   ├── specify init --agent claude
│   ├── /speckit.constitution (использовать prototype из §4)
│   ├── /speckit.specify для фичи L2
│   └── /speckit.plan + /speckit.tasks
├── Day 3-5: Имплементация через /speckit.implement
│   ├── AI-агент работает по спеке
│   └── Человек ревьюит PR
└── Day 5: Retrospective Spec Kit

Неделя 2:
├── Day 1-2: Pilot OpenSpec
│   ├── npm install -g @fission-ai/openspec@latest
│   ├── /opsx:explore для той же (или похожей) фичи
│   └── /opsx:propose → specs/ + design.md + tasks.md
├── Day 3-5: /opsx:apply → имплементация
│   ├── Delta specs для brownfield-изменений
│   └── /opsx:verify
└── Day 5: Retrospective OpenSpec + сравнение
```

**Критерии сравнения:**

1. **Overhead**: минуты на документацию per-фича.
2. **Качество спек**: полнота, ясность, AI-парсируемость.
3. **Опыт агента**: сколько итераций до корректного кода.
4. **Human experience**: удобство ревью, понятность артефактов.
5. **Brownfield-fit**: как работает на существующем коде.

### Решения, которые можно принять сейчас

- **№3 (ideas/)**: да, `docs/ideas/` директория — low-risk, можно менять.
- **№6 (EARS в spec.md)**: да, вариант A — формат не критичен, миграция
  возможна потом.

### Решения, которые требуют pilot

- **№1 (Gauge)**: попробовать на pilot-фиче, оценить Markdown-спеки vs
  Gherkin.
- **№5 (Spec Kit vs OpenSpec)**: pilot оба, сравнить.
- **№2 (PRD)**: автоматически решится с №5.

### Решения, которые требуют пользовательского ревью

- **№4 (AGENTS.md / CONSTITUTION.md)**: черновики в §4 — пользователь
  корректирует под свой контекст.
