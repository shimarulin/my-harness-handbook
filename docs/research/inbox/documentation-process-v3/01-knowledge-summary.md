# Сводка знаний: подходы, спецификации, фреймворки, инструменты

| Параметр | Значение |
|---|---|
| Дата | 2026-09-28 |
| Статус | Draft |
| Связан с | `00-goals.md` |

---

## 1. Управление решениями (Decision Management)

### 1.1 Architecture Decision Records (ADR)

| Вариант | Формат | Особенности | Источник |
|---|---|---|---|
| **Nygard (классический)** | Markdown, 5 секций | Title/Context/Decision/Status/Consequences; 1–2 страницы; «разговор с будущим разработчиком» | [cognitect.com/blog](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions) |
| **MADR 4.0.0** | Markdown, структурированный | Decision Drivers, Considered Options, Pros/Cons per option; 4 шаблона (full/minimal/bare/bare-minimal) | [adr.github.io/madr](https://adr.github.io/madr), [github.com/adr/madr](https://github.com/adr/madr) |
| **YADR** | YAML | Machine-readable, для CI/дашбордов | [ozimmer.ch/practices/2022/11/22/MADRTemplatePrimer.html](https://ozimmer.ch/practices/2022/11/22/MADRTemplatePrimer.html) |
| **ISO/IEC/IEEE 42010:2022** | Концептуальная модель | Stakeholder Perspectives, Architecture Aspects; ADL: SysML, ArchiMate, ACME, xADL | [iso-architecture.org/42010/cm](http://www.iso-architecture.org/42010/cm/) |
| **Any Decision Records** | Расширение ADR | Не только архитектура: любые значимые решения (процессные, орг.) | [adr.github.io](https://adr.github.io) |

### 1.2 ADR-инструменты

| Инструмент | Тип | Статус | Источник |
|---|---|---|---|
| **adr-tools** (Nat Pryce) | CLI, Nygard-формат | Активный | [github.com/npryce/adr-tools](https://github.com/npryce/adr-tools) |
| **Log4brains** | Docs-as-code knowledge base, static site | ⚠️ выглядит unmaintained (2024) | [github.com/thomvaill/log4brains](https://github.com/thomvaill/log4brains) |
| **docToolchain** | Docs-as-code для arc42 (Gradle) | Активный | [doctoolchain.org](https://doctoolchain.org) |
| **pyadr / adr-log** | CLI + генерация лога | Ограниченная поддержка | [adr.github.io/adr-tooling](https://adr.github.io/adr-tooling) |

**Выводы для процесса:**

- Базовый формат ADR: **MADR** (лучший баланс структуры и лёгкости;
  lint-инструменты, machine-readable через YAML-вариант).
- Нумерация сквозная, monotonic; reversal — через `superseded`.
- Хранение: `docs/adr/NNNN-slug.md` в репозитории проекта.
- Публикация: статический сайт (MkDocs/Antora) из тех же файлов.

---

## 2. Архитектурная документация

### 2.1 Модели и шаблоны

| Подход | Что даёт | Источник |
|---|---|---|
| **C4 Model** | 4 уровня абстракции: System Context → Container → Component → Code; + Landscape/Dynamic/Deployment | [c4model.com](https://c4model.com) |
| **Arc42** | 12 секций шаблона архитектурного документа; Building Block View — центр | [arc42.org](https://arc42.org), [docs.arc42.org](https://docs.arc42.org) |
| **4+1 View Model (Kruchten)** | Logical/Process/Development/Physical + Scenarios | [Wikipedia](https://en.wikipedia.org/wiki/4%2B1_architectural_view_model) |
| **ArchiMate** | Enterprise-моделирование, слои Business/Application/Technology/Strategy | [opengroup.org/archimate-forum](https://www.opengroup.org/archimate-forum/archimate-overview) |
| **TOGAF** | Метод ADM для enterprise architecture | [opengroup.org/togaf](https://www.opengroup.org/togaf) |
| **SysML v1.7/v2.0** | Моделирование complex systems (HW+SW) | [omg.org/sysml](https://www.omg.org/sysml), [sysml.org](https://sysml.org) |

**Совместимость C4+Arc42** (подтверждена официально): Context → Building Block L1
(Container) → L2 (Component) → L3 (Code). Источник: [c4model.com/faq](https://c4model.com/faq).

**Качество**: [quality.arc42.org](https://quality.arc42.org) — 191 характеристика
качества, 150 примеров требований.

**Выводы для процесса:**

- Ядро: **C4** (диаграммы как код) + **arc42** (структура документа) для L3–L4.
- 4+1/ArchiMate/TOGAF — только при enterprise-требованиях (L4+).
- Диаграммы: PlantUML (глубина нотации) / Mermaid (нативный рендер GitHub) /
  D2 (лучшая автолayout). Выбор — per-проект, формат текстовый всегда.

### 2.2 Diagram-as-Code

| Инструмент | Сильная сторона | Источник |
|---|---|---|
| **PlantUML** | Глубина нотации, C4-integration | [plantuml.com](https://plantuml.com) |
| **Mermaid** | Нативный рендер в GitHub/GitLab | [mermaid.js.org](https://mermaid.js.org) |
| **D2** | Лучший default layout | [d2lang.com](https://d2lang.com) |
| **Graphviz** | Общая визуализация графов | [graphviz.org](https://graphviz.org) |
| **Structurizr** | C4 из кода (Java/DSL) | [structurizr.com](https://structurizr.com) |

---

## 3. Requirements и Specification

### 3.1 Нотации требований

| Нотация | Формат | Применение | Источник |
|---|---|---|---|
| **EARS** | While/When/Where/If-Then + shall | System requirements, testability; используется Kiro | [alistairmavin.com/ears](https://alistairmavin.com/ears), [Wikipedia](https://en.wikipedia.org/wiki/Easy_Approach_to_Requirements_Syntax) |
| **Gherkin** | Given-When-Then | Executable scenarios (BDD) | [cucumber.io/docs/gherkin](https://cucumber.io/docs/gherkin) |
| **Job Story** | When[situation] I want[motivation] so[outcome] | Продуктовые требования, альтернатива User Story | [intercom.com (Klement)](https://www.intercom.com/blog/designing-features-using-job-stories/), [mountaingoatsoftware.com](https://www.mountaingoatsoftware.com/blog/job-stories) |
| **User Story** | As a… I want… so that… | Классика agile | [Wikipedia](https://en.wikipedia.org/wiki/User_story) |

**EARS vs Gherkin**: EARS — high-level system requirements (неисполняемые,
структурированные), Gherkin — детальные executable acceptance criteria.
Совместимы: EARS для требований, Gherkin для сценариев.

### 3.2 Дискавери-практики (requirements elicitation)

| Практика | Что даёт | Источник |
|---|---|---|
| **Event Storming** (Brandolini) | Workshop: mapping domain events, bounded contexts | [ddd.academy](https://ddd.academy) |
| **Domain Story Telling** (Hofer) | Pictographic stories от domain experts | [domainstorytelling.org](https://domainstorytelling.org) |
| **Event Modeling** (Dymitruk) | Blueprint: события+команды на timeline; AI-friendly спецификации | [eventmodeling.org](https://eventmodeling.org) |
| **Impact Mapping** (Adzic) | Goal→Actor→Impact→Deliverable, трассировка к бизнес-цели | [impactmapping.org](https://www.impactmapping.org) |
| **User Story Mapping** (Patton) | Визуальная карта user journey, release planning | [jpattonassociates.com](https://jpattonassociates.com) |
| **Example Mapping** | Конкретные примеры к acceptance criteria | [draft.io](https://draft.io) |

### 3.3 Спецификации по примерам

| Подход | Суть | Источник |
|---|---|---|
| **Specification by Example** (Adzic) | Живая документация из реалистичных примеров | [amazon.com (книга)](https://www.amazon.com/Specification-Example-Successful-Deliver-Software/dp/1617290084) |
| **ATDD** | Acceptance tests до имплементации | [oreilly.com (ATDD by Example)](https://www.oreilly.com/library/view/atdd-by-example/9780132532209/) |

---

## 4. BDD и исполняемые спецификации (фреймворки)

| Фреймворк | Язык | Формат спек | Статус/Источник |
|---|---|---|---|
| **Cucumber** | Java/JS/Ruby и др. | Gherkin | [cucumber.io](https://cucumber.io) |
| **Reqnroll** | .NET | Gherkin | [reqnroll.net](https://reqnroll.net) (fork SpecFlow после EOL 2024-12-31) |
| **Behave** | Python | Gherkin | [behave.readthedocs.io](https://behave.readthedocs.io) |
| **Behat** | PHP | Gherkin | [behat.org](https://behat.org) |
| **JBehave** | Java | Gherkin-подобный | [jbehave.org](https://jbehave.org) |
| **Gauge** | Multi | **Markdown** (не Gherkin) | [gauge.org](https://gauge.org), [docs.gauge.org](https://docs.gauge.org) |
| **Karate** | DSL (Java-based) | Gherkin-подобный DSL | [karatelabs.io](https://karatelabs.io), [github.com/karatelabs/karate](https://github.com/karatelabs/karate) |
| **Concordion** | Java/.NET | **HTML** с аннотациями | [concordion.org](https://concordion.org) |
| **JGiven** | Java | Plain Java fluent API → отчёты | [jgiven.org](https://jgiven.org) |
| **FitNesse** | Java/_multi | Wiki-таблицы | [fitnesse.org](https://fitnesse.org) |
| **Spock** | Groovy/Java | Groovy DSL | [spockframework.org](https://spockframework.org) |

**Анти-паттерны Cucumber** (важно для процесса): feature-coupled step
definitions, conjunction steps; «Don't use Cucumber-like tools without
following BDD». Источник: [cucumber.io/docs/guides/anti-patterns](https://cucumber.io/docs/guides/anti-patterns).

**Выводы:** Gherkin-формат — межинструментный стандарт (переносимость между
Cucumber/Reqnroll/Behave). Gauge интересен Markdown-спеками (AI-friendly).

---

## 5. Product/Process-артефакты верхнего уровня

| Артефакт | Вопрос | Источник |
|---|---|---|
| **PRD** | What & why (продукт) | [Atlassian](https://www.atlassian.com/agile/product-management/requirements), [шаблон](https://www.atlassian.com/software/confluence/templates/product-requirements) |
| **RFC / Design Doc** | How? Proposal + debate | Attentive process: [tech.attentive.com](https://tech.attentive.com/articles/rfc-process-for-teams); Google Design Docs: [industrialempathy.com](https://www.industrialempathy.com/posts/design-docs-at-google); коллекция шаблонов: [pragmaticengineer.com](https://blog.pragmaticengineer.com/rfcs-and-design-docs) |
| **Amazon PR/FAQ** | Working backwards: PR+FAQ до кода, 6-pager | [workingbackwards.com](https://workingbackwards.com), [инструкция](https://workingbackwards.com/resources/working-backwards-pr-faq) |
| **ADR** | Что решили, навсегда | см. раздел 1 |

**Pipeline PRD → RFC → ADR** (what&why → how+debate → decided forever).
Источник: [aridanemartin.dev](https://aridanemartin.dev/blog/prd-adr-rfc-decision-documents).

**Google Design Doc структура**: Context/Scope, Goals/Non-goals, Design
(trade-offs!), System-context diagram, APIs, Data storage, Alternatives,
Cross-cutting concerns. Источник: [industrialempathy.com](https://www.industrialempathy.com/posts/design-docs-at-google).

**Паттерны RFC-процесса** (Attentive): time-boxed review (1 неделя),
авторы владеют outcome, Staff+ — стюарды, lifecycle статусов
(Draft→In Review→Approved/Rejected). Источник: [tech.attentive.com](https://tech.attentive.com/articles/rfc-process-for-teams).

---

## 6. Spec-Driven Development (SDD) — AI-эра

| Инструмент | Подход | Agent-agnostic | Источник |
|---|---|---|---|
| **GitHub Spec Kit** | `/speckit.*` slash-команды: constitution→specify→plan→tasks→implement; 38 интеграций | Да (generic escape hatch) | [github.com/github/spec-kit](https://github.com/github/spec-kit) |
| **Kiro (AWS)** | IDE/CLI; requirements.md (EARS) → design.md → tasks.md | Ограничен экосистемой Kiro | [kiro.dev](https://kiro.dev/docs/specs/feature-specs) |
| **BMAD-METHOD** | 12+ специализированных AI-агентов (product/arch/UX/dev/test) | Да (skills) | [github.com/bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) |
| **OpenSpec (Fission-AI)** | Lightweight, `/opsx:*`, без жёстких phase gates | Да (30+ ассистентов) | [openspec.dev](https://openspec.dev), [github.com/Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec) |
| **ForgeSDLC** | Event-driven workflow, Jira→PR, human-gated | Да (model factory) | [forgesdlc.com](https://forgesdlc.com), [github.com/Forge-sdlc/forge](https://github.com/Forge-sdlc/forge) |

**Ключевые SDD-артефакты**: `spec.md` (что строим), `plan.md` (как),
`tasks.md` (разбиение). Конституция — постоянные принципы проекта.

**Когда SDD**: работа переживает один context window; много сессий агентов;
параллельная работа; greenfield; correctness > speed.
Источник: [utsabpant.com](https://utsabpant.com/blog/spec-driven-development-without-the-hype).

---

## 7. API и Data-контракты

| Спецификация | Область | Источник |
|---|---|---|
| **OpenAPI 3.x** | HTTP API (REST) | [openapis.org](https://www.openapis.org), [spec.openapis.org/oas](https://spec.openapis.org/oas) |
| **AsyncAPI 3.1** | Event-driven (Kafka, MQTT, AMQP…) | [asyncapi.com](https://www.asyncapi.com), [github.com/asyncapi/spec](https://github.com/asyncapi/spec) |
| **JSON Schema** | Валидация JSON-данных | [json-schema.org](https://json-schema.org) |
| **Avro** | Схемы + эволюция | [avro.apache.org](https://avro.apache.org) |
| **Protobuf** | Сериализация, gRPC | [developers.google.com/protocol-buffers](https://developers.google.com/protocol-buffers) |

---

## 8. Docs-as-Code платформы

| Инструмент | Формат | Источник |
|---|---|---|
| **MkDocs** (+Material) | Markdown | [mkdocs.org](https://www.mkdocs.org) |
| **Docusaurus** | Markdown/MDX, React | [docusaurus.io](https://docusaurus.io) |
| **Sphinx** | reST/MyST | [sphinx-doc.org](https://www.sphinx-doc.org) |
| **Antora** | AsciiDoc, multi-repo, версии | [antora.org](https://antora.org) |
| **Read the Docs** | Хостинг+CI | [readthedocs.org](https://readthedocs.org) |

---

## 9. Воспроизводимость (Research/Repro)

| Ресурс | Что даёт | Источник |
|---|---|---|
| **Research Compendium** | data+code+text вместе, окружение зафиксировано | [Turing Way](https://book.the-turing-way.org/reproducible-research/compendia) |
| **rrrpkg / rrtools** | Шаблоны compendium для R | [github.com/ropensci/rrrpkg](https://github.com/ropensci/rrrpkg), [github.com/benmarwick/rrtools](https://github.com/benmarwick/rrtools) |
| **Quarto** | Multi-language publishing (Python/R/Julia) | [quarto.org](https://quarto.org) |
| **Jupyter Book / MyST** | Книги из notebooks | [jupyterbook.org](https://jupyterbook.org) |
| **Docker/Singularity** | Воспроизводимые окружения | [docker.com](https://www.docker.com), [sylabs.io](https://sylabs.io) |

---

## 10. Синтез: карта «проблема → инструмент/практика»

| Вопрос процесса | Основной вариант | Альтернативы |
|---|---|---|
| Зафиксировать продуктовое «что и почему» | PRD (Markdown) | Amazon PR/FAQ, Job Stories |
| Обсудить «как» до кода | RFC/Design Doc (Markdown) | Google Design Doc структура |
| Спецификация поведения | EARS (требования) + Gherkin (сценарии) | Gauge Markdown-спеки |
| Согласовать архитектуру | ADR (MADR) | YADR (YAML) для CI |
| Описать архитектуру системы | C4 (PlantUML/Mermaid) + arc42 | 4+1, ArchiMate (L4) |
| Распланировать задачи | tasks.md (Spec Kit-стиль) | BMAD plan, OpenSpec tasks |
| Контракты API | OpenAPI / AsyncAPI | JSON Schema |
| Исполняемая документация | Cucumber/Reqnroll (Gherkin) | Gauge, Karate (API) |
| Публикация доков | MkDocs/Antora | Docusaurus, Sphinx |
| Правила для AI-агентов | `AGENTS.md`/`specify init` | BMAD skills, `.kiro/` |
| Исследовательские артефакты | Research Compendium + Quarto | Jupyter Book |

## 11. Пробелы (что нужно проработать)

1. **Единая раскладка репозитория**, совместимая со всеми инструментами.
2. **Протокол Human↔AI approval-гейтов** (кто и когда утверждает артефакт).
3. **CI-пайплайн для документации**: lint (markdownlint, MADR-check),
   рендер диаграмм, проверка ссылок, сборка сайта.
4. **Правила продвижения артефактов между уровнями масштаба** (L1→L2→L3).
5. **Идентификация и трассировка**: сквозные ID (idea-001 → prd-001 →
   rfc-001 → adr-0001 → spec-001).
