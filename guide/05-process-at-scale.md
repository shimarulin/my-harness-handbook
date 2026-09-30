# Глава 5. Проектирование процесса под масштаб

Центральная глава руководства: как набор обязательных артефактов и глубина ревью делаются пропорциональными размеру и цене ошибки инициативы, а не константой. Это прямой ответ на главную критику SDD — «overhead не окупается» ([глава 4](04-sdd-and-ai-agents.md)). Детали — `../research/kb/methods/process-levels.md`, `../research/kb/methods/artifact-pipeline.md`.

## 5.1. Две оси масштаба

| Ось | Что определяет | Диапазон |
|---|---|---|
| **Инициатива (L0–L4)** | Набор артефактов и gates для одного изменения | Выбирается автором при создании артефакта идеи |
| **Организация (S1–S5)** | Процессный контекст проекта/команды (governance, координация) | Определяется размером команды/кодовой базы |

Оси независимы: L3-инициатива возможна в S2-команде (solo с архитектурным решением), L1-задача — в S5-enterprise (hotfix). Это снимает ложную дилемму «лёгкий процесс vs строгий процесс»: они для разных изменений в одной команде.

## 5.2. Уровни инициативы L0–L4

| Уровень | Размер | Обязательные артефакты | Overhead | Ревью |
|---|---|---|---|---|
| **L0** Trivial | Typo, hotfix | Нет; коммит `trivial: …` | ~0 | Code review |
| **L1** Small | Локальное изменение | `tasks/NNN-*.md` (Job Story + чеклист) + PR | ~10–15 мин | Code review |
| **L2** Feature | Фича | PRD-lite + `spec.md` (EARS) + `design.md` (notes) + `tasks.md` | ~2–4 ч | Spec review + code review |
| **L3** Major | Крупная фича, архитектурные последствия | L2 + RFC + ADR (MADR) + Gherkin scenarios + C4 | ~1–2 дня | RFC + ADR + spec + code |
| **L4** Platform | Новая платформа/продукт | L3 + PRD полный (+PR/FAQ) + arc42 + C4 все уровни + quality scenarios | дни | Полное |

Правила: **docs-first** — переход на следующий этап только при approved-артефакте предыдущего (кроме L0); AI-агент не имплементирует без approved-спеки (кроме L0); на L1 задача укладывается в одно context window. Scale-тест: L1 ≤ 15 минут на документацию.

## 5.3. Продвижение между уровнями (только вверх)

Артефакты не выбрасываются, а разворачиваются (обратная совместимость масштаба): L1→L2 — Job Story разворачивается в PRD; L2→L3 — design notes оформляются в RFC, новое архитектурное решение → обязательно ADR; L3→L4 — RFC-серия консолидируется в arc42. Открытый вопрос: понижение уровня не определено (см. [главу 10](10-open-questions.md)).

## 5.4. Модульный пайплайн артефактов

«Не выбирайте pipeline — **соберите его** из нужных модулей». Core-блоки (присутствуют всегда): **Problem Statement → Requirements (EARS) → Approach → Tasks → Implementation + ADR при каждом решении**. Optional-модули по критериям: PRD (новая продуктовая линейка, > $100k, > 1 мес), RFC (реальные альтернативы, cross-team, high-risk), BDD (критичные business rules, compliance), Event Storming, User Story Mapping, Design-First, Formal Methods, API Specs, Research Compendium.

```
Idea → Problem Statement → [PRD] → [discovery] → [RFC] → Requirements (EARS)
     → Approach → [API Specs] → [BDD] → Tasks → Implementation → ADR → Tests → Release
```

Канонический порядок обязателен; каждый артефакт — файл открытого формата с уникальным ID, статусом, ссылкой на предшественника (`traces`) и approval-гейтом у человека. Соответствие уровней и модулей — в `../research/kb/methods/process-levels.md` §5.

## 5.5. Уровни организации S1–S5 (governance)

S1 Solo (ADR только для major, Y-Statements) → S2 Small Team (EARS lightweight + ADR для всех решений) → S3 Growing (+ Approach, Tasks, BDD, RFC, C4) → S4 Large (+ PRD, API Specs, cross-team RFC/ARB) → S5 Enterprise (+ ARB gate, security review, compliance audit). Паттерны роста: vertical, horizontal (shared standards), federation. Триггеры upgrade: team size, длительность, техдолг, coordination overhead, compliance.

## 5.6. Трассировка

Единый механизм: YAML front-matter каждого артефакта (`id, type, status, created, title, traces[], …`). ID-схема: `idea/task/prd/spec-NNN`, `rfc/adr-NNNN`; requirements — `REQ-<FEATURE>-<NNN>` (стабильные, не переиспользуются). CI проверяет: все `traces` существуют, статусы валидны, `superseded` имеет `superseded_by`. Инвариант: ни один значимый артефакт не существует только «в голове» или в чате. → `../research/kb/methods/artifact-pipeline.md` §Трассировка

## 5.7. Пример композиции по размеру

| Сценарий | Состав |
|---|---|
| Bug fix | Problem (commit message) → Implementation |
| Small feature (API endpoint) | Problem → Requirements → Approach → Tasks → Implementation → ADR (если выбрана библиотека) |
| Major feature | PRD → RFC → Requirements → Design (C4) → API Specs → BDD → Tasks → Implementation → ADRs |

Нормативные заполненные эталоны L1/L2/L3 и полный модульный проход (export-service) — `../research/kb/methods/process-examples.md`. Эталоны пригодны как шаблоны и few-shot examples для агентов.

---

**Дальше:** [Глава 6. Структура репозитория и toolchain](06-repository-and-toolchain.md) — каноническая раскладка и реестр инструментов.
