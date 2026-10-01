# Problem Statement

Первый и самый важный модуль Core Foundation. Без чёткой формулировки проблемы все последующие решения будут неправильными.

## Что такое Problem Statement

**Problem Statement** — краткое (1-3 абзаца) описание проблемы, которую мы решаем. Отвечает на вопросы:
- **Что** не работает?
- **Почему** это проблема?
- **Кто** страдает?
- **Какова** стоимость проблемы?
- **Что** будет если не решить?

**Это НЕ**:
- Описание решения (это придёт позже)
- Техническая спецификация (это RFC/SDD)
- Список задач (это tasks breakdown)

**Это**:
- Формулировка проблемы на языке пользователя/бизнеса
- Обоснование почему это стоит решать
- North star для всех последующих решений

---

## Когда использовать

### Всегда
- Любая новая работа (feature, bug fix, refactor)
- Любое architectural decision (как context для ADR)
- Любой RFC (как motivation)
- Любая PR (как justification)

### Формат зависит от контекста

**Bug fix**: В commit message или PR description
**Small feature**: В начале spec файла
**Major feature**: Отдельный раздел в PRD
**Architectural decision**: В ADR как Context section

---

## Структура Problem Statement

### Базовый шаблон (3 абзаца)

```markdown
## Problem Statement

### The Problem
[Что не работает? Описание текущего состояния.]

### The Impact
[Почему это проблема? Кто страдает? Какова стоимость?]

### The Goal
[Какое состояние мы хотим достичь? (НЕ как это сделать)]
```

### Расширенный шаблон (для PRD/RFC)

```markdown
## Problem Statement

### Context
[Бэкграунд: что привело к этой проблеме?]

### Current State
[Как сейчас работает? Что сломано?]

### Pain Points
[Конкретные боли пользователей/бизнеса с evidence]

### Impact
[Количественная оценка: деньги, время, пользователи]

### Success Criteria
[Как мы поймём что проблема решена?]
```

---

## Техники формулировки

### Техника 1: 5 Whys

**Цель**: Дойти до root cause вместо симптомов.

**Как работает**:
Задавайте "Почему?" 5 раз подряд, каждый раз углубляясь.

**Пример**:
```
Проблема: Пользователи уходят с checkout page

1. Почему? → Форма слишком длинная
2. Почему? → Мы требуем 15 полей
3. Почему? → Юридический отдел требует все данные
4. Почему? → У нас нет integration с KYC service
5. Почему? → Мы не инвестировали в KYC automation

Root cause: Отсутствие KYC automation вынуждает собирать данные вручную
```

**Результат**: Problem statement фокусируется на root cause, не симптомах.

**Когда использовать**:
- Когда проблема кажется "очевидной"
- Когда разные stakeholders видят разные проблемы
- Когда хотите избежать "XY problem"

**AI Prompt**:
```
Help me apply the 5 Whys technique to get to the root cause:
[describe the symptom you're seeing]

Ask me "why" 5 times, each time going deeper based on my answers.
```

---

### Техника 2: Problem-User-Impact Matrix

**Цель**: Структурировать проблему по измерениям.

**Матрица**:
```
┌─────────────────┬──────────────────┬──────────────────┐
│ User Segment    │ Pain Point       │ Impact           │
├─────────────────┼──────────────────┼──────────────────┤
│ New users       │ Can't find docs  │ 40% drop-off     │
│ Power users     │ Slow search      │ 2h/week lost     │
│ Mobile users    │ Layout broken    │ 60% bounce rate  │
└─────────────────┴──────────────────┴──────────────────┘
```

**Когда использовать**:
- Multiple user segments affected
- Нужно prioritization
- Хотите quantitative evidence

---

### Техника 3: Before/After Bridge

**Цель**: Показать gap между current и desired state.

**Шаблон**:
```
BEFORE (Current State):
[Как сейчас работает? Что сломано?]

AFTER (Desired State):
[Как должно работать? Что улучшится?]

BRIDGE (What We Need):
[Что нужно чтобы перейти от BEFORE к AFTER?]
```

**Пример**:
```markdown
## Problem Statement

**BEFORE**:
Developers spend 30 minutes setting up local environment for each new project. 
Setup docs are outdated, dependencies conflict, no standardization.

**AFTER**:
Developers can start coding in 5 minutes with one command. 
Environment is reproducible, consistent, documented.

**BRIDGE**:
Need standardized dev environment tooling with automation.
```

