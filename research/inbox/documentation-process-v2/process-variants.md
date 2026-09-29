# Варианты процессов разработки

## Введение

Pipeline **PRD → RFC → SDD → Tasks → Implementation → ADR** — это **один из возможных вариантов** для сложных проектов. В реальности процессы должны адаптироваться под:
- Размер и сложность проекта
- Уровень неопределённости
- Количество stakeholders
- Критичность системы
- Доступное время

Этот документ описывает **7 основных pipelines** и когда их использовать.

---

## Pipeline 1: Full Pipeline (Сложные проекты)

```
PRD → RFC → SDD → Tasks → Implementation → ADR
```

### Когда использовать
- **Новая продуктовая линейка** или major feature
- **Высокая неопределённость** в требованиях и реализации
- **Множество stakeholders** (product, design, engineering, security)
- **Критичная система** (auth, payments, data retention)
- **Cross-team impact** — затрагивает несколько команд
- **Бюджет > $100k** или **длительность > 1 месяц**

### Артефакты
| Артефакт | Автор | Когда | Хранение |
|----------|-------|-------|----------|
| PRD | Product Manager | Start | `docs/prd/` |
| RFC | Engineer | After PRD | `docs/rfc/` |
| SDD (requirements.md, design.md, tasks.md) | Engineer + AI | After RFC approved | `docs/specs/` |
| ADR | Engineer | At decision points | `docs/adr/` |

### Преимущества
- ✅ Thorough consideration всех аспектов
- ✅ Team alignment и consensus
- ✅ Documentation для future reference
- ✅ AI-agent friendly (clear specs)

### Недостатки
- ❌ Time-consuming (может замедлить development)
- ❌ Overhead для простых задач
- ❌ Требует discipline и commitment

### Примеры использования
- Новая микросервисная архитектура
- Миграция на новую платформу
- Feature с regulatory requirements (GDPR, HIPAA)
- Integration с external systems

---

## Pipeline 2: Lightweight SDD (Средние проекты)

```
Spec → Implementation → ADR (optional)
```

### Когда использовать
- **Одна фича** в существующем проекте
- **Ясные требования**, низкая неопределённость
- **Одна команда** работает над фичей
- **Длительность 1-4 недели**
- **Brownfield project** (существующая кодовая база)

### Артефакты
| Артефакт | Автор | Когда | Хранение |
|----------|-------|-------|----------|
| Spec (1-2 страницы) | Engineer | Before coding | `docs/specs/feature-NNN.md` |
| ADR | Engineer | If architectural decision | `docs/adr/` |

### Spec Template (Lightweight)
```markdown
# Feature: <name>

## Context
Brief background and why we're doing this.

## Requirements
- REQ-1: The system shall <requirement>
- REQ-2: When <trigger>, the system shall <response>

## Approach
Brief description of implementation approach.

## Alternatives Considered
- Option A: <description> - rejected because <reason>
- Option B: <description> - chosen because <reason>

## Testing Strategy
- Unit tests for <components>
- Integration tests for <scenarios>

## Open Questions
- [ ] Question 1
- [ ] Question 2
```

### Преимущества
- ✅ Fast start (минимум bureaucracy)
- ✅ Достаточно documentation для context
- ✅ AI-agents могут генерировать spec
- ✅ Easy to maintain

### Недостатки
- ❌ Меньше scrutiny чем full pipeline
- ❌ Может пропустить edge cases

### Примеры использования
- Добавить новый API endpoint
- Refactor компонента
- Добавить новую feature в existing service
- Bug fix с architectural implications

---

## Pipeline 3: Minimal (Малые задачи)

```
Task → Implementation → Commit message
```

### Когда использовать
- **Bug fix** или **small enhancement**
- **Длительность < 1 день**
- **Ясное решение**, нет alternatives
- **No architectural impact**
- **Single developer**

### Артефакты
| Артефакт | Автор | Когда | Хранение |
|----------|-------|-------|----------|
| Git commit message | Developer | At commit | Git history |
| PR description | Developer | At PR | GitHub/GitLab |

### Commit Message Template
```
feat(auth): add rate limiting to login endpoint

- Limit to 5 attempts per minute per IP
- Return 429 Too Many Requests when exceeded
- Use Redis for distributed rate limiting

Closes #123
```

### Преимущества
- ✅ Zero overhead
- ✅ Fast execution
- ✅ Git history как documentation

### Недостатки
- ❌ No formal documentation
- ❌ Hard to understand context later
- ❌ Knowledge loss при team changes

