# AI-Agent Workflows

Комплексное руководство по интеграции AI-агентов в каждый этап процесса разработки документации.

---

## Принципы работы с AI-агентами

### 1. AI как Collaborator, не Autority
- AI генерирует **черновики**, человек принимает **решения**
- AI ускоряет **повторяющуюся работу**, человек фокусируется на **критическом мышлении**
- AI помогает **исследовать варианты**, человек выбирает **правильный путь**

### 2. Context is King
- Всегда предоставляйте полный контекст (проблема, требования, подход)
- Указывайте формат вывода (Markdown, EARS, Gherkin, OpenAPI)
- Ссылайтесь на предыдущие артефакты (проблема → требования → дизайн)

### 3. Verification is Mandatory
- Каждый AI-вывод проходит **человеческую проверку**
- Автоматические проверки (линтеры, тесты) дополняют, но не заменяют ревью
- "Trust but verify" — даже если вывод выглядит хорошо

### 4. Iteration over Perfection
- Первый вывод = черновик
- Уточняйте через дополнительные промпты
- Итерируйте пока не получите удовлетворительный результат

### 5. Human-in-the-Loop Gates
Критические решения **всегда** за человеком:
- Архитектурные решения (→ ADR)
- Продуктовые приоритеты (→ PRD)
- Выбор между альтернативами (→ RFC)
- Финальный ревью кода

---

## Матрица интеграции по модулям

| Модуль | Что может делать AI | Что остаётся человеку | Инструменты |
|--------|--------------------|-----------------------|-------------|
| **Problem Statement** | Формулировка, 5 Whys, структуризация | Финальный выбор проблемы | Claude, GPT |
| **Requirements (EARS)** | Генерация, проверка полноты, конвертация | Приоритизация, валидация | AI + EARS linter |
| **ADR** | Генерация черновика, альтернативы | Принятие решения | AI + adr-tools |
| **Approach** | Генерация, диаграммы, ревью | Выбор архитектуры | AI + PlantUML/Mermaid |
| **Tasks** | Разбиение, оценка, зависимости | Планирование, назначение | AI + task management |
| **Implementation** | Генерация кода, тестов | Финальный ревью, мерж | AI + IDE |
| **PRD** | Генерация черновика, метрики | Продуктовые решения | AI + product tools |
| **RFC** | Альтернативы, анализ, резюме | Принятие решения | AI + collaboration tools |
| **BDD** | Генерация сценариев, step definitions | Валидация с бизнесом | AI + Cucumber/Behave |
| **API Specs** | Генерация из требований, валидация | Финальная валидация | AI + Stoplight/Spectral |

---

## Паттерны интеграции по модулям

### Модуль 1: Problem Statement

#### Паттерн: 5 Whys Facilitation

**Цель**: Дойти до корневой причины проблемы

**Промпт**:
```
I need to understand the root cause of this problem. Apply the 5 Whys technique.

Problem symptom: [describe what you observe]

Ask me "why" 5 times, each time going deeper based on my answers.
After 5 whys, summarize the root cause and suggest 2-3 possible solutions.

Format:
- Number each "why" question
- Wait for my answer before asking the next
- At the end, provide root cause summary
```

**Пример диалога**:
```
Human: Our users complain that checkout is slow

AI: Why do you think checkout is slow?
    (What specific aspect of checkout feels slow to users?)

Human: The payment step takes 30 seconds

AI: Why does the payment step take 30 seconds?
    (Is it the payment processing itself or something else?)

Human: The payment service is called synchronously

AI: Why is the payment service called synchronously?
    (Was there a specific reason for this design choice?)

Human: We didn't want users to see their order created before payment confirmed

AI: Why did we want to avoid that?
    (What was the user experience concern?)

Human: We were worried about confusion if payment failed after order creation

AI: ROOT CAUSE SUMMARY:
    The synchronous payment call is a workaround for lack of optimistic
    order creation with proper failure handling. The real issue is missing
    async payment processing with user notification.
    
    Suggested solutions:
    1. Implement async payment with optimistic order creation
    2. Add payment failure notifications to users
    3. Use payment status tracking UI
```

