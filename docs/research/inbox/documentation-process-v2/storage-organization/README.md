# Хранение и организация

Полное руководство по структуре, именованию, навигации и связям между артефактами документации в репозиториях.

---

## Принципы организации

### 1. Git-Native
- Всё в репозитории (код + документация)
- Версионирование через Git
- PR-based review для документации
- Branching strategy единая для кода и документации

### 2. Discoverability
- Логичная структура, предсказуемая для новых членов команды
- Консистентные naming conventions
- Index файлы (README.md) в каждой директории
- Search-friendly

### 3. Colocation
- Документация рядом с тем, что она описывает
- Feature specs рядом с кодом фичи
- ADRs в docs/ для всего проекта
- Cross-references через относительные ссылки

### 4. Scalability
- Структура растёт вместе с проектом
- Добавление новых модулей без reorganization
- Поддержка monorepo и multi-repo

---

## Структуры репозиториев

### Вариант 1: Feature-based (для средних проектов)

```
project/
│
├── README.md                           # Project overview
├── CONTRIBUTING.md                     # How to contribute
│
├── docs/                               # Project-wide documentation
│   ├── README.md                       # Index всех docs
│   │
│   ├── prd/                            # Product Requirements Documents
│   │   ├── README.md
│   │   ├── export-feature.md
│   │   └── authentication-v2.md
│   │
│   ├── rfc/                            # Request for Comments
│   │   ├── README.md
│   │   ├── rfc-001-export-architecture.md
│   │   └── rfc-002-microservices-migration.md
│   │
│   ├── adr/                            # Architecture Decision Records
│   │   ├── README.md                   # Index всех ADR
│   │   ├── adr-0001-use-postgresql.md
│   │   ├── adr-0002-use-celery.md
│   │   └── templates/                  # ADR templates
│   │       ├── madr-full.md
│   │       └── nygard.md
│   │
│   ├── architecture/                   # Arc42 documentation
│   │   ├── README.md
│   │   ├── 01-introduction.md
│   │   ├── 02-constraints.md
│   │   ├── 03-context.md
│   │   │   ├── context.md
│   │   │   └── system-context.puml
│   │   ├── 04-solution-strategy.md
│   │   ├── 05-building-blocks.md
│   │   └── ...
│   │
│   ├── standards/                      # Coding standards, guidelines
│   │   ├── api-design.md
│   │   ├── error-handling.md
│   │   └── security.md
│   │
│   └── guides/                         # User/developer guides
│       ├── getting-started.md
│       ├── contribution.md
│       └── troubleshooting.md
│
├── specs/                              # Feature specifications
│   ├── README.md
│   │
│   ├── export/                         # Export feature
│   │   ├── README.md                   # Feature overview
│   │   ├── problem-statement.md        # Phase 1
│   │   ├── requirements.md             # Phase 1 (EARS)
│   │   ├── approach.md                 # Phase 2 (Technical design)
│   │   ├── tasks.md                    # Phase 2 (Task breakdown)
│   │   │
│   │   ├── api/                        # API specifications
│   │   │   ├── openapi.yaml
│   │   │   └── examples/
│   │   │       ├── request.json
│   │   │       └── response.json
│   │   │
│   │   └── adr/                        # Feature-specific ADRs
│   │       ├── adr-001-streaming.md
│   │       └── adr-002-s3-bucket.md
│   │
│   └── authentication/                 # Another feature
│       ├── README.md
│       ├── problem-statement.md
│       ├── requirements.md
│       ├── approach.md
│       └── tasks.md
│
├── features/                           # BDD scenarios (optional)
│   ├── README.md
│   ├── export.feature
│   ├── authentication.feature
│   └── steps/
│       ├── export_steps.py
│       └── auth_steps.py
│
├── src/                                # Source code
│   ├── README.md
│   ├── main.py
│   │
│   ├── api/
│   │   ├── README.md
│   │   ├── exports.py                  # Ссылка: ../../specs/export/requirements.md
│   │   └── auth.py
│   │
│   ├── services/
│   │   ├── README.md
│   │   ├── export_service.py
│   │   └── notification_service.py
│   │
│   └── models/
│       ├── README.md
│       └── export.py
│
├── tests/                              # Tests
│   ├── README.md
│   │
│   ├── unit/
│   │   ├── README.md
│   │   ├── test_export_service.py
│   │   └── test_auth.py
│   │
│   ├── integration/
│   │   ├── README.md
│   │   └── test_export_flow.py
│   │
│   └── e2e/
│       ├── README.md
│       └── test_full_export.py
│
├── scripts/                            # Automation scripts
│   ├── lint_ears.py
│   ├── check_requirements_coverage.py
│   └── validate_adrs.sh
│
└── .github/
    └── workflows/
        ├── ci.yml
        ├── docs-lint.yml
        └── requirements-check.yml
```