### Примеры использования
- Fix typo в UI
- Update dependency version
- Small bug fix
- Add missing validation

---

## Pipeline 4: Design-First (Технически ограниченные проекты)

```
Design → Requirements → Implementation
```

### Когда использовать
- **Technically constrained projects** (интеграции, migrations)
- **Performance-critical systems**
- **Legacy system modernization**
- **Когда "how" определяет "what"**

### Артефакты
| Артефакт | Автор | Когда | Хранение |
|----------|-------|-------|----------|
| design.md | Engineer/Architect | Start | `docs/design/` |
| requirements.md | Engineer | After design | `docs/specs/` |
| tasks.md | Engineer/AI | After requirements | `docs/tasks/` |

### Workflow
1. **Design first**: Определить technical constraints и solution strategy
2. **Derive requirements**: Из design вывести что система должна делать
3. **Break into tasks**: Разбить на implementable tasks
4. **Implement**: Код на основе design и requirements

### Преимущества
- ✅ Optimal для technical projects
- ✅ Clear technical vision
- ✅ Avoids rework из-за technical constraints

### Недостатки
- ❌ Может пропустить user needs
- ❌ Less product-focused

### Примеры использования
- Database migration
- API integration с external system
- Performance optimization
- Infrastructure as code

---

## Pipeline 5: BDD-Driven (Behavior-focused projects)

```
Discovery → Examples → Scenarios → Implementation
```

### Когда использовать
- **Business rules are critical** (finance, healthcare, legal)
- **Stakeholder collaboration** важна
- **Executable documentation** нужна
- **Complex user workflows**
- **Regulatory compliance**

### Артефакты
| Артефакт | Автор | Когда | Хранение |
|----------|-------|-------|----------|
| Discovery notes | Team | Workshop | `docs/discovery/` |
| Examples | Team + Stakeholders | After discovery | `docs/examples/` |
| Scenarios (Gherkin) | Team | After examples | `features/*.feature` |
| Step definitions | Developer | During implementation | `tests/steps/` |

### Workflow (Three Amigos)
1. **Discovery workshop**: Product, Dev, QA обсуждают feature
2. **Real-world examples**: Конкретные сценарии с real data
3. **Formulate scenarios**: Given-When-Then format
4. **Automate**: Step definitions для scenarios
5. **Implement**: Код, который проходит scenarios
6. **Living documentation**: Scenarios как documentation

### Пример Scenario
```gherkin
Feature: User authentication
  Scenario: Successful login with valid credentials
    Given a user "alice" with password "secret123" exists
    When alice submits username "alice" and password "secret123"
    Then alice is logged in
    And alice sees the dashboard
    
  Scenario: Failed login with invalid password
    Given a user "alice" with password "secret123" exists
    When alice submits username "alice" and password "wrong"
    Then alice sees "Invalid credentials" error
    And alice is not logged in
```

### Преимущества
- ✅ Shared understanding между business и tech
- ✅ Executable specifications
- ✅ Living documentation
- ✅ High test coverage

### Недостатки
- ❌ Overhead для simple features
- ❌ Требует BDD expertise
- ❌ Может стать "QA thing" без proper adoption

### Примеры использования
- Payment processing
- User authentication/authorization
- Order management system
- Compliance-critical workflows

---

## Pipeline 6: RFC-First (Архитектурные решения)

```
Problem → RFC → Debate → ADR → Implementation
```

### Когда использовать
- **Архитектурное решение** с multiple alternatives
- **Cross-team impact**
- **Нужен consensus building**
- **High-risk decision**
- **Reversible vs irreversible choice**

### Артефакты
| Артефакт | Автор | Когда | Хранение |
|----------|-------|-------|----------|
| RFC | Engineer | Before decision | `docs/rfc/` |
| Comments | Team | During review | RFC comments |
| ADR | Engineer | After decision | `docs/adr/` |

### RFC Template
```markdown
# RFC: <Title>

## Status
Draft | In Review | Approved | Rejected

## Context
What is the issue or problem we're trying to solve?

## Proposal
What is the proposed solution?

## Alternatives Considered
### Alternative 1: <name>
Description...
Pros: ...
Cons: ...

### Alternative 2: <name>
Description...
Pros: ...
Cons: ...

## Decision
What did we decide and why?

## Consequences
What are the trade-offs and risks?

## Open Questions
- [ ] Question 1
- [ ] Question 2
```

