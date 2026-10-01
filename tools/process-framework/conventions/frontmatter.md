---
id: convention-frontmatter-20261001
type: process-doc
status: draft
created: 2026-10-01
updated: 2026-10-01
topics: [conventions, frontmatter, metadata]
author: agent:omp
---

# Конвенция: frontmatter

## Обязательность

Frontmatter обязателен во **всех** markdown-файлах всех слоёв (`content/`, `docs/`, `tools/`). Без frontmatter файл не считается частью корпуса.

## Схема

```yaml
---
id: <type>-<YYYYMMDD>-<HHMMSSfff>   # уникальный, неизменный; UTC с миллисекундами
type: <type>                          # см. таксономию ниже
status: <status>                      # см. таксономию ниже
created: YYYY-MM-DD                   # дата создания (UTC)
updated: YYYY-MM-DD                   # дата последнего изменения (UTC)
topics: [<topic1>, <topic2>]          # для навигации views/by-topic/
author: human:<name> | agent:<name>   # автор
---
```

## Таксономия `type`

| Значение | Слой | Описание |
|---|---|---|
| `kb-article` | `content/kb/` | Статья базы знаний |
| `handbook-chapter` | `content/handbook/` | Глава handbook'а |
| `guide-chapter` | `content/guide/` | Глава guide |
| `research-note` | `docs/research/notes/` | Активное исследование |
| `plan` | `docs/plans/_objects/` | План работы |
| `note` | `docs/notes/_objects/` | Быстрая заметка, идея, сомнение |
| `draft` | `docs/drafts/` | Черновик контента |
| `adr` | `docs/adr/`, `tools/process-framework/adr/` | Architecture Decision Record |
| `process-doc` | `tools/process-framework/` | Описание процесса, конвенция |

## Таксономия `status`

| Значение | Описание | Когда |
|---|---|---|
| `draft` | Черновик, не вычитан | Начальное состояние |
| `active` | Активная работа | Research, план в работе |
| `review` | На проверке | Ожидает ревью человеком |
| `final` | Завершено, вычитано | Готово для читателя |
| `archived` | Устарело, сохранено для истории | Заменено, отменено |

## Правила

1. **`id` неизменен.** Присваивается один раз при создании; никогда не меняется, даже при переименовании файла.
2. **`created` неизменен.** Дата создания в UTC; не обновляется при правках.
3. **`updated` обновляется.** При каждом коммите, затрагивающем файл.
4. **`topics` — массив.** Даже для одной темы: `topics: [research]`. Используется для `views/by-topic/`.
5. **`author` — префикс.** `human:` или `agent:` — обязательно; имя — идентификатор (не email).
6. **Дополнительные поля.** Разрешены, но должны быть задокументированы в конвенции типа (например, `freshness_notes` для `kb-article`).

## Примеры

### План

```yaml
---
id: plan-20261001-164751701
type: plan
status: final
created: 2026-10-01
updated: 2026-10-01
topics: [repository-structure, docs-layers, process]
author: agent:omp
---
```

### Research-заметка

```yaml
---
id: research-note-20261001-143000123
type: research-note
status: active
created: 2026-10-01
updated: 2026-10-01
topics: [orm, python, async]
author: agent:scout
---
```

### KB-статья (после миграции)

```yaml
---
id: kb-article-20260930-120000000
type: kb-article
status: final
created: 2026-09-30
updated: 2026-10-01
topics: [adr, architecture, decisions]
author: agent:omp
freshness_notes: "По состоянию на 2026-09-30; ADR-ландшафт стабилен"
---
```

## Валидация

Будущая проверка в CI (не реализовано):
- Наличие всех обязательных полей.
- Соответствие `id` формату `<type>-<YYYYMMDD>-<HHMMSSfff>`.
- Соответствие `type` и `status` таксономии.
- `updated` ≥ `created`.

## Источники

- План: `docs/plans/_objects/PLAN-20261001-164751701-repository-structure.md`
- AGENTS.md: `AGENTS.md`
