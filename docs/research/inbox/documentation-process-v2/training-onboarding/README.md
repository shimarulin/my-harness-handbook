# Обучение и Onboarding

Комплексное руководство по внедрению процессов разработки документации в команде. Включает материалы для разных ролей, onboarding checklists, workshops и примеры.

---

## Обзор

### Цели обучения

После прохождения обучения участники смогут:
1. ✅ Создавать все необходимые артефакты (Problem Statement → Implementation)
2. ✅ Использовать правильные форматы (EARS, MADR, Gherkin, OpenAPI)
3. ✅ Эффективно работать с AI-агентами
4. ✅ Применять модульный подход (собирать процесс под задачу)
5. ✅ Верифицировать качество документации и кода
6. ✅ Использовать инструменты автоматизации

### Целевая аудитория

| Роль | Фокус обучения | Длительность |
|------|---------------|--------------|
| **Product Manager** | PRD, Problem Statement, Requirements prioritization | 4 часа |
| **Developer** | Requirements, Approach, Tasks, Implementation | 8 часов |
| **Architect** | ADR, RFC, Architecture diagrams, Decision-making | 8 часов |
| **QA Engineer** | Requirements validation, BDD, Testing strategy | 6 часов |
| **Tech Lead** | Весь процесс + coaching команды | 12 часов |
| **AI Engineer** | Prompt engineering, AI-agent workflows | 6 часов |

---

## Структура обучения

### Level 1: Foundation (Обязательный для всех)

**Длительность**: 4 часа  
**Формат**: Workshop + hands-on

**Модули**:
1. Введение в процесс (30 мин)
2. Problem Statement (45 мин)
3. Requirements (EARS) (60 мин)
4. ADR (45 мин)
5. Практика: мини-проект (60 мин)

**Результат**: Участник может создать базовую документацию для простой фичи

### Level 2: Practitioner (Для разработчиков)

**Длительность**: 8 часов  
**Формат**: Workshop + real project

**Модули**:
1. Approach (Technical Design) (90 мин)
2. Tasks Breakdown (60 мин)
3. Implementation workflow (90 мин)
4. AI-agent integration (60 мин)
5. Verification и testing (60 мин)
6. Практика: средняя фича (120 мин)

**Результат**: Участник может вести фичу от идеи до реализации

### Level 3: Expert (Для architects и tech leads)

**Длительность**: 8 часов  
**Флормат**: Workshop + case studies

**Модули**:
1. PRD (Product Requirements) (60 мин)
2. RFC (Request for Comments) (90 мин)
3. Advanced ADR patterns (60 мин)
4. BDD и executable specifications (60 мин)
5. API-first development (60 мин)
6. Coaching и ревью (90 мин)
7. Case study: крупный проект (60 мин)

**Результат**: Участник может вести крупные проекты и обучать других

---

## Training Materials

### Module 1: Введение в процесс (30 мин)

#### Презентация

```markdown
# Документация как код: новый подход к разработке

## Проблема (5 мин)
- Документация устаревает быстрее чем пишется
- Решения теряются в Slack/emails
- Новые члены команды теряются месяцами
- AI-агенты не могут работать без контекста

## Решение (10 мин)
- Documentation-first подход
- Git-native хранение
- Модульная система
- AI-friendly форматы

## Модули (10 мин)
- Core Foundation: Problem → Requirements → ADR
- Execution Flow: Approach → Tasks → Implementation
- Optional: PRD, RFC, BDD, API Specs

## Пример (5 мин)
- End-to-end: Export Service
```

#### Интерактивное упражнение

**Задача**: Разделите команду на группы по 3-4 человека

**Сценарий**: "Пользователи жалуются что поиск работает медленно"

**Задание** (10 мин):
1. Сформулируйте Problem Statement (5 Whys)
2. Напишите 3-5 требований в EARS
3. Определите нужно ли ADR

**Обсуждение** (10 мин):
- Каждая группа презентует
- Сравнение подходов
- Feedback от фасилитатора

---

### Module 2: Problem Statement (45 мин)

#### Теория (15 мин)

**Что такое Problem Statement**:
- Краткое описание проблемы (1-3 абзаца)
- Отвечает на: Что? Почему? Кто? Стоимость?
- НЕ решение, НЕ техническая спецификация

**Техники**:
1. **5 Whys** — дойти до root cause
2. **Before/After Bridge** — gap analysis
3. **Problem-User-Impact Matrix** — структурирование

#### Практика (30 мин)

**Упражнение 1: 5 Whys** (10 мин)

```
Индивидуальное задание:

Проблема: "Наш API слишком медленный"

Задайте "Почему?" 5 раз, углубляясь каждый раз.

Запишите:
1. Symptom: API медленный
2. Why? → [ваш ответ]
3. Why? → [ваш ответ]
4. Why? → [ваш ответ]
5. Why? → [ваш ответ]
6. Root cause: [вывод]
```

