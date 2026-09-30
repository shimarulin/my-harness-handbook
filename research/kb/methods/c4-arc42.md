# C4 Model + arc42: архитектурная документация

| Параметр | Значение |
|---|---|
| Статус | draft |
| Обновлено | 2026-09-30 |

## Что это

**C4 Model** — «easy to learn, developer friendly approach to software architecture diagramming»: диаграммирование архитектуры на нескольких уровнях абстракции. Notation independent, tooling independent.

**arc42** — template для документирования и коммуникации архитектуры: 12 секций, центр тяжести — Building Block View.

Оба решают одну проблему с двух сторон: C4 даёт нотацию диаграмм, arc42 — структуру документа. Совместимы официально (C4 FAQ) и часто комбинируются.

## Ключевые концепции

### C4: уровни и диаграммы

4 уровня абстракции: **Software system** → **Container** (applications, data stores, микросервисы) → **Component** → **Code** (классы/интерфейсы, опционально).

Core-диаграммы (4): System Context, Container, Component, Code (опционально).
Supporting (3): System Landscape, Dynamic, Deployment.

Ключевой принцип: «You don't need to use all 4 levels of diagram; only those that add value».

### arc42: 12 секций

| # | Секция | Содержимое |
|---|---|---|
| 01 | Introduction and Goals | Requirements, stakeholders, top quality goals |
| 02 | Constraints | Технические и организационные ограничения, конвенции |
| 03 | Context and Scope | Business и technical context, внешние интерфейсы |
| 04 | Solution Strategy | Фундаментальные решения и идеи |
| 05 | **Building Block View** | Абстракции кода, black-/whiteboxes (центр тяжести) |
| 06 | Runtime View | Сценарии взаимодействия building blocks |
| 07 | Deployment View | Hardware, инфраструктура, deployment |
| 08 | Crosscutting Concepts | Повторяющиеся подходы и паттерны |
| 09 | Architecture Decisions | Важные/дорогие/рискованные решения (место для ADR) |
| 10 | Quality Requirements | Обзор качества + quality scenarios |
| 11 | Risks and Technical Debt | Известные проблемы, риски, техдолг |
| 12 | Glossary | Определения терминов |

### Маппинг C4 ↔ arc42 (официальный, C4 FAQ)

| arc42 секция | C4 диаграмма |
|---|---|
| Context and Scope (03) | System Context |
| Building Block View level 1 (05) | Container |
| Building Block View level 2 (05) | Component |
| Building Block View level 3 (05) | Code (class) |

### Docs-as-code раскладка (пример)

`docs/architecture/01-introduction-and-goals.md` … `12-glossary.md`; диаграммы как код: `system-context.puml`, `level-1-container.puml` …; секция 09 содержит `adr/adr-0001-*.md`.

### Tooling (diagram-as-code)

- **Structurizr** — C4-based, генерирует диаграммы из кода/DSL
- **PlantUML** — text-based, поддерживает C4
- **Mermaid** — text-based, рендерится GitHub/GitLab

### arc42 Quality Model (quality.arc42.org)

191 quality characteristics, 150 example requirements, 55 solution approaches, 48 standards & regulations.

## Сильные и слабые стороны

C4: независимость от нотации и инструментов; граница применимости заявлена самим методом — использовать только уровни, добавляющие ценность (уровень Code опционален). Явных каталогов слабых сторон и анти-паттернов в первоисточниках нет.

arc42: полнота шаблона — и сила (ничего не забыто), и риск (для маленькой системы 12 секций избыточны; шаблон допускает сокращение, но это решение остаётся на команде).

## Источники

- C4 Model: https://c4model.com (+ FAQ: https://c4model.com/faq)
- arc42: https://arc42.org (+ docs: https://docs.arc42.org; quality: https://quality.arc42.org; GitHub: https://github.com/arc42)
- Structurizr: https://structurizr.com
- Пример arc42+C4: https://github.com/bitsmuggler/arc42-c4-software-architecture-documentation-example
- iSAQB ADOC: https://tecnovy.com
- Входные материалы inbox: `documentation-process/reference/architecture-c4-arc42.md`
