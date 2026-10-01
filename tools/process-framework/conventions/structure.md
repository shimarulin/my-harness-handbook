---
id: convention-structure-20261001
type: process-doc
status: draft
created: 2026-10-01
updated: 2026-10-01
topics: [conventions, structure, repository]
author: agent:omp
---

# Конвенция: структура репозитория

## Три слоя документации

| Слой | Каталог | Назначение | Изменчивость |
|---|---|---|---|
| **1. Контент** | `content/` | Продукт для читателя: handbook, kb, guide | Низкая-средняя |
| **2. Рабочее пространство** | `docs/` | Производство контента: research, drafts, plans, notes | Высокая |
| **3. Фреймворк процессов** | `tools/process-framework/` | Описание процессов как таковых: конвенции, шаблоны, примеры | Средняя |

Граница слоёв 2 и 3: `docs/` — процессные файлы **для конкретного репозитория**; `tools/process-framework/` — описание процессов **в общем** (переносимо между репозиториями).

## Полная раскладка

```
repo/
├── README.md / README.ru.md   # вход: что это, ссылка на docs/ABOUT.md
├── AGENTS.md                  # правила для AI-агентов (durable context)
│
├── content/                   # СЛОЙ 1: контент для читателя
│   ├── handbook/              #   основной артефакт (главы; форма открыта)
│   ├── kb/                    #   база знаний: methods/, landscape/, principles/
│   └── guide/                 #   нарративное руководство (10 глав)
│
├── docs/                      # СЛОЙ 2: рабочее пространство репозитория
│   ├── README.md              #   вход в рабочее пространство
│   ├── ABOUT.md               #   что делаем, для кого, форма, статус, открытые вопросы
│   ├── research/              #   исследования (research как первая фаза разработки)
│   │   ├── inbox/             #     вход: внешние источники, неразобранное
│   │   └── notes/             #     активные исследования: YYYY-MM-DD-<slug>/
│   ├── drafts/                #   черновики контента до промоушена
│   │   └── handbook/          #     черновики глав handbook'а
│   ├── plans/                 #   планы работ
│   │   └── _objects/          #     неперемещаемые объекты (source of truth)
│   ├── notes/                 #   быстрые заметки, идеи, сомнения
│   │   └── _objects/          #     неперемещаемые объекты (source of truth)
│   ├── views/                 #   навигация: by-status/, by-topic/ (симлинки)
│   ├── adr/                   #   решения о процессе (MADR, проектные)
│   ├── STATUS.md              #   журнал состояния корпуса
│   └── learnings.md           #   накопленные уроки (cross-research)
│
└── tools/
    └── process-framework/     # СЛОЙ 3: описание процессов, примеры, конвенции
        ├── README.md          #   вход: как устроен фреймворк процессов
        ├── conventions/       #   конвенции: frontmatter, naming, structure
        ├── templates/         #   шаблоны: research-note, chapter, plan, adr
        ├── examples/          #   примеры заполненных артефактов
        └── adr/               #   решения о фреймворке процессов (общие)
```

## Правила размещения

| Тип объекта | Куда | Почему |
|---|---|---|
| Готовая статья KB | `content/kb/<category>/` | Читательский контент |
| Черновик главы | `docs/drafts/handbook/` | Ещё не готово для читателя |
| Активное исследование | `docs/research/notes/YYYY-MM-DD-<slug>/` | Рабочий процесс |
| План работы | `docs/plans/_objects/PLAN-<YYYYMMDD>-<HHMMSSfff>-<slug>.md` | Неперемещаемый объект |
| Быстрая заметка | `docs/notes/_objects/NOTE-<YYYYMMDD>-<HHMMSSfff>-<slug>.md` | Неперемещаемый объект |
| Решение о процессе (проект) | `docs/adr/ADR-<NNNN>-<slug>.md` | Конкретное для репозитория |
| Решение о фреймворке | `tools/process-framework/adr/ADR-<NNNN>-<slug>.md` | Общее, переносимое |
| Конвенция | `tools/process-framework/conventions/<name>.md` | Общее правило |
| Шаблон | `tools/process-framework/templates/<name>.md` | Переиспользуемая форма |
| Пример | `tools/process-framework/examples/<name>.md` | Эталон для подражания |

## Принципы

1. **Research — первая фаза.** Перед выбором инструмента, написанием главы, изменением процесса — `docs/research/notes/`.
2. **Поглощение, не перемещение.** `content/` переписывается по `docs/`; `docs/` остаётся как сырьё.
3. **Контент стабилен, структура виртуальна.** `_objects/` не перемещаются; навигация через `views/` (симлинки).
4. **Предсказуемая структура важнее графа.** Путь к информации вычислим из соглашения.

## Источники

- План: `docs/plans/_objects/PLAN-20261001-164751701-repository-structure.md`
- Принципы: `content/kb/principles/content-stays-virtual-structure.md` (после миграции)
- Research knowledge: `content/kb/methods/research-knowledge.md` (после миграции)
