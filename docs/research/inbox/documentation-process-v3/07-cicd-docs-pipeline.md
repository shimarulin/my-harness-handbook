# CI/CD Pipeline для документации

| Параметр | Значение |
|---|---|
| Дата | 2026-09-29 |
| Статус | Draft |
| Связан с | `06-repository-structure.md` |

---

## 1. Архитектура пайплайна

### 1.1 Этапы

```
Push/PR → [Lint] → [Validate] → [Render] → [Build] → [Test Specs] → [Deploy]
           │           │            │           │            │            │
           │           │            │           │            │            └→ GitHub Pages / Netlify
           │           │            │           │            └→ Gauge / Cucumber
           │           │            │           └→ MkDocs site
           │           │            └→ PlantUML / Mermaid → SVG/PNG
           │           └→ Trace-check, ADR-lint, Front-matter schema
           └→ markdownlint, yamllint
```

### 1.2 Принципы

| # | Принцип | Следствие |
|---|---|---|
| C1 | Docs = Code | Тот же CI/CD, те же гейты |
| C2 | Fail fast | Ошибка линтинга блокирует merge |
| C3 | Артефакты версионируются | Диаграммы рендерятся в CI, не коммитятся |
| C4 | Кэширование | Зависимости кэшируются между ранами |
| C5 | Параллельность | Независимые джобы跑 параллельно |

---

## 2. Линтинг

### 2.1 markdownlint-cli2

**Конфигурация**: `.markdownlint-cli2.jsonc` в корне репозитория.

```jsonc
{
  "config": {
    "default": true,
    "MD013": false,           // line-length: отключено (длинные URL)
    "MD033": false,           // inline HTML: разрешено (PlantUML embed)
    "MD041": false,           // first-line-heading: front-matter first
    "MD024": {                // no-duplicate-heading: разрешить в разных секциях
      "siblings_only": true
    },
    "MD025": {                // single-h1: front-matter title считается
      "front_matter_title": ""
    }
  },
  "customRules": [],
  "ignores": [
    "node_modules/**",
    "vendor/**",
    ".specify/templates/**",   // Spec Kit templates — не наши
    "openspec/changes/archive/**"  // Архивные changes — не линтим
  ]
}
```

### 2.2 yamllint (для front-matter и YAML-файлов)

**Конфигурация**: `.yamllint.yaml`

```yaml
extends: relaxed

rules:
  line-length:
    max: 120
    level: warning
  truthy:
    allowed-values: ['true', 'false', 'yes', 'no']
  document-start:
    present: false  # front-matter не считается document start
```

### 2.3 Pre-commit hooks

**Конфигурация**: `.pre-commit-config.yaml`

```yaml
repos:
  # Markdown linting
  - repo: https://github.com/DavidAnson/markdownlint-cli2
    rev: v0.14.0
    hooks:
      - id: markdownlint-cli2
        name: markdownlint
        entry: markdownlint-cli2
        language: node
        types: [markdown]

  # YAML linting
  - repo: https://github.com/adrienverhall/yamllint
    rev: v1.35.1
    hooks:
      - id: yamllint
        args: [-c, .yamllint.yaml]
        types: [yaml]

  # Front-matter validation (see §3.2)
  - repo: local
    hooks:
      - id: frontmatter-validate
        name: Validate YAML front-matter
        entry: python scripts/validate_frontmatter.py
        language: python
        types: [markdown]
        files: ^(docs/|tasks/|openspec/changes/)

  # PlantUML syntax check
  - repo: local
    hooks:
      - id: plantuml-check
        name: PlantUML syntax check
        entry: bash scripts/check_plantuml.sh
        language: system
        types: [plantuml]
        files: \.puml$

  # Traceability check (see §3.1)
  - repo: local
    hooks:
      - id: trace-check
        name: Check artifact traceability
        entry: python scripts/trace_check.py
        language: python
        pass_filenames: false
```

---

## 3. Валидация

### 3.1 Traceability Check (пользовательский скрипт)

**Скрипт**: `scripts/trace_check.py`

Проверяет:
- Каждый артефакт с `traces:` имеет валидный ID предшественника
- ADR со статусом `superseded` имеет непустой `superseded_by`
- Статусы из допустимого множества
- Уникальность ID в рамках типа

