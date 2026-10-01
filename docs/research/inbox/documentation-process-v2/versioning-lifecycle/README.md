# Versioning и Lifecycle

Руководство по управлению жизненным циклом артефактов документации: от создания до архивирования, включая версионирование, deprecation и supersession.

---

## Принципы управления жизненным циклом

### 1. Immutable Record
- Принятые решения (ADR, RFC) **никогда не редактируются**
- Изменения фиксируются через **supersession**
- История сохраняется для audit и обучения

### 2. Living Documentation
- Спецификации (requirements, approach) **обновляются по мере развития**
- Код и документация **эволюционируют вместе**
- Versioning через Git (commits, tags, branches)

### 3. Explicit Status
- Каждый артефакт имеет явный статус (Draft, In Review, Approved, Deprecated, Archived)
- Статус виден в metadata артефакта
- Автоматическая проверка статуса в CI

### 4. Traceability
- Связь между версиями (supersedes, deprecated by)
- Cross-references обновляются при supersession
- Migration path для устаревших артефактов

---

## Типы артефактов и их lifecycle

### Тип 1: Immutable Decisions (ADR, RFC)

**Характеристики**:
- Никогда не редактируются после approval
- Только supersede новым решением
- Постоянный historical record

**Lifecycle**:
```
Draft → In Review → Changes Requested → Approved → Superseded
                    ↘ Blocked/Discarded
```

| Статус | Описание | Разрешено изменять? |
|--------|----------|---------------------|
| **Draft** | Начальная фаза написания | ✅ Да, автор |
| **In Review** | Открыт для feedback | ✅ Да, автор |
| **Changes Requested** | Нужны изменения | ✅ Да, автор |
| **Approved** | Принято решение | ❌ Нет, только supersede |
| **Superseded** | Заменено новым ADR | ❌ Нет |
| **Rejected** | Отклонено | ❌ Нет |
| **Discarded** | Заброшено без решения | ❌ Нет |

**Пример supersession**:

```markdown
# ADR-0007: Use PostgreSQL for primary database

## Status
Superseded by [ADR-0015](./adr-0015-use-cockroachdb.md)

## Context
[original context]

## Decision
We will use PostgreSQL 15 as our primary database.

## Supersession
This decision was superseded by ADR-0015 due to:
- Need for horizontal scaling
- Multi-region requirements
- Higher availability SLAs

**Superseded on**: 2026-03-15
**Reason**: Business expansion to 5 regions
```

### Тип 2: Living Specifications (Requirements, Approach, Tasks)

**Характеристики**:
- Обновляются по мере эволюции feature
- Versioned через Git
- Могут быть deprecated когда feature retired

**Lifecycle**:
```
Draft → In Review → Approved → Active → Deprecated → Archived
```

| Статус | Описание | Разрешено изменять? |
|--------|----------|---------------------|
| **Draft** | Начальная версия | ✅ Да |
| **In Review** | Команда ревьюит | ✅ Да |
| **Approved** | Baseline established | ⚠️ Только с justification |
| **Active** | Feature в production | ⚠️ Через amendment process |
| **Deprecated** | Feature retired | ❌ Нет |
| **Archived** | Historical record | ❌ Нет |

**Пример amendment**:

```markdown
# Requirements: Data Export

- **Status**: Active
- **Version**: 2.1
- **Last amended**: 2026-03-15
- **Amendment history**:
  - v1.0 (2026-01-20): Initial version
  - v2.0 (2026-02-15): Added scheduled exports (REQ-EXP-012)
  - v2.1 (2026-03-15): Updated REQ-EXP-020 performance target

## Amendment Log

### v2.1 (2026-03-15)
**Changed**: REQ-EXP-020 performance target
**From**: "The system shall complete export within 30 seconds for < 10K records"
**To**: "The system shall complete export within 15 seconds for < 10K records"
**Reason**: Performance optimization completed, new benchmark
**Approved by**: @tech-lead
**Related**: ADR-0023 (Redis caching layer)
```

### Тип 3: Product Artifacts (PRD)

