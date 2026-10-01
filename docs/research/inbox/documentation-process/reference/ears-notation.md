# EARS (Easy Approach to Requirements Syntax)

## Определение

**EARS** — механизм для мягкого ограничения текстовых требований. EARS паттерны предоставляют структурированное руководство, которое позволяет авторам писать высококачественные текстовые требования【turn7fetch0】.

> «The Easy Approach to Requirements Syntax (EARS) is a mechanism to gently constrain textual requirements»【turn7fetch0】

---

## История【turn7fetch0】

Разработан **Alistair Mavin** и коллегами в **Rolls-Royce PLC** при анализе airworthiness regulations для системы управления jet engine. Опубликован в 2009.

Используется: Airbus, Bosch, Dyson, Honeywell, Intel, NASA, Rolls-Royce, Siemens【turn7fetch0】.

---

## Generic EARS Syntax【turn7fetch0】

```
While <optional pre-condition(s)>,
when <optional trigger>,
the <system name> shall <system response>
```

**Ruleset:**
- Zero or many preconditions
- Zero or one trigger
- One system name
- One or many system responses

---

## 5 Паттернов EARS

### 1. Ubiquitous requirements【turn7fetch0】

Всегда активны (нет EARS keyword):

```
The <system name> shall <system response>
```

**Пример:**
> The mobile phone shall have a mass of less than XX grams.

---

### 2. State-driven requirements (While)【turn7fetch0】

Активны пока указанное состояние остаётся true:

```
While <precondition(s)>, the <system name> shall <system response>
```

**Пример:**
> While there is no card in the ATM, the ATM shall display "insert card to begin".

---

### 3. Event-driven requirements (When)【turn7fetch0】

Указывают как система должна реагировать на triggering event:

```
When <trigger>, the <system name> shall <system response>
```

**Пример:**
> When "mute" is selected, the laptop shall suppress all audio output.

---

### 4. Optional feature requirements (Where)【turn7fetch0】

Применяются в продуктах, которые включают указанную feature:

```
Where <feature is included>, the <system name> shall <system response>
```

**Пример:**
> Where the car has a sunroof, the car shall have a sunroof control panel on the driver door.

---

### 5. Unwanted behaviour requirements (If/Then)【turn7fetch0】

Указывают required system response для undesired situations:

```
If <trigger>, then the <system name> shall <system response>
```

**Пример:**
> If an invalid credit card number is entered, then the website shall display "please re-enter credit card details".

---

## Complex requirements【turn7fetch0】

Комбинация нескольких EARS keywords:

```
While <precondition(s)>, When <trigger>, the <system name> shall <system response>
```

**Пример:**
> While the aircraft is on ground, when reverse thrust is commanded, the engine control system shall enable reverse thrust.

---

## EARS в Kiro

Kiro использует EARS для requirements.md【turn14fetch0】:

```
WHEN [condition/event]
THE SYSTEM SHALL [expected behavior]
```

**Пример из Kiro docs**【turn14fetch0】:
```
WHEN a user submits a form with invalid data
THE SYSTEM SHALL display validation errors next to the relevant fields
```

### Преимущества EARS в Kiro【turn14fetch0】

- **Clarity**: Requirements unambiguous
- **Testability**: Каждое требование напрямую переводится в test cases
- **Traceability**: Отдельные требования отслеживаются через implementation
- **Completeness**: Формат поощряет мышление через все conditions

---

## EARS vs BDD/Gherkin

| Aspect | EARS | Gherkin (BDD) |
|---|---|---|
| **Focus** | System requirements | User scenarios |
| **Syntax** | When/While/Where/If-Then + THE SYSTEM SHALL | Given-When-Then |
| **Target** | Systems engineering, requirements | Software behavior, collaboration |
| **Executable** | No (структурированные требования) | Yes (через step definitions) |
| **Origin** | Aerospace (Rolls-Royce) | Software (Dan North) |

**Совместимость:** EARS для requirements specification, Gherkin для executable scenarios. Могут использоваться вместе: EARS для high-level requirements, Gherkin для детальных acceptance criteria.

---

## Источники

- EARS Official (Alistair Mavin): https://alistairmavin.com/ears【turn7fetch0】
- Wikipedia EARS: https://en.wikipedia.org/wiki/Easy_Approach_to_Requirements_Syntax【turn0search0】
- EARS Paper (IEEE): https://ieeexplore.ieee.org/document/5576790【turn0search3】
- Kiro EARS: https://kiro.dev/docs/specs/feature-specs【turn14fetch0】
- Jama Software EARS: https://www.jamasoftware.com【turn0search2】
