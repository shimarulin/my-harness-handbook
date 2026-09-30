# Метрики и dashboards процесса

| Параметр | Значение |
|---|---|
| Статус | draft |
| Обновлено | 2026-09-30 |

## Что это

Система метрик эффективности процесса, работы AI-агентов и предотвращения повторения ошибок. Принципы: измерять важное (не vanity metrics; каждая метрика имеет alert threshold и actionable); обязательный feedback loop (**Данные → Анализ → Действия → Проверка эффективности**); обучение на ошибках (patterns выявляются автоматически, защита через checklists/linting); прозрачность (dashboards для всей команды, ретроспективы на данных, не мнениях).

## 1. Process Metrics

### 1.1 Cycle Time

| Метрика | Target | Alert |
|---|---|---|
| Problem → Requirements time | < 2 часа | > 4 часа |
| Requirements → Approach time | < 1 день | > 2 дня |
| Approach → Implementation time | < 1 день | > 3 дня |
| Full cycle time (идея → production) | baseline | 2× baseline |

### 1.2 Quality

| Метрика | Target | Alert |
|---|---|---|
| Requirements completeness (% покрытых тестами) | > 95% | < 80% |
| EARS format compliance | 100% | < 90% |
| ADR coverage (% архитектурных решений с ADR) | 100% | < 80% |
| Documentation freshness (средний возраст) | < 30 дней | > 90 дней |
| Cross-reference integrity | 100% | < 95% |

### 1.3 Collaboration

| Метрика | Target | Alert |
|---|---|---|
| Review time (PR с документацией) | < 1 день | > 3 дня |
| Review iterations | < 2 | > 5 |
| Comment response time | < 4 часа | > 24 часа |
| Stale PRs (> 7 дней без активности) | 0% | > 10% |

## 2. AI-Agent Metrics

### 2.1 Effectiveness

| Метрика | Target | Alert |
|---|---|---|
| Task completion rate (% без human intervention) | > 80% | < 60% |
| First-time quality (% принятых без major revisions) | > 70% | < 50% |
| Context usage (эффективность context window) | > 80% | < 50% или > 95% |
| Token efficiency (tokens per successful task) | baseline ± 20% | 2× baseline |
| Hallucination rate (% с фактическими ошибками) | < 5% | > 15% |

### 2.2 Deviation

| Метрика | Target | Alert |
|---|---|---|
| Scope creep (% требований после approval) | < 10% | > 30% |
| Architecture drift (код vs Approach) | 0 | любое |
| Requirements violation | 0 | любое |
| Timeline deviation | < 20% | > 50% |

### 2.3 Learning

| Метрика | Target | Alert |
|---|---|---|
| Repeated errors (одинаковые у одного агента) | 0 | > 2 раза |
| Pattern recognition (% известных patterns) | > 90% | < 70% |
| Improvement rate (метрик за sprint) | > 5% | < 0% |

## 3. Resource Metrics

| Метрика | Target | Alert |
|---|---|---|
| Human time per task | baseline ± 20% | 2× baseline |
| Review overhead (% времени ревью vs реализация) | < 30% | > 50% |
| Documentation debt (% dev time на поддержку доков) | < 10% | > 20% |
| Token cost per task | baseline ± 30% | 2× baseline |
| Infrastructure cost (CI для проверок) | < $100/мес | > $500/мес |

## Лог метрик агента (jsonl, `.agent_metrics/metrics.jsonl`)

```json
{"task_id": "REQ-001-generation", "agent": "claude", "duration": "20m",
 "tokens": 2328, "iterations": 2, "human_interventions": 1,
 "quality": "accepted_after_minor_revision",
 "issues": ["incomplete_patterns", "vague_terms"], "timestamp": "…"}
```

Значения output_quality: `accepted | minor_revision | major_revision | rejected`. Производные: acceptance_rate, major_revision_rate, avg_tokens_per_task, avg_human_interventions.

## Feedback loops

- **Real-time**: pre-commit hooks + IDE plugins (EARS linter в VSCode).
- **Post-action**: GitHub Actions + dashboard (quality-gate workflow с комментарием на PR).
- **Periodic**: weekly/monthly automated reports (Slack webhook).
- **Ручная**: structured code review (шаблон: Quality Assessment → Issues Found (severity + suggestion) → Feedback for AI Agent → Action Items: update prompt template / add to examples library / create checklist item).

Качественный разбор кейса (генерация требований): total 20 мин (target < 15 ⚠️), tokens 2328 (< 2000 ⚠️), iterations 2 (target 1 ⚠️) → root cause: промпт без checklist всех 5 EARS-паттернов → после обновления промпта: iterations 1, ~1500 tokens, ~10 мин.

## Prevention patterns (защита от повторения)

- **Pre-generation checklist**: Context (problem/requirements/approach/ADRs provided?) → Quality Gates (output format, acceptance criteria, examples, constraints) → Verification Plan (automated checks, human review points, success metrics).
- **Post-generation checklist**: Completeness (requirements/edge cases/error handling/docs) → Quality (linter, no hallucinations, patterns, standards) → Traceability (REQ-XXX, approach sections, ADRs, valid cross-refs) → Testing.
- **Prompt templates с защитой**: Output Format + Quality Checklist (MUST verify: все 5 паттернов, NFR, edge cases, no vague terms, atomicity) + Examples + Anti-Patterns to Avoid (❌ «fast» → ✅ «< 200ms»; ❌ «gracefully» → ✅ «retry 3x then 503»).
- **CI quality gates** (5, все continue-on-error: false): EARS Format → Requirements Coverage (> 95%) → Architecture Compliance → Test Coverage (`--cov-fail-under=80`) → AI Agent Metrics (acceptance rate ≥ 70%).

## Dashboards

1. **Team Dashboard** (Grafana/Metabase): Process metrics + AI metrics + Trends за 4 недели.
2. **AI Agent Dashboard**: PERFORMANCE за 30 дней (tasks, acceptance rate, avg tokens, interventions) + task types breakdown + recent issues + recommendations.
3. **Error Pattern Dashboard** (90 дней): pattern → occurrences / agents / task types / root cause / mitigation (done/in progress). Примеры: missing error handling (12 occ), incomplete requirements (8), architecture drift (5).

## Continuous improvement (каденс)

- **Weekly Review** (lead + 2 dev, 30 мин): dashboard (10) / top 3 issues (10) / action items (10).
- **Monthly Retrospective** (команда, 1 ч): metrics deep dive (20) / root cause (20) / improvements (15) / tool updates (5).
- **Quarterly Planning** (команда + stakeholders, 2 ч): quarterly metrics (30) / strategic improvements (45) / plan (45).

## Инструменты

Prometheus (time-series), Grafana (визуализация), Metabase (BI), GitHub Actions (checks), Slack (notifications), Jupyter/Pandas (analysis), Retool (custom dashboards). Скрипты: `calculate_cycle_time.py`, `check_requirements_coverage.py`, `track_agent_metrics.py`, `check_architecture_compliance.py`, `generate_weekly_report.py`.

## Источники

- Входные материалы inbox: `documentation-process-v2/metrics-dashboards/README.md`
- Связанные KB: `docs-cicd.md` (quality gates), `review-collaboration.md` (метрики ревью), `ai-agent-workflows.md` (верификация)