**Упражнение 2: Написание Problem Statement** (15 мин)

```
Индивидуальное задание:

Выберите ОДНУ проблему из списка:
- Users can't reset their password
- Checkout conversion rate dropped 15%
- Support tickets increased 300% this month
- Developers spend 40% time on manual tasks
- System crashes during peak hours

Напишите Problem Statement используя шаблон:

## The Problem
[Что не работает? Описание текущего состояния]

## The Impact
[Почему это проблема? Кто страдает? Какова стоимость?]
- Evidence: [numbers, data]
- Users affected: [количество/процент]
- Business impact: [деньги, время, риск]

## The Goal
[Какое состояние мы хотим достичь?]
- Specific: [конкретно]
- Measurable: [измеримо]
- Time-bound: [сроки]

## Non-goals
[Что мы НЕ делаем в этой итерации]
```

**Peer Review** (5 мин):
- Обменяйтесь с соседом
- Проверьте по checklist:
  - [ ] Конкретность (есть numbers?)
  - [ ] Impact (объяснено почему важно?)
  - [ ] No solution (описана проблема, не решение?)
  - [ ] Testable (понятно как verify?)

---

### Module 3: Requirements (EARS) (60 мин)

#### Теория (20 мин)

**Что такое EARS**:
- Easy Approach to Requirements Syntax
- 5 паттернов для структурирования требований
- Убирает ambiguity, делает требования testable

**5 Паттернов**:

| Паттерн | Синтаксис | Когда |
|---------|-----------|-------|
| **Ubiquitous** | `The system shall...` | Всегда активно |
| **State-driven** | `While <state>, the system shall...` | Пока состояние |
| **Event-driven** | `When <trigger>, the system shall...` | При событии |
| **Optional** | `Where <feature>, the system shall...` | Если фича включена |
| **Unwanted** | `If <error>, then the system shall...` | При ошибке |

#### Практика (40 мин)

**Упражнение 1: Распознавание паттернов** (10 мин)

```
Определите паттерн для каждого требования:

1. "The system shall encrypt all passwords" → ____________
2. "When user clicks logout, system shall clear session" → ____________
3. "While user is logged in, system shall show dashboard" → ____________
4. "If payment fails, system shall retry 3 times" → ____________
5. "Where enterprise plan, system shall allow SSO" → ____________

Ответы:
1. Ubiquitous
2. Event-driven
3. State-driven
4. Unwanted
5. Optional
```

**Упражнение 2: Конвертация в EARS** (15 мин)

```
Преобразуйте эти нечёткие требования в EARS:

1. "System should be fast"
   → EARS: ________________________________________________

2. "Handle errors gracefully"
   → EARS: ________________________________________________

3. "Users can export data"
   → EARS: ________________________________________________

4. "Login should be secure"
   → EARS: ________________________________________________

Примеры хороших ответов:

1. "The search API shall return results within 200ms for 95th percentile"
2. "If database connection fails, then system shall retry 3 times with exponential backoff"
3. "When user requests export, system shall generate file within 30 seconds"
4. "All passwords shall be hashed using bcrypt with cost factor ≥ 12"
```

**Упражнение 3: Полная спецификация** (15 мин)

```
Групповое задание (3-4 человека):

Feature: User password reset

Напишите требования используя ВСЕ 5 паттернов:

## Ubiquitous
- REQ-001: [всегда активное требование]

## State-driven
- REQ-002: [требование активное пока состояние]

## Event-driven
- REQ-003: [реакция на событие]

## Optional
- REQ-004: [если фича включена]

## Unwanted
- REQ-005: [обработка ошибки]

## Non-functional
- REQ-006: [performance/security/usability]

Минимум: 6 требований (по одному каждого типа)
```

**Обсуждение** (5 мин):
- Каждая группа читает свои требования
- Проверка: все 5 паттернов покрыты?
- Feedback от фасилитатора

---

### Module 4: ADR (45 мин)

#### Теория (15 мин)

**Что такое ADR**:
- Architecture Decision Record
- Запись ОДНОГО архитектурного решения
- Immutable (никогда не редактируется)

**Когда создавать**:
- ✅ Выбор technology stack
- ✅ Архитектурные паттерны
- ✅ Data model decisions
- ✅ Integration choices
- ❌ Trivial decisions
- ❌ Coding standards

**Форматы**:
- **Nygard** (простой): Context → Decision → Consequences
- **MADR** (структурированный): + Decision Drivers + Options + Pros/Cons
- **Y-Statements** (lightweight): одно предложение

#### Практика (30 мин)

