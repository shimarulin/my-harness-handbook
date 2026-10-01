# Архитектурная документация: C4 Model + Arc42

## C4 Model

**Официальный сайт:** https://c4model.com【turn6fetch0】

### Определение

**C4 Model** — «easy to learn, developer friendly approach to software architecture diagramming»【turn6fetch0】.

### Уровни абстракции【turn6fetch0】

1. **Software system** — highest level
2. **Container** — applications, data stores, микросервисы
3. **Component** — внутренние компоненты контейнера
4. **Code** — классы/интерфейсы (опционально)

### Диаграммы【turn6fetch0】

**Core:**
1. **System Context diagram** — система в контексте пользователей и других систем
2. **Container diagram** — контейнеры внутри системы
3. **Component diagram** — компоненты внутри контейнера
4. **Code diagram** — классы (опционально)

**Supporting:**
- **System Landscape diagram**
- **Dynamic diagram**
- **Deployment diagram**

### Ключевые принципы【turn6fetch0】

- **Notation independent**
- **Tooling independent**
- «You don't need to use all 4 levels of diagram; only those that add value»

---

## Arc42

**Официальный сайт:** https://arc42.org【turn4fetch0】
**Docs:** https://docs.arc42.org【turn4fetch0】

### Определение

**Arc42** — template для документирования и коммуникации архитектуры ПО. 12 секций, которые описывают архитектуру, с **Building Block View как центром тяжести**【turn2search7】.

### 12 Секций【turn4fetch0】

| # | Section | Content |
|---|---|---|
| 01 | **Introduction and Goals** | Requirements, stakeholder, (top) quality goals |
| 02 | **Constraints** | Technical and organizational constraints, conventions |
| 03 | **Context and Scope** | Business and technical context, external interfaces |
| 04 | **Solution Strategy** | Fundamental solution decisions and ideas |
| 05 | **Building Block View** | Abstractions of source code, black-/whiteboxes |
| 06 | **Runtime View** | Runtime scenarios: how do building blocks interact |
| 07 | **Deployment View** | Hardware and technical infrastructure, deployment |
| 08 | **Crosscutting Concepts** | Recurring solution approaches and patterns |
| 09 | **Architecture Decisions** | Important, expensive, risky or contentious decisions |
| 10 | **Quality Requirements** | Quality requirements overview and detailed quality scenarios |
| 11 | **Risks and Technical Debt** | Known problems, risks and technical debt |
| 12 | **Glossary** | Definitions of important business and technical terms |

---

## Совместимость C4 + Arc42

**Да, многие команды комбинируют**, и C4 model совместим с arc42 documentation template следующим образом【turn11fetch0】:

| Arc42 Section | C4 Diagram |
|---|---|
| **Context and Scope** | System Context diagram |
| **Building Block View (level 1)** | Container diagram |
| **Building Block View (level 2)** | Component diagram |
| **Building Block View (level 3)** | Code (e.g. class) diagram |

---

## Пример структуры с Documentation as Code

```
docs/
├── architecture/
│   ├── README.md
│   ├── 01-introduction-and-goals.md
│   ├── 02-architecture-constraints.md
│   ├── 03-context-and-scope.md
│   │   ├── context.md
│   │   └── system-context.puml
│   ├── 04-solution-strategy.md
│   ├── 05-building-block-view.md
│   │   ├── level-1-container.puml
│   │   ├── level-2-component.puml
│   │   └── level-3-code.puml
│   ├── 06-runtime-view.md
│   ├── 07-deployment-view.md
│   ├── 08-crosscutting-concepts.md
│   ├── 09-architecture-decisions.md
│   │   └── adr/
│   │       ├── adr-0001-choose-database.md
│   │       └── adr-0002-api-style.md
│   ├── 10-quality-requirements.md
│   ├── 11-risks-and-technical-debt.md
│   └── 12-glossary.md
└── ...
```

---

## Tools

### Diagram as Code【turn5search4】

- **Structurizr** — C4 model based solution, генерирует диаграммы из кода
- **PlantUML** — text-based диаграммы, поддерживает C4
- **Mermaid** — text-based, поддерживается GitHub/GitLab

### Arc42 Templates【turn0search8】

- Markdown, AsciiDoc, и другие форматы
- https://github.com/arc42

---

## Качество (arc42 quality model)

**Quality.arc42.org**【turn3search5】:
- 191 quality characteristics entries
- 150 example requirements
- 55 solution approaches
- 48 standards & regulations

---

## Источники

- C4 Model: https://c4model.com【turn6fetch0】
- C4 FAQ (Arc42 compatibility): https://c4model.com/faq【turn11fetch0】
- Arc42: https://arc42.org【turn4fetch0】
- Arc42 Docs: https://docs.arc42.org【turn4fetch0】
- Arc42 Quality: https://quality.arc42.org【turn3search5】
- Arc42 GitHub: https://github.com/arc42【turn0search8】
- Structurizr: https://structurizr.com【turn5search4】
- Arc42 + C4 Example: https://github.com/bitsmuggler/arc42-c4-software-architecture-documentation-example【turn0search12】
- iSAQB ADOC: https://tecnovy.com【turn0search13】
