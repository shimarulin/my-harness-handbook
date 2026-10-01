# Глава 7. AI-агенты в процессе

Как встроить AI-агентов в процесс так, чтобы они усиливали, а не дестабилизировали его: durable context, разделение ролей, протоколы handoff, верификация. Детали — `../content/kb/methods/agents-constitution.md`, `../content/kb/methods/ai-agent-workflows.md`.

## 7.1. Durable context: AGENTS.md и CONSTITUTION.md

Агенту нужен не переобъяснение в каждом промпте, а слой контекста, который он читает до любой задачи:

- **AGENTS.md** — открытый cross-tool стандарт операционных правил «как работать в этом репо» (де-факто стандарт). Обновляется регулярно. Layered setup: canonical `AGENTS.md` в корне + tool-specific файлы импортируют (`# CLAUDE.md` → `@AGENTS.md`); в monorepo агент использует ближайший AGENTS.md в дереве.
- **CONSTITUTION.md** — immutable high-level principles «почему так строим» (происхождение: Spec Kit). Меняется только через RFC; содержит Governance-секцию (amendment process). Ключевое: **конституция — не конфиг-файл** — каждый запрет с rationale («don't do X because Y, and instead do Z»), иначе агент pattern-match'ит против.

Порядок чтения агентом: CONSTITUTION.md (inviolable principles) → AGENTS.md (operational rules) → specs/\<feature\>/ (что строим). Закрепляется секцией `## Mandatory Context (read before any task)`.

Правила AGENTS.md: точные команды с полными флагами; конкретные версии стека; < 500 строк; позитивные инструкции; security prominent; обновлять при смене конвенций («устаревший AGENTS.md хуже отсутствующего»).

## 7.2. Разделение ролей (human / AI)

Принцип P8: **человек утверждает, агент исполняет**. Approval-гейты у людей.

| Этап | Человек | AI-агент |
|---|---|---|
| Idea/PRD | Формулирует, ревьюит, утверждает | Черновик, сбор open questions |
| RFC | Дебатирует, утверждает | Alternatives, trade-offs, risks |
| Spec | Утверждает (gate) | Черновик EARS из PRD/RFC |
| ADR | Принимает решение | MADR-черновик |
| Tasks | Приоритизирует | Разбиение |
| Code | Ревьюит PR | Имплементация по spec+tasks, сверка code↔spec |

**5 принципов работы с агентами**: AI = collaborator, не authority; Context is King; Verification is Mandatory («trust but verify»); Iteration over Perfection; Human-in-the-Loop Gates (архитектурные → ADR, продуктовые → PRD, выбор альтернатив → RFC, финальный ревью кода — всегда за человеком).

## 7.3. HITL-паттерны (протоколы handoff)

1. **AI Drafts, Human Decides** (ADR, RFC, PRD): агент черновик → человек ревьюит и решает.
2. **AI Generates, Human Validates** (Requirements, Tasks, API Specs): агент → автопроверки → человек валидирует.
3. **AI Assists, Human Executes** (Implementation, Testing): человек описывает → агент подсказывает → человек реализует.
4. **Human Defines, AI Implements** (Implementation после approval): человек спека → агент код → автотесты → человек ревьюит → merge.

**Жёсткие правила агентов** (закрепляются в AGENTS.md): не имплементировать без approved-спеки (кроме L0); перед имплементацией прочитать constitution → spec → tasks → ADR; любое отклонение от спеки — стоп и вопрос человеку; принципиальные решения не принимать — оформлять draft ADR; по завершении обновить tasks.md и (при поведенческом изменении) scenarios.

## 7.4. Верификация (4 уровня)

1. **Automated** (CI): формат, синтаксис, линтеры — при каждом коммите.
2. **AI Review**: логика, полнота, соответствие — после генерации.
3. **Peer Review**: корректность, целесообразность — перед merge.
4. **Human Decision**: архитектурные/продуктовые решения — в критических точках.

Противодействие феноменам деградации ([глава 4](04-sdd-and-ai-agents.md)): явные маркеры неопределённости (`NEEDS CLARIFICATION`, `DECIDE`) против умолчаний; регулярная сверка с reference после каждой итерации + явные границы изменений против дрейфа; diff-based подход + property-based тесты против эрозии; канонические примеры (`examples/`) + архитектурные принципы в `ARCHITECTURE.md` против наплыва.

## 7.5. Контекстная инженерия

Деградация (повторы, галлюцинации) начинается при заполнении **50–60% контекстного окна**. Четыре стадии: понимание (что модель видит: системный промпт, AGENTS.md, skills, MCPs, tools) → мониторинг (программная проверка заполнения, порог 60%) → планирование (оценить размер задачи, большую разбить, ненужные MCPs выгрузить) → прунинг (`/compact` с инструкциями, не `/clear`). Delta-подход: загружать только изменения.

## 7.6. Метрики успеха

Agent onboarding time < 15 мин (до первого корректного PR); context accuracy > 80% (задач без уточнений); convention violations < 1 per PR; agent iteration count < 3; compliance rate > 95%; drift incidents < 2/мес. → `../content/kb/methods/agents-constitution.md`, `../content/kb/methods/metrics-dashboards.md`.

---

**Дальше:** [Глава 8. Исследовательские процессы](08-research-processes.md) — как вести research внутри проекта.
