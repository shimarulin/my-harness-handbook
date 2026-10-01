# Superpowers: обзор и место в ландшафте

## Коротко

**[Superpowers](https://github.com/obra/superpowers)** — самый популярный инструмент в нише (293k звёзд, 26.3k форков) — это **methodology как набор composable skills**, которые срабатывают автоматически в AI-агенте. В отличие от Spec Kitty (mission types) и specs.md (flows), Superpowers не требует выбора workflow — skills сами определяют, когда активироваться.

**Для research-задачи:** Superpowers имеет **brainstorming skill** — Socratic design refinement, который покрывает начальную research/ideation фазу. Но это менее структурированно, чем Research Mission в Spec Kitty или Ideation Flow в specs.md.

---

## Как работает Superpowers

### Ключевой принцип: автоматическая активация

Из README【turn1fetch0】:

> "It starts from the moment you fire up your coding agent. As soon as it sees that you're building something, it *doesn't* just jump into trying to write code. Instead, it steps back and asks you what you're really trying to do."

> "And because the skills trigger automatically, you don't need to do anything special. Your coding agent just has Superpowers."

Это фундаментальное отличие от других инструментов:
- **Spec Kitty:** ты запускаешь `/spec-kitty.specify --mission research`
- **specs.md:** ты выбираешь flow при install
- **Superpowers:** просто начинаешь работать — skills сами определяют момент

### Основной workflow

Из README【turn0fetch0】:

```
1. brainstorming        → Socratic design refinement, уточнение идеи, exploring alternatives
2. using-git-worktrees → Изолированное workspace, чистый baseline
3. writing-plans        → Задачи по 2-5 минут, exact file paths, verification steps
4. subagent-driven-development / executing-plans → Subagent на задачу
5. test-driven-development → RED-GREEN-REFACTOR enforcement
6. requesting-code-review   → Ревью против плана
7. finishing-a-development-branch → Merge/PR/cleanup
```

> "The agent checks for relevant skills before any task. Mandatory workflows, not suggestions."

### Skills Library

| Категория | Skills | Что делает |
|---|---|---|
| **Testing** | `test-driven-development` | RED-GREEN-REFACTOR, deletes code written before tests |
| **Debugging** | `systematic-debugging`, `verification-before-completion`, `diagnosing-superpowers` | 4-phase root cause, verification, session diagnostics |
| **Collaboration** | **`brainstorming`**, `writing-plans`, `executing-plans`, `dispatching-parallel-agents`, `requesting-code-review`, `receiving-code-review`, `using-git-worktrees`, `finishing-a-development-branch`, `subagent-driven-development` | Полный delivery lifecycle |
| **Meta** | `writing-skills`, `using-superpowers` | Создание новых skills, introduction |

### Поддержка harnesses — 15+ инструментов

| Harness | Тип установки |
|---|---|
| Claude Code | Official plugin marketplace |
| Antigravity | `agy plugin install` |
| Codex App / CLI | Official Codex marketplace |
| Cursor | `/add-plugin superpowers` |
| Devin CLI | `devin plugins install` |
| Factory Droid | `droid plugin install` |
| Gemini CLI | `gemini extensions install` |
| GitHub Copilot CLI | `copilot plugin install` |
| Grok Build CLI | Official Grok marketplace |
| Kimi Code | Plugin marketplace |
| OpenCode | Custom install |
| Pi | `pi install git:...` |
| Qwen Code | `qwen extensions install` |
| Hermes Agent | `hermes plugins install` |
| Muse | Native plugin |

Это **самая широкая поддержка harnesses** среди всех рассмотренных инструментов.

### Философия

Из README【turn0fetch0】:
- **Test-Driven Development** — write tests first, always
- **Systematic over ad-hoc** — process over guessing
- **Complexity reduction** — simplicity as primary goal
- **Evidence over claims** — verify before declaring success

---

## Research в Superpowers

### Brainstorming skill

Из описания【turn0fetch0】:

> "brainstorming - Activates before writing code. Refines rough ideas through questions, explores alternatives, presents design in sections for validation. Saves design document."

Это research/ideation фаза:
- **Когда:** автоматически, при начале новой задачи
- **Что делает:** Socratic questioning, уточнение rough idea, exploring alternatives
- **Output:** design document

**Сравнение с аналогами:**

| Инструмент | Research механизм | Подход |
|---|---|---|
| **Superpowers** | `brainstorming` skill | Socratic, автоматический, встроен в любой workflow |
| **Spec Kitty** | `research` mission type | Формальный state machine: scoping→methodology→gathering↔synthesis→output, evidence-gated |
| **specs.md** | `Ideation Flow` | Структурированный: Spark→Flame→Forge, anti-bias engine, 12-domain wheel |

**Разница в подходе:**
- Superpowers: "задай правильные вопросы" (Socratic method)
- Spec Kitty: "собери evidence по методологии" (systematic research)
- specs.md: "сгенерируй разнообразные идеи" (creative brainstorming)

### Чего НЕ хватает Superpowers для полноценного research

1. **Нет evidence tracking** — нет `evidence-log.csv`, нет source register
2. **Нет formal methodology** — нет "минимум 3 источника для synthesis"
3. **Нет iterative gathering loop** — нет `gathering ↔ synthesis` цикла
4. **Нет comparison matrices** — нет структурированного сравнения
5. **Нет findings document** — нет отдельного `findings.md` с evidence synthesis

Brainstorming — это про **уточнение идеи перед началом работы**, не про **систематическое исследование**.

---

## Полное сравнение: Superpowers vs Spec Kitty vs specs.md vs GitHub Spec Kit

| Критерий | Superpowers | Spec Kitty | specs.md | GitHub Spec Kit |
|---|---|---|---|---|
| **Звёзды** | 293k | 1.7k | — (npm) | 139k |
| **Язык** | TypeScript/JS (skills) | Python | Node.js | Python |
| **Архитектура** | Composable skills | Mission types | Pluggable flows | Templates + presets |
| **Research поддержка** | ⚠️ Brainstorming only | ✅ Full research mission | ✅ Ideation Flow | ❌ Нет |
| **Evidence tracking** | ❌ | ✅ CSV evidence log | ⚠️ Session artifacts | ❌ |
| **Автоактивация** | ✅ Skills trigger automatically | ❌ Explicit commands | ❌ Explicit commands | ❌ Explicit commands |
| **State machine** | ❌ Skills не имеют state | ✅ Evidence-gated | ⚠️ Per-flow | ⚠️ Basic |
| **TDD enforcement** | ✅ Deletes code before tests | ⚠️ Per mission | ❌ | ❌ |
| **Subagent orchestration** | ✅ Per-task subagents | ✅ Per-WP worktrees | ❌ | ❌ |
| **Git worktrees** | ✅ Isolated branches | ✅ Per-WP isolation | ❌ | ❌ |
| **Code review** | ✅ Mandatory between tasks | ✅ Per-WP | ❌ | ❌ |
| **Harnesses** | 15+ | 10+ | 11+ | 3-4 |
| **Масштаб процессов** | Implicit (skills compose) | ✅ 4 mission types | ✅ 4 flows | ⚠️ Presets |

### Уникальные фишки каждого

**Superpowers:**
- Skills срабатывают автоматически (zero-friction)
- TDD enforcement (deletes code written before tests)
- 15+ harnesses — самая широкая поддержка
- Diagnosing-superpowers (session debugging)
- Subagent-driven development с per-task review

**Spec Kitty:**
- Research mission с evidence-gated transitions
- CSV evidence log с confidence ratings
- 4 mission types (research, software-dev, plan, documentation)
- Kanban board + dashboard
- Per-feature missions (разные миссии в одном проекте)

**specs.md:**
- Ideation Flow (Spark→Flame→Forge)
- Anti-bias engine (12-domain wheel)
- 3 flows для разных уровней формальности
- VS Code extension + Web/CLI dashboard
- AI-DLC с полным DDD

**GitHub Spec Kit:**
- Наиболее зрелый (139k звёзд, GitHub официальный)
- Presets + extensions
- AGENTS.md стандарт
- Простейший entry point

---

## Для вашего проекта: как Superpowers вписывается

### Где Superpowers силён

1. **Если нужен TDD-first процесс** — Superpowers enforcement строже всех
2. **Если много разных harnesses** — 15+ поддержка, один и тот же behavior везде
3. **Если нужна нулевая фрикция** — skills срабатывают без команд
4. **Если нужен subagent orchestration** — per-task subagents с review

### Где Superpowers НЕ закрывает вашу задачу

Для **research knowledge management**:
- Нет evidence tracking
- Нет systematic methodology
- Нет iterative research loop
- Нет findings/comparison artifacts
- Нет cross-mission knowledge accumulation

Brainstorming покрывает **начальную** фазу (уточнение идеи), но не **систематическое исследование**.

### Комбинация инструментов

**Наиболее полная комбинация для вашего сценария:**

```
Superpowers (delivery + TDD + subagents)
    +
Spec Kitty Research Mission (systematic research + evidence)
    +
Собственные extensions (knowledge accumulation + topic navigation)
```

**Или:**

```
Superpowers (brainstorming + writing-plans + TDD)
    +
specs.md Ideation Flow (структурированный ideation)
    +
Spec Kitty (research missions для глубокого research)
```

**Или минимально:**

```
Superpowers alone — если research ограничивается brainstorming перед задачей
```

---

## Паттерны Superpowers для заимствования

Даже если не adopting Superpowers целиком, эти паттерны ценны:

1. **Composable skills** — вместо жёстких workflows, набор композируемых behaviors
2. **Auto-triggering** — skills определяют момент, не пользователь
3. **Mandatory enforcement** — "deletes code written before tests" — это enforcement, не suggestion
4. **Session diagnostics** — `diagnosing-superpowers` — анализ того, что пошло не так
5. **Per-harness plugins** — один набор skills, разные plugin wrappers для каждого harness
6. **Marketplace distribution** — установка через официальные marketplace каждого harness

---

## Ссылки

- **Superpowers:** [https://github.com/obra/superpowers](https://github.com/obra/superpowers) — 293k звёзд
- **Автор:** Jesse Vincent ([obra](https://github.com/obra)), [Prime Radiant](https://primeradiant.com)
- **Discord:** [Superpowers community](https://discord.gg/superpowers)
- **Spec Kitty:** [https://github.com/spec-kitty/spec-kitty](https://github.com/spec-kitty/spec-kitty) | [Mission System](https://github.com/spec-kitty/spec-kitty/blob/main/docs/architecture/mission-system.md)
- **specs.md:** [https://github.com/fabriqaai/specs.md](https://github.com/fabriqaai/specs.md) | [Ideation Flow](https://specs.md/ideation-flow/overview)
- **GitHub Spec Kit:** [https://github.com/github/spec-kit](https://github.com/github/spec-kit)