**Когда использовать**:
- Когда solution очевиден (но нужно justify)
- Когда stakeholders не видят ценности
- Для internal tooling projects

---

### Техника 4: Jobs to be Done (JTBD)

**Цель**: Фокус на user job, не product.

**Шаблон**:
```
When [situation], 
I want to [motivation], 
so I can [expected outcome].
```

**Пример**:
```markdown
## Problem Statement

**Situation**: When I'm onboarding a new team member
**Motivation**: I want them to understand our system architecture quickly  
**Outcome**: So they can contribute to code within first week

**Current Problem**: 
Our architecture documentation is scattered across Confluence, README files, 
and tribal knowledge. New hires take 3-4 weeks to become productive.
```

**Когда использовать**:
- Product-driven features
- User experience problems
- Когда нужно empathy с user

---

## Примеры

### Пример 1: Bug Fix (Minimal)

**Контекст**: Users report login failures

**Bad** ❌:
```
Fix login bug
```

**Good** ✅:
```markdown
## Problem

Users with special characters in passwords (e.g., "pass&word") cannot login. 
Error message is generic "Invalid credentials" which doesn't help diagnose.

## Impact
- Affects ~2% of users based on password analysis
- Support tickets: 15 this week
- User frustration visible in app store reviews

## Goal
Allow login with special characters AND provide helpful error messages.
```

**Где хранить**: Commit message или PR description

---

### Пример 2: Small Feature (Lightweight)

**Контекст**: Добавить data export feature

```markdown
## Problem Statement

Users cannot export their data from our platform. This violates GDPR 
data portability requirements and prevents users from migrating to 
competitors or backing up their data.

## Impact
- Enterprise customers (40% of revenue) cannot comply with GDPR Article 20
- 3 enterprise deals blocked in Q3 due to this
- Users requesting this in 23% of feedback surveys
- Competitive disadvantage vs Competitor X who offers this

## Goal
Users can export all their data in standard formats (CSV/JSON) 
within 30 seconds, with email notification when ready.

## Non-goals
- Real-time sync with external systems
- Import functionality (separate feature)
- Custom export formats (v1 is CSV/JSON only)
```

**Где хранить**: `docs/specs/export-feature.md` (в начале файла)

---

### Пример 3: Major Feature (PRD)

**Контекст**: Новая аналитическая платформа

```markdown
## Problem Statement

### Context
Our current analytics platform was built 5 years ago when we had 10K users. 
We now have 2M users and process 500M events/day. The system is showing cracks.

### Current State
- Dashboard queries take 30-60 seconds (unacceptable for real-time decisions)
- Cannot handle >100 concurrent users (product team blocked)
- Data freshness is T+1 day (business needs real-time)
- No self-service: every report requires engineering (2-week backlog)

### Pain Points
**Product Managers** (15 people):
- Cannot answer "how did feature X perform yesterday?" in meetings
- Must wait 2 weeks for custom reports
- Making decisions based on stale data

**Engineering** (40 people):
- Spend 30% time on ad-hoc analytics requests
- System crashes during peak hours (3 incidents last month)
- Cannot scale without complete rewrite

**Executives** (5 people):
- Board meetings without real-time metrics
- Cannot track OKRs effectively
- Competitor X has real-time dashboards (sales objection)

### Impact
- **Revenue**: 2 enterprise deals lost ($2M ARR) due to analytics limitations
- **Productivity**: 1200 engineering hours/year on ad-hoc reports
- **Risk**: System will not support projected 10M users next year
- **Morale**: Engineers frustrated with firefighting vs innovation

### Success Criteria
- Query latency < 3 seconds for 95th percentile
- Support 1000+ concurrent users
- Data freshness < 5 minutes
- Self-service: PMs can create reports without engineering
- Handle 10B events/day (10x current)

### Non-goals
- Replacing our data warehouse (BigQuery is fine)
- Building visualization library (use existing)
- Real-time streaming (5-minute freshness is sufficient for v1)
```

**Где хранить**: `docs/prd/analytics-platform-v2.md`

---

### Пример 4: Architectural Decision (ADR Context)

**Контекст**: Choosing message queue for event processing

