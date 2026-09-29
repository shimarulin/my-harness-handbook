# ADR (Architecture Decision Record)

Третий модуль Core Foundation. ADR — это короткая, фокусированная запись единственного архитектурного решения: что выбрали, контекст, вынудивший выбор, альтернативы и последствия. Одно решение — одна запись.

---

## Что такое ADR

**Architecture Decision Record (ADR)** — документ, который фиксирует:
- **Что** решили
- **Почему** решили (контекст и drivers)
- **Какие альтернативы** рассматривали
- **Какие последствия** решения (хорошие и плохие)

**Это НЕ**:
- RFC (предложение для обсуждения)
- PRD (продуктовые требования)
- Техническая спецификация (это Design/Approach)
- README (общая документация)

**Это**:
- Immutable record принятого решения
- Контекст для будущих разработчиков
- Rationale для выбора
- История эволюции архитектуры

---

## Когда создавать ADR

### Обязательно создавать ADR когда:

1. **Выбор technology stack**
   - Database (PostgreSQL vs MySQL vs MongoDB)
   - Framework (React vs Vue vs Svelte)
   - Message queue (RabbitMQ vs Kafka vs Redis)
   - Cloud provider (AWS vs GCP vs Azure)

2. **Архитектурные паттерны**
   - Microservices vs monolith
   - Event-driven vs request-response
   - REST vs GraphQL vs gRPC
   - CQRS vs CRUD

3. **Data model decisions**
   - Schema design
   - Sharding strategy
   - Caching layer
   - Data retention policy

4. **Integration choices**
   - External APIs
   - Authentication/authorization (OAuth vs JWT vs sessions)
   - Third-party services

5. **Deployment strategy**
   - Containerization (Docker vs Podman)
   - Orchestration (Kubernetes vs ECS vs Cloud Run)
   - CI/CD tools (GitHub Actions vs GitLab CI)

6. **Security decisions**
   - Encryption strategy
   - Key management
   - Authentication mechanism

7. **Performance trade-offs**
   - Consistency vs availability (CAP theorem)
   - Latency vs throughput
   - Cost vs performance

### НЕ создавать ADR когда:

- ❌ Trivial decisions (названия переменных, форматирование)
- ❌ Already decided (если есть existing ADR)
- ❌ Temporary/experimental (PoC, spike)
- ❌ Team preferences без architectural impact
- ❌ Bug fixes (если не меняют архитектуру)

---

## Форматы ADR

### 1. Nygard Format (Классический)

**Оригинал**: [Michael Nygard, 2011](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions)

**Когда использовать**:
- Маленькие команды
- Простые решения
- Быстрый старт
- Минимум bureaucracy

**Шаблон**:

```markdown
# ADR <NNN>: <Title>

## Status
[proposed | accepted | deprecated | superseded by ADR-XXX]

## Context
Опишите силы в игре (technological, political, social, project local).
Эти силы вероятно в tension. Что заставило нас принять это решение?

## Decision
Наш ответ на эти силы. Полные предложения, active voice.
"We will..."

## Consequences
Результирующий контекст после применения решения.
ВСЕ последствия должны быть здесь, не только "positive" ones.
```

**Пример**:

```markdown
# ADR 007: Use PostgreSQL for primary database

## Status
Accepted

## Context
Our current MongoDB setup cannot handle complex JOINs efficiently. 
Reports that should take 5 seconds take 5 minutes. We need a 
relational database with strong ACID guarantees and good JOIN 
performance. Team has experience with both PostgreSQL and MySQL.

## Decision
We will use PostgreSQL 15 as our primary database.

## Consequences
- Good: Excellent JOIN performance for complex queries
- Good: Strong ACID guarantees
- Good: Rich ecosystem of tools (pgAdmin, Postico)
- Good: Team has prior experience
- Bad: Need to migrate existing MongoDB data (2 weeks effort)
- Bad: Less flexible schema than MongoDB
- Bad: Need to learn PostgreSQL-specific features (JSONB, CTEs)
- Risk: Migration may cause downtime (plan for maintenance window)
```

---

### 2. MADR (Markdown Architectural Decision Records)

**Официальный сайт**: https://adr.github.io/madr

