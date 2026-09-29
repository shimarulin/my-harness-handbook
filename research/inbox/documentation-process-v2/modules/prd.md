# PRD (Product Requirements Document)

Опциональный модуль для продуктовых решений. Описывает **что** строим и **зачем** — до написания первой строчки кода.

---

## Что такое PRD

**PRD** — product-артефакт, определяющий намерение продукта:
- Какую проблему решаем?
- Для кого?
- Почему именно сейчас?
- Как измеряем успех?

**Это НЕ**:
- Технический дизайн (это Approach)
- Архитектурное решение (это ADR)
- Требования к системе (это Requirements/EARS)
- Список задач (это Tasks)

**Это**:
- Обоснование существования фичи/продукта
- Мост между бизнес-потребностью и технической реализацией
- Документ для alignment команды
- Вход для всех последующих артефактов

---

## Когда создавать PRD

### Создавать когда:

1. **Новая продуктовая линейка** — нет прецедента
2. **Крупная фича** (> 1 месяц, несколько команд)
3. **Нужен product alignment** — стейкхолдеры должны согласовать направление
4. **Бюджет > $100k** — нужно обоснование инвестиций
5. **Регуляторные требования** — нужны документы для аудита

### НЕ создавать когда:

- ❌ Баг-фикс
- ❌ Малая фича (< 1 недели)
- ❌ Техническая задача без продуктовых изменений
- ❌ Уже есть ясное направление от руководства

---

## Структура PRD

### Шаблон

```markdown
# PRD: <Feature / Product Name>

- **Author**: <name>
- **Status**: Draft | In Review | Approved
- **Last updated**: <date>
- **Stakeholders**: <PM, eng lead, design, security>
- **Related ADRs**: [links]

---

## Overview
Один абзац: что это и для кого.

## Problem
Пользовательская боль или бизнес-возможность. С доказательствами.

**Формат**: Используйте [Problem Statement](./problem-statement.md) технику.

## Goals
- <Измеримый результат, который мы хотим достичь>
- <Например: "Увеличить activation rate на 10% в Q3">

## Non-goals
- <Что мы явно НЕ делаем в этом цикле>
- <Защита от scope creep>

## Requirements / User Stories

### User Stories
- As a <user>, I want <capability> so that <benefit>.

### Prioritization
| Requirement | Priority | Effort |
|-------------|----------|--------|
| REQ-1: ... | Must | M |
| REQ-2: ... | Should | L |
| REQ-3: ... | Could | S |

## Success Metrics
- <Метрика + целевое значение>
- <Например: "Активация: +10% к концу Q3">
- <Retention: >60% на 30-й день>

## User Experience
- Ссылки на макеты/дизайны
- Ключевые экраны/флоу
- Дизайн-система

## Constraints & Assumptions
### Constraints
- Дедлайны
- Зависимости
- Платформенные ограничения
- Юридические/комплаенс

### Assumptions
- <О пользователях>
- <О технических ограничениях>
- <О бизнес-целях>

## Open Questions
- [ ] <Нерешённые вопросы с владельцем и дедлайном>
- [ ] <Вопрос 2>

## Out of Scope
- <Явно исключено из этого цикла>

## Timeline & Milestones
| Milestone | Date | Deliverable |
|-----------|------|-------------|
| Design complete | W1-W2 | Approved designs |
| Technical RFC | W3 | Approved RFC |
| Alpha | W6 | Internal demo |
| Beta | W8 | Limited release |
| GA | W10 | Full release |

## References
- [Problem Statement](../specs/feature-name/problem-statement.md)
- [Competitor Analysis](https://...)
- [User Research](https://...)
```

---

## Пример PRD