**Упражнение 1: Выбор формата** (5 мин)

```
Для каждого решения выберите формат:

1. "Используем camelCase для переменных"
   → Формат: ____________ (Ответ: Не создавать ADR)

2. "Выбираем PostgreSQL вместо MongoDB"
   → Формат: ____________ (Ответ: MADR)

3. "Используем JWT для аутентификации"
   → Формат: ____________ (Ответ: MADR или Nygard)

4. "Команда решает работать удалённо по пятницам"
   → Формат: ____________ (Ответ: Y-Statements)
```

**Упражнение 2: Написание ADR** (20 мин)

```
Индивидуальное задание:

Scenario: Вы выбираете message queue для async processing

Напишите ADR в MADR формате:

# ADR NNN: Use [Technology] for [Purpose]

## Status
[proposed | accepted | deprecated | superseded]

## Context and Problem Statement
[Опишите проблему и контекст]

## Decision Drivers
- [driver 1]
- [driver 2]
- [driver 3]

## Considered Options
- [Option 1]
- [Option 2]
- [Option 3]
- [Do nothing]

## Decision Outcome
Chosen option: "[option]", because [justification]

### Consequences
* Good, because [positive]
* Bad, because [negative]
* Risk: [potential issue]

## Pros and Cons of the Options

### [Option 1]
* Good: [pro]
* Bad: [con]

### [Option 2]
* Good: [pro]
* Bad: [con]

## More Information
[Ссылки, related ADRs]
```

**Peer Review** (5 мин):
- Обменяйтесь ADR
- Проверьте:
  - [ ] Context ясен?
  - [ ] Все alternatives рассмотрены?
  - [ ] Decision обоснован?
  - [ ] Consequences включают bad outcomes?

---

### Module 5: Практика — мини-проект (60 мин)

#### Сценарий

```
Feature: User Profile Photo Upload

Problem:
Users cannot upload profile photos. This makes the platform feel outdated
and impersonal. Competitor X has had this feature for 2 years.

Business Impact:
- User satisfaction score: 3.2/5 (target: 4.0)
- 40% of users have default avatar (looks unprofessional)
- Sales team reports this as top-5 objection

Success Criteria:
- >60% of active users upload photo within 3 months
- User satisfaction increases to 3.8/5
- Zero security incidents related to uploads

Constraints:
- Must ship in 2 weeks (marketing campaign)
- Max file size: 5MB
- Formats: JPG, PNG only
- Must work on mobile and web
```

#### Задание (50 мин)

**Phase 1: Problem Statement** (10 мин)
- Напишите Problem Statement используя Before/After Bridge
- Примените 5 Whys для root cause

**Phase 2: Requirements** (15 мин)
- Напишите 8-10 требований в EARS
- Покройте все 5 паттернов
- Включите non-functional requirements

**Phase 3: ADR** (15 мин)
- Определите 2-3 архитектурных решения
- Напишите ADR для каждого (можно Y-Statements для простых)

**Phase 4: Presentation** (10 мин)
- Каждая группа презентует (3 мин)
- Feedback от других групп и фасилитатора

#### Evaluation Criteria

```markdown
## Evaluation Checklist

### Problem Statement (20 points)
- [ ] Specific with evidence (5 pts)
- [ ] Clear impact explained (5 pts)
- [ ] No solution included (5 pts)
- [ ] Testable success criteria (5 pts)

### Requirements (40 points)
- [ ] All 5 EARS patterns used (10 pts)
- [ ] Specific and testable (10 pts)
- [ ] Non-functional included (10 pts)
- [ ] Proper REQ-IDs (10 pts)

### ADR (30 points)
- [ ] Appropriate decisions selected (10 pts)
- [ ] Alternatives considered (10 pts)
- [ ] Consequences (good and bad) listed (10 pts)

### Presentation (10 points)
- [ ] Clear explanation (5 pts)
- [ ] Answered questions (5 pts)

Total: ___/100 points
```

---

## Role-Specific Training

### Product Manager Track

**Фокус**: PRD, Problem Statement, Requirements prioritization

**Материалы**:

#### PRD Workshop (2 часа)

```markdown
# PRD Writing Workshop

## Agenda
1. PRD structure deep dive (30 мин)
2. User story writing (30 мин)
3. Success metrics definition (30 мин)
4. Stakeholder alignment (30 мин)

## Exercise: Write a PRD

Scenario: "Add dark mode to mobile app"

### Step 1: Problem (15 мин)
- User research findings
- Competitor analysis
- Business opportunity

### Step 2: Goals & Metrics (15 мин)
- SMART goals
- Quantitative metrics
- Timeline

### Step 3: User Stories (20 мин)
- As a [user], I want [goal], so that [benefit]
- Prioritize: Must/Should/Could
- Acceptance criteria

### Step 4: Constraints (10 мин)
- Technical limitations
- Timeline
- Resources

### Step 5: Review (20 мин)
- Peer review
- Stakeholder feedback simulation
```