```python
#!/usr/bin/env python3
"""
Traceability validator for documentation artifacts.
Checks YAML front-matter for:
- Valid ID format
- Valid status values
- Existing trace targets
- Superseded ADRs have superseded_by
"""

import os
import re
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Patterns
ID_PATTERNS = {
    'idea': r'^idea-\d{3}$',
    'task': r'^task-\d{3}$',
    'prd': r'^prd-\d{3}$',
    'rfc': r'^rfc-\d{4}$',
    'adr': r'^adr-\d{4}$',
}

VALID_STATUSES = {
    'draft', 'review', 'approved', 'rejected',
    'superseded', 'archived', 'promoted', 'candidate'
}

REQUIRED_FIELDS = {'id', 'type', 'status', 'created', 'title'}

class Artifact:
    def __init__(self, path: Path, frontmatter: Dict):
        self.path = path
        self.frontmatter = frontmatter
        self.id = frontmatter.get('id', '')
        self.type = frontmatter.get('type', '')
        self.status = frontmatter.get('status', '')
        self.traces = frontmatter.get('traces', [])
        self.superseded_by = frontmatter.get('superseded_by')

def extract_frontmatter(filepath: Path) -> Dict:
    """Extract YAML front-matter from Markdown file."""
    content = filepath.read_text(encoding='utf-8')
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError:
            return {}
    return {}

def collect_artifacts(root: Path) -> List[Artifact]:
    """Find all Markdown files with front-matter."""
    artifacts = []
    search_dirs = ['docs/decisions', 'docs/prd', 'docs/rfc',
                   'docs/ideas', 'tasks', 'openspec/changes']

    for dir_name in search_dirs:
        dir_path = root / dir_name
        if not dir_path.exists():
            continue
        for md_file in dir_path.rglob('*.md'):
            fm = extract_frontmatter(md_file)
            if fm and 'id' in fm:
                artifacts.append(Artifact(md_file, fm))
    return artifacts

def validate_artifacts(artifacts: List[Artifact]) -> List[str]:
    """Run all validation rules."""
    errors = []
    all_ids = {a.id for a in artifacts}

    for artifact in artifacts:
        # Required fields
        missing = REQUIRED_FIELDS - set(artifact.frontmatter.keys())
        if missing:
            errors.append(f"{artifact.path}: Missing fields: {missing}")

        # ID format
        pattern = ID_PATTERNS.get(artifact.type)
        if pattern and not re.match(pattern, artifact.id):
            errors.append(f"{artifact.path}: Invalid ID format: {artifact.id}")

        # Status validity
        if artifact.status not in VALID_STATUSES:
            errors.append(f"{artifact.path}: Invalid status: {artifact.status}")

        # Trace targets exist
        for trace_id in artifact.traces:
            if trace_id not in all_ids:
                errors.append(
                    f"{artifact.path}: Trace target not found: {trace_id}"
                )

        # Superseded ADRs need superseded_by
        if artifact.type == 'adr' and artifact.status == 'superseded':
            if not artifact.superseded_by:
                errors.append(
                    f"{artifact.path}: Superseded ADR missing superseded_by"
                )
            elif artifact.superseded_by not in all_ids:
                errors.append(
                    f"{artifact.path}: superseded_by not found: "
                    f"{artifact.superseded_by}"
                )

    # Duplicate IDs
    seen_ids = {}
    for artifact in artifacts:
        if artifact.id in seen_ids:
            errors.append(
                f"Duplicate ID: {artifact.id} in "
                f"{seen_ids[artifact.id]} and {artifact.path}"
            )
        seen_ids[artifact.id] = artifact.path

    return errors

def main():
    root = Path(__file__).parent.parent
    artifacts = collect_artifacts(root)

    if not artifacts:
        print("No artifacts found to validate.")
        return 0

    errors = validate_artifacts(artifacts)

    if errors:
        print(f"\n❌ Validation failed with {len(errors)} errors:\n")
        for error in errors:
            print(f"  - {error}")
        return 1
    else:
        print(f"✅ All {len(artifacts)} artifacts valid.")
        return 0

if __name__ == '__main__':
    sys.exit(main())
```

### 3.2 Front-matter Schema Validation

**Схема**: `schemas/frontmatter.schema.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "type", "status", "created", "title"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^(idea|task|prd)-\\d{3}$|^(rfc|adr)-\\d{4}$"
    },
    "type": {
      "type": "string",
      "enum": ["idea", "task", "prd", "rfc", "adr", "spec", "change"]
    },
    "status": {
      "type": "string",
      "enum": ["draft", "review", "approved", "rejected",
               "superseded", "archived", "promoted", "candidate"]
    },
    "created": {
      "type": "string",
      "format": "date"
    },
    "title": {
      "type": "string",
      "minLength": 1
    },
    "traces": {
      "type": "array",
      "items": {"type": "string"}
    },
    "relates_to": {
      "type": "array",
      "items": {"type": "string"}
    },
    "deciders": {
      "type": "array",
      "items": {"type": "string"}
    },
    "tags": {
      "type": "array",
      "items": {"type": "string"}
    },
    "priority": {
      "type": "string",
      "enum": ["P0", "P1", "P2", "P3"]
    },
    "level": {
      "type": "string",
      "enum": ["L0", "L1", "L2", "L3", "L4"]
    }
  }
}
```

