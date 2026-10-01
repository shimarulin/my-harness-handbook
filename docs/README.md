---
id: readme-docs-20261001
type: process-doc
status: draft
created: 2026-10-01
updated: 2026-10-01
topics: [docs, readme, workspace]
author: agent:omp
---

# docs/ — рабочее пространство

Этот каталог — **слой 2** документации: производство контента для `content/`. Здесь ведутся исследования, пишутся черновики, фиксируются планы и заметки. Читательский продукт — в `content/`; описание процессов — в `tools/process-framework/`.

## Быстрый старт

| Я хочу… | Куда идти |
|---|---|
| Понять, что это за проект | `docs/ABOUT.md` |
| Узнать текущий статус | `docs/STATUS.md` |
| Начать исследование | `docs/research/notes/YYYY-MM-DD-<slug>/` (см. шаблон ниже) |
| Записать быструю заметку | `docs/notes/_objects/NOTE-<YYYYMMDD>-<HHMMSSfff>-<slug>.md` |
| Создать план | `docs/plans/_objects/PLAN-<YYYYMMDD>-<HHMMSSfff>-<slug>.md` |
| Написать черновик главы | `docs/drafts/handbook/` |
| Посмотреть правила для агента | `AGENTS.md` (корень) |
| Посмотреть конвенции | `tools/process-framework/conventions/` |

## Структура

```
docs/
├── README.md              # этот файл
├── ABOUT.md               # что делаем, для кого, форма, статус, открытые вопросы
├── STATUS.md              # журнал состояния корпуса (исторический, до миграции)
│
├── research/              # исследования (research как первая фаза разработки)
│   ├── inbox/             #   вход: внешние источники, неразобранное
│   │   ├── about/         #     материалы о структуре книги (14 файлов)
│   │   ├── agents-md/     #     материалы для AGENTS.md
│   │   ├── documentation-process/      # v1: референс-справочники
│   │   ├── documentation-process-v2/   # v2: процессы
│   │   ├── documentation-process-v3/   # v3: уровни L0–L4
│   │   ├── documentation-process-criticism/  # критика SDD
│   │   ├── markdown-and-text-linting/  # линтинг markdown
│   │   ├── research-and-notes/         # research-процессы (E)
│   │   └── superpovers/                # Superpowers критика
│   └── notes/             #   активные исследования: YYYY-MM-DD-<slug>/
│
├── drafts/                # черновики контента до промоушена
│   └── handbook/          #   черновики глав handbook'а
│
├── plans/                 # планы работ
│   └── _objects/          #   неперемещаемые объекты (source of truth)
│       ├── PLAN-000000__kb-guide-ideas.md      # исторический
│       └── PLAN-20261001-164751701-repository-structure.md
│
├── notes/                 # быстрые заметки, идеи, сомнения
│   └── _objects/          #   неперемещаемые объекты
│       ├── README.md      #     описание кластеров идей
│       ├── agent-governance/
│       ├── enforcement/
│       ├── knowledge-architecture/
│       ├── process-core/
│       └── tooling-strategy/
│
├── views/                 # навигация: by-status/, by-topic/ (симлинки, пока пусто)
│
└── adr/                   # решения о процессе (MADR, пока пусто)
```

## Правила

### 1. Research — первая фаза

Перед любым нетривиальным решением (выбор инструмента, написание главы, изменение процесса):

```bash
mkdir docs/research/notes/YYYY-MM-DD-<slug>/
# создать: question.md, findings/, comparison.md, decision.md
```

Шаблон: `tools/process-framework/templates/research-note.md` (когда будет).

### 2. Идентификаторы

Все новые объекты: `TYPE-<YYYYMMDD>-<HHMMSSfff>-<slug>.md` (UTC, миллисекунды).

- Проверка коллизии: файл существует → ждём следующую миллисекунду.
- Имя не меняется после создания.

### 3. Frontmatter обязателен

См. `tools/process-framework/conventions/frontmatter.md`. Минимум:

```yaml
---
id: <type>-<YYYYMMDD>-<HHMMSSfff>
type: <type>
status: draft | active | review | final | archived
created: YYYY-MM-DD
updated: YYYY-MM-DD
topics: [<topic1>]
author: human:<name> | agent:<name>
---
```

### 4. Неперемещаемые объекты

`_objects/` — реальные файлы, не перемещаются. Статус меняется в frontmatter. Навигация — через `views/` (симлинки, материализация frontmatter).

### 5. Промоушен в `content/`

Переписывание, не перемещение. `docs/` остаётся как сырьё с атрибуцией; `content/` — чистый продукт.

## Текущий статус (2026-10-01)

- ✅ Структура репозитория принята (PLAN-20261001-164751701).
- ✅ Миграция завершена: `content/kb/`, `content/guide/`, `docs/notes/`, `docs/research/inbox/`.
- 🔄 `docs/STATUS.md` — исторический журнал (фазы 0–8 старого плана); новый формат — в работе.
- ⏳ `docs/views/` — пусто; появится после tooling.
- ⏳ `docs/adr/` — пусто; первые ADR — по мере решений.
- ⏳ `docs/research/notes/` — пусто; первое исследование — структура handbook'а.

## Источники

- План структуры: `docs/plans/_objects/PLAN-20261001-164751701-repository-structure.md`
- Конвенции: `tools/process-framework/conventions/`
- AGENTS.md: `AGENTS.md`
- ABOUT.md: `docs/ABOUT.md`
