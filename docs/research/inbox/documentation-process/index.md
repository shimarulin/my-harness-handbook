# Справочная база знаний

Коллекция руководств, методологий и фреймворков для Spec-Driven Development и Documentation-Driven Engineering.

## Основные документы

### Разработка через документацию

- [SDD Landscape](reference/sdd-landscape.md) — Инструменты: GitHub Spec Kit, Kiro, BMAD-METHOD, OpenSpec, ForgeSDLC
- [PRD (Product Requirements Document)](reference/prd.md) — Определение, шаблоны, связь с RFC/ADR
- [RFC vs SDD](reference/rfc-vs-sdd.md) — Сравнение подходов, Attentive RFC Process
- [EARS Notation](reference/ears-notation.md) — Easy Approach to Requirements Syntax, 5 паттернов

### Архитектурная документация

- [ADR Standards](reference/adr-standards.md) — MADR 4.0.0, Nygard format, YADR, ISO 42010
- [C4 + Arc42](reference/architecture-c4-arc42.md) — Визуализация архитектуры, 12 секций arc42

### Исполняемые спецификации

- [BDD Alternatives](reference/bdd-alternatives.md) — Cucumber, SpecFlow→Reqnroll, Behave, Behat, JBehave, анти-паттерны

### Research

- [Research Compendium](reference/research-compendium.md) — rOpenSci, rrtools, o2r ERC, Turing Way

### Предыдущие справочники

- [Documentation Frameworks](documentation.md) — Diátaxis, DITA, Docs-as-Code, style guides
- [Note-Taking](note-taking.md) — Zettelkasten, PARA, Bullet Journal
- [Software Architecture](software-architecture.md) — C4, Arc42, DDD, Event Storming

## Как пользоваться

Каждый документ содержит:
1. **Определение и историю**
2. **Структуру и шаблоны**
3. **Сравнение с альтернативами**
4. **Практические рекомендации**
5. **Ссылки на источники**

## Матрица выбора

| Сценарий | Рекомендация |
|---|---|
| **Простая фича** | Lightweight spec (страница) |
| **Сложная фича + AI-агенты** | Spec Kit / OpenSpec + EARS |
| **Архитектурное решение** | RFC → ADR |
| **Product alignment** | PRD |
| **Executable specifications** | BDD (Cucumber/Reqnroll) |
| **Architecture documentation** | C4 + Arc42 + ADR |
| **Research + notes** | Research Compendium + Zettelkasten |