### Workflow
1. **Identify problem**: Архитектурное решение нужно
2. **Write RFC**: Proposal с alternatives
3. **Circulate for feedback**: Team review (1 week time-box)
4. **Debate**: Discussion, questions, concerns
5. **Decide**: Approve or reject
6. **Create ADR**: Permanent record
7. **Implement**: На основе decision

### Преимущества
- ✅ Thorough consideration
- ✅ Team alignment
- ✅ Historical record
- ✅ Prevents "I told you so"

### Недостатки
- ❌ Time-consuming
- ❌ Может замедлить development
- ❌ Overhead для simple decisions

### Примеры использования
- Выбор database (SQL vs NoSQL)
- API design (REST vs GraphQL vs gRPC)
- Authentication strategy (OAuth vs JWT vs sessions)
- Deployment strategy (containers vs serverless)
- Build vs buy decision

---

## Pipeline 7: Research Compendium (Исследовательские проекты)

```
Data → Methods → Output → Documentation
```

### Когда использовать
- **Data science / ML projects**
- **Research и experimentation**
- **Reproducible research**
- **Academic projects**
- **Proof of concept**

### Артефакты
| Артефакт | Автор | Когда | Хранение |
|----------|-------|-------|----------|
| Raw data | Researcher | Collected | `data/raw/` |
| Processing code | Researcher | During analysis | `code/` |
| Clean data | Project | After processing | `data/clean/` |
| Figures | Project | After analysis | `figures/` |
| Paper/report | Researcher | Final | `paper.Rmd` |
| Environment | Project | Setup | `Dockerfile` |

### Структура репозитория
```
compendium/
├── data/
│   ├── raw/           # Read-only, original data
│   └── clean/         # Processed data
├── code/              # Analysis scripts
├── figures/           # Generated plots
├── paper.Rmd          # Main document
├── Dockerfile         # Environment specification
├── Makefile           # Reproduction commands
└── README.md          # Instructions
```

### Workflow
1. **Collect data**: Raw data в `data/raw/`
2. **Write methods**: Code в `code/`
3. **Process data**: Generate `data/clean/`
4. **Analyze**: Generate `figures/`
5. **Write paper**: `paper.Rmd` с references к data и code
6. **Containerize**: `Dockerfile` для reproducibility
7. **Publish**: GitHub + Zenodo (DOI)

### Преимущества
- ✅ Reproducibility
- ✅ Transparency
- ✅ Collaboration-friendly
- ✅ Publication-ready

### Недостатки
- ❌ Overhead для production code
- ❌ Not для operational systems
- ❌ Требует discipline

### Примеры использования
- ML model training
- Data analysis project
- A/B testing analysis
- Academic research
- Proof of concept

---

## Сравнительная таблица

| Pipeline | Сложность | Время | Артефакты | Когда использовать |
|----------|-----------|-------|-----------|-------------------|
| **Full** | Высокая | Недели | PRD, RFC, SDD, ADR | Новая продуктовая линия, critical systems |
| **Lightweight SDD** | Средняя | Дни | Spec, ADR | Средняя фича, одна команда |
| **Minimal** | Низкая | Часы | Commit message | Bug fix, small enhancement |
| **Design-First** | Средняя | Дни-недели | Design, Requirements | Technical constraints, performance |
| **BDD-Driven** | Высокая | Недели | Scenarios, Steps | Business rules, compliance |
| **RFC-First** | Средняя | Неделя | RFC, ADR | Architectural decisions |
| **Research** | Средняя | Дни-недели | Data, Code, Paper | Data science, research |

---

## Decision Matrix: Какой pipeline выбрать?

```
Начните с вопроса: "Насколько это сложно?"

├─ Тривиально (< 1 день)
│  └─ Pipeline 3: Minimal
│
├─ Просто (1-4 недели)
│  ├─ Ясные требования?
│  │  └─ Pipeline 2: Lightweight SDD
│  │
│  ├─ Нужен consensus?
│  │  └─ Pipeline 6: RFC-First
│  │
│  └─ Business rules critical?
│     └─ Pipeline 5: BDD-Driven
│
├─ Сложно (> 1 месяц)
│  ├─ Новая продуктовая линия?
│  │  └─ Pipeline 1: Full
│  │
│  ├─ Technical constraints?
│  │  └─ Pipeline 4: Design-First
│  │
│  └─ Research/ML project?
│     └─ Pipeline 7: Research Compendium
│
└─ Не уверен?
   └─ Начните с Pipeline 2, upgrade если нужно
```

---

## Масштабирование процессов

### Проект растёт: как эволюционирует процесс