#### Requirements Prioritization (1 час)

```markdown
# Prioritization Frameworks

## MoSCoW Method
- **Must have**: Critical for launch
- **Should have**: Important but not critical
- **Could have**: Nice to have
- **Won't have**: Explicitly excluded

## RICE Score
- **Reach**: How many users?
- **Impact**: How much impact per user?
- **Confidence**: How confident are we?
- **Effort**: How much work?

Score = (Reach × Impact × Confidence) / Effort

## Exercise
Prioritize these features using RICE:
1. Dark mode
2. Push notifications
3. Offline support
4. Social sharing
5. Custom themes
```

### Developer Track

**Фокус**: Approach, Tasks, Implementation, AI-agent workflows

**Материалы**:

#### Technical Design Workshop (3 часа)

```markdown
# From Requirements to Code

## Agenda
1. Approach writing (60 мин)
2. Task breakdown (45 мин)
3. Implementation workflow (45 мин)
4. AI-agent integration (30 мин)

## Exercise: Design a Feature

Feature: "Rate limiting for API"

### Step 1: Approach (60 мин)
Write technical approach including:
- Architecture diagram (Mermaid)
- Data flow
- Key design decisions
- Error handling
- Performance considerations

### Step 2: Tasks (45 мин)
Break down into tasks:
- Phase 1: Setup
- Phase 2: Core implementation
- Phase 3: Testing
- Phase 4: Deployment

Each task needs:
- Description
- Acceptance criteria
- Dependencies
- Estimate (S/M/L)

### Step 3: Implementation Plan (45 мин)
- Choose 2-3 tasks to implement
- Write pseudo-code
- Define tests

### Step 4: AI Workflow (30 мин)
- Write prompts for AI-agent
- Review AI output
- Iterate and refine
```

#### AI-Agent Integration (2 часа)

```markdown
# Working with AI Agents Effectively

## Principles
1. Context is King
2. Iteration over Perfection
3. Verification is Mandatory
4. Human-in-the-Loop for decisions

## Prompt Engineering

### Bad Prompt
"Write code for user authentication"

### Good Prompt
"Implement JWT-based authentication for our FastAPI application.

Context:
- Framework: FastAPI
- Database: PostgreSQL with SQLAlchemy
- Requirements: REQ-AUTH-001 through REQ-AUTH-015

Generate:
1. Authentication endpoints (login, logout, refresh)
2. JWT token generation and validation
3. Middleware for protected routes
4. Unit tests for each component

Follow these requirements:
- REQ-AUTH-001: All endpoints require HTTPS
- REQ-AUTH-002: Access tokens expire in 15 minutes
- REQ-AUTH-003: Refresh tokens expire in 7 days

Include error handling for:
- Invalid credentials
- Expired tokens
- Token tampering

Reference requirement IDs in code comments."

## Exercise: Prompt Writing

Write prompts for:
1. Generate requirements from problem statement
2. Create technical approach
3. Break down into tasks
4. Generate code for a task
5. Write tests

## Verification Checklist
- [ ] Output matches requirements
- [ ] No hallucinations (verified facts)
- [ ] Follows established patterns
- [ ] Error handling included
- [ ] Tests provided
```

### Architect Track

**Фокус**: ADR, RFC, Architecture diagrams, Decision-making

**Материалы**:

#### Architecture Decision Making (3 часа)

```markdown
# Making Better Architecture Decisions

## Agenda
1. Decision frameworks (60 мин)
2. RFC writing (60 мин)
3. Architecture diagrams (45 мин)
4. Coaching others (15 мин)

## Decision Frameworks

### Decision Matrix
| Criteria | Weight | Option A | Option B | Option C |
|----------|--------|----------|----------|----------|
| Performance | 30% | 8/10 | 6/10 | 9/10 |
| Cost | 25% | 9/10 | 8/10 | 5/10 |
| Maintainability | 25% | 7/10 | 9/10 | 6/10 |
| Team expertise | 20% | 8/10 | 7/10 | 4/10 |
| **Total** | **100%** | **8.0** | **7.4** | **6.3** |

### Trade-off Analysis
For each option:
- What do we gain?
- What do we lose?
- What risks do we accept?
- What opportunities do we miss?

## Exercise: Architecture Decision

Scenario: "Choose a database for our new analytics platform"

Requirements:
- Handle 1B+ records
- Complex analytical queries
- Real-time dashboards
- Team has SQL experience

Options:
1. PostgreSQL
2. ClickHouse
3. Snowflake
4. Custom solution

### Task 1: Decision Matrix (20 мин)
Create weighted decision matrix

### Task 2: Trade-off Analysis (20 мин)
Analyze pros/cons for each option

### Task 3: Write ADR (20 мин)
Document decision in MADR format

## RFC Writing

### Structure
1. Summary (2-3 sentences)
2. Context and Problem
3. Proposal (with diagrams)
4. Alternatives Considered
5. Trade-offs and Risks
6. Open Questions
7. Timeline

### Exercise: Write an RFC (60 мин)

Scenario: "Migrate from monolith to microservices"

Write RFC including:
- Current state analysis
- Proposed architecture
- Migration strategy
- Risks and mitigations
- Timeline (phased approach)
```