### Вариант 2: Monorepo (для нескольких сервисов)

```
monorepo/
│
├── README.md
├── CONTRIBUTING.md
│
├── docs/                               # Cross-service documentation
│   ├── README.md
│   ├── adr/                            # Cross-service ADRs
│   │   ├── README.md
│   │   ├── adr-0001-shared-database.md
│   │   └── adr-0002-event-bus.md
│   ├── rfc/
│   │   └── rfc-001-platform-strategy.md
│   └── architecture/
│       └── system-landscape.puml
│
├── services/
│   │
│   ├── export-service/                 # Export service
│   │   ├── README.md
│   │   │
│   │   ├── specs/                      # Service-specific specs
│   │   │   ├── export/
│   │   │   │   ├── requirements.md
│   │   │   │   ├── approach.md
│   │   │   │   └── tasks.md
│   │   │   └── api/
│   │   │       └── openapi.yaml
│   │   │
│   │   ├── adr/                        # Service-specific ADRs
│   │   │   ├── adr-001-use-celery.md
│   │   │   └── adr-002-s3-storage.md
│   │   │
│   │   ├── src/
│   │   ├── tests/
│   │   └── Dockerfile
│   │
│   ├── auth-service/                   # Auth service
│   │   ├── README.md
│   │   ├── specs/
│   │   ├── adr/
│   │   ├── src/
│   │   ├── tests/
│   │   └── Dockerfile
│   │
│   └── notification-service/
│       └── ...
│
├── shared/                             # Shared code
│   ├── README.md
│   ├── libraries/
│   │   ├── common/
│   │   └── utils/
│   └── proto/                          # Shared protobuf definitions
│       ├── user.proto
│       └── export.proto
│
└── infrastructure/                     # Infrastructure as code
    ├── README.md
    ├── terraform/
    └── kubernetes/
```

### Вариант 3: Multi-repo (для независимых сервисов)

```
organization/
│
├── docs/                               # Shared documentation repo
│   ├── README.md
│   ├── adr/                            # Cross-repo ADRs
│   ├── rfc/
│   ├── standards/
│   └── architecture/
│
├── export-service/                     # Export service repo
│   ├── README.md
│   ├── specs/
│   │   └── export/
│   │       ├── requirements.md
│   │       ├── approach.md
│   │       └── tasks.md
│   ├── adr/
│   ├── src/
│   └── tests/
│
├── auth-service/                       # Auth service repo
│   ├── README.md
│   ├── specs/
│   ├── adr/
│   ├── src/
│   └── tests/
│
└── frontend/                           # Frontend repo
    ├── README.md
    ├── specs/
    ├── src/
    └── tests/
```

**Cross-repo references**:
```markdown
# В export-service/specs/export/approach.md

## Dependencies
- Auth service: [Authentication API](https://github.com/org/auth-service/specs/auth/api/openapi.yaml)
- Notification service: [Email API](https://github.com/org/notification-service/specs/notification/api/openapi.yaml)
```

---

## Naming Conventions

### Файлы

