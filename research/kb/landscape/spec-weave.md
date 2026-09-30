# SpecWeave: spec-first AI development с cross-tool handoff

| Параметр | Значение |
|---|---|
| Статус | draft |
| Обновлено | 2026-09-30 (по README v3.0.0 от 2026-09-25 и репозиторию) |

## Что это

**SpecWeave** — spec-first фреймворк для AI-разработки: «describe a feature → AI creates spec + plan + tasks, builds autonomously, syncs to GitHub/JIRA». Позиционирование: «Change agents. Keep the thread.» TypeScript, MIT, Node.js 20.12.0+. Автор: Anton Abyzov. Статус на 09.2026: 164 звёзды, 21 форк (молодой, нишевой — против 126K OpenSpec и 139K Spec Kit; при этом активен: 600+ increments, 538+ releases).

## Ключевые концепции

### Increment как единица работы

Одна папка `.specweave/increments/NNNN-slug/` на фичу: один читаемый файл `spec.md` (Problem, Scope, Acceptance Criteria, Approach, Tasks) + append-only `ledger.jsonl` (claims, evidence, handoffs, test evidence). Increments из 2.x с `tasks.md` работают без миграции. Это реализация change-based модели (ср. OpenSpec `changes/`, Spec Kitty `kitty-specs/`).

### Cross-tool handoff (дифференцирующая фича)

```
you (in Claude, account 1):   hand off
you (in Codex, or account 2): pick up
```

`specweave handoff`: releases task claims, записывает причину остановки, пушит branch + snapshot незакоммиченных правок. `specweave pickup` в любом другом инструменте/аккаунте/машине/cloud-сессии: подтягивает работу и печатает следующую задачу с acceptance criteria. **Auto-handoff**: при достижении 90% 5-часового/недельного лимита плана — автоматический handoff (Claude Code через status line, Codex через Stop hook; `--at 85` для порога). Это прямой ответ на «AI forgets everything between sessions» и на экономику внимания/контекста (`../principles/attention-economy.md`) — durable context переносится между инструментами и аккаунтами.

### Project memory, переносимая с кодом

`.specweave/memory/` — тот же формат, что Claude Code Projects `MEMORY.md` + один файл на факт, но **закоммичен** — Codex, Grok и вторая подписка Claude стартуют с тех же решений. (Project memory в claude.ai привязана к одному аккаунту; SpecWeave переносит её с кодом.)

### 11 skills (один источник для всех агентов)

`increment` (план в один spec.md), `do` (claim → implement → close with evidence), `auto` (unattended loop), `team` (worktree per agent, claims через ledger), `review` (fresh-context adversarial review, findings cite `path:line`), `done` (verify + review check + complete), `handoff`, `sync` (GitHub first-class; Jira, Azure DevOps opt-in), `project` (shared goals/artifacts/briefs), `brainstorm` (framed alternatives → pick), `jev` (closed-set decisions ~250 ms). CLI — продукт, работает в любом инструменте и в CI; skills — тонкий слой к агентам (`/sw:<name>` в Claude Code, `sw-<name>` в `.claude/skills/` и `.agents/skills/`).

### Evidence и closure gate

`specweave task done --run "<test>"` **отказывает при падающем тесте** и сохраняет exit code + output tail в ledger — реализация принципа `../principles/invariants-and-gates.md` (блокирующий gate, не advisory; ср. критику OpenSpec `verify`, не блокирующий archive). `verify` запускает test/lint/build; fresh-context review цитирует `path:line`. Acceptance criteria закрываются выполнением задач, не галочками («nobody ticks boxes»). `specweave report` — HTML-таймлайн «кто что сделал» из ledger.

### Прочее

LSP code intelligence (198× faster than grep, 0 false positives). Dashboard из локальных файлов без model calls. Enterprise: compliance audit trails, brownfield analysis, multi-repo workspaces. Skills ecosystem: verified-skill.com (105K+ verified skills) + vskill (package manager: security scanning 52 attack patterns, 49 agent platforms, skill evals).

## Сильные и слабые стороны

Сильные: cross-tool handoff (уникальный на дату исследования — ни Spec Kit, ни OpenSpec, ни BMAD не переносят работу между вендорами и аккаунтами); блокирующий evidence-gate (`done --run` отказывает при fail); append-only ledger (auditable, claims arbitrated); memory, переносимая с кодом; CLI-first (работает в CI и любом harness).

Слабые / риски: молодой и нишевый (164 звезды — bus factor и устойчивость проекта под вопросом, ср. критику OpenSpec bus factor = 1 в `sdd-criticism.md` §2.10); автор — один мейнтейнер (Anton Abyzov); handoff-модель требует дисциплины ветвления (branch + snapshot); отсутствие независимых production-отчётов на дату исследования (портфолио автора — usage examples, «not controlled productivity measurements»).

## Позиционирование в ландшафте

| Способность | Spec Kit | OpenSpec | BMAD | SpecWeave |
|---|---|---|---|---|
| Cross-tool handoff | — | — | — | **Yes** |
| Блокирующий evidence-gate | phase gates | advisory | — | **`done --run` refuses fail** |
| Append-only ledger | — | — | — | **Yes** |
| Memory с кодом | constitution | AGENTS.md | durable context | **`.specweave/memory/`** |
| Зрелость | 139K | 126K | 48K | 164 |

Ближайший аналог handoff-концепции: нет (уникальна). По change-based модели — OpenSpec (`changes/`), по evidence-gate — Spec Kitty Research Mission (guards), по memory — BMAD durable context.

## Источники

- Site: https://spec-weave.com | GitHub: https://github.com/anton-abyzov/specweave | npm: https://www.npmjs.com/package/specweave | verified-skill: https://verified-skill.com | vskill: https://www.npmjs.com/package/vskill
- Входные материалы inbox: `README.md` (бэклог F)
- Связанные KB: `sdd-tools-overview.md`, `spec-kitty-research.md`, `../principles/invariants-and-gates.md`, `../principles/attention-economy.md`