### QA Engineer Track

**Фокус**: Requirements validation, BDD, Testing strategy

**Материалы**:

#### BDD Workshop (3 часа)

```markdown
# Behavior-Driven Development

## Agenda
1. BDD principles (30 мин)
2. Gherkin syntax (60 мин)
3. Writing scenarios (60 мин)
4. Step definitions (30 мин)

## BDD Principles
1. Collaboration across roles
2. Small iterations with feedback
3. Executable documentation

## Gherkin Syntax

```gherkin
Feature: [Feature name]
  As a [user]
  I want [goal]
  So that [benefit]

  Background:
    Given [common setup]

  Rule: [Business rule]
    Scenario: [Scenario name]
      Given [precondition]
      When [action]
      Then [expected result]
      And [additional result]
```

## Exercise: Write BDD Scenarios (60 мин)

Feature: User login

### Task 1: Identify scenarios (15 мин)
- Happy path
- Invalid credentials
- Account locked
- Session expired

### Task 2: Write scenarios (30 мин)
Write Gherkin for each scenario

### Task 3: Review (15 мин)
- Are scenarios specific?
- Do they cover requirements?
- Are they independent?

## Step Definitions

### Example (Python + Behave)

```python
from behave import given, when, then

@given('user "{name}" with password "{password}" exists')
def step_impl(context, name, password):
    context.user = create_user(name, password)

@when('{name} submits credentials')
def step_impl(context, name):
    context.response = login(name, context.password)

@then('{name} is authenticated')
def step_impl(context, name):
    assert context.response.status_code == 200
    assert 'token' in context.response.json()
```

### Exercise: Write step definitions (30 мин)
Implement steps for your scenarios
```

---

## Onboarding Checklists

### New Team Member (First Week)

```markdown
# Week 1 Onboarding Checklist

## Day 1: Orientation
- [ ] Meet the team
- [ ] Setup development environment
- [ ] Get access to repositories
- [ ] Read team documentation guide
- [ ] Review existing ADRs (docs/adr/)

## Day 2: Process Overview
- [ ] Attend "Introduction to Process" training (Module 1)
- [ ] Read: modules/problem-statement.md
- [ ] Read: modules/requirements.md
- [ ] Read: modules/adr.md
- [ ] Review end-to-end example (examples/export-service/)

## Day 3: Hands-on Practice
- [ ] Complete Problem Statement exercise
- [ ] Complete Requirements (EARS) exercise
- [ ] Complete ADR writing exercise
- [ ] Shadow a senior developer on a feature

## Day 4: Real Work
- [ ] Pick up small task (bug fix or enhancement)
- [ ] Write Problem Statement (even for small tasks)
- [ ] Write basic Requirements
- [ ] Create ADR if architectural decision needed
- [ ] Submit PR with documentation

## Day 5: Review
- [ ] Code review with mentor
- [ ] Feedback on documentation quality
- [ ] Identify areas for improvement
- [ ] Plan Week 2 learning goals

## Resources
- [Modules Index](../../modules/README.md)
- [Tools & Automation](../../tools-automation/README.md)
- [AI-Agent Workflows](../../ai-agent-workflows/README.md)
- [Metrics & Dashboards](../../metrics-dashboards/README.md)
```

### New Tech Lead (First Month)

```markdown
# Month 1 Tech Lead Onboarding

## Week 1: Foundation
- [ ] Complete Level 1 training (Foundation)
- [ ] Complete Level 2 training (Practitioner)
- [ ] Review all existing documentation
- [ ] Understand current metrics and dashboards
- [ ] Meet with PMs and understand product roadmap

## Week 2: Advanced
- [ ] Complete Level 3 training (Expert)
- [ ] Review recent RFCs and ADRs
- [ ] Understand team's pain points with process
- [ ] Identify process improvements
- [ ] Shadow architectural decision meetings

## Week 3: Coaching
- [ ] Conduct onboarding for new team member
- [ ] Lead a requirements writing workshop
- [ ] Review team's documentation quality
- [ ] Provide feedback on ADRs and RFCs
- [ ] Establish regular documentation review cadence

## Week 4: Leadership
- [ ] Lead an RFC process
- [ ] Make architectural decisions (write ADRs)
- [ ] Optimize team's workflow
- [ ] Present process improvements to stakeholders
- [ ] Plan next quarter's training schedule

## Success Criteria
- [ ] Can explain process to new team members
- [ ] Can write high-quality ADRs and RFCs
- [ ] Can coach others on documentation
- [ ] Team's documentation quality improved
- [ ] Process bottlenecks identified and addressed
```

