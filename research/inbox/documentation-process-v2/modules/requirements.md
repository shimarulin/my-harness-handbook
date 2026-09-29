# Requirements (EARS)

Второй модуль Core Foundation. Требования — это мост между проблемой и реализацией. Без структурированных требований невозможно проверить правильность решения, невозможно генерировать код, невозможно объяснить что система должна делать.

---

## Что такое Requirements в нашем процессе

**Requirements** — формализованное описание того, что система **должна делать**, выраженное в структурированном синтаксисе, который:
- Убирает двусмысленность
- Делает каждое требование проверяемым
- Позволяет проследить от проблемы до кода
- Понятен и людям, и AI-агентам

**Это НЕ**:
- Описание проблемы (это Problem Statement)
- Технический дизайн (это Approach/Design)
- Список задач (это Tasks)
- Тесты (хотя требования → тесты)

**Это**:
- Контракт поведения системы
- Source of truth для верификации
- Вход для AI-агентов при генерации кода
- Основа для acceptance testing

---

## Почему EARS

### История и происхождение

EARS (Easy Approach to Requirements Syntax) разработан **Alistair Mavin** и коллегами в **Rolls-Royce PLC** при анализе airworthiness regulations для системы управления jet engine. Опубликован в 2009.

**Используется в**: Airbus, Bosch, Dyson, Honeywell, Intel, NASA, Rolls-Royce, Siemens.

### Почему именно EARS в нашем процессе

| Критерий | Оценка | Пояснение |
|----------|--------|-----------|
| Простота | ⭐⭐⭐⭐⭐ | 5 паттернов, легко запомнить |
| Однозначность | ⭐⭐⭐⭐⭐ | Убирает ambiguity по структуре |
| Testability | ⭐⭐⭐⭐⭐ | Каждое требование → тест |
| AI-friendly | ⭐⭐⭐⭐⭐ | Kiro использует EARS нативно |
| Human-friendly | ⭐⭐⭐⭐ | Простой синтаксис, понятен без обучения |
| Tool support | ⭐⭐⭐⭐ | Kiro, Spec Kit, линтеры |
| Промышленный опыт | ⭐⭐⭐⭐⭐ | Аэрокосмос, автомобиль, промышленность |

### Сравнение с альтернативами

| Формат | Пример | Плюсы | Минусы |
|--------|--------|-------|--------|
| **EARS** | `When X, the system shall Y` | Однозначный, тестовый | Не исполняемый |
| **User Stories** | `As a user, I want X` | Простой, Agile-friendly | Слишком поверхностный |
| **Gherkin (BDD)** | `Given X, When Y, Then Z` | Исполняемый | Требует step definitions |
| **Formal (TLA+)** | `∀x ∈ S: P(x)` | Математически строгий | Слишком сложный |
| **Plain text** | `The system should handle errors` | Гибкий | Двусмысленный, не тестовый |

**Наш выбор**: EARS для спецификации + опционально BDD для исполняемых сценариев.

---

## 5 Паттернов EARS

### Generic Syntax

```
While <optional pre-condition(s)>,
when <optional trigger>,
the <system name> shall <system response>
```

**Правила**:
- Ноль или более предусловий (`While`)
- Ноль или один триггер (`When`)
- Одно имя системы
- Один или более откликов системы (`shall`)

---

### Паттерн 1: Ubiquitous (всегда активные)

**Когда**: Требование всегда активно, без условий и триггеров.

**Синтаксис**:
```
The <system name> shall <system response>
```

**Примеры**:
```markdown
- REQ-001: The mobile phone shall have a mass of less than 200 grams
- REQ-002: The export service shall support CSV and JSON formats
- REQ-003: The API shall respond within 2 seconds for 95th percentile
- REQ-004: All user data shall be encrypted at rest using AES-256
```

**Когда использовать**:
- Физические свойства
- Всегда активные характеристики
- Глобальные ограничения (безопасность, производительность)
- Константы системы

**Проверка**: Можно ли написать тест без триггера? Если да → Ubiquitous.

---

### Паттерн 2: State-Driven (пока состояние)

