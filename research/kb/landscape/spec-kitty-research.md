# Spec Kitty Research Mission и specs.md Ideation Flow: research как фаза delivery

| Параметр | Значение |
|---|---|
| Статус | reviewed |
| Обновлено | 2026-09-30 (выжимка восстановлена полностью; Spec Kitty активно развивается — перепроверять в фазе 6) |

## Что это
Два инструмента, закрывающих research-функцию внутри SDD-доставки: **Spec Kitty** (форк Spec Kit с mission-архитектурой) имеет полноценный Research Mission — evidence-gated state machine с машинными проверками; **specs.md** покрывает pre-research brainstorming через Ideation Flow. Вывод исходного исследования после **трёх итераций пересмотра позиции**: (1) изначально утверждалось «все три инструмента — только delivery, RKM — уникальная ниша собственного проекта» (ошибочно); (2) после уточнения — specs.md покрывает research через Ideation Flow, RKM — не ниша, а фаза delivery; (3) после изучения Spec Kitty mission-system — **Spec Kitty имеет full research support и является наиболее полным инструментом для research в контексте software delivery**. Собственную research-систему строить с нуля не обязательно — варианты adopt/adapt (см. ниже), заимствуя уникальные фичи собственной архитектуры.

Тренд, подтверждённый обоими: SDD-инструменты стандартизируют не «генерацию кода», а **управление delivery-процессом** в условиях множества AI-агентов. Из mission-system.md: «A workflow designed for software development doesn't fit research: 'All tests pass' makes no sense for a literature review; 'Documented sources' isn't relevant for code implementation» — разные типы работы требуют разных workflows (missions).

## Spec Kitty: Research Mission

Позиционирование: «turns intent into reviewable specs, governs execution across the tools developers already use, and leaves an auditable delivery record from first decision to merge». Per-feature missions (0.8.0+): в одном проекте сосуществуют миссии разных типов (`software-dev`, `research`, `documentation`) — meta.json в kitty-specs/NNN-<slug>/.

### State machine и guards (evidence-gated)

```
scoping → methodology → gathering ↔ synthesis → output → done
```

| Переход | Условие (машинно проверяемое) |
|---|---|
| scoping → methodology | `spec.md` существует (research objectives определены) |
| methodology → gathering | `plan.md` существует (methodology описана) |
| **gathering → synthesis** | **Минимум 3 источника documented** |
| synthesis → output | `findings.md` существует |
| output → done | Publication approved |

Ключевая особенность — цикл `gathering ↔ synthesis` (итеративный сбор evidence). Сравните с критикой OpenSpec (advisory verification): здесь переходы **блокируются** условиями — реализация принципа `../principles/invariants-and-gates.md`.

### Артефакты research-миссии

```
kitty-specs/001-serverless-auth-study/
├── spec.md              # Research objectives, hypothesis, scope
├── plan.md              # Methodology, sources, criteria
├── tasks.md             # Work package breakdown
├── findings.md          # Key discoveries, synthesis, recommendations
├── data-model.md        # Concepts, relationships, taxonomies
├── research/
│   ├── evidence-log.csv      # Structured source tracking
│   ├── source-register.csv   # Source registry
│   ├── comparison-matrix.md  # Side-by-side comparisons
│   └── synthesis-notes.md    # Integration insights
└── meta.json            # mission type: "research"
```

**evidence-log.csv** (машинно-читаемый след evidence):

```csv
timestamp,source_type,citation,key_finding,confidence,notes
2025-01-15T10:30:00Z,paper,"Smith et al 2024, JWT Security","Token rotation reduces breach window",high,"Peer-reviewed"
```

Поля: timestamp, source_type, citation, key_finding, confidence (high/medium/low), notes.

### Research patterns (типовые разбиения на work packages)

- **Technology Selection**: WP01–WP0N — один WP на опцию; последний WP — comparison matrix + рекомендация.
- **Literature Review**: WP01 — сбор источников; WP02–N — анализ по темам; последний — synthesis + gaps.
- **Best Practices Study**: standards research → case studies → pattern extraction → рекомендации для контекста.

Agent context: «You are a research agent conducting systematic literature reviews. Document ALL sources.»

### Template override (трёхуровневый lookup)

1. `.kittify/overrides/command-templates/` (per-project) → 2. `~/.kittify/missions/{mission}/command-templates/` (user-wide) → 3. package default. Тот же fallback-паттерн, что в `../methods/research-tooling.md`.

## Сравнение трёх SDD-инструментов (Spec Kit / Spec Kitty / specs.md)