| Тип файла | Формат | Пример |
|-----------|--------|--------|
| **Problem Statement** | `problem-statement.md` | `specs/export/problem-statement.md` |
| **Requirements** | `requirements.md` | `specs/export/requirements.md` |
| **Approach** | `approach.md` | `specs/export/approach.md` |
| **Tasks** | `tasks.md` | `specs/export/tasks.md` |
| **PRD** | `<feature-name>.md` | `docs/prd/export-feature.md` |
| **RFC** | `rfc-<NNN>-<title>.md` | `docs/rfc/rfc-001-export-architecture.md` |
| **ADR** | `adr-<NNNN>-<title>.md` | `docs/adr/adr-0001-use-postgresql.md` |
| **API Spec** | `openapi.yaml` / `asyncapi.yaml` | `specs/export/api/openapi.yaml` |
| **BDD** | `<feature>.feature` | `features/export.feature` |

### Правила именования

1. **Kebab-case** для всех файлов и директорий
   ```
   ✅ good: problem-statement.md
   ❌ bad: ProblemStatement.md
   ❌ bad: problem_statement.md
   ```

2. **Lowercase** для всех путей
   ```
   ✅ good: specs/export/requirements.md
   ❌ bad: Specs/Export/Requirements.md
   ```

3. **Номера с leading zeros** (для сортировки)
   ```
   ✅ good: adr-0001.md, adr-0002.md
   ❌ bad: adr-1.md, adr-2.md
   ```

4. **Descriptive names** для RFC и ADR
   ```
   ✅ good: rfc-001-export-architecture.md
   ❌ bad: rfc-001.md
   ❌ bad: rfc-export.md
   ```

5. **Consistent prefixes**
   ```
   RFC: rfc-<NNN>-<title>.md
   ADR: adr-<NNNN>-<title>.md
   PRD: <feature-name>.md (без prefix)
   ```

---

## Index Files

### Project-level README.md

```markdown
# Project Name

Краткое описание проекта (1-2 предложения).

## Quick Links

- **Getting Started**: [docs/guides/getting-started.md](docs/guides/getting-started.md)
- **Architecture**: [docs/architecture/README.md](docs/architecture/README.md)
- **API Documentation**: [specs/api/README.md](specs/api/README.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)

## Documentation

### Product
- [PRDs](docs/prd/README.md) — Product Requirements Documents
- [Roadmap](https://notion.example.com/roadmap)

### Technical
- [Architecture](docs/architecture/README.md) — C4 + Arc42
- [ADRs](docs/adr/README.md) — Architecture Decision Records
- [RFCs](docs/rfc/README.md) — Request for Comments
- [Standards](docs/standards/README.md) — Coding standards

### Features
- [Export](specs/export/README.md) — Data export feature
- [Authentication](specs/authentication/README.md) — User authentication

## Development

- [Getting Started](docs/guides/getting-started.md)
- [Contributing Guide](CONTRIBUTING.md)
- [Code Style](docs/standards/code-style.md)

## Support

- Slack: #project-name
- Email: team@example.com
```

### docs/adr/README.md (ADR Index)

```markdown
# Architecture Decision Records

Архитектурные решения проекта.

## Active Decisions

| ADR | Title | Status | Date | Deciders |
|-----|-------|--------|------|----------|
| [ADR-0001](./adr-0001-use-postgresql.md) | Use PostgreSQL for primary database | Accepted | 2025-01-10 | @alice, @bob |
| [ADR-0002](./adr-0002-use-celery.md) | Use Celery for async task processing | Accepted | 2025-01-15 | @bob, @charlie |
| [ADR-0003](./adr-0003-s3-storage.md) | Use S3 for file storage | Accepted | 2025-01-20 | @alice, @diana |
| [ADR-0004](./adr-0004-jwt-auth.md) | Use JWT for stateless authentication | Proposed | 2025-01-25 | @bob |

## Superseded Decisions

| ADR | Title | Superseded By | Date |
|-----|-------|---------------|------|
| [ADR-0000](./adr-0000-use-mongodb.md) | Use MongoDB for database | ADR-0001 | 2025-01-10 |

## How to Create a New ADR

1. Copy template: `cp templates/madr-full.md adr-<NNNN>-<title>.md`
2. Fill in all sections
3. Get review from team
4. Commit: `git commit -m "docs(adr): add ADR-<NNNN> <title>"`
5. Update this index

## Templates

- [MADR Full](./templates/madr-full.md)
- [MADR Minimal](./templates/madr-minimal.md)
- [Nygard](./templates/nygard.md)

## Tools

- [adr-tools](https://github.com/npryce/adr-tools) — CLI для управления ADR
- [Log4brains](https://github.com/thomvaill/log4brains) — ADR publishing
```

