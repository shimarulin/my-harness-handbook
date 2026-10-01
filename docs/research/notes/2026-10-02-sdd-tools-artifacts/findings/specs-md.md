---
id: findings-specs-md-20261002
type: research-note
status: final
created: 2026-10-02
updated: 2026-10-02
topics: [specs-md, artifacts, flows, integration]
author: agent:SpecsMdResearch
---

# Findings: specs.md (fabriqaai/specs.md)

## Что это

AI-native spec-driven development FRAMEWORK с 4 pluggable flows (Ideation, Simple, FIRE, AI-DLC). Не code generator — устанавливает markdown-агентов, slash-команды и схемы артефактов в репозиторий; ваш AI-инструмент (Claude Code, Cursor, Copilot) исполняет их. «Methodology distribution system».

## Установка и команды

```bash
npx specsmd@latest install   # интерактив: выбор инструментов (12) → выбор flow (4) → копирование
```

CLI: `install`, `uninstall`, `dashboard`, `dashboard-cli`.

## Артефакты при установке

| Путь | Что |
|---|---|
| `.specsmd/manifest.yaml` | `{flow, version, installed_at, tools}` |
| `.specsmd/<flow>/agents/` | agent.md файлы (YAML frontmatter: name, description, version) |
| `.specsmd/<flow>/agents/<agent>/skills/<skill>/SKILL.md` | skill definitions (frontmatter + XML body) |
| `.specsmd/<flow>/agents/<agent>/skills/<skill>/templates/*.hbs` | Handlebars templates |
| `.specsmd/<flow>/memory-bank.yaml` | схема flow: artifact_root, structure, naming, ownership, execution modes |
| `.claude/commands/specsmd-*.md` | slash-команды (или .cursor/rules/, .github/agents/ и т.д.) |

**Важно**: артефакты runtime (`.specs-fire/`, `specs/`, `memory-bank/`) создаются при первом `project-init`, не при install.

## Артефакты по flows

### Ideation Flow (best fit для нас)

```
.specs-ideation/sessions/{topic-slug}-{YYYYMMDD}/
├── session.yaml              # {phase, favorites, scores, domains_used}
├── spark-bank.md             # идеи по темам, frontmatter: {session, topic, phase, created, total_ideas, ...}
├── flame-report.md           # Six Hats + Impact×Feasibility matrix
└── concept-briefs/{name}.md  # vision (Dreamer), plan (Realist), risks (Critic)
```

- Spark: 5 идей/batch, 12-domain anti-bias wheel, 6-step deep thinking.
- Flame: Six Hats + Impact×Feasibility → shortlist 3–5.
- Forge: Disney Creative Strategy (Dreamer → Realist → Critic) → concept briefs.
- **Zero checkpoints** — non-blocking.

### Simple Flow

```
specs/{feature-name}/
├── requirements.md   # user stories + EARS acceptance criteria (NO frontmatter)
├── design.md         # architecture, components, data models
└── tasks.md          # numbered checklist with requirement refs
```

3 phase gates (explicit approval). Code-feature-oriented.

### FIRE Flow

```
.specs-fire/
├── state.yaml                # CENTRAL STATE: project, workspace, intents, work_items, runs
├── standards/
│   ├── constitution.md       # universal policies (git, PR, security) — never overridden
│   ├── tech-stack.md
│   ├── coding-standards.md
│   └── testing-standards.md
├── intents/{intent-id}/
│   ├── brief.md              # {id, title, status, created} + Goal, Users, Problem, Success Criteria
│   ├── work-items/{id}.md    # acceptance criteria
│   └── work-items/{id}-design.md   # design doc (Validate mode)
└── runs/{run-id}/
    ├── run.md                # log
    ├── plan.md               # implementation plan (all modes)
    ├── test-report.md
    ├── review-report.md
    └── walkthrough.md        # auto-generated change documentation
```

- Adaptive checkpoints: autopilot (0) / confirm (1) / validate (2) по complexity × autonomy_bias.
- Hierarchical standards: root constitution.md always inherited; module overrides.
- Walkthrough generation after every run.

### AI-DLC Flow

```
memory-bank/
├── project.yaml
├── intents/{NNN}-{name}/
│   ├── requirements.md
│   ├── system-context.md
│   ├── inception-log.md
│   └── units/{UUU}-{name}/stories/{SSS}-{slug}.md
├── bolts/{BBB}-{name}/
│   ├── bolt.md
│   ├── ddd-01-domain-model.md
│   ├── ddd-02-technical-design.md
│   └── ddd-03-test-report.md
├── standards/
│   ├── tech-stack.md
│   ├── coding-standards.md
│   └── decision-index.md     # ADR index
└── story-index.md            # global story index
```

