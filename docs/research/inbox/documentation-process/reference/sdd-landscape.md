# Spec-Driven Development: ландшафт инструментов

## Обзор

**Spec-Driven Development (SDD)** — методология, где спецификации и документация являются source of truth, а код — производная. Вместо промптинга агента описанием и получения кода, вы сначала создаёте письменные артефакты — спецификацию, технический план, разбиение на задачи — и ревьюите каждый перед следующим шагом【turn5fetch0】.

## Сравнительная таблица

| Инструмент | Разработчик | GitHub Stars | Подход | Agent-agnostic |
|---|---|---|---|---|
| **GitHub Spec Kit** | GitHub | 137k+ | Slash commands, 4 фазы | Да: 38 интеграций + generic |
| **Kiro** | AWS | — | IDE/CLI, 3 фазы (Req/Design/Tasks), EARS | Ограничен Kiro ecosystem |
| **BMAD-METHOD** | BMad Code | 53.5k | 12+ специализированных AI-агентов | Да: через skills |
| **OpenSpec** | Fission-AI | 68k | Lightweight, /opsx команды, без phase gates | Да: 30+ AI assistants |
| **ForgeSDLC** | Forge | — | Event-driven workflow, Jira→PR | Да: через model factory |

---

## 1. GitHub Spec Kit

**Официальный сайт:** https://github.com/github/spec-kit

### Архитектура

Spec Kit работает внутри существующего агента — Claude Code, Copilot, и несколько десятков других — через набор slash команд【turn5fetch0】:

```
/speckit.constitution   → project principles the agent must respect
/speckit.specify        → what you're building: user stories, acceptance criteria
/speckit.plan           → how: architecture, data model, contracts
/speckit.tasks          → an ordered, reviewable task breakdown
/speckit.implement      → the agent executes the tasks
```

Каждая фаза пишет markdown файлы в `specs/` директорию в репозитории【turn5fetch0】.

### Поддержка агентов

- **38 интеграций** из коробки: Copilot, Gemini, Codex, Kilo Code, Zed, Claude, Forge, Kiro【turn0search4】
- **Generic integration** как escape hatch для любого инструмента: «If your agent isn't listed, the `generic` integration is an escape hatch for any tool»【turn1search0】
- **157 community extensions** (90+ авторов), 33 presets【turn0search4】
- Switch между агентами одной командой【turn0search4】

### Установка

```bash
specify init --agent claude   # или copilot, gemini, и т.д.
```

### Документация

- GitHub: https://github.com/github/spec-kit【turn3fetch0】
- Docs: https://github.github.com/spec-kit【turn1search0】

---

## 2. Kiro (AWS)

**Официальный сайт:** https://kiro.dev【turn4search2】

### Three-Phase Workflow

Kiro генерирует **три документа** для каждой фичи【turn5fetch0】:
1. **requirements.md** — требования в EARS-нотации
2. **design.md** — технический дизайн
3. **tasks.md** — список задач

### Workflow Variants

**Requirements-First**【turn15fetch0】:
- Start: requirements.md → design.md → Implementation
- Для: product-driven development, greenfield

**Design-First**【turn15fetch0】:
- Start: design.md → requirements.md → Implementation
- Для: technically-constrained projects

**Quick Spec**【turn15fetch0】:
- Автоматический запуск всех трёх фаз без approval gates

### EARS Notation

Kiro использует **EARS (Easy Approach to Requirements Syntax)**【turn5fetch0】【turn14fetch0】:

```
WHEN [condition/event]
THE SYSTEM SHALL [expected behavior]
```

Пример【turn14fetch0】:
```
WHEN a user submits a form with invalid data
THE SYSTEM SHALL display validation errors next to the relevant fields
```

### design.md структура

```
design.md
├── Architecture
├── Data Flow
├── Interfaces
├── Data Models
├── Error Handling
├── Unit Testing Strategy
└── ...
```

### Документация

- Feature Specs: https://kiro.dev/docs/specs/feature-specs【turn4search2】
- GitHub: https://github.com/kiro-dev

---

## 3. BMAD-METHOD

**Официальный сайт:** https://github.com/bmad-code-org/BMAD-METHOD【turn24fetch0】

### Обзор

**BMAD (Breakthrough Method for Agile Ai Driven Development)** — 53.5k GitHub stars, 6k forks【turn24fetch0】.

> «Ai Driven Development (AiDD) covers the whole effort, not only the code: what to build, how it holds together, and how it changes as you learn»【turn24fetch0】

### Ключевые принципы【turn24fetch0】

