# BDD и исполняемые спецификации

## Что такое BDD

**Behaviour-Driven Development (BDD)** — процесс разработки ПО, который закрывает gap между бизнесом и техническими людьми【turn18fetch0】:

- **Encouraging collaboration** across roles to build shared understanding
- **Working in rapid, small iterations** to increase feedback
- **Producing system documentation** that is automatically checked against system's behaviour

---

## Три практики BDD【turn18fetch0】

1. **Discovery** (What it *could* do) — discovery workshops, real-world examples
2. **Formulation** (What it *should* do) — structured documentation
3. **Automation** (What it *does*) — automated tests

---

## Cucumber

**Сайт:** https://cucumber.io【turn18fetch0】

### Преимущества【turn35fetch0】

- **Force tests to be behavior-driven, not procedure-driven**
- **Provide inherent structure with steps** — guide rails for test cases
- **Easy reusability** — new test cases using pre-existing steps
- **Self-documenting** — plain English
- **Integrate with other testing packages** — Selenium WebDriver, Page Object Model

### Gherkin синтаксис

```gherkin
Feature: Withdrawing cash
  Rule: Customers cannot withdraw more than their balance

  Scenario: Successful withdrawal within balance
    Given Alice has 234.56 in their account
    When Alice tries to withdraw 40
    Then Alice sees 40 dispensed
```

---

## Альтернативы Cucumber

### По языкам【turn1search0】【turn1search3】

| Фреймворк | Язык | Статус |
|---|---|---|
| **Cucumber** | Java, JavaScript, Ruby, Go, и др. | Active, наиболее популярный |
| **SpecFlow** | .NET/C# | **End-of-life 31 Dec 2024**【turn8fetch0】 |
| **Reqnroll** | .NET/C# | Активный fork SpecFlow【turn8fetch0】 |
| **Behave** | Python | Active |
| **Behat** | PHP | Active |
| **JBehave** | Java | Active, предшественник Cucumber |
| **Gauge** | Multi-language | Active |
| **Karate** | Java/API testing | Active |

### SpecFlow → Reqnroll

**SpecFlow** достиг **end-of-life 31 декабря 2024**. Tricentis удалил GitHub-проекты【turn8fetch0】.

**Reqnroll** — fork SpecFlow, созданный Gáspár Nagy (оригинальным создателем SpecFlow)【turn8fetch0】:
- Сайт: https://reqnroll.net
- BSD 3-Clause License
- Постоянно расширяется и исправляется

---

## Анти-паттерны и критика

### Официальные анти-паттерны Cucumber【turn18fetch0】

**1. Feature-coupled step definitions**
- Step definitions, которые **не могут быть переиспользованы** между фичами
- Ведёт к **explosion of step definitions**, code duplication, high maintenance costs
- Решение: организовывать шаги по domain concept

**2. Conjunction steps**
- Шаги, объединяющие много разных вещей: `Given I have shades and a brand new Mustang`
- Делает шаги слишком специализированными
- Решение: разбить на атомарные шаги

### Слабые стороны BDD【turn35fetch0】

1. **Extra development overhead at first** — не так просты, как unit-тест фреймворки
2. **Требуется много практики для написания хорошего Gherkin**
3. **Strict behavior independence** — каждая операция покрывается отдельным сценарием, что требует повторяющихся setup
4. **Может стать «QA thing»** — pigeonholed как тестовый инструмент, а не процесс коллаборации

### Ключевое предупреждение【turn21search1】

> «Don't use Cucumber-like tools without following BDD. There is one anti-pattern that is guaranteed to kill your test automation success»

---

## Преимущества BDD vs другие подходы

### BDD vs TDD【turn2search11】

- **TDD**: «does this function do what I coded?»
- **BDD**: «does the system behave the way the business expects?»

### Living Documentation【turn17search4】

- Спецификации исполняемы — source of truth = тест
- Feature files double as user stories
- CI pipelines регенерируют доки на каждый merge
- Публикация в Confluence/Notion для stakeholder access

---

## Порог входа

| Аспект | Оценка |
|---|---|
| **Синтаксис Gherkin** | Лёгкий (Given-When-Then) |
| **Настройка infrastructure** | Средняя (step definitions, hooks) |
| **Хорошее написание сценариев** | Требует практики |
| **Поддержка** | Высокие затраты при feature-coupled steps |

---

## Конфликты с другими подходами

### BDD + Spec-Driven Development

**Совместимы**: BDD может быть частью SDD как исполняемые acceptance criteria в specification фазе【turn1search6】.

### BDD + ADR

**Дополняют**: BDD фиксирует **поведение**, ADR фиксирует **архитектурные решения**【turn39fetch0】.

### BDD + RFC

**Разные домены**: BDD — executable specifications, RFC — proposal + debate【turn39fetch0】.

---

## Рекомендации

### Когда использовать BDD【turn18fetch0】

- Business и development работают вместе
- Нужна executable documentation
- Поведение системы важно для stakeholders
- Фичи с чёткими business rules

### Когда НЕ использовать【turn35fetch0】

- Unit-тестирование (используйте JUnit/pytest)
- Internal technical testing без business stakeholders
- Маленькие фиксы без behavior change

---

## Источники

- Cucumber BDD Docs: https://cucumber.io/docs/bdd【turn18fetch0】
- Cucumber Anti-patterns: https://cucumber.io/docs/guides/anti-patterns【turn18fetch0】
- Automation Panda (Weaknesses): https://automationpanda.com/2017/07/26/bdd-automation-without-collaboration【turn35fetch0】
- Reqnroll (SpecFlow EOL): https://reqnroll.net/news/2025/01/specflow-end-of-life-has-been-announced【turn8fetch0】
- BDD Frameworks Comparison: https://qaskills.sh【turn1search0】
- Living Documentation BDD: https://qaskills.sh/blog/living-documentation-bdd-cucumber【turn17search4】