**Когда использовать**:
- Средние команды
- Нужен structured подход
- Want Decision Drivers и Options analysis
- Интеграция с tooling (adr-tools, linting)

**Полный шаблон**:

```markdown
# <Title>

* Status: [proposed | rejected | accepted | deprecated | superseded by [ADR-NNN](./adr-NNN.md)]
* Deciders: [list everyone involved in the decision]
* Date: [YYYY-MM-DD when the decision was last updated]

Technical Story: [description | ticket/issue | URL | ...]

## Context and Problem Statement

[Describe the context and problem statement, e.g., in free form using two to three sentences or in the form of an illustrative story. It may be desirable to split the section into "Context" and "Problem Statement" if the context description is more extensive.]

## Decision Drivers

* [driver 1, e.g., a force, facing concern, ...]
* [driver 2, e.g., a force, facing concern, ...]
* ...

## Considered Options

* [title of option 1]
* [title of option 2]
* [title of option 3]
* ...

## Decision Outcome

Chosen option: "[title of option 1]", because [justification. e.g., only option, which meets k.o. criterion decision driver | which resolves force force | ... | comes out best (see below)].

### Consequences

* Good, because [positive consequence, e.g., improvement of one or more desired qualities, ...]
* Bad, because [negative consequence, e.g., compromising one or more desired qualities, ...]
* ...

### Confirmation

[Describe how the implementation/compliance with the decision can be confirmed. Is the decision even implemented/complied with?]

## Pros and Cons of the Options

### [title of option 1]

[example | description | pointer to more information | ...]

* Good, because [argument a]
* Good, because [argument b]
* ...
* Bad, because [argument c]
* Bad, because [argument d]
* ...

### [title of option 2]

[example | description | pointer to more information | ...]

* Good, because [argument a]
* Good, because [argument b]
* ...
* Bad, because [argument c]
* Bad, because [argument d]
* ...

## More Information

[More information, e.g., links to external resources, related ADRs, ...]
```

**Минимальный шаблон**:

```markdown
# <Title>

* Status: [proposed | rejected | accepted | deprecated | superseded by [ADR-NNN](./adr-NNN.md)]
* Date: [YYYY-MM-DD]

## Context and Problem Statement

[Describe the context and problem statement]

## Considered Options

* [title of option 1]
* [title of option 2]
* [title of option 3]

## Decision Outcome

Chosen option: "[title of option 1]", because [justification].

### Consequences

* Good, because [positive consequence]
* Bad, because [negative consequence]
```

**Пример (Full MADR)**:

```markdown
# Use Celery for async task processing

* Status: accepted
* Deciders: @alice, @bob, @charlie
* Date: 2025-01-15

Technical Story: [TASK-1234](https://jira.example.com/browse/TASK-1234)

## Context and Problem Statement

Our data export feature requires long-running operations (10 seconds to 1 hour).
Synchronous processing blocks API responses and causes timeouts. We need an
async task processing solution that:
- Handles tasks from 10 seconds to 1 hour
- Provides retry mechanism for failures
- Scales horizontally with our worker fleet
- Integrates well with our Python/FastAPI stack
- Has good monitoring and debugging tools

## Decision Drivers

* Task duration: 10 seconds to 1 hour (need long-running support)
* Reliability: must retry failed tasks automatically
* Scalability: need to add workers dynamically based on queue size
* Observability: need to monitor queue depth, task duration, failures
* Team familiarity: team has Python expertise, limited Go experience
* Infrastructure: already running Redis for caching

## Considered Options

* Celery + Redis
* RQ (Redis Queue)
* AWS SQS + Lambda
* Custom background workers (Python threading/multiprocessing)
* Dramatiq

## Decision Outcome

Chosen option: "Celery + Redis", because:
- Mature, battle-tested solution (10+ years in production)
- Rich feature set: retries, scheduling, rate limiting, monitoring
- Excellent Python integration
- Redis already in use (no new infrastructure)
- Flower UI for monitoring
- Large community and documentation

### Consequences

* Good, because well-documented with large community
* Good, because Flower provides excellent monitoring UI
* Good, because supports task priorities and routing
* Good, because integrates with our existing Redis infrastructure
* Bad, because adds operational complexity (need to manage Celery workers)
* Bad, because steeper learning curve than simpler solutions (RQ)
* Bad, because some advanced features (Canvas workflows) have quirks
* Risk: Celery workers can consume significant memory if not configured properly

### Confirmation

* [ ] Celery workers deployed to staging
* [ ] Export tasks successfully queued and processed
* [ ] Flower UI accessible and showing task metrics
* [ ] Retry mechanism tested with simulated failures
* [ ] Memory usage monitored under load

## Pros and Cons of the Options

### Celery + Redis

* Good, because mature and battle-tested (10+ years)
* Good, because rich feature set (retries, scheduling, monitoring)
* Good, because excellent Python integration
* Good, because uses existing Redis infrastructure
* Good, because Flower UI for monitoring
* Bad, because operational complexity (worker management)
* Bad, because steeper learning curve
* Bad, because some advanced features have quirks

### RQ (Redis Queue)

* Good, because simpler than Celery
* Good, because also uses Redis
* Good, because easier to learn
* Bad, because fewer features (no built-in retries, scheduling)
* Bad, because less mature ecosystem
* Bad, because limited monitoring tools

### AWS SQS + Lambda

* Good, because fully managed (no worker management)
* Good, because auto-scaling built-in
* Bad, because 15-minute timeout limit (our tasks can be 1 hour)
* Bad, because cold start latency
* Bad, because vendor lock-in to AWS
* Bad, because more expensive at scale

### Custom background workers

* Good, because full control
* Good, because no external dependencies
* Bad, because reinventing the wheel
* Bad, because need to build monitoring, retries, scaling
* Bad, because high maintenance burden
* Bad, because team would need to maintain this forever

### Dramatiq

* Good, because modern design
* Good, because better error handling than Celery
* Bad, because smaller community
* Bad, because fewer integrations
* Bad, because team unfamiliar

## More Information

* [Celery Documentation](https://docs.celeryq.dev)
* [ADR-002](./adr-002-use-redis-for-caching.md) - Redis already in use
* [ADR-015](./adr-015-async-processing-pattern.md) - General async strategy
* [Celery Best Practices](https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html#best-practices)
```

---

### 3. Y-Statements (Lightweight)

**Когда использовать**:
- Множество мелких решений
- Team agreements
- Быстрая фиксация без overhead
- Когда Nygard/MADR слишком тяжелые

**Формат**:

```
In the context of <use case>,
facing <concern>
we decided for <option>
to achieve <quality>,
accepting <downside>
```

**Примеры**:

```markdown
# Team Decisions

## Authentication
- In the context of user authentication, facing need for stateless tokens, 
  we decided for JWT to achieve scalability, accepting token revocation complexity

## Database
- In the context of user profiles, facing need for flexible schema, 
  we decided for PostgreSQL JSONB to achieve schema flexibility, accepting query complexity

## Caching
- In the context of API responses, facing need for low latency, 
  we decided for Redis to achieve sub-50ms response times, accepting cache invalidation complexity
```

**Где хранить**:
- `docs/decisions.md` (один файл для всех мелких решений)
- Inline в README или PR description
- В начале spec файла

---

### 4. YADR (YAML ADR)

**Когда использовать**:
- Machine-readable ADRs
- CI/CD pipelines
- Метрики и dashboards
- Автоматическая обработка

**Шаблон**:

```yaml
---
title: Use PostgreSQL for primary database
status: accepted
date: 2025-01-15
deciders:
  - alice
  - bob
  - charlie
context: |
  Our current MongoDB setup cannot handle complex JOINs efficiently.
  Reports that should take 5 seconds take 5 minutes.
decision: We will use PostgreSQL 15 as our primary database.
consequences:
  good:
    - Excellent JOIN performance
    - Strong ACID guarantees
    - Rich ecosystem of tools
  bad:
    - Need to migrate existing MongoDB data
    - Less flexible schema
    - Need to learn PostgreSQL-specific features
considered_options:
  - PostgreSQL
  - MySQL
  - MongoDB (current)
---

Detailed discussion and rationale can go here in free-form text.
```

**Инструменты**:
- YAML parsers для автоматической обработки
- Генерация reports и dashboards
- Интеграция с CI/CD

---

## Какой формат выбрать?

### Decision Matrix