**Когда**: Требование активно пока указанное состояние остаётся истинным.

**Синтаксис**:
```
While <precondition(s)>, the <system name> shall <system response>
```

**Примеры**:
```markdown
- REQ-005: While there is no card in the ATM, the ATM shall display 
  "insert card to begin"
- REQ-006: While the export is in progress, the system shall display 
  a progress bar with estimated completion time
- REQ-007: While the user session is expired, the system shall redirect 
  to the login page
- REQ-008: While the system is in maintenance mode, the API shall return 
  HTTP 503 for all requests
```

**Когда использовать**:
- Поведение зависит от текущего состояния
- Режимы работы системы
- Условные ограничения
- Переходные состояния

**Проверка**: Есть ли явное состояние которое можно проверить? Если да → State-driven.

**Частая ошибка**: Не путать с Event-driven!
- State-driven: **пока** состояние активно → поведение
- Event-driven: **когда** событие происходит → реакция

---

### Паттерн 3: Event-Driven (когда событие)

**Когда**: Указывает как система должна реагировать на конкретное событие.

**Синтаксис**:
```
When <trigger>, the <system name> shall <system response>
```

**Примеры**:
```markdown
- REQ-009: When "mute" is selected, the laptop shall suppress all audio output
- REQ-010: When a user submits a form with invalid data, the system shall 
  display validation errors next to the relevant fields
- REQ-011: When the export completes, the system shall send an email 
  notification with the download link
- REQ-012: When a payment fails, the system shall retry up to 3 times 
  with exponential backoff
```

**Когда использовать**:
- Реакция на пользовательские действия
- Обработка событий из внешних систем
- Реакция на изменение данных
- Триггеры и переходы состояний

**Проверка**: Есть ли дискретное событие? Если да → Event-driven.

---

### Паттерн 4: Optional Feature (если включена фича)

**Когда**: Требование применяется только если указанная фича включена.

**Синтаксис**:
```
Where <feature is included>, the <system name> shall <system response>
```

**Примеры**:
```markdown
- REQ-013: Where the car has a sunroof, the car shall have a sunroof 
  control panel on the driver door
- REQ-014: Where multi-language support is enabled, the system shall 
  display UI in the user's selected language
- REQ-015: Where the enterprise plan is active, the system shall allow 
  SSO authentication via SAML 2.0
- REQ-016: Where offline mode is available, the app shall sync data 
  when connectivity is restored
```

**Когда использовать**:
- Функциональность по конфигурации
- Планы подписки (free/pro/enterprise)
- Региональные различия
- Feature flags

**Проверка**: Есть ли конфигурация/план которая включает/выключает фичу? Если да → Optional.

---

### Паттерн 5: Unwanted Behaviour (нежелательное поведение)

**Когда**: Указывает требуемый ответ системы на нежелательные ситуации.

**Синтаксис**:
```
If <trigger>, then the <system name> shall <system response>
```

**Примеры**:
```markdown
- REQ-017: If an invalid credit card number is entered, then the website 
  shall display "please re-enter credit card details"
- REQ-018: If the export file exceeds 1GB, then the system shall switch 
  to streaming mode and notify the user of extended processing time
- REQ-019: If the database connection is lost, then the system shall 
  cache requests locally and retry connection every 30 seconds
- REQ-020: If the user exceeds API rate limit, then the system shall 
  return HTTP 429 with retry-after header
```

**Когда использовать**:
- Обработка ошибок
- Граничные случаи
- Отказоустойчивость
- Валидация и восстановление

**Проверка**: Описываете ли вы что делать когда что-то идёт не так? Если да → Unwanted.

---

### Complex Requirements (комбинации)

**Когда**: Нужно комбинировать несколько паттернов.

**Синтаксис**:
```
While <precondition(s)>, when <trigger>, the <system name> shall <system response>
```

**Примеры**:
```markdown
- REQ-021: While the aircraft is on ground, when reverse thrust is 
  commanded, the engine control system shall enable reverse thrust

- REQ-022: While the user is authenticated, when they request export, 
  the system shall generate the file within 30 seconds

- REQ-023: While the system is in peak mode (>1000 concurrent users), 
  when a new request arrives, the system shall queue the request and 
  process within 60 seconds
```