| Аспект | GitHub Spec Kit | Spec Kitty | specs.md |
|---|---|---|---|
| Язык | Python | Python | Node.js |
| Установка | `uvx` | `uv tool install spec-kitty-cli` / pipx | `npx specsmd@latest install` |
| Звёзды | 139k | 1.7k (13,844 коммитов) | — (npm, 196 версий) |
| Ключевая концепция | Templates + prompts + presets | Missions + kanban + worktrees | Flows (Simple/FIRE/AI-DLC) |
| Governance | Базовый (checkpoints) | Полный (evidence, audit, acceptance) | Средний (adaptive checkpoints) |
| Brownfield | Ограниченно | Ограниченно | ✅ FIRE (auto-detect patterns) |
| Monorepo | Нет | Нет | ✅ FIRE (hierarchical standards) |
| Kanban/Dashboard | Нет | ✅ Kanban board | ✅ Web/CLI dashboard + VS Code ext |
| Git worktree | Нет | ✅ Isolation | Нет |
| AI-агентов | 3–4 (через instructions) | 10+ (спец. директории) | 11+ (спец. директории) |
| Team features | Community-driven | TeamSpace (коммерческий) | Community-driven |
| Философия | «Spec-first development» | «Governed delivery» | «Right-size the rigor» |

**Research-поддержка (итог итерации 3):** Spec Kitty — ✅ Full (research mission type); specs.md — ✅ Good (Ideation Flow); GitHub Spec Kit — ❌ нет (только software-dev templates).

### specs.md: три flows

| Flow | Для | Агентов | Checkpoints |
|---|---|---|---|
| Simple | Быстрая генерация спеков, прототипы | 1 | 3 (phase gates) |
| FIRE (Fast Intent-Run Engineering) | Адаптивное выполнение, brownfield, monorepos | 3 | Adaptive (0–2) |
| AI-DLC | Полная методология, DDD, regulated | 4 | Comprehensive |

**Adaptive checkpoints** (FIRE, аналог уровней L0–L4): L0 (trivial) → 0 checkpoints (autopilot); L1–L2 → 1 checkpoint (confirm); L3–L4 → 2 checkpoints (validate).

### Spec Kitty: 4 mission types и ключевые возможности

| Mission Type | Primary Goal | Key Activities |
|---|---|---|
| `software-dev` | Working code | Write tests, implement features, review code |
| `research` | Validated findings | Collect evidence, analyze data, synthesize conclusions |
| `plan` | Actionable plan | Define architecture, map dependencies, write roadmaps |
| `documentation` | Clear docs | Audit gaps, create content, validate accessibility |

Возможности: Kanban board (lanes specification → plan → execution → review → merge); Git worktree isolation (каждый агент в изолированном worktree); governance + evidence (audit trail от spec до merge, evidence к work packages); TeamSpace (командная версия, shared visibility, proof-of-delivery).

## Сопоставление с собственной архитектурой (notes/+views/)

`notes/YYYY-MM-DD-<slug>/` ↔ `kitty-specs/NNN-<slug>/` (эквивалент); `question.md` ↔ `spec.md`; `findings/NN-*.md` ↔ `research.md` + `evidence-log.csv` (**Spec Kitty лучше**: CSV structured, парсится без NLP); `comparison.md` ↔ `comparison-matrix.md`; `decision.md` → ADR ↔ `findings.md` + recommendations (Spec Kitty интегрирован с accept/merge); `views/` симлинки ↔ Kanban board (visual, **Spec Kitty лучше** для мониторинга); `learnings.md` — **нет аналога (наша фича)**; смена статуса скриптом ↔ state machine с guards (**Spec Kitty лучше**: evidence-gated); `threads/` ↔ Work Packages (эквивалент).

Что Spec Kitty делает лучше (8): evidence-gated state machine; evidence log в CSV; work packages (параллелизация); kanban board; dashboard; research → dev seamless (`/spec-kitty.accept` + `/spec-kitty.merge`); template override (трёхуровневый); per-feature missions.

Что наша архитектура добавляет (чего нет в Spec Kitty): **cross-mission knowledge accumulation** (`learnings.md` — Spec Kitty не накапливает lessons между миссиями, каждая — изолированный sandbox); **topic-based навигация** (`views/by-topic/` — Spec Kitty организует по mission, не по теме); frontmatter с произвольными полями (meta.json фиксирован); простота для малых задач (Spec Kitty предполагает полный state machine даже для «быстро глянуть 2 библиотеки»).

## Варианты A–D (рекомендации с содержанием)