```
Насколько сложное решение?

├─ Trivial (название переменной, форматирование)
│  └─ Не создавать ADR
│
├─ Small (library choice, minor config)
│  ├─ Много мелких решений?
│  │  └─ Y-Statements
│  └─ Одно решение?
│     └─ Nygard
│
├─ Medium (tech stack, pattern choice)
│  ├─ Нужен detailed analysis?
│  │  └─ MADR (full)
│  ├─ Нужен quick decision?
│  │  └─ MADR (minimal) или Nygard
│  └─ Нужна automation?
│     └─ YADR
│
└─ Large (architecture, platform)
   └─ MADR (full) с detailed pros/cons
```

### Сравнение форматов

| Формат | Сложность | Структура | Когда использовать |
|--------|-----------|-----------|-------------------|
| **Nygard** | Низкая | 5 секций | Quick decisions, small teams |
| **MADR (minimal)** | Низкая | 4 секции | Medium decisions, structured |
| **MADR (full)** | Средняя | 7+ секций | Important decisions, detailed analysis |
| **Y-Statements** | Очень низкая | 1 sentence | Many small decisions, team agreements |
| **YADR** | Низкая | YAML | Machine-readable, automation |

---

## Workflow: Создание ADR

### Шаг 1: Определить что это архитектурное решение

**Checklist**:
- [ ] Влияет ли это на multiple components?
- [ ] Есть ли multiple viable options?
- [ ] Сложно ли изменить позже?
- [ ] Есть ли significant trade-offs?
- [ ] Нужен ли consensus?

Если да → создавайте ADR.

### Шаг 2: Выбрать формат

Используйте decision matrix выше.

**Рекомендация**: Начните с MADR (minimal), upgrade до full если нужно.

### Шаг 3: Написать ADR

**Process**:
1. **Context**: Опишите проблему и силы в игре
2. **Options**: Перечислите все рассмотренные альтернативы
3. **Decision**: Что выбрали и почему
4. **Consequences**: ВСЕ последствия (хорошие, плохие, риски)
5. **Review**: Попросите коллегу ревьюить
6. **Commit**: Добавьте в репозиторий

### Шаг 4: Commit ADR

**Commit message**:
```
docs(adr): add ADR-007 use PostgreSQL for primary database

Context: MongoDB JOIN performance issues
Decision: Migrate to PostgreSQL 15
Consequences: Better JOINs, ACID guarantees, migration effort

Closes #1234
```

### Шаг 5: Update related ADRs

Если новое решение **supersedes** старое:

```markdown
# ADR 007: Use PostgreSQL for primary database

## Status
Accepted

*Supersedes [ADR-003](./adr-003-use-mongodb.md)*
```

И обновите старый ADR:

```markdown
# ADR 003: Use MongoDB for primary database

## Status
Superseded by [ADR-007](./adr-007-use-postgresql.md)

## Context
[original context]

## Decision
We will use MongoDB as our primary database.

## Consequences
[original consequences]

## Supersession
This decision was superseded by ADR-007 due to:
- Poor JOIN performance for complex queries
- Need for ACID guarantees
- Reports taking too long to generate
```

---

## Структура репозитория

### Вариант 1: Dedicated ADR directory

```
project/
├── docs/
│   ├── adr/
│   │   ├── README.md                    ← index всех ADRs
│   │   ├── adr-0001-use-jwt.md
│   │   ├── adr-0002-use-postgresql.md
│   │   ├── adr-0003-use-celery.md
│   │   └── ...
│   └── ...
└── src/
```

### Вариант 2: Feature-scoped ADRs

```
project/
├── features/
│   ├── export/
│   │   ├── spec.md
│   │   ├── design.md
│   │   ├── adr/
│   │   │   ├── adr-001-use-celery.md
│   │   │   └── adr-002-use-s3.md
│   │   └── ...
│   └── ...
```

### Вариант 3: Monorepo

```
monorepo/
├── packages/
│   ├── api/
│   │   ├── docs/
│   │   │   └── adr/
│   │   └── src/
│   └── web/
│       ├── docs/
│       │   └── adr/
│       └── src/
└── docs/
    └── adr/                               ← cross-package ADRs
```

---

## ADR Index

Создайте `docs/adr/README.md` как index всех ADRs:

```markdown
# Architecture Decision Records

This directory contains all architectural decisions for this project.

## Active Decisions

| ADR | Title | Status | Date | Deciders |
|-----|-------|--------|------|----------|
| [ADR-001](./adr-001-use-jwt.md) | Use JWT for authentication | Accepted | 2025-01-10 | @alice, @bob |
| [ADR-002](./adr-002-use-postgresql.md) | Use PostgreSQL for database | Accepted | 2025-01-12 | @alice, @charlie |
| [ADR-003](./adr-003-use-celery.md) | Use Celery for async tasks | Accepted | 2025-01-15 | @bob, @charlie |
| [ADR-004](./adr-004-use-redis.md) | Use Redis for caching | Proposed | 2025-01-20 | @alice |

## Superseded Decisions

| ADR | Title | Superseded By | Date |
|-----|-------|---------------|------|
| [ADR-000](./adr-000-use-mongodb.md) | Use MongoDB for database | ADR-002 | 2025-01-12 |

## How to Create a New ADR

1. Copy template: `cp template.md adr-NNN-title.md`
2. Fill in all sections
3. Get review from team
4. Commit with message: `docs(adr): add ADR-NNN title`
5. Update this index

## Templates

- [MADR Full](./templates/madr-full.md)
- [MADR Minimal](./templates/madr-minimal.md)
- [Nygard](./templates/nygard.md)
- [Y-Statement](./templates/y-statement.md)
```

---

## Инструменты

### adr-tools

**GitHub**: https://github.com/npryce/adr-tools

**Установка**:
```bash
brew install adr-tools  # macOS
# или
# Скачать и добавить в PATH
```

**Команды**:
```bash
# Инициализация
adr init

# Создать новый ADR
adr new Use PostgreSQL for database
# Создаст: doc/adr/0002-use-postgresql-for-database.md

# Supersede старый ADR
adr new -s 1 Use PostgreSQL for database
# Обновит ADR-001 как superseded

# Generate graph
adr generate graph
# Создаст DOT файл для визуализации

# Generate TOC
adr generate toc
# Обновит index
```

### Log4brains

**GitHub**: https://github.com/thomvaill/log4brains

**Описание**: Publish ADRs as static site

**Установка**:
```bash
npm install -g log4brains
```

**Использование**:
```bash
# Инициализация
log4brains init

# Создать ADR
log4brains adr new

# Preview
log4brains preview

# Build static site
log4brains build
```

**Features**:
- Automatic ADR generation
- Static site generation
- Search functionality
- Timeline view
- Git integration

### VS Code Extensions

**ADR Tools**: https://marketplace.visualstudio.com/items?itemName=jan-berger.adr-tools

**Features**:
- Snippets для ADR templates
- Navigation между ADRs
- Link validation

### GitHub Actions

**ADR Linter**:

```yaml
# .github/workflows/adr-lint.yml
name: ADR Lint

on:
  pull_request:
    paths:
      - 'docs/adr/**'

jobs:
  lint-adrs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check ADR format
        run: |
          # Проверить что все ADRs имеют required sections
          for file in docs/adr/adr-*.md; do
            grep -q "## Status" "$file" || exit 1
            grep -q "## Context" "$file" || exit 1
            grep -q "## Decision" "$file" || exit 1
            grep -q "## Consequences" "$file" || exit 1
          done
      - name: Check for broken links
        run: |
          # Проверить что superseded ссылки корректны
          grep -r "superseded by" docs/adr/ | while read line; do
            # Extract ADR number and check if file exists
            adr=$(echo "$line" | grep -oP 'ADR-\d+' | head -1)
            [ -f "docs/adr/${adr,,}.md" ] || exit 1
          done
```

---

## AI-Agent Integration

### Prompt: Генерация ADR из discussion

```
Based on this discussion, create an ADR in MADR format:

Discussion:
[paste discussion summary, Slack thread, meeting notes]

Include:
- Context and problem statement
- All options considered (with pros/cons)
- Decision outcome with justification
- Consequences (good, bad, risks)
- Confirmation steps
```

### Prompt: Ревью ADR