**Правило**: Не более 1 `While` + 1 `When` на требование. Если нужно больше — разбейте на несколько требований.

---

## Требования к качеству требований

### Критерии качества (из IREB)

Каждое требование должно быть:

| Критерий | Описание | Проверка |
|----------|----------|----------|
| **Необходимость** | Требование нужно для решения проблемы | Ссылка на Problem Statement |
| **Однозначность** | Только одно прочтение | Может ли два человека понять по-разному? |
| **Полнота** | Все условия и реакции указаны | Нет скрытых допущений |
| **Проверяемость** | Можно написать тест | Есть конкретные значения/условия |
| **Прослеживаемость** | Связь с проблемой и кодом | Есть ID, ссылки |
| **Атомарность** | Одно требование = одна мысль | Нет "и" между разными вещами |
| **Независимость** | Не зависит от других требований | Можно проверить изолированно |
| **Реализуемость** | Технически возможно | Не требует невозможного |

### SMART для требований

```
Specific   — конкретное, не расплывчатое
Measurable — можно измерить/проверить
Achievable — технически реализуемо
Relevant   — решает реальную проблему
Time-bound — есть временные рамки (если применимо)
```

**Пример трансформации**:
```
❌ Bad:  "System should be fast"
✅ Good: "The search API shall return results within 200ms 
          for 95th percentile under load of 1000 concurrent users"
```

---

## Нумерация и именование

### Формат

```
REQ-<NNN>: <краткое название>
```

Или с префиксом фичи:

```
REQ-<FEATURE>-<NNN>: <краткое название>
```

**Примеры**:
```
REQ-EXP-001: Export shall support CSV format
REQ-EXP-002: Export shall complete within 30 seconds
REQ-AUTH-001: Login shall accept special characters in password
```

### Правила нумерации

1. **Последовательная**: 001, 002, 003...
2. **Не переиспользуется**: Удалённое требование не освобождает номер
3. **Стабильная**: Номер не меняется при рефакторинге
4. **Уникальная**: Один номер — одно требование

### Категоризация

Для крупных проектов, группируйте требования:

```markdown
## Functional Requirements
- REQ-FUNC-001: ...
- REQ-FUNC-002: ...

## Non-Functional Requirements
### Performance
- REQ-PERF-001: ...

### Security
- REQ-SEC-001: ...

### Reliability
- REQ-REL-001: ...

### Usability
- REQ-USE-001: ...
```

