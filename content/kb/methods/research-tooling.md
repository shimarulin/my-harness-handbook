# Tooling для research-процессов: язык, CLI-дизайн, кастомизация

| Параметр | Значение |
|---|---|
| Статус | draft |
| Обновлено | 2026-09-30 |

## Что это

Архитектура инструментария вокруг research-процессов (`research-knowledge.md`, `../principles/content-stays-virtual-structure.md`): выбор языка, дизайн CLI для двух потребителей (человек + AI-агент), модели распространения (внешний пакет vs vendoring vs гибрид), механизмы кастомизации. Главный тезис: **архитектура важнее языка** — «вместо вопроса "какой язык" — вопрос "какая архитектура CLI"».

## Выбор языка

Вердикт исходного исследования: Python оправдан (экосистема подтверждена: GitHub Spec Kit на Python + uv, 139k звёзд; `uvx` решает дистрибуцию; официальный MCP SDK; Textual для TUI; нет cost of migration). Для сценария «Markdown-центричный, AI-first, быстрая итерация» Python и Node.js — равнозначные кандидаты; Go/Rust избыточны (в SDD-нише редки: скорость итерации важнее бинарной дистрибуции). Примечание: в позднейшей сессии того же исследования TypeScript признан валидным и, возможно, лучшим выбором — факторы: стек команды и целевые агенты.

| Критерий | Python | Node.js/TS | Go | Rust |
|---|---|---|---|---|
| Время до прототипа | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Парсинг Markdown/YAML frontmatter | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| MCP-сервер | ⭐⭐⭐⭐⭐ (офиц. SDK) | ⭐⭐⭐⭐⭐ (офиц. SDK) | ⭐⭐⭐ | ⭐⭐ |
| Интерактивный TUI | ⭐⭐⭐⭐ (Textual) | ⭐⭐⭐ (Ink) | ⭐⭐⭐⭐⭐ (Bubble Tea) | ⭐⭐⭐⭐ (Ratatui) |
| Распространение | ⭐⭐⭐ (uv) | ⭐⭐⭐ (npm/npx) | ⭐⭐⭐⭐⭐ (бинарник) | ⭐⭐⭐⭐⭐ |
| Читаемость кода для AI | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |

Слабости Python и купирование: нет runtime → `uvx` (изолированное окружение, нужен только uv); типизация → type hints + pyright/mypy в CI; Windows → Python работает нативно («лучше, чем симлинки»).

## Ядро + интерфейсы (архитектурный принцип)

«Разделять ядро (чистые функции для работы с frontmatter, симлинками, Git) и интерфейс (CLI сейчас, TUI/MCP потом). Ядро — стабильно, интерфейсы — добавляются.» Migration path: ядро можно переписать на Go/Rust, сохранив CLI-интерфейс (те же команды и флаги) — пользователи (люди и агенты) не заметят смены языка.

### Четыре уровня интерфейсов

1. **CLI** — одинаково работает для человека и агента: `research-status.py <path> --status active --author "human:vasya"`.
2. **Dual-mode** — ключевой приём: один инструмент, два режима. Человек — интерактивный wizard; агент — всё через флаги + `--json`: `research-link.py add notes/2026-09-30-orm --topic orm --status active --json` → `{"created": ["views/by-topic/orm/orm-comparison"], "status": "ok"}`. Прецедент: uvtemplate (`uvx uvtemplate` — wizard; `--yes --data key=value` — для агента).
3. **MCP-сервер** — агент вызывает типизированный инструмент напрямую, без shell и парсинга вывода (скелет на `mcp` Python SDK: tool `research_add_topic` с input schema).
4. **TUI** (опционально, для человека) — Textual: дерево из views/.

Как Spec Kit решает «человек + агент»: CLI-интерфейс (оба вызывают одни команды через shell) + промпт-фреймворк (инструкции в `.specify/` и AGENTS.md) + шаблоны с параметризацией (`--data key=value`) + extensions. Тот же паттерн: **CLI → генерация/валидация артефактов → Markdown в Git**.

## Модели распространения

| Модель | Механика | Плюсы | Минусы | Когда достаточно |
|---|---|---|---|---|
| **Внешний tool (uvx)** | `uvx research-tools status …`; в проекте только данные | Одна версия, автообновления, чистый проект | Нельзя кастомизировать; зависимость от пакета | Все проекты следуют одному процессу |
| **Vendoring** | `research-tools init --vendor` копирует скрипты в `scripts/` | Полный контроль, ноль внешних зависимостей | Обновления вручную; дрейф между проектами | Один проект, никогда не будет второго |
| **Гибрид (рекомендуемая)** | Ядро — внешний пакет (dev-dependency); кастомизация — project-local `.research/` | Централизованные обновления ядра + кастомизация per-project | Сложнее начальной настройки | Два+ проекта, вариации процесса |

Паттерн гибрида подтверждён: Spec Kit (`.specify/` — templates копируются при init, инструмент внешний), pre-commit (`.pre-commit-config.yaml` + `repo: local`), Husky (`.husky/`), Copier (`.copier-answers.yml` + `copier update`).

## Кастомизация: `.research/` и fallback chain

```
project/
├── .research/                  # PROJECT-LOCAL кастомизация (версионируется)
│   ├── config.yaml             # настройки (deep merge поверх дефолтов)
│   ├── templates/              # переопределённые шаблоны (question.md, findings-note.md…)
│   ├── hooks/                  # точки расширения: pre-sync.py, post-add.py, pre-commit.py
│   └── extensions/             # кастомные подкоманды: team-report.py → research-tools team-report
└── research/                   # ДАННЫЕ (project-owned, всегда)
```

Четыре механизма (все с fallback chain «project-local → package default → error»):

1. **Templates lookup**: `project/.research/templates/<name>.md` → package `defaults/templates/<name>.md`. Проект переопределяет один шаблон, не трогая остальные.
2. **Config merge**: `DEFAULTS` (paths, statuses: draft/active/review/decided/archived, required_fields) + project `config.yaml` (deep merge; пример кастомизации: статус `blocked`, обязательное поле `team`).
3. **Hooks**: `.research/hooks/<name>.py` с функцией `main(**context)`; отсутствует → silent skip; может валидировать, модифицировать контекст или abort (raise). Пример: pre-sync валидация required_fields во всех README.md.
4. **Extensions**: discovery `.research/extensions/*.py` → каждый файл = подкоманда CLI.

Правила версионирования: коммитятся `research/notes/`, `research/views/` (симлинки), `.research/` целиком; игнорируется `.venv/`; `scripts/` — только если vendored.

## Путь роста (Stage 1 → 3)

1. **Stage 1 (один проект)**: скрипты в `scripts/` проекта, шаблоны в `research/templates/`. «Не усложняйте. Работает, просто, версионируется.»
2. **Stage 2 (появился второй проект)**: вынос ядра в пакет (`research_tools/` с `cli.py`, `core/` (frontmatter, symlinks, sync), `defaults/`, `hooks.py`); проекты подключают как dev-dependency + свои `.research/`.
3. **Stage 3 (нужно)**: publish + `uvx my-research-tools`.

## Источники

- Входные материалы inbox: `research-and-notes/research-process.md` (строки 1568–2229)
- Прецеденты: Spec Kit (https://github.com/github/spec-kit), uvtemplate (https://github.com/jlevy/uvtemplate), uv (https://docs.astral.sh/uv/), Textual (https://github.com/Textualize/textual), MCP Python SDK (https://github.com/modelcontextprotocol/python-sdk)
- Связанные KB: `research-knowledge.md`, `../principles/content-stays-virtual-structure.md`
