# Инструменты и автоматизация

Комплексный набор готовых OpenSource инструментов для автоматизации процессов разработки документации.

---

## Принципы выбора инструментов

### Критерии

1. **OpenSource first** — свободное ПО или open-core с полной функциональностью
2. **Открытые форматы** — Markdown, YAML, JSON, PlantUML, Mermaid
3. **Git-native** — интеграция с репозиториями
4. **CLI-first** — автоматизация через командную строку
5. **AI-friendly** — поддержка работы с AI-агентами
6. **Composable** — можно комбинировать, не монолит

### Матрица инструментов по модулям

| Модуль процесса | Инструменты | Назначение |
|----------------|------------|-----------|
| **ADR** | adr-tools, Log4brains, ADR VS Code Extension | Создание, управление, публикация |
| **Requirements (EARS)** | Custom linter, AI validation | Проверка формата, completeness |
| **Approach (Design)** | PlantUML, Mermaid, Structurizr | Диаграммы |
| **API Specs** | Stoplight, Spectral, OpenAPI Generator | Проектирование, валидация, генерация |
| **BDD** | Cucumber, Behave, Reqnroll | Исполняемые спецификации |
| **Documentation** | MkDocs, Docusaurus, Antora | Публикация документации |
| **SDD Tools** | GitHub Spec Kit, OpenSpec, BMAD-METHOD | AI-agent workflows |
| **CI/CD** | GitHub Actions, GitLab CI | Автоматизация проверок |
| **Linting** | markdownlint, yamllint, Custom scripts | Проверка форматов |

---

## Обзор инструментов

### 1. ADR Management

#### adr-tools (CLI)
**GitHub**: https://github.com/npryce/adr-tools  
**Назначение**: Управление ADR через командную строку

**Возможности**:
- Инициализация проекта
- Создание новых ADR
- Supersession (замена старых ADR)
- Генерация графа зависимостей
- Генерация TOC

**Установка**:
```bash
# macOS
brew install adr-tools

# Linux
wget https://github.com/npryce/adr-tools/archive/refs/tags/3.0.0.tar.gz
tar -xzf 3.0.0.tar.gz
sudo cp adr-tools-3.0.0/src/adr /usr/local/bin/
sudo cp -r adr-tools-3.0.0/src/* /usr/local/share/adr-tools/
```

**Использование**:
```bash
# Инициализация
adr init docs/adr

# Создать новый ADR
adr new Use PostgreSQL for database

# Supersede старый ADR
adr new -s 1 Use MySQL instead of PostgreSQL

# Генерация графа
adr generate graph | dot -Tpng > adr-graph.png

# Генерация TOC
adr generate toc > docs/adr/README.md
```

**Интеграция в процесс**:
- Автоматическое создание ADR при архитектурных решениях
- Проверка корректности supersession в CI
- Генерация визуализаций для документации

---

#### Log4brains
**GitHub**: https://github.com/thomvaill/log4brains  
**Назначение**: Публикация ADR как статический сайт

**Возможности**:
- Генерация статического сайта из ADR
- Поиск по всем ADR
- Timeline view
- Git integration
- Автоматическое обновление при commit

**Установка**:
```bash
npm install -g log4brains

# Инициализация
log4brains init

# Preview
log4brains preview

# Build
log4brains build --out ./public
```

**Интеграция в процесс**:
- Публикация ADR на GitHub Pages
- Автоматическое обновление при merge в main
- Search-friendly интерфейс для команды

---

#### ADR VS Code Extension
**Marketplace**: https://marketplace.visualstudio.com/items?itemName=jan-berger.adr-tools

**Возможности**:
- Snippets для ADR templates
- Navigation между ADR
- Link validation
- Preview диаграмм

---

### 2. Requirements Validation

#### Custom EARS Linter
**Назначение**: Проверка соответствия EARS нотации

**Реализация**: Python script

**Проверки**:
- Наличие обязательных паттернов (While/When/Where/If)
- Формат: `THE SYSTEM SHALL` или `the <system> shall`
- Атомарность требований
- Тестируемость (конкретные значения)
- Traceability (REQ-IDs)