**Фаза 1: MVP (1-2 разработчика, 1-3 месяца)**
- Pipeline: Lightweight SDD
- Артефакты: Spec, README, ADR (если нужно)
- Фокус: Speed, learning

**Фаза 2: Growth (3-10 разработчиков, 3-12 месяцев)**
- Pipeline: Full для major features, Lightweight для minor
- Артефакты: PRD (для product), RFC (для architecture), SDD, ADR
- Фокус: Quality, collaboration

**Фаза 3: Scale (10+ разработчиков, 12+ месяцев)**
- Pipeline: Full для critical, RFC для decisions, BDD для business rules
- Артефакты: Полный набор + formal reviews
- Фокус: Governance, compliance

**Фаза 4: Enterprise (Multiple teams, years)**
- Pipeline: Full + TOGAF/ArchiMate + formal methods
- Артефакты: Enterprise architecture + project-level docs
- Фокус: Standardization, auditability

### Пример эволюции

**Start-up (Phase 1)**
```
Feature: User authentication
└─ spec.md (1 page)
   └─ Implementation
```

**Scale-up (Phase 2)**
```
Feature: User authentication
├─ prd.md
├─ rfc.md (OAuth vs JWT)
├─ specs/
│  ├─ requirements.md
│  └─ design.md
└─ adr/
   └─ adr-001-use-jwt.md
```

**Enterprise (Phase 4)**
```
Feature: User authentication
├─ prd.md
├─ rfc.md
├─ architecture/
│  ├─ system-context.puml
│  └─ container-diagram.puml
├─ specs/
│  ├─ requirements.md (EARS)
│  ├─ design.md
│  └─ tasks.md
├─ bdd/
│  └─ features/auth.feature
├─ adr/
│  ├─ adr-001-use-jwt.md
│  └─ adr-002-jwt-library.md
└─ compliance/
   └─ gdpr-assessment.md
```

---

## Hybrid Approaches

### Комбинирование pipelines

**Пример 1: Full + BDD**
```
PRD → RFC → SDD + BDD scenarios → Implementation → ADR
```
Использование: Critical feature с business rules

**Пример 2: Design-First + RFC**
```
RFC (architecture) → Design → Requirements → Implementation → ADR
```
Использование: Technical project с architectural decisions

**Пример 3: Lightweight + ADR**
```
Spec → ADR (для decisions) → Implementation
```
Использование: Medium feature с architectural choices

---

## Recommendations

### Для старта проекта
1. **Начните с Lightweight SDD** (Pipeline 2)
2. **Upgrade до Full** (Pipeline 1) для major features
3. **Используйте RFC-First** (Pipeline 6) для architectural decisions
4. **Добавьте BDD** (Pipeline 5) если business rules critical

### Для зрелого проекта
1. **Full pipeline** для new product lines
2. **Lightweight SDD** для regular features
3. **RFC-First** для cross-cutting concerns
4. **BDD** для compliance и business rules
5. **Minimal** для bug fixes

### Для AI-agent workflow
1. **SDD pipelines** (2, 4) — AI генерирует specs
2. **BDD pipeline** (5) — AI генерирует scenarios
3. **RFC pipeline** (6) — AI помогает с alternatives analysis
4. **Human review** для всех critical decisions

---

## Anti-patterns

### ❌ Over-engineering
**Проблема**: Использование Full pipeline для bug fix
**Решение**: Match pipeline к complexity

### ❌ Under-documenting
**Проблема**: Minimal pipeline для critical feature
**Решение**: Upgrade pipeline если stakes high

### ❌ One-size-fits-all
**Проблема**: forcing all projects через один pipeline
**Решение**: Choose pipeline per feature/project

### ❌ Process for process sake
**Проблема**: Documentation без value
**Решение**: Каждый артефакт должен иметь clear purpose

---

## Заключение

**Нет единственно правильного pipeline.** Процессы должны:
- ✅ Адаптироваться под размер и сложность проекта
- ✅ Масштабироваться вместе с проектом
- ✅ Балансировать speed и quality
- ✅ Поддерживать human и AI collaboration

**Ключевой принцип**: Start small, scale as needed.

---

## References

- [Goals](./goals.md)
- [Knowledge Base](./knowledge-base.md)
- [Process Architecture](./process-architecture.md)
- [Attentive RFC Process](https://tech.attentive.com/articles/rfc-process-for-teams)
- [Kiro Three-Phase Workflow](https://kiro.dev/docs/specs/feature-specs)
- [Research Compendium](https://book.the-turing-way.org/reproducible-research/compendia)