**Интеграция с remark-lint**【turn0search6】:

```bash
npm install remark-lint-frontmatter-schema
remark --use lint-frontmatter-schema --schema schemas/frontmatter.schema.json docs/**/*.md
```

### 3.3 OpenSpec Validate

Если используется OpenSpec【turn0search16】:

```bash
# Валидация всех активных changes
openspec validate

# Валидация конкретного change
openspec validate add-user-auth

# Строгий режим
openspec validate --strict
```

### 3.4 MADR Lint

Для ADR в формате MADR【turn0search1】:

```bash
# Использует конфигурацию .markdownlint из MADR проекта
markdownlint-cli2 "docs/decisions/*.md" --config madr.markdownlint.jsonc
```

---

## 4. Рендеринг диаграмм

### 4.1 PlantUML

**Скрипт**: `scripts/render_plantuml.sh`

```bash
#!/bin/bash
set -euo pipefail

# Find all PlantUML files
PUMl_FILES=$(find docs -name "*.puml" -type f)

if [ -z "$PUML_FILES" ]; then
    echo "No PlantUML files found."
    exit 0
fi

# Render to SVG
for file in $PUML_FILES; do
    output="${file%.puml}.svg"
    echo "Rendering: $file → $output"
    plantuml -tsvg "$file"
done

echo "✅ All PlantUML diagrams rendered."
```

### 4.2 Mermaid

Mermaid рендерится нативно в GitHub, но для локальной сборки MkDocs:

```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -i docs/architecture/diagram.mmd -o docs/architecture/diagram.svg
```

### 4.3 CI Rendering

В GitHub Actions диаграммы рендерятся как артефакты:

```yaml
- name: Render PlantUML diagrams
  run: |
    sudo apt-get install -y plantuml
    bash scripts/render_plantuml.sh
```

**Важно**: Рендеренные SVG/PNG **не коммитятся** в git. Они генерируются в CI и деплоятся вместе со статическим сайтом.

---

## 5. Сборка сайта

### 5.1 MkDocs Material

**Конфигурация**: `mkdocs.yml`

```yaml
site_name: Project Documentation
site_description: Documentation for [Project Name]
site_url: https://username.github.io/project

theme:
  name: material
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - search.highlight
    - search.share
    - content.code.copy
  palette:
    - scheme: default
      primary: indigo
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - scheme: slate
      primary: indigo
      toggle:
        icon: material/brightness-4
        name: Switch to light mode

markdown_extensions:
  - admonition
  - attr_list
  - def_list
  - footnotes
  - md_in_html
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.tabbed:
      alternate_style: true
  - toc:
      permalink: true

plugins:
  - search
  - git-revision-date-localized:
      type: datetime

nav:
  - Home: index.md
  - Process:
      - Goals: process/00-goals.md
      - Process Design: process/02-process-design.md
      - Repository Structure: process/06-repository-structure.md
  - Decisions: decisions/index.md
  - PRD: prd/index.md
  - RFC: rfc/index.md
  - Ideas: ideas/index.md
  - Architecture: architecture/index.md
```

### 5.2 Автогенерация index-файлов

**Скрипт**: `scripts/generate_indexes.py`

