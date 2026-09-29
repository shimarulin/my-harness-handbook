# RFC-Driven Development vs Spec-Driven Development

## Определения

### RFC (Request for Comments)

**RFC** — предложение, открытое для обратной связи. У вас есть идея **как** решить проблему — новый сервис, редизайн API, миграция — и вместо прямой имплементации вы записываете это и приглашаете команду poke holes в этом до коммитмента【turn39fetch0】.

### SDD (Spec-Driven Development)

**SDD** — методология, где вы производите письменные артефакты сначала — спецификацию, технический план, разбиение на задачи — и ревьюите каждый перед следующим шагом. Код приходит последним, генерируется против документов, которые вы уже одобрили【turn5fetch0】.

---

## Когда использовать что

| Ситуация | Инструмент |
|---|---|
| **Простая фича, один контекст window** | Lightweight SDD (страница спецификации)【turn7fetch0】 |
| **Сложная фича, много сессий** | SDD (Spec Kit / Kiro / OpenSpec)【turn5fetch0】 |
| **Архитектурное решение, нужны альтернативы** | RFC【turn39fetch0】 |
| **Фиксация уже принятого решения** | ADR【turn39fetch0】 |
| **Product alignment** | PRD【turn38fetch0】 |
| **Технический дизайн, нужен debate** | RFC【turn39fetch0】 |

---

## Стоит ли объединять?

**Да, они дополняют друг друга** как pipeline【turn38fetch0】:

```
PRD                RFC                     ADR
"what & why"  →   "how? let's debate"  →  "here's what we
(product intent)   (proposal + feedback)   decided, forever"
```

1. **PRD** устанавливает *что* продукт требует и *почему* — intent
2. **RFC** предлагает *как* — и команда дебатирует альтернативы
3. **ADR** фиксирует постоянную запись результирующих архитектурных решений

**Не каждое изменение требует все три.** Крошечный баг-фикс не требует ничего. Новая продуктовая линейка может требовать PRD, несколько RFC и дюжину ADR【turn38fetch0】.

---

## Attentive Engineering RFC Process

**Пример прагматичного RFC-процесса** от Attentive【turn2fetch0】【turn3fetch0】:

### Принципы【turn3fetch0】

1. **RFCs are tools for consensus-building** — «Here is the direction we propose. What are we missing?»
2. **Start early, but not prematurely** — когда дизайн структурно завершён
3. **RFCs can be done before, in parallel, or after prototyping**
4. **Avoid perpetual drafts** — документ, который никогда не покидает «draft» статус
5. **Time-box the review period** — по умолчанию 1 неделя для среднего RFC
6. **Authors own the outcome** — авторы empowered to accept or reject feedback
7. **Tenured engineers act as stewards** — Staff+ engineers менторят авторов

### RFC Status Lifecycle【turn3fetch0】

- **Draft**: Initial writing phase
- **In Review**: Ready for broad feedback
- **Changes Requested:** Serious concerns to address
- **Approved / Closed**: Review complete
- **Blocked / Discarded**: Major issues

### Что входит в RFC【turn39fetch0】

- **Context / problem** — что решаем
- **Proposal** — дизайн, за который вы выступаете
- **Alternatives considered** — другие подходы и почему отклонены
- **Trade-offs and risks** — что это стоит
- **Open questions** — где вы хотите feedback

---

## Сравнительная таблица

| Characteristic | **RFC** | **SDD** |
|---|---|---|
| **Фокус** | Proposal + alternatives, open for comment | Specification → Plan → Tasks → Implement |
| **Время жизни** | Living during review, then resolved | Живёт вечно как source of truth |
| **Автор** | Любой engineer | Product manager / любой инженер |
| **Аудитория** | Команда, для feedback | AI-агенты + команда |
| **Результат** | Принятое/отклонённое решение | Исполненная спецификация |
| **AI-агенты** | Не основной фокус | Основной фокус |

---

## Практические рекомендации

### Когда SDD【turn5fetch0】

- Работа outlives один context window
- Feature занимает дни agent sessions
- Multiple люди или агенты работают параллельно
- Greenfield module без существующего кода
- Correctness важнее скорости (auth, money, data retention)

### Когда RFC【turn3fetch0】

- Решение **ещё не сделано**
- Нужны **реальные альтернативы**, не straw men
- Решение затрагивает системы или команды, с которыми вы не работаете ежедневно
- Scope или blast radius изменения достаточно большой

### Когда объединять【turn38fetch0】

- Новая продуктовая линейка: PRD + несколько RFC + дюжина ADR
- Сложная фича с архитектурными решениями: SDD для workflow + RFC для архитектурных дебатов + ADR для фиксации

---

## Источники

- PRD vs ADR vs RFC: https://aridanemartin.dev/blog/prd-adr-rfc-decision-documents【turn38fetch0】
- Attentive RFC Process: https://tech.attentive.com/articles/rfc-process-for-teams【turn2fetch0】
- SDD Without the Hype: https://utsabpant.com/blog/spec-driven-development-without-the-hype【turn5fetch0】
- Scaling via RFCs: https://blog.pragmaticengineer.com/scaling-engineering-teams-via-writing-things-down-rfcs【turn2search1】