```markdown
## Context and Problem Statement

### The Problem
Our monolith processes payment events synchronously. During Black Friday, 
we had 3 outages because payment processing blocked checkout flow.

### Current State
- Checkout → Payment Processing → Order Creation (synchronous)
- Payment service latency: 2-5 seconds normally, 30+ seconds under load
- No retry mechanism: failed payments = failed orders
- No way to scale payment processing independently

### Impact
- **Revenue**: $500K lost during Black Friday outages
- **Customer**: 8,000 failed orders, angry support tickets
- **Engineering**: 2 weeks firefighting, no feature work
- **Risk**: Will happen again next peak season

### Goal
Decouple payment processing from checkout so:
1. Checkout completes instantly (optimistic)
2. Payment processing scales independently  
3. Failed payments retry automatically
4. System survives 10x traffic spikes
```

**Где хранить**: `docs/adr/adr-007-event-driven-payments.md` (Context section)

---

## Anti-patterns

### ❌ Solution in Disguise

**Bad**:
```
Problem: We need to migrate to PostgreSQL
```

**Good**:
```
Problem: Our current database (MongoDB) cannot handle complex JOINs 
efficiently. Reports that should take 5 seconds take 5 minutes. 
Engineering spends 10 hours/week optimizing queries instead of features.
```

**Почему плохо**: Решение выдаётся за проблему. Не понятно почему это проблема.

**Как исправить**: Спросите "Почему это проблема?" — получите настоящую проблему.

---

### ❌ Too Vague

**Bad**:
```
Problem: System is slow
```

**Good**:
```
Problem: Search page takes 8-12 seconds to load (target: <2 seconds). 
This affects 85% of users who use search daily. 
User satisfaction score for search is 2.1/5 (lowest in app).
```

**Почему плохо**: Нет конкретики, невозможно verify решение.

**Как исправить**: Добавьте numbers, evidence, scope.

---

### ❌ Too Broad

**Bad**:
```
Problem: Our entire platform needs to be rewritten
```

**Good**:
```
Problem: Checkout conversion rate dropped 15% after adding payment options. 
User research shows form is confusing - 40% abandon at payment step. 
This costs us $200K/month in lost revenue.
```

**Почему плохо**: Невозможно решить "всё сразу". Paralysis by analysis.

**Как исправить**: Сфокусируйтесь на одной конкретной проблеме с measurable impact.

---

### ❌ No Impact

**Bad**:
```
Problem: We're using an outdated library version
```

**Good**:
```
Problem: Library X v1.2 has known security vulnerability (CVE-2024-1234). 
Security scan flagged our app. Enterprise customers require patching 
within 30 days per contract. We have 45 days until breach.
```

**Почему плохо**: Не понятно почему это стоит решать. "So what?"

**Как исправить**: Добавьте business impact (деньги, время, риск).

---

### ❌ Jumping to Solution

**Bad**:
```
Problem: We don't have Redis cache
Solution: Let's add Redis cache
```

**Good**:
```
Problem: Database queries take 500ms average. Under load, 5+ seconds. 
Users see loading spinners, 30% abandon. 
Adding Redis cache could reduce to 50ms, but we need to validate first.
```

**Почему плохо**: Решение выбрано до понимания проблемы. Может быть wrong solution.

**Как исправить**: Сначала problem, потом explore solutions (в RFC/Design).

---

## Checklist для ревью

Перед тем как считать Problem Statement готовым, проверьте:

### Must Have
- [ ] **Конкретность**: Есть numbers/evidence? (не "slow", а "5 seconds")
- [ ] **Impact**: Объяснено почему это важно? (деньги, время, пользователи)
- [ ] **Scope**: Ясно что входит и что НЕ входит?
- [ ] **No solution**: Описана проблема, не решение?
- [ ] **Testable**: Понятно как проверить что проблема решена?

### Should Have
- [ ] **User perspective**: Описано с точки зрения user/business?
- [ ] **Evidence**: Есть data/research/citations?
- [ ] **Urgency**: Ясно почему сейчас, не потом?
- [ ] **Stakeholders**: Ясно кто страдает?

### Nice to Have
- [ ] **Visual**: Есть диаграмма/схема current state?
- [ ] **Comparison**: Есть benchmark vs competitors?
- [ ] **History**: Объяснено как мы сюда пришли?

---

## AI-Agent Integration

### Prompt: Refine Problem Statement

