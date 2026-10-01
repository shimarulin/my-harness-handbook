# База знаний: подходы и инструменты для документации ПО

Этот документ систематизирует все изученные подходы, спецификации, фреймворки и инструменты для построения процессов разработки документации.

## 1. Documentation Formats & Standards

### 1.1 Markdown
**Описание**: Стандартный формат для технической документации
**Плюсы**:
- Простой синтаксис
- Поддержка во всех инструментах
- Readable в raw виде
- Git-friendly

**Минусы**:
- Ограниченная семантика
- Нет встроенной валидации

**Инструменты**:
- MkDocs
- Docusaurus
- Antora
- GitBook

### 1.2 PlantUML
**Описание**: Text-to-diagram для архитектурных диаграмм
**Плюсы**:
- Version control friendly
- Быстрая генерация
- Множество типов диаграмм
- Поддержка C4 Model

**Минусы**:
- Требует Java runtime
- Ограниченная кастомизация

**Использование**: C4 diagrams, sequence diagrams, component diagrams

### 1.3 Mermaid
**Описание**: JavaScript-based diagramming tool
**Плюсы**:
- Нативная поддержка в GitHub/GitLab
- Быстрый rendering
- Хорошая документация

**Минусы**:
- Зависимость от JavaScript
- Меньше возможностей чем PlantUML

**Использование**: Flowcharts, sequence diagrams, Gantt charts

### 1.4 ArchiMate
**Описание**: Open standard для enterprise architecture modeling
**Плюсы**:
- Стандартизированная нотация
- Совместимость с TOGAF
- Богатая семантика

**Минусы**:
- Крутая кривая обучения
- Требует специализированных инструментов

**Инструменты**:
- Archi (OpenSource)
- Visual Paradigm

### 1.5 Structurizr
**Описание**: C4 Model based solution для diagram as code
**Плюсы**:
- Генерация диаграмм из кода
- Поддержка всех уровней C4
- Export в различные форматы

**Минусы**:
- Требует изучения DSL
- Коммерческая версия для некоторых features

**Ссылка**: https://structurizr.com

## 2. Requirements Engineering

### 2.1 EARS (Easy Approach to Requirements Syntax)
**Описание**: Структурированный синтаксис для написания требований
**Паттерны**:
- Ubiquitous: `The <system> shall <response>`
- State-driven: `While <precondition>, the <system> shall <response>`
- Event-driven: `When <trigger>, the <system> shall <response>`
- Optional: `Where <feature>, the <system> shall <response>`
- Unwanted: `If <trigger>, then the <system> shall <response>`

**Плюсы**:
- Убирает ambiguity
- Улучшает testability
- Простой для изучения

**Использование**: Kiro, Rolls-Royce, Airbus, NASA

**Ссылка**: https://alistairmavin.com/ears

### 2.2 Volere
**Описание**: Comprehensive requirements specification template
**Плюсы**:
- Полный coverage всех аспектов
- Проверенный в enterprise
- Структурированный подход

**Минусы**:
- Может быть избыточным для малых проектов
- Требует обучения

**Ссылка**: https://www.volere.org

### 2.3 IREB (International Requirements Engineering Board)
**Описание**: Сертификация и стандарты для requirements engineering
**Плюсы**:
- Industry standard
- Comprehensive framework
- Certification path

**Минусы**:
- Формальный подход
- Требует обучения

**Ссылка**: https://www.ireb.org

### 2.4 Use Cases (Alistair Cockburn)
**Описание**: Сценарии использования системы
**Плюсы**:
- Фокус на user interactions
- Хорошая визуализация
- Понятны stakeholders

**Минусы**:
- Могут стать слишком детальными
- Требуют maintenance

**Ссылка**: https://alistaircockburn.com

### 2.5 User Stories
**Описание**: Короткие описания функциональности от лица пользователя
**Формат**: `As a <role>, I want <goal>, so that <benefit>`
**Плюсы**:
- Простые для написания
- Agile-friendly
- Фокус на value

