---
id: findings-mechanics-20261002
type: research-note
status: final
created: 2026-10-02
updated: 2026-10-02
topics: [sdd-tools, specs-md, spec-kitty, pi, oh-my-pi, commands, gates, hooks]
author: agent:omp
---

# Findings: механика процессов, gates, команд и хуков (вторая волна вопросов)

Спутник `question.md` в этой директории. Все утверждения — из клонированных исходников (пути указаны). Отвечает на четыре вопроса: (1) команды vs промпты, процессы и их запуск; (2) действительно ли «блокирующие» gates; (3) формат команд в pi/omp, аргументы, хуки, детерминированный код; (4) как добавить pi/omp в specs.md.

## A. Команды или промпт? Какие процессы? Как запускаются?

### Оба инструмента — гибриды: тонкая команда-промпт + вся методология в файлах

**specs.md.** Command-файл (`src/flows/*/commands/*.md`, ~30–50 строк) — это промпт-активатор. Пример `src/flows/fire/commands/fire.md`: frontmatter `{description}`, затем «You are now the FIRE Orchestrator», «IMMEDIATELY read agent persona from `.specsmd/fire/agents/orchestrator/agent.md`», затем «execute route skill». Вся логика — в agent.md / SKILL.md / .hbs-шаблонах, команда только маршрутизирует. Это и есть контекст-экономика: команда весит копейки, тело загружается по задаче.

**spec-kitty.** Аналогично: `.claude/commands/spec-kitty.specify.md` или рендеренный skill `.agents/skills/spec-kitty.specify/SKILL.md` (frontmatter `name, description, user-invocable` — из `command_renderer.py::build_frontmatter`, строки ~383) активирует шаг миссии; промпт шага лежит в `packs/built-in/missions/mission-steps/<type>/<step>/prompt.md`.

### Инвентарь процессов

| | specs.md | spec-kitty |
|---|---|---|
| Процессы | 4 flows: ideation, simple, fire, aidlc (выбирается при install, один на проект) | 4 mission types: software-dev, research, plan, documentation (сосуществуют, выбирается на миссию) |
| Запуск процесса | `/specsmd-fire` (одна точка входа на flow) | `/spec-kitty.specify "name" --mission-type research` или CLI `spec-kitty specify <name> --mission-type research` |
| Запуск шага | `/specsmd-spark`, `/specsmd-flame`… или маршрутизация сама | `/spec-kitty.plan`, `/spec-kitty.implement WP01`…; для pi: `/skill:spec-kitty.plan` |
| Continue/авто | FIRE `route` skill сам решает следующий шаг | `spec-kitty next --agent X --json` — машина решает; канонический цикл агента (из `runtime/next/decision.py`): `while True: decision = spec-kitty next --json; if terminal: break; execute(decision.prompt_file)` |

### Может ли агент сам понять, что пора запустить процесс?

**specs.md — да, через route-сканирование** (`src/flows/fire/agents/orchestrator/skills/route/SKILL.md`): мандаты «ALWAYS scan file system for intents/work-items not in state.yaml», «FILE SYSTEM is source of truth — state.yaml may be incomplete», «Route based on VERIFIED state». Route читает state.yaml, сверяет с ФС, находит pending work items / active runs и направляет на planner/builder. Т.е. агент определяет следующий шаг детерминированно-процедурно (по состоянию), а не «понимает» свободно.

**spec-kitty — да, и это основной цикл**: `spec-kitty next` — не промпт, а Python-команда, возвращающая JSON-решение (`Decision` в `runtime/next/decision.py`): kind ∈ {step, decision_required, blocked, terminal, query}, с prompt_file, reason, guard_failures, question/options. Агент вызывает `next`, получает следующий шаг или блокировку с причиной. Плюс ступень выше: каждый prompt-файл шага (например `mission-steps/research/gathering/prompt.md`) содержит инструкции что делать и как эмитить события.

**Но ни один не «просыпается» без триггера**: запуск процесса всегда инициирует человек (`/команда`) или внешний цикл, вызывающий `next`. Skill-механика pi/omp добавляет автоактивацию по описанию (см. C), но это про skills вообще, не про SDD-процессы spec-kitty: их skills имеют `user-invocable: true` и заточены под явный вызов.

