# Пример L1: Простая задача

| Параметр | Значение |
|---|---|
| Уровень | L1 — Small change |
| Сценарий | Bug fix: login timeout error message unclear |
| Артефактов | 1 (task.md) |
| AI-агент | 1 session |
| Время | ~15 минут документация |

## Сценарий

Пользователи сообщают, что при timeout входа отображается общее сообщение
"Something went wrong" вместо понятного "Session expired. Please login again."

## Пайплайн

```
[Observe bug] → [Create task-042.md with Job Story] → [AI implements] → [PR] → [Review + Merge]
     5 min           10 min                        15 min      5 min      10 min
```

## Что демонстрирует

1. **Job Story** формат для постановки задачи
2. **Минимальный overhead** — только один артефакт
3. **AI-агент** выполняет за одну сессию
4. **CI checks** проходят автоматически

## Файлы

- [`task-042.md`](task-042.md) — Задача с Job Story
- [`PR_DESCRIPTION.md`](PR_DESCRIPTION.md) — Описание PR для этой задачи
