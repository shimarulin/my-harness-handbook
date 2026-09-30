# Глава 6. Структура репозитория и toolchain

Как устроен репозиторий как source of truth всех артефактов и как выбирать/менять инструменты без vendor-lock. Детали — `../research/kb/methods/repository-structure.md`, `../research/kb/landscape/toolchain-registry.md`.

## 6.1. Принципы раскладки

Один репозиторий = один source of truth (R1); предсказуемость (единая раскладка во всех проектах, R3); machine-readable метаданные — YAML front-matter в каждом артефакте (R4); сквозная трассировка (R5); только открытые форматы (R6); CI-friendly (R7). Плюс colocation (документация рядом с описываемым) и discoverability (index-файл в каждой директории).

## 6.2. Каноническая раскладка

```
project/
├── README.md                  # входная точка: что, зачем, статус, Quick Links
├── AGENTS.md                  # правила для AI-агентов (durable context)
├── CONSTITUTION.md            # постоянные принципы проекта
├── docs/
│   ├── prd/                   # PRD (L2+): NNN-slug.md + _index.md
│   ├── rfc/                   # RFC (L3+): NNNN-slug.md
│   ├── adr/                   # ADR (MADR, всегда): 0001-…, NNNN-slug.md, README.md
│   ├── specs/NNN-slug/        # фича-спеки (L2+): spec.md, design.md, tasks.md, api/, scenarios/
│   ├── architecture/          # L3+: c4/, arc42/ (L4)
│   ├── ideas/                 # idea-NNN + _index.md
│   └── process/               # документация процесса + templates/
├── tasks/                     # L1-задачи: NNN-slug.md + _index.md
├── tests/features/            # исполняемые Gherkin
├── api/                       # openapi.yaml, asyncapi.yaml
├── .ai/rules.md               # дополнительные правила агентов
└── .github/workflows/         # docs.yml, trace-check.yml
```

SDD-инструменты живут в собственных каталогах (`.specify/` + `specs/` для Spec Kit, `openspec/` для OpenSpec), не смешиваясь с общей территорией. Минимальная раскладка (L1–L2): README + AGENTS.md + CONSTITUTION.md + `docs/adr/` (обязательно всегда) + `tasks/` (+ один SDD-инструмент или ни одного).

## 6.3. ID, naming, индексы

ID: `idea/task/prd/spec-NNN` (3 знака), `rfc/adr-NNNN` (4 знака); ADR-0001 зарезервирован (`0001-record-architecture-decisions.md`). Naming: kebab-case для файлов и директорий; номера с leading zeros; descriptive names (`rfc-0031-export-architecture.md` ✅). Индексы: `_index.md` auto-generated для растущих коллекций (adr, prd, rfc, ideas, tasks — снимает ручную поддержку), README.md для точек входа (кураторский контент: статус фаз, timeline, контакты).

## 6.4. Split-repository

Когда: публичная документация / приватный код; мультипроектная документация; разные access levels. docs-repo (AGENTS.md, CONSTITUTION.md, docs/, openspec/) + code-repo (specs/, tasks/, api/, src/); cross-repo трассировка `traces: [repo:project-docs:adr-0007]`; формат и ID одинаковы в обоих.

## 6.5. Toolchain: принципы выбора

Принцип T1: **формат важнее инструмента**. Для каждой категории — primary + ≥1 альтернатива (T2), exit strategy (T3), quarterly health check (T4), заменимость ≤ 1 sprint (T5). Смена инструмента = архитектурное решение → ADR. Критерии: открытая лицензия, открытый формат данных, экспорт 100% (critical); активная разработка, сообщество, документация (high); экосистема, порог входа (medium).

Реестр primary по категориям (полный — `../research/kb/landscape/toolchain-registry.md`): SDD — Spec Kit (greenfield) + OpenSpec (brownfield); BDD — Gauge; ADR — MADR + adr-tools; docs — MkDocs Material; диаграммы — Mermaid + PlantUML; требования — EARS + Gherkin; CI — GitHub Actions; CD — ArgoCD; broker — Kafka; API — OpenAPI + AsyncAPI + JSON Schema; research — Quarto + Docker.

## 6.6. Spec Kit vs OpenSpec (decision matrix)

| Критерий | Spec Kit | OpenSpec |
|---|---|---|
| Greenfield / Brownfield | ✅ / ⚠️ | ⚠️ / ✅ (delta specs) |
| Guardrails (phase gates) | Сильные | Слабые (advisory) |
| Overhead per-фича | ~800 строк | ~250 строк |
| Compliance | ✅ | ⚠️ |

Триггеры миграции с порогами: Spec Kit → OpenSpec (brownfield > 50%, docs > 30% времени, команда < 3); OpenSpec → Spec Kit (команда > 5 распределённая, compliance, vibe-coding дрейф > 2/мес). Exit strategy ~1 день в обе стороны (Markdown → Markdown); не мигрируют: slash commands, phase gates, delta specs.

## 6.7. Quarterly health check

Workflow по cron (1-е число квартала): last commit, stars, active contributors через GitHub API. Пороги: red = > 30 дней без коммита или < 3 contributors → «Consider alternative»; триггер смены — альтернатива score > current + 0.5. `tools.yaml` в корне: primary/secondary + thresholds + exit_strategies.

---

**Дальше:** [Глава 7. AI-агенты в процессе](07-ai-agents-in-process.md) — durable context, роли и протоколы human↔AI.