---

## Common Mistakes и как их избежать

### Mistake 1: Over-documentation

**Проблема**: Документируем каждую мелочь  
**Симптомы**: 
- Bug fix имеет PRD, RFC и 5 ADR
- Команда тратит больше времени на документацию чем на код
- Burnout от bureaucracy

**Решение**:
```markdown
## Decision Matrix: Когда документировать?

| Задача | Problem Statement | Requirements | ADR | Approach | Tasks |
|--------|------------------|--------------|-----|----------|-------|
| Bug fix (< 1 день) | В commit message | ❌ | ❌ | ❌ | ❌ |
| Small feature (1-3 дня) | ✅ | ✅ | Если нужно | ❌ | ✅ |
| Medium feature (1-2 недели) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Large feature (1+ месяц) | ✅ | ✅ | ✅ | ✅ | ✅ |
| New product | ✅ | ✅ | ✅ | ✅ | ✅ |
```

### Mistake 2: Under-documentation

**Проблема**: Не документируем важные решения  
**Симптомы**:
- Одинаковые обсуждения повторяются
- Новые члены команды теряются
- Решения теряются в Slack

**Решение**:
```markdown
## Minimum Viable Documentation

Для ЛЮБОЙ задачи (даже bug fix):
- Problem Statement (в commit message или PR description)
- Requirements (если не очевидно)
- ADR (если архитектурное решение)

Для фичи > 1 день:
- Все вышеперечисленное +
- Approach (technical design)
- Tasks (breakdown)
- Tests

Для фичи > 1 неделя:
- Все вышеперечисленное +
- PRD (если product decision)
- RFC (если нужны дебаты)
- BDD (если критические business rules)
```

### Mistake 3: Solution in Problem Statement

**Проблема**: Пишем решение вместо проблемы  
**Пример**:
```
❌ Bad: "Problem: We need to migrate to PostgreSQL"
✅ Good: "Problem: Current database (MongoDB) cannot handle complex JOINs.
         Reports take 5+ minutes. Engineering spends 10h/week optimizing queries."
```

**Решение**: Всегда спрашивайте "Почему это проблема?"

### Mistake 4: Vague Requirements

**Проблема**: Требования без конкретики  
**Примеры**:
```
❌ "System should be fast"
❌ "Handle errors gracefully"
❌ "User-friendly interface"

✅ "API shall respond within 200ms for 95th percentile"
✅ "If DB fails, retry 3x with exponential backoff, then return 503"
✅ "New users shall complete onboarding within 5 minutes"
```

**Решение**: Используйте SMART критерии + конкретные числа

### Mistake 5: Missing Error Handling

**Проблема**: Документируем только happy path  
**Симптомы**:
- Production surprises
- Unexpected errors
- Poor user experience

**Решение**: Всегда включайте Unwanted pattern (If/Then)
```markdown
## Requirements Checklist

- [ ] Happy path covered (Event-driven, State-driven)
- [ ] Error scenarios covered (Unwanted: If/Then)
- [ ] Edge cases covered
- [ ] Performance under load
- [ ] Security considerations
```

### Mistake 6: ADR Without Alternatives

**Проблема**: ADR без анализа альтернатив  
**Пример**:
```
❌ Bad: "We chose PostgreSQL because it's good"
✅ Good: "Considered: PostgreSQL, MySQL, MongoDB
         Chose PostgreSQL because: excellent JOINs, ACID, team experience
         Trade-offs: migration effort, less flexible schema"
```

**Решение**: Всегда включайте минимум 2-3 альтернативы + "do nothing"

### Mistake 7: No Verification

**Проблема**: Документация есть, но никто не проверяет  
**Симптомы**:
- Documentation drift
- Outdated docs
- Broken cross-references

**Решение**: Автоматические проверки + manual review
```yaml
# GitHub Actions для verification
- EARS format linter
- Requirements coverage check
- Architecture compliance check
- Cross-reference validation
- Test coverage check
```

### Mistake 8: AI as Black Box

**Проблема**: Принимаем AI output без проверки  
**Симптомы**:
- Hallucinations в продакшене
- Неправильные архитектурные решения
- Security vulnerabilities

