# Реестр тулчейна: выбор, скоринг, exit strategies (синтез v2+v3)

| Параметр | Значение |
|---|---|
| Статус | draft |
| Обновлено | 2026-09-30 (скоринги и звёзды — на дату источников; перепроверять при quarterly health check) |

## Что это

Реестр инструментов по категориям с принципом «формат важнее инструмента» (T1): для каждой категории — primary + минимум одна альтернатива, скоринг, оценка vendor lock и заранее прописанная exit strategy. Любой инструмент заменяем за ≤ 1 sprint (T5: никакой критической зависимости). Смена инструмента = архитектурное решение → ADR.

## Принципы T1–T5

T1 формат важнее инструмента; T2 primary + alternatives (≥2 варианта на категорию); T3 exit strategy обязательна; T4 мониторинг здоровья (quarterly review); T5 замена ≤ 1 sprint.

## Критерии выбора

**Critical**: открытая лицензия (MIT/Apache/GPL); открытый формат данных; экспорт 100% данных (проверять тестом). **High**: активная разработка (коммит за 30 дней); сообщество (>100 contributors ИЛИ >1000 stars); документация с примерами. **Medium**: экосистема плагинов; порог входа (новичок продуктивен < 1 дня, проверка pilot). Скоринг: criterion 0–3, порог принятия Score ≥ 2.0, триггер смены — альтернатива > current + 0.5.

## Реестр по категориям (primary → альтернативы)

| Категория | Primary | Альтернативы | Не рекомендовано / legacy |
|---|---|---|---|
| **SDD** | Spec Kit (greenfield, 2.6), OpenSpec (brownfield, 2.5) | BMAD-METHOD (2.3, Medium lock) | Kiro (1.8, High lock — AWS ecosystem) |
| **BDD** | Gauge (2.7, Markdown-спеки) | Cucumber (JVM, 2.5), Reqnroll (.NET, 2.4), Behave (Python, 2.3), Karate (API, 2.4) | JBehave (legacy, 1.9); SpecFlow — EOL 2024-12-31 |
| **ADR** | MADR (2.8), adr-tools (Nygard CLI, 2.5) | YADR (YAML, 2.0), Structurizr (C4, 2.3) | Log4brains (2.2, ⚠️ unmaintained >18 мес.) |
| **Docs-генераторы** | MkDocs Material (2.8) | Docusaurus (2.6), Sphinx (Python+API, 2.5), Antora (AsciiDoc multi-repo, 2.3), VitePress (Vue, 2.2) | — |
| **Diagram-as-Code** | Mermaid (2.7, GitHub-native) + PlantUML (2.6, полный C4) | D2 (2.4, лучший autolayout), Graphviz (2.2) | — |
| **Нотации требований** | EARS (2.7, high-level) + Gherkin (2.6, executable) | Job Story (2.3), User Story (2.2) | — |
| **CI/CD** | GitHub Actions (2.7, Medium lock); ArgoCD (GitOps CD, 2.8) | GitLab CI (2.6), Flux (2.6) | Jenkins (legacy, 1.9) |
| **Message brokers** | Kafka (2.8: replay, schema registry) | RabbitMQ (2.5, нет replay), Redis Streams (2.2, memory-bound), SQS/SNS (2.3, не cloud-agnostic) | — |
| **API specs** | OpenAPI 3.x (REST, 2.8) + AsyncAPI 3.x (Event, 2.6) + JSON Schema (2.7) | Avro (Kafka, 2.5), Protobuf (gRPC, 2.5) | — |
| **Research/repro** | Quarto (2.8) + Docker (2.8) | Jupyter Book (2.5), Singularity (HPC, 2.4) | R Markdown (legacy, 2.3) |

Выбор per-стек: BDD — multi-language → Gauge; JVM → Cucumber; .NET → Reqnroll; Python → Behave/Gauge; API → Karate. Docs — Python → MkDocs Material; React/Node → Docusaurus; multi-repo → Antora. Диаграммы: Mermaid для простых (README), PlantUML для архитектурных (C4, sequence).

Инструменты из v2 tools-automation (готовые workflows и скрипты): Spectral (API linting, 400+ rules), OpenAPI Generator (codegen 40+ языков), Stoplight (визуальный OpenAPI editor), `lint_ears.py` (EARS-линтер: паттерны, REQ-IDs, vague terms), `check_links.py` (cross-references), adr-tools, Log4brains (с оговоркой выше).