```markdown
# PRD: Data Export Feature

- **Author**: Alice Chen (PM)
- **Status**: Approved
- **Last updated**: 2025-01-15
- **Stakeholders**: Alice (PM), Bob (Eng Lead), Charlie (Design), Diana (Security)

---

## Overview
Users need to export their data from our platform in standard formats (CSV, JSON).
This is required for GDPR compliance and competitive parity.

## Problem

### Problem Statement
Users cannot export their data from our platform. This violates GDPR Article 20
(data portability) and prevents users from backing up their data.

### Evidence
- 3 enterprise deals blocked in Q3 ($2M ARR at risk)
- 23% of feedback surveys mention data export
- Legal requirement: GDPR Article 20, effective since 2018
- Competitor X offers this since 2022

### Impact
- **Revenue**: $2M ARR at risk
- **Legal**: Non-compliance fines up to 4% revenue
- **Customer**: Users trapped in platform (churn risk)

## Goals
- Enable users to export all their data in CSV/JSON formats
- Comply with GDPR Article 20 within Q1
- Unlock enterprise deals blocked by this limitation
- Reduce support tickets related to data access by 50%

## Non-goals
- Real-time sync with external systems
- Import functionality (separate feature, Q3)
- Custom export formats beyond CSV/JSON
- API for programmatic export (separate feature)

## Requirements

### User Stories
- As a **user**, I want to export my data as CSV so that I can back it up
- As a **user**, I want to export my data as JSON so that I can migrate to another platform
- As an **admin**, I want to see export logs so that I can audit data access
- As a **user**, I want to receive email notification when export is ready

### Prioritization
| Requirement | Priority | Rationale |
|-------------|----------|-----------|
| CSV export | Must | GDPR compliance, most common |
| JSON export | Must | Migration use case |
| Email notification | Must | User experience |
| Progress indicator | Should | Large exports take time |
| Export logs for admins | Could | Nice-to-have for enterprise |

## Success Metrics
- **Compliance**: 0 GDPR violations related to data portability
- **Revenue**: Unlock 3 enterprise deals ($2M ARR) within 6 months
- **Support**: 50% reduction in "how do I get my data" tickets
- **Usage**: >30% of active users use export within 6 months
- **Performance**: >95% exports complete within 30 seconds

## Constraints
- **Timeline**: Must ship by end of Q1 (legal deadline)
- **Team**: 2 engineers, 1 designer
- **Infrastructure**: Must work with existing S3 setup
- **Security**: All exports encrypted at rest
- **Privacy**: User consent required for data export

## Assumptions
- Users have sufficient storage for export files
- Most exports < 100MB (edge case: 1GB+)
- Email delivery service available (SendGrid)

## Open Questions
- [ ] Should we limit export frequency? (PM + Eng, by W2)
- [ ] What's the max file size we support? (Eng + Infra, by W2)
- [ ] Do we need to include deleted data in export? (Legal, by W1)

## Timeline
| Milestone | Date | Deliverable |
|-----------|------|-------------|
| PRD Approved | Jan 15 | This document |
| Technical RFC | Jan 22 | RFC-004: Export Architecture |
| Design Complete | Feb 1 | Approved designs |
| Alpha | Feb 15 | Internal demo |
| Beta | Mar 1 | 5% of users |
| GA | Mar 15 | Full release |

## References
- [Problem Statement](../specs/export/problem-statement.md)
- [GDPR Article 20](https://gdpr.eu/article-20-right-to-data-portability/)
- [Competitor Analysis](https://notion.example.com/competitor-export)
- [User Research - Data Needs](https://research.example.com/data-needs)
```

---

## AI-Agent Integration

### Prompt: Генерация PRD из идеи

```
Help me create a PRD for this product idea:

Idea: [brief description]
Target users: [who]
Problem: [what pain we solve]

Generate a PRD with:
1. Overview
2. Problem (use 5 Whys technique)
3. Goals (measurable)
4. Non-goals
5. User stories (with priorities)
6. Success metrics (quantitative)
7. Constraints and assumptions
8. Open questions
9. Timeline suggestion
```

### Prompt: Ревью PRD

```
Review this PRD for:
1. Clarity: Is the problem and goal clear?
2. Evidence: Is there data supporting the need?
3. Measurability: Can success be quantified?
4. Completeness: Are there gaps?
5. Feasibility: Can this be achieved with constraints?

PRD:
[paste PRD]

Provide:
- Issues found
- Missing sections
- Suggestions for improvement
- Questions to resolve
```

### Prompt: PRD → Requirements

```
Based on this PRD, generate EARS requirements:

PRD:
[paste PRD content]

Generate:
1. Functional requirements in EARS notation (all 5 patterns)
2. Non-functional requirements (performance, security, usability)
3. Edge cases and error scenarios
4. Requirements traceability back to PRD sections
```

---

## Связь с другими модулями

### → Requirements (выход)
**Как**: PRD определяет направление → Requirements детализируют поведение

```
PRD Goal: "Enable CSV/JSON export"
    ↓
Requirements:
- REQ-001: The export service shall support CSV format
- REQ-002: When export completes, system shall send email
```

### → RFC (выход)
**Как**: После PRD нужен RFC для архитектурных решений

```
PRD Approved
    ↓
RFC: "Export Architecture"
- Options: sync vs async
- Options: S3 vs local storage
- Options: polling vs push notifications
```

### → ADR (выход)
**Как**: Решения из PRD фиксируются как ADR

```
PRD Constraint: "Must comply with GDPR"
    ↓
ADR-012: "Encrypt all exports at rest"
```

---

## Анти-паттерны

### ❌ PRD как технический дизайн
**Bad**: PRD содержит "мы будем использовать PostgreSQL и Celery"
**Good**: PRD описывает ЧТО и ЗАЧЕМ, не КАК

### ❌ Нет метрик успеха
**Bad**: "Мы хотим сделать экспорт"
**Good**: "Мы хотим увеличить экспорт-запросы до 30% активных пользователей за 6 месяцев"

### ❌ Нет non-goals
**Bad**: Нет явных ограничений
**Good**: "Real-time sync НЕ входит в эту фичу"

### ❌ Бесконечный черновик
**Bad**: PRD никогда не утверждается
**Good**: Time-box ревью (1-2 недели), затем решение

---

## References

- [Atlassian PRD Guide](https://www.atlassian.com/agile/product-management/requirements)
- [PRD vs ADR vs RFC](https://aridanemartin.dev/blog/prd-adr-rfc-decision-documents)
- [Product School PRD Template](https://productschool.com/blog/product-strategy/product-template-requirements-document-prd)
- [Previous: Implementation](./implementation.md)
- [Next: RFC](./rfc.md)
- [Back to Modules Index](./README.md)