```
Review this ADR for:
1. Clarity: Is the context clear?
2. Completeness: Are all options considered?
3. Justification: Is the decision well-justified?
4. Consequences: Are all consequences (good and bad) listed?
5. Actionability: Can someone understand and implement this?

ADR:
[paste ADR content]

Provide:
- Issues found
- Suggestions for improvement
- Missing considerations
```

### Prompt: Генерация из Requirements

```
Based on these requirements, suggest architectural decisions 
that need ADRs:

Requirements:
[paste requirements]

For each suggested ADR:
- What decision needs to be made?
- What are the options?
- What are the key trade-offs?
```

### Prompt: Supersession

```
We're replacing [old technology] with [new technology]. 
Update the old ADR and create a new one:

Old ADR:
[paste old ADR]

New decision:
[describe new decision]

Generate:
1. Updated old ADR with "superseded by" status
2. New ADR with "supersedes" reference
3. Explanation of why we're changing
```

---

## Примеры по доменам

### Пример 1: Authentication

```markdown
# ADR 001: Use JWT for stateless authentication

## Status
Accepted

## Context
We need an authentication mechanism for our API that:
- Supports multiple client types (web, mobile, third-party)
- Scales horizontally (no shared session state)
- Works with our microservices architecture
- Provides good security guarantees

Our current session-based auth requires sticky sessions and doesn't
work well with our load balancer configuration.

## Decision Drivers
* Stateless: must not require server-side session storage
* Scalable: must work with horizontal scaling
* Secure: must prevent common attacks (CSRF, XSS, replay)
* Flexible: must support multiple client types
* Team familiarity: team has experience with both JWT and sessions

## Considered Options
* JWT (JSON Web Tokens)
* Session-based with Redis
* OAuth 2.0 with opaque tokens
* PASETO (Platform-Agnostic Security Tokens)

## Decision Outcome
Chosen option: "JWT", because:
- Stateless (no server-side storage needed)
- Well-supported across all platforms and languages
- Team has prior experience
- Large ecosystem of libraries and tools
- Industry standard for API authentication

### Consequences
* Good, because stateless (scales horizontally without sticky sessions)
* Good, because self-contained (token includes all user info)
* Good, because cross-domain/cross-origin friendly
* Good, because large ecosystem (libraries, tools, documentation)
* Bad, because tokens are larger than session IDs (more bandwidth)
* Bad, because token revocation is complex (need blacklist or short expiry)
* Bad, because sensitive data in token is visible (even if signed)
* Risk: long-lived tokens can be stolen and misused

### Confirmation
* [ ] JWT library integrated (PyJWT)
* [ ] Token generation endpoint implemented
* [ ] Token validation middleware implemented
* [ ] Token refresh mechanism implemented
* [ ] Token blacklist for logout/revocation
* [ ] Security review completed

## Pros and Cons of the Options

### JWT
* Good: Stateless, scalable
* Good: Self-contained, includes user info
* Good: Cross-domain friendly
* Good: Large ecosystem
* Bad: Larger token size
* Bad: Complex revocation
* Bad: Visible payload (don't store secrets)

### Session-based with Redis
* Good: Small token size (just session ID)
* Good: Easy revocation (delete session)
* Good: Can store large data server-side
* Bad: Requires Redis infrastructure
* Bad: Not truly stateless
* Bad: Sticky sessions or session replication needed

### OAuth 2.0 with opaque tokens
* Good: Industry standard for third-party access
* Good: Fine-grained scopes
* Good: Token introspection endpoint
* Bad: More complex setup
* Bad: Requires authorization server
* Bad: Overkill for first-party auth

### PASETO
* Good: More secure than JWT by design
* Good: No algorithm confusion attacks
* Bad: Smaller ecosystem
* Bad: Fewer libraries
* Bad: Team unfamiliar

## More Information
* [JWT.io](https://jwt.io) - JWT debugger and libraries
* [Auth0 JWT Handbook](https://auth0.com/resources/ebooks/jwt-handbook)
* [ADR-005](./adr-005-token-refresh-strategy.md) - Token refresh details
```

### Пример 2: Database