## Spec Kit vs OpenSpec (decision matrix)

| Критерий | Spec Kit | OpenSpec |
|---|---|---|
| Greenfield | ✅ | ⚠️ |
| Brownfield | ⚠️ | ✅ (delta specs) |
| Guardrails (phase gates) | Сильные | Слабые (advisory) |
| Скорость итерации | Медленнее | Быстрее |
| Enterprise compliance | ✅ | ⚠️ |
| Overhead per-фича | ~800 строк | ~250 строк |
| Расширяемость | Extensions + presets | Schemas + config |
| Runtime | Python (uv) | Node.js |

Когда Spec Kit: новая платформа L4; команда > 5 распределённая; регулируемая отрасль; несколько параллельных агентов; Python-first. Когда OpenSpec: существующий проект + AI; solo/небольшая команда; эволюционирующие требования; L1–L2; Node.js; параллельные small changes. L0 — оба overkill. Hybrid: openspec/ для фич + specs/ для платформенных решений; общие CONSTITUTION.md и AGENTS.md с правилом «Workflow Selection».

### Триггеры миграции (с порогами)

Spec Kit → OpenSpec: brownfield (>50% изменений — модификация существующего); docs > 30% времени имплементации; команда < 3; > 5 экспериментальных фич подряд; > 3 смены требований за sprint. OpenSpec → Spec Kit: команда > 5 распределённая; compliance/audit; vibe-coding дрейф (> 2 инцидента несоответствия спеке за месяц); L3–L4; формальный approval workflow с внешними стейкхолдерами.

Метрики quarterly review: documentation overhead; spec-code alignment (< 80% — alarm); agent iteration count (> 5 per фича); rework rate (> 20%).

## Exit strategies (типовые)

Шаблон: Trigger Conditions (last commit > 30 дней; unpatched critical vulnerability; license changed; альтернатива score > +0.5; потеря экспертизы) → Migration Plan (7 шагов: identify usages `grep -r`; estimate effort; select target; pilot на smallest usage; full migration; update AGENTS.md/CI/docs; remove) → Data Format Compatibility → Rollback Plan (keep old 1 sprint) → Cost Estimation.

| Миграция | Усилие | Что конвертируется |
|---|---|---|
| Spec Kit ↔ OpenSpec | ~1 день | specs/<feature>/ ↔ openspec/changes/; constitution ↔ CONSTITUTION.md. НЕ мигрирует: slash commands (обновить AGENTS.md), phase gates, extensions ↔ schemas, delta specs («выпрямить» в полный spec) |
| Gauge → Cucumber | 2–3 дня / 100+ спек | Заголовки → Feature/Scenario, steps → Given/When/Then; переписать step implementations |
| MADR → Nygard | ~2 ч / 50+ ADR | Секции схлопываются (Context+Problem → Context; Outcome → Decision; Pros/Cons → Consequences) |
| MkDocs → Docusaurus | 1–2 дня | mkdocs.yml → docusaurus.config.js; admonitions → :::note |
| Mermaid → PlantUML | ~1 день / 20+ диаграмм | Community converter + ручная доработка |
| GHA → GitLab CI | 3–5 дней | jobs → stages; uses → include; runs-on → tags |
| Kafka → RabbitMQ | 2–4 недели | Dual-write → миграция consumers → producers; риск: потеря replay |

## Quarterly health check

Workflow `.github/workflows/tool-health.yml` (cron, 1-е число квартала): через GitHub API — last commit, stars, active contributors. Пороги: days since commit — green < 7, yellow 7–30, red > 30 («Consider alternative»); contributors — > 10 / 3–10 / < 3 (single-maintainer risk); open issues — < 50 / 50–100 / > 100; breaking changes/год — 0–1 / 2–3 / > 3. Decision tree: red + критическая зависимость → миграция в next quarter (RFC + ADR); red + заменим → next sprint + ADR.

`tools.yaml` в корне репо: реестр primary/secondary по категориям + health_check thresholds + exit_strategies (target, effort, data_loss).

## Источники

- Входные материалы inbox: `documentation-process-v3/09-toolchain-registry.md` (реестр, скоринг, health check, exit strategies), `documentation-process-v3/04-tool-selection-and-migration.md` (Spec Kit vs OpenSpec, триггеры, процедуры), `documentation-process-v2/tools-automation/README.md` (каталог инструментов, CI workflows, скрипты)
- Связанные KB: `sdd-tools-overview.md`, `../methods/repository-structure.md`
