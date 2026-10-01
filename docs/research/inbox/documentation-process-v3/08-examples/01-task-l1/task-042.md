---
id: task-042
type: task
status: approved
created: 2026-09-25
title: Fix unclear timeout error message on login
traces: []              # Возникла из bug report, не из idea
level: L1
tags: [bugfix, ux, login]
---

# Задача: Fix unclear timeout error message on login

## Job Story

```
When my session expires and I try to perform an action
I want to see a clear message saying my session expired
So I can understand why I need to login again instead of thinking the app is broken
```

## Критерии готовности

- [x] Заменить "Something went wrong" на "Session expired. Please login again." при timeout
- [x] Добавить кнопку "Login again" в error state
- [x] Unit test: verify error message for timeout vs other errors
- [x] E2E test: simulate session timeout, verify message
- [x] Документация не требуется (bug fix)

## Контекст

**Связанные артефакты:**
- Нет ADR — не архитектурное решение
- Не связано с существующими specs

**Технический контекст:**
- Error handling в `src/auth/errorHandler.ts`
- Timeout detection в `src/auth/sessionManager.ts`
- Текущее сообщение hardcoded в `src/constants/errors.ts`

## Implementation Notes

**Для AI-агента:**

1. Прочитать `src/auth/sessionManager.ts` — понять как определяется timeout
2. В `src/auth/errorHandler.ts` — добавить специальный case для timeout errors
3. Обновить `src/constants/errors.ts` — добавить константу `SESSION_EXPIRED_MESSAGE`
4. Добавить кнопку "Login again" в error component
5. Написать tests

**Constraints:**
- Не менять общую error handling architecture
- Не добавлять новые dependencies
- Message должен быть локализуем (использовать i18n keys)

## Заметки

- Bug report: #1234 (user @jane_doe)
- Similar issue reported 2x in last month
- Priority: P1 (affects user trust)
