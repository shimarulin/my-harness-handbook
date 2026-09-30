# Глава 9. Операционка

Как процесс живёт в ежедневной работе: CI/CD для документации, метрики, обучение, review, жизненный цикл артефактов. Это слой, отличающий «процесс на бумаге» от работающего. Детали — `../research/kb/methods/docs-cicd.md`, `metrics-dashboards.md`, `review-collaboration.md`, `versioning-lifecycle.md`, `training-onboarding.md`.

## 9.1. Docs-as-Code CI/CD

Принцип: **Docs = Code** — те же гейты, линтинг, валидация и деплой, что для кода. Шесть этапов:

```
Push/PR → [Lint] → [Validate] → [Render] → [Build] → [Test Specs] → [Deploy]
```

- **Lint**: markdownlint (MD013/033/041 off, MD024 siblings), yamllint.
- **Validate**: front-matter JSON schema (required `id, type, status, created, title`), `trace_check.py` (все `traces` существуют, superseded имеет `superseded_by`, статусы валидны, ID уникальны), `openspec validate`.
- **Render**: PlantUML/Mermaid → SVG **в CI, не в git** (диаграммы не коммитятся).
- **Build**: `mkdocs build --strict` (битые ссылки = ошибка).
- **Test Specs**: Gauge / Cucumber (исполняемые спеки = living documentation).
- **Deploy**: GitHub Pages (только main).

Pre-commit hooks — локальный gate до CI (markdownlint, yamllint, frontmatter-validate, plantuml-check, trace-check). Минимальный пайплайн (старт): lint + trace_check + mkdocs build --strict; расширять по мере появления диаграмм, спек, деплоя.

## 9.2. Метрики и обучение на ошибках

Принципы: измерять важное (не vanity); обязательный feedback loop (Данные → Анализ → Действия → Проверка); обучение на ошибках (patterns выявляются автоматически, защита в tooling, не в инструкциях); прозрачность (ретроспективы на данных).

Три категории (`../research/kb/methods/metrics-dashboards.md` — полные таблицы с target/alert):
- **Process**: cycle time по этапам, requirements completeness (> 95%), ADR coverage (100%), documentation freshness (< 30 дней), cross-reference integrity (100%).
- **AI-Agent**: task completion rate (> 80%), first-time quality (> 70%), hallucination rate (< 5%), token efficiency, architecture drift (0).
- **Resource**: review overhead (< 30%), documentation debt (< 10% dev time), token cost.

**Error Pattern Dashboard** (90 дней): pattern → occurrences / root cause / mitigation. Prevention: prompt templates с anti-patterns (❌ «fast» → ✅ «< 200ms»), pre/post-generation checklists, 5 CI quality gates (EARS → coverage → architecture → tests → AI metrics, все блокирующие). Каденс: weekly review (30 мин) → monthly retrospective (1 ч) → quarterly planning (2 ч).

## 9.3. Review и коллаборация

Принцип: **review is collaboration, not gatekeeping**; explicit expectations; async-first; time-boxed (1 неделя RFC, 2 дня ADR).

Четыре workflow: Lightweight (1 ревьюер, 1–2 дня — bug fixes), Standard (2: domain expert + peer, 2–5 дней — requirements/ADR/approach), Formal (3+, 1–2 недели — RFC/PRD/major), ARB (5–7 members, 2–4 недели — cross-team/compliance + post-implementation review через 3 мес). Паттерны approval: unanimous consent (RFC, major), majority vote (standard ADR), lazy consensus (minor — с осторожностью, см. [главу 10](10-open-questions.md)), designated approver (time-sensitive). Feedback — SBI-модель (Situation → Behavior → Impact), не оценочная критика.

## 9.4. Жизненный цикл артефактов

Три типа (`../research/kb/methods/versioning-lifecycle.md`):
- **Immutable Decisions** (ADR, RFC): Approved → только **supersede** (новый ADR + старый `Superseded by`, оба одним коммитом); никогда не редактируются.
- **Living Specifications** (requirements, approach): Approved → Active → изменения через **amendment process** (proposal → review → apply с bump версии и amendment log → update related).
- **Product Artifacts** (PRD): Approved → Frozen.

Deprecation: 3–6 мес notice → migration guide → monitor → sunset (410 Gone) → archive (read-only). Анти-паттерн «eternal drafts»: time-box draft 30 дней → auto-archive. Semver для документации: MAJOR (breaking) / MINOR (новые артефакты) / PATCH (исправления).

## 9.5. Обучение и онбординг

Принцип: **learning by doing (70% practice, 30% theory)**. Три уровня: L1 Foundation (все, 4 ч — PS, EARS, ADR, мини-проект), L2 Practitioner (developers, 8 ч — Approach…Implementation, AI integration), L3 Expert (architects/tech leads, 8 ч — PRD, RFC, coaching). Ролевые треки (PM 4 ч … Tech Lead 12 ч). Onboarding: новый сотрудник — неделя (orientation → process → hands-on → real work → review), новый tech lead — месяц (foundation → advanced → coaching → leadership). Сертификация с quiz ≥ 80% и real project. Восемь типичных ошибок с противоядиями (over/under-documentation, vague requirements, missing error handling, AI as black box…) — `../research/kb/methods/training-onboarding.md`.

---

**Дальше:** [Глава 10. Открытые вопросы и трейдоффы](10-open-questions.md) — что не решено и где честные компромиссы.