Full AWS AI-DLC + DDD. 4 agents, comprehensive checkpoints. Для software teams.

## Frontmatter и метаданные

| Артефакт | Frontmatter | Наше соответствие |
|---|---|---|
| agent.md / SKILL.md | `{name, description, version}` | ❌ Нет (наш: id, type, status, created, updated, topics, author) |
| spark-bank.md | `{session, topic, phase, created, total_ideas, ...}` | ⚠️ Частичное (нет updated, topics, author, наш id format) |
| fire brief.md | `{id, title, status, created}` | ⚠️ Частичное (нет updated, topics, author) |
| simple requirements.md | **Нет frontmatter** | ❌ |
| session.yaml / state.yaml | Pure YAML (не frontmatter) | ⚠️ Другой формат |

Timestamps: ISO 8601 с timezone (`YYYY-MM-DDTHH:MM:SSZ`). Наш: date-only `YYYY-MM-DD` + ms-precision id.

## Source code structure

- `src/bin/cli.js` — commander CLI.
- `src/lib/installer.js` — interactive install.
- `src/lib/installers/` — 12 tool installers (Claude, Cursor, Copilot, ...).
- `src/flows/<flow>/` — flow content: agents/, commands/, shared/, memory-bank.yaml.
- `src/lib/dashboard/` — per-flow state readers.

**Extensibility**: новый flow = `src/flows/<name>/` + register in constants.js + dashboard reader. Agent/skill behavior = pure markdown — редактируется после install. Handlebars templates полностью перезаписываемы.

## Интеграция с нашим репозиторием

### Конфликты

| Конфликт | Severity | Разрешение |
|---|---|---|
| `docs/` — нет конфликта | ✅ Нет | specs.md не пишет в `docs/` (verified in installer.js) |
| Root clutter: `.specsmd/` + `.specs-ideation/` (или `specs/`, `memory-bank/`) | 🟡 Moderate | Hidden dirs low-noise; `specs/` и `memory-bank/` — visible, confusing для documentation repo |
| `specs/` semantic clash | 🟡 Moderate | Рядом с `content/` и `docs/` — readers mistake for handbook corpus |
| `memory-bank/` semantic clash | 🟡 Moderate | Overlaps with our `docs/` workspace conceptually |
| `standards/` overlap (FIRE/AI-DLC) | 🟡 Moderate | `constitution.md`, `tech-stack.md` overlap with `tools/process-framework/conventions/` — two sources of truth |
| Frontmatter mismatch | 🔴 High | Generated artifacts violate our conventions |

### Fit assessment по flows

| Flow | Fit | Почему |
|---|---|---|
| **Ideation** | ✅ Best | Self-contained sessions, non-code artifacts (ideas, evaluations, briefs) map to `docs/research/` и `docs/notes/`. Concept briefs → `docs/plans/`. Zero checkpoints. |
| Simple | ❌ Poor | Code-feature-oriented (EARS, implementation tasks). `specs/` root clash. No frontmatter. |
| FIRE | 🟡 Moderate | Intent→WorkItem→Run attractive for doc work. Walkthrough useful. But state.yaml code-shaped, standards/ duplicates our conventions/, brownfield assumes codebases. |
| AI-DLC | ❌ Poor | DDD bolts, deployment, mob rituals — software teams. `memory-bank/` root. Massive overkill. |

### Рекомендация

**Не устанавливать as-is в repo root.** Если adopted:
1. Запустить installer в scratch dir.
2. Cherry-pick markdown agent definitions в `tools/process-framework/` как reference.
3. Ideation flow's Spark/Flame/Forge skill files + shared protocols (anti-bias.md, deep-thinking.md) — copy и adapt с нашим frontmatter.
4. FIRE's `.hbs` template approach — adopt pattern, но с нашим frontmatter schema.
5. Walkthrough generation — pattern для `docs/notes/` (auto-documenting agent work sessions).

## Ключевые цитаты

- Installer source: `src/lib/installer.js` — no `docs/` references.
- Flow schemas: `.specsmd/<flow>/memory-bank.yaml` — declarative artifact_root, paths, naming, ownership.
- Templates: `src/flows/<flow>/agents/<agent>/skills/<skill>/templates/*.hbs` — Handlebars, overridable.

## Источники

- GitHub: https://github.com/fabriqaai/specs.md
- npm: https://www.npmjs.com/package/specsmd
- Research agent: SpecsMdResearch (task, 7m27s)