**Характеристики**:
- Living до commitment point
- Frozen после approval
- Archived когда product retired

**Lifecycle**:
```
Draft → In Review → Approved → Frozen → Archived
```

---

## Git Workflow для документации

### Branching Strategy

```
main (production)
  ↓
release/v1.2 (release branch)
  ↓
feature/data-export (feature branch)
  ├── specs/export/problem-statement.md
  ├── specs/export/requirements.md
  ├── specs/export/approach.md
  └── specs/export/tasks.md
```

### Commit Conventions

```bash
# Создание нового артефакта
git commit -m "docs(spec): add export feature problem statement

Initial problem statement for data export feature.
Addresses GDPR Article 20 compliance and enterprise customer needs."

# Обновление артефакта
git commit -m "docs(spec): update export requirements v2.1

Changes:
- REQ-EXP-020: Performance target improved to 15s (was 30s)
- Added REQ-EXP-032: New streaming requirement

Amendment approved by @tech-lead"

# Supersession ADR
git commit -m "docs(adr): supersede ADR-0007 with ADR-0015

ADR-0007 (PostgreSQL) superseded by ADR-0015 (CockroachDB).
Reason: Multi-region scaling requirements."
```

### Tagging для Releases

```bash
# Tag когда feature goes в production
git tag -a v1.2.0 -m "Release v1.2.0: Data Export Feature

Includes:
- Export feature (specs/export/)
- 5 new ADRs
- Updated architecture docs"

# Semantic versioning для документации
# MAJOR: Breaking changes в API/process
# MINOR: New features/artifacts
# PATCH: Corrections, clarifications
```

---

## Amendment Process (для Living Specifications)

### Шаг 1: Propose Amendment

```markdown
## Amendment Proposal: REQ-EXP-020

**Proposed by**: @alice
**Date**: 2026-03-10
**Document**: specs/export/requirements.md
**Current version**: v2.0

### Current Requirement
REQ-EXP-020: The system shall complete export within 30 seconds 
for datasets < 10,000 records

### Proposed Change
REQ-EXP-020: The system shall complete export within 15 seconds 
for datasets < 10,000 records

### Justification
- Performance optimization completed (ADR-0023)
- Redis caching layer added
- Benchmarks show 15s is achievable for p95
- Competitive parity with Product X

### Impact Analysis
- **Code changes**: None (already implemented)
- **Tests**: Update performance test threshold
- **Documentation**: Update approach.md Section 6.1
- **Risk**: Low (proven in staging)

### Approval Required
- [ ] Tech Lead (@bob)
- [ ] PM (@charlie)
- [ ] QA (@diana)
```

### Шаг 2: Review и Approval

**Review Checklist**:
- [ ] Justification sound
- [ ] Impact analyzed
- [ ] No breaking changes
- [ ] Stakeholders notified
- [ ] Tests updated

**Decision**: Approved / Rejected / Needs Changes

### Шаг 3: Apply Amendment

```bash
# Create amendment branch
git checkout -b amend/req-exp-020-v2.1

# Update requirements.md
# - Change version to v2.1
# - Add amendment to log
# - Update requirement

# Commit
git commit -m "docs(spec): amend REQ-EXP-020 to 15s target

Version: v2.0 → v2.1
Approved by: @bob, @charlie, @diana"

# PR и merge
git push origin amend/req-exp-020-v2.1
# Create PR, get reviews, merge
```

### Шаг 4: Update Related Artifacts

```markdown
# В approach.md Section 6.1

## Performance Considerations
- **Previous**: Complete within 30 seconds for < 10K records
- **Updated (v2.1)**: Complete within 15 seconds for < 10K records
- **How**: Redis caching layer (see ADR-0023)

## Requirements Reference
- REQ-EXP-020 (v2.1): 15 seconds target
```

---

## Supersession Pattern (для ADR/RFC)

### Полный Supersession Workflow

#### Шаг 1: Создать новый ADR