```markdown
# ADR 002: Use PostgreSQL for primary database

## Status
Accepted

*Supersedes [ADR-000](./adr-000-use-mongodb.md)*

## Context
Our current MongoDB setup (chosen in ADR-000 for flexible schema) is 
showing limitations:
- Complex reports with JOINs take 5+ minutes
- Need ACID guarantees for financial transactions
- Query optimization is difficult without proper relations
- Team spends 10 hours/week on MongoDB aggregation pipelines

## Decision Drivers
* Query performance: reports must complete in <5 seconds
* Data integrity: ACID guarantees for financial data
* Team productivity: reduce time on query optimization
* Ecosystem: good tooling and community support
* Migration cost: reasonable effort to migrate from MongoDB

## Considered Options
* PostgreSQL 15
* MySQL 8
* CockroachDB
* Stay with MongoDB + optimize

## Decision Outcome
Chosen option: "PostgreSQL 15", because:
- Excellent JOIN performance for complex queries
- Strong ACID guarantees
- Rich feature set (JSONB, CTEs, window functions)
- Large ecosystem of tools (pgAdmin, Postico, pganalyze)
- Team has prior experience
- Active development and community

### Consequences
* Good, because excellent JOIN performance (reports <5 seconds)
* Good, because ACID guarantees for financial data
* Good, because JSONB provides schema flexibility (best of both worlds)
* Good, because rich feature set (CTEs, window functions, etc.)
* Good, because excellent tooling ecosystem
* Bad, because need to migrate existing MongoDB data (2 weeks effort)
* Bad, because less flexible schema than pure MongoDB
* Bad, because need to learn PostgreSQL-specific features
* Risk: migration may cause downtime (plan maintenance window)

### Confirmation
* [ ] PostgreSQL 15 deployed to staging
* [ ] Schema designed and created
* [ ] Data migration script tested
* [ ] Application updated to use PostgreSQL
* [ ] Performance tests show reports <5 seconds
* [ ] Production migration completed

## Pros and Cons of the Options

### PostgreSQL 15
* Good: Excellent JOIN performance
* Good: Strong ACID guarantees
* Good: JSONB for flexible schema
* Good: Rich feature set
* Good: Large ecosystem
* Bad: Migration effort
* Bad: Less flexible than pure document store

### MySQL 8
* Good: Good performance
* Good: Widely used
* Good: Team familiar
* Bad: Fewer advanced features than PostgreSQL
* Bad: JSON support less mature
* Bad: Window functions added later

### CockroachDB
* Good: Distributed by design
* Good: PostgreSQL compatible
* Good: Strong consistency
* Bad: More complex to operate
* Bad: Smaller community
* Bad: Overkill for our scale

### Stay with MongoDB + optimize
* Good: No migration effort
* Good: Team already familiar
* Bad: Fundamental limitations remain
* Bad: Reports still slow
* Bad: No ACID guarantees
* Bad: Ongoing optimization burden

## More Information
* [PostgreSQL Documentation](https://www.postgresql.org/docs/)
* [MongoDB to PostgreSQL Migration Guide](https://www.postgresql.org/docs/current/migration.html)
* [ADR-000](./adr-000-use-mongodb.md) - Original decision
* [Migration Plan](https://confluence.example.com/display/ENG/PostgreSQL+Migration)
```

---

## Anti-patterns

### ❌ ADR for Trivial Decisions

**Bad**:
```markdown
# ADR 042: Use camelCase for variable names

## Context
We need to decide on naming convention.

## Decision
We will use camelCase.

## Consequences
- Good: Consistent code style
```

**Why bad**: Это не архитектурное решение, это coding standard. Используйте linter.

**Solution**: ADR только для решений с architectural impact.

---

### ❌ Missing Alternatives

**Bad**:
```markdown
# ADR 007: Use PostgreSQL

## Context
We need a database.

## Decision
We will use PostgreSQL because it's good.

## Consequences
- Good: PostgreSQL is reliable
```

**Why bad**: Нет анализа альтернатив. Не понятно почему именно PostgreSQL.

**Solution**: Всегда перечисляйте 2-4 альтернативы с pros/cons.

---

### ❌ Only Positive Consequences

**Bad**:
```markdown
## Consequences
- Good: Excellent performance
- Good: Easy to use
- Good: Well documented
```

**Why bad**: Нет честной оценки trade-offs. Будущие разработчики не поймут risks.

**Solution**: ВСЕГДА включайте negative consequences и risks.

---

### ❌ Vague Justification

