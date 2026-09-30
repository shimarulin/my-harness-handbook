# Docs-as-Code CI/CD: пайплайн проверок документации

| Параметр | Значение |
|---|---|
| Статус | draft |
| Обновлено | 2026-09-30 |

## Что это

CI/CD пайплайн для документации по принципу **«Docs = Code»**: те же гейты, линтинг, валидация и деплой, что для кода. Шесть этапов: Lint → Validate → Render → Build → Test Specs → Deploy.

```
Push/PR → [Lint] → [Validate] → [Render] → [Build] → [Test Specs] → [Deploy]
           │           │            │           │            │            └→ GitHub Pages / Netlify
           │           │            │           │            └→ Gauge / Cucumber
           │           │            │           └→ MkDocs site
           │           │            └→ PlantUML / Mermaid → SVG (артефакты CI)
           │           └→ trace-check, front-matter schema, ADR-lint, openspec validate
           └→ markdownlint, yamllint
```

Принципы: C1 Docs = Code (те же гейты); C2 Fail fast (ошибка линтинга блокирует merge); C3 Артефакты версионируются (диаграммы рендерятся в CI, **не коммитятся**); C4 Кэширование зависимостей; C5 Параллельность независимых jobs.

## Этапы и проверки

### 1. Lint

- **markdownlint-cli2** (`.markdownlint-cli2.jsonc`): default rules; MD013 (line-length) off — длинные URL; MD033 (inline HTML) off — embed диаграмм; MD041 off — front-matter first; MD024 siblings_only; MD025 front_matter_title. Ignores: node_modules, vendor, `.specify/templates/**`, `openspec/changes/archive/**`.
- **yamllint** (`.yamllint.yaml`): extends relaxed; line-length max 120 (warning); truthy: true/false/yes/no; document-start: present: false.

### 2. Validate

- **Front-matter schema** (`schemas/frontmatter.schema.json`, через remark-lint-frontmatter-schema): required `id, type, status, created, title`; id pattern `^(idea|task|prd)-\d{3}$|^(rfc|adr)-\d{4}$`; type enum `idea|task|prd|rfc|adr|spec|change`; status enum `draft|review|approved|rejected|superseded|archived|promoted|candidate`; опциональные `traces[], relates_to[], deciders[], tags[], priority (P0–P3), level (L0–L4)`.
- **trace_check.py**: каждый `traces:` имеет валидный ID предшественника; superseded ADR имеет непустой `superseded_by` (и цель существует); статусы из допустимого множества; уникальность ID в рамках типа. Search dirs: `docs/decisions, docs/prd, docs/rfc, docs/ideas, tasks, openspec/changes`.
- **generate_indexes.py**: генерация `_index.md` по директориям (decisions/prd/rfc/ideas/tasks) со статус-иконками (✅ approved, 📝 draft, 👀 review, ❌ rejected, ⏭️ superseded, 📦 archived, 💭 candidate).
- **openspec validate** (условно, если есть `openspec/config.yaml`): `--strict` для строгой проверки.

### 3. Render

PlantUML: `plantuml -tsvg` для всех `docs/**/*.puml`. Mermaid: нативно в GitHub; локально/CI `mmdc -i <in>.mmd -o <out>.svg`. **Важно**: рендеренные SVG/PNG не коммитятся — генерируются в CI, деплоятся со статическим сайтом (upload-artifact `rendered-diagrams`, retention 7 дней).

### 4. Build

`mkdocs build --strict` (битые ссылки = ошибка сборки) + плагины: search, git-revision-date-localized; theme material (navigation.tabs/sections, search.highlight, palette toggle); markdown_extensions: admonition, pymdownx.highlight, superfences с mermaid fence, tabbed, toc. Nav: Home, Process, Decisions, PRD, RFC, Ideas, Architecture — все `*/index.md`.

### 5. Test Specs (опционально)

Gauge: `gauge run specs/` в `tests/`; Cucumber: `./gradlew test` (Java 21). Исполняемые спецификации в CI = living documentation.

### 6. Deploy

GitHub Pages: configure-pages@v4 → upload-pages-artifact@v3 (path: site) → deploy-pages@v4; только `if: github.ref == 'refs/heads/main' && github.event_name == 'push'`.

## Pre-commit hooks (локальный gate до CI)

`.pre-commit-config.yaml` (5 hooks): markdownlint-cli2 (types: markdown); yamllint (-c .yamllint.yaml, types: yaml); frontmatter-validate (local, `scripts/validate_frontmatter.py`, files: `^(docs/|tasks/|openspec/changes/)`); plantuml-check (local, files: `\.puml$`); trace-check (local, pass_filenames: false).

## Структура скриптов

```
scripts/
├── trace_check.py           # валидация трассировки
├── generate_indexes.py      # генерация _index.md
├── render_plantuml.sh       # рендеринг диаграмм
├── check_plantuml.sh        # syntax check
└── validate_frontmatter.py  # front-matter валидация (pre-commit)
schemas/
└── frontmatter.schema.json
```

## Минимальный пайплайн (стартовая точка)

Один job: checkout → setup-node → `markdownlint-cli2 "docs/**/*.md"` → setup-python → `python scripts/trace_check.py` → `mkdocs build --strict`. Расширять до полного по мере появления диаграмм, спек и деплоя.

## Метрики пайплайна

Documentation coverage (trace_check статистика); broken links (mkdocs --strict); linting violations (количество); artifact counts per тип (generate_indexes); diagram render time и site build time (CI logs). Бейджи: Docs CI badge + «docs online» shield в README.

## Источники

- markdownlint-cli2: https://github.com/DavidAnson/markdownlint-cli2; remark-lint-frontmatter-schema: https://github.com/JulianCataldo/remark-lint-frontmatter-schema; MkDocs Material publishing: https://squidfunk.github.io/mkdocs-material/publishing-your-site; pre-commit: https://pre-commit.com; OpenSpec validate: https://openspec.dev/docs/cli
- Входные материалы inbox: `documentation-process-v3/07-cicd-docs-pipeline.md`
- Связанные KB: `repository-structure.md`, `versioning-lifecycle.md` (CI-проверки статусов/supersession), `../landscape/toolchain-registry.md`