**Минусы**:
- Могут быть слишком поверхностными
- Требуют acceptance criteria

### 2.6 Job Stories
**Описание**: Альтернатива user stories с фокусом на motivation
**Формат**: `When <situation>, I want to <motivation>, so I can <expected outcome>`
**Плюсы**:
- Фокус на контексте
- Меньше assumptions о роли
- Лучше для discovery

**Минусы**:
- Менее распространены
- Требуют переобучения команды

**Origin**: Intercom

### 2.7 User Story Mapping (Jeff Patton)
**Описание**: Визуальная техника для организации user stories
**Плюсы**:
- Holistic view продукта
- Помогает prioritization
- Улучшает communication

**Минусы**:
- Требует workshop
- Может быть сложным для remote команд

**Ссылка**: https://jpattonassociates.com/story-mapping

## 3. Architecture Documentation

### 3.1 C4 Model
**Описание**: 4 уровня абстракции для архитектурных диаграмм
**Уровни**:
1. System Context - система в контексте
2. Container - applications, data stores
3. Component - внутренние компоненты
4. Code - классы (опционально)

**Плюсы**:
- Простой для изучения
- Developer-friendly
- Tool-agnostic

**Минусы**:
- Не покрывает все аспекты
- Требует дополнительных документов

**Ссылка**: https://c4model.com

### 3.2 Arc42
**Описание**: Template для документирования архитектуры (12 секций)
**Секции**:
1. Introduction and Goals
2. Constraints
3. Context and Scope
4. Solution Strategy
5. Building Block View
6. Runtime View
7. Deployment View
8. Crosscutting Concepts
9. Architecture Decisions
10. Quality Requirements
11. Risks and Technical Debt
12. Glossary

**Плюсы**:
- Comprehensive coverage
- Проверенный template
- Совместим с C4 Model

**Минусы**:
- Может быть избыточным
- Требует времени на заполнение

**Ссылка**: https://arc42.org

### 3.3 TOGAF (The Open Group Architecture Framework)
**Описание**: Enterprise architecture framework
**Плюсы**:
- Industry standard
- Comprehensive methodology
- Certification available

**Минусы**:
- Очень формальный
- Overhead для малых проектов
- Требует обучения

**Использование**: Large enterprises, government organizations

### 3.4 Zachman Framework
**Описание**: Ontology для организации architectural artifacts
**Матрица**: 6x6 (What, How, Where, Who, When, Why × Contexts)
**Плюсы**:
- Систематический подход
- Полный coverage

**Минусы**:
- Сложный
- Академический
- Не методология

### 3.5 4+1 View Model (Philippe Kruchten)
**Описание**: 5 views для описания архитектуры
**Views**:
1. Logical view
2. Process view
3. Development view
4. Physical view
5. Scenarios (+1)

**Плюсы**:
- Multi-stakeholder approach
- Balanced coverage

**Минусы**:
- Требует координации
- Может быть избыточным

## 4. Decision Records

### 4.1 ADR (Architecture Decision Record)
**Формат Nygard**:
```markdown
# ADR N: Title
## Context
## Decision
## Status
## Consequences
```

**Плюсы**:
- Простой
- Lightweight
- Git-friendly

**Хранение**: `doc/arch/adr/` в репозитории

**Ссылка**: https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions

### 4.2 MADR (Markdown Architectural Decision Records)
**Описание**: Расширенный формат ADR
**Дополнительные секции**:
- Decision Drivers
- Considered Options
- Pros and Cons of Options
- Confirmation

**Плюсы**:
- Более структурированный
- Лучшая traceability
- Machine-readable

**Ссылка**: https://adr.github.io/madr

### 4.3 Y-Statements
**Формат**: `In the context of <use case>, facing <concern> we decided for <option> to achieve <quality>, accepting <downside>`
**Плюсы**:
- Очень краткие
- Для множества мелких решений
- Easy to scan