```python
#!/usr/bin/env python3
"""Generate _index.md files for artifact directories."""

from pathlib import Path
import yaml

def extract_frontmatter(filepath):
    content = filepath.read_text(encoding='utf-8')
    import re
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError:
            return {}
    return {}

def generate_index(dir_path: Path, title: str):
    """Generate _index.md listing all artifacts in directory."""
    md_files = sorted(dir_path.glob('*.md'))
    md_files = [f for f in md_files if f.name != '_index.md']

    if not md_files:
        return

    lines = [f'# {title}\n']

    for md_file in md_files:
        fm = extract_frontmatter(md_file)
        if not fm:
            continue

        artifact_id = fm.get('id', '')
        title = fm.get('title', md_file.stem)
        status = fm.get('status', 'unknown')
        created = fm.get('created', '')

        status_icon = {
            'approved': '✅',
            'draft': '📝',
            'review': '👀',
            'rejected': '❌',
            'superseded': '⏭️',
            'archived': '📦',
            'candidate': '💭',
        }.get(status, '❓')

        rel_path = md_file.relative_to(dir_path.parent)
        lines.append(
            f'- {status_icon} [{artifact_id}: {title}]({rel_path}) '
            f'({status}, {created})'
        )

    index_path = dir_path / '_index.md'
    index_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f'Generated: {index_path}')

def main():
    root = Path(__file__).parent.parent

    dirs_to_index = [
        (root / 'docs' / 'decisions', 'Architecture Decision Records'),
        (root / 'docs' / 'prd', 'Product Requirements Documents'),
        (root / 'docs' / 'rfc', 'Request for Comments'),
        (root / 'docs' / 'ideas', 'Ideas'),
        (root / 'tasks', 'Tasks'),
    ]

    for dir_path, title in dirs_to_index:
        if dir_path.exists():
            generate_index(dir_path, title)

if __name__ == '__main__':
    main()
```

---

## 6. GitHub Actions Workflow

### 6.1 Полный пайплайн

**Файл**: `.github/workflows/docs.yml`

```yaml
name: Documentation Pipeline

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'
      - 'tasks/**'
      - 'openspec/**'
      - 'specs/**'
      - '.specify/**'
      - 'mkdocs.yml'
      - '.markdownlint-cli2.jsonc'
  pull_request:
    branches: [main]
    paths:
      - 'docs/**'
      - 'tasks/**'
      - 'openspec/**'
      - 'specs/**'

permissions:
  contents: read
  pages: write
  id-token: write

env:
  PYTHON_VERSION: '3.12'
  NODE_VERSION: '20'

jobs:
  # ═══════════════════════════════════════════════════
  # Stage 1: Lint
  # ═══════════════════════════════════════════════════
  lint:
    name: Lint Markdown & YAML
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}

      - name: Install markdownlint-cli2
        run: npm install -g markdownlint-cli2

      - name: Run markdownlint
        run: markdownlint-cli2 "docs/**/*.md" "tasks/**/*.md" "AGENTS.md" "CONSTITUTION.md"

      - name: Install yamllint
        run: pip install yamllint

      - name: Run yamllint
        run: |
          yamllint -c .yamllint.yaml mkdocs.yml
          yamllint -c .yamllint.yaml openspec/config.yaml

  # ═══════════════════════════════════════════════════
  # Stage 2: Validate
  # ═══════════════════════════════════════════════════
  validate:
    name: Validate Artifacts & Traceability
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install dependencies
        run: |
          pip install pyyaml
          npm install -g remark remark-lint-frontmatter-schema

      - name: Validate front-matter schema
        run: |
          remark --use lint-frontmatter-schema \
            --schema schemas/frontmatter.schema.json \
            "docs/decisions/*.md" "docs/prd/*.md" "docs/rfc/*.md"

      - name: Run traceability check
        run: python scripts/trace_check.py

      - name: Generate index files
        run: python scripts/generate_indexes.py

      # OpenSpec validation (if using OpenSpec)
      - name: Setup Node for OpenSpec
        if: hashFiles('openspec/config.yaml') != ''
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}

      - name: Install OpenSpec
        if: hashFiles('openspec/config.yaml') != ''
        run: npm install -g @fission-ai/openspec

      - name: Validate OpenSpec changes
        if: hashFiles('openspec/config.yaml') != ''
        run: openspec validate

  # ═══════════════════════════════════════════════════
  # Stage 3: Render Diagrams
  # ═══════════════════════════════════════════════════
  render:
    name: Render Diagrams
    runs-on: ubuntu-latest
    needs: validate
    steps:
      - uses: actions/checkout@v4

      - name: Install PlantUML
        run: |
          sudo apt-get update
          sudo apt-get install -y plantuml

      - name: Render PlantUML diagrams
        run: bash scripts/render_plantuml.sh

      - name: Upload rendered diagrams
        uses: actions/upload-artifact@v4
        with:
          name: rendered-diagrams
          path: |
            docs/**/*.svg
          retention-days: 7

  # ═══════════════════════════════════════════════════
  # Stage 4: Build Site
  # ═══════════════════════════════════════════════════
  build:
    name: Build Documentation Site
    runs-on: ubuntu-latest
    needs: [validate, render]
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install MkDocs Material
        run: |
          pip install mkdocs-material
          pip install mkdocs-git-revision-date-localized-plugin

      - name: Generate index files
        run: python scripts/generate_indexes.py

      - name: Download rendered diagrams
        uses: actions/download-artifact@v4
        with:
          name: rendered-diagrams
          path: .

      - name: Build site
        run: mkdocs build --strict

      - name: Upload site artifact
        uses: actions/upload-artifact@v4
        with:
          name: documentation-site
          path: site/
          retention-days: 7

  # ═══════════════════════════════════════════════════
  # Stage 5: Deploy (main only)
  # ═══════════════════════════════════════════════════
  deploy:
    name: Deploy to GitHub Pages
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Download site
        uses: actions/download-artifact@v4
        with:
          name: documentation-site
          path: site

      - name: Setup Pages
        uses: actions/configure-pages@v4

      - name: Upload to GitHub Pages
        uses: actions/upload-pages-artifact@v3
        with:
          path: site

      - name: Deploy
        id: deployment
        uses: actions/deploy-pages@v4
```