#### Паттерн: Problem Statement Generation

**Промпт**:
```
Help me write a problem statement for this issue.

Context: [describe the situation]
Symptoms: [what users/business experience]
Impact: [quantify if possible]

Generate a problem statement with:
1. The Problem (1-2 paragraphs)
2. The Impact (quantified)
3. The Goal (what we want to achieve)
4. Non-goals (what we're NOT doing)
5. Success criteria (how we'll know it's solved)

Use specific numbers where possible. Avoid vague language like "fast" or "good".
```

#### Паттерн: Problem Statement Review

**Промпт**:
```
Review this problem statement for:
1. Clarity: Is the problem clearly defined?
2. Specificity: Are there concrete numbers/evidence?
3. Completeness: Is the impact fully explained?
4. Solution-free: Does it avoid prescribing solutions?
5. Testability: Can we verify when the problem is solved?

Problem Statement:
[paste problem statement]

Provide:
- Issues found (with line references)
- Suggestions for improvement
- Missing elements
- Revised version (if significant changes needed)
```

---

### Модуль 2: Requirements (EARS)

#### Паттерн: Генерация из Problem Statement

**Промпт**:
```
Based on this problem statement, generate EARS requirements.

Problem Statement:
[paste problem statement]

Generate requirements using all 5 EARS patterns:
1. Ubiquitous: "The system shall..." (always active)
2. State-driven: "While <state>, the system shall..." (conditional)
3. Event-driven: "When <trigger>, the system shall..." (on event)
4. Optional: "Where <feature>, the system shall..." (configuration-based)
5. Unwanted: "If <error>, then the system shall..." (error handling)

Rules:
- Use REQ-<PREFIX>-<NNN> numbering
- Tag each requirement with its pattern type
- Make requirements specific and testable
- Include concrete values (numbers, timeouts, formats)
- Cover non-functional requirements (performance, security, usability)

Also identify:
- Requirements that might be missing
- Edge cases to consider
- Open questions that need clarification
```

**Пример вывода**:
```markdown
## Functional Requirements

### Ubiquitous
- REQ-EXP-001 [Ubiquitous]: The export service shall support CSV format
- REQ-EXP-002 [Ubiquitous]: The export service shall support JSON format

### Event-driven
- REQ-EXP-003 [Event]: When a user requests export, the system shall 
  acknowledge within 2 seconds and return an export ID
- REQ-EXP-004 [Event]: When the export completes, the system shall 
  send email notification with download link

### State-driven
- REQ-EXP-005 [State]: While the export is in progress, the system shall 
  display progress percentage

### Optional
- REQ-EXP-006 [Optional]: Where enterprise plan is active, the system shall 
  allow scheduled exports

### Unwanted
- REQ-EXP-007 [Unwanted]: If the export fails, then the system shall 
  retry once and notify user on second failure

## Non-Functional Requirements
- REQ-EXP-008 [Performance]: The system shall complete export within 
  30 seconds for datasets < 10,000 records
- REQ-EXP-009 [Security]: Export files shall be encrypted at rest 
  using AES-256
```

#### Паттерн: Проверка полноты

**Промпт**:
```
Review these EARS requirements for completeness:

Requirements:
[paste requirements]

Problem Statement:
[paste problem statement]

Check:
1. Coverage: Does every aspect of the problem have requirements?
2. Patterns: Are all 5 EARS patterns used where appropriate?
3. Specificity: Are there concrete values, not vague terms?
4. Testability: Can each requirement be tested?
5. Edge cases: Are error scenarios and edge cases covered?
6. Non-functional: Are performance, security, usability addressed?

Provide:
- Missing requirements (suggest new ones)
- Vague requirements (suggest specific versions)
- Un-testable requirements (suggest testable versions)
- Completeness score (0-100%)
```

#### Паттерн: Конвертация в BDD

