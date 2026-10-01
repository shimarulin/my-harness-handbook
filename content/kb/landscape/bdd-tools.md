# BDD и исполняемые спецификации: инструменты

| Параметр | Значение |
|---|---|
| Статус | draft |
| Обновлено | 2026-09-30 |

## Что это

**Behaviour-Driven Development (BDD)** — процесс разработки, закрывающий разрыв между бизнесом и техническими людьми. Три цели: collaboration across roles (shared understanding); rapid small iterations (feedback); system documentation, автоматически проверяемая против поведения системы.

Три практики: **Discovery** (what it *could* do — workshops, real-world examples) → **Formulation** (what it *should* do — structured documentation, Gherkin) → **Automation** (what it *does* — automated tests).

```gherkin
Feature: Withdrawing cash
  Rule: Customers cannot withdraw more than their balance
  Scenario: Successful withdrawal within balance
    Given Alice has 234.56 in their account
    When Alice tries to withdraw 40
    Then Alice sees 40 dispensed
```

## Инструменты (по состоянию на 2025; см. свежесть ниже)

| Фреймворк | Язык | Статус |
|---|---|---|
| **Cucumber** | Java, JavaScript, Ruby, Go и др. | Active, наиболее популярный |
| **SpecFlow** | .NET/C# | **End-of-life 31.12.2024**; Tricentis удалил GitHub-проекты |
| **Reqnroll** | .NET/C# | Активный fork SpecFlow (автор — Gáspár Nagy, создатель SpecFlow; BSD 3-Clause) |
| **Behave** | Python | Active |
| **Behat** | PHP | Active |
| **JBehave** | Java | Active, предшественник Cucumber |
| **Gauge** | Multi-language | Active |
| **Karate** | Java / API testing | Active |

Преимущества Cucumber: behavior-driven (не procedure-driven) тесты; структура шагов как guide rails; переиспользование шагов; self-documenting (plain English); интеграции (Selenium WebDriver, Page Object Model).

### Living Documentation

Исполняемые спецификации = source of truth (тест); feature files double as user stories; CI регенерирует документацию на каждый merge; публикация в Confluence/Notion для stakeholders.

## Сильные и слабые стороны, анти-паттерны

### Официальные анти-паттерны Cucumber

1. **Feature-coupled step definitions** — шаги, не переиспользуемые между фичами → взрыв количества step definitions, дублирование, дорогая поддержка. Решение: организовывать шаги по domain concept.
2. **Conjunction steps** — шаг «обо всём» (`Given I have shades and a brand new Mustang`) → сверхспециализированные шаги. Решение: атомарные шаги.

Ключевое предупреждение: «Don't use Cucumber-like tools without following BDD» — инструмент без процесса коллаборации гарантированно убивает успех автоматизации.

### Слабые стороны BDD

1. Дополнительный overhead на старте (не так просто, как unit-test фреймворки).
2. Хороший Gherkin требует практики.
3. Strict behavior independence: каждая операция отдельным сценарием → повторяющийся setup.
4. Риск стать «QA thing»: pigeonhole как тестовый инструмент вместо процесса коллаборации.

### Порог входа

| Аспект | Оценка |
|---|---|
| Синтаксис Gherkin | Лёгкий (Given-When-Then) |
| Инфраструктура | Средняя (step definitions, hooks) |
| Хорошие сценарии | Требуют практики |
| Поддержка | Дорогая при feature-coupled steps |

## Сравнение / выбор

- **BDD vs TDD**: TDD — «does this function do what I coded?»; BDD — «does the system behave the way the business expects?»
- **BDD + SDD**: совместимы — BDD как исполняемые acceptance criteria в specification-фазе SDD.
- **BDD + ADR**: дополняют — BDD фиксирует поведение, ADR — архитектурные решения.
- **BDD + RFC**: разные домены (executable specs vs proposal+debate).

Когда использовать: business и development работают вместе; нужна executable documentation; поведение важно для stakeholders; фичи с чёткими business rules.

Когда НЕ: unit-тестирование (JUnit/pytest); внутреннее техническое тестирование без business stakeholders; маленькие фиксы без behavior change.

## Источники

- Cucumber: https://cucumber.io (+ BDD docs: https://cucumber.io/docs/bdd; anti-patterns: https://cucumber.io/docs/guides/anti-patterns)
- Automation Panda (BDD weaknesses): https://automationpanda.com/2017/07/26/bdd-automation-without-collaboration
- Reqnroll: https://reqnroll.net (+ SpecFlow EOL: https://reqnroll.net/news/2025/01/specflow-end-of-life-has-been-announced)
- BDD Frameworks Comparison: https://qaskills.sh
- Living Documentation BDD: https://qaskills.sh/blog/living-documentation-bdd-cucumber
- Входные материалы inbox: `documentation-process/reference/bdd-alternatives.md`
