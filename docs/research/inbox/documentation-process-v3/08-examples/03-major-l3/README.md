# Пример L3: Крупная фича с архитектурными решениями

| Параметр | Значение |
|---|---|
| Уровень | L3 — Major feature |
| Сценарий | Переход на event-driven architecture для уведомлений |
| Артефактов | 5+ (RFC, ADR, spec, design, tasks) |
| AI-агент | Multiple sessions |
| Время | ~1-2 дня документация |

## Сценарий

Система уведомлений перегружена: sync processing блокирует API responses
при пиках нагрузки. Нужно перейти на async event-driven architecture
с использованием message queue.

Это архитектурное решение, требующее:
- RFC для обсуждения альтернатив
- ADR для фиксации решения
- Полная спецификация новой архитектуры
- Migration plan

## Пайплайн

```
[Problem identified] → [RFC with alternatives] → [Debate] → [ADR] → [Spec] → [Design] → [Tasks] → [Implementation]
      30 min                4 hours               2 hours    1 hour   2 hours   1 hour    1 hour    Multiple days
```

## Что демонстрирует

1. **RFC процесс** — предложение с альтернативами и дебатами
2. **ADR (MADR)** — фиксация архитектурного решения с обоснованием
3. **Event-driven spec** — требования к новой архитектуре
4. **Migration plan** — как перейти от текущего состояния

## Файлы

- [`rfc-0031.md`](rfc-0031.md) — RFC с альтернативами
- [`adr-0007.md`](adr-0007.md) — Architecture Decision Record (MADR format)
- [`spec-015/spec.md`](spec-015/spec.md) — Specification для event-driven notifications
- [`spec-015/tasks.md`](spec-015/tasks.md) — Implementation tasks
- [`PR_DESCRIPTION.md`](PR_DESCRIPTION.md) — PR description

## Связь артефактов

```
rfc-0031 (RFC: Event-driven notifications)
    ↓ debated, decision made
adr-0007 (ADR: Use Kafka for event-driven notifications)
    ↓ decision documented
spec-015 (Spec: Notification system requirements)
    ↓ spec approved
tasks (Implementation breakdown)
    ↓ implementation
PR (Pull Request)
```
