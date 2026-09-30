# ADR (Architecture Decision Record): стандарты и форматы

| Параметр | Значение |
|---|---|
| Статус | draft |
| Обновлено | 2026-09-30 |

## Что это

**ADR** — короткая, фокусированная запись единственного архитектурного решения: что выбрали, контекст, вынудивший выбор, альтернативы и последствия. Ключевой принцип: **одно решение — одна запись**.

Решаемая проблема: архитектурные решения исчезают в чатах и головах; ADR фиксирует их в краткой читаемой форме рядом с кодом. Nygard называет это «conversation with a future developer».

## Ключевые форматы

### Nygard format (классический, 2011)

Michael Nygard, статья «Documenting Architecture Decisions» (2011-11-15). Пять секций:

- **Title** — short noun phrase («ADR 9: LDAP for Multitenant Integration»)
- **Context** — силы в напряжении: технологические, политические, социальные, проектные
- **Decision** — ответ на силы, полными предложениями, active voice («We will …»)
- **Status** — `proposed` | `accepted` | `deprecated` | `superseded`
- **Consequences** — контекст после применения решения; перечисляются **все** последствия, не только позитивные

Правила хранения и написания:

- файлы `doc/arch/adr-NNN.md` в репозитории проекта;
- нумерация sequential и monotonic; номера не переиспользуются;
- при отмене решения старый ADR помечается `superseded` (не редактируется);
- объём 1–2 страницы; bullets допустимы только для визуального стиля, не как оправдание обрывочных фраз.

### MADR 4.0.0 (2024-09-17)

Markdown Architectural Decision Records — структурированное развитие Nygard. Четыре шаблона: `adr-template.md` (все секции с объяснениями), `adr-template-minimal.md`, `adr-template-bare.md` (все секции пустые), `adr-template-bare-minimal.md`.

Полная структура (bare):

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
## More Information
```

Минимум (bare-minimal): Title → Context and Problem Statement → Considered Options → Decision Outcome (+ Consequences).

Характерные маркеры: формулировка `Chosen option: "...", because ...`; буллеты `Good, because …` / `Bad, because …`. Tooling: adr-tools, linting.

### YADR

MADR в YAML (Oliver Zimmermann, 2022-11-22). Почти так же human-readable, как Markdown, но напрямую machine-readable — для automation: CI/CD pipelines, метрики, dashboards.

### ISO/IEC/IEEE 42010:2022

Не шаблон ADR, а концептуальная мета-модель архитектурного описания: Entity of Interest → Architecture → Architecture Description; Stakeholders → Concerns → Stakeholder Perspectives (новое в 2022) → Viewpoints → Views → View Components (переименовано из Architecture Models) → Architecture Aspects (новое в 2022).

Ключевые термины: **Architecture Decision** — affects AD Elements, pertains to Concerns; **Architecture Rationale** — explanation/justification решений. Фреймворки: MODAF, TOGAF, Kruchten 4+1, RM-ODP. ADL: Rapide, SysML, ArchiMate, ACME, xADL.

## Сильные и слабые стороны

| Формат | Сложность | Порог входа | Когда выбирать |
|---|---|---|---|
| **Nygard** | Минимальная (5 секций) | Очень низкий | Быстрый старт, минимум bureaucracy; маленькие команды, простые решения |
| **MADR** | Низкая (структурированный) | Низкий | Decision Drivers + Options; средние команды; интеграция с tooling |
| **YADR** | Низкая (machine-readable) | Низкий | Automation: CI/CD, метрики, dashboard |
| **ISO 42010** | Высокая (мета-модель) | Высокий | Enterprise, compliance, audited systems |

Границы применимости: Nygard без структуры рискует быть пустым для сложных решений; ISO 42010 избыточен вне регулируемого enterprise. ADR не заменяет RFC (debate до решения) — ADR фиксирует уже принятое решение: immutable, superseded, never edited.

## Источники

- Nygard original: https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- MADR: https://adr.github.io/madr (+ GitHub: https://github.com/adr/madr; examples: https://adr.github.io/madr/examples.html; templates: https://github.com/adr/madr/tree/main/template)
- YADR (Zimmermann, «MADR Template Primer»): https://ozimmer.ch/practices/2022/11/22/MADRTemplatePrimer.html
- ISO 42010 conceptual model: http://www.iso-architecture.org/42010/cm
- Входные материалы inbox: `documentation-process/reference/adr-standards.md`
