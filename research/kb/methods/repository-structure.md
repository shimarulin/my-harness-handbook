# Структура репозитория: раскладка, ID, индексы (синтез v2+v3)

| Параметр | Значение |
|---|---|
| Статус | draft |
| Обновлено | 2026-09-30 |

## Что это

Каноническая раскладка git-репозитория как source of truth всех артефактов процесса: предсказуемые директории, единая ID-система, machine-readable метаданные (YAML front-matter), index-файлы для навигации. Синтез v3/06 (строгая система с ID и front-matter) + v2 storage-organization (принципы colocation, naming, index-файлы).

## Принципы

- **R1. Один репозиторий = один source of truth** (всё в git; split-repo — осознанное исключение, см. ниже).
- **R3. Предсказуемость**: единая раскладка во всех проектах организации.
- **R4. Machine-readable**: YAML front-matter в каждом артефакте (обязательные поля: id, type, status, created, title).
- **R5. Сквозная трассировка**: ID и связи `traces` (см. `artifact-pipeline.md`).
- **R6. Открытые форматы**: только Markdown, YAML, PlantUML/Mermaid/D2, Gherkin, OpenAPI/AsyncAPI/JSON Schema.
- **R7. CI-friendly**: lint, validate, build в CI.
- **Colocation**: документация рядом с описываемым (feature specs рядом с кодом фичи; ADR — общие в docs/).
- **Discoverability**: index-файл в каждой директории.

## Каноническая раскладка (полная, L3–L4)

```
project/
├── README.md                  # входная точка: что, зачем, статус, Quick Links
├── AGENTS.md                  # правила для AI-агентов (durable context)
├── CONSTITUTION.md            # постоянные принципы проекта
├── docs/
│   ├── prd/                   # PRD (L2+): NNN-slug.md + _index.md
│   ├── rfc/                   # RFC/Design Docs (L3+): NNNN-slug.md
│   ├── adr/                   # ADR (MADR, всегда): 0001-record-architecture-decisions.md, NNNN-slug.md, README.md (index)
│   ├── specs/                 # фича-спецификации (L2+)
│   │   └── NNN-slug/
│   │       ├── spec.md        # EARS-требования
│   │       ├── design.md      # дизайн (notes или полный)
│   │       ├── tasks.md       # задачный чеклист
│   │       ├── api/           # openapi.yaml (если есть API)
│   │       └── scenarios/     # Gherkin (L3+)
│   ├── architecture/          # L3+: c4/ (.puml/.mmd), arc42/ (L4, 12 секций)
│   ├── quality/               # quality scenarios (L4)
│   ├── research/              # research compendia
│   ├── ideas/                 # idea-NNN + _index.md (фильтр по статусу)
│   ├── decisions.md           # Y-Statements для мелких решений (S1–S2)
│   └── process/               # документация самого процесса + templates/
├── tasks/                     # L1-задачи: NNN-slug.md + _index.md
├── tests/
│   └── features/              # исполняемые Gherkin-фичи
├── api/                       # глобальные контракты: openapi.yaml, asyncapi.yaml
├── .ai/
│   └── rules.md               # дополнительные правила агентов
├── .github/workflows/         # docs.yml, trace-check.yml
└── mkdocs.yml                 # сборка сайта документации
```

SDD-инструменты живут в собственных каталогах, не смешиваясь с общей территорией: `.specify/` + `specs/` (Spec Kit), `openspec/` (OpenSpec: `specs/` canonical + `changes/` + `changes/archive/`).

## Минимальная раскладка (L1–L2, S1–S2)

`README.md` + `AGENTS.md` + `CONSTITUTION.md` + `docs/adr/` (обязательно всегда) + `docs/decisions.md` (Y-Statements) + `tasks/` + один SDD-инструмент (openspec/ ИЛИ .specify/) или ни одного.

## Раскладка по размеру организации (v2 storage)

| Размер | Структура |
|---|---|
| Small (< 3 мес, 1–3 dev) | README, docs/adr/ + decisions.md, один spec.md, src/, tests/ |
| Medium (3–12 мес, 3–10 dev) | + docs/rfc/, docs/architecture/, specs/feature-N/, features/ (BDD) |
| Large (12+ мес, 10+ dev) | Полный набор + specs/<feature>/ со всеми фазами + api/ + feature-adr/, scripts/ |
| Enterprise | Monorepo (docs/ cross-service + services/<svc>/{specs,adr,src}) или multi-repo + governance repo (standards/, compliance/, audit/) |

## Split-repository (2 репо)

Когда: публичная документация / приватный код; мультипроектная документация; разные access levels. docs-repo: AGENTS.md, CONSTITUTION.md, docs/ (adr, prd, rfc, architecture, process), openspec/ (canonical specs), mkdocs.yml. code-repo: AGENTS.md (ссылается на docs-repo), specs/, tasks/, tests/, api/, src/. Cross-repo трассировка: `traces: [repo:project-docs:adr-0007]`. Формат и ID одинаковы в обоих.

## Naming conventions

- kebab-case для всех файлов и директорий (❌ underscores, ❌ spaces, ❌ CamelCase); lowercase для путей.
- Номера с leading zeros: ADR — 4 знака (`adr-0007`), PRD/RFC/idea/task/spec — 3 знака (`prd-005`, `task-042`).
- Descriptive names: `rfc-0031-export-architecture.md` ✅, `rfc-0031.md` ❌.
- Фиксированные имена фаз: `problem-statement.md`, `requirements.md`, `approach.md`, `tasks.md`.
- PRD без ID-префикса в v2 (`docs/prd/<feature-name>.md`); v3 — `prd-NNN`. Рекомендация синтеза: v3-схема (единообразие ID).
- Commit-форматы: `docs(adr): add ADR-NNNN <title>`; `trivial: <описание>` (L0).

## Index-файлы (две конвенции)

- **v2**: `README.md` в каждой директории (ручной: таблицы статусов, ссылки, контакты).
- **v3**: `_index.md` auto-generated (скрипт по front-matter; у ideas — фильтр по статусу).

Рекомендация синтеза: `_index.md` (auto-generated) для растущих коллекций (adr, prd, rfc, ideas, tasks) — снимает ручную поддержку; README.md — для точек входа (корень, specs/<feature>/), где нужен кураторский контент (статус фаз, timeline, контакты). Согласуется с принципом «ссылка дешевле файла» из research-процессов (инсайт #7).

## Миграция существующего проекта без SDD (3 фазы)

1. Минимальная структура: CONSTITUTION.md, AGENTS.md, первый ADR, шаблоны.
2. Выбрать SDD-инструмент (`openspec init` или `specify init`) — или остаться без него.
3. Мигрировать документацию: design docs → docs/rfc/, wiki → docs/, решения из чатов → docs/adr/.

## Анти-паттерны

- Documentation Scatter (разброс без логики); No Index Files; Inconsistent Naming (→ линтеры + review); Broken Cross-References (→ `check_links.py` в CI); Monolithic Documentation (один огромный файл); Documentation Without Code (отдельный репо без colocation).

## Источники

- Входные материалы inbox: `documentation-process-v3/06-repository-structure.md` (каноническая раскладка, ID, front-matter, checklist), `documentation-process-v2/storage-organization/README.md` (принципы, 3 варианта, naming, index, анти-паттерны)
- Связанные KB: `artifact-pipeline.md`, `process-levels.md`, `../landscape/toolchain-registry.md`
