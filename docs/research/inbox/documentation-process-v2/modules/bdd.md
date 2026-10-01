# BDD (Behavior-Driven Development)

Опциональный модуль для создания исполняемых спецификаций. Мост между бизнес-правилами и техническими тестами.

---

## Что такое BDD

**BDD** — процесс разработки ПО, который закрывает разрыв между бизнесом и техническими людьми:
- Поощряет кросс-функциональную коллаборацию
- Работает в быстрых итерациях
- Создаёт документацию, автоматически проверяемую поведением системы

**Это НЕ**:
- Фреймворк тестирования (хотя использует их)
- Замена unit-тестов
- Только про Gherkin синтаксис

**Это**:
- Процесс для общего понимания поведения системы
- Исполняемые спецификации как living documentation
- Мост между requirements и implementation

---

## Три практики BDD

### 1. Discovery (What it could do)
**Цель**: Совместно с командой и стейкхолдерами исследовать поведение

**Инструменты**:
- Example Mapping
- Event Storming
- User Story Mapping

**Результат**: Конкретные примеры (real-world examples)

### 2. Formulation (What it should do)
**Цель**: Записать примеры в структурированном формате

**Инструмент**: Gherkin (Given-When-Then)

**Результат**: `.feature` файлы

### 3. Automation (What it does)
**Цель**: Автоматизировать проверку сценариев

**Инструменты**: Cucumber, Behave, Reqnroll, Gauge

**Результат**: Автоматические тесты + living documentation

---

## Gherkin синтаксис

### Базовая структура

```gherkin
Feature: <Название фичи>
  Краткое описание

  Background:
    Given <предусловие для всех сценариев>

  Rule: <Правило 1>
    Scenario: <Описание сценария>
      Given <состояние>
      When <действие>
      Then <ожидаемый результат>

    Scenario: <Описание сценария 2>
      Given <состояние>
      When <действие>
      Then <ожидаемый результат>
```

### Ключевые слова

| Ключевое слово | Назначение | Пример |
|----------------|-----------|--------|
| **Feature** | Название фичи | `Feature: Data Export` |
| **Background** | Общее предусловие | `Background:` |
| **Rule** | Бизнес-правило | `Rule: Export limits` |
| **Scenario** | Один тест-кейс | `Scenario: CSV export` |
| **Given** | Начальное состояние | `Given user is authenticated` |
| **When** | Действие | `When user requests export` |
| **Then** | Ожидаемый результат | `Then export is queued` |
| **And** | Дополнительное условие | `And email is sent` |
| **But** | Негативное условие | `But no duplicate is created` |

---

## Инструменты

### Сравнение

