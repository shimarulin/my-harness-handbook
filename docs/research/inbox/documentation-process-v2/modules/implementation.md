# Implementation

Третий и финальный модуль **Execution Flow** (Phase 2). Implementation описывает как документация связывается с кодом: как писать код на основе спецификаций, как верифицировать соответствие, как поддерживать документацию актуальной.

---

## Что такое Implementation в нашем контексте

**Implementation** — это не просто "написание кода". Это:
- **Генерация кода** на основе Approach и Tasks
- **Верификация** соответствия Requirements
- **Поддержание** документации актуальной
- **Связь** между артефактами и кодом

**Ключевой принцип**: Код — это производная от документации, не наоборот.

---

## Workflow: Документация → Код

### Полный цикл

```
Problem Statement
    ↓
Requirements (EARS)
    ↓
Approach (Technical Design)
    ↓
Tasks Breakdown
    ↓
Implementation (код)
    ↓
Verification (тесты)
    ↓
Documentation (обновление)
```

### Для каждого этапа

| Этап | Вход | Выход | Кто |
|------|------|-------|-----|
| **Coding** | Approach + Tasks | Source code | Human / AI |
| **Testing** | Requirements + Approach | Tests | Human / AI |
| **Review** | Code + Documentation | Approved PR | Human |
| **Documentation** | Code changes | Updated docs | Human / AI |

---

## Структура репозитория

### Рекомендуемая структура

```
project/
├── docs/
│   ├── adr/                          ← Architecture Decision Records
│   │   ├── README.md                 ← Index всех ADRs
│   │   ├── adr-001.md
│   │   ├── adr-002.md
│   │   └── ...
│   ├── architecture/                 ← Arc42 / C4 diagrams
│   │   ├── 01-introduction.md
│   │   ├── 02-constraints.md
│   │   ├── 03-context.md
│   │   └── ...
│   └── guides/                       ← User/developer guides
│       ├── getting-started.md
│       └── contribution.md
├── specs/                            ← Feature specifications
│   ├── feature-name/
│   │   ├── problem-statement.md      ← Problem (Phase 1)
│   │   ├── requirements.md           ← Requirements EARS (Phase 1)
│   │   ├── approach.md               ← Technical design (Phase 2)
│   │   ├── tasks.md                  ← Tasks breakdown (Phase 2)
│   │   └── adr/                      ← Feature-specific ADRs
│   │       ├── adr-001.md
│   │       └── adr-002.md
│   └── ...
├── src/                              ← Source code
│   ├── main.py
│   ├── api/
│   │   ├── exports.py
│   │   └── auth.py
│   ├── services/
│   │   ├── export_service.py
│   │   └── notification_service.py
│   └── models/
│       └── export.py
├── tests/                            ← Tests
│   ├── unit/
│   │   ├── test_export_service.py
│   │   └── test_auth.py
│   ├── integration/
│   │   └── test_export_flow.py
│   └── e2e/
│       └── test_full_export.py
├── features/                         ← BDD scenarios (optional)
│   └── export.feature
├── .github/
│   └── workflows/
│       ├── ci.yml                    ← CI pipeline
│       ├── docs-lint.yml             ← Documentation checks
│       └── requirements-check.yml    ← Requirements verification
└── README.md
```

### Альтернатива: Feature-based

```
project/
├── features/
│   ├── export/
│   │   ├── spec/
│   │   │   ├── problem-statement.md
│   │   │   ├── requirements.md
│   │   │   ├── approach.md
│   │   │   └── tasks.md
│   │   ├── adr/
│   │   │   └── adr-001-use-celery.md
│   │   ├── src/
│   │   │   ├── handler.py
│   │   │   └── service.py
│   │   └── tests/
│   │       └── test_export.py
│   └── auth/
│       ├── spec/
│       └── src/
├── docs/
│   └── adr/                          ← Cross-feature ADRs
└── README.md
```

---

## Coding на основе спецификаций

### Принцип: Requirement → Code → Test

