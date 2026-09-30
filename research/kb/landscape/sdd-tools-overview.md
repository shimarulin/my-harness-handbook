# SDD-инструменты: обзор ландшафта (Spec Kit, Kiro, BMAD, OpenSpec, ForgeSDLC)

| Параметр | Значение |
|---|---|
| Статус | draft |
| Обновлено | 2026-09-30 (данные по состоянию на ~09.2026; звёзды GitHub и экосистемы меняются быстро — перепроверять при использовании) |

## Что это

**Spec-Driven Development (SDD)** — методология, где спецификации и документация являются **source of truth**, а код — производная: сначала письменные артефакты (спецификация → план → задачи), каждый ревьюится, код генерируется против одобренных документов. Статья — карта основных инструментов SDD эпохи AI-агентов.

## Сравнительная таблица

| Инструмент | Разработчик | GitHub Stars | Подход | Agent-agnostic |
|---|---|---|---|---|
| **GitHub Spec Kit** | GitHub | 137k+ | Slash commands, 4+1 фаз | Да: 38 интеграций + generic |
| **Kiro** | AWS | — | IDE/CLI, 3 фазы (Req/Design/Tasks), EARS | Ограничен Kiro ecosystem |
| **BMAD-METHOD** | BMad Code | 53.5k (6k forks) | 12+ специализированных AI-агентов | Да: через skills |
| **OpenSpec** | Fission-AI | 126k (08.2026) | Lightweight, /opsx команды, без phase gates | Да: 30+ AI assistants |
| **ForgeSDLC** | Forge | — | Event-driven workflow, Jira→PR | Да: через model factory |

> **Обновление 09.2026 (фаза 6):** OpenSpec — 126K звёзд на 08.2026 (aicodingpatterns.com), рост с 68K. Дополняющие инструменты: **SpecWeave** (см. `spec-weave.md` — cross-tool handoff, уникально), **Spec Kitty** (см. `spec-kitty-research.md` — Research Mission, 1.7K звёзд), **specs.md** (Ideation Flow). Kiro — GA с free tier, Pro $19/мес (paperclipped.de 03.2026).

## Инструменты

### GitHub Spec Kit

Работает внутри существующего агента через slash-команды; каждая фаза пишет markdown в `specs/`:

```
/speckit.constitution → принципы проекта, обязательные для агента
/speckit.specify      → что строим: user stories, acceptance criteria
/speckit.plan         → как: архитектура, data model, контракты
/speckit.tasks        → упорядоченное ревьюируемое разбиение
/speckit.implement    → агент исполняет задачи
```

Экосистема: 38 интеграций из коробки (Copilot, Gemini, Codex, Kilo Code, Zed, Claude, Forge, Kiro); `generic` integration как escape hatch; 157 community extensions (90+ авторов), 33 presets; переключение агентов одной командой. Установка: `specify init --agent <name>`.

### Kiro (AWS)

Три документа на фичу: `requirements.md` (EARS-нотация), `design.md` (Architecture, Data Flow, Interfaces, Data Models, Error Handling, Unit Testing Strategy), `tasks.md`.

Варианты workflow: **Requirements-First** (product-driven, greenfield), **Design-First** (technically-constrained), **Quick Spec** (все фазы без approval gates — скорость ценой контроля).

EARS в Kiro: `WHEN [condition/event]` / `THE SYSTEM SHALL [expected behavior]` (см. `research/kb/methods/ears.md`).

Слабость: agent-agnostic ограничен собственной экосистемой.

### BMAD-METHOD

«Breakthrough Method for Agile Ai Driven Development»; AiDD покрывает весь цикл, не только код: «what to build, how it holds together, and how it changes as you learn».

Принципы: right-sized process (от прямой имплементации до глубокого планирования); new or existing code; durable context; specialized perspectives (product, architecture, UX, dev, testing); guided collaboration; one delivery path.

