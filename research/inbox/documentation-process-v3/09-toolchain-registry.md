# Реестр инструментов: процессы v3

| Параметр | Значение |
|---|---|
| Дата | 2026-09-29 |
| Статус | Draft |
| Связан с | `04-tool-selection-and-migration.md`, `06-repository-structure.md`, `07-cicd-docs-pipeline.md` |

---

## 1. Принципы реестра

| # | Принцип | Следствие |
|---|---|---|
| T1 | Формат важнее инструмента | Артефакты в открытых форматах, инструменты заменяемы |
| T2 | Primary + Alternatives | Для каждой категории минимум 2 варианта |
| T3 | Exit strategy обязательна | Заранее определено, как сменить инструмент |
| T4 | Мониторинг здоровья | Quarterly review состояния инструментов |
| T5 | Никакой критической зависимости | Любой инструмент можно выкинуть за ≤ 1 sprint |

---

## 2. Критерии выбора инструментов

### 2.1 Обязательные критерии

| Критерий | Weight | Порог | Как проверить |
|---|---|---|---|
| **Открытая лицензия** | Critical | MIT/Apache-2.0/GPL | LICENSE file в репо |
| **Открытый формат данных** | Critical | Markdown/YAML/JSON/text | Документация tool |
| **Экспорт данных** | Critical | Возможность export 100% | Test: экспортировать существующие данные |
| **Активная разработка** | High | Коммит за последние 30 дней | GitHub API: `GET /repos/{owner}/{repo}/commits?per_page=1` |
| **Сообщество** | High | >100 contributors ИЛИ >1000 stars | GitHub API: contributors_count, stargazers_count |
| **Документация** | High | Полная docs + examples | Ревью docs сайта |
| **Экосистема** | Medium | Plugins/extensions существуют | Поиск в реестрах (npm, PyPI) |
| **Порог входа** | Medium | Новичок продуктивен за <1 день | Pilot с новым участником |

### 2.2 Дополнительные критерии (per-категория)

| Категория | Дополнительные критерии |
|---|---|
| **SDD-инструменты** | Agent-agnostic, Brownfield support, Delta specs |
| **BDD фреймворки** | Language runners, CI integration, Report quality |
| **Docs генераторы** | Themes, Plugins, Search, Versioning, i18n |
| **Diagram tools** | Rendering quality, GitHub integration, C4 support |
| **Message brokers** | Replay, Scale, Persistence, Latency |
| **CI/CD** | Kubernetes native, GitOps support, Matrix builds |

### 2.3 Скоринг

```
Score = Σ(criterion_weight × criterion_score) / Σ(criterion_weight)

criterion_score: 0 (не проходит порог) | 1 (минимально) | 2 (хорошо) | 3 (отлично)

Порог принятия: Score ≥ 2.0
```

---

## 3. Реестр по категориям

### 3.1 SDD (Spec-Driven Development) инструменты