### specs/export/README.md (Feature Overview)

```markdown
# Export Feature

Data export functionality for user data.

## Status

| Phase | Status | Progress |
|-------|--------|----------|
| Problem Statement | ✅ Approved | 100% |
| Requirements | ✅ Approved | 100% |
| Approach | ✅ Approved | 100% |
| Tasks | 🔄 In Progress | 60% |
| Implementation | 🔄 In Progress | 40% |

## Documentation

### Specifications
- [Problem Statement](./problem-statement.md)
- [Requirements (EARS)](./requirements.md)
- [Technical Approach](./approach.md)
- [Task Breakdown](./tasks.md)

### API
- [OpenAPI Specification](./api/openapi.yaml)
- [API Examples](./api/examples/)

### Decisions
- [ADR-001: Use streaming for large exports](./adr/adr-001-streaming.md)
- [ADR-002: S3 bucket structure](./adr/adr-002-s3-bucket.md)

### Testing
- [BDD Scenarios](../../features/export.feature)
- [Unit Tests](../../tests/unit/test_export_service.py)
- [Integration Tests](../../tests/integration/test_export_flow.py)

## Implementation

- [Export API](../../src/api/exports.py)
- [Export Service](../../src/services/export_service.py)
- [Export Model](../../src/models/export.py)

## Timeline

| Milestone | Date | Status |
|-----------|------|--------|
| PRD Approved | Jan 15 | ✅ |
| Requirements Approved | Jan 20 | ✅ |
| Approach Approved | Jan 25 | ✅ |
| Alpha Release | Feb 15 | 🔄 |
| Beta Release | Mar 1 | ⬜ |
| GA Release | Mar 15 | ⬜ |

## Contact

- **PM**: Alice Chen
- **Tech Lead**: Bob Smith
- **Designer**: Charlie Johnson
```

---

## Cross-References

### Относительные ссылки

```markdown
# В specs/export/approach.md

## Requirements
See [requirements.md](./requirements.md) for full list.

Key requirements:
- REQ-EXP-005: Acknowledge within 2 seconds
- REQ-EXP-020: Complete within 30 seconds for <10K records

## Related ADRs
- [ADR-001: Async Processing](../../docs/adr/adr-0001-use-celery.md)
- [ADR-002: S3 Storage](../../docs/adr/adr-0002-s3-storage.md)

## Related RFCs
- [RFC-001: Export Architecture](../../docs/rfc/rfc-001-export-architecture.md)
```

### Абсолютные ссылки (для multi-repo)

```markdown
# В export-service/specs/export/approach.md

## Dependencies

### Auth Service
- [Authentication API](https://github.com/org/auth-service/specs/auth/api/openapi.yaml)
- [Auth Requirements](https://github.com/org/auth-service/specs/auth/requirements.md)

### Notification Service
- [Email API](https://github.com/org/notification-service/specs/notification/api/openapi.yaml)

### Shared Documentation
- [API Design Standards](https://github.com/org/docs/standards/api-design.md)
- [ADR-001: Use JWT](https://github.com/org/docs/adr/adr-0001-use-jwt.md)
```

### Автоматическая проверка ссылок