**Промпт**:
```
Convert these EARS requirements into BDD scenarios (Gherkin).

Requirements:
[paste requirements]

For each requirement, generate:
1. Feature name (group related requirements)
2. Rule name (business rule being tested)
3. Scenario(s) with Given-When-Then
4. Test data (concrete values)
5. Tags (@fast, @slow, @critical, @edge-case)

Rules:
- One requirement can generate multiple scenarios
- Include happy path AND error paths
- Use realistic test data
- Tag scenarios appropriately
```

#### Паттерн: Конвертация из User Stories

**Промпт**:
```
Convert these user stories into EARS requirements.

User Stories:
[paste user stories]

For each user story:
1. Extract the functional requirement (what the system does)
2. Identify implicit requirements (error handling, edge cases)
3. Add non-functional requirements (performance, security)
4. Format in EARS notation

Output format:
- REQ-<NNN> [Pattern]: The system shall...
```

---

### Модуль 3: ADR

#### Паттерн: Генерация из обсуждения

**Промпт**:
```
Based on this discussion, create an ADR in MADR format.

Discussion summary:
[paste discussion notes, Slack thread, meeting summary]

Context:
- Problem we're solving: [context]
- Team involved: [names/roles]
- Date: [when]

Generate ADR with:
1. Title (short noun phrase)
2. Status: proposed (until approved)
3. Context and Problem Statement
4. Decision Drivers (what forced this decision)
5. Considered Options (ALL options discussed, including rejected)
6. Decision Outcome (what was chosen and why)
7. Consequences (good, bad, risks)
8. Confirmation (how we'll verify)
9. Pros and Cons of each option

Rules:
- Be honest about trade-offs (include negative consequences)
- Document rejected options with reasons
- Use specific justification, not "because it's better"
```

#### Паттерн: Генерация из требований

**Промпт**:
```
Based on these requirements, identify architectural decisions that need ADRs.

Requirements:
[paste requirements]

For each decision that needs an ADR:
1. What decision needs to be made?
2. What are the options?
3. What are the key trade-offs?
4. Which requirement(s) drive this decision?

Generate draft ADRs for the top 3 most important decisions.
```

#### Паттерн: Ревью ADR

**Промпт**:
```
Review this ADR for quality:

ADR:
[paste ADR]

Check:
1. Clarity: Is the context and problem clear?
2. Completeness: Are all options considered?
3. Justification: Is the decision well-reasoned?
4. Consequences: Are ALL consequences (good and bad) listed?
5. Actionability: Can someone implement based on this?
6. Alternatives: Are alternatives fairly evaluated?

Provide:
- Issues found
- Missing considerations
- Suggested improvements
- Approval recommendation (approve / needs work)
```

#### Паттерн: Supersession

**Промпт**:
```
We're replacing [old technology/approach] with [new technology/approach].

Old ADR:
[paste old ADR]

New decision context:
[why we're changing]

Generate:
1. Updated old ADR with "superseded by ADR-XXX" status
2. New ADR with:
   - Reference to superseded ADR
   - Explanation of why we're changing
   - Migration considerations
   - Impact on dependent systems
```

---

### Модуль 4: Approach (Technical Design)

#### Паттерн: Генерация из требований

**Промпт**:
```
Based on these requirements, generate a technical approach document.

Requirements:
[paste requirements]

Problem Statement:
[paste problem statement]

Constraints:
- Tech stack: [languages, frameworks]
- Team: [size, expertise]
- Timeline: [deadline]
- Infrastructure: [existing systems]

Generate Approach with:
1. Overview (executive summary)
2. Architecture (components + Mermaid diagram)
3. Data Flow (sequence diagram)
4. Data Model (key entities)
5. API Contracts (if applicable)
6. Key Design Decisions (with alternatives and trade-offs)
7. Error Handling
8. Performance Considerations
9. Security Considerations
10. Testing Strategy
11. Out of Scope

Use Mermaid for diagrams. Reference requirement IDs in relevant sections.
```

#### Паттерн: Генерация диаграмм

**Промпт**:
```
Generate Mermaid diagrams for this architecture:

Architecture description:
[paste description]

Generate:
1. Component diagram (high-level)
2. Sequence diagram (main flow)
3. Sequence diagram (error flow)
4. Deployment diagram (if applicable)

Format: Mermaid syntax, ready to embed in Markdown.
```

