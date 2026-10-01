---
id: decision-final-20261002
type: research-note
status: final
created: 2026-10-02
updated: 2026-10-02
topics: [decision, toolchain, mise, process-framework, adopt-adapt-build]
author: agent:omp
---

# Decision: итоговая рекомендация для текущего репозитория

## Контекст

Три research-итерации (веб → клонирование specs.md/spec-kitty → механика процессов + pi/omp) дали достаточно оснований для финального решения. Дополнительное требование пользователя: в проекте должен быть механизм установки среды исполнения для скриптовых языков и инструментов — кандидат **mise** (уже установлен: 2026.4.18).

## Рекомендация

### 1. Среда исполнения: adopt mise

`.mise.toml` в корне — единая точка входа для рантаймов и инструментов:

```toml
[tools]
node = "24"          # tooling (TypeScript CLI, markdownlint-cli2)
python = "3.13"      # если появится need (spec-kitty CLI)

[env]
NODE_ENV = "development"

[tasks.lint]
description = "Lint markdown корпуса"
run = "npx markdownlint-cli2 \"**/*.md\""

[tasks.verify-links]
description = "Проверка битых ссылок и симлинков (будущее)"
run = "node tools/process-framework/scripts/verify.mjs"
```

Почему mise, а не альтернативы:
- **Один файл** декларирует и рантаймы, и задачи — агенту достаточно прочитать `.mise.toml`, чтобы понять, как запустить проект (`mise tasks`).
- **Tasks с описаниями** — двойной режим: человек читает `mise tasks`, агент читает тот же список и вызывает `mise run <task>`. Это наш dual-mode принцип без написания CLI.
- **Инструменты как зависимости проекта** (`[tools]`), не глобальные: node/python/специфичные версии фиксируются в репо, `mise install` воспроизводит среду. Fresh checkout → `mise install` → всё работает.
- 2026: наследование задач/инструментов из родительских конфигов — монорепо-режим на будущее.
- Не привносит vendor-lock: `.mise.toml` — декларация, задачи — обычные shell-команды; выход на asdf-экосистему или ручные скрипты тривиален.

### 2. Процессный слой: наша `tools/process-framework/`, без рантайма SDD-инструментов

Подтверждение вывода первой итерации после изучения механики (вторая-третья итерации):

- **spec-kitty решает чужую задачу**: его ценность — state machine с машинными переходами, WP-механика, worktree-изоляция, review-циклы для *кодовых* миссий с параллельными агентами. Наш репозиторий — knowledge corpus (текст, не код): миссий software-dev нет, параллельных WP-агентов нет. Cost (4 root-директории: `.kittify/`, `kitty-specs/`, `.worktrees/`, `.agents/`) без соответствующей ценности.
- **«Блокирующие gates» слабее, чем звучат** (mechanics.md §B): это отказ state machine выдать следующий шаг, не прерывание LLM-цикла; работает в связке с его же event-движком. Для нас (без их runtime) паттерн деградирует до «CI-проверка», которую мы реализуем напрямую.
- **Автоопределение следующего шага** (route/next) — паттерн, а не инструмент: у нас его играет `docs/STATUS.md` + `docs/plans/` + AGENTS.md-протокол «начало сессии: прочитать ABOUT → STATUS → планы».

**Что берём из исследования в наш process-framework (adopt артефактов, не рантаймов):**
- `evidence-log.csv` / `source-register.csv` схемы (spec-kitty) → шаблоны для `docs/research/notes/`.
- Research type taxonomy (Literature Review | Empirical | Case Study | Meta-Analysis) → поле frontmatter.
- Принцип «floor ≠ target» и «events, not file rows» → в конвенцию research-процесса: валидация по журналам событий/коммитам, не по наличию файлов.
- Command-as-thin-activator паттерн (specs.md) → если заведём slash-команды для pi/omp: команда = 30 строк маршрутизации, методология в SKILL.md.

### 3. Tooling репозитория: минимальный набор через mise tasks

| Потребность | Инструмент | Статус |
|---|---|---|
| Линтинг markdown | `markdownlint-cli2` (53 правила, --fix, GFM) + при нужде Vale (проза/терминология) | Research есть: `docs/research/inbox/markdown-and-text-linting/` (6 файлов) — синтезировать в kb-статью при внедрении |
| Проверка frontmatter | свой verify-скрипт (TypeScript/Node из mise) | Stage 2; сначала ручная конвенция |
| Симлинки views/ | sync/verify в том же скрипте | Stage 2 |
| SDD-процессы для будущих кодовых проектов | spec-kitty (`--ai pi`) | **Применять в целевых кодовых репозиториях**, не здесь; план адаптации — question.md §Decision той же заметки |

### 4. Поддержка pi/omp в этом репозитории

Уже обеспечена нативно: корневой `AGENTS.md` читают оба (pi: resource-loader walk-up; omp: провайдер agents-md). Дополнительно ничего не нужно. Если захотим наши процессы как команды: `.omp/commands/*.md` + `.pi/prompts/` (вариант 1 из mechanics.md §D) — mise task для синхронизации копий.

## Итоговая структура обязанностей

```
mise                 → среда (node/python версии) + задачи (lint, verify, build)
tools/process-framework/ → процесс (конвенции, шаблоны) — свой, развиваемый
docs/                → рабочие артефакты (research, plans, notes) — свой формат
content/             → продукт — свой формат
spec-kitty           → НЕ здесь; в будущих кодовых репозиториях
```

## Следующие шаги

1. `.mise.toml`: node 24 + задача lint (markdownlint-cli2) — первый коммит.
2. Синтез research по линтингу → kb-статья + конфиг `.markdownlint-cli2.jsonc` с учётом нашего frontmatter (MD041 off и т.п.).
3. AGENTS.md: секция «Commands» со ссылкой на `mise tasks` как канонический способ запуска.
4. Шаблоны research-note + CSV в `tools/process-framework/templates/` (из decision первой итерации).

## Источники

- Первая итерация: `../2026-10-02-sdd-tools-artifacts/` (артефакты, GAP, adopt CSV-схем).
- Вторая-третья итерации: `question.md` + `findings/mechanics.md` этой заметки (механика процессов, gates, команды pi/omp).
- mise: https://mise.jdx.dev (configuration, tasks; локальная версия 2026.4.18).
- Линтинг: `docs/research/inbox/markdown-and-text-linting/` (markdownlint-cli2, Vale, rumdl).