- **Right-sized process** — прямо к имплементации для простых изменений или глубокое планирование для больших инициатив
- **New or existing code** — с нуля или на существующей кодовой базе
- **Durable context** — продуктовые и технические решения сохраняются
- **Specialized perspectives** — product, architecture, UX, development, testing expertise
- **Guided collaboration** — структурированные workflow и multi-agent discussions
- **One delivery path** — от раннего мышления через reviewed implementation

### Модули【turn25fetch0】

| Module | Purpose |
|---|---|
| **BMad Method** | Plan and deliver software |
| **BMad Builder** | Skill, workflow, and agent builder |
| **BMad Creative Intelligence Suite** | Creative thinking partners |
| **BMad Test Architect** | Enterprise testing add-on |
| **BMad Loop** | Builds, verifies, and retros a whole epic unattended |
| **BMad Game Dev Studio** | Games in Unity, Unreal, Godot, Phaser |

### Установка

```bash
npx skills add bmad-code-org/BMAD-METHOD
```

Или через Claude Code plugin marketplace【turn24fetch0】:
```
/plugin marketplace add bmad-code-org/bmad-plugins
```

---

## 4. OpenSpec (Fission-AI)

**Официальный сайт:** https://openspec.dev【turn43fetch0】

### Обзор

**OpenSpec** — 68k GitHub stars, lightweight и configurable spec framework【turn43fetch0】.

> «A lightweight and configurable framework for creating and managing software specifications. With OpenSpec, you capture what you want to build in a spec and keep your team and coding agents aligned as the work evolves»【turn43fetch0】

### Ключевые особенности【turn42search0】

- **Agree before you build** — human и AI выравниваются на спецификациях до кода
- **Stay organized** — каждое изменение получает свою папку с proposal, specs, design, tasks
- **Work fluidly** — обновление любого артефакта в любое время, без жёстких phase gates
- **Use your tools** — работает с 30+ AI assistants через slash commands

### Workflow

```
/opsx:explore  → map the problem and understand the codebase
/opsx:propose  → draft proposal.md, specs/, design.md, tasks.md
/opsx:apply    → implement tasks from the specification
/opsx:verify   → check the implementation matches the spec
/opsx:archive  → archive completed changes
```

### Сравнение со Spec Kit【turn42search0】

> «vs. Spec Kit (GitHub) — Thorough but heavyweight. Rigid phase gates, lots of Markdown, Python setup. OpenSpec is lighter and lets you iterate freely»

### Совместимость

Claude Code, Codex, Cursor, GitHub Copilot, Gemini CLI, OpenCode + 33 more【turn43fetch0】

### Установка

```bash
npm install -g @fission-ai/openspec@latest
```

---

## 5. ForgeSDLC

**Официальный сайт:** https://forgesdlc.com【turn12search0】

### Обзор

> «ForgeSDLC turns ideas into governed, traceable execution from concept to production — so teams can move faster with AI agents without losing judgment, structure, or control»【turn12search0】

### Принципы【turn12search0】

- **Human-governed. Agent-executed.**
- **Refinement before execution** — shape problems, outcomes, constraints while ideas are still cheap
- **Human judgment stays accountable** — direction, risk, irreversible calls stay with people
- **Agents need structure, not just prompts** — explicit intent, boundaries, expected outputs
- **Traceability from idea to production** — decisions and artifacts stay connected

### Workflow

**Jira ticket** → **Human-gated plan** → **Repo-scoped implementation** → **GitHub PRs** → **CI repair** → **Human review** → **Summary + dashboards**【turn15fetch0】

### GitHub

https://github.com/Forge-sdlc/forge【turn13fetch0】

---

## Agent-agnostic подходы

Если нужен **другой harness, отличный от перечисленных**:

1. **GitHub Spec Kit** — используйте `generic` integration【turn1search0】
2. **OpenSpec** — работает с любым AI-ассистентом через slash commands【turn43fetch0】
3. **BMAD-METHOD** — через skills CLI【turn24fetch0】
4. **ForgeSDLC** — через model factory, любой LangChain-compatible chat model【turn15fetch0】

## Источники

- Spec Kit: https://github.com/github/spec-kit【turn3fetch0】
- Spec Kit Docs: https://github.github.com/spec-kit【turn1search0】
- Kiro: https://kiro.dev/docs/specs/feature-specs【turn4search2】
- BMAD-METHOD: https://github.com/bmad-code-org/BMAD-METHOD【turn24fetch0】
- OpenSpec: https://openspec.dev【turn43fetch0】
- OpenSpec GitHub: https://github.com/Fission-AI/OpenSpec【turn42search0】
- ForgeSDLC: https://forgesdlc.com【turn12search0】
- Forge GitHub: https://github.com/Forge-sdlc/forge【turn13fetch0】
- SDD Without the Hype: https://utsabpant.com/blog/spec-driven-development-without-the-hype【turn5fetch0】