#### Паттерн: Ревью Approach

**Промпт**:
```
Review this technical approach for:

Approach:
[paste approach]

Requirements:
[paste requirements]

Check:
1. Completeness: Does it cover all requirements?
2. Feasibility: Can it be implemented with our tech stack?
3. Scalability: Will it handle expected load?
4. Security: Are there vulnerabilities?
5. Testability: Can we verify it works?
6. Maintainability: Is it understandable?
7. Trade-offs: Are alternatives fairly considered?

Provide:
- Issues found (with severity: critical/major/minor)
- Missing sections
- Risks and mitigations
- Alternative approaches to consider
```

---

### Модуль 5: Tasks

#### Паттерн: Генерация из Approach

**Промпт**:
```
Based on this technical approach, generate a detailed task breakdown.

Approach:
[paste approach.md content]

Requirements:
[paste requirements.md content]

Generate tasks.md with:
1. Phased structure:
   - Phase 1: Setup & Infrastructure
   - Phase 2: Core Implementation
   - Phase 3: Testing
   - Phase 4: Deployment

2. For each task:
   - Task ID and title
   - Description (what needs to be done)
   - Acceptance Criteria (checkboxes, specific)
   - Requirements covered (REQ-XXX references)
   - Approach reference (section number)
   - Dependencies (task IDs)
   - Estimate (S=2-4h, M=1-2d, L=3-5d)
   - Risk level (Low/Medium/High)
   - Suitable for AI-agent? (yes/no)

3. Dependency graph (Mermaid)
4. Parallelization opportunities
5. Critical path analysis
6. Risk register

Rules:
- No task larger than 2 days (split if needed)
- Every requirement covered by at least one task
- Acceptance criteria specific and testable
- Mark AI-suitable tasks
```

#### Паттерн: Ревью Tasks

**Промпт**:
```
Review this task breakdown:

Tasks:
[paste tasks.md]

Requirements:
[paste requirements.md]

Check:
1. Coverage: Are all requirements covered?
2. Dependencies: Are they correct and complete?
3. Feasibility: Can each task be done in estimated time?
4. Specificity: Are acceptance criteria testable?
5. Parallelization: Are there missed opportunities?
6. Risks: Are risks identified and mitigated?

Provide:
- Missing tasks (requirements not covered)
- Incorrect dependencies
- Tasks to split or merge
- Missing acceptance criteria
- Revised dependency graph
```

---

### Модуль 6: Implementation

#### Паттерн: Task-by-Task Execution

**Промпт для каждого таска**:
```
Implement Task [ID]: [Title]

Task Description:
[description]

Acceptance Criteria:
[checkboxes]

Requirements covered:
[REQ-XXX list]

Approach reference:
[Section X.X from approach.md]

Dependencies completed:
[Task IDs that are done]

Tech stack:
[languages, frameworks, libraries]

Generate:
1. Source code (with file paths)
2. Unit tests (with file paths)
3. Integration tests (if applicable)
4. Configuration changes (if any)
5. Documentation updates (if any)

Rules:
- Reference REQ-IDs in code comments
- Follow approach architecture
- Include error handling
- Write tests before or with implementation
- Keep code production-ready
```

#### Паттерн: Генерация тестов из требований

**Промпт**:
```
Generate tests for these requirements:

Requirements:
[paste requirements]

Approach:
[paste relevant approach sections]

Tech stack:
[testing framework, assertion library]

Generate:
1. Unit tests for each requirement
2. Integration tests for interactions
3. Edge case tests
4. Error scenario tests

Format:
- Test file structure
- Test function names (descriptive)
- Given-When-Then comments in each test
- Mock/stub setup
- Assertions (specific, not vague)
```

#### Паттерн: Ревью кода

**Промпт**:
```
Review this code for:

Code:
[paste code]

Requirements:
[paste requirements]

Approach:
[paste approach]

Check:
1. Correctness: Does it implement requirements correctly?
2. Completeness: Are all requirements covered?
3. Error handling: Are edge cases handled?
4. Performance: Are there bottlenecks?
5. Security: Are there vulnerabilities?
6. Testability: Is it easy to test?
7. Maintainability: Is it readable and documented?

Provide:
- Issues found (with severity)
- Missing requirements coverage
- Suggested improvements
- Code examples for fixes
```