**Решение**: Human-in-the-loop для критических решений
```markdown
## AI Output Verification Checklist

- [ ] Facts verified (no hallucinations)
- [ ] Requirements covered
- [ ] Architecture aligns with ADRs
- [ ] Error handling included
- [ ] Security considerations addressed
- [ ] Tests provided and passing
```

---

## Workshop Materials

### Workshop 1: Documentation as Code (Half-day)

**Цель**: Внедрить documentation-first подход  
**Участники**: Вся команда (8-12 человек)  
**Длительность**: 4 часа

**Agenda**:
```
09:00 - 09:30  Введение и мотивация (30 мин)
09:30 - 10:15  Problem Statement workshop (45 мин)
10:15 - 10:30  Coffee break (15 мин)
10:30 - 11:30  Requirements (EARS) workshop (60 мин)
11:30 - 12:15  ADR workshop (45 мин)
12:15 - 13:00  Mini-project practice (45 мин)
```

**Материалы**:
- Презентация (PDF)
- Exercise sheets (Markdown)
- Примеры (end-to-end example)
- Evaluation rubric

**Подготовка**:
```bash
# За день до workshop
1. Распечатать exercise sheets
2. Подготовить flip charts и маркеры
3. Настроить проектор
4. Создать Slack channel для вопросов
5. Отправить pre-reading materials

# В день workshop
1. Прийти за 30 минут
2. Настроить оборудование
3. Раздать материалы
4. Начать вовремя
```

**Follow-up**:
```markdown
## Post-Workshop Actions

### Immediately (same day)
- [ ] Send thank you email с materials
- [ ] Share photos от workshop
- [ ] Collect feedback (Google Forms)

### Within 1 week
- [ ] Review feedback и identify improvements
- [ ] Schedule 1-on-1 с участниками у кого были вопросы
- [ ] Update training materials based on feedback
- [ ] Plan follow-up workshop (Level 2)

### Within 1 month
- [ ] Check adoption rate (метрики)
- [ ] Identify champions и barriers
- [ ] Provide additional coaching where needed
- [ ] Celebrate wins (share success stories)
```

### Workshop 2: AI-Agent Integration (Half-day)

**Цель**: Научить команду эффективно работать с AI-агентами  
**Участники**: Developers + Architects (6-10 человек)  
**Длительность**: 4 часа

**Agenda**:
```
09:00 - 09:30  AI principles и patterns (30 мин)
09:30 - 10:30  Prompt engineering workshop (60 мин)
10:30 - 10:45  Coffee break (15 мин)
10:45 - 11:45  Hands-on: AI для requirements (60 мин)
11:45 - 12:30  Hands-on: AI для code generation (45 мин)
12:30 - 13:00  Verification и quality gates (30 мин)
```

**Материалы**:
- Prompt templates library
- AI-agent workflows guide
- Example prompts (good vs bad)
- Verification checklists

**Упражнения**:
1. Write prompts for each module
2. Generate requirements from problem statement
3. Generate approach from requirements
4. Generate code from tasks
5. Review AI output

### Workshop 3: RFC Process (Half-day)

**Цель**: Внедрить RFC-driven development для архитектурных решений  
**Участники**: Senior developers + Architects (6-8 человек)  
**Длительность**: 4 часа

**Agenda**:
```
09:00 - 09:45  RFC principles и examples (45 мин)
09:45 - 10:45  Writing RFC workshop (60 мин)
10:45 - 11:00  Coffee break (15 мин)
11:00 - 12:00  Review process simulation (60 мин)
12:00 - 12:45  Decision-making и ADR creation (45 мин)
12:45 - 13:00  Wrap-up и next steps (15 мин)
```

**Упражнения**:
1. Identify decisions that need RFC
2. Write RFC for real architectural decision
3. Simulate review process (authors + reviewers)
4. Make decision и create ADR
5. Plan implementation

---

## Evaluation и Certification

### Level 1 Certification (Foundation)

**Requirements**:
- [ ] Attend Level 1 training (4 hours)
- [ ] Complete all exercises with passing score (≥70%)
- [ ] Submit mini-project documentation
- [ ] Pass quiz (20 questions, ≥80% correct)

**Quiz Topics**:
```markdown
## Level 1 Quiz

### Problem Statement (5 questions)
1. Что должно быть в Problem Statement?
2. Какие техники формулировки вы знаете?
3. Как избежать "solution in disguise"?
4. Что такое 5 Whys?
5. Как проверить quality Problem Statement?

### Requirements (8 questions)
1. Что такое EARS?
2. Назовите 5 паттернов EARS
3. Какой паттерн для "always active" requirements?
4. Какой паттерн для error handling?
5. Как сделать требование testable?
6. Что такое atomicity?
7. Как избежать vague language?
8. Что такое non-functional requirements?

### ADR (7 questions)
1. Что такое ADR?
2. Когда создавать ADR?
3. Когда НЕ создавать ADR?
4. Назовите форматы ADR
5. Что должно быть в ADR?
6. Что такое supersession?
7. Где хранить ADR?
```