**Пример**:
```python
# scripts/lint_ears.py
import re
import sys
from pathlib import Path

def check_ears_format(content: str, filename: str) -> list[str]:
    errors = []
    
    # Проверка паттернов
    patterns = {
        'ubiquitous': r'The \w+ shall',
        'state': r'While .+, the \w+ shall',
        'event': r'When .+, the \w+ shall',
        'optional': r'Where .+, the \w+ shall',
        'unwanted': r'If .+, then the \w+ shall'
    }
    
    for pattern_name, pattern in patterns.items():
        if not re.search(pattern, content, re.IGNORECASE):
            errors.append(f"{filename}: Missing {pattern_name} pattern")
    
    # Проверка REQ-IDs
    req_ids = re.findall(r'REQ-\w+-\d+', content)
    if not req_ids:
        errors.append(f"{filename}: No REQ-IDs found")
    
    # Проверка конкретных значений (не "быстро", а "200ms")
    vague_terms = ['быстро', 'хорошо', 'легко', 'удобно', 'fast', 'good', 'easy']
    for term in vague_terms:
        if term in content.lower():
            errors.append(f"{filename}: Vague term '{term}' found")
    
    return errors

if __name__ == '__main__':
    files = sys.argv[1:]
    all_errors = []
    
    for file_path in files:
        content = Path(file_path).read_text()
        errors = check_ears_format(content, file_path)
        all_errors.extend(errors)
    
    if all_errors:
        for error in all_errors:
            print(f"❌ {error}")
        sys.exit(1)
    else:
        print(f"✅ All {len(files)} files passed EARS validation")
        sys.exit(0)
```

**Интеграция**: GitHub Action для автоматической проверки

---

### 3. Diagram as Code

#### PlantUML
**Сайт**: https://plantuml.com  
**Назначение**: Text-based диаграммы

**Возможности**:
- UML диаграммы (sequence, class, component)
- C4 Model (через stdlib)
- Архитектурные диаграммы
- Mind maps, Gantt charts

**Установка**:
```bash
#Requires Java
brew install plantuml  # macOS
apt-get install plantuml  # Ubuntu

# VS Code extension
code --install-extension jebbs.plantuml
```

**Интеграция**:
- GitHub/GitLab native rendering
- VS Code preview
- CI: генерация PNG/SVG из .puml файлов

---

#### Mermaid
**Сайт**: https://mermaid.js.org  
**Назначение**: JavaScript-based диаграммы

**Возможности**:
- Flowcharts
- Sequence diagrams
- Gantt charts
- Class diagrams
- State diagrams

**Интеграция**:
- GitHub/GitLab native rendering (без установки)
- VS Code: `bierner.markdown-mermaid`
- Docusaurus/MkDocs plugins

**Преимущество перед PlantUML**: Не требует Java, native в GitHub

---

#### Structurizr
**Сайт**: https://structurizr.com  
**Назначение**: C4 Model с генерацией из кода

**Возможности**:
- C4 Model DSL
- Генерация диаграмм из кода
- Multiple output formats (PNG, SVG, PlantUML)
- Versioning

**Пример**:
```java
Workspace workspace = new Workspace("Export System", "Data export feature");
Model model = workspace.getModel();

Person user = model.addPerson("User", "End user");
SoftwareSystem system = model.addSoftwareSystem("Export System", "Data export");

Container api = system.addContainer("API", "FastAPI application", "Python");
Container worker = system.addContainer("Worker", "Celery worker", "Python");

user.uses(system, "Requests export");
api.uses(worker, "Enqueues tasks");
```

---

### 4. API Specifications

#### Stoplight
**Сайт**: https://stoplight.io  
**Назначение**: Visual OpenAPI editor + governance

**Возможности**:
- Visual OpenAPI editor
- Mock server
- Documentation generation
- Linting (Spectral)
- Collaboration

**Установка**:
```bash
# Stoplight Studio (desktop app)
# Download from stoplight.io/studio

# Spectral (CLI linter)
npm install -g @stoplight/spectral-cli
```

---

#### Spectral
**GitHub**: https://github.com/stoplightio/spectral  
**Назначение**: Linting для OpenAPI/AsyncAPI

**Возможности**:
- 400+ built-in rules
- Custom rules
- OpenAPI 2.0/3.x support
- AsyncAPI support
- JSON/YAML support

**Установка**:
```bash
npm install -g @stoplight/spectral-cli
```

**Использование**:
```bash
# Lint OpenAPI spec
spectral lint openapi.yaml

# Custom ruleset
spectral lint openapi.yaml --ruleset .spectral.yaml
```