---

### Модуль 7: PRD

#### Паттерн: Генерация из идеи

**Промпт**:
```
Help me create a PRD for this product idea.

Idea: [brief description]
Target users: [who]
Problem: [what pain we solve]
Business context: [why now, revenue impact]

Generate PRD with:
1. Overview (1 paragraph)
2. Problem (with evidence, quantified)
3. Goals (measurable, with targets)
4. Non-goals (explicit exclusions)
5. User Stories (with priorities: Must/Should/Could)
6. Success Metrics (quantitative, with targets)
7. User Experience (key flows, references to designs)
8. Constraints & Assumptions
9. Open Questions (with owners and deadlines)
10. Out of Scope
11. Timeline & Milestones

Rules:
- Use specific numbers, not "many" or "fast"
- Every goal must be measurable
- Include evidence for problem statement
- Identify risks early
```

#### Паттерн: Ревью PRD

**Промпт**:
```
Review this PRD:

PRD:
[paste PRD]

Check:
1. Clarity: Is the problem and goal clear?
2. Evidence: Is there data supporting the need?
3. Measurability: Can success be quantified?
4. Completeness: Are there gaps?
5. Feasibility: Can this be achieved with constraints?
6. Alignment: Does it support business objectives?

Provide:
- Issues found
- Missing sections
- Suggestions for improvement
- Questions to resolve
- Approval recommendation
```

---

### Модуль 8: RFC

#### Паттерн: Генерация из проблемы

**Промпт**:
```
Based on this problem and context, generate an RFC.

Problem Statement:
[paste problem statement]

Constraints:
[list constraints]

Current architecture:
[brief description]

Team:
[size, expertise]

Generate RFC with:
1. Summary (2-3 sentences)
2. Context and Problem
3. Motivation (why now)
4. Proposal (with architecture diagram)
5. Alternatives Considered (at least 3, including "do nothing")
6. Trade-offs and Risks
7. Open Questions
8. Timeline
9. References

Rules:
- Be honest about trade-offs
- Include "do nothing" as alternative
- Provide concrete migration plan
- Identify risks with mitigations
```

#### Паттерн: Анализ альтернатив

**Промпт**:
```
Analyze these alternatives for [decision]:

Context:
[problem description]

Alternatives to compare:
1. [Alternative 1]
2. [Alternative 2]
3. [Alternative 3]

For each alternative, evaluate:
- Pros (with specifics)
- Cons (with specifics)
- Effort to implement
- Maintenance burden
- Team familiarity
- Risk level
- Cost

Then recommend one with justification.
```

---

### Модуль 9: BDD

#### Паттерн: Генерация сценариев

**Промпт**:
```
Based on these requirements, generate BDD scenarios.

Requirements:
[paste requirements]

Generate Gherkin scenarios with:
1. Feature name and description
2. Background (common setup)
3. Rules (group related scenarios)
4. Scenarios with Given-When-Then
5. Scenario Outlines for parameterized tests
6. Tags (@fast, @slow, @critical, @edge-case)

Rules:
- Cover all requirements
- Include happy path AND error paths
- Use realistic test data
- One scenario per behavior (not multiple actions)
- Keep scenarios focused and readable
```

#### Паттерн: Генерация step definitions

**Промпт**:
```
Generate step definitions for these scenarios:

Scenarios:
[paste Gherkin]

Tech stack:
[Python + Behave / Java + Cucumber / etc.]

Generate:
1. Step definition functions
2. Helper utilities (auth, setup, teardown)
3. Data factories (test data generation)
4. Custom assertions
5. Hooks (before/after scenarios)

Rules:
- Reusable steps (not feature-coupled)
- Atomic steps (one action per step)
- Clear error messages
- Proper cleanup
```

---

### Модуль 10: API Specs

#### Паттерн: Генерация из требований

