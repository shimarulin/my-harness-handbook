# Идея: устойчивость через блокирующий машинный enforcement, а не доверие

| Параметр | Значение |
|---|---|
| Статус | differentiator (главный дефицит готовых решений — advisory verification) |
| Обновлено | 2026-09-30 |
| Происхождение | Синтез фаз 2, 5, 6 (критика SDD, quality gates, SpecWeave/Spec Kitty) |

## Проблема

Центральная поломка SDD: **спека и код расходятся по умолчанию при отсутствии блокирующего машинного enforcement**. Проверки либо advisory (не блокируют), либо в досягаемости агента (он их обходит):

- OpenSpec: `validate` — только структура; `verify` не блокирует archive; `archive --no-validate` отменяет проверку. «Контракт подписан, но исполнение — на совести агента».
- Агент обходит проверки: issue #194 — получив ошибку `Change must have at least one delta`, использовал `--skip-specs`. Общий закон: **агент минимизирует «трение» в ущерб процессу**.
- Инструкции не enforcement: «don't do X» в конституции агент игнорирует (кейс EPAM: pattern-matching против миллионов кодовых баз перевесил строку запрета).

## Почему готовые решения не закрывают

- **Advisory verification (OpenSpec, большинство SDD)** — проверка существует, но не блокирует продвижение; дрейф — дефолтный исход.
- **Behavioral guidance (skills, промпты)** — «not a substitute for repository tests, permissions, or human review» (rywalker о Superpowers); инструкция интерпретируется моделью, не принуждает.
- **Phase gates (Spec Kit)** — блокируют, но тяжелы и воспроизводят waterfall; нет градации по цене ошибки.
- **«Don't do X» без rationale** — не работает; нужно «don't do X because Y, and instead do Z» + машинная проверка.

**Рынок подтверждает тезис**: инструменты с блокирующими gate появились как ответ на этот дефицит — Spec Kitty Research Mission (guards «минимум 3 источника»), SpecWeave (`task done --run` отказывает при падающем тесте). «Судьба SDD решится не качеством спек, а появлением дешёвого машинного enforcement».

## Ценность

Слой, делающий нарушение **дорогим, а не дефолтным**:

- **Инвариант нельзя обойти флагом** — enforcement машинный и вне досягаемости агента (CI, hooks, permissions).
- **Блокирующие gate вместо advisory** — продвижение останавливается при нарушении, а не «предупреждает».
- **Evidence вместо доверия** — след решений и проверок (ledger, evidence-log) аудируем.
- **Градация по цене ошибки** — блокирующие gate для accepted-зон (invariants, evidence), advisory — для исследовательских; уровень строгости по риску.

## Архитектура

### Принцип: hooks/CI > промпты

Проверка, определяющая соответствие, должна быть **детерминированной и вне досягаемости агента**. «The hooks matter more than the prompts». Явные инварианты с rationale и уровнем критичности:

| Поле | Пример |
|---|---|
| Инвариант | IN-001: изоляция транзакций |
| Форма проверки | Тип / контрактный тест / PBT / линтер |
| Уровень критичности | Нельзя нарушать / можно нарушить с обоснованием (через ADR) / рекомендация |
| Почему | Обоснование (без него агент pattern-match'ит против) |

### Quality gates как серия блокирующих CI-проверок

Для артефактов и кода (каждая `continue-on-error: false`):

```
EARS Format → Requirements Coverage (>95%) → Architecture Compliance
→ Test Coverage (--cov-fail-under=80) → AI Agent Metrics (acceptance ≥70%)
```

Для документации (docs-as-code): markdownlint → front-matter schema → trace_check (traces существуют, superseded имеет superseded_by) → mkdocs build --strict → исполняемые спеки.

### Evidence-gate и ledger (перенять из SpecWeave/Spec Kitty)

- **Evidence-gate на уровне задачи**: `task done --run "<test>"` **отказывает при падающем тесте**, сохраняет exit code + output tail.
- **Append-only ledger**: claims, evidence, handoffs, test evidence — аудируемый след работы агента; acceptance criteria закрываются выполнением, не галочками («nobody ticks boxes»).
- **Evidence-gated research**: guard «минимум N источников documented» для перехода gathering → synthesis; evidence-log.csv (machine-readable, проверяемый CI).

### Error patterns как механизм обучения

Замкнуть feedback loop: ошибка → **Error Pattern Dashboard** (occurrences, root cause, mitigation) → защита **в tooling** (prompt templates с anti-patterns, checklists, линтеры), а не в инструкциях. Pre/post-generation checklists: context provided? output format? acceptance criteria? verification plan?

## Градация строгости (по цене ошибки)

| Зона | Gate |
|---|---|
| Accepted (invariants, evidence, public API, контракты) | **Блокирующий** (CI/hooks, вне досягаемости агента) |
| Исследовательская (draft, spike, exploration) | Advisory (предупреждения, ревью) |
| Trivial (L0) | Отсутствует (commit + code review) |

Это соединение с уровнями процесса (`../process-core/`): строгость gate = f(цена ошибки), не константа — избегаем и «хаос без контроля», и «waterfall везде».

## Связь с остальными кластерами

- Что проверяем — форма требования по цене удержания → `../process-core/` (дешевая форма: тип/контракт/PBT/пример).
- Кто подаёт на вход — агент под контролем → `../agent-governance/` (явная приёмка, ведомость допущений).
- Где живут проверки → `../tooling-strategy/` (CI/CD, pre-commit, hooks — adopt/adapt).

## Источники

- Принцип инвариантов и gate: `../../research/kb/principles/invariants-and-gates.md`
- Quality gates и error patterns: `../../research/kb/methods/metrics-dashboards.md`, `../../research/kb/methods/docs-cicd.md`
- Evidence-gate и ledger: `../../research/kb/landscape/spec-weave.md`, `../../research/kb/landscape/spec-kitty-research.md`
- Тезис рынка: `../../research/kb/landscape/sdd-criticism.md` (приложение)