**Вариант A: Adopt Spec Kitty для research.** Если процессы укладываются в mission types:
```bash
uv tool install spec-kitty-cli
spec-kitty specify --mission research "Which ORM for our async Python project?"
# → /spec-kitty.specify → /spec-kitty.plan → /spec-kitty.research → …
# → evidence-log.csv, comparison-matrix.md, findings.md
spec-kitty mission switch software-dev   # затем на реализацию
```
Плюсы: готовый evidence-gated workflow, guards, CSV log, WPs, kanban, worktree isolation. Минусы: нет cross-mission knowledge accumulation, нет topic-навигации.

**Вариант B: Spec Kitty + расширение для knowledge accumulation.** Spec Kitty для research-миссий + `learnings.md` на уровне проекта + `views/` с симлинками + скрипт извлечения:
```bash
# После /spec-kitty.accept:
python scripts/extract-learnings.py kitty-specs/001-orm-comparison/
# → обновляет learnings.md; создаёт симлинки в views/by-topic/orm/
```

**Вариант C: specs.md Ideation + Spec Kitty Research + Development** (см. pipeline выше в статье).

**Вариант D: Собственная архитектура (максимальная гибкость).** Оставить notes/+views/+frontmatter/+learnings, заимствовать: **evidence-log.csv** формат; **guards** (минимум N источников для transition); **work packages** (параллелизация). НЕ строить state machine — использовать frontmatter + скрипты.

### Матрица выбора

| Сценарий | Рекомендация |
|---|---|
| Быстрый старт, минимальная кастомизация | specs.md + Ideation Flow |
| Глубокая кастомизация research-процесса | Форк/extension specs.md (TypeScript) |
| Полный контроль, своя архитектура | Собственный research-tools (TS или Python) |
| Интеграция с GitHub Spec Kit | Extension к Spec Kit (Python) |
| Governance + audit trail | Spec Kitty + extension (Python) |

### Паттерны для заимствования (сводно)

| Паттерн | Источник | Применение |
|---|---|---|
| Missions как blueprints | Spec Kitty | mission-types: «technology-evaluation», «landscape-survey», «architecture-spike» |
| Adaptive checkpoints | specs.md/FIRE | L0=0 checks, L1=1, L2–3=2, L4=full review |
| AGENTS.md + CLAUDE.md symlink | Spec Kitty | Единый AGENTS.md, CLAUDE.md → symlink |
| Worktree isolation | Spec Kitty | Каждый research-цикл в отдельном worktree |
| Kanban lanes | Spec Kitty | `inbox → active → review → decided` визуализация |
| Hierarchical overrides | specs.md | Project config → module overrides |
| Walkthrough generation | specs.md | Auto-summary после каждого research-цикла |
| Tool-specific agent dirs | Оба | `.cursor/commands/research-*.mdc`, `.claude/commands/research-*.md` |
| Pack system | Spec Kitty | Research-packs: «orm-research», «auth-research» с готовыми шаблонами |

## TypeScript vs Python (пересмотренная позиция)

Честный вывод исследования: «для вашей задачи TypeScript — валидный и возможно лучший выбор». Решающие факторы: target ecosystem (specs.md → TS; Spec Kit/Spec Kitty → Python); team expertise; TUI (Ink для TS vs Textual для Python — оба зрелые); AI harness integration (Claude Code/Canvas, Cursor `.mdc`, Copilot `.agent.md`, Codex `.codex/` — TS-friendly; MCP SDK официальный у обоих); типизация (TS строгая vs Python optional); distribution (npx vs uvx). Python конкурентен если: target — Spec Kit/Spec Kitty ecosystem; Textual; data/ML; быстрота итерации без build step.

### Ideation Flow — ключевые фичи

1. **Anti-Bias Engine** — 12-domain wheel (Technology, Psychology, Business, Nature, Art, Games…) гарантирует разнообразие идей.
2. **Deep Thinking Per Batch** — 6-step reasoning chain: domain check → raw concepts → novelty filter → cross-pollination → provocation → polish.
3. **Research-Backed Methods** — синтез Osborn-Parnes CPS, de Bono's Six Hats, Dilts' Disney Strategy; методы невидимы — виден только результат.
4. **Resumable Sessions** — сессии автоматически persist'ятся (`.specs-ideation/sessions/{topic-slug}-{YYYYMMDD}/session.yaml`).

Когда использовать: starting a new feature / want novel angles; stuck in an echo chamber (anti-bias pulls from non-tech domains); product discovery session; concept brief for a meeting; stress-test an idea (Black Hat + Critic surface risks early).