## B. «Блокирующие» gates — так ли невозможно?

**Уточнение формулировки: gate не прерывает агентный цикл физически — он не даёт движку выдать следующий шаг.** Механика (из `runtime/next/runtime_bridge_cores.py`, `_evaluate_research_guards`, строки ~553–576):

```python
def _evaluate_gathering_guard(snapshot):
    failures = _check_artifact_present(snapshot, "source-register.csv")
    if snapshot.status_facts["source_documented_count"] < 3:
        failures.append("Insufficient sources documented (need >=3)")
    return failures
# ...
if action == "synthesis":
    return _check_artifact_present(snapshot, "findings.md")
# fail-closed default:
return [f"No guard registered for research action: {action}"]
```

Ответы по пунктам:

1. **«Физически невозможно» — верно в границах протокола**: `decide_next` при непройденном guard возвращает `kind="blocked"` c `guard_failures` (списком причин) и `guard_failure_paths` (путь, который guard читал — добавлено issue #3883 «диагностика без чтения исходника»). Агент, следующий циклу `next → execute`, не получит prompt_file следующего шага. Если вызвать `/spec-kitty.synthesis` напрямую, slash-команда выполнится как промпт, но при завершении шага `next` не продвинет миссию — цикл замкнётся на gathering.

2. **Прерывает ли агентный цикл?** Нет — и не должен. Gate пассивен для LLM: он проверяет состояние (event log + артефакты) и возвращает вердикт. «Прерывание» происходит на уровне протокола: агент видит blocked + reason и должен вернуться и добрать источники. Fail-closed default (неизвестный action → блок) исключает обход через незарегистрированный шаг.

3. **Задаёт вопросы?** Да, но другим механизмом: `DecisionKind.decision_required` и `query` с полями `question`, `options` — движок сам спрашивает агента/человека, когда требуется выбор (например, приёмка). Это не guard, а параллельный механизм. Guard молчит о «почему», если только не смотрели guard_failures.

4. **Объясняет ли поведение?** Частично: `guard_failures` — строки вида `"Insufficient sources documented (need >=3)"`, `guard_failure_paths` — какой файл/путь проверялся. Плюс промпты шагов сами предупреждают (gathering/prompt.md, строка 32): gate на `gathering -> synthesis` считает **events, не строки CSV** — «Editing the CSV without the run engine observing the corresponding event does not advance the mission; follow your harness's event-emission mechanism». Т.е. подделка артефакта не проходит: событие `source_documented` эмитит движок, а не файл.

5. **Где граница силы gate**: guard проверяет то, что может проверить машина (наличие файлов, счётчик событий, approval-флаги). Он не проверяет качество источников — «три источника» может быть тремя слабыми. Промпт methodology прямо говорит: floor ≠ target, план должен ставить цель выше.

**Итог по B**: «блокирующий» = «state machine не переходит дальше и объясняет почему», а не «прерывает LLM-цикл». Для нашей терминологии честнее: **машинно-проверяемые переходы с диагностируемым отказом**. Agent-цикл прерывать и не нужно — прицип экономики внимания: машина фильтрует, человек решает по квалифицированным расхождениям (наш kb: attention-economy).

## C. Команды в pi/omp: формат, аргументы, хуки, код без LLM

### Три типа «команд» в pi (docs: slash-commands.md, prompt-templates.md, skills.md, extensions.md)

| Механизм | Что это | Аргументы | Код без LLM |
|---|---|---|---|
| **Skill** `/skill:name` | Каталог `SKILL.md` + scripts/references/assets. В промпте — только name+description; тело грузится по задаче | Всё после `/skill:name` — как user request: `/skill:pdf-tools extract report.pdf`. `disable-model-invocation: true` — только явный вызов | Скрипты скилла запускает сам агент (bash); вне цикла — нет |
| **Prompt template** `/name` | Один .md в `~/.pi/agent/prompts/` или `.pi/prompts/`; filename = имя команды | Shell-подобные: `$1`, `$2`, `$@`/`$ARGUMENTS`, `${1:-default}`, `${@:N:L}`; `argument-hint` в frontmatter для автодополнения; `/review "API compatibility"` — один аргумент с пробелом | Нет — это чистый промпт |
| **Extension command** `/name` | TypeScript-модуль, `pi.registerCommand("hello", {handler})` — из docs/extensions.md | Произвольные, сам парсишь в handler | **Да** — handler исполняется без LLM (пример hello просто печатает notify) |

Пути поиска skills в pi: `~/.agents/skills/`, `.agents/skills/` (walk-up от cwd до корня репо), `.pi/skills/`, пакеты. Валидация: name ≤64 `[a-z0-9-]`, description ≤1024; без description — не грузится. `/reload` после правок.

### omp: те же три механизма + более широкая система discovery

- Команды: провайдеры с приоритетами — native `.omp/commands/*.md` (100) > omp-plugins (90) > claude `.claude/commands/**/*.md` (80, project-level включён по умолчанию) > claude-plugins/agents/codex (70) > opencode (55). `.agents/commands/` на команды НЕ сканируется — только на skills.
- Skills: те же провайдеры + `agents` (`.agents/skills/`) — сюда попадают артефакты spec-kitty; тело через `skill://` URL, неймспейсы при коллизиях.
- Формат командного .md у native/claude-провайдеров: frontmatter `description` (+ `name` для override у codex/opencode), `$ARGUMENTS`-подстановки как в pi.

### Хуки до/после детерминированно — да, через extensions/hooks (оба инструмента)

pi (extensions.md) — события: `session_start`, `before_agent_start` (может модифицировать промпт/systemPromptOptions), `agent_start`, `tool_call` (pre; может `{block: true, reason}` или заменить input), `tool_result` (post; может заменить content/isError), `turn_start/turn_end`, `agent_end`, `session_shutdown`. Расширения пишутся на TS, грузятся без компиляции (jiti): `pi --extension ./hook.ts`.

omp (hooks.md): `--hook` — алиас `--extension`; hook-файлы `.omp/hooks/pre/*.ts` (и пост) подхватываются как extension-модули с `pi.on(...)`. Пример из docs — блокировка `rm -rf` в `tool_call`. Тот же жизненный цикл: `before_agent_start` → `tool_call/tool_result` → `agent_end`.

**Ответ на «команда может выполнить хуки до и после работы агента детерминировано»**: сама markdown-команда — нет (она промпт), но связка «extension слушает `before_agent_start` (детектит вызов команды по промпту) + `agent_end`» — да, полностью детерминированно и без LLM. Для строгих gate это правильное место: guard-код в extension не может быть «уговорён» моделью.

### Код без LLM

- pi/omp extension: `registerCommand` handler, `registerTool` — детерминированный код.
- specs.md: FIRE-скиллы включают Node-скрипты (`scripts/init-run.cjs`, `update-phase.cjs`, `complete-run.cjs`) — их запускает агент через bash, но сами они чистый код: мутация state.yaml, детерминированная генерация run ID.
- spec-kitty: весь CLI — Python без LLM: `next`, `mission list`, `agent tasks status --json`, `charter context --action gathering --json`. Агент вызывает их как инструменты; результат — JSON.

## D. Как добавить поддержку pi/omp в specs.md?

Установщик — правильное место, архитектура готова. Три уровня усилий:

### Вариант 1: минимальный, без изменения specs.md (работает уже сейчас)

omp нативно читает `.claude/commands/**/*.md` (провайдер claude, project-level, включён по умолчанию). После `npx specsmd install` c выбранным Claude Code файлы `.claude/commands/specsmd-*.md` уже видны в omp как команды. Для pi: скопировать `commands/*.md` в `.pi/prompts/` (или `~/.pi/agent/prompts/`) — pi превратит каждый .md в `/specsmd-<name>` с `$ARGUMENTS`. Подстановки в командах specs.md уже используют `$ARGUMENTS` (simple/commands/agent.md, строка 22) — формат pi-шаблонов совместим напрямую.

Стоимость: пара скриптовых строк, ноль изменений в specs.md. Ограничение: skills-механика specs.md (SKILL.md в `.specsmd/`) не станет auto-invocable — команды будут «прочитай и действуй», что для активатор-команд specs.md и есть задуманный режим.

### Вариант 2: PR в specs.md — новые установщики (правильный путь)

Структура установщика (из `src/lib/installers/ToolInstaller.js` + `ClaudeInstaller.js`):

1. Создать `PiInstaller.js`:
   ```js
   class PiInstaller extends ToolInstaller {
     get key() { return 'pi'; }
     get name() { return 'Pi'; }
     get commandsDir() { return path.join('.pi', 'prompts'); }
     get detectPath() { return '.pi'; }
   }
   ```
   `installCommands` наследуется: копирует `flowPath/commands/*.md` → `.pi/prompts/specsmd-<name>.md`. `$ARGUMENTS`/`$1` работают без трансформации.
2. Создать `OmpInstaller.js`: `commandsDir = '.omp/commands'` — omp native-провайдер (priority 100).
3. Зарегистрировать оба в `installer.js` (массив установщиков) и, при желании, в детект (`detect()` по `detectPath`).
4. Альтернатива для обоих: если хотим Agent Skills вместо промптов — рендерить каждый command как `SKILL.md`-каталог (как делает spec-kitty: `.agents/skills/specsmd-<name>/SKILL.md` с frontmatter name/description). Тогда оба (pi читает `.agents/skills/`, omp — через провайдер agents) получат авто-подгрузку по описанию. Это дороже: нужен рендерер frontmatter из `description:` command-файлов.

### Вариант 3: skills-first (макс. интеграция)

Рендерить skills-пакеты в `.agents/skills/specsmd.*/SKILL.md` + `user-invocable`. Тогда pi получит `/skill:specsmd-fire`, omp — `/skill:specsmd-fire` тоже (оба читают `.agents/skills/`). Именно так spec-kitty поддерживает pi — можно подсмотреть рендеринг в `spec-kitty/src/specify_cli/skills/command_renderer.py` (build_frontmatter: name/description/user-invocable; description из frontmatter команды → первого предложения Purpose → первого абзаца → fallback).

### Рекомендация

Для своих проектов — вариант 1 немедленно (omp уже работает, pi — копирование промптов). Если хотим_contribить в specs.md — вариант 2 (два установщика, ~50 строк, формат команд совместим). Skills-first имеет смысл, только если нужна авто-активация по контексту задачи; для SDD-процессов с явными фазами явный вызов честнее (и наш принцип: релевантный текст по задаче, не мёртвый груз — description-роутинг skills как раз может грузить лишнее).

## Источники

- spec-kitty клон: `packs/built-in/missions/mission-steps/research/{methodology,gathering}/prompt.md` (floor≠target, events-not-rows), `src/runtime/next/runtime_bridge_cores.py` (_evaluate_gathering_guard, fail-closed), `src/runtime/next/decision.py` (DecisionKind, Decision.guard_failures/guard_failure_paths, канонический while-цикл), `src/specify_cli/cli/commands/lifecycle.py` (specify: --mission-type, interview FR-002), `docs/guides/how-to/harnesses/pi-tui.md` (/skill:spec-kitty.*, «Pi is a skill host, not a slash-command host»), `src/specify_cli/skills/command_renderer.py` (frontmatter name/description/user-invocable, приоритет description)
- specs.md клон: `src/flows/fire/commands/fire.md` (команда-активатор ~30 строк), `src/flows/fire/agents/orchestrator/skills/route/SKILL.md` (file-system-is-truth, маршрутизация по состоянию), `src/flows/fire/agents/builder/skills/run-execute/scripts/*.cjs` (детерминированные скрипты), `src/lib/installers/ToolInstaller.js` + `ClaudeInstaller.js` (how to add installer), `src/flows/simple/commands/agent.md` ($ARGUMENTS)
- pi клон: `packages/coding-agent/docs/skills.md` (Agent Skills spec, `/skill:name args`, disable-model-invocation, discovery roots, валидация), `docs/prompt-templates.md` ($1/$@/${1:-default}, argument-hint), `docs/slash-commands.md`, `docs/extensions.md` (registerCommand без LLM, события до/после, jiti)
- omp клон: `docs/slash-command-internals.md` (провайдеры и приоритеты команд, .agents/commands не сканируется), `docs/skills.md` (провайдеры skills, skill://), `docs/hooks.md` (—hook алиас, .omp/hooks/pre, tool_call block), `docs/context-files.md`