```markdown
# ADR-0015: Use CockroachDB for distributed database

## Status
Proposed

## Supersedes
[ADR-0007: Use PostgreSQL](./adr-0007-use-postgresql.md)

## Context
Since ADR-0007 (PostgreSQL decision, Jan 2026):
- Business expanded to 5 regions
- Need 99.99% availability
- PostgreSQL single-region not sufficient
- Multi-region replication required

## Decision Drivers
* Multi-region: 5 regions active
* Availability: 99.99% SLA
* Consistency: Strong consistency required
* Migration: Reasonable effort from PostgreSQL

## Considered Options
* CockroachDB
* YugabyteDB
* PostgreSQL + Citus
* Vitess (MySQL-based)

## Decision Outcome
Chosen option: "CockroachDB", because:
- PostgreSQL wire-compatible (minimal app changes)
- Built-in multi-region replication
- Strong consistency
- Active community

### Consequences
* Good: Multi-region by design
* Good: PostgreSQL compatibility
* Bad: Higher operational complexity
* Bad: 10x cost vs single PostgreSQL
* Risk: Migration effort (2-3 weeks)
```

#### Шаг 2: Update старый ADR

```markdown
# ADR-0007: Use PostgreSQL for primary database

## Status
Superseded by [ADR-0015: Use CockroachDB](./adr-0015-use-cockroachdb.md)

## Supersession Date
2026-03-15

## Supersession Reason
Business expansion to 5 regions required distributed database.
CockroachDB chosen for multi-region capabilities and PostgreSQL compatibility.

[Original content below — preserved for historical record]

---

## Context
[original context]

## Decision
[original decision]

## Consequences
[original consequences]
```

#### Шаг 3: Commit вместе

```bash
git add docs/adr/adr-0007-use-postgresql.md
git add docs/adr/adr-0015-use-cockroachdb.md
git commit -m "docs(adr): supersede ADR-0007 with ADR-0015

ADR-0007 (PostgreSQL) → ADR-0015 (CockroachDB)
Reason: Multi-region scaling requirements"
```

---

## Deprecation Patterns

### Deprecation Notification

```markdown
# Deprecation Notice: Export API v1

## Status
Deprecated

## Deprecation Date
2026-03-15

## Sunset Date
2026-06-15 (3 months notice)

## Replacement
[Export API v2](./export-api-v2/openapi.yaml)

## Migration Guide
See [Migration Guide: v1 → v2](./migration-v1-to-v2.md)

## What Changed
- Endpoint paths: `/exports` → `/v2/exports`
- Authentication: JWT → OAuth 2.0
- Response format: flat JSON → nested objects

## Why Deprecated
- Better performance in v2
- OAuth 2.0 more secure
- Aligned with company API standards (ADR-0042)

## Action Required
All consumers must migrate by 2026-06-15.
After sunset date, v1 endpoints will return 410 Gone.
```

### Deprecation Workflow

```
1. Announce deprecation (3-6 months notice)
   ↓
2. Provide migration guide
   ↓
3. Monitor usage (who hasn't migrated)
   ↓
4. Reach out to lagging consumers
   ↓
5. Sunset (disable old version)
   ↓
6. Archive documentation
```

---

## Archive Strategy

### Когда архивировать

| Триггер | Действие |
|---------|----------|
| Feature retired | Archive all related specs |
| ADR/RFC superseded | Keep but mark as superseded |
| Major version bump | Archive v1, start v2 |
| Project completed | Archive all non-active docs |
| Team dissolution | Archive to historical repo |

### Архивная структура

```
project/
├── docs/
│   ├── archive/                        # Archived documentation
│   │   ├── README.md                   # Archive index
│   │   │
│   │   ├── v1/                         # Version 1 archive
│   │   │   ├── 2025-Q4/
│   │   │   │   ├── export-feature/
│   │   │   │   └── auth-v1/
│   │   │   └── 2026-Q1/
│   │   │
│   │   └── deprecated/                 # Deprecated features
│   │       ├── legacy-export/
│   │       └── old-auth/
│   │
│   ├── adr/                            # Active ADRs
│   ├── rfc/                            # Active RFCs
│   └── architecture/                   # Active architecture
│
├── specs/                              # Active feature specs
└── src/
```

### Archive README

