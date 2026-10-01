# Architecture Decision Records: стандарты

## Определение ADR

**Architecture Decision Record (ADR)** — короткая, фокусированная запись единственного архитектурного решения: что выбрали, контекст, вынудивший выбор, альтернативы и последствия. **Одно решение — одна запись**【turn39fetch0】.

---

## 1. Michael Nygard Format (Классический)

**Оригинальная статья:** https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions【turn17fetch0】

### Структура【turn17fetch0】

```
# ADR 1: Deployment on Ruby on Rails 3.0.10

## Title
Short noun phrases, e.g. "ADR 9: LDAP for Multitenant Integration"

## Context
Forces at play, including technological, political, social, and project local.
These forces are probably in tension.

## Decision
Our response to these forces. Stated in full sentences, with active voice.
"We will ..."

## Status
"proposed" | "accepted" | "deprecated" | "superseded"

## Consequences
The resulting context, after applying the decision.
All consequences should be listed here, not just the "positive" ones.
```

### Хранение【turn17fetch0】

- `doc/arch/adr-NNN.md` в репозитории проекта
- **Sequential и monotonic** нумерация
- Номера **не переиспользуются**
- При reversal: старый ADR помечается как **superseded**

### Ключевые принципы【turn17fetch0】

- Document должен быть **1-2 страницы**
- Писать как **conversation with a future developer**
- Full sentences, organized into paragraphs
- Bullets acceptable only for visual style, не как excuse для sentence fragments

---

## 2. MADR (Markdown Architectural Decision Records)

**Официальный сайт:** https://adr.github.io/madr【turn0search2】
**GitHub:** https://github.com/adr/madr【turn0search3】

### Версии

- **MADR 4.0.0** (released 2024-09-17)【turn0search2】

### Шаблоны【turn4search1】

MADR предоставляет **четыре шаблона**:

1. **adr-template.md** — все секции с объяснениями
2. **adr-template-minimal.md** — только обязательные секции с объяснениями
3. **adr-template-bare.md** — все секции, пустые (без объяснений)
4. **adr-template-bare-minimal.md** — обязательные секции, без объяснений

### Полная структура (bare template)【turn9find0】

```markdown
# <Title>

## Context and Problem Statement

## Decision Drivers

## Considered Options

## Decision Outcome

Chosen option: "<option>", because <reasoning>

### Consequences

* Good, because <positive consequence>
* Bad, because <negative consequence>

### Confirmation

## Pros and Cons of the Options

### <Option 1>

* Good, because <pro>
* Bad, because <con>

### <Option 2>

* Good, because <pro>
* Bad, because <con>

## More Information
```

### Минимальная структура (bare-minimal)【turn7fetch0】

```markdown
# <Title>

## Context and Problem Statement

## Considered Options

## Decision Outcome

### Consequences
```

### Пример (Short Version)【turn1fetch0】

```markdown
# Use Plain JUnit5 for advanced test assertions

## Context and Problem Statement
How to write readable test assertions?
How to write readable test assertions for advanced tests?

## Considered Options
* Plain JUnit5
* Hamcrest
* AssertJ

## Decision Outcome
Chosen option: "Plain JUnit5", because it is a standard framework
and the features of the other frameworks do not outweigh the
drawback of adding a new dependency.
```

---

## 3. YADR (YAML ADR)

**YADR** — вариант MADR в YAML формате, где абстрактный ADR template синтаксис также доступен в YAML【turn3search3】.

- YAML почти так же human-readable, как Markdown
- Может быть обработан инструментами гораздо проще
- Многочисленные YAML parsers существуют

---

## 4. ISO/IEC/IEEE 42010:2022

**Стандарт:** ISO/IEC/IEEE 42010:2022【turn11fetch0】

### Концептуальная модель【turn11fetch0】【turn12fetch0】

```
Entity of Interest
    ↓
Architecture
    ↓
Architecture Description (AD)
    ↓
Stakeholders → Concerns
    ↓
Stakeholder Perspectives (new in 2022)
    ↓
Architecture Viewpoints → Architecture Views
    ↓
View Components (renamed from Architecture Models)
    ↓
Architecture Aspects (new in 2022)
```

### Ключевые концепции【turn12fetch0】

| Концепция | Определение |
|---|---|
| **Stakeholder** | Individuals, groups or organizations holding Concerns |
| **Concern** | Any interest in the system (purpose, functionality, structure, behavior) |
| **Architecture Viewpoint** | Conventions for constructing, interpreting one type of Architecture View |
| **Architecture View** | Expresses Architecture from perspective of Stakeholders to address Concerns |
| **Architecture Decision** | Affects AD Elements, pertains to Concerns |
| **Architecture Rationale** | Records explanation, justification about Architecture Decisions |

### Architecture Frameworks (примеры)【turn12fetch0】

- MODAF
- TOGAF
- Kruchten's 4+1 View Model
- RM-ODP

### Architecture Description Languages (ADLs)【turn12fetch0】

- Rapide, SysML, ArchiMate, ACME, xADL

---

## Сравнение стандартов

| Standard | Формат | Сложность | Порог входа |
|---|---|---|---|
| **Nygard** | Markdown | Минимальная (5 секций) | Очень низкий |
| **MADR** | Markdown | Низкая (структурированный) | Низкий |
| **YADR** | YAML | Низкая (machine-readable) | Низкий |
| **ISO 42010** | Conceptual model | Высокая (мета-модель) | Высокий |

---

## Рекомендации по выбору

### Nygard Format
- **Быстрый старт**, минимум bureaucracy
- Маленькие команды, простые решения

### MADR
- **Стандартизированный**, с Decision Drivers и Options
- Средние команды, нужен structured подход
- Интеграция с tooling (adr-tools, linting)

### YADR
- **Machine-readable**, для automation
- CI/CD pipelines, метрики, dashboard

### ISO 42010
- **Enterprise**, compliance
- Крупные организации, audited systems

---

## Источники

- Nygard Original: https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions【turn17fetch0】
- MADR: https://adr.github.io/madr【turn0search2】
- MADR GitHub: https://github.com/adr/madr【turn0search3】
- MADR Examples: https://adr.github.io/madr/examples.html【turn1fetch0】
- MADR Templates: https://github.com/adr/madr/tree/main/template【turn4search1】
- ISO 42010: http://www.iso-architecture.org/42010/cm【turn11fetch0】
- YADR (Zimmermann): https://ozimmer.ch/practices/2022/11/22/MADRTemplatePrimer.html【turn3search3】