| Инструмент | Язык | Статус | Особенности |
|-----------|------|--------|-------------|
| [Cucumber](https://cucumber.io) | Java, JS, Ruby, Go | Active | Самый популярный, огромный экосистема |
| [Behave](https://behave.readthedocs.io) | Python | Active | Python-native, простой |
| [Reqnroll](https://reqnroll.net) | .NET/C# | Active | Fork SpecFlow (EOL Dec 2024) |
| [Behat](https://behat.org) | PHP | Active | PHP-native |
| [Gauge](https://gauge.org) | Multi-language | Active | Markdown-based, VS Code |
| [Karate](https://github.com/karatelabs/karate) | Java/API | Active | API testing, без step definitions |
| [FitNesse](https://fitnesse.org) | Multi-language | Legacy | Wiki-based |
| [Concordion](https://concordion.org) | Java | Active | HTML-based |

### Спецификации и альтернативы

**Вместо BDD для API**:
- [Specmatic](https://specmatic.io) — контрактное тестирование из OpenAPI
- [Postman](https://www.postman.com) — коллекции с тестами

**Вместо BDD для E2E**:
- [Playwright](https://playwright.dev) — Playwright + Cucumber
- [Cypress](https://www.cypress.io) — с BDD плагином

---

## Примеры

### Пример 1: Экспорт данных

```gherkin
Feature: Data Export
  As a user
  I want to export my data
  So that I can back it up or migrate

  Background:
    Given user "alice" is authenticated
    And alice has 1000 records

  Rule: Export formats
    Scenario: Export as CSV
      When alice requests CSV export
      Then export is queued
      And alice receives an export ID
      And export completes within 30 seconds
      And email notification is sent

    Scenario: Export as JSON
      When alice requests JSON export
      Then export file is valid JSON
      And file contains all 1000 records

  Rule: Export limits
    Scenario: Cannot export while another export is in progress
      Given alice has an export in progress
      When alice requests another export
      Then request is rejected with "Export already in progress"

  Rule: Error handling
    Scenario: Failed export notifies user
      Given database connection will fail during export
      When alice requests CSV export
      Then export status becomes "failed"
      And alice receives email with error details

  @slow @large-dataset
  Scenario: Large export uses streaming
    Given alice has 10 million records
    When alice requests CSV export
    Then system uses streaming approach
    And memory usage stays below 512MB
    And export completes within 30 minutes
```

### Пример 2: Аутентификация

```gherkin
Feature: User Authentication
  As a user
  I want to securely log in
  So that I can access my data

  Background:
    Given user "bob" with email "bob@example.com" exists
    And bob's password is "correct-horse-battery-staple"

  Rule: Successful login
    Scenario: Login with valid credentials
      When bob submits email and correct password
      Then bob is authenticated
      And session token is issued
      And bob sees dashboard

  Rule: Failed login
    Scenario: Login with wrong password
      When bob submits email and wrong password
      Then login fails with "Invalid credentials"
      And no indication whether email exists (security)

    Scenario: Account lockout after 5 attempts
      Given bob has 4 failed login attempts in last 15 minutes
      When bob submits wrong password again
      Then account is locked for 30 minutes
      And bob sees "Account locked, try again in 30 minutes"

  Rule: Session management
    Scenario: Session expires after inactivity
      Given bob logged in 2 hours ago
      And bob has been inactive for 2 hours
      When bob makes any API request
      Then response is 401 Unauthorized
      And bob must log in again
```

---

## Связь с EARS Requirements

**Правило**: Каждое EARS требование может быть покрыто одним или несколькими BDD сценариями.

```
EARS:
REQ-EXP-004: When a user requests export, the system shall acknowledge 
the request within 2 seconds and return an export ID

    ↓

BDD:
Feature: Data Export
  Rule: Request acknowledgment
    Scenario: Export request returns ID within 2 seconds
      Given user is authenticated
      When user requests CSV export
      Then response status is 202
      And response contains "export_id"
      And response time is less than 2 seconds
```

---

## Step Definitions

### Пример (Python + Behave)

```python
# features/steps/export_steps.py

from behave import given, when, then
import httpx
import time

@given('user "{name}" is authenticated')
def step_impl(context, name):
    context.token = get_auth_token(name)
    context.headers = {"Authorization": f"Bearer {context.token}"}

@when('{name} requests CSV export')
def step_impl(context, name):
    context.start_time = time.time()
    response = httpx.post(
        f"{context.base_url}/api/exports",
        json={"format": "csv"},
        headers=context.headers
    )
    context.response = response

@then('response status is {status_code}')
def step_impl(context, status_code):
    assert context.response.status_code == int(status_code)

@then('response contains "{field}"')
def step_impl(context, field):
    assert field in context.response.json()

@then('response time is less than {seconds} seconds')
def step_impl(context, seconds):
    elapsed = time.time() - context.start_time
    assert elapsed < float(seconds)
```

---

## AI-Agent Integration

### Prompt: Генерация сценариев из требований

```
Based on these EARS requirements, generate BDD scenarios:

Requirements:
[paste requirements]

Generate Gherkin scenarios that:
1. Cover all requirements
2. Include happy path and error paths
3. Use concrete test data
4. Follow Given-When-Then structure
5. Group by business rules
6. Tag scenarios by type (@fast, @slow, @critical)
```

### Prompt: Генерация step definitions

```
Generate step definitions for these scenarios:

Scenarios:
[paste Gherkin]

Tech stack: Python + Behave + httpx

Generate:
1. Step definition functions
2. Helper utilities (auth, setup)
3. Assertions
```

---

## Анти-паттерны (из [официальной документации Cucumber](https://cucumber.io/docs/guides/anti-patterns))

### ❌ Feature-coupled step definitions
**Проблема**: Шаги привязаны к конкретной фиче, не переиспользуются
**Решение**: Организовывать шаги по доменным концепциям, не по фичам

### ❌ Conjunction steps
**Проблема**: `Given I have shades and a brand new Mustang`
**Решение**: Разбить на атомарные шаги

### ❌ BDD без Collaboration
**Проблема**: Использовать Cucumber как test framework без Discovery и Formulation
**Результат**: "This anti-pattern is guaranteed to kill your test automation success"
**Решение**: Следовать всем трём практикам (Discovery, Formulation, Automation)

### ❌ Слишком много сценариев
**Проблема**: Каждый edge case отдельным сценарием
**Результат**: Тысячи сценариев, невозможность поддержки
**Решение**: Использовать Scenario Outline с Examples

---

## Когда использовать

### ✅ Использовать когда:
- Бизнес-правила критичны (финансы, здоровье, право)
- Нужен комплаенс (GDPR, HIPAA, SOX)
- Сложные пользовательские флоу
- Стейкхолдеры должны видеть и понимать тесты
- Нужна living documentation

### ❌ Не использовать когда:
- Простой CRUD без бизнес-правил
- Внутренние технические фичи без бизнес-стейкхолдеров
- Нет времени на поддержку сценариев
- Команда не следует BDD процессу

---

## References

- [Cucumber BDD Documentation](https://cucumber.io/docs/bdd)
- [Cucumber Anti-patterns](https://cucumber.io/docs/guides/anti-patterns)
- [Behave Documentation](https://behave.readthedocs.io)
- [Reqnroll](https://reqnroll.net)
- [Previous: RFC](./rfc.md)
- [Next: API Specs](./api-specs.md)
- [Back to Modules Index](./README.md)
