---
id: research-note-20261002-cli-tool-selection
type: research-note
status: active
created: 2026-10-02
updated: 2026-10-02
topics: [sdd-tools, specs-md, spec-kitty, pi, oh-my-pi, cli-tool, adopt-adapt-build]
author: agent:omp
---

# Research: выбор SDD-инструмента для разработки сложного CLI с нуля

## Вопрос

Для нового репозитория, где будет разрабатываться сложный инструмент командной строки: какой SDD-инструмент adopt (с адаптацией, закрывая ~95% потребностей) вместо написания своего с неясным результатом?

Критические требования:
1. **Совместимость с нашими harnesses**: [earendil-works/pi](https://github.com/earendil-works/pi) и [can1357/oh-my-pi](https://github.com/can1357/oh-my-pi) — omp не просто форк pi, полностью переписан и возможно не совсем совместим.
2. **Контекст-экономика**: размер текста в контексте неважен, если он ведёт к решению за меньшее число шагов/выходных токенов. Важно: релевантный текст подключается по задаче; нерелевантный не лежит мёртвым грузом.
3. **Настраиваемость процесса**: можно ли адаптировать под свои конвенции.

## Метод

Клонированы и изучены исходники (вторая итерация; первая — только веб, оказалась неполной):

| Репозиторий | Коммит | Что изучено |
|---|---|---|
| fabriqaai/specs.md | main, depth 1 | src/flows/* (все 4 flow), src/lib/installers/, memory-bank.yaml, все .hbs шаблоны |
| spec-kitty/spec-kitty | main, depth 1 | src/specify_cli/ (98 модулей), missions/*/templates, packs/built-in/, skills/command_installer.py, core/config.py |
| earendil-works/pi | main, depth 1 | packages/coding-agent/src/core/skills.ts, resource-loader.ts, config.ts |
| can1357/oh-my-pi | main, depth 1 | docs/skills.md, docs/context-files.md, docs/slash-command-internals.md, docs/config-usage.md |

Точное имя пакета pi: `@earendil-works/pi-coding-agent` (раньше badlogic/pi-mono). omp — форк старого pi-mono, переписанный: TypeScript → Rust addons + TypeScript, своя система discovery.

## Findings

### F1. Поддержка наших harnesses

**spec-kitty: pi — официально поддержан (tier: partial).**

Из `docs/api/supported-harnesses.md` (коммит main на 2026-10-02):

| Harness | Ключ | Механизм | Tier |
|---|---|---|---|
| Claude Code | `claude` | `.claude/commands/*.md` | first_class |
| Codex CLI | `codex` | `.agents/skills/` | first_class |
| (9 инструментов) | opencode, cursor, gemini, qwen, q, copilot, auggie, kilocode, windsurf | commands/workflows/prompts | supported |
| **Pi TUI** | `pi` | `.agents/skills/spec-kitty.*/SKILL.md` | **partial** |
| Letta Code | `letta` | `.agents/skills/` | partial |

Из `src/specify_cli/core/config.py`:
```python
"pi": {"class": SKILL_CLASS_SHARED, "skill_roots": [".agents/skills/", ".pi/skills/"]},
```
Pi входит в `_agent_roster.py::SUPPORTED_AGENTS = ("codex", "vibe", "pi", "letta")` — «shared-root command-skill agents». Installer рендерит каждую команду как Agent Skill: `.agents/skills/spec-kitty.specify/SKILL.md` с frontmatter `name, description, user-invocable`.

«Partial», а не «supported» — только потому, что у spec-kitty нет записанного real-session smoke-теста с Pi (правило повышения tier: один задокументированный smoke test). Механизм при этом стандартный и рабочий: pi читает `.agents/skills/` (подтверждено из исходников pi, см. F2).

**spec-kitty: oh-my-pi — НЕ поддержан напрямую.** В supported-harnesses.md отсутствует. Но: omp читает `.agents/skills/` через провайдер `agents` (см. F3), т.е. артефакты spec-kitty для pi будут подхвачены omp автоматически.

**specs.md: pi — отсутствует в списке установщиков.** `src/lib/installers/` содержит 12 установщиков (Claude, Cursor, Copilot, Antigravity, Cline, Codex, Gemini, Kiro, OpenCode, Roo, Windsurf, base). Pi и oh-my-pi — нет.

### F2. pi (earendil-works): как он находит skills и контекст

Из `packages/coding-agent/src/core/skills.ts`:
- Skills — стандарт Agent Skills: `<skills-root>/<name>/SKILL.md`, frontmatter `name` (≤64, `[a-z0-9-]`), `description` (≤1024). `disable-model-invocation` поддержан.
- Roots: проектные `.agents/skills/`, `.pi/skills/` (совпадает с ожиданиями spec-kitty).

Из `packages/coding-agent/src/core/resource-loader.ts`:
- Контекст-файлы: `AGENTS.override.md` → `AGENTS.md` → `CLAUDE.md` (и `.MD` варианты), иерархическая загрузка от cwd вверх до корня репо + глобальный `~/.pi/agent/`.
- Т.е. наш корневой `AGENTS.md` pi подхватит нативно.

### F3. oh-my-pi (omp): discovery-система — самая широкая

Из `docs/skills.md` и `docs/context-files.md`:

**Skills** — три прохода, приоритеты провайдеров:
1. `native` (.omp) — 100
2. `skillshare` — 95
3. `omp-plugins` — 90
4. `claude` — 80
5. `agent-plugins` — 75
6. `claude-plugins`, `agents` (.agent/.agents), `codex` — 70
7. `opencode` — 55
8. `github` — 30
9. `omp-managed` — 5

**`agents`-провайдер читает `.agents/skills/`** — значит SKILL-пакеты spec-kitty, установленные «для pi», omp обнаружит без какой-либо модификации. Skill exposure: name+description в system prompt (легковесно), тело — по требованию через `skill://...` (read tool). Это ровно наша контекст-экономика: полный текст не грузится, пока не понадобился.

**Slash-команды** (`docs/slash-command-internals.md`): провайдеры native (`.omp/commands/*.md`), claude (`.claude/commands/**/*.md`), codex (`.codex/commands/`), opencode. `.agents/commands/` — **не** сканируется на команды (только skills). Т.е. command-файлы spec-kitty в формате `.claude/commands/` omp прочитает (провайдер claude, project-level, включён по умолчанию), но штатный механизм spec-kitty для pi — skills, и это правильно.

**Контекст-файлы**: `AGENTS.md` (standalone, walk-up от cwd до корня репо) — нативно; `RULES.md` — sticky (always-apply). omp также наследует `.claude`, `.cursor`, `.codex` и т.д. «No migration script».

**Вывод по F3**: omp обратно совместим с pi-артефактами на уровне `.agents/skills/` и `AGENTS.md`. «Полностью переписан» относится к ядру (Rust crates: pi-edit, pi-walker, pi-shell и т.д.) и TUI, а не к формату skill-пакетов — формат стандартизован (Agent Skills).

### F4. Контекст-экономика в spec-kitty vs specs.md

**spec-kitty** — контекст подключается по фазе миссии:
- Step contracts (`packs/built-in/missions/built_in_step_contracts/research-*.step-contract.yaml`): на каждом шаге загружается charter-контекст только для этого action (`spec-kitty charter context --action gathering --json`), промпт шага, и WP-контекст.
- Skills: только `name`+`description` в системе; тело — по вызову.
- State в `status.events.jsonl` (append-only) и frontmatter WP — агент перечитывает состояние вместо удержания в контексте.
- Каждая сессия WP начинается fresh: «Each agent invocation starts fresh — agents reload all context from artifacts at startup».

**specs.md** — аналогично: agents/skills — markdown с description; память в артефактах (`state.yaml`, `session.yaml`), агент перечитывает. FIREbuilder-скрипты (`init-run.cjs`, `update-phase.cjs`) мутируют state машинно, не через контекст.

**Оба инструмента решают контекст-экономику одинаково**: тонкие метаданные в промпте, тело по требованию, состояние на диске. Разница в gate-модели:
- spec-kitty: **блокирующие машинные gates** (`event_count("source_documented", 3)` — переход к synthesis физически невозможен, пока движок не увидит 3 события; WP review: for_review → in_review → approved).
- specs.md: checkpoints advisory (0/1/2 по complexity×autonomy), человек решает.

### F5. Настраиваемость процесса

**spec-kitty** (порядок убывания стоимости):
1. `.kittify/overrides/command-templates/` — переопределение шаблонов артефактов и промптов (3-tier: project → user-global → package).
2. `.kittify/missions/<key>/mission.yaml` — custom mission: свои шаги, required artifacts, validation checks, paths (workspace/data/deliverables), agent_context, MCP tools. Появляется в picker `/spec-kitty.specify`.
3. `validators.py` рядом с mission.yaml — кастомные машинные проверки (`validation.custom_validators: true`).
4. `plan-field-declaration.yaml` — машинно-проверяемая декларация обязательных полей плана.
5. mission-runtime.yaml — DAG шагов с depends_on и agent-profiles.
6. Constitution/charter — governance-слой (директивы, процедуры, тактики) — для нас избыточен, можно не активировать.

Проверено в исходниках: custom mission — это YAML + templates + опциональный validators.py, без кода в ядре.

**specs.md**:
1. После install всё — редактируемый markdown: `.specsmd/<flow>/agents/*/skills/*/SKILL.md`, `.hbs` шаблоны.
2. `memory-bank.yaml` — декларативная схема артефактов (artifact_root, structure, schema, naming, ownership) — можно переназначить корень артефактов.
3. Новый flow = каталог в src/flows/ + регистрация (это уже форк-уровень, но дёшево: 90% методологии — markdown).
4. 12 установщиков; pi/omp нет — пришлось бы писать установщик (или класть команды руками в `.omp/commands/`, что omp поддерживает нативно).

### F6. Процесс для CLI-разработки (software-dev)

**spec-kitty software-dev mission**: discovery → specify → plan → tasks_outline → tasks_packages → tasks_finalize → implement → review → accept. Guards: plan блокируется до существования spec.md; implement — до plan+tasks; review — до approval всех WPs. WP-механика: worktree-изоляция на lane, `tasks/WP##-*.md` с frontmatter (dependencies, lane, history[]), append-only event log, review-цикл с feedback-указателями. Плюс: research-миссия как upstream-фаза (evidence-log.csv, source-register.csv, guard ≥3 источников) перед software-dev. Полный lifecycle: research → specify → plan → tasks → implement → review → accept → merge + retrospective.

**specs.md FIRE**: intent → work-item → run; adaptive checkpoints; walkthrough после каждого run; brownfield-сканирование; hierarchical standards (constitution.md не переопределяется модулями). Меньше governance, больше автономии.

Для «сложного CLI с нуля» миссия spec-kitty — более точное попадание: спецификация и план фазово блокируются, работа пакуется в WPs, review обязателен. FIRE оптимизирован под скорость в brownfield.

## Comparison

| Критерий | spec-kitty | specs.md | Своё с нуля |
|---|---|---|---|
| pi (earendil-works) | ✅ partial (официально, skills) | ❌ нет установщика | ✅ |
| oh-my-pi | 🟡 не заявлен, но `.agents/skills/` omp читает через провайдер `agents` | ❌ | ✅ |
| AGENTS.md (наш) | не трогает; pi/omp подхватят | не трогает | ✅ |
| Контекст по задаче | ✅ charter context per-action + skills on-demand | ✅ skills + state на диске | Строить |
| Блокирующие gates | ✅ машинные (event_count, WP lanes) | ⚠️ advisory checkpoints | Строить |
| Software-dev процесс | ✅ полный lifecycle с review | 🟡 FIRE (быстрее, меньше governance) | Строить |
| Research перед кодом | ✅ research mission → software-dev | ⚠️ ideation (brainstorm) | Строить |
| Кастомизация без форка | ✅ overrides + custom missions + validators | ✅ markdown/.hbs после install | По определению |
| Зрелость | 13k+ commits, 4.0.0rc2 | молодая (12.2025) | — |

## Decision

**Для CLI-инструмента: adopt spec-kitty (вариант A), адаптировать 5%.**

Обоснование:
1. **Поддержка pi — официальная** (tier partial только из-за отсутствия smoke-теста в их docs; механизм стандартный). omp подхватит те же `.agents/skills/` автоматически (провайдер `agents`, priority 70). У specs.md нет ни pi, ни omp.
2. **Контекст-экономика — правильная в обоих, но gates различают**: spec-kitty блокирует переходы машинно; для сложного CLI (высокая цена ошибки) это важнее скорости FIRE.
3. **95% процесса готово**: research → software-dev → merge с worktree-изоляцией, WP-механикой, обязательным review, retrospective. Писать это с нуля — месяцы.
4. **Адаптация — штатные механизмы, не форк**: template overrides (наш frontmatter), custom mission при необходимости, validators.py для своих проверок.

**План адаптации (те самые ~5%):**

1. `spec-kitty init . --ai pi` (+ при работе через omp — артефакты те же, `--ai pi` создаёт `.agents/skills/`, который omp читает).
2. `.kittify/overrides/command-templates/` — переопределить шаблоны артефактов нашим frontmatter (id/type/status/created/updated/topics/author из нашего `tools/process-framework/conventions/frontmatter.md`).
3. Smoke-тест на pi и на omp (одна low-risk миссия): убедиться, что `/skill:spec-kitty.specify` резолвится в обоих. Это заодно снимет «partial»-неопределённость для нас.
4. При несовпадении шагов — custom mission `cli-dev` на базе software-dev (mission.yaml + templates + validators.py).
5. В наш `AGENTS.md` добавить секцию о совместном проживании: `.kittify/`, `kitty-specs/`, `.worktrees/` — tooling state, exempt из конвенций корпуса.

**Fallback-условия (переоценка решения):**
- Smoke-тест на omp падает и не чинится настройкой провайдеров → смотреть specs.md с ручной установкой команд в `.omp/commands/` (omp нативно поддерживает), ценой потери блокирующих gates.
- Появится потребность в параллельных worktree-агентах с иным lifecycle → переоценить FIRE.

## Риски

| Риск | Митигация |
|---|---|
| omp-несовместимость глубже, чем discovery (вызовы `spec-kitty` CLI из сессии, exit codes) | smoke-тест обоих harnesses на шаге 3 до принятия решения |
| Spec Kitty 4.0.0rc2 — prerelease; API может дрейфовать | pin версии CLI; `spec-kitty upgrade` запускать осознанно |
| Frontmatter WP-файлов не проходит нашу конвенцию | overrides шаблонов (шаг 2); kitty-specs/ — tooling state |
| Root clutter (.kittify/, kitty-specs/, .worktrees/) | gitignore .worktrees/; принять как стоимость |

## Источники

- spec-kitty клон, main: `src/specify_cli/core/config.py` (AGENT_SKILL_CONFIG, pi: shared, `.agents/skills/`+`.pi/skills/`), `src/specify_cli/skills/_agent_roster.py` (SUPPORTED_AGENTS), `docs/api/supported-harnesses.md` (tiers), `docs/guides/how-to/harnesses/pi-tui.md` (структура установки, `/skill:spec-kitty.*`), `packs/built-in/missions/built_in_step_contracts/research-gathering.step-contract.yaml` (event_count guard), `src/specify_cli/skills/command_renderer.py` (frontmatter name/description/user-invocable)
- specs.md клон, main: `src/lib/installers/` (12 установщиков, pi/omp отсутствуют), `src/flows/ideation/memory-bank.yaml` (schema, anti-bias config), `src/flows/*/templates/*.hbs`
- pi клон, main (`@earendil-works/pi-coding-agent`): `packages/coding-agent/src/core/skills.ts` (Agent Skills spec, валидация name/description), `src/core/resource-loader.ts` (AGENTS.md/CLAUDE.md walk-up + worktree shadow)
- omp клон, main: `docs/skills.md` (провайдеры, приоритеты, `agents`-провайдер читает `.agents/skills/`, skill:// on-demand), `docs/context-files.md` (native .omp, agents-md walk-up, RULES.md sticky), `docs/slash-command-internals.md` (провайдеры команд, `.agents/commands/` не сканируется)
- Связанное: `../2026-10-02-sdd-tools-artifacts/` (первая итерация: артефакты, GAP-анализ, adopt CSV-схем для knowledge-репо)
