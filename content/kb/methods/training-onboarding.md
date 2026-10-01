# Обучение и онбординг процессу

| Параметр | Значение |
|---|---|
| Статус | draft |
| Обновлено | 2026-09-30 |

## Что это

Программа внедрения процессов разработки в команде: 3-уровневое обучение, ролевые треки, onboarding checklists, workshops, сертификация. Принципы обучения: **Learning by doing (70% practice, 30% theory)**, progressive complexity, peer learning, continuous improvement.

## Уровни обучения

| Уровень | Для кого | Длительность | Результат |
|---|---|---|---|
| **L1 Foundation** | Все (обязательный) | 4 ч (workshop + hands-on) | Базовая документация для простой фичи: Введение (30 мин) → Problem Statement (45) → EARS (60) → ADR (45) → мини-проект (60) |
| **L2 Practitioner** | Developers | 8 ч | Вести фичу от идеи до реализации: Approach (90) → Tasks (60) → Implementation workflow (90) → AI-agent integration (60) → Verification (60) → практика: средняя фича (120) |
| **L3 Expert** | Architects, Tech Leads | 8 ч | Вести крупные проекты и обучать других: PRD (60) → RFC (90) → Advanced ADR (60) → BDD (60) → API-first (60) → Coaching и ревью (90) → case study (60) |

## Ролевые треки

| Роль | Фокус | Длительность |
|---|---|---|
| Product Manager | PRD, Problem Statement, prioritization (MoSCoW, RICE) | 4 ч |
| Developer | Requirements, Approach, Tasks, Implementation, AI integration | 8 ч |
| Architect | ADR, RFC, диаграммы, decision-making | 8 ч |
| QA Engineer | Requirements validation, BDD, testing strategy | 6 ч |
| Tech Lead | Весь процесс + coaching | 12 ч |
| AI Engineer | Prompt engineering, AI-agent workflows | 6 ч |

## Onboarding checklists

**Новый сотрудник (неделя)**: Day 1 — orientation (team, dev env, repos, docs guide, review существующих ADR); Day 2 — process overview (Module 1, чтение модулей, сквозной пример export-service); Day 3 — hands-on (упражнения PS/EARS/ADR, shadow senior); Day 4 — real work (малая задача с документацией, PR); Day 5 — review с ментором + цели на неделю 2.

**Новый Tech Lead (месяц)**: Week 1 — Foundation (L1+L2, все docs, метрики, PMs); Week 2 — Advanced (L3, недавние RFC/ADR, pain points); Week 3 — Coaching (провести onboarding, requirements workshop, review качества, review cadence); Week 4 — Leadership (вести RFC, принимать ADR, оптимизировать workflow, план обучения на квартал). Success criteria: объясняет процесс, пишет качественные ADR/RFC, обучает других, качество документации команды улучшилось.

## Expert role (ответственности)

Coaching (onboard, review quality, feedback on ADR/RFC); Leadership (lead RFC, architectural decisions, complex ADRs, resolve conflicts); Improvement (bottlenecks, improvements, update materials); Metrics (team documentation quality score, onboarding time, RFC approval rate, adoption rate).

## Типичные ошибки обучения (8, с противоядиями)

1. **Over-documentation** (документируем каждую мелочь) → Decision Matrix: bug fix — PS в commit message; small feature (1–3 дня) — PS + Requirements + Tasks; medium (1–2 нед) — + ADR + Approach; large/new product — всё.
2. **Under-documentation** → Minimum Viable Documentation: любая задача — PS; неочевидное — Requirements; архитектурное решение — ADR; фича > 1 дня — + Approach/Tasks/Tests; > 1 недели — + PRD/RFC/BDD по критериям.
3. **Solution in Problem Statement** → всегда «почему это проблема?» (5 Whys); пример хорошего PS: «Current database cannot handle complex JOINs. Reports take 5+ minutes. 10h/week optimizing.»
4. **Vague Requirements** → SMART + числа: ❌ «fast» → ✅ «within 200ms for 95th percentile»; ❌ «gracefully» → ✅ «retry 3x exponential backoff, then 503»; ❌ «user-friendly» → ✅ «complete onboarding within 5 minutes».
5. **Missing Error Handling** → всегда Unwanted pattern (If/Then); checklist: happy path + error scenarios + edge cases + performance + security.
6. **ADR Without Alternatives** → минимум 2–3 альтернативы + «do nothing».
7. **No Verification** (documentation drift) → автоматические проверки (EARS linter, requirements coverage, architecture compliance, cross-reference, test coverage) + manual review.
8. **AI as Black Box** → human-in-the-loop для критических решений; verification checklist: facts verified, requirements covered, architecture aligns with ADRs, error handling, tests passing.

## Workshops (полдня, 4 ч)

1. **Documentation as Code** (8–12 чел): введение 30 / PS 45 / EARS 60 / ADR 45 / мини-проект 45.
2. **AI-Agent Integration** (6–10 чел): AI principles 30 / prompt engineering 60 / hands-on requirements 60 / hands-on code generation 45 / verification & quality gates 30.
3. **RFC Process** (6–8 чел): RFC principles 45 / writing RFC 60 / review simulation 60 / decision-making + ADR 45 / wrap-up 15.

## Сертификация

- **L1**: training (4 ч) + exercises ≥ 70% + мини-проект + quiz 20 вопросов ≥ 80%. Награда: digital badge, доступ к advanced workshops.
- **L2**: L1 cert + training (8 ч) + real project с полной документацией (≥ 10 requirements всех паттернов, ≥ 10 tasks) + peer review от 2 коллег (≥ 80%) + presentation + production без major issues 1 месяц.
- **L3**: L2 cert + training (8 ч) + lead RFC process + coach 2 new members + conduct workshop + process improvements.

Success metrics программы: documentation quality score, onboarding time, process adoption rate, team satisfaction.

## Источники

- Входные материалы inbox: `documentation-process-v2/training-onboarding/README.md`
- Книги: «Documentation as Code» (Tom Johnson), «Software Requirements» (Karl Wiegers), «Building Evolutionary Architectures» (Neal Ford), «Team Topologies» (Skelton)
- Связанные KB: `artifact-templates.md` (материалы модулей), `ai-agent-workflows.md` (AI principles), `metrics-dashboards.md` (success metrics)