## specs.md: Ideation Flow (pre-research brainstorming)

Три фазы, три навыка, разный AI/user ratio:

| Фаза | Навык | Что делает | AI/User | Output |
|---|---|---|---|---|
| **Generate** | Spark | Дивергентная генерация, 5 идей за batch, multi-domain, anti-bias | 80/20 | `spark-bank.md` |
| **Evaluate** | Flame | Конвергенция: Six Hats analysis, Impact × Feasibility scoring | 60/40 | `flame-report.md` |
| **Shape** | Forge | Disney's Creative Strategy (Dreamer→Realist→Critic) | 40/60 | `concept-briefs/*.md` |

Сессия: `.specs-ideation/sessions/{topic-slug}-{YYYYMMDD}/` с `session.yaml` (phase, favorites, scores — resumable).

Другие flows specs.md: Simple (Requirements → Design → Tasks), FIRE (Fast Intent-Run Engineering: orchestrator/planner/builder, `.specs-fire/` с state.yaml), AI-DLC (Inception → Construction (bolts: Model → Design → ADR → Implement → Test) → Operations; `memory-bank/`). Позиционирование против конкурентов: 3 phase-based агента вместо 19+ role-based (vs BMAD); pluggable flows, выбор overhead (vs Spec Kit); IDE и AI-agnostic, открытая реализация AWS AI-DLC (vs Kiro). 11+ интеграций (Claude Code, Cursor, Copilot, Antigravity, Windsurf, Kiro, Gemini CLI, Cline, Roo, Codex, OpenCode).

## Пересмотренная модель: research как фаза pipeline

```
Ideation → Research → Specification → Planning → Implementation → Review → Deploy
   ↑          ↑           ↑            ↑           ↑           ↑
 Ideation   (notes/     Simple       FIRE       AI-DLC     Evidence
 Flow       собств.)    Flow         Flow       Flow       (Spec Kitty)
```

**Вариант C (комбинация)**: Ideation (specs.md) → Research (Spec Kitty) → Development (Spec Kitty): concept-briefs → evidence-log.csv / findings.md / comparison-matrix.md → working code.

## Сильные и слабые стороны

Spec Kitty сильные: evidence-gated переходы (машинный gate, не advisory); CSV-след evidence (machine-readable, проверяемый CI); per-feature mission types; auditable delivery record; 10+ агентных интеграций. Слабые/риски: форк-модель (может наследовать проблемы Spec Kit — см. `sdd-criticism.md` §2.6); молодой проект (1.7K звёзд на 09.2026, 13,737 commits — интенсивная разработка, стабильность под вопросом); явной независимой критики на дату исследования нет.

specs.md сильные: Ideation Flow — уникальное покрытие pre-research фазы (генерация и оценка идей); выбор overhead через flows; brownfield-first. Слабые: community «just born (December 2025)», нет публичной критики и production-постмортемов.

Чего не закрывают оба (уникальные фичи собственной архитектуры из `../principles/content-stays-virtual-structure.md`): cross-mission learnings (курсорный файл уроков между исследованиями) и topic-навигация (views/ по темам через симлинки) — кандидаты на заимствование в собственную систему либо на contribution.

## Выбор (рекомендации исходного исследования, пересмотренные)

- Research в контексте delivery проекта → Spec Kitty Research Mission (adopt), при необходимости adapt через template overrides.
- Brainstorming до research → specs.md Ideation Flow.
- Собственная система — только если нужны cross-mission learnings + topic-views как первоклассные механизмы и независимость от форк-модели (вариант D в терминах исследования: свои скрипты поверх notes/+views/, заимствуя evidence-gated guards и CSV-форматы).
- Полный разбор альтернатив и статус ландшафта: `sdd-tools-overview.md`; cross-tool handoff и переносимая memory — `spec-weave.md` (SpecWeave, дополняющий инструмент: переносит работу и project memory между вендорами/аккаунтами — закрывает «AI forgets everything between sessions» на уровне delivery, чего Research Mission не делает).

## Источники

- Spec Kitty: https://github.com/spec-kitty/spec-kitty | https://docs.spec-kitty.ai | https://spec-kitty.ai
- specs.md: https://github.com/fabriqaai/specs.md | https://www.npmjs.com/package/specsmd
- Входные материалы inbox: `research-and-notes/research-process.md` (строки 2230–3019), `README.md` (бэклог F)
- Связанные KB: `../methods/research-knowledge.md`, `../principles/content-stays-virtual-structure.md`, `sdd-tools-overview.md`
