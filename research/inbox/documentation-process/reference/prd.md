# Product Requirements Document (PRD)

## Определение

**PRD (Product Requirements Document)** — документ, определяющий **что** строим и **почему**, до написания первой строчки кода. Это product-артефакт, а не технический. Описывает user problem, intended solution, success metrics и scope, намеренно избегая деталей реализации【turn38fetch0】【turn10fetch0】.

## Что входит в PRD

Согласно Atlassian【turn19fetch0】【turn20fetch0】:

| Секция | Описание |
|---|---|
| **Basics and team roles** | Target release date, current status, core team |
| **Objective** | Как проект поддерживает цели организации |
| **Success metrics** | Продукт/фича-специфичные цели и метрики мониторинга |
| **Assumptions** | О пользователях, технических ограничениях, бизнес-целях |
| **Options** | Все product requirements, user stories, importance levels, Jira issues |
| **Supporting documentation** | Mockups, diagrams, visual designs |
| **Open questions** | Вопросы и ответы, отслеживание прогресса |
| **Out of scope** | Что явно исключено |

## Шаблон PRD

Согласно aridanemartin.dev【turn38fetch0】:

```markdown
# PRD: <Feature / product name>
- **Author:** <name>
- **Status:** Draft | In review | Approved
- **Last updated:** 2026-08-09
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

## Что НЕ должен содержать PRD

**Технический дизайн.** Как только PRD начинает специфицировать database schemas или API contracts, он выполняет работу RFC или ADR【turn38fetch0】.

## PRD vs RFC vs ADR

| Characteristic | **PRD** | **RFC** | **ADR** |
|---|---|---|---|
| **Question it answers** | What are we building, and why? | How should we build it? | What did we decide, and why? |
| **Domain** | Product | Technical design | Architecture |
| **Typical author** | Product manager | Any engineer | Engineer / architect |
| **Timing** | Before design & build | Before committing to a design | At the moment of decision |
| **Length** | Medium–long | Medium–long | Short (≈1 page) |
| **Mutability** | Living, then frozen at commitment | Living during review, then resolved | Immutable — superseded, never edited |
| **Where it lives** | Product docs / PM tool | Docs repo or wiki | In the code repo (`docs/adr/`) |
| **Lifespan** | Life of the feature/product | Archived after decision | Permanent historical record |

**Pipeline:** PRD → RFC → ADR
- PRD: «what & why» → intent
- RFC: «how? let's debate» → proposal + feedback
- ADR: «here's what we decided, forever» → permanent record

## Источники

- Atlassian PRD Guide: https://www.atlassian.com/agile/product-management/requirements【turn10fetch0】
- Atlassian PRD Template: https://www.atlassian.com/software/confluence/templates/product-requirements【turn19fetch0】
- Product School PRD Template: https://productschool.com/blog/product-strategy/product-template-requirements-document-prd【turn6search3】
- PRD vs ADR vs RFC: https://aridanemartin.dev/blog/prd-adr-rfc-decision-documents【turn38fetch0】