Каждое требование должно быть:
1. **Реализовано** в коде
2. **Покрыто** тестом
3. **Прослежено** до требования

### Пример: EARS → Code

**Requirement**:
```markdown
REQ-EXP-004: When a user requests export, the system shall acknowledge 
the request within 2 seconds and return an export ID
```

**Approach reference**: Section 3.1 (API Contracts)

**Code**:
```python
# src/api/exports.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4
import time

app = FastAPI()

class ExportRequest(BaseModel):
    format: str  # csv | json
    filters: dict = {}

class ExportResponse(BaseModel):
    export_id: str
    status: str
    status_url: str

@app.post("/api/exports", response_model=ExportResponse, status_code=202)
async def create_export(request: ExportRequest) -> ExportResponse:
    """
    REQ-EXP-004: When a user requests export, the system shall acknowledge 
    the request within 2 seconds and return an export ID
    """
    start_time = time.time()
    
    # Validate format
    if request.format not in ["csv", "json"]:
        raise HTTPException(status_code=400, detail="Invalid format")
    
    # Create export record
    export_id = str(uuid4())
    
    # Enqueue task (async, non-blocking)
    await enqueue_export_task(export_id, request)
    
    # REQ-EXP-004: Respond within 2 seconds
    elapsed = time.time() - start_time
    assert elapsed < 2.0, f"Response took {elapsed}s, must be < 2s"
    
    return ExportResponse(
        export_id=export_id,
        status="pending",
        status_url=f"/api/exports/{export_id}"
    )
```

**Test**:
```python
# tests/integration/test_export_api.py

import pytest
from httpx import AsyncClient
import time

@pytest.mark.asyncio
async def test_create_export_returns_202_with_id(client: AsyncClient):
    """
    REQ-EXP-004: When a user requests export, the system shall acknowledge 
    the request within 2 seconds and return an export ID
    """
    start = time.time()
    
    response = await client.post("/api/exports", json={
        "format": "csv",
        "filters": {}
    })
    
    elapsed = time.time() - start
    
    # REQ-EXP-004: Respond within 2 seconds
    assert elapsed < 2.0
    assert response.status_code == 202
    assert "export_id" in response.json()
    assert response.json()["status"] == "pending"

@pytest.mark.asyncio
async def test_create_export_invalid_format(client: AsyncClient):
    """
    REQ-EXP-004: Unwanted behaviour - invalid format
    """
    response = await client.post("/api/exports", json={
        "format": "xml",  # Invalid
        "filters": {}
    })
    
    assert response.status_code == 400
```

### Пример: EARS → BDD → Code

**Requirement**:
```markdown
REQ-EXP-007: While the export is in progress, the system shall display 
progress percentage and estimated completion time
```

**BDD Scenario**:
```gherkin
# features/export.feature

Feature: Data Export
  Background:
    Given user "alice" is authenticated
    And alice has 100000 records

  Rule: Progress tracking while export is in progress
    # REQ-EXP-007
    
    Scenario: Export shows progress
      Given alice has requested a CSV export
      And the export is in progress
      When alice checks the export status
      Then the response contains "progress_percentage"
      And the response contains "estimated_completion_time"
      And progress_percentage is between 0 and 100
```

**Step Definitions**:
```python
# tests/steps/export_steps.py

from behave import given, when, then
import httpx

@given('alice has requested a CSV export')
def step_impl(context):
    response = httpx.post(
        f"{context.base_url}/api/exports",
        json={"format": "csv", "filters": {}},
        headers={"Authorization": f"Bearer {context.token}"}
    )
    context.export_id = response.json()["export_id"]

@when('alice checks the export status')
def step_impl(context):
    context.status_response = httpx.get(
        f"{context.base_url}/api/exports/{context.export_id}",
        headers={"Authorization": f"Bearer {context.token}"}
    )

@then('the response contains "{field}"')
def step_impl(context, field):
    assert field in context.status_response.json()
```

---

## AI-Agent Workflow для Implementation