```python
# scripts/check_links.py
import re
import subprocess
from pathlib import Path

def check_internal_links():
    """Проверяет что все относительные ссылки валидны"""
    
    errors = []
    
    # Сканируем все markdown файлы
    for md_file in Path('.').rglob('*.md'):
        content = md_file.read_text()
        
        # Ищем markdown links [text](path)
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        
        for text, path in links:
            # Пропускаем внешние ссылки
            if path.startswith('http'):
                continue
            
            # Пропускаем anchors
            if '#' in path:
                path = path.split('#')[0]
            
            # Проверяем существование файла
            target = (md_file.parent / path).resolve()
            if not target.exists():
                errors.append(f"{md_file}: Broken link '{path}'")
    
    return errors

def main():
    errors = check_internal_links()
    
    if errors:
        print(f"❌ Found {len(errors)} broken links:")
        for error in errors:
            print(f"  - {error}")
        return 1
    
    print("✅ All internal links valid")
    return 0

if __name__ == '__main__':
    exit(main())
```

---

## Search и Discovery

### Поиск через GitHub/GitLab

**GitHub Search**:
```
# Поиск всех ADR
path:docs/adr filename:adr-*.md

# Поиск требований для конкретной фичи
path:specs/export filename:requirements.md

# Поиск RFC по статусу
path:docs/rfc "Status: Proposed"

# Поиск упоминаний технологии
"PostgreSQL" path:docs/adr
```

**GitLab Search**:
```
# Аналогично GitHub
path:docs/adr filename:adr-*.md
```

### Локальный поиск

```bash
# Поиск всех ADR
find docs/adr -name "adr-*.md" | sort

# Поиск требований по ID
grep -r "REQ-EXP-005" specs/

# Поиск упоминаний технологии
grep -r "PostgreSQL" docs/adr/

# Поиск всех feature specs
find specs -name "requirements.md"

# Поиск сломанных ссылок
./scripts/check_links.py
```

### Documentation Sites

**MkDocs** (с search plugin):
```yaml
# mkdocs.yml
site_name: Project Documentation
theme:
  name: material
  features:
    - search.suggest
    - search.highlight
    - search.share

plugins:
  - search
  - awesome-pages  # Custom navigation

nav:
  - Home: README.md
  - Architecture:
    - Overview: architecture/README.md
    - ADRs: architecture/adr/README.md
    - C4 Diagrams: architecture/c4/README.md
  - Features:
    - Export: specs/export/README.md
    - Auth: specs/auth/README.md
```

**Docusaurus** (с built-in search):
```javascript
// docusaurus.config.js
module.exports = {
  title: 'Project Documentation',
  themeConfig: {
    algolia: {
      apiKey: '...',
      indexName: 'project-docs',
    },
    navbar: {
      items: [
        { to: '/docs/architecture', label: 'Architecture' },
        { to: '/docs/features', label: 'Features' },
        { to: '/docs/adr', label: 'ADRs' },
      ],
    },
  },
};
```

---

## Организация для разных размеров проектов

### Small Project (< 3 месяца, 1-3 разработчика)

```
project/
├── README.md
├── docs/
│   ├── adr/
│   │   ├── README.md
│   │   └── adr-0001-*.md
│   └── decisions.md          # Y-Statements для мелких решений
├── spec.md                   # Один файл со всеми specs
├── src/
└── tests/
```

**Преимущества**:
- Простота
- Минимум overhead
- Быстрый старт

**Недостатки**:
- Сложно масштабировать
- Всё в одном файле

### Medium Project (3-12 месяцев, 3-10 разработчиков)

```
project/
├── README.md
├── docs/
│   ├── adr/
│   ├── rfc/
│   └── architecture/
├── specs/
│   ├── feature-1/
│   ├── feature-2/
│   └── feature-3/
├── features/                 # BDD
├── src/
└── tests/
```

**Преимущества**:
- Хорошая организация
- Feature-based структура
- Легко навигировать

**Недостатки**:
- Больше overhead
- Требует discipline

### Large Project (12+ месяцев, 10+ разработчиков)

```
project/
├── README.md
├── CONTRIBUTING.md
├── docs/
│   ├── prd/
│   ├── rfc/
│   ├── adr/
│   ├── architecture/        # Arc42
│   ├── standards/
│   └── guides/
├── specs/
│   ├── feature-1/
│   │   ├── problem-statement.md
│   │   ├── requirements.md
│   │   ├── approach.md
│   │   ├── tasks.md
│   │   ├── api/
│   │   └── adr/
│   └── ...
├── features/
├── src/
├── tests/
└── scripts/
```

