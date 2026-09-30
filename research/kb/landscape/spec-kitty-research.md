# Spec Kitty Research Mission и specs.md Ideation Flow: research как фаза delivery

| Параметр | Значение |
|---|---|
| Статус | draft |
| Обновлено | 2026-09-30 (по материалам исследования 09.2026; Spec Kitty активно развивается — перепроверять в фазе 6) |

## Что это

Два инструмента, закрывающих research-функцию внутри SDD-доставки: **Spec Kitty** (форк Spec Kit с mission-архитектурой) имеет полноценный Research Mission — evidence-gated state machine с машинными проверками; **specs.md** покрывает pre-research brainstorming через Ideation Flow. Вывод исходного исследования после пересмотра позиции: **research — не отдельная ниша, а фаза software delivery**; собственную research-систему строить с нуля не обязательно — варианты adopt/adapt с заимствованием уникальных фич собственной архитектуры (cross-mission learnings, topic-views).

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
- Полный разбор альтернатив и статус ландшафта: `sdd-tools-overview.md`; пересмотр в фазе 6 (spec-weave, свежий поиск).

## Источники

- Spec Kitty: https://github.com/spec-kitty/spec-kitty | https://docs.spec-kitty.ai | https://spec-kitty.ai
- specs.md: https://github.com/fabriqaai/specs.md | https://www.npmjs.com/package/specsmd
- Входные материалы inbox: `research-and-notes/research-process.md` (строки 2230–3019), `README.md` (бэклог F)
- Связанные KB: `../methods/research-knowledge.md`, `../principles/content-stays-virtual-structure.md`, `sdd-tools-overview.md`