**Использование**: Быстрые решения, team agreements

### 4.4 RFC (Request for Comments)
**Описание**: Proposal для обсуждения перед принятием решения
**Секции**:
- Context / problem
- Proposal
- Alternatives considered
- Trade-offs and risks
- Open questions

**Плюсы**:
- Structured debate
- Consensus building
- Documentation of alternatives

**Использование**: Архитектурные решения, major changes

**Пример**: Attentive Engineering RFC Process

### 4.5 RFD (Request for Discussion)
**Описание**: Процесс для технических proposals
**Использование**: Oxide, Joyent, Rust, Kubernetes
**Плюсы**:
- Community-driven
- Transparent decision-making
- Historical record

**Ссылка**: https://rfd.shared.oxide.computer

## 5. Process Workflows

### 5.1 PRD (Product Requirements Document)
**Описание**: Product-level requirements
**Фокус**: What & Why
**Автор**: Product Manager
**Секции**:
- Overview
- Problem
- Goals
- Requirements
- Success metrics
- Constraints

**Ссылка**: https://www.atlassian.com/agile/product-management/requirements

### 5.2 RFC-Driven Development
**Workflow**:
1. Identify need for change
2. Write RFC with proposal
3. Circulate for feedback
4. Iterate based on comments
5. Approve or reject
6. Implement or create ADR

**Плюсы**:
- Thorough consideration
- Team alignment
- Knowledge sharing

**Минусы**:
- Time-consuming
- Может замедлить development

### 5.3 Spec-Driven Development (SDD)
**Описание**: Documentation-first подход
**Workflow**:
1. Write specification
2. Review specification
3. Generate/plan implementation
4. Implement against spec
5. Verify against spec

**Инструменты**:
- GitHub Spec Kit
- Kiro
- BMAD-METHOD
- OpenSpec
- ForgeSDLC

**Плюсы**:
- Clear requirements
- AI-agent friendly
- Reduces ambiguity

