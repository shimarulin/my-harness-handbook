# EARS (Easy Approach to Requirements Syntax)

| Параметр | Значение |
|---|---|
| Статус | draft |
| Обновлено | 2026-09-30 |

## Что это

**EARS** — механизм мягкого ограничения («gently constrain») текстовых требований: набор синтаксических паттернов, делающих требования однозначными, тестируемыми и отслеживаемыми, оставаясь читаемой прозой.

Разработан **Alistair Mavin** и коллегами в **Rolls-Royce PLC** при анализе норм лётной годности (airworthiness regulations) для системы управления jet engine; опубликован в **2009** (IEEE paper 5576790). Используют: Airbus, Bosch, Dyson, Honeywell, Intel, NASA, Rolls-Royce, Siemens.

## Ключевые концепции

### Generic syntax

```
While <optional pre-condition(s)>,
when <optional trigger>,
the <system name> shall <system response>
```

Ruleset: ноль или много предусловий; ноль или один триггер; ровно одно имя системы; один или много откликов системы.

### 5 паттернов

| # | Паттерн | Keyword | Шаблон | Пример |
|---|---|---|---|---|
| 1 | **Ubiquitous** | — (без keyword) | `The <system> shall <response>` | «The mobile phone shall have a mass of less than XX grams.» |
| 2 | **State-driven** | While | `While <precondition(s)>, the <system> shall <response>` | «While there is no card in the ATM, the ATM shall display "insert card to begin".» |
| 3 | **Event-driven** | When | `When <trigger>, the <system> shall <response>` | «When "mute" is selected, the laptop shall suppress all audio output.» |
| 4 | **Optional feature** | Where | `Where <feature is included>, the <system> shall <response>` | «Where the car has a sunroof, the car shall have a sunroof control panel on the driver door.» |
| 5 | **Unwanted behaviour** | If/Then | `If <trigger>, then the <system> shall <response>` | «If an invalid credit card number is entered, then the website shall display "please re-enter credit card details".» |

### Complex requirements

Комбинация keywords в одном требовании; порядок: While перед When.

```
While the aircraft is on ground, when reverse thrust is commanded,
the engine control system shall enable reverse thrust.
```

### EARS в Kiro

Kiro (AWS) использует EARS в `requirements.md`, верхний регистр, две строки:

```
WHEN a user submits a form with invalid data
THE SYSTEM SHALL display validation errors next to the relevant fields
```

## Сильные и слабые стороны

Сильные (по преимуществам в Kiro): **clarity** (однозначность), **testability** (требование напрямую переводится в test case), **traceability** (отслеживание через implementation), **completeness** (формат заставляет продумать все conditions).

Слабые: EARS — **не executable** (в отличие от Gherkin), это структурированные текстовые требования; анти-паттерны в первоисточниках явно не каталогизированы.

## Сравнение / выбор: EARS vs Gherkin (BDD)

| Аспект | EARS | Gherkin (BDD) |
|---|---|---|
| Фокус | System requirements | User scenarios |
| Синтаксис | When/While/Where/If-Then + THE SYSTEM SHALL | Given-When-Then |
| Применение | Systems engineering, requirements | Software behavior, collaboration |
| Executable | Нет (структурированные требования) | Да (через step definitions) |
| Происхождение | Aerospace (Rolls-Royce) | Software (Dan North) |

Совместное применение: EARS — для high-level requirements; Gherkin — для детальных executable acceptance criteria.

## Источники

- EARS official (Mavin): https://alistairmavin.com/ears
- Wikipedia: https://en.wikipedia.org/wiki/Easy_Approach_to_Requirements_Syntax
- IEEE paper: https://ieeexplore.ieee.org/document/5576790
- Kiro EARS: https://kiro.dev/docs/specs/feature-specs
- Jama Software: https://www.jamasoftware.com
- Входные материалы inbox: `documentation-process/reference/ears-notation.md`
