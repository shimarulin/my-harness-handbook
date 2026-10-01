# PRD (Product Requirements Document)

| Параметр | Значение |
|---|---|
| Статус | draft |
| Обновлено | 2026-09-30 |

## Что это

**PRD** — product-артефакт (не технический), определяющий **что** строим и **почему**, до написания первой строчки кода: user problem, intended solution, success metrics, scope — намеренно без деталей реализации. Типичный автор: product manager. Жизненный цикл: living document, frozen at commitment; живёт в product docs / PM tool на протяжении жизни фичи/продукта.

## Ключевые концепции

### Секции PRD по Atlassian

| Секция | Содержимое |
|---|---|
| Basics and team roles | Target release date, current status, core team |
| Objective | Как проект поддерживает цели организации |
| Success metrics | Цели и метрики мониторинга продукта/фичи |
| Assumptions | О пользователях, технических ограничениях, бизнес-целях |
| Options | Product requirements, user stories, importance levels, Jira issues |
| Supporting documentation | Mockups, diagrams, visual designs |
| Open questions | Вопросы и ответы, отслеживание прогресса |
| Out of scope | Что явно исключено |

### Шаблон (aridanemartin.dev)

```markdown
# PRD: <Feature / product name>
- **Author:** <name>
- **Status:** Draft | In review | Approved
- **Last updated:** <date>
- **Stakeholders:** <PM, eng lead, design>

## Overview
One paragraph: what this is and who it's for.
## Problem
The user pain or business opportunity. Include evidence.
## Goals
- <Measurable outcome we want>
## Non-goals
- <What we are explicitly NOT doing this cycle>
## Requirements / User stories
- As a <user>, I want <capability> so that <benefit>.
- <Prioritize: Must / Should / Could>
## Success metrics
- <Metric + target, e.g. "activation rate +10% in Q3">
## Constraints & assumptions
- <Deadlines, dependencies, platform limits, known unknowns>
## Open questions
- <Unresolved decisions to close before build>
```

## Сильные и слабые стороны, анти-паттерны

Главный анти-паттерн: **технический дизайн в PRD**. Как только PRD начинает специфицировать database schemas или API contracts — он выполняет работу RFC или ADR, размывая границу product/technical.

## Сравнение / выбор: PRD vs RFC vs ADR

| Характеристика | **PRD** | **RFC** | **ADR** |
|---|---|---|---|
| Вопрос | What are we building, and why? | How should we build it? | What did we decide, and why? |
| Домен | Product | Technical design | Architecture |
| Автор | Product manager | Any engineer | Engineer / architect |
| Тайминг | Before design & build | Before committing to a design | At the moment of decision |
| Объём | Medium–long | Medium–long | Short (≈1 page) |
| Изменяемость | Living, frozen at commitment | Living during review, then resolved | Immutable — superseded, never edited |
| Где живёт | Product docs / PM tool | Docs repo or wiki | Code repo (`docs/adr/`) |
| Время жизни | Жизнь фичи/продукта | Archived after decision | Permanent historical record |

Pipeline: PRD («what & why», intent) → RFC («how? let's debate», proposal + feedback) → ADR («here's what we decided, forever», permanent record). См. `content/kb/methods/rfc-vs-sdd.md`.

## Источники

- Atlassian PRD Guide: https://www.atlassian.com/agile/product-management/requirements
- Atlassian PRD Template: https://www.atlassian.com/software/confluence/templates/product-requirements
- Product School PRD Template: https://productschool.com/blog/product-strategy/product-template-requirements-document-prd
- PRD vs ADR vs RFC: https://aridanemartin.dev/blog/prd-adr-rfc-decision-documents
- Входные материалы inbox: `documentation-process/reference/prd.md`