### 6.2 Минимальный пайплайн (для малых проектов)

```yaml
name: Docs CI

on: [push, pull_request]

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Lint
        run: |
          npm install -g markdownlint-cli2
          markdownlint-cli2 "docs/**/*.md"

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Validate
        run: |
          pip install pyyaml
          python scripts/trace_check.py

      - name: Build
        run: |
          pip install mkdocs-material
          mkdocs build --strict
```

---

## 7. Исполняемые спецификации в CI

### 7.1 Gauge (если используется)

```yaml
  test-specs:
    name: Run Executable Specifications
    runs-on: ubuntu-latest
    needs: validate
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install Gauge
        run: |
          wget https://github.com/getgauge/gauge/releases/download/v1.0.8/gauge_1.0.8_linux_64bit.deb
          sudo dpkg -i gauge_1.0.8_linux_64bit.deb

      - name: Install Gauge Python plugin
        run: gauge install python

      - name: Run Gauge specs
        run: |
          cd tests/
          gauge run specs/
```

### 7.2 Cucumber (если используется)

```yaml
  test-features:
    name: Run BDD Features
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-java@v4
        with:
          java-version: '21'
          distribution: 'temurin'

      - name: Run Cucumber
        run: |
          ./gradlew test
```

---

## 8. Метрики и отчёты

### 8.1 Собираемые метрики

| Метрика | Инструмент | Where |
|---|---|---|
| Documentation coverage | trace_check.py | Скрипт выводит статистику |
| Broken links | mkdocs build --strict | Ошибка при сборке |
| Linting violations | markdownlint-cli2 | Количество ошибок |
| Artifact counts | generate_indexes.py | Количество per тип |
| Diagram render time | CI logs | Длительность джобы |
| Site build time | CI logs | Длительность build |

### 8.2 Бейджи статуса

```markdown
# README.md

[![Docs CI](https://github.com/user/repo/actions/workflows/docs.yml/badge.svg)](https://github.com/user/repo/actions/workflows/docs.yml)
[![Documentation](https://img.shields.io/badge/docs-online-blue)](https://user.github.io/repo)
```

---

## 9. Структура CI-скриптов

```
scripts/
├── trace_check.py           # Валидация трассировки артефактов
├── generate_indexes.py      # Генерация _index.md файлов
├── render_plantuml.sh       # Рендеринг PlantUML диаграмм
├── check_plantuml.sh        # Syntax check PlantUML
└── validate_frontmatter.py  # Front-matter валидация (для pre-commit)

schemas/
└── frontmatter.schema.json  # JSON Schema для front-matter
```

---

## 10. Источники

| Ресурс | Что даёт | Ссылка |
|---|---|---|
| markdownlint-cli2 | Markdown линтер | [github.com/DavidAnson/markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2) |
| remark-lint-frontmatter-schema | Front-matter валидация | [github.com/JulianCataldo/remark-lint-frontmatter-schema](https://github.com/JulianCataldo/remark-lint-frontmatter-schema) |
| MkDocs Material Publishing | GitHub Actions workflow | [squidfunk.github.io/mkdocs-material/publishing-your-site](https://squidfunk.github.io/mkdocs-material/publishing-your-site) |
| Deploy MkDocs Action | GitHub Action для деплоя | [github.com/marketplace/actions/deploy-mkdocs](https://github.com/marketplace/actions/deploy-mkdocs) |
| OpenSpec Validate | CLI валидация спеков | [openspec.dev/docs/cli](https://openspec.dev/docs/cli) |
| Pre-commit | Управление hooks | [pre-commit.com](https://pre-commit.com) |