### 5.4 Pipeline: PRD → RFC → SDD → ADR
**Workflow**:
1. **PRD**: Product intent (what & why)
2. **RFC**: Technical proposal (how, let's debate)
3. **SDD**: Specification (detailed how)
4. **ADR**: Decision record (what we decided)

**Использование**: Complex features, new product lines

## 6. Behavioral Specifications

### 6.1 BDD (Behavior-Driven Development)
**Описание**: Collaboration framework для разработки
**Практики**:
- Discovery workshops
- Formulation (structured documentation)
- Automation (executable specs)

**Плюсы**:
- Bridge business & tech
- Living documentation
- Executable specifications

**Минусы**:
- Overhead
- Требует discipline
- Может стать "QA thing"

### 6.2 Gherkin (Given-When-Then)
**Синтаксис**:
```gherkin
Feature: Feature name
  Scenario: Scenario name
    Given <precondition>
    When <action>
    Then <expected result>
```

**Инструменты**:
- Cucumber
- SpecFlow / Reqnroll
- Behave
- Behat
- Gauge

**Ссылка**: https://cucumber.io

### 6.3 FitNesse
**Описание**: Wiki-based acceptance testing
**Плюсы**:
- Collaborative
- Executable specifications
- Integration-friendly

**Минусы**:
- Устаревший
- Требует setup

**Ссылка**: https://fitnesse.org

### 6.4 Concordion
**Описание**: BDD framework для Java
**Плюсы**:
- HTML-based specifications
- Flexible
- IDE integration

**Минусы**:
- Java-only
- Требует programming

**Ссылка**: https://concordion.org

## 7. API Specifications

### 7.1 OpenAPI (Swagger)
**Описание**: Standard для REST APIs
**Плюсы**:
- Industry standard
- Tool support
- Code generation

**Инструменты**:
- Stoplight
- Postman
- Swagger Editor

**Ссылка**: https://www.openapis.org

### 7.2 AsyncAPI
**Описание**: Standard для event-driven APIs
**Плюсы**:
- Для message queues, event streams
- Similar to OpenAPI
- Growing adoption

**Инструменты**:
- AsyncAPI Studio
- Solace Event Portal

**Ссылка**: https://www.asyncapi.com

### 7.3 GraphQL Schema
**Описание**: Specification для GraphQL APIs
**Плюсы**:
- Self-documenting
- Type system
- Introspection

**Минусы**:
- Specific to GraphQL

### 7.4 JSON Schema
**Описание**: Specification для JSON data structures
**Плюсы**:
- Validation
- Documentation
- Code generation

**Использование**: API payloads, configuration files

### 7.5 Protocol Buffers (Protobuf)
**Описание**: Serialization format от Google
**Плюсы**:
- Efficient
- Language-agnostic
- Schema evolution

**Минусы**:
- Binary format
- Требует compilation

## 8. Formal Methods

### 8.1 TLA+
**Описание**: Formal specification language для distributed systems
**Плюсы**:
- Mathematical rigor
- Model checking
- Proven in industry

**Минусы**:
- Steep learning curve
- Требует expertise
- Time-consuming

**Использование**: AWS, Microsoft, critical systems

**Ссылка**: https://lamport.azurewebsites.net/tla/tla.html

### 8.2 Alloy
**Описание**: Declarative language для software modeling
**Плюсы**:
- Easier than TLA+
- Good для requirements
- Automated analysis

**Минусы**:
- Limited to certain properties
- Требует обучения

**Ссылка**: https://alloytools.org

### 8.3 FizzBee
**Описание**: Python-based formal specification
**Плюсы**:
- Familiar syntax (Python)
- Lower barrier to entry
- Model checking

**Минусы**:
- Новый инструмент
- Меньше community

**Ссылка**: https://fizzbee.io

### 8.4 Event-B
**Описание**: Formal method для system development
**Плюсы**:
- Refinement support
- Tool support (Rodin)
- Proven in industry

**Минусы**:
- Academic
- Требует expertise

## 9. Quality Frameworks

### 9.1 ISO/IEC 25010
**Описание**: Software quality model
**Characteristics**:
- Functional suitability
- Performance efficiency
- Compatibility
- Usability
- Reliability
- Security
- Maintainability
- Portability
- Safety

**Плюсы**:
- Industry standard
- Comprehensive
- Measurable

**Ссылка**: https://www.iso.org/standard/35733.html

### 9.2 ATAM (Architecture Tradeoff Analysis Method)
**Описание**: Method для evaluating architecture
**Плюсы**:
- Systematic evaluation
- Stakeholder involvement
- Identifies risks

**Минусы**:
- Time-consuming
- Требует facilitation
- Expensive

**Origin**: SEI (Software Engineering Institute)

### 9.3 QAW (Quality Attribute Workshop)
**Описание**: Workshop для identifying quality attributes
**Плюсы**:
- Early identification
- Stakeholder alignment
- Prioritization

**Минусы**:
- Требует facilitation
- Time investment

**Origin**: SEI

## 10. Documentation as Code Tools

### 10.1 MkDocs
**Описание**: Static site generator для documentation
**Плюсы**:
- Простой
- Fast
- Material theme

**Минусы**:
- Limited features
- Требует customization

**Ссылка**: https://www.mkdocs.org

### 10.2 Docusaurus
**Описание**: Documentation site generator от Meta
**Плюсы**:
- Feature-rich
- React-based
- Good for OSS projects

**Минусы**:
- Требует JavaScript knowledge
- Heavier than MkDocs

**Ссылка**: https://docusaurus.io

### 10.3 Antora
**Описание**: Documentation site для multi-repo projects
**Плюсы**:
- Multi-repository support
- Versioning
- AsciiDoc support

**Минусы**:
- Steeper learning curve
- Требует setup

**Ссылка**: https://antora.org

### 10.4 GitBook
**Описание**: Documentation platform
**Плюсы**:
- Easy to use
- Good UI
- Collaboration features

**Минусы**:
- Commercial
- Vendor lock-in risk

**Ссылка**: https://www.gitbook.com

## 11. AI-Agent Integration

### 11.1 GitHub Spec Kit
**Описание**: Slash commands для SDD workflow
**Features**:
- 38 integrations
- 4 phases (constitution, specify, plan, tasks)
- Agent-agnostic

**Плюсы**:
- Flexible
- Community extensions
- Well-maintained

**Ссылка**: https://github.com/github/spec-kit

### 11.2 Kiro
**Описание**: IDE с встроенным SDD workflow
**Features**:
- 3-phase workflow (requirements, design, tasks)
- EARS notation
- AI-generated specs

**Плюсы**:
- Integrated experience
- AWS backing
- Modern tooling

**Минусы**:
- Vendor-specific
- Limited to Kiro ecosystem

**Ссылка**: https://kiro.dev

### 11.3 BMAD-METHOD
**Описание**: Multi-agent development framework
**Features**:
- 12+ specialized agents
- Skills-based architecture
- Agile AI-driven development

**Плюсы**:
- Comprehensive
- Flexible
- Community-driven

**Ссылка**: https://github.com/bmad-code-org/BMAD-METHOD

### 11.4 OpenSpec
**Описание**: Lightweight spec framework
**Features**:
- 30+ AI assistants
- Slash commands
- No phase gates

**Плюсы**:
- Lightweight
- Configurable
- Open source

**Ссылка**: https://openspec.dev

### 11.5 ForgeSDLC
**Описание**: Event-driven SDLC workflow
**Features**:
- Jira integration
- Human-governed, agent-executed
- Traceability

**Плюсы**:
- Enterprise-ready
- Governance-focused
- Comprehensive

**Ссылка**: https://forgesdlc.com

## 12. Collaborative Modeling

### 12.1 Event Storming
**Описание**: Workshop technique для domain discovery
**Плюсы**:
- Fast discovery
- Collaborative
- Visual

**Минусы**:
- Требует facilitation
- Физическое присутствие (или good remote tools)

**Инструменты**:
- Miro
- Mural
- Prooph Board

**Ссылка**: https://www.eventstorming.com

### 12.2 Domain Storytelling
**Описание**: Collaborative modeling technique
**Плюсы**:
- Simple
- Visual
- Story-based

**Минусы**:
- Less formal
- Требует facilitation

**Ссылка**: https://domainstorytelling.org

### 12.3 Context Mapping
**Описание**: DDD technique для bounded contexts
**Плюсы**:
- Clear boundaries
- Integration patterns
- Team organization

**Минусы**:
- Требует DDD knowledge
- Abstract

## 13. Enterprise Architecture Tools

### 13.1 Archi
**Описание**: OpenSource ArchiMate modeling tool
**Плюсы**:
- Free
- Full ArchiMate support
- Cross-platform

**Минусы**:
- Desktop-only
- Limited collaboration

**Ссылка**: https://www.archimatetool.com

### 13.2 Visual Paradigm
**Описание**: Commercial EA tool
**Плюсы**:
- Feature-rich
- Multiple standards
- Good UI

**Минусы**:
- Commercial
- Expensive

**Ссылка**: https://www.visual-paradigm.com

### 13.3 Sparx Systems Enterprise Architect
**Описание**: Comprehensive EA tool
**Плюсы**:
- Industry standard
- Comprehensive
- Good support

**Минусы**:
- Commercial
- Complex
- Expensive

**Ссылка**: https://sparxsystems.com

## 14. Research Compendium

### 14.1 Концепция
**Описание**: Организация reproducible research projects
**Принципы**:
- Conventional folder structure
- Separation of data, methods, output
- Specified computational environment

**Инструменты**:
- rrtools (R)
- rOpenSci
- o2r (Executable Research Compendium)

**Ссылка**: https://book.the-turing-way.org/reproducible-research/compendia

### 14.2 Структура
```
compendium/
├── data/
│   ├── raw/
│   └── processed/
├── code/
├── output/
├── docs/
├── Dockerfile
└── README.md
```

## 15. Summary Matrix

| Категория | Подход | Сложность | OpenSource | AI-Friendly |
|-----------|--------|-----------|------------|-------------|
| **Requirements** | EARS | Low | ✓ | ✓✓✓ |
| **Requirements** | Volere | Medium | ✓ | ✓✓ |
| **Requirements** | User Stories | Low | ✓ | ✓✓✓ |
| **Architecture** | C4 Model | Low | ✓ | ✓✓✓ |
| **Architecture** | Arc42 | Medium | ✓ | ✓✓ |
| **Architecture** | ArchiMate | High | ✓ | ✓ |
| **Decisions** | ADR (Nygard) | Low | ✓ | ✓✓✓ |
| **Decisions** | MADR | Medium | ✓ | ✓✓✓ |
| **Decisions** | RFC | Medium | ✓ | ✓✓ |
| **Process** | PRD | Medium | ✓ | ✓✓ |
| **Process** | SDD | Medium | ✓ | ✓✓✓ |
| **Behavioral** | BDD/Gherkin | Medium | ✓ | ✓✓ |
| **API** | OpenAPI | Low | ✓ | ✓✓✓ |
| **API** | AsyncAPI | Low | ✓ | ✓✓✓ |
| **Formal** | TLA+ | High | ✓ | ✓ |
| **Formal** | FizzBee | Medium | ✓ | ✓✓ |
| **Quality** | ISO 25010 | Medium | ✓ | ✓✓ |
| **Quality** | ATAM | High | ✓ | ✓ |

## 16. Recommendations for Our Process

### Must-Have (Foundation)
1. **Markdown** - base format для всех документов
2. **EARS** - для структурирования требований
3. **C4 Model** - для архитектурных диаграмм
4. **Arc42** - для архитектурной документации
5. **ADR (MADR)** - для архитектурных решений
6. **Git-based workflow** - для версионирования
7. **PlantUML/Mermaid** - для diagram as code

### Should-Have (Enhancement)
1. **BDD/Gherkin** - для behavioral specifications
2. **OpenAPI/AsyncAPI** - для API specifications
3. **RFC process** - для major decisions
4. **PRD template** - для product requirements
5. **User Story Mapping** - для product discovery

### Nice-to-Have (Advanced)
1. **Formal methods** (FizzBee) - для critical systems
2. **ArchiMate** - для enterprise architecture
3. **ATAM/QAW** - для quality evaluation
4. **Event Storming** - для domain discovery
5. **Research Compendium** - для reproducible research

### AI-Agent Integration
1. **GitHub Spec Kit** - для agent-agnostic workflow
2. **OpenSpec** - для lightweight spec framework
3. **BMAD-METHOD** - для multi-agent development

## 17. References

### From Uploaded Documents
- [EARS Notation](../../ears-notation.md)
- [Research Compendium](../../research-compendium.md)
- [ADR Standards](../../adr-standards.md)
- [SDD Landscape](../../sdd-landscape.md)
- [Architecture C4 Arc42](../../architecture-c4-arc42.md)
- [RFC vs SDD](../../rfc-vs-sdd.md)
- [PRD](../../prd.md)
- [BDD Alternatives](../../bdd-alternatives.md)

### From Web Search
- [Design Docs at Google](https://www.industrialempathy.com/posts/design-docs-at-google/)
- [Amazon 6-Pager](https://www.larksuite.com/en_us/blog/amazon-6-pager)
- [TOGAF](https://www.opengroup.org/togaf)
- [C4 Model](https://c4model.com)
- [Arc42](https://arc42.org)
- [MADR](https://adr.github.io/madr)
- [GitHub Spec Kit](https://github.com/github/spec-kit)
- [Kiro](https://kiro.dev)
- [OpenSpec](https://openspec.dev)
- [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD)