**Пример .spectral.yaml**:
```yaml
extends: spectral:oas
rules:
  operation-operationId: error
  operation-description: warn
  info-contact: error
```

---

#### OpenAPI Generator
**GitHub**: https://github.com/OpenAPITools/openapi-generator  
**Назначение**: Генерация кода из OpenAPI specs

**Возможности**:
- 40+ языков (Python, JavaScript, Java, Go, etc.)
- Client SDK generation
- Server stubs generation
- Documentation generation

**Установка**:
```bash
npm install -g @openapitools/openapi-generator-cli

# Или через Docker
docker pull openapitools/openapi-generator-cli
```

**Использование**:
```bash
# Generate Python client
openapi-generator-cli generate \
  -i openapi.yaml \
  -g python \
  -o ./generated-client

# Generate FastAPI server
openapi-generator-cli generate \
  -i openapi.yaml \
  -g python-fastapi \
  -o ./server
```

---

### 5. BDD Frameworks

#### Cucumber
**Сайт**: https://cucumber.io  
**Назначение**: BDD framework (multi-language)

**Установка**:
```bash
# Java
# Add to pom.xml

# JavaScript
npm install @cucumber/cucumber

# Ruby
gem install cucumber
```

---

#### Behave (Python)
**GitHub**: https://github.com/behave/behave  
**Назначение**: BDD для Python

**Установка**:
```bash
pip install behave
```

**Использование**:
```bash
behave features/
```

---

#### Reqnroll (.NET)
**Сайт**: https://reqnroll.net  
**Назначение**: Замена SpecFlow (EOL Dec 2024)

**Установка**:
```bash
dotnet add package Reqnroll
```

---

### 6. Documentation Sites

#### MkDocs
**Сайт**: https://www.mkdocs.org  
**Назначение**: Static site generator для документации

**Установка**:
```bash
pip install mkdocs
pip install mkdocs-material  # Popular theme
```

**Использование**:
```bash
# Инициализация
mkdocs new docs-site
cd docs-site

# Dev server
mkdocs serve

# Build
mkdocs build
```

**Конфигурация mkdocs.yml**:
```yaml
site_name: Project Documentation
theme:
  name: material
  features:
    - navigation.instant
    - navigation.tracking
    - search.suggest
    - search.highlight

markdown_extensions:
  - admonition
  - codehilite
  - toc:
      permalink: true

plugins:
  - search
  - mermaid2  # Mermaid support
```

---

#### Docusaurus
**Сайт**: https://docusaurus.io  
**Назначение**: Documentation site generator от Meta

**Установка**:
```bash
npx create-docusaurus@latest docs-site
cd docs-site
npm start
```

**Преимущества**:
- React-based
- Versioning
- Blog support
- i18n

---

#### Antora
**Сайт**: https://antora.org  
**Назначение**: Multi-repository documentation

**Установка**:
```bash
npm install -g @antora/cli @antora/site-generator-default
```

**Особенности**:
- AsciiDoc format
- Multi-repo support
- Versioning
- Component-based

---

### 7. SDD Tools (Spec-Driven Development)

#### GitHub Spec Kit
**GitHub**: https://github.com/github/spec-kit  
**Назначение**: Slash commands для SDD workflow

**Возможности**:
- 38 интеграций с AI-агентами
- 4 фазы: constitution, specify, plan, tasks
- Agent-agnostic (generic integration)
- 157 community extensions

**Установка**:
```bash
npm install -g @github/spec-kit

# Инициализация
specify init --agent claude
```

**Команды**:
```bash
/speckit.constitution   # Project principles
/speckit.specify        # User stories, acceptance criteria
/speckit.plan           # Architecture, data model
/speckit.tasks          # Task breakdown
/speckit.implement      # Execute tasks
```

---

#### OpenSpec
**GitHub**: https://github.com/Fission-AI/OpenSpec  
**Назначение**: Lightweight spec framework

**Установка**:
```bash
npm install -g @fission-ai/openspec@latest
```

**Команды**:
```bash
/opsx:explore   # Understand problem
/opsx:propose   # Draft proposal
/opsx:apply     # Implement tasks
/opsx:verify    # Check implementation
/opsx:archive   # Archive completed
```

---

#### BMAD-METHOD
**GitHub**: https://github.com/bmad-code-org/BMAD-METHOD  
**Назначение**: Multi-agent development framework