```markdown
# Documentation Archive

Historical documentation for retired features and past versions.

## Why Archive?
- Preserve institutional knowledge
- Audit trail for compliance
- Learning from past decisions
- Reference for similar future work

## Structure
- **v1/**: Version 1 documentation (2025-2026)
- **deprecated/**: Features retired but not versioned

## Active Documentation
For current documentation, see:
- [ADR Index](../adr/README.md)
- [RFC Index](../rfc/README.md)
- [Feature Specs](../../specs/README.md)

## Important Note
Archived documentation is **read-only** and **not maintained**.
For current information, refer to active documentation.
```

---

## Automation

### Status Validation (CI)

```yaml
# .github/workflows/validate-doc-status.yml
name: Validate Document Status

on:
  pull_request:
    paths:
      - 'docs/**'
      - 'specs/**'

jobs:
  validate-status:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check ADR status consistency
        run: |
          python scripts/validate_adr_status.py
      
      - name: Check supersession references
        run: |
          python scripts/validate_supersessions.py
      
      - name: Check amendment approvals
        run: |
          python scripts/validate_amendments.py
```

### Validation Scripts

```python
# scripts/validate_adr_status.py
import re
from pathlib import Path

def validate_adr_status():
    """Проверяет что все ADRs имеют корректный статус"""
    
    valid_statuses = {
        'Draft', 'In Review', 'Changes Requested', 
        'Approved', 'Superseded', 'Rejected', 'Discarded'
    }
    
    errors = []
    
    for adr_file in Path('docs/adr').glob('adr-*.md'):
        content = adr_file.read_text()
        
        # Извлекаем статус
        status_match = re.search(r'## Status\s*\n(.+)', content)
        if not status_match:
            errors.append(f"{adr_file}: Missing status")
            continue
        
        status_line = status_match.group(1).strip()
        
        # Проверяем валидность статуса
        if status_line not in valid_statuses:
            # Может быть "Superseded by [ADR-XXX](...)"
            if not status_line.startswith('Superseded by'):
                errors.append(f"{adr_file}: Invalid status '{status_line}'")
        
        # Проверяем что superseded ADR ссылается на существующий ADR
        if 'Superseded by' in status_line:
            ref_match = re.search(r'ADR-(\d+)', status_line)
            if ref_match:
                superseding_adr = f"adr-{ref_match.group(1).zfill(4)}"
                if not (Path('docs/adr') / f"{superseding_adr}-*.md").exists():
                    errors.append(
                        f"{adr_file}: References non-existent {superseding_adr}"
                    )
    
    if errors:
        print(f"❌ Found {len(errors)} status issues:")
        for error in errors:
            print(f"  - {error}")
        return 1
    
    print("✅ All ADR statuses valid")
    return 0

if __name__ == '__main__':
    exit(validate_adr_status())
```

```python
# scripts/validate_supersessions.py
import re
from pathlib import Path

def validate_supersessions():
    """Проверяет что все supersession ссылки корректны"""
    
    errors = []
    
    for adr_file in Path('docs/adr').glob('adr-*.md'):
        content = adr_file.read_text()
        
        # Проверяем "Supersedes" ссылки
        supersedes_matches = re.findall(
            r'Supersedes.*?ADR-(\d+)', 
            content
        )
        
        for old_adr_num in supersedes_matches:
            old_adr_pattern = f"adr-{old_adr_num.zfill(4)}-*.md"
            old_adr_files = list(Path('docs/adr').glob(old_adr_pattern))
            
            if not old_adr_files:
                errors.append(
                    f"{adr_file.name}: Supersedes non-existent ADR-{old_adr_num}"
                )
                continue
            
            # Проверяем что старый ADR помечен как superseded
            old_adr_content = old_adr_files[0].read_text()
            if 'Superseded by' not in old_adr_content:
                errors.append(
                    f"{old_adr_files[0].name}: Not marked as superseded"
                )
    
    if errors:
        print(f"❌ Found {len(errors)} supersession issues:")
        for error in errors:
            print(f"  - {error}")
        return 1
    
    print("✅ All supersession references valid")
    return 0

if __name__ == '__main__':
    exit(validate_supersessions())
```

