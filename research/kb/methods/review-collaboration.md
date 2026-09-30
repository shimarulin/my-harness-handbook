# Ревью и коллаборация над документацией

| Параметр | Значение |
|---|---|
| Статус | draft |
| Обновлено | 2026-09-30 |

## Что это

Модель ревью документации как коллаборации, а не gatekeeping: четыре workflow разной тяжести, балльные чек-листы по типам артефактов, паттерны approval, формализованный feedback, эскалация, SLA, автоматизация.

## Принципы

1. **Review is Collaboration, Not Gatekeeping** — цель улучшить документ, не заблокировать; конструктивный feedback; учимся друг у друга.
2. **Explicit Expectations** — чек-листы для каждого типа артефакта; известные ревьюеры и сроки; ясные критерии approval.
3. **Async-First** — ревью через PR и комментарии; не требует synchronous meetings; время для глубокого анализа.
4. **Time-Boxed** — default: **1 неделя для RFC, 2 дня для ADR**; эскалация при отсутствии ответа.

## Четыре workflow

| Workflow | Для чего | Ревьюеры | Timeline | Approvals |
|---|---|---|---|---|
| **1. Lightweight** | Bug fixes, minor clarifications, typos | 1 (любой team member) | 1–2 дня | 1 |
| **2. Standard** | Requirements, Approach, Tasks, ADR | 2 (domain expert + peer) | 2–5 дней | 2 |
| **3. Formal** | RFC, PRD, major architectural changes | 3+ (diverse perspectives; PM для PRD; Security при applicable) | 1–2 недели | Consensus или designated approver |
| **4. ARB** | Cross-team impact, compliance, major investments | Architecture Review Board (5–7 members) | 2–4 недели | ARB decision: Approved / Approved with conditions / Changes requested / Rejected + post-implementation review через 3 месяца |

## Балльные чек-листы (scoring)

- **Problem Statement (40 баллов)**: порог ≥ 30.
- **Requirements / ADR / Approach (100 баллов)**: порог ≥ 80.
- **RFC (100 баллов)**: ≥ 85 approve; 70–84 approved with conditions; < 70 changes requested.

## Паттерны approval

1. **Unanimous Consent** — все назначенные ревьюеры; один rejects → changes. Для: RFC, major ADR, PRD (high quality bar; медленно, один может заблокировать).
2. **Majority Vote** — 2 из 3; dissenting opinion документируется. Для: standard ADR, Approach.
3. **Lazy Consensus** — объявление + ждать (default 3 дня); молчание = согласие. Для: minor ADR, documentation updates (быстро; риск пропустить concern — см. принцип «молчание ≠ согласие» в `../principles/ai-degradation-phenomena.md`: для зоны accepted-решений применять с осторожностью).
4. **Designated Approver** — один ответственный (tech lead для технических, PM для PRD). Для: time-sensitive decisions.

## Feedback: SBI-модель

**Situation → Behavior → Impact**: «В секции Error Handling (S) описан только happy path (B) — при сбое S3 пользователь не узнает о проблеме (I)». Противопоставляется оценочному feedback («плохо написано»). Для AI output — расширенный шаблон: Quality Assessment (Correctness/Completeness/Clarity/Consistency) → Issues Found (severity + suggestion) → Feedback for AI Agent (what worked / what needs improvement / context missing) → Action Items (update prompt template / add to examples library / create checklist item).

## Conflict resolution и эскалация

Шаги: обсуждение в PR (async) → sync-звонок при тупике → эскалация. Эскалация: **24h → 48h → 1 week → VP/CTO** (для RFC/major decisions; применительно к ревью, не к срокам ответа ревьюера — для тех: SLA + напоминания).

## SLA на ревью

Lightweight 1–2 дня; Standard 2–5 дней; Formal 1–2 недели (review period default 1 неделя); ARB preliminary review 1 неделя, meeting 30–60 мин. Stale PR: % PR без активности > 7 дней — target 0% (alert > 10%).

## Автоматизация

- **Auto-assign reviewers** (`kentaro-m/auto-assign-action@v1.2.0`).
- **Auto-approve low-risk** (`hmarr/auto-approve-action@v3`): LINES_CHANGED < 10 и только docs-файлы.
- **Pre-review checks** (CI до назначения ревьюеров: lint, trace-check, coverage — см. `docs-cicd.md`).
- GitHub/GitLab features: PRs (inline comments, suggested changes), Discussions (RFC debates), Projects (Kanban).

## Метрики ревью

Review time (target < 1 день, alert > 3); review iterations (< 2, alert > 5); comment response time (< 4 часа, alert > 24); stale PRs (0%, alert > 10%). Ретроспектива ревью-процесса — по данным (`metrics-dashboards.md`).

## Анти-паттерны (6)

Review as gatekeeping (блокируют вместо улучшения); no explicit criteria (субъективные ревью); synchronous-only (требуют встреч для всего); endless review cycles (без time-box); feedback without specifics («плохо» вместо SBI); approval без чтения (rubber-stamping).

## Источники

- Входные материалы inbox: `documentation-process-v2/review-collaboration/README.md`
- Связанные KB: `docs-cicd.md`, `metrics-dashboards.md`, `ai-agent-workflows.md` (уровни верификации), `../principles/attention-economy.md`
