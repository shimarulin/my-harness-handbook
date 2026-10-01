# Выбор SDD-инструмента: Spec Kit vs OpenSpec

| Параметр | Значение |
|---|---|
| Дата | 2026-09-29 |
| Статус | Draft |
| Связан с | `02-process-design.md`, `03-open-questions-analysis.md` |

---

## 1. Общая стратегия: оба инструмента в арсенале

Поскольку ни один инструмент не является явным лидером для всех сценариев,
мы разрабатываем процессы для **обоих** параллельно. Выбор делается
per-проект (или per-инициатива), с возможностью миграции.

### Принципы

| # | Принцип |
|---|---|
| 1 | Формат артефактов (Markdown) — общий для обоих, что обеспечивает переносимость |
| 2 | Выбор инструмента — не навсегда; критерии миграции определены |
| 3 | Процессы L0–L4 работают в обоих; различия — в workflow создания артефактов |
| 4 | AGENTS.md и CONSTITUTION.md — cross-tool, работают с обоими |

---

## 2. Критерии выбора

### 2.1 Decision Matrix

| Критерий | Spec Kit | OpenSpec | Влияние на выбор |
|---|---|---|---|
| **Greenfield (новый проект)** | ✅ Excellent | ⚠️ Good | Новый проект → Spec Kit |
| **Brownfield (существующий код)** | ⚠️ Workable | ✅ Excellent | Существующий проект → OpenSpec |
| **Guardrails (защита от vibe-coding)** | ✅ Сильные (phase gates) | ⚠️ Слабые | Команда с риском хаотичного AI → Spec Kit |
| **Скорость итерации** | ⚠️ Медленнее | ✅ Быстрее | Solo-dev, быстрый прототип → OpenSpec |
| **Enterprise compliance** | ✅ Поддержка | ⚠️ Ограничена | Регулируемая отрасль → Spec Kit |
| **Delta specs (изменения требований)** | ❌ Нет | ✅ ADDED/MODIFIED/REMOVED | Эволюция требований → OpenSpec |
| **Фрагментация артефактов** | ⚠️ Несколько файлов | ✅ Unified + delta | Минимизация файлов → OpenSpec |
| **Расширяемость** | ✅ Extensions + presets | ⚠️ Schemas + config | Кастомизация → Spec Kit |
| **Runtime** | Python | Node.js/TypeScript | Зависит от стека команды |
| **Overhead per-фича** | ⚠️ Выше (~800 lines) | ✅ Ниже (~250 lines) | Малые фичи → OpenSpec |

### 2.2 Сценарии предпочтения

#### Когда явно выбрать Spec Kit

| Ситуация | Почему |
|---|---|
| **Новая платформа/продукт (L4)** | Constitution-фаза, жёсткие phase gates, enterprise-подход |
| **Команда > 5 человек, распределённая** | Guardrails предотвращают дрейф; формальный workflow |
| **Регулируемая отрасль (fintech, health)** | Compliance-требования, audit trail, формальные фазы |
| **Несколько параллельных AI-агентов** | Phase gates координируют работу |
| **Требуется глубокая кастомизация** | Extension system, presets, overrides |
| **Python-first команда** | Нативный runtime |

#### Когда явно выбрать OpenSpec

| Ситуация | Почему |
|---|---|
| **Существующий проект + AI** | Delta specs: изменения без переписывания legacy |
| **Solo-dev или небольшая команда** | Легче, быстрее, меньше бюрократии |
| **Быстрое прототипирование** | Fluid workflow, нет обязательных фаз |
| **Эволюционирующие требования** | Delta specs track changes elegantly |
| **Малые/средние фичи (L1–L2)** | Меньше overhead per-фича |
| **Node.js/TypeScript команда** | Нативный runtime |
| **Множественные small changes параллельно** | Change directories изолированы |

#### Когда выбрать любой (interchangeable)

| Ситуация | Комментарий |
|---|---|
| **L0 (trivial)** | Оба инструмента — overkill; прямой commit |
| **L1 (small)** | Оба работают; OpenSpec чуть легче |
| **Обучение команды SDD** | Начать с OpenSpec (проще), мигрировать при необходимости |

---

## 3. Миграция между инструментами

### 3.1 Совместимость артефактов

| Артефакт | Spec Kit формат | OpenSpec формат | Мигрируемость |
|---|---|---|---|
| **Спецификация** | `specs/<feature>/spec.md` | `openspec/changes/<id>/specs/` | ✅ Markdown → Markdown |
| **Tasks** | `specs/<feature>/tasks.md` | `openspec/changes/<id>/tasks.md` | ✅ Markdown → Markdown |
| **Design** | В составе spec.md | `openspec/changes/<id>/design.md` | ✅ Раздел → файл |
| **Constitution** | `.specify/memory/constitution.md` | `CONSTITUTION.md` (root) | ✅ Markdown → Markdown |
| **Proposal** | Отсутствует | `openspec/changes/<id>/proposal.md` | ⚠️ Создать при миграции |
| **Delta specs** | Отсутствует | `ADDED/MODIFIED/REMOVED` секции | ⚠️ Сгенерировать diff |

### 3.2 Критерии для миграции

#### Триггеры миграции Spec Kit → OpenSpec

| Триггер | Порог |
|---|---|
| Проект стал brownfield | > 50% изменений — модификация существующего кода |
| Overhead Spec Kit замедляет delivery | Время на документацию > 30% времени на имплементацию |
| Команда сократилась | < 3 человек — guardrails избыточны |
| Требуется быстрое прототипирование | > 5 экспериментальных фич подряд |
| Delta specs стали необходимы | > 3 существенных изменения требований за sprint |