### Deprecation Monitoring

```python
# scripts/monitor_deprecations.py
import json
from datetime import datetime, timedelta
from pathlib import Path

def find_upcoming_sunset():
    """Находит артефакты которые скоро будут sunset"""
    
    sunset_threshold = datetime.now() + timedelta(days=30)
    
    upcoming = []
    
    # Сканируем все markdown файлы
    for md_file in Path('.').rglob('*.md'):
        content = md_file.read_text()
        
        # Ищем "Sunset Date"
        sunset_match = re.search(
            r'Sunset Date[::]?\s*(\d{4}-\d{2}-\d{2})',
            content
        )
        
        if sunset_match:
            sunset_date = datetime.strptime(
                sunset_match.group(1), 
                '%Y-%m-%d'
            )
            
            if sunset_date <= sunset_threshold:
                upcoming.append({
                    'file': str(md_file),
                    'sunset_date': sunset_date.strftime('%Y-%m-%d'),
                    'days_remaining': (sunset_date - datetime.now()).days
                })
    
    return upcoming

def main():
    upcoming = find_upcoming_sunset()
    
    if upcoming:
        print(f"⚠️  {len(upcoming)} deprecations approaching sunset:")
        for item in upcoming:
            print(
                f"  - {item['file']}: "
                f"{item['days_remaining']} days until sunset "
                f"({item['sunset_date']})"
            )
        
        # Send notification to Slack/email
        send_deprecation_alert(upcoming)
        
        return 1
    
    print("✅ No deprecations approaching sunset")
    return 0

if __name__ == '__main__':
    exit(main())
```

---

## Versioning Strategy

### Documentation Versioning

#### Approach 1: Git-based (рекомендуется)

**Как работает**:
- Документация версионируется вместе с кодом
- Git tags = release versions
- Branches = parallel development

**Пример**:
```bash
# Текущая разработка
git checkout feature/new-export
# Работа с документацией в specs/export/

# Релиз
git tag v1.2.0

# Hotfix для v1.2
git checkout -b hotfix/1.2.1 v1.2.0
# Обновление документации
git tag v1.2.1

# Просмотр документации для конкретного релиза
git checkout v1.2.0
# Все docs/ в состоянии на момент релиза
```

**Плюсы**:
- Автоматически синхронизировано с кодом
- Бесплатно (использует Git)
- Полная история изменений

**Минусы**:
- Сложно для non-technical пользователей
- Нет web UI для версий

#### Approach 2: Docusaurus/MkDocs Versioning

**Как работает**:
- Documentation site с versioning
- Каждая версия доступна по URL

**Пример (Docusaurus)**:
```javascript
// docusaurus.config.js
module.exports = {
  presets: [
    ['@docusaurus/preset-classic', {
      docs: {
        versions: {
          current: { label: 'Next (v2.0)' },
          '1.2.0': { label: 'v1.2.0 (Latest)' },
          '1.1.0': { label: 'v1.1.0' },
          '1.0.0': { label: 'v1.0.0 (Archived)' },
        },
      },
    }],
  ],
};
```

**URL structure**:
- `/docs/intro` → current version
- `/docs/1.2.0/intro` → v1.2.0
- `/docs/1.1.0/intro` → v1.1.0

**Плюсы**:
- User-friendly UI
- Переключатель версий
- Поиск по конкретной версии

**Минусы**:
- Требует дополнительного tooling
- Риск рассинхронизации с кодом

#### Approach 3: Hybrid (рекомендуется для enterprise)

**Как работает**:
- Git для versioning (source of truth)
- Docusaurus/MkDocs для presentation
- Автоматическая синхронизация

**Workflow**:
```
1. Developer updates documentation в Git
   ↓
2. Git tag created (v1.2.0)
   ↓
3. CI/CD pipeline builds documentation
   ↓
4. Docusaurus version created
   ↓
5. Documentation site updated
```

### Semantic Versioning для документации