**Промпт**:
```
Based on these requirements and approach, generate OpenAPI 3.0 specification.

Requirements:
[paste requirements]

Approach:
[paste approach.md API section]

Generate OpenAPI spec with:
1. Info (title, version, description)
2. Servers (production, staging)
3. Paths (all endpoints)
4. Request/response schemas
5. Error responses
6. Security schemes
7. Examples for each endpoint
8. Tags for grouping

Rules:
- Reference REQ-IDs in descriptions
- Include all error codes
- Provide realistic examples
- Use proper data types
- Include validation rules
```

#### Паттерн: Генерация тестов из API спецификации

**Промпт**:
```
Based on this OpenAPI spec, generate:

OpenAPI:
[paste spec]

Generate:
1. Contract tests (validate schemas)
2. Integration tests for each endpoint
3. Error handling tests
4. Authentication tests
5. Rate limiting tests

Tech stack:
[Python + pytest + httpx / etc.]
```

---

## Verification и Quality Gates

### Уровни верификации

| Уровень | Что проверяется | Кто | Когда |
|---------|----------------|-----|-------|
| **1. Automated** | Формат, синтаксис, линтеры | CI/CD | При каждом коммите |
| **2. AI Review** | Логика, полнота, соответствие | AI-агент | После генерации |
| **3. Peer Review** | Корректность, целесообразность | Коллега | Перед мержем |
| **4. Human Decision** | Архитектурные/продуктовые решения | Человек | В критических точках |

### Quality Gates по модулям

| Модуль | Gate | Проверка |
|--------|------|----------|
| **Problem Statement** | Human review | Ясность, конкретность |
| **Requirements** | AI + Human | Полнота, тестируемость |
| **ADR** | Human approval | Обоснованность решения |
| **Approach** | Peer review | Техническая корректность |
| **Tasks** | Team planning | Реалистичность оценок |
| **Implementation** | Code review + tests | Корректность, покрытие |
| **PRD** | Stakeholder approval | Бизнес-целесообразность |
| **RFC** | Team consensus | Выбор оптимального варианта |
| **BDD** | Business validation | Соответствие ожиданиям |
| **API Specs** | Automated + Human | Валидность, полнота |

---

## Human-in-the-Loop Patterns

### Pattern 1: AI Drafts, Human Decides

```
AI генерирует черновик → Человек ревьюит → Человек решает → 
(Если нужно) Уточнение → Финальный вариант
```

**Применение**: ADR, RFC, PRD

### Pattern 2: AI Generates, Human Validates

```
AI генерирует → Автоматические проверки → Человек валидирует → 
Принятие/отклонение
```

**Применение**: Requirements, Tasks, API Specs

### Pattern 3: AI Assists, Human Executes

```
Человек описывает задачу → AI помогает (подсказки, примеры) → 
Человек реализует → Человек коммитит
```

**Применение**: Implementation, Testing

### Pattern 4: Human Defines, AI Implements

```
Человек пишет спецификацию → AI генерирует код → 
Автоматические тесты → Человек ревьюит → Мерж
```

**Применение**: Implementation (после Approval)

---

## Инструменты и интеграции

### Специализированные инструменты