#### Триггеры миграции OpenSpec → Spec Kit

| Триггер | Порог |
|---|---|
| Команда выросла | > 5 человек, распределённая |
| Появились compliance-требования | Регулятор, audit, сертификация |
| Vibe-coding дрейф | > 2 инцидента несоответствия спеке за месяц |
| Проект стал complex | L3–L4 фичи, enterprise architecture |
| Требуется формальный approval workflow | Внешние стейкхолдеры, legal review |

### 3.3 Процедура миграции

#### Spec Kit → OpenSpec

```bash
# 1. Установить OpenSpec
npm install -g @fission-ai/openspec@latest

# 2. Инициализировать в проекте
cd project/
openspec init

# 3. Мигрировать существующие спеки
# Для каждого specs/<feature>/:
#   - Создать openspec/changes/<feature-id>/
#   - Скопировать spec.md → specs/
#   - Скопировать tasks.md → tasks.md
#   - Извлечь design-секции → design.md
#   - Сгенерировать proposal.md из intro

# 4. Перенести constitution
cp .specify/memory/constitution.md CONSTITUTION.md

# 5. Обновить AGENTS.md (если есть)
# Добавить ссылки на OpenSpec workflow
```

#### OpenSpec → Spec Kit

```bash
# 1. Установить Spec Kit
uv tool install specify-cli

# 2. Инициализировать
cd project/
specify init --agent claude

# 3. Мигрировать существующие changes
# Для каждого openspec/changes/<id>/:
#   - Создать specs/<feature>/
#   - Скопировать specs/*.md → spec.md (объединить если fragmentированы)
#   - Скопировать tasks.md → tasks.md
#   - Включить design.md в spec.md (как раздел)

# 4. Перенести constitution
cp CONSTITUTION.md .specify/memory/constitution.md

# 5. Запустить /speckit.constitution для валидации
```

### 3.4 Что не мигрирует автоматически

| Элемент | Spec Kit | OpenSpec | Решение |
|---|---|---|---|
| **Slash commands** | `/speckit.*` | `/opsx:*` | Обновить AGENTS.md и muscle memory |
| **Phase gates** | Обязательные | Опциональные | Определить, нужны ли формальные гейты |
| **Extensions/presets** | Spec Kit extensions | OpenSpec schemas | Переписать под целевой инструмент |
| **CI integrations** | Spec Kit hooks | OpenSpec scripts | Адаптировать pipeline |
| **Delta specs** | Нет | ADDED/MODIFIED/REMOVED | При миграции → OpenSpec: сгенерировать; → Spec Kit: «выпрямить» в полный spec |

### 3.5 Риски миграции

| Риск | Вероятность | Mitigation |
|---|---|---|
| **Потеря истории изменений** | Средняя | Git history сохраняется; delta specs конвертируются |
| **Нарушение ongoing work** | Высокая | Мигрировать между sprint-ами, не mid-feature |
| **Первая фича после миграции — сбой** | Высокая | Pilot: одна малая фича через новый инструмент |
| **Команда сопротивляется** | Средняя | Обосновать триггерами; обучение; parallel run |

---

## 4. Совместное использование (Hybrid)

### 4.1 Сценарий: OpenSpec для разработки, Spec Kit для платформенных решений

```
project/
├── openspec/           # OpenSpec: фичи, изменения, delta specs
│   ├── changes/
│   └── ...
├── specs/              # Spec Kit: платформенные ADR, architecture
│   ├── platform-auth/
│   └── platform-billing/
├── CONSTITUTION.md     # Общий для обоих
├── AGENTS.md           # Общий, описывает оба workflow
└── ...
```

**AGENTS.md в этом случае:**

```markdown
## Workflow Selection

- **Feature development**: Use OpenSpec (/opsx:* commands)
- **Platform/architectural decisions**: Use Spec Kit (/speckit.* commands)
- **Constitution applies to both**: Read CONSTITUTION.md first
```

### 4.2 Сценарий: Миграция поэтапная

```
Phase 1 (Month 1): Новые фичи через OpenSpec, legacy через Spec Kit
Phase 2 (Month 2): Миграция active specs
Phase 3 (Month 3): Полный переход на целевой инструмент
```

---

## 5. Мониторинг и переоценка

### 5.1 Метрики для переоценки выбора

| Метрика | Способ измерения | Порог для переоценки |
|---|---|---|
| **Documentation overhead** | Время на docs / время на код | > 30% |
| **Spec-code alignment** | Процент PR, соответствующих спеке | < 80% |
| **Team velocity** | Story points per sprint | Долгое снижение |
| **Agent iteration count** | Итераций до корректного кода | > 5 per фича |
| **Rework rate** | PR, требующие major rework | > 20% |

### 5.2 Quarterly Review

Каждый квартал:
1. Собрать метрики §5.1
2. Проверить триггеры §3.2
3. Решить: продолжать, мигрировать, или hybrid
4. Задокументировать решение в ADR

---

## 6. Связанные документы

- `02-process-design.md` — уровни L0–L4, работающие с обоими инструментами
- `05-agents-and-constitution-guide.md` — cross-tool AGENTS.md/CONSTITUTION.md
- (план) `06-spec-kit-workflow.md` — детальный workflow для Spec Kit
- (план) `07-openspec-workflow.md` — детальный workflow для OpenSpec