### Pattern 1: Task-by-Task Execution

**Для**: Средние и крупные проекты

```
For each task in tasks.md:
    1. AI reads task description + acceptance criteria
    2. AI reads relevant Approach sections
    3. AI reads relevant Requirements
    4. AI generates code
    5. AI generates tests
    6. AI runs tests
    7. If tests pass → mark task complete
    8. If tests fail → iterate
    9. Human reviews
```

**Prompt для AI**:
```
Implement Task 2.3: Implement export API endpoint

Task Description:
Create POST /api/exports endpoint

Acceptance Criteria:
- Endpoint accepts format and filters
- Validates input (format must be csv/json)
- Creates export record in database
- Enqueues Celery task
- Returns 202 with export_id
- Integration tests pass

Requirements covered: REQ-EXP-004

Approach reference: Section 3.1 (API Contracts)

Dependencies completed:
- Task 1.1: Celery setup ✅
- Task 1.3: Database migration ✅

Generate:
1. Source code (src/api/exports.py)
2. Unit tests (tests/unit/test_export_api.py)
3. Integration tests (tests/integration/test_export_api.py)

Follow the API contract specified in Approach Section 3.1.
Reference requirement IDs in code comments.
```

### Pattern 2: Requirement-by-Requirement

**Для**: Small features, quick iterations

```
For each requirement:
    1. AI reads requirement
    2. AI generates code implementing requirement
    3. AI generates test verifying requirement
    4. AI runs test
    5. Human reviews
```

**Prompt для AI**:
```
Implement requirement REQ-EXP-004:
"When a user requests export, the system shall acknowledge 
the request within 2 seconds and return an export ID"

Context:
- API framework: FastAPI
- Database: PostgreSQL with SQLAlchemy
- Task queue: Celery with Redis

Generate:
1. API endpoint code
2. Test that verifies the requirement
3. Reference the requirement ID in comments
```

### Pattern 3: Approach-Driven

**Для**: Complex features, AI-agent execution

```
1. AI reads entire Approach document
2. AI generates implementation plan
3. AI implements component by component
4. AI generates comprehensive tests
5. AI verifies against Requirements
6. Human reviews
```

**Prompt для AI**:
```
Based on this Approach document, implement the complete solution:

Approach:
[paste approach.md]

Requirements:
[paste requirements.md]

Generate:
1. All source code files
2. All test files
3. Configuration files
4. README with setup instructions

Ensure:
- Every requirement is implemented
- Every requirement has at least one test
- Code follows the architecture described in Approach
- Error handling matches Approach Section 6
```

---

## Verification: Соответствие кода документации

### Уровень 1: Manual Review

**Что**: Человек читает код и сравнивает с документацией

**Checklist**:
- [ ] Все requirements реализованы?
- [ ] Архитектура соответствует Approach?
- [ ] Error handling покрывает все сценарии?
- [ ] Naming соответствует conventions?
- [ ] Comments reference requirement IDs?

### Уровень 2: Automated Checks

**Что**: CI/CD проверяет соответствие

**Примеры проверок**:

```python
# scripts/verify_requirements.py

import re
import os

def check_requirement_coverage():
    """Проверяет что все требования упомянуты в коде или тестах"""
    
    # Собираем все REQ-IDs из requirements.md
    with open("specs/export/requirements.md") as f:
        content = f.read()
    requirement_ids = set(re.findall(r'REQ-EXP-\d+', content))
    
    # Ищем упоминания в коде и тестах
    found_in_code = set()
    for root, dirs, files in os.walk("src"):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path) as f:
                    code = f.read()
                found_in_code.update(re.findall(r'REQ-EXP-\d+', code))
    
    # Ищем в тестах
    for root, dirs, files in os.walk("tests"):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path) as f:
                    code = f.read()
                found_in_code.update(re.findall(r'REQ-EXP-\d+', code))
    
    # Сравниваем
    missing = requirement_ids - found_in_code
    if missing:
        print(f"❌ Requirements not covered in code/tests: {missing}")
        return False
    else:
        print(f"✅ All {len(requirement_ids)} requirements covered")
        return True

if __name__ == "__main__":
    success = check_requirement_coverage()
    exit(0 if success else 1)
```