| Инструмент | Назначение | Ссылка |
|-----------|-----------|--------|
| **GitHub Spec Kit** | SDD workflow с slash commands | [github/spec-kit](https://github.com/github/spec-kit) |
| **Kiro** | IDE с 3-фазным workflow | [kiro.dev](https://kiro.dev) |
| **OpenSpec** | Lightweight spec framework | [openspec.dev](https://openspec.dev) |
| **BMAD-METHOD** | Multi-agent development | [bmad-code-org](https://github.com/bmad-code-org/BMAD-METHOD) |
| **ForgeSDLC** | Event-driven SDLC | [forgesdlc.com](https://forgesdlc.com) |

### Интеграция с нашим процессом

**Для Problem Statement + Requirements**:
- Любой AI-ассистент (Claude, GPT, Gemini)
- Custom промпты из этого документа

**Для Approach + Tasks**:
- GitHub Spec Kit: `/speckit.specify`, `/speckit.plan`, `/speckit.tasks`
- OpenSpec: `/opsx:propose`
- Kiro: requirements.md → design.md → tasks.md

**Для Implementation**:
- Любой coding agent (Claude Code, Cursor, Copilot)
- BMAD-METHOD для multi-agent

**Для Verification**:
- Custom линтеры (см. [инструменты](../tools-automation/README.md))
- GitHub Actions для автоматических проверок
- BDD для исполняемых спецификаций

---

## Пример полного workflow

### Сценарий: Реализация фичи экспорта данных

```
Шаг 1: Problem Statement
─────────────────────────
Human: Описывает проблему (1-2 предложения)
AI: Применяет 5 Whys, генерирует Problem Statement
Human: Ревьюит и уточняет
Результат: specs/export/problem-statement.md ✅

Шаг 2: Requirements
───────────────────
Human: Даёт Problem Statement
AI: Генерирует EARS требования (все 5 паттернов)
AI: Проверяет полноту
Human: Проверяет, добавляет недостающее
Результат: specs/export/requirements.md ✅

Шаг 3: RFC (опционально, если нужны архитектурные дебаты)
────────────────────────────────────────────────────────
Human: Описывает проблему и контекст
AI: Генерирует RFC с альтернативами
Team: Обсуждает в PR/Slack
Human: Принимает решение
Результат: docs/rfc/rfc-001.md ✅

Шаг 4: ADR
──────────
Human: Описывает решение
AI: Генерирует ADR в MADR формате
Human: Проверяет и коммитит
Результат: docs/adr/adr-001.md ✅

Шаг 5: Approach
───────────────
Human: Даёт Requirements + ADR
AI: Генерирует технический подход с диаграммами
Human: Ревьюит, уточняет
Результат: specs/export/approach.md ✅

Шаг 6: API Spec
───────────────
Human: Даёт Approach
AI: Генерирует OpenAPI spec
Automated: Spectral linting
Human: Финальная валидация
Результат: specs/export/api/openapi.yaml ✅

Шаг 7: BDD (опционально, если критичные бизнес-правила)
─────────────────────────────────────────────────────
Human: Даёт Requirements
AI: Генерирует Gherkin сценарии
Business: Валидирует сценарии
Результат: features/export.feature ✅

Шаг 8: Tasks
────────────
Human: Даёт Approach
AI: Генерирует tasks с зависимостями и оценками
Team: Планирование, назначение
Результат: specs/export/tasks.md ✅

Шаг 9: Implementation
─────────────────────
For each task:
  Human: Выбирает задачу
  AI: Генерирует код + тесты
  Automated: Тесты, линтинг
  Human: Ревьюит и мержит
Результат: Код в репозитории ✅

Шаг 10: Verification
────────────────────
Automated: Все тесты проходят
Automated: Requirements coverage check
Human: Финальный ревью
Результат: Фича готова к релизу ✅
```

---

## Анти-паттерны

### ❌ AI как "чёрный ящик"
**Проблема**: Принимаем AI-вывод без проверки
**Решение**: Всегда верифицируем, особенно критические решения

### ❌ Слишком широкий промпт
**Проблема**: "Сделай всё за меня" без контекста
**Решение**: Конкретные промпты с контекстом и форматом вывода

### ❌ Нет итерации
**Проблема**: Берём первый вывод как финальный
**Решение**: Итерируем, уточняем, улучшаем

### ❌ Пропуск human gates
**Проблема**: AI принимает архитектурные решения
**Решение**: Критические решения всегда за человеком

### ❌ Нет контекста
**Проблема**: Генерируем без предыдущих артефактов
**Решение**: Всегда ссылаемся на Problem → Requirements → Approach

---

## References

- [GitHub Spec Kit](https://github.com/github/spec-kit)
- [Kiro](https://kiro.dev/docs/specs/feature-specs)
- [OpenSpec](https://openspec.dev)
- [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD)
- [ForgeSDLC](https://forgesdlc.com)
- [SDD Without the Hype](https://utsabpant.com/blog/spec-driven-development-without-the-hype)
- [Tools & Automation](../tools-automation/README.md)
- [Modules Index](../modules/README.md)
