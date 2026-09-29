# Пример L2: Фича

| Параметр | Значение |
|---|---|
| Уровень | L2 — Feature |
| Сценарий | Добавить экспорт данных в CSV |
| Артефактов | 3 (PRD, spec, tasks) |
| AI-агент | 2-3 sessions |
| Время | ~3 часа документация |

## Сценарий

Product team хочет добавить возможность экспорта пользовательских данных в CSV.
Это новая фича, требующая UI, API endpoint, и data processing logic.

## Пайплайн

```
[Idea] → [PRD] → [Spec with EARS] → [Tasks] → [AI implements in 2-3 sessions] → [PR] → [Review]
  5 min    45 min     60 min          30 min     90 min                          15 min    30 min
```

## Что демонстрирует

1. **PRD** с user stories и success metrics
2. **EARS-нотация** для системных требований
3. **Task breakdown** для multi-session AI work
4. **Approval gates** — spec review перед implementation

## Файлы

- [`prd-005.md`](prd-005.md) — Product Requirements Document
- [`spec-012/spec.md`](spec-012/spec.md) — Specification с EARS requirements
- [`spec-012/tasks.md`](spec-012/tasks.md) — Implementation tasks
- [`PR_DESCRIPTION.md`](PR_DESCRIPTION.md) — PR description

## Сравнение артефактов

| Артефакт | Отвечает на | Кто пишет | Кто ревьюит |
|---|---|---|---|
| PRD | What & Why | Product/PM + AI draft | PM + Engineering lead |
| Spec | What exactly (behavior) | Engineer + AI | Engineering team |
| Tasks | How (implementation order) | AI + Engineer | Engineer (self-review) |