### Уровень 3: BDD Verification

**Что**: Исполняемые спецификации как living documentation

```bash
# Run BDD tests to verify implementation matches spec
behave features/ --tags=@REQ-EXP-004
```

### GitHub Action для верификации

```yaml
# .github/workflows/verify-requirements.yml
name: Verify Requirements Coverage

on:
  pull_request:
    paths:
      - 'src/**'
      - 'tests/**'
      - 'specs/**'

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check requirement coverage
        run: python scripts/verify_requirements.py
      
      - name: Run tests
        run: pytest tests/ -v --tb=short
      
      - name: Check BDD scenarios
        run: behave features/ --no-capture
      
      - name: Verify ADR references
        run: python scripts/check_adr_references.py
```

---

## Поддержание документации актуальной

### Правило: Код и документация меняются вместе

**Когда меняем код**:
1. Обновляем соответствующую документацию
2. Обновляем тесты
3. Обновляем ADR если решение изменилось
4. Коммитим всё в одном PR

### PR Template

```markdown
## Description
[What changed and why]

## Requirements Addressed
- REQ-EXP-004: [what was implemented]
- REQ-EXP-007: [what was implemented]

## Documentation Updated
- [ ] specs/export/approach.md
- [ ] specs/export/tasks.md
- [ ] docs/adr/adr-XXX.md (if decision changed)

## Tests
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] BDD scenarios added/updated (if applicable)

## Verification
- [ ] All tests pass
- [ ] Requirements coverage check passes
- [ ] Documentation is accurate
```

---

## Анти-паттерны

### ❌ Code Without Documentation

**Bad**: Пишем код без обновления документации
**Результат**: Документация устаревает, становится бесполезной
**Решение**: Документация и код в одном PR

---

### ❌ Documentation Without Code

**Bad**: Пишем подробную документацию, но не реализуем
**Результат**: Documentation debt, false sense of progress
**Решение**: Документация должна приводить к коду

---

### ❌ Ignoring Requirements in Code

**Bad**: Код делает что-то, но не ссылается на требования
**Результат**: Невозможно проверить соответствие
**Решение**: Комментарии с REQ-IDs, tests reference requirements

---

### ❌ AI Generates Code Without Context

**Bad**: AI пишет код без чтения Approach/Requirements
**Результат**: Код не соответствует спецификации
**Решение**: AI всегда читает документацию перед генерацией

---

### ❌ No Verification

**Bad**: Нет автоматической проверки соответствия
**Результат**: Дрейф между документацией и кодом
**Решение**: CI checks для requirements coverage

---

## Summary

**Implementation** — это финальный этап Execution Flow, где документация становится кодом. Ключевые принципы:

1. **Документация → Код**
   - Код генерируется на основе Approach и Tasks
   - Не наоборот

2. **Верификация**
   - Каждое требование имеет соответствующий код и тест
   - Автоматическая проверка соответствия

3. **Прослеживаемость**
   - Requirement → Code → Test
   - Комментарии с REQ-IDs
   - Traceability matrix

4. **AI-Friendly**
   - Чёткие инструкции из документации
   - Проверяемые результаты
   - Human review для критических решений

5. **Актуальность**
   - Документация и код меняются вместе
   - Один PR = код + документация + тесты

---

## References

- [GitHub Spec Kit](https://github.com/github/spec-kit) — `/speckit.implement`
- [Kiro](https://kiro.dev) — Implementation phase
- [OpenSpec](https://openspec.dev) — `/opsx:apply`, `/opsx:verify`
- [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) — BMad Loop
- [ForgeSDLC](https://forgesdlc.com) — Agent execution
- [Previous: Tasks](./tasks.md)
- [Back to Modules Index](./README.md)
