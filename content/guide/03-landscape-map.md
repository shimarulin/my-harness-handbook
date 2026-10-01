# Глава 3. Карта ландшафта

Ландшафт методологий и инструментов для разработки через документацию разбит на семь доменов. Для каждого — что это, зачем, ключевые варианты и как выбирать. Детали и полные сравнения — в статьях базы знаний.

## 3.1. Управление решениями: ADR и RFC

**ADR (Architecture Decision Record)** — короткая запись единственного решения: контекст, вынудивший выбор, альтернативы, последствия. Одно решение — одна запись; immutable, superseded, never edited. Форматы: **Nygard** (минимум, 5 секций), **MADR** (структурированный, decision drivers + options, рекомендуемый баланс), **YADR** (YAML, machine-readable для CI). → `../content/kb/methods/adr.md`

**RFC (Request for Comments)** — предложение решения, открытое для debate до коммитмента. Нужен, когда решение ещё не принято и есть реальные альтернативы; фиксирует процесс, ADR — результат. → `../content/kb/methods/rfc-vs-sdd.md`

**Когда что:** архитектурное решение с альтернативами → RFC; фиксация принятого решения → ADR; много мелких решений → Y-Statements.

## 3.2. Нотации требований: EARS, истории, Gherkin

**EARS (Easy Approach to Requirements Syntax)** — 5 паттернов (Ubiquitous / While / When / Where / If-Then) + `the <system> shall <response>`: однозначные, тестируемые текстовые требования. Из aerospace (Rolls-Royce), используется в Kiro. Не executable. → `../content/kb/methods/ears.md`

**User Story / Job Story** — лёгкие продуктовые форматы (`As a… I want… so that…` / `When… I want to… so I can…`). Менее строгие, для L1-задач.

**Gherkin (Given-When-Then)** — executable acceptance criteria (BDD). → `../content/kb/landscape/bdd-tools.md`

**Когда что:** EARS для high-level system requirements; Gherkin для executable acceptance criteria; вместе — EARS для требований, Gherkin для сценариев. Принцип: требование в самой дешёвой удерживающей форме ([гл. 2](02-principles.md)).

## 3.3. Исполняемые спецификации: BDD

**BDD** — процесс в трёх практиках (Discovery → Formulation → Automation), закрывающий разрыв бизнес/техника. Ценность — в разговоре при построении сценариев; артефакт (Gherkin + step definitions) — второй слой поддержки, который гниёт быстрее кода, если нет машинной поддержки. Инструменты: **Gauge** (Markdown-спеки, multi-language, AI-friendly), **Cucumber** (JVM), **Reqnroll** (.NET, форк SpecFlow EOL 2024), **Behave** (Python), **Karate** (API). → `../content/kb/landscape/bdd-tools.md`

**Когда:** критичные business rules (финансы, здоровье, право), compliance, сложные workflows. **Когда нет:** simple CRUD, внутренние техфичи, нет business stakeholders.

## 3.4. Архитектурная документация: C4 + arc42

**C4 Model** — диаграммирование на 4 уровнях абстракции (System Context → Container → Component → Code, последний опционально); notation/tooling independent; использовать только уровни, добавляющие ценность. **arc42** — шаблон архитектурного документа из 12 секций (Building Block View — центр). Совместимы официально: arc42 Context and Scope → C4 System Context; Building Block levels 1–3 → Container/Component/Code. → `../content/kb/methods/c4-arc42.md`

**Когда:** L3–L4 инициативы, сложные системы, onboarding. Диаграммы — как код (PlantUML / Mermaid / D2).

## 3.5. Product-артефакты: PRD

**PRD (Product Requirements Document)** — product-артефакт (не технический): что строим и почему, до кода. Анти-паттерн: технический дизайн в PRD (это работа RFC/ADR). → `../content/kb/methods/prd.md`

**Pipeline:** PRD («what & why») → RFC («how? let's debate») → ADR («decided, forever»). Не каждое изменение требует всех трёх.

## 3.6. SDD-инструменты AI-эры

**Spec-Driven Development** — спецификации как source of truth, код — производная. Основные (подробно — `../content/kb/landscape/sdd-tools-overview.md` и критика в [главе 4](04-sdd-and-ai-agents.md)):

| Инструмент | Подход | Сильное | Риск |
|---|---|---|---|
| **GitHub Spec Kit** (139K) | Slash commands, constitution → specify → plan → tasks → implement | Структура, 38 интеграций, экосистема | Тяжесть, waterfall-like, greenfield-bias |
| **OpenSpec** (126K) | Lightweight, /opsx, без phase gates, delta specs | Лёгкость, brownfield, переносимость | Advisory verification, multi-repo, bus factor 1 |
| **BMAD-METHOD** (48K) | 12+ специализированных агентов | Полный SDLC, adversarial review | Overhead, token-heavy, process multiplier |
| **Kiro (AWS)** | IDE/CLI, Req→Design→Tasks, EARS | Спек-пайплайн, GA free tier | Vendor lock (AWS), overkill для quick edits |
| **SpecWeave** | Spec-first + cross-tool handoff | Handoff между вендорами, evidence-gate, ledger | Нишевый (164★), один мейнтейнер |
| **Spec Kitty** | Missions, Research Mission | Evidence-gated research, audit | Молодой (1.7K), форк-модель |
| **specs.md** | Flows (Simple/FIRE/AI-DLC), Ideation | Ideation Flow, adaptive overhead | Молодое community (Dec 2025) |

→ `../content/kb/landscape/sdd-tools-overview.md`, `../content/kb/landscape/spec-weave.md`, `../content/kb/landscape/spec-kitty-research.md`

## 3.7. Docs-as-Code платформы

Сборка и публикация документации из репозитория: **MkDocs Material** (primary, простой, быстрый), **Docusaurus** (React, versioning), **Antora** (AsciiDoc, multi-repo), **Sphinx** (Python+API). → `../content/kb/landscape/toolchain-registry.md`

## Матрица выбора (one-page)

| Нужно | Кандидат |
|---|---|
| Зафиксировать решение | ADR (MADR) |
| Обсудить «как» до кода | RFC |
| Требования системы | EARS |
| Executable acceptance criteria | Gherkin (Gauge/Cucumber) |
| Архитектурная документация | C4 + arc42 |
| Product alignment | PRD |
| Brownfield + AI, лёгкий старт | OpenSpec |
| Greenfield + структура | Spec Kit |
| Research в delivery | Spec Kitty |
| Cross-tool handoff | SpecWeave |
| Публикация доков | MkDocs Material |

---

**Дальше:** [Глава 4. SDD и AI-агенты: что работает, что нет](04-sdd-and-ai-agents.md) — честный разбор критики.