**Bad**:
```markdown
## Decision
We will use React because it's popular and modern.
```

**Why bad**: Не объясняет почему React лучше Vue/Svelte для нашего случая.

**Solution**: Конкретные причины связанные с нашим контекстом.

**Good**:
```markdown
## Decision
We will use React because:
- Team has 3 years React experience (vs 6 months Vue)
- Large ecosystem for our specific needs (react-query, react-table)
- Better TypeScript support than Vue 3 at time of decision
```

---

### ❌ Not Updating Superseded ADRs

**Bad**: ADR-003 всё ещё "Accepted", хотя ADR-007 supersedes его.

**Why bad**: Confusion о текущем состоянии. Не ясно что в использовании.

**Solution**: Всегда обновляйте status старого ADR на "Superseded by ADR-XXX".

---

### ❌ ADR Without Implementation

**Bad**: ADR создан, но решение не реализовано.

**Why bad**: Documentation debt. ADR становится устаревшим.

**Solution**: Добавьте Confirmation section с checklist. Отслеживайте реализацию.

---

## Connection to Other Modules

### ← Problem Statement (вход)

**Как**: Problem statement определяет context для ADR

```
Problem: "Database queries too slow for real-time analytics"
    ↓
ADR Context: 
"Current MongoDB cannot handle complex JOINs efficiently.
Reports take 5+ minutes. Need better query performance."
```

### ← Requirements (вход)

**Как**: Requirements как decision drivers

```
REQ-001: Queries must complete within 5 seconds
REQ-002: System must support complex JOINs
REQ-003: Must provide ACID guarantees
    ↓
ADR Decision Drivers:
- Query performance: <5 seconds
- Complex JOIN support
- ACID guarantees
```

### → RFC (опциональный вход)

**Как**: RFC → ADR (после принятия решения)

```
RFC: "Database Migration Strategy"
- Proposal: Migrate to PostgreSQL
- Discussion: 2 weeks
- Decision: Approved
    ↓
ADR: "Use PostgreSQL for primary database"
- Supersedes: ADR-000 (MongoDB)
- Status: Accepted
```

### → Implementation (выход)

**Как**: ADR guides implementation

```
ADR-002: Use PostgreSQL
- Decision: PostgreSQL 15
- Consequences: Need migration
    ↓
Implementation:
- Install PostgreSQL
- Design schema
- Write migration scripts
- Update application code
```

### → Future ADRs (связь)

**Как**: ADRs build on each other

```
ADR-002: Use PostgreSQL
    ↓
ADR-005: Use connection pooling (pgbouncer)
    ↓
ADR-008: Use read replicas for analytics
```

---

## Summary

**ADR (Architecture Decision Record)** — это immutable record архитектурных решений. Ключевые принципы:

1. **Одно решение = одна запись**
   - Не объединяйте multiple decisions
   - Каждое решение отдельно

2. **Формат зависит от сложности**
   - Y-Statements: trivial decisions
   - Nygard: simple decisions
   - MADR: medium/complex decisions
   - YADR: machine-readable

3. **Всегда включайте**
   - Context (почему нужно решение)
   - Alternatives (что ещё рассматривали)
   - Decision (что выбрали и почему)
   - Consequences (ВСЕ: good, bad, risks)

4. **Immutable**
   - Никогда не редактируйте accepted ADR
   - Supersede старым ADR новым
   - Сохраняйте историю

5. **Хранение в репозитории**
   - `docs/adr/adr-NNN.md`
   - Index в README.md
   - Version controlled
   - Reviewable via PR

6. **Инструменты**
   - adr-tools: CLI для управления
   - Log4brains: static site generation
   - GitHub Actions: linting
   - VS Code: snippets и navigation

---

## References

- [ADR GitHub](https://adr.github.io) - Official ADR site
- [MADR](https://adr.github.io/madr) - MADR specification
- [Nygard Original](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions) - Original article
- [adr-tools](https://github.com/npryce/adr-tools) - CLI tools
- [Log4brains](https://github.com/thomvaill/log4brains) - Static site generator
- [ISO/IEC/IEEE 42010:2022](http://www.iso-architecture.org/42010/cm) - Architecture standard
- [Previous: Requirements (EARS)](./requirements.md)
- [Back to Modules Index](./README.md)