Модули: BMad Method (plan & deliver), BMad Builder (skill/workflow/agent builder), Creative Intelligence Suite, Test Architect, BMad Loop (unattended epic: build → verify → retro), Game Dev Studio (Unity, Unreal, Godot, Phaser).

Установка: `npx skills add bmad-code-org/BMAD-METHOD` или `/plugin marketplace add bmad-code-org/bmad-plugins`.

### OpenSpec (Fission-AI)

Lightweight-фреймворк: «capture what you want to build in a spec and keep your team and coding agents aligned as the work evolves».

Особенности: agree before you build; каждое изменение — своя папка (proposal, specs, design, tasks); **work fluidly** — обновление любого артефакта в любое время, без жёстких phase gates; 30+ AI assistants через slash commands.

```
/opsx:explore → карта проблемы и кодовой базы
/opsx:propose → proposal.md, specs/, design.md, tasks.md
/opsx:apply   → имплементация по задачам
/opsx:verify  → соответствие реализации спеке
/opsx:archive → архивация завершённых изменений
```

Позиционирование против Spec Kit: Spec Kit — «thorough but heavyweight» (rigid phase gates, много Markdown, Python setup); OpenSpec — легче, свободная итерация.

Установка: `npm install -g @fission-ai/openspec@latest`.

### ForgeSDLC

Governance-ориентированный: «ideas → governed, traceable execution from concept to production». Принцип: **Human-governed. Agent-executed.**

Принципы: refinement before execution (shape problems, пока идеи дёшевы); human judgment stays accountable (направление, риск, irreversible calls — у людей); agents need structure, not just prompts (explicit intent, boundaries, expected outputs); traceability from idea to production.

Workflow: Jira ticket → Human-gated plan → Repo-scoped implementation → GitHub PRs → CI repair → Human review → Summary + dashboards. Любой LangChain-compatible chat model через model factory.

## Сильные и слабые стороны (кросс-инструментальные)

- **Phase gates vs fluid**: Spec Kit — жёсткие фазы (контроль, тяжесть); OpenSpec — без гейтов (лёгкость, меньше контроля); Kiro Quick Spec — опциональный обход гейтов.
- **Привязка к экосистеме**: Kiro — AWS-only; остальные agent-agnostic (Spec Kit 38, OpenSpec 30+, BMAD через skills, ForgeSDLC через model factory).
- **Governance**: ForgeSDLC — максимум (human-gated, traceability); Spec Kit — средний (constitution + фазы); OpenSpec — минимум (align on specs, дальше свобода).
- **Масштабирование процесса**: BMAD — right-sized по размеру изменения.

## Выбор (косвенные критерии из источников)

| Нужно | Кандидат |
|---|---|
| Максимум интеграций агентов, экосистема расширений | Spec Kit |
| EARS-требования, AWS-окружение, IDE-интеграция | Kiro |
| Multi-agent роли, масштабируемый процесс, unattended epic | BMAD-METHOD |
| Лёгкий старт, свободная итерация, любой ассистент | OpenSpec |
| Governance, трассировка Jira→PR, enterprise-контроль | ForgeSDLC |

См. также критику SDD-подходов: `research/inbox/documentation-process-criticism/` (обработка — фаза 2 плана) и `research/kb/methods/rfc-vs-sdd.md`.

## Источники

- Spec Kit: https://github.com/github/spec-kit; docs: https://github.github.com/spec-kit
- Kiro: https://kiro.dev; feature specs: https://kiro.dev/docs/specs/feature-specs; GitHub: https://github.com/kiro-dev
- BMAD-METHOD: https://github.com/bmad-code-org/BMAD-METHOD
- OpenSpec: https://openspec.dev; GitHub: https://github.com/Fission-AI/OpenSpec
- ForgeSDLC: https://forgesdlc.com; GitHub: https://github.com/Forge-sdlc/forge
- SDD Without the Hype: https://utsabpant.com/blog/spec-driven-development-without-the-hype
- Входные материалы inbox: `documentation-process/reference/sdd-landscape.md`