| Инструмент | Primary/Alt | Score | Vendor Lock | Миграция | Источник |
|---|---|---|---|---|---|
| **GitHub Spec Kit** | Primary (greenfield) | 2.6 | Low | Markdown→Markdown, 1 день | [github.com/github/spec-kit](https://github.com/github/spec-kit)【turn0search5】 |
| **OpenSpec** | Primary (brownfield) | 2.5 | Low | Markdown→Markdown, 1 день | [github.com/Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec)【turn0search5】 |
| **BMAD-METHOD** | Alternative | 2.3 | Medium | Skills→Skills, 2-3 дня | [github.com/bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) |
| **Kiro (AWS)** | NOT RECOMMENDED | 1.8 | High | Ecosystem-locked | [kiro.dev](https://kiro.dev) |

**Health метрики (проверять quarterly):**

| Метрика | Spec Kit | OpenSpec | BMAD |
|---|---|---|---|
| GitHub stars | 139k+ | ~68k | ~53.5k |
| Contributors | 270+ | TBD | TBD |
| Last commit (days ago) | <7 | <7 | <30 |
| Extensions/presets | 157+ | N/A | N/A |
| Integrations | 38 | 30+ | Via skills |

**Exit Strategy (Spec Kit → OpenSpec):**

```bash
# Миграция занимает ~1 день
1. npm install -g @fission-ai/openspec
2. openspec init
3. Мигрировать specs/<feature>/ → openspec/changes/<name>/
   - spec.md → specs/<capability>/spec.md (объединить если fragmentированы)
   - tasks.md → tasks.md
   - Извлечь design-секции → design.md
4. cp .specify/memory/constitution.md CONSTITUTION.md
5. Удалить .specify/
6. Обновить AGENTS.md
7. Прогнать openspec validate
```

**Exit Strategy (OpenSpec → Spec Kit):**

```bash
# Миграция занимает ~1 день
1. uv tool install specify-cli
2. specify init --agent <agent>
3. Мигрировать openspec/changes/<id>/ → specs/<feature>/
   - proposal.md → intro section of spec.md
   - specs/*.md → specs/<feature>/spec.md
   - design.md → design section of spec.md
   - tasks.md → tasks.md
4. cp CONSTITUTION.md .specify/memory/constitution.md
5. Удалить openspec/
6. Запустить /speckit.constitution для валидации
```

**Что не мигрирует автоматически:**

| Элемент | Решение |
|---|---|
| Slash commands | Переписать AGENTS.md |
| Phase gates | Определить, нужны ли формальные гейты |
| Extensions/presets | Переписать под целевой инструмент |
| Delta specs | Spec Kit: «выпрямить» в полный spec |
| CI integrations | Адаптировать pipeline |

---

### 3.2 BDD / Executable Specifications

| Инструмент | Primary/Alt | Языки | Score | Vendor Lock | Источник |
|---|---|---|---|---|---|
| **Gauge** | Primary | Java, JS/TS, Python, .NET, Ruby | 2.7 | Low (Markdown specs) | [gauge.org](https://gauge.org)【turn0search5】 |
| **Cucumber** | Alternative (JVM) | Java, JS, Ruby | 2.5 | Medium (Gherkin format) | [cucumber.io](https://cucumber.io) |
| **Reqnroll** | Alternative (.NET) | C# | 2.4 | Medium (Gherkin format) | [reqnroll.net](https://reqnroll.net) |
| **Behave** | Alternative (Python) | Python | 2.3 | Medium (Gherkin format) | [behave.readthedocs.io](https://behave.readthedocs.io) |
| **Karate** | Alternative (API) | DSL (Java-based) | 2.4 | Medium (Karate DSL) | [karatelabs.io](https://karatelabs.io) |
| **JBehave** | Legacy | Java | 1.9 | Medium | [jbehave.org](https://jbehave.org) |

**Критерии выбора per-стек:**

| Ситуация | Рекомендация | Почему |
|---|---|---|
| Multi-language команда | Gauge | Один инструмент, разные language runners |
| Java/JVM-first | Cucumber | Зрелая экосистема, step libraries |
| .NET-first | Reqnroll | SpecFlow EOL (2024-12-31), Reqnroll — fork |
| Python-first | Behave ИЛИ Gauge | Зависит от приоритетов |
| API testing | Karate | Self-contained DSL, нет step definitions |
| Mixed stack | Gauge (primary) + Karate (API) | Покрытие всех сценариев |

**Exit Strategy (Gauge → Cucumber):**

```bash
# Миграция: Markdown specs → Gherkin
1. Экспортировать Gauge specs (Markdown) 
2. Конвертировать Markdown → Gherkin:
   - Заголовки (#) → Feature:
   - Секции (##) → Scenario:
   - Steps (*) → Given/When/Then
3. Переписать step implementations
4. Обновить CI pipeline

# Timeline: 2-3 дня на 100+ specs
```

**Формат спек — переносимость:**

| Формат | Gauge | Cucumber | Behave | Karate |
|---|---|---|---|---|
| Markdown | ✅ Native | ⚠️ Через плагины | ⚠️ Нет | ❌ |
| Gherkin | ⚠️ Через конвертацию | ✅ Native | ✅ Native | ⚠️ Похоже на Gherkin |
| YAML | ❌ | ❌ | ❌ | ❌ |

---

### 3.3 Architecture / Decision Documentation

| Инструмент | Primary/Alt | Формат | Score | Источник |
|---|---|---|---|---|
| **MADR** | Primary (ADR) | Markdown | 2.8 | [adr.github.io/madr](https://adr.github.io/madr) |
| **adr-tools** | Primary (CLI) | Markdown (Nygard) | 2.5 | [github.com/npryce/adr-tools](https://github.com/npryce/adr-tools) |
| **Log4brains** | Alternative | Markdown → static site | 2.2 | [github.com/thomvaill/log4brains](https://github.com/thomvaill/log4brains) |
| **YADR** | Alternative | YAML | 2.0 | [ozimmer.ch](https://ozimmer.ch/practices/2022/11/22/MADRTemplatePrimer.html) |
| **Structurizr** | Alternative (C4) | DSL/Java | 2.3 | [structurizr.com](https://structurizr.com) |

**Health Check Log4brains:** ⚠️ Выглядит unmaintained — автор недоступен >18 месяцев (по состоянию на 2024)【turn0search1】. Не рекомендуется для новых проектов.

**Exit Strategy (MADR → Nygard):**

```bash
# Обратная совместимость высокая
1. Конвертировать MADR → Nygard:
   - Убрать YAML front-matter (опционально)
   - Context and Problem Statement → Context
   - Decision Drivers → удалить (нет в Nygard)
   - Considered Options → Alternatives
   - Decision Outcome → Decision
   - Pros and Cons of the Options → Consequences
2. Переименовать файлы: NNNN-slug.md (unchanged)

# Timeline: ~2 часа на 50+ ADRs
```

---

### 3.4 Documentation Site Generators

| Инструмент | Primary/Alt | Формат | Score | Vendor Lock | Источник |
|---|---|---|---|---|---|
| **MkDocs Material** | Primary | Markdown | 2.8 | Low | [squidfunk.github.io/mkdocs-material](https://squidfunk.github.io/mkdocs-material) |
| **Docusaurus** | Alternative | Markdown/MDX | 2.6 | Low | [docusaurus.io](https://docusaurus.io) |
| **Sphinx** | Alternative (Python) | reST/MyST | 2.5 | Low | [sphinx-doc.org](https://www.sphinx-doc.org) |
| **Antora** | Alternative (AsciiDoc) | AsciiDoc | 2.3 | Medium (AsciiDoc) | [antora.org](https://antora.org) |
| **VitePress** | Alternative | Markdown | 2.2 | Low | [vitepress.dev](https://vitepress.dev) |

**Критерии выбора:**

| Ситуация | Рекомендация | Почему |
|---|---|---|
| Python проект | MkDocs Material | Простота, Material theme лучший |
| React/Node проект | Docusaurus | React components в MDX |
| Multi-repo документация | Antora | Component-based, versioning |
| Python + API docs | Sphinx | Autodoc из docstrings |
| Vue проект | VitePress | Vue-powered |

**Exit Strategy (MkDocs → Docusaurus):**

```bash
# Markdown совместим, миграция лёгкая
1. Конвертировать mkdocs.yml → docusaurus.config.js:
   - nav → navbar + sidebar
   - theme → themeConfig
2. Переместить docs/ → content/docs/
3. Конвертировать Material-specific admonitions:
   - !!! note → :::note
   - ??? tip → :::tip (collapsible → details)
4. Обновить GitHub Actions workflow
5. Перенастроить деплой

# Timeline: 1-2 дня для среднего проекта
```

---

### 3.5 Diagram-as-Code

| Инструмент | Primary/Alt | Score | GitHub Native | C4 Support | Источник |
|---|---|---|---|---|---|
| **Mermaid** | Primary | 2.7 | ✅ Yes | ⚠️ Limited | [mermaid.js.org](https://mermaid.js.org) |
| **PlantUML** | Primary (complex) | 2.6 | ❌ No (need renderer) | ✅ Yes (C4-PlantUML) | [plantuml.com](https://plantuml.com) |
| **D2** | Alternative | 2.4 | ❌ No | ⚠️ Limited | [d2lang.com](https://d2lang.com) |
| **Graphviz** | Alternative | 2.2 | ❌ No | ❌ No | [graphviz.org](https://graphviz.org) |

**Критерии выбора:**

| Критерий | Mermaid | PlantUML | D2 |
|---|---|---|---|
| **GitHub рендеринг** | ✅ Native | ❌ CI-only | ❌ CI-only |
| **Нотационная глубина** | ⚠️ Basic | ✅ Full UML/C4 | ⚠️ Good |
| **Autolayout качество** | ⚠️ Basic | ⚠️ Better | ✅ Best |
| **Простота изучения** | ✅ Easy | ⚠️ Medium | ✅ Easy |
| **Экосистема** | ✅ Wide | ✅ Mature | ⚠️ Growing |

**Правило выбора:** Mermaid для простых диаграмм (README, quick docs), PlantUML для архитектурных (C4 model, sequence diagrams)【turn0search10】【turn0search12】.

**Exit Strategy (Mermaid → PlantUML):**

```bash
# Синтаксис разный, нужна конвертация
1. Установить mermaid-to-plantuml конвертер (community tool)
2. Конвертировать .mmd → .puml
3. Настроить CI rendering (plantuml -tsvg)
4. Обновить MkDocs конфигурацию

# Timeline: 1 день на 20+ диаграмм
```

---

### 3.6 Requirements / Specification Notation

| Инструмент | Primary/Alt | Формат | Score | Исполнение | Источник |
|---|---|---|---|---|---|
| **EARS** | Primary | Text (WHEN/SHALL) | 2.7 | ❌ Неисполняемая | [alistairmavin.com/ears](https://alistairmavin.com/ears) |
| **Gherkin** | Primary (BDD) | Given-When-Then | 2.6 | ✅ Исполняемая | [cucumber.io/docs/gherkin](https://cucumber.io/docs/gherkin) |
| **Job Story** | Alternative | When-I want-So | 2.3 | ❌ Неисполняемая | [intercom.com](https://www.intercom.com) |
| **User Story** | Alternative | As a-I want-So | 2.2 | ❌ Неисполняемая | [Wikipedia](https://en.wikipedia.org/wiki/User_story) |

**Совместимость:** EARS для high-level требований, Gherkin для executable acceptance criteria. Использовать вместе【turn0search3】.

---

### 3.7 CI/CD

| Инструмент | Primary/Alt | Score | Vendor Lock | Kubernetes | Источник |
|---|---|---|---|---|---|
| **GitHub Actions** | Primary | 2.7 | Medium (GitHub) | Via runners | [github.com/features/actions](https://github.com/features/actions) |
| **GitLab CI** | Alternative | 2.6 | Medium (GitLab) | Via runners | [docs.gitlab.com/ee/ci](https://docs.gitlab.com/ee/ci/) |
| **ArgoCD** | Primary (GitOps CD) | 2.8 | Low (CNCF) | ✅ Native | [argoproj.github.io/cd](https://argoproj.github.io/cd/) |
| **Flux** | Alternative (GitOps CD) | 2.6 | Low (CNCF) | ✅ Native | [fluxcd.io](https://fluxcd.io) |
| **Jenkins** | Legacy | 1.9 | Low | Via plugins | [jenkins.io](https://www.jenkins.io) |

**Exit Strategy (GitHub Actions → GitLab CI):**

```bash
# CI definitions нужно переписать
1. Конвертировать .github/workflows/*.yml → .gitlab-ci.yml:
   - jobs → stages/jobs
   - uses → include:component
   - runs-on → tags
   - needs → dependencies
2. Перенести secrets в GitLab CI variables
3. Перенастроить deployment

# Timeline: 3-5 дней для сложного pipeline
```

---

### 3.8 Message Brokers / Event Streaming

| Инструмент | Primary/Alt | Score | Replay | Scale | Persistence | Источник |
|---|---|---|---|---|---|---|
| **Apache Kafka** | Primary | 2.8 | ✅ Offset-based | ✅ Partitions | ✅ Configurable | [kafka.apache.org](https://kafka.apache.org) |
| **RabbitMQ** | Alternative | 2.5 | ❌ No replay | ⚠️ Manual | ⚠️ Optional | [rabbitmq.com](https://www.rabbitmq.com) |
| **Redis Streams** | Alternative (light) | 2.2 | ⚠️ Limited | ⚠️ Memory-bound | ⚠️ Config | [redis.io](https://redis.io) |
| **AWS SQS/SNS** | Alternative (AWS) | 2.3 | ❌ No replay | ✅ Infinite | ✅ Managed | [aws.amazon.com/sqs](https://aws.amazon.com/sqs/) |

**Критерии выбора (из примера L3):**

| Требование | Kafka | RabbitMQ | Redis Streams | SQS |
|---|---|---|---|---|
| Replay capability | ✅ | ❌ | ⚠️ | ❌ |
| 10M+ msgs/day | ✅ | ✅ | ⚠️ | ✅ |
| Cloud-agnostic | ✅ | ✅ | ✅ | ❌ |
| Schema registry | ✅ | ❌ | ❌ | ❌ |
| Consumer scaling | ✅ Groups | ⚠️ Manual | ⚠️ Limited | ✅ Auto |
| Operational overhead | High | Medium | Low | Zero |

**Exit Strategy (Kafka → RabbitMQ):**

```bash
# Сложная миграция: разная модель
1. Реализовать dual-write (Kafka + RabbitMQ)
2. Мигрировать consumers
3. Переключить producers на RabbitMQ only
4. Удалить Kafka infra

# Timeline: 2-4 недели
# Risks: потеря replay capability, изменение семантики delivery
```

---

### 3.9 API Specification

| Инструмент | Primary/Alt | Формат | Score | Источник |
|---|---|---|---|---|
| **OpenAPI 3.x** | Primary (REST) | YAML/JSON | 2.8 | [openapis.org](https://www.openapis.org) |
| **AsyncAPI 3.x** | Primary (Event) | YAML/JSON | 2.6 | [asyncapi.com](https://www.asyncapi.com) |
| **JSON Schema** | Primary (validation) | JSON | 2.7 | [json-schema.org](https://json-schema.org) |
| **Avro** | Alternative (Kafka) | JSON→binary | 2.5 | [avro.apache.org](https://avro.apache.org) |
| **Protobuf** | Alternative (gRPC) | .proto | 2.5 | [developers.google.com/protocol-buffers](https://developers.google.com/protocol-buffers) |

**Все форматы открытые, vendor lock-in отсутствует.** Миграция между форматами возможна через конвертеры.

---

### 3.10 Research / Reproducibility

| Инструмент | Primary/Alt | Языки | Score | Источник |
|---|---|---|---|---|
| **Quarto** | Primary | R, Python, Julia, Observable | 2.8 | [quarto.org](https://quarto.org) |
| **Jupyter Book** | Alternative | Python | 2.5 | [jupyterbook.org](https://jupyterbook.org) |
| **R Markdown** | Legacy (R) | R | 2.3 | [rmarkdown.rstudio.com](https://rmarkdown.rstudio.com) |
| **Docker** | Primary (env) | Language-agnostic | 2.8 | [docker.com](https://www.docker.com) |
| **Singularity** | Alternative (HPC) | Language-agnostic | 2.4 | [sylabs.io](https://sylabs.io) |

**Exit Strategy (Quarto → Jupyter Book):**

```bash
# Оба основаны на Jupyter/MyST, миграция лёгкая
1. Конвертировать .qmd → .ipynb (quarto convert)
2. Переместить в структуру Jupyter Book
3. Обновить _config.yml

# Timeline: 1-2 дня для книги/сайта
```

---

## 4. Метрики мониторинга инструментов

### 4.1 Quarterly Health Check

```yaml
# .github/workflows/tool-health.yml
name: Tool Health Check

on:
  schedule:
    - cron: '0 6 1 */3 *'  # Quarterly (Jan, Apr, Jul, Oct) 1st day

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check GitHub project health
        run: |
          PROJECTS=(
            "github/spec-kit"
            "Fission-AI/OpenSpec"
            "getgauge/gauge"
            "cucumber/cucumber-js"
            "adr/madr"
            "squidfunk/mkdocs-material"
            "mermaid-js/mermaid"
            "plantuml/plantuml"
            "quarto-dev/quarto-cli"
          )

          for repo in "${PROJECTS[@]}"; do
            echo "Checking: $repo"

            # Last commit date
            LAST_COMMIT=$(curl -s "https://api.github.com/repos/$repo/commits?per_page=1" | jq -r '.[0].commit.committer.date')

            # Days since last commit
            DAYS_SINCE=$(($(date +%s) - $(date -d "$LAST_COMMIT" +%s)) / 86400)

            # Stars
            STARS=$(curl -s "https://api.github.com/repos/$repo" | jq -r '.stargazers_count')

            # Contributors
            CONTRIBUTORS=$(curl -s "https://api.github.com/repos/$repo/contributors?per_page=1" -I | grep -oP 'link:.*page=(\d+)' | grep -oP '\d+' | tail -1)

            # Health status
            if [ $DAYS_SINCE -gt 30 ]; then
              echo "⚠️  $repo: Last commit $DAYS_SINCE days ago"
              echo "   Last commit: $LAST_COMMIT"
              echo "   Stars: $STARS"
              echo "   Contributors: ~${CONTRIBUTORS:-1}"
              echo "   → Consider alternative"
            else
              echo "✅ $repo: Active ($DAYS_SINCE days since last commit)"
            fi
          done
```

### 4.2 Пороги для alarm

| Метрика | Green | Yellow | Red | Action |
|---|---|---|---|---|
| **Days since last commit** | <7 | 7-30 | >30 | Начать eval альтернативы |
| **Stars** (trend) | Growing | Stable | Declining | Investigate |
| **Contributors** (active) | >10 | 3-10 | <3 | Single-maintainer risk |
| **Open issues ratio** | <50 | 50-100 | >100 | Maintainability concerns |
| **Breaking changes** (last year) | 0-1 | 2-3 | >3 | Migration cost increasing |

---

## 5. Exit Strategy Templates

### 5.1 Template: документирование exit strategy

```markdown
## Exit Strategy: [Tool Name]

### Trigger Conditions
- [ ] Last commit > 30 days ago
- [ ] Critical vulnerability unpatched
- [ ] License changed to non-open
- [ ] Better alternative available (score > current + 0.5)
- [ ] Team expertise no longer available

### Migration Plan
1. [ ] Identify all usages: `grep -r "tool_name" --include="*.md"`
2. [ ] Estimate migration effort: [days]
3. [ ] Select target tool: [name]
4. [ ] Pilot migration on smallest usage
5. [ ] Full migration
6. [ ] Update AGENTS.md, CI, documentation
7. [ ] Remove old tool from dependencies

### Data Format Compatibility
| From | To | Converter | Loss |
|---|---|---|---|
| [format] | [format] | [tool/сript] | [what's lost] |

### Rollback Plan
- [ ] Keep old tool installed for 1 sprint after migration
- [ ] Feature flag to switch between old/new
- [ ] Document rollback procedure

### Cost Estimation
| Item | Effort | Risk |
|---|---|---|
| Data migration | [X days] | [Low/Med/High] |
| Code changes | [X days] | [Low/Med/High] |
| Team retraining | [X days] | [Low/Med/High] |
| CI/CD updates | [X days] | [Low/Med/High] |
```

### 5.2 Матрица миграционной сложности

| From → To | Сложность | Timeline | Data Loss |
|---|---|---|---|
| Spec Kit → OpenSpec | Low | 1 day | Minimal |
| OpenSpec → Spec Kit | Low | 1 day | Minimal |
| Gauge → Cucumber | Medium | 2-3 days | Format change |
| MkDocs → Docusaurus | Low | 1-2 days | Theme-specific |
| Mermaid → PlantUML | Medium | 1 day | Syntax change |
| Kafka → RabbitMQ | High | 2-4 weeks | Replay capability |
| GitHub Actions → GitLab CI | Medium | 3-5 days | Syntax rewrite |
| Quarto → Jupyter Book | Low | 1-2 days | Minimal |

---

## 6. Принятие решений

### 6.1 ADR для смены инструмента

Любая смена инструмента — это архитектурное решение, требующее ADR:

```markdown
---
id: adr-NNNN
type: adr
status: proposed
title: Switch from [Old Tool] to [New Tool]
traces: [rfc-NNNN]
---

# NNNN. Switch from [Old Tool] to [New Tool]

## Context and Problem Statement
[Why current tool no longer suitable]

## Decision Drivers
- [Health metrics that triggered change]
- [New requirements]
- [Team constraints]

## Considered Options
- Stay with [Old Tool]
- Switch to [New Tool]
- Switch to [Alternative 2]

## Decision Outcome
Chosen option: "[New Tool]", because [reasons]

### Consequences
- Good, because [benefits]
- Bad, because [costs]

## Migration Plan
[Reference to exit strategy]
```

### 6.2 Decision Tree

```
Инструмент требует замены?
│
├── Нет (health green, требования выполнены)
│   └── Продолжить мониторинг
│
├── Да (health yellow/red, новые требования)
│   ├── Есть критическая зависимость? (> 1 sprint to migrate)
│   │   ├── Да → Планировать миграцию в next quarter
│   │   │   └── Создать RFC + ADR
│   │   └── Нет → Мигрировать в next sprint
│   │       └── Быстрая миграция + ADR
│   │
│   └── Есть лучшая альтернатива? (score > current + 0.5)
│       ├── Да → RFC для обсуждения
│       └── Нет → Document limitations, continue
```

---

## 7. Сводная таблица: Primary инструменты

| Категория | Primary | Альтернатива | Exit Effort |
|---|---|---|---|
| **SDD** | Spec Kit + OpenSpec | BMAD | 1 day |
| **BDD** | Gauge | Cucumber/Reqnroll | 2-3 days |
| **ADR** | MADR | Nygard | 2 hours |
| **Docs Site** | MkDocs Material | Docusaurus | 1-2 days |
| **Diagrams** | Mermaid + PlantUML | D2 | 1 day |
| **Requirements** | EARS + Gherkin | Job Stories | Format change only |
| **CI/CD** | GitHub Actions | GitLab CI | 3-5 days |
| **CD (GitOps)** | ArgoCD | Flux | 2-3 days |
| **Message Broker** | Kafka | RabbitMQ | 2-4 weeks |
| **API Spec** | OpenAPI + AsyncAPI | Avro/Protobuf | Converter exists |
| **Research** | Quarto | Jupyter Book | 1-2 days |
| **Research Env** | Docker | Singularity | 1 day |

---

## 8. Файл конфигурации реестра

```yaml
# tools.yaml (корень репозитория)
version: 1

tools:
  sdd:
    primary:
      name: "spec-kit"
      repo: "github/spec-kit"
      version: "latest"
      use_for: "greenfield"
    secondary:
      name: "openspec"
      repo: "Fission-AI/OpenSpec"
      version: "latest"
      use_for: "brownfield"

  bdd:
    primary:
      name: "gauge"
      repo: "getgauge/gauge"
      version: "latest"
      specs_format: "markdown"

  adr:
    primary:
      name: "madr"
      repo: "adr/madr"
      version: "4.0.0"
      format: "markdown"

  docs_site:
    primary:
      name: "mkdocs-material"
      repo: "squidfunk/mkdocs-material"
      version: "latest"

  diagrams:
    primary:
      name: "mermaid"
      repo: "mermaid-js/mermaid"
      use_for: "simple"
    secondary:
      name: "plantuml"
      repo: "plantuml/plantuml"
      use_for: "complex_c4"

health_check:
  frequency: "quarterly"
  thresholds:
    days_since_commit: 30
    min_stars: 100
    min_contributors: 3

exit_strategies:
  spec-kit:
    target: "openspec"
    effort: "1 day"
    data_loss: "minimal"

  gauge:
    target: "cucumber"
    effort: "2-3 days"
    data_loss: "format change"
```

---

## 9. Источники

### 9.1 Официальные сайты инструментов

| Категория | Инструменты |
|---|---|
| **SDD** | [Spec Kit](https://github.com/github/spec-kit), [OpenSpec](https://github.com/Fission-AI/OpenSpec), [BMAD](https://github.com/bmad-code-org/BMAD-METHOD) |
| **BDD** | [Gauge](https://gauge.org), [Cucumber](https://cucumber.io), [Reqnroll](https://reqnroll.net), [Karate](https://karatelabs.io) |
| **ADR** | [MADR](https://adr.github.io/madr), [adr-tools](https://github.com/npryce/adr-tools), [Log4brains](https://github.com/thomvaill/log4brains) |
| **Docs** | [MkDocs Material](https://squidfunk.github.io/mkdocs-material), [Docusaurus](https://docusaurus.io), [Sphinx](https://www.sphinx-doc.org) |
| **Diagrams** | [Mermaid](https://mermaid.js.org), [PlantUML](https://plantuml.com), [D2](https://d2lang.com) |
| **CI/CD** | [GitHub Actions](https://github.com/features/actions), [ArgoCD](https://argoproj.github.io/cd), [Flux](https://fluxcd.io) |
| **Messaging** | [Kafka](https://kafka.apache.org), [RabbitMQ](https://www.rabbitmq.com) |
| **API** | [OpenAPI](https://www.openapis.org), [AsyncAPI](https://www.asyncapi.com) |
| **Research** | [Quarto](https://quarto.org), [Jupyter Book](https://jupyterbook.org) |

### 9.2 Сравнения и обзоры

| Ресурс | Что покрывает |
|---|---|
| [BDD Tools Comparison 2026](https://thectoclub.com)【turn0search0】 | Cucumber, Gauge, Karate и др. |
| [Docs Generators Comparison](https://damilola-oladele.dev)【turn0search5】 | MkDocs, Docusaurus, Sphinx |
| [Diagram Tools Comparison 2026](https://codepic.cc)【turn0search10】 | Mermaid vs PlantUML vs D2 |
| [Spec-Driven AI Tools](https://ranthebuilder.cloud)【turn0search5】 | Spec Kit, OpenSpec, BMAD |
| [Message Brokers Comparison](https://dev.to)【turn0search10】 | Kafka, RabbitMQ, SQS |
| [Dependency Tools Comparison](https://rafter.so)【turn0search11】 | Snyk, Dependabot, Renovate |
| [CI/CD Tools 2026](https://devtoollab.com)【turn0search15】 | ArgoCD, Flux, Jenkins |