```
I have a problem I'm trying to solve. Help me make it more specific 
and impactful using the 5 Whys technique.

Initial problem: [your rough description]

Ask me clarifying questions to get to the root cause and business impact.
```

### Prompt: Generate from Symptoms

```
Users are complaining about [symptom]. Help me write a proper problem 
statement that includes:
1. Root cause (use 5 Whys)
2. Business impact (quantify)
3. Success criteria (how we know it's solved)
```

### Prompt: Check Quality

```
Review this problem statement and tell me:
1. Is it specific enough?
2. Does it avoid being a solution in disguise?
3. Is the impact clear?
4. What's missing?

Problem statement: [paste your statement]
```

### Prompt: Before/After Bridge

```
Help me structure this as a Before/After Bridge problem statement:

Current situation: [describe current state]
Desired situation: [describe what you want]

Format it as:
- BEFORE (current state with pain points)
- AFTER (desired state with benefits)  
- BRIDGE (what we need to build)
```

---

## Tools

### Где писать Problem Statement

**Git Commit** (для bug fixes):
```bash
git commit -m "fix: login fails with special characters

Problem: Users with '&' or '@' in passwords cannot login.
Impact: 2% of users affected, 15 support tickets this week.
Goal: Allow special characters + helpful error messages.

Fixes #123"
```

**Pull Request Description**:
```markdown
## Problem
[problem statement here]

## Approach
[how you're solving it]

## Testing
[how you verified]
```

**Spec File** (для features):
```markdown
# Feature: Data Export

## Problem Statement
[problem statement here]

## Requirements
[derived from problem]

## Approach
[technical design]
```

**PRD** (для major features):
```markdown
# PRD: Analytics Platform v2

## Problem Statement
[detailed problem statement]

## Goals & Non-goals
[what we will/won't do]

## Success Metrics
[how we measure]
```

### AI Tools

**Claude/GPT**:
- Refine problem statements
- Apply 5 Whys
- Generate from symptoms
- Check quality

**Diagramming**:
- [Mermaid](https://mermaid.js.org) — для current state diagrams
- [PlantUML](https://plantuml.com) — для system context
- [Excalidraw](https://excalidraw.com) — для rough sketches

---

## Connection to Other Modules

### → Requirements (EARS)

**Как**: Problem statement → derive requirements

**Пример**:
```
Problem: Users cannot export data (GDPR violation)
    ↓
Requirements:
- When user requests export, system shall generate file within 30 seconds
- While export is processing, system shall show progress
- If export fails, system shall send email with error details
```

### → RFC (Request for Comments)

**Как**: Problem statement → RFC context/motivation

**Пример**:
```
Problem: Sync payment processing causes outages under load
    ↓
RFC: "Event-Driven Payment Processing"
- Context: [problem statement]
- Proposal: async processing with message queue
- Alternatives: different queue solutions
```

### → ADR (Architecture Decision Record)

**Как**: Problem statement → ADR context

**Пример**:
```
Problem: Database queries too slow for real-time analytics
    ↓
ADR: "Use Redis for Analytics Caching"
- Context: [problem statement]
- Decision: Redis cache layer
- Consequences: faster queries, operational complexity
```

---

## Summary

**Problem Statement** — это foundation всего процесса. Без него:
- Решаем не ту проблему
- Выбираем wrong solutions
- Не можем verify success
- Теряем context со временем

**Ключевые принципы**:
1. **Specific** — с numbers и evidence
2. **Impact-focused** — почему это важно
3. **Solution-free** — проблема, не решение
4. **Testable** — ясно как verify

**Когда писать**:
- ✅ Всегда в начале работы
- ✅ Для любого размера задачи
- ✅ Даже если "очевидно"

**Где хранить**:
- Bug fix: commit message
- Feature: spec file
- Major: PRD
- Decision: ADR context

---

## References

- [5 Whys Technique](https://www.atlassian.com/team-playbook/plays/5-whys) — Atlassian
- [Problem Statement Examples](https://miro.com/strategic-planning/customer-problem-statement-examples/) — Miro
- [Problem Statement Template](https://airfocus.com/blog/how-to-write-a-product-problem-statement-with-problem-statement-template/) — Airfocus
- [Next: Requirements (EARS)](./requirements.md)
- [Back to Modules Index](./README.md)