```
MAJOR.MINOR.PATCH

MAJOR: Breaking changes
- API spec changes (breaking)
- Process changes (workflow changes)
- Terminology changes

MINOR: New features
- New arтефакты
- New sections
- New patterns

PATCH: Corrections
- Typos
- Clarifications
- Examples
```

**Примеры**:
```
v1.0.0 → v1.0.1: Fixed typos in ADR template
v1.0.1 → v1.1.0: Added BDD module
v1.1.0 → v2.0.0: Migrated from MADR 3.0 to MADR 4.0
```

---

## Anti-Patterns

### ❌ Silent Edits to Approved Documents

**Проблема**: Редактирование approved ADR без supersession  
**Результат**: Потеря history, audit issues  
**Решение**: Всегда использовать supersession pattern

### ❌ Orphaned Documents

**Проблема**: Документы без metadata (status, version, date)  
**Результат**: Непонятно актуальны ли они  
**Решение**: Каждая doc имеет metadata header

### ❌ Inconsistent Status

**Проблема**: Разные status formats в разных документах  
**Результат**: Автоматизация не работает  
**Решение**: Enforce через linters и CI

### ❌ No Amendment Process

**Проблема**: Изменения вносятся без tracking  
**Результат**: Непонятно что/когда/почему изменилось  
**Решение**: Amendment log + approval process

### ❌ Broken Supersession Links

**Проблема**: ADR ссылается на несуществующий superseding ADR  
**Результат**: Broken references, confusion  
**Решение**: Автоматическая проверка в CI

### ❌ Eternal Drafts

**Проблема**: Документы годами в Draft status  
**Результат**: Unclear ownership, stale content  
**Решение**: Time-box draft phase (30 days), auto-archive

---

## Tools

### adr-tools (с lifecycle support)

```bash
# Инициализация
adr init

# Создать ADR
adr new Use PostgreSQL

# Supersede
adr new -s 1 Use CockroachDB

# List all ADRs с status
adr list

# Generate graph
adr generate graph | dot -Tpng > adr-graph.png
```

### Log4brains (с versioning)

```bash
# Инициализация
log4brains init

# Создать ADR
log4brains adr new

# Preview
log4brains preview

# Build (с versioning)
log4brains build --versions
```

### Custom Lifecycle Manager

```python
# scripts/lifecycle_manager.py
import yaml
from datetime import datetime
from pathlib import Path

class LifecycleManager:
    def __init__(self):
        self.config_file = Path('.lifecycle.yml')
        self.load_config()
    
    def load_config(self):
        """Загружает lifecycle configuration"""
        if self.config_file.exists():
            self.config = yaml.safe_load(self.config_file.read_text())
        else:
            self.config = {
                'artifacts': {
                    'adr': {
                        'mutable': False,
                        'supersession': True,
                        'statuses': ['Draft', 'In Review', 'Approved', 'Superseded']
                    },
                    'requirements': {
                        'mutable': True,
                        'amendment': True,
                        'statuses': ['Draft', 'Approved', 'Active', 'Deprecated']
                    }
                }
            }
    
    def check_mutation_allowed(self, artifact_type, status):
        """Проверяет можно ли изменять артефакт"""
        artifact_config = self.config['artifacts'].get(artifact_type, {})
        
        if not artifact_config.get('mutable', True):
            if status not in ['Draft', 'In Review', 'Changes Requested']:
                return False, f"Cannot modify {artifact_type} in {status} status"
        
        return True, "OK"
    
    def record_amendment(self, file_path, amendment):
        """Записывает amendment в log"""
        # Implementation details...
        pass
```

---

## Summary

**Versioning и Lifecycle** — это:

1. **Immutable decisions** — ADR/RFC никогда не редактируются, только supersede
2. **Living specifications** — Specs обновляются через amendment process
3. **Explicit status** — Каждый артефакт имеет явный статус
4. **Traceability** — Supersession links, amendment logs
5. **Automation** — CI checks для status, supersession, deprecation
6. **Archive strategy** — Retired features, old versions

**Ключевые workflows**:
- Supersession (для immutable)
- Amendment (для living)
- Deprecation (для retirement)
- Archive (для historical)
