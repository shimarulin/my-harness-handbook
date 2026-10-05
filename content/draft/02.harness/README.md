# Harness для агентной разработки ПО

Единый раздел, объединяющий исследование мультиагентных harness для
разработки ПО: от формулировки проблемы через анализ архитектурных
паттернов и ландшафта инструментов к выбору стека и практическим
рекомендациям.

## Контекст

Harness — это операционный слой вокруг языковых моделей, который
превращает их из генераторов текста в агентов, способных выполнять
инженерные задачи: читать код, искать по проекту, вносить правки,
запускать тесты. Проект начался с простого вопроса («какой фреймворк
взять для цепочки агентов?») и эволюционировал через серию
архитектурных итераций в целостную картину экосистемы coding-агентов
2026 года.

## Структура раздела

Документы ведут читателя от проблематики к решениям. Порядок чтения
рекомендуется последовательный, но каждый документ самодостаточен.

| # | Документ | О чём | Статус |
|---|---|---|---|
| 01 | [Проблема и требования](01.problem-and-requirements.md) | Что мы строим, для кого, с какими ограничениями и критериями успеха | черновик |
| 02 | [Принципы проектирования](02.design-principles.md) | Детерминизм vs гибкость, cost optimization, слабые модели | черновик |
| 03 | [Архитектурные паттерны](03.architecture-patterns.md) | Producer-Verifier, Planner-Executor, Blackboard, Category Routing, Hierarchical Delegation | черновик |
| 04 | [Ландшафт инструментов](04.framework-overview.md) | Обзор всех рассмотренных решений с ключевыми характеристиками | черновик |
| 05 | [Mastra](05.mastra.md) | Детальный анализ: workflows, Zod, Studio, observability | черновик |
| 06 | [Экосистема Pi](06.pi-ecosystem.md) | Pi, pi-subagents, pi-fabric, pi-web, pi-acp, senpi, omp | черновик |
| 07 | [OmO Native и senpi](07.omo-native.md) | oh-my-openagent, senpi engine, curated агенты, memory | черновик |
| 08 | [Oh My Pi (omp)](08.oh-my-pi.md) | Rust core, debuggers, persistent workers, LSP, worktree isolation | черновик |
| 09 | [Herdr](09.herdr.md) | Terminal multiplexer, agent monitoring, multi-machine federation | черновик |
| 10 | [Маршрутизация моделей](10.model-routing.md) | Per-step routing, fallback chains, cost optimization | черновик |
| 11 | [Интерфейсы](11.interfaces.md) | TUI, Web UI, ACP — три поверхности одного harness | черновик |
| 12 | [Отказоустойчивость](12.fault-tolerance.md) | Snapshots, suspend/resume, persistence, переживание сбоев | черновик |
| 13 | [Сравнение решений](13.comparison.md) | Матрица по 8 критериям, общий рейтинг | черновик |
| 14 | [Руководство по выбору](14.selection-guide.md) | Decision tree, сценарии, anti-patterns | черновик |
| 15 | [Паттерны интеграции](15.integration-patterns.md) | Оркестратор+исполнитель, координатор+агенты, слои | черновик |
| 16 | [Наше решение](16.our-solution.md) | Рекомендуемый стек: omp + Herdr + Mastra | черновик |
| 17 | [Ссылки](17.references.md) | Первоисточники, документация, GitHub | черновик |

## Ключевые решения (summary)

| Решение | Выбор | Обоснование |
|---|---|---|
| Основной runtime | **oh-my-pi (omp)** | Rust core, 31+ инструментов (на дату среза), workflowz, ACP built-in, memory, debuggers |
| Observability | **Mastra Studio** | Traces, cost tracking, time-travel — то, чего нет в omp |
| Persistence / multi-machine | **Herdr** | Terminal multiplexer, machine federation, state tracking |
| Сложные pipelines | **Mastra workflows** | Zod schemas, suspend/resume, явные графы |
| Model routing | **omp model roles + OmO categories** | Per-role, fallback chains, cost optimization |
| Memory | **omp built-in** | retain/recall/learn, pluggable backends |
| Альтернатива ванильного стека | **Mastra Code** | Observational memory, TUI, единый вендор |

## Как читать

- Если вы **новичок** в теме — читайте по порядку от 01.
- Если ищете **конкретное сравнение** — начните с 13 (comparison) или 14 (selection guide).
- Если хотите **быстро начать** — переходите к 16 (our solution).
- Если нужны **теоретические основы** — 02 (принципы) и 03 (паттерны).

## Статус раздела

**В работе.** Ландшафт coding-агентов меняется быстро (еженедельные
мажорные релизы omp, OmO, Mastra). Перед принятием архитектурных
решений сверяйтесь с первоисточниками — ссылки в [17.references.md](17.references.md).

## Связанные разделы

- [01.sandbox/](../01.sandbox/README.md) — песочница для безопасного
  выполнения кода агентами.