**Certification**:
- Digital badge (можно share в LinkedIn)
- Access to advanced workshops
- Recognition in team

### Level 2 Certification (Practitioner)

**Requirements**:
- [ ] Level 1 certification
- [ ] Attend Level 2 training (8 hours)
- [ ] Complete real project with full documentation
- [ ] Peer review от 2 коллег
- [ ] Presentation to team

**Project Requirements**:
```markdown
## Level 2 Project

Choose a real feature you're working on (1-2 weeks scope)

Deliverables:
1. Problem Statement (approved)
2. Requirements in EARS (≥10 requirements, all patterns)
3. Approach with diagrams
4. Tasks breakdown (≥10 tasks)
5. Implementation (code + tests)
6. ADR(s) for decisions (if any)

Quality Criteria:
- All requirements covered by tests
- Documentation passes automated checks
- Peer review score ≥ 80%
- No major issues found in production (1 month)
```

### Level 3 Certification (Expert)

**Requirements**:
- [ ] Level 2 certification
- [ ] Attend Level 3 training (8 hours)
- [ ] Lead RFC process for architectural decision
- [ ] Coach 2 new team members
- [ ] Conduct workshop для команды
- [ ] Contribute to process improvements

**Expert Responsibilities**:
```markdown
## Expert Role

### Coaching
- Onboard new team members
- Review documentation quality
- Provide feedback on ADRs/RFCs
- Answer questions in team channel

### Leadership
- Lead RFC processes
- Make architectural decisions
- Write complex ADRs
- Resolve documentation conflicts

### Improvement
- Identify process bottlenecks
- Propose improvements
- Update training materials
- Share best practices

### Metrics
- Team documentation quality score
- Onboarding time for new members
- RFC approval rate
- Process adoption rate
```

---

## Resources

### Documentation
- [Modules Index](../../modules/README.md) — все модули
- [Tools & Automation](../../tools-automation/README.md) — инструменты
- [AI-Agent Workflows](../../ai-agent-workflows/README.md) — работа с AI
- [Metrics & Dashboards](../../metrics-dashboards/README.md) — метрики
- [End-to-End Example](../../examples/export-service/README.md) — полный пример

### Templates
- Problem Statement template
- Requirements (EARS) template
- ADR templates (Nygard, MADR, Y-Statements)
- Approach template
- Tasks template
- PRD template
- RFC template
- BDD scenarios template

### Tools
- [adr-tools](https://github.com/npryce/adr-tools) — CLI для ADR
- [Log4brains](https://github.com/thomvaill/log4brains) — ADR publishing
- [Spectral](https://github.com/stoplightio/spectral) — API linting
- [GitHub Spec Kit](https://github.com/github/spec-kit) — SDD workflow
- [MkDocs](https://www.mkdocs.org) — documentation site

### Communities
- [EARS Community](https://alistairmavin.com/ears)
- [ADR GitHub](https://adr.github.io)
- [Cucumber Community](https://cucumber.io/community)
- [Documentation as Code Slack](https://docsascode.slack.com)

### Books
- "Documentation as Code" — Tom Johnson
- "Software Requirements" — Karl Wiegers
- "Building Evolutionary Architectures" — Neal Ford
- "Team Topologies" — Matthew Skelton

### Courses
- [IREB Requirements Engineering](https://www.ireb.org)
- [C4 Model Course](https://c4model.com)
- [BDD Foundation](https://cucumber.io/training)

---

## Summary

**Обучение и Onboarding** — это:

1. **Структурированный подход** — 3 уровня (Foundation, Practitioner, Expert)
2. **Role-specific треки** — PM, Developer, Architect, QA, Tech Lead
3. **Hands-on практика** — workshops с реальными упражнениями
4. **Onboarding checklists** — для новых членов команды
5. **Common mistakes** — и как их избежать
6. **Certification** — с evaluation criteria

**Ключевые принципы**:
- Learning by doing (70% practice, 30% theory)
- Progressive complexity (simple → complex)
- Peer learning (workshops, pair exercises)
- Continuous improvement (feedback loops)

**Success metrics**:
- Documentation quality score
- Onboarding time
- Process adoption rate
- Team satisfaction

**Next steps**:
1. Провести pilot workshop с командой
2. Собрать feedback
3. Iterate и улучшить materials
4. Scale на всю организацию
5. Establish regular training cadence