**Категории** (из [ISO/IEC 25010](https://www.iso.org/standard/35733.html)):
- Functional suitability
- Performance efficiency
- Compatibility
- Usability
- Reliability
- Security
- Maintainability
- Portability

---

## Шаблоны файлов

### Шаблон: Lightweight (для small features)

```markdown
# Feature: <Feature Name>

## Problem Statement
[1-2 абзаца проблемы — см. module/problem-statement.md]

## Requirements

### Functional
- REQ-001: [Ubiquitous] The <system> shall <response>
- REQ-002: [Event] When <trigger>, the <system> shall <response>
- REQ-003: [Unwanted] If <error condition>, then the <system> shall <response>

### Non-Functional
- REQ-004: [Performance] The <system> shall respond within <time>
- REQ-005: [Security] The <system> shall encrypt <data> using <algorithm>

## Out of Scope
- [Что явно НЕ делаем в этой итерации]

## Open Questions
- [ ] [Вопрос 1]
- [ ] [Вопрос 2]
```

### Шаблон: Full (для major features)

```markdown
# Feature: <Feature Name> — Requirements Specification

## Metadata
- **Author**: <name>
- **Status**: Draft | In Review | Approved
- **Created**: <date>
- **Last Updated**: <date>
- **Problem Statement**: [link to problem-statement.md]
- **Related PRD**: [link to PRD if exists]
- **Related RFC**: [link to RFC if exists]

## Overview
[1 абзац — что делаем и зачем]

## Stakeholder Requirements

### User Requirements
| ID | Requirement | Priority | Source |
|----|-------------|----------|--------|
| REQ-U-001 | ... | Must | User interview |
| REQ-U-002 | ... | Should | Feedback survey |

### Business Requirements
| ID | Requirement | Priority | Source |
|----|-------------|----------|--------|
| REQ-B-001 | ... | Must | Legal (GDPR) |
| REQ-B-002 | ... | Should | Revenue target |

## System Requirements

### Functional Requirements

#### Ubiquitous
- REQ-F-001: The <system> shall <response>

#### Event-Driven
- REQ-F-002: When <trigger>, the <system> shall <response>

#### State-Driven
- REQ-F-003: While <state>, the <system> shall <response>

#### Optional Feature
- REQ-F-004: Where <feature>, the <system> shall <response>

#### Unwanted Behaviour
- REQ-F-005: If <error>, then the <system> shall <response>

### Non-Functional Requirements

#### Performance
- REQ-NF-001: The <system> shall respond within <time> under <load>

#### Security
- REQ-NF-002: The <system> shall <security requirement>

#### Reliability
- REQ-NF-003: The <system> shall maintain <uptime> availability

#### Scalability
- REQ-NF-004: The <system> shall support <scale> without degradation

## Traceability Matrix

| Requirement | Problem Statement | Design | Test | Code |
|-------------|-------------------|--------|------|------|
| REQ-F-001 | PS-1 | Design §3 | T-001 | `src/export.py` |
| REQ-F-002 | PS-1 | Design §4 | T-002 | `src/notify.py` |

## Acceptance Criteria Summary
[Сводка критериев приёмки для каждого требования]

## Open Questions
- [ ] [Вопрос с владельцем и дедлайном]

## Change Log
| Date | Author | Change | Reason |
|------|--------|--------|--------|
| 2025-01-15 | Alice | Added REQ-F-005 | Security review |
| 2025-01-20 | Bob | Modified REQ-NF-001 | Performance testing |
```

---

## Примеры по доменам

### Пример 1: Data Export Feature

```markdown
# Feature: Data Export — Requirements

## Problem Statement
Users cannot export their data, violating GDPR Article 20 (data portability).
Enterprise customers (40% revenue) blocked. 3 deals lost in Q3.

## Requirements

### Ubiquitous
- REQ-EXP-001: The export service shall support CSV format
- REQ-EXP-002: The export service shall support JSON format
- REQ-EXP-003: The export service shall include all user data 
  (profile, content, metadata)

### Event-Driven
- REQ-EXP-004: When a user requests export, the system shall acknowledge 
  the request within 2 seconds and return an export ID
- REQ-EXP-005: When the export completes, the system shall send an email 
  with download link valid for 7 days
- REQ-EXP-006: When the download link is clicked, the system shall serve 
  the file with Content-Type matching the format

### State-Driven
- REQ-EXP-007: While the export is in progress, the system shall display 
  progress percentage and estimated completion time
- REQ-EXP-008: While the user has an active export job, the system shall 
  prevent duplicate export requests

### Optional Feature
- REQ-EXP-009: Where enterprise plan is active, the system shall allow 
  scheduled exports (daily/weekly/monthly)
- REQ-EXP-010: Where custom fields are configured, the system shall 
  include custom field data in export

### Unwanted Behaviour
- REQ-EXP-011: If the export fails due to timeout (>30 min), then the 
  system shall retry once and notify user via email on second failure
- REQ-EXP-012: If the export file exceeds 5GB, then the system shall 
  split into multiple files and inform the user
- REQ-EXP-013: If the user's account is deleted during export, then 
  the system shall complete the current export before deletion

### Non-Functional
- REQ-EXP-014: [Performance] The system shall complete export within 
  30 seconds for datasets < 10,000 records
- REQ-EXP-015: [Performance] The system shall complete export within 
  30 minutes for datasets > 1,000,000 records using streaming
- REQ-EXP-016: [Security] Export files shall be encrypted at rest 
  using AES-256
- REQ-EXP-017: [Security] Download links shall require authentication 
  and expire after 7 days
- REQ-EXP-018: [Reliability] The export service shall maintain 99.9% 
  availability during business hours
```

### Пример 2: Authentication Feature

```markdown
# Feature: User Authentication — Requirements

## Requirements

### Ubiquitous
- REQ-AUTH-001: The authentication system shall support email/password login
- REQ-AUTH-002: Passwords shall be stored using bcrypt with cost factor ≥ 12
- REQ-AUTH-003: All authentication traffic shall use HTTPS (TLS 1.3+)

### Event-Driven
- REQ-AUTH-004: When a user submits valid credentials, the system shall 
  create a session and redirect to dashboard
- REQ-AUTH-005: When a user submits invalid credentials, the system shall 
  display generic "Invalid credentials" message (not specific field error)
- REQ-AUTH-006: When a user requests password reset, the system shall 
  send reset link valid for 1 hour

### State-Driven
- REQ-AUTH-007: While the user has 5 failed login attempts in 15 minutes, 
  the system shall lock the account for 30 minutes
- REQ-AUTH-008: While the session is active, the system shall refresh 
  the token every 30 minutes

### Optional Feature
- REQ-AUTH-009: Where 2FA is enabled, the system shall require TOTP 
  code after password verification
- REQ-AUTH-010: Where SSO is configured, the system shall redirect 
  to identity provider for authentication

### Unwanted Behaviour
- REQ-AUTH-011: If the token expires during a request, then the system 
  shall attempt silent refresh once before requiring re-login
- REQ-AUTH-012: If the identity provider is unavailable, then the system 
  shall fall back to password authentication and log the incident

### Non-Functional
- REQ-AUTH-013: [Performance] Login shall complete within 500ms 
  including password hash verification
- REQ-AUTH-014: [Security] The system shall never log passwords or tokens
- REQ-AUTH-015: [Security] Rate limiting: max 10 login attempts per 
  IP per minute
```

### Пример 3: API Rate Limiting

```markdown
# Feature: API Rate Limiting — Requirements

## Requirements

### Ubiquitous
- REQ-RL-001: The API gateway shall enforce rate limits on all endpoints
- REQ-RL-002: Rate limits shall be tracked per API key, not per user

### Event-Driven
- REQ-RL-003: When a request arrives, the system shall check current 
  usage against rate limit before processing
- REQ-RL-004: When rate limit is exceeded, the system shall return 
  HTTP 429 with `Retry-After` header

### State-Driven
- REQ-RL-005: While the user is on free plan, the system shall limit 
  to 100 requests per minute
- REQ-RL-006: While the user is on enterprise plan, the system shall 
  limit to 10,000 requests per minute
- REQ-RL-007: While the system is under DDoS attack (>10x normal traffic), 
  the system shall activate emergency rate limiting (10 req/min per IP)

### Unwanted Behaviour
- REQ-RL-008: If the rate limiter service is unavailable, then the 
  system shall allow requests through (fail-open) and alert operations
- REQ-RL-009: If a client exceeds rate limit 100 times in 1 hour, then 
  the system shall temporarily suspend the API key for 24 hours

### Non-Functional
- REQ-RL-010: [Performance] Rate limit check shall add < 1ms latency 
  per request
- REQ-RL-011: [Scalability] Rate limiter shall support 1M unique API keys
- REQ-RL-012: [Reliability] Rate limiter shall use distributed storage 
  (Redis) for multi-instance consistency
```

---

## Workflow: Создание требований

### Шаг 1: От проблемы к требованиям

```
Problem Statement → Вопросы → Требования

Пример:
Problem: "Users cannot export data"
    ↓
Вопросы:
- Какие форматы нужны? → REQ-EXP-001, REQ-EXP-002
- Что входит в экспорт? → REQ-EXP-003
- Как пользователь узнает что экспорт готов? → REQ-EXP-005
- Что если экспорт сломается? → REQ-EXP-011
- Какие ограничения по размеру? → REQ-EXP-012
- Насколько быстро должен быть экспорт? → REQ-EXP-014, REQ-EXP-015
- Какие требования безопасности? → REQ-EXP-016, REQ-EXP-017
```

### Шаг 2: Проверка полноты

Используйте **5 паттернов** как чеклист:

```
☐ Есть ли требования которые всегда активны? (Ubiquitous)
☐ Есть ли состояния которые влияют на поведение? (State-Driven)
☐ Есть ли события на которые система должна реагировать? (Event-Driven)
☐ Есть ли опциональные фичи/планы? (Optional)
☐ Что может пойти не так? (Unwanted Behaviour)
☐ Есть ли нефункциональные требования? (Performance, Security, etc.)
```

### Шаг 3: Ревью

Каждое требование проходит проверку:
- [ ] Однозначно ли оно?
- [ ] Можно ли написать тест?
- [ ] Есть ли конкретные значения?
- [ ] Атомарно ли оно?
- [ ] Нужно ли оно для решения проблемы?

---

## AI-Agent Integration

### Prompt: Генерация требований из Problem Statement

```
Based on this problem statement, generate EARS requirements using all 
5 patterns (Ubiquitous, State-driven, Event-driven, Optional, Unwanted).

Problem Statement:
[paste problem statement]

For each requirement:
- Use REQ-<PREFIX>-<NNN> numbering
- Tag the pattern type
- Make it specific and testable
- Include concrete values where possible

Also identify:
- Non-functional requirements (performance, security, reliability)
- Edge cases and error scenarios
- Out of scope items
```

### Prompt: Ревью требований

```
Review these EARS requirements for:
1. Ambiguity - can any requirement be interpreted multiple ways?
2. Testability - can you write a test for each one?
3. Completeness - are all 5 EARS patterns covered?
4. Atomicity - does any requirement contain multiple concerns?
5. Traceability - does each requirement connect to the problem?

Requirements:
[paste requirements]

Problem Statement:
[paste problem statement]

Output:
- Issues found (with suggestions)
- Missing requirements (suggested additions)
- Requirements that should be split or merged
```

### Prompt: Конвертация из User Stories в EARS

```
Convert these user stories into EARS requirements:

User Stories:
- As a user, I want to export my data so I can back it up
- As an admin, I want to see export logs so I can audit usage
- As a user, I want progress indication so I know it's working

For each user story, generate one or more EARS requirements covering:
- Happy path (Ubiquitous or Event-driven)
- State-dependent behavior (State-driven)
- Error handling (Unwanted Behaviour)
- Edge cases
```

### Prompt: Генерация тестов из требований

```
For each of these EARS requirements, generate:
1. Test name (descriptive)
2. Test scenario (Given-When-Then)
3. Test data needed
4. Expected outcome
5. Edge cases to test

Requirements:
[paste requirements]
```

---

## Валидация и автоматизация

### Линтинг требований

**Проверки** (можно автоматизировать):

```python
# Псевдокод линтера требований
def validate_requirement(req):
    checks = []
    
    # Есть ли system name
    checks.append(has_system_name(req))
    
    # Есть ли конкретные значения (не "быстро", а "200ms")
    checks.append(has_concrete_values(req))
    
    # Атомарность (нет "и" между разными действиями)
    checks.append(is_atomic(req))
    
    # Паттерн определён
    checks.append(has_pattern_tag(req))
    
    # Тестируемость (можно написать assert)
    checks.append(is_testable(req))
    
    return all(checks)
```

**Инструменты**:
- **Custom script**: Python/Bash для проверки формата
- **AI-based**: LLM проверяет на двусмысленность
- **Kiro**: Нативная валидация EARS нотации
- **GitHub Actions**: CI check для формата требований

### Example: GitHub Action для валидации

```yaml
# .github/workflows/requirements-lint.yml
name: Requirements Lint

on:
  pull_request:
    paths:
      - 'specs/**'
      - 'docs/specs/**'

jobs:
  lint-requirements:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check EARS format
        run: |
          python scripts/lint_requirements.py specs/
      - name: Check for ambiguous language
        run: |
          # Проверяем отсутствие слов типа "быстро", "хорошо", "легко"
          grep -rn "should be fast\|should be easy\|should be good" specs/ && exit 1 || true
      - name: Check testability
        run: |
          python scripts/check_testability.py specs/
```

---

## Связь с другими модулями

### ← Problem Statement (вход)

**Как**: Проблема → Вопросы → Требования

```
Problem: "Users can't export data"
    ↓
Questions:
- What formats? → REQ-EXP-001 (CSV), REQ-EXP-002 (JSON)
- How fast? → REQ-EXP-014 (30 sec for <10K records)
- What if it fails? → REQ-EXP-011 (retry + notify)
    ↓
Requirements: REQ-EXP-001 through REQ-EXP-018
```

### → Approach/Design (выход)

**Как**: Требования определяют solution space

```
REQ-EXP-014: Export within 30 seconds for <10K records
REQ-EXP-015: Export within 30 minutes for >1M records (streaming)
    ↓
Design decisions:
- Need async processing (30 seconds too long for sync)
- Need streaming for large datasets
- Need queue (Celery/RQ)
- Need progress tracking
```

### → BDD Scenarios (опциональный выход)

**Как**: Требования → исполняемые сценарии

```
REQ-EXP-004: When user requests export, system shall acknowledge 
             within 2 seconds with export ID
    ↓
Feature: Data Export
  Scenario: Request export returns ID
    Given user "alice" is authenticated
    When alice requests CSV export
    Then response status is 202
    And response contains "export_id"
    And response time is < 2 seconds
```

### → Tests (выход)

**Как**: Требования → тесты

```
REQ-EXP-005: When export completes, system shall send email with link
    ↓
Test cases:
- test_export_complete_sends_email()
- test_email_contains_download_link()
- test_download_link_valid_for_7_days()
- test_no_email_if_user_opted_out()
```

### → ADR (связь)

**Как**: Требования как decision drivers для ADR

```
REQ-EXP-015: Streaming for >1M records
    ↓
ADR-003: Use S3 multipart upload for large exports
Context: REQ-EXP-015 requires streaming for large datasets
Decision: Use S3 multipart upload with 5MB chunks
```

---

## Анти-паттерны

### ❌ Ambiguous Language

**Bad**:
```
- REQ-001: The system should be fast
- REQ-002: The system should handle errors gracefully
- REQ-003: The UI should be user-friendly
```

**Good**:
```
- REQ-001: The search API shall return results within 200ms 
  for 95th percentile
- REQ-002: If a database connection fails, the system shall retry 
  3 times with 1s delay, then return HTTP 503 with error details
- REQ-003: New users shall complete onboarding within 5 minutes 
  without reading documentation
```

**Правило**: Если нельзя написать тест → требование плохое.

---

### ❌ Solution in Requirements

**Bad**:
```
- REQ-001: The system shall use Redis for caching
- REQ-002: The system shall use PostgreSQL database
- REQ-003: The frontend shall be built with React
```

**Good**:
```
- REQ-001: The system shall return cached data within 50ms 
  for repeated queries
- REQ-002: The system shall persist user data with ACID guarantees
- REQ-003: The frontend shall load initial page within 2 seconds 
  on 3G connection
```

**Правило**: Требования описывают ЧТО, не КАК. Как — это Design/Approach.

---

### ❌ Combined Requirements

**Bad**:
```
- REQ-001: The system shall export data in CSV format and send 
  email notification and delete old exports after 7 days
```

**Good**:
```
- REQ-001: The system shall support CSV export format
- REQ-002: When export completes, the system shall send email notification
- REQ-003: The system shall delete export files after 7 days
```

**Правило**: Одно требование = одна мысль. Нет "и" между разными действиями.

---

### ❌ Missing Unwanted Behaviour

**Bad**:
```
- REQ-001: When user requests export, system shall generate file
- REQ-002: When export completes, system shall send email
```

**Good** (добавлены ошибки):
```
- REQ-001: When user requests export, system shall generate file
- REQ-002: When export completes, system shall send email
- REQ-003: If export fails, system shall retry once then notify user
- REQ-004: If email service is down, system shall queue notification 
  and retry for 24 hours
- REQ-005: If user deletes account during export, system shall 
  complete current export before deletion
```

**Правило**: Всегда думайте "что может пойти не так?"

---

### ❌ No Non-Functional Requirements

**Bad**: Только функциональные требования, ничего о производительности/безопасности.

**Good**: Добавьте:
```
### Non-Functional
- REQ-NF-001: [Performance] Response time < 200ms for 95th percentile
- REQ-NF-002: [Security] All data encrypted at rest (AES-256)
- REQ-NF-003: [Reliability] 99.9% uptime during business hours
- REQ-NF-004: [Scalability] Support 10,000 concurrent users
```

---

## Traceability Matrix

Для крупных проектов, ведите матрицу трассировки:

```markdown
| Req ID | Problem | Pattern | Design | Test | Code | Status |
|--------|---------|---------|--------|------|------|--------|
| REQ-EXP-001 | PS-1 | Ubiquitous | Design §3.1 | T-001 | `export.py:L45` | ✅ Done |
| REQ-EXP-004 | PS-1 | Event | Design §4.2 | T-004 | `api.py:L120` | 🔨 In Progress |
| REQ-EXP-011 | PS-1 | Unwanted | Design §5.1 | T-011 | `retry.py:L30` | ⬜ TODO |
| REQ-EXP-014 | PS-1 | NF-Perf | Design §6.1 | T-014 | `perf_test.py` | ✅ Done |
```

**Колонки**:
- **Req ID**: Идентификатор требования
- **Problem**: Ссылка на Problem Statement
- **Pattern**: Какой паттерн EARS
- **Design**: Где в дизайне
- **Test**: Какой тест покрывает
- **Code**: Где реализовано
- **Status**: Статус реализации

---

## Хранение в репозитории

### Структура

```
project/
├── specs/
│   ├── feature-name/
│   │   ├── requirements.md      ← этот документ
│   │   ├── design.md            ← Approach/Design
│   │   ├── tasks.md             ← Tasks breakdown
│   │   └── bdd/                 ← опционально
│   │       └── feature.feature
│   └── ...
├── docs/
│   ├── adr/
│   │   ├── adr-001.md
│   │   └── adr-002.md
│   └── ...
└── tests/
    └── ...
```

### Или для монорепозитория

```
monorepo/
├── packages/
│   ├── export-service/
│   │   ├── specs/
│   │   │   └── requirements.md
│   │   ├── src/
│   │   └── tests/
│   └── ...
└── docs/
    └── adr/
```

---

## Summary

**Requirements (EARS)** — это контракт поведения системы. Ключевые принципы:

1. **5 паттернов** покрывают все случаи:
   - Ubiquitous (всегда)
   - State-driven (пока состояние)
   - Event-driven (когда событие)
   - Optional (если фича включена)
   - Unwanted (если что-то не так)

2. **Качество**:
   - Конкретные значения, не "быстро"
   - Атомарность — одна мысль на требование
   - Тестируемость — можно написать тест
   - Нет решений — только поведение

3. **Полнота**:
   - Все 5 паттернов рассмотрены
   - Нефункциональные требования включены
   - Ошибки и граничные случаи покрыты

4. **Прослеживаемость**:
   - Проблема → Требования → Дизайн → Тесты → Код
   - Матрица трассировки для крупных проектов

5. **Хранение**:
   - В репозитории (Git)
   - Markdown формат
   - Version controlled
   - Reviewable via PR

---

## References

- [EARS Official](https://alistairmavin.com/ears) — Alistair Mavin
- [EARS Wikipedia](https://en.wikipedia.org/wiki/Easy_Approach_to_Requirements_Syntax)
- [EARS Paper (IEEE)](https://ieeexplore.ieee.org/document/5576790)
- [Kiro EARS](https://kiro.dev/docs/specs/feature-specs) — AWS Kiro
- [ISO/IEC 25010](https://www.iso.org/standard/35733.html) — Quality characteristics
- [IREB Requirements Engineering](https://www.ireb.org)
- [Volere Requirements Template](https://www.volere.org)
- [Previous: Problem Statement](./problem-statement.md)
- [Next: ADR](./adr.md)
- [Back to Modules Index](./README.md)