**Установка**:
```bash
npx skills add bmad-code-org/BMAD-METHOD
```

**Возможности**:
- 12+ специализированных AI-агентов
- Skills-based architecture
- BMad Loop (build, verify, retro)

---

### 8. CI/CD Automation

#### GitHub Actions Workflows

**ADR Validation**:
```yaml
# .github/workflows/adr-check.yml
name: ADR Validation

on:
  pull_request:
    paths:
      - 'docs/adr/**'

jobs:
  validate-adrs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install adr-tools
        run: |
          wget https://github.com/npryce/adr-tools/archive/refs/tags/3.0.0.tar.gz
          tar -xzf 3.0.0.tar.gz
          sudo cp adr-tools-3.0.0/src/adr /usr/local/bin/
      
      - name: Check ADR format
        run: |
          for file in docs/adr/adr-*.md; do
            grep -q "## Status" "$file" || exit 1
            grep -q "## Context" "$file" || exit 1
            grep -q "## Decision" "$file" || exit 1
          done
      
      - name: Validate supersession
        run: |
          # Check that superseded ADRs reference existing ADRs
          grep -r "superseded by" docs/adr/ | while read line; do
            adr=$(echo "$line" | grep -oP 'ADR-\d+' | head -1)
            [ -f "docs/adr/${adr,,}.md" ] || exit 1
          done
```

**Requirements Validation**:
```yaml
# .github/workflows/requirements-check.yml
name: Requirements Validation

on:
  pull_request:
    paths:
      - 'specs/**/requirements.md'

jobs:
  validate-requirements:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install pyyaml
      
      - name: Validate EARS format
        run: python scripts/lint_ears.py specs/**/requirements.md
      
      - name: Check requirements coverage
        run: python scripts/check_requirements_coverage.py
```

**API Spec Validation**:
```yaml
# .github/workflows/api-spec-check.yml
name: API Spec Validation

on:
  pull_request:
    paths:
      - 'specs/api/**'

jobs:
  validate-api:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install Spectral
        run: npm install -g @stoplight/spectral-cli
      
      - name: Lint OpenAPI specs
        run: |
          for spec in specs/api/**/*.yaml; do
            spectral lint "$spec"
          done
      
      - name: Validate examples
        run: python scripts/validate_api_examples.py
```

**Documentation Build**:
```yaml
# .github/workflows/docs.yml
name: Build Documentation

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'
      - 'specs/**'

jobs:
  build-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install MkDocs
        run: |
          pip install mkdocs
          pip install mkdocs-material
          pip install mkdocs-mermaid2-plugin
      
      - name: Build documentation
        run: mkdocs build --strict
      
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./site
```

---

## Интеграция с модулями процесса

### Модуль: Problem Statement
**Инструменты**: Любой text editor, AI assistants
**Автоматизация**: Manual (творческий процесс)

### Модуль: Requirements (EARS)
**Инструменты**: Custom linter, AI validation
**Автоматизация**:
- GitHub Action: `requirements-check.yml`
- Pre-commit hook: `lint_ears.py`
- AI: генерация требований из problem statement

### Модуль: ADR
**Инструменты**: adr-tools, Log4brains, VS Code extension
**Автоматизация**:
- `adr new` для создания
- GitHub Action: проверка формата
- Log4brains: автогенерация сайта

### Модуль: Approach
**Инструменты**: PlantUML, Mermaid, Structurizr
**Автоматизация**:
- GitHub: native Mermaid rendering
- VS Code: PlantUML preview
- CI: генерация PNG из .puml

### Модуль: Tasks
**Инструменты**: Markdown, GitHub Issues
**Автоматизация**:
- GitHub Action: проверка зависимостей
- AI: генерация tasks из approach

### Модуль: Implementation
**Инструменты**: IDE, Git, CI/CD
**Автоматизация**:
- GitHub Actions: CI pipeline
- Pre-commit hooks: linting
- AI: code generation из specs

### Модуль: API Specs
**Инструменты**: Stoplight, Spectral, OpenAPI Generator
**Автоматизация**:
- Spectral: linting в CI
- OpenAPI Generator: code generation
- Mock server для testing

### Модуль: BDD
**Инструменты**: Cucumber, Behave, Reqnroll
**Автоматизация**:
- CI: запуск BDD тестов
- Living documentation generation
- AI: генерация сценариев из requirements

