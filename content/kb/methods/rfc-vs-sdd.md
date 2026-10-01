# RFC vs SDD: proposal-driven и spec-driven разработка

| Параметр | Значение |
|---|---|
| Статус | draft |
| Обновлено | 2026-09-30 |

## Что это

**RFC (Request for Comments)** — предложение решения, открытое для обратной связи до коммитмента: автор записывает, **как** он собирается решить проблему, и приглашает команду «poke holes» — искать дыры до начала имплементации. Закрывает дорогие архитектурные ошибки, обнаруживаемые после кода, и согласование решений, затрагивающих чужие системы.

**SDD (Spec-Driven Development)** — методология, где сначала создаются письменные артефакты (спецификация → технический план → разбиение на задачи), каждый ревьюится перед следующим шагом, а код приходит последним и генерируется против одобренных документов. Закрывает работу, не помещающуюся в один context window AI-агента; спецификация живёт вечно как source of truth.

Вердикт источников: это **не конкуренты, а pipeline** — RFC для дебатов о решении, SDD для исполнения одобренного.

## Ключевые концепции

### Pipeline PRD → RFC → ADR

```
PRD                RFC                     ADR
"what & why"  →   "how? let's debate"  →  "here's what we
(product intent)   (proposal + feedback)   decided, forever"
```

Не каждое изменение требует все три: крошечный баг-фикс — ничего; новая продуктовая линейка — PRD + несколько RFC + дюжина ADR.

### Состав RFC-документа

- **Context / problem** — что решаем
- **Proposal** — дизайн, за который выступает автор
- **Alternatives considered** — другие подходы и почему отклонены
- **Trade-offs and risks** — цена решения
- **Open questions** — где нужен feedback

### Attentive Engineering RFC Process: 7 принципов

1. **RFCs are tools for consensus-building** — «Here is the direction we propose. What are we missing?»
2. **Start early, but not prematurely** — когда дизайн структурно завершён.
3. **RFCs can be done before, in parallel, or after prototyping.**
4. **Avoid perpetual drafts.**
5. **Time-box the review period** — по умолчанию **1 неделя** для среднего RFC.
6. **Authors own the outcome** — автор вправе принять или отклонить feedback.
7. **Tenured engineers act as stewards** — Staff+ менторят авторов.

Статусный lifecycle: Draft → In Review → Changes Requested → Approved/Closed; Blocked/Discarded при серьёзных проблемах.

## Сильные и слабые стороны, анти-паттерны

Анти-паттерны RFC: perpetual drafts; преждевременный старт (дизайн структурно не готов); бессрочный review; straw men вместо реальных альтернатив.

Граница SDD: простая фича в один context window не требует полного цикла — достаточно lightweight SDD (одна страница спецификации).

## Сравнение / выбор

| Характеристика | **RFC** | **SDD** |
|---|---|---|
| Фокус | Proposal + alternatives, open for comment | Specification → Plan → Tasks → Implement |
| Время жизни | Living during review, then resolved | Живёт вечно как source of truth |
| Автор | Любой engineer | Product manager / любой инженер |
| Аудитория | Команда (feedback) | AI-агенты + команда |
| Результат | Принятое/отклонённое решение | Исполненная спецификация |
| AI-агенты | Не основной фокус | Основной фокус |

Матрица выбора:

| Ситуация | Инструмент |
|---|---|
| Простая фича, один context window | Lightweight SDD (страница спеки) |
| Сложная фича, много сессий | SDD (Spec Kit / Kiro / OpenSpec) |
| Архитектурное решение, нужны альтернативы | RFC |
| Фиксация уже принятого решения | ADR |
| Product alignment | PRD |
| Технический дизайн, нужен debate | RFC |

Когда SDD: работа переживает один context window; дни agent-сессий; параллельная работа людей/агентов; greenfield-модуль; correctness важнее скорости (auth, money, data retention).

Когда RFC: решение ещё не принято; нужны реальные альтернативы; blast radius затрагивает чужие системы/команды.

Когда объединять: сложная фича с архитектурными решениями — SDD для workflow + RFC для архитектурных дебатов + ADR для фиксации.

## Источники

- PRD vs ADR vs RFC: https://aridanemartin.dev/blog/prd-adr-rfc-decision-documents
- Attentive RFC Process: https://tech.attentive.com/articles/rfc-process-for-teams
- SDD Without the Hype: https://utsabpant.com/blog/spec-driven-development-without-the-hype
- Scaling via RFCs (Pragmatic Engineer): https://blog.pragmaticengineer.com/scaling-engineering-teams-via-writing-things-down-rfcs
- Входные материалы inbox: `documentation-process/reference/rfc-vs-sdd.md`