**Преимущества**:
- Полная документация
- Clear separation of concerns
- Поддержка многих команд

**Недостатки**:
- Высокий overhead
- Требует processes и tooling

### Enterprise (много команд, compliance)

Используйте **Monorepo** или **Multi-repo** структуру (см. выше) + добавьте:

```
docs/
├── compliance/               # Compliance documentation
│   ├── gdpr.md
│   ├── hipaa.md
│   └── sox.md
├── audit/                    # Audit trails
│   └── ...
└── governance/               # Governance policies
    ├── adr-process.md
    └── rfc-process.md
```

---

## Tools для организации

### adr-tools

**Установка**:
```bash
brew install adr-tools
```

**Использование**:
```bash
# Инициализация
adr init docs/adr

# Создать ADR
adr new Use PostgreSQL

# Supersede
adr new -s 1 Use MySQL instead

# Generate TOC
adr generate toc > docs/adr/README.md
```

### MkDocs

**Установка**:
```bash
pip install mkdocs mkdocs-material
```

**Использование**:
```bash
# Инициализация
mkdocs new .

# Dev server
mkdocs serve

# Build
mkdocs build
```

### Documentation Linters

**markdownlint**:
```bash
npm install -g markdownlint-cli
markdownlint docs/
```

**Custom linter**:
```python
# scripts/lint_docs.py
import sys
from pathlib import Path

def check_readme_exists():
    """Проверяет что каждая директория имеет README.md"""
    errors = []
    
    for dir_path in Path('docs').rglob('*'):
        if dir_path.is_dir() and not (dir_path / 'README.md').exists():
            errors.append(f"{dir_path}: Missing README.md")
    
    return errors

def check_naming_conventions():
    """Проверяет naming conventions"""
    errors = []
    
    # Проверяем что все файлы в kebab-case
    for file_path in Path('.').rglob('*.md'):
        if '_' in file_path.name or ' ' in file_path.name:
            errors.append(f"{file_path}: Use kebab-case (no underscores or spaces)")
    
    return errors

def main():
    errors = []
    errors.extend(check_readme_exists())
    errors.extend(check_naming_conventions())
    
    if errors:
        print(f"❌ Found {len(errors)} issues:")
        for error in errors:
            print(f"  - {error}")
        return 1
    
    print("✅ Documentation structure valid")
    return 0

if __name__ == '__main__':
    exit(main())
```

---

## Anti-Patterns

### ❌ Documentation Scatter
**Проблема**: Документация разбросана по репозиторию без логики  
**Решение**: Consistent структура (docs/, specs/, features/)

### ❌ No Index Files
**Проблема**: Нет README.md в директориях  
**Решение**: Каждая директория имеет index файл

### ❌ Inconsistent Naming
**Проблема**: Разные naming conventions  
**Решение**: Enforce через linters и code review

### ❌ Broken Cross-References
**Проблема**: Ссылки на несуществующие файлы  
**Решение**: Автоматическая проверка в CI

### ❌ Monolithic Documentation
**Проблема**: Один огромный файл  
**Решение**: Split на логические модули

### ❌ Documentation Without Code
**Проблема**: Документация в отдельном репозитории  
**Решение**: Colocation (docs рядом с кодом)

---

## Summary

**Хранение и организация** — это:

1. **Структура** — предсказуемая, логичная, масштабируемая
2. **Naming** — консистентная, kebab-case, descriptive
3. **Index** — README.md в каждой директории
4. **Cross-references** — относительные ссылки, автоматическая проверка
5. **Search** — GitHub/GitLab search, MkDocs/Docusaurus
6. **Tools** — adr-tools, MkDocs, linters

**Ключевые принципы**:
- Git-native (всё в репозитории)
- Discoverability (легко найти)
- Colocation (docs рядом с кодом)
- Scalability (растёт с проектом)