### Модуль: PRD
**Инструменты**: Markdown, Notion/Confluence
**Автоматизация**: Manual (product decisions)

### Модуль: RFC
**Инструменты**: Markdown, GitHub PRs
**Автоматизация**:
- PR template для RFC
- GitHub Discussions для debates
- ADR creation после approval

---

## Практические примеры

### Пример 1: Полный pipeline для фичи

```bash
# 1. Создать feature spec
mkdir specs/export
cd specs/export

# 2. Написать problem statement
nano problem-statement.md

# 3. Сгенерировать requirements (AI)
# Prompt: "Generate EARS requirements from problem-statement.md"
# Результат: requirements.md

# 4. Валидация requirements
python scripts/lint_ears.py requirements.md

# 5. Создать RFC (если нужно)
cp templates/rfc-template.md ../../docs/rfc/rfc-004-export.md

# 6. После approval RFC создать ADR
adr new Use Celery for async export processing

# 7. Написать approach
nano approach.md

# 8. Добавить диаграммы (Mermaid)
# Вставить mermaid код в approach.md

# 9. Сгенерировать tasks (AI)
# Prompt: "Generate tasks from approach.md"
# Результат: tasks.md

# 10. Создать API spec
nano api/openapi.yaml

# 11. Валидация API spec
spectral lint api/openapi.yaml

# 12. Генерация кода из API spec
openapi-generator-cli generate \
  -i api/openapi.yaml \
  -g python-fastapi \
  -o ../../src/api

# 13. Написать BDD сценарии
nano ../../features/export.feature

# 14. Реализация
# Код + тесты

# 15. Commit и PR
git add .
git commit -m "feat: implement data export"
git push origin feature/export
```

### Пример 2: GitHub Actions pipeline

```yaml
# .github/workflows/full-pipeline.yml
name: Full Documentation Pipeline

on:
  pull_request:
    paths:
      - 'specs/**'
      - 'docs/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install tools
        run: |
          pip install pyyaml
          npm install -g @stoplight/spectral-cli
      
      - name: Validate requirements (EARS)
        run: python scripts/lint_ears.py specs/**/requirements.md
      
      - name: Validate API specs
        run: spectral lint specs/api/**/*.yaml
      
      - name: Validate ADRs
        run: |
          for file in docs/adr/adr-*.md; do
            grep -q "## Status" "$file" || exit 1
          done
      
      - name: Check requirements coverage
        run: python scripts/check_requirements_coverage.py
      
      - name: Build documentation
        run: mkdocs build --strict
  
  test:
    needs: validate
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run tests
        run: pytest tests/ -v
      
      - name: Run BDD scenarios
        run: behave features/
```

---

## Матрица: Когда какой инструмент

| Ситуация | Инструмент | Альтернатива |
|----------|-----------|-------------|
| Создание ADR | adr-tools | Manual |
| Публикация ADR | Log4brains | MkDocs |
| Валидация EARS | Custom linter | Manual review |
| Диаграммы | Mermaid (GitHub native) | PlantUML |
| API spec | Stoplight + Spectral | Swagger Editor |
| Code generation | OpenAPI Generator | Manual |
| BDD (Python) | Behave | Cucumber |
| BDD (.NET) | Reqnroll | SpecFlow (EOL) |
| Documentation site | MkDocs + Material | Docusaurus |
| SDD workflow | GitHub Spec Kit | OpenSpec |
| Multi-agent | BMAD-METHOD | Custom |

---

## Next Steps

1. **Выбрать инструменты** для каждого модуля (см. матрицу выше)
2. **Настроить CI/CD** (GitHub Actions workflows)
3. **Создать templates** для каждого типа артефактов
4. **Написать документацию** для команды
5. **Протестировать** на реальном проекте
6. **Итеративно улучшать** процесс

---

## References

- [adr-tools](https://github.com/npryce/adr-tools)
- [Log4brains](https://github.com/thomvaill/log4brains)
- [Spectral](https://github.com/stoplightio/spectral)
- [OpenAPI Generator](https://github.com/OpenAPITools/openapi-generator)
- [GitHub Spec Kit](https://github.com/github/spec-kit)
- [OpenSpec](https://github.com/Fission-AI/OpenSpec)
- [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD)
- [MkDocs](https://www.mkdocs.org)
- [PlantUML](https://plantuml.com)
- [Mermaid](https://mermaid.js.org)
