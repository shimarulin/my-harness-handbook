# Метрики и Dashboards

Комплексная система метрик для отслеживания эффективности процессов разработки, работы AI-агентов и предотвращения повторения ошибок.

---

## Принципы системы метрик

### 1. Измеряй то, что важно
- Метрики должны отражать **реальные проблемы**, не vanity metrics
- Каждая метрика имеет **threshold** (порог) для alerting
- Метрики **actionable** — ведут к конкретным действиям

### 2. Feedback Loop обязательно
- Данные → Анализ → Действия → Проверка эффективности
- Автоматическая обратная связь для AI-агентов
- Ручная обратная связь для критических решений

### 3. Учимся на ошибках
- Каждая ошибка документируется (ADR, postmortem)
- Patterns ошибок выявляются автоматически
- Защита от повторения через checklists и linting

### 4. Прозрачность
- Dashboards доступны всей команде
- AI-агенты видят свои метрики
- Ретроспективы на основе данных, не мнений

---

## Категории метрик

### 1. Process Metrics (метрики процесса)

Отслеживают эффективность самого процесса разработки документации.

#### 1.1 Cycle Time метрики

| Метрика | Описание | Target | Alert threshold |
|---------|----------|--------|-----------------|
| **Problem → Requirements time** | Время от формулировки проблемы до готовых требований | < 2 часа | > 4 часа |
| **Requirements → Approach time** | Время от требований до технического дизайна | < 1 день | > 2 дня |
| **Approach → Implementation time** | Время от дизайна до первого кода | < 1 день | > 3 дня |
| **Full cycle time** | Время от идеи до production | Зависит от сложности | 2x от baseline |

**Как собирать**:
```python
# .github/workflows/track-cycle-time.yml
name: Track Cycle Time

on:
  push:
    paths:
      - 'specs/**/problem-statement.md'
      - 'specs/**/requirements.md'
      - 'specs/**/approach.md'

jobs:
  track:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Calculate cycle time
        run: |
          python scripts/calculate_cycle_time.py \
            --feature ${{ github.event.head_commit.message }}

      - name: Update dashboard
        run: |
          curl -X POST ${{ secrets.DASHBOARD_WEBHOOK }} \
            -H "Content-Type: application/json" \
            -d '{"metric": "cycle_time", "value": $CYCLE_TIME}'
```

#### 1.2 Quality метрики

| Метрика | Описание | Target | Alert threshold |
|---------|----------|--------|-----------------|
| **Requirements completeness** | % требований покрытых тестами | > 95% | < 80% |
| **EARS format compliance** | % требований в правильном EARS формате | 100% | < 90% |
| **ADR coverage** | % архитектурных решений с ADR | 100% | < 80% |
| **Documentation freshness** | Средний возраст документации | < 30 дней | > 90 дней |
| **Cross-reference integrity** | % рабочих ссылок между артефактами | 100% | < 95% |

**Скрипт проверки**:
```python
# scripts/check_requirements_coverage.py
import re
import subprocess
from pathlib import Path

def get_requirements():
    """Собирает все REQ-IDs из requirements.md"""
    req_files = Path('specs').rglob('requirements.md')
    requirements = set()

    for req_file in req_files:
        content = req_file.read_text()
        req_ids = re.findall(r'REQ-\w+-\d+', content)
        requirements.update(req_ids)

    return requirements

def get_test_coverage():
    """Проверяет какие требования покрыты тестами"""
    test_files = Path('tests').rglob('*.py')
    covered = set()

    for test_file in test_files:
        content = test_file.read_text()
        req_ids = re.findall(r'REQ-\w+-\d+', content)
        covered.update(req_ids)

    return covered

def main():
    all_requirements = get_requirements()
    covered_requirements = get_test_coverage()

    coverage = len(covered_requirements) / len(all_requirements) * 100

    print(f"Requirements: {len(all_requirements)}")
    print(f"Covered: {len(covered_requirements)}")
    print(f"Coverage: {coverage:.1f}%")

    uncovered = all_requirements - covered_requirements
    if uncovered:
        print(f"\n❌ Uncovered requirements: {uncovered}")
        return 1

    if coverage < 95:
        print(f"\n⚠️  Coverage below target (95%)")
        return 1

    print(f"\n✅ All requirements covered")
    return 0

if __name__ == '__main__':
    exit(main())
```

#### 1.3 Collaboration метрики

| Метрика | Описание | Target | Alert threshold |
|---------|----------|--------|-----------------|
| **Review time** | Среднее время ревью PR с документацией | < 1 день | > 3 дня |
| **Review iterations** | Количество итераций до approval | < 2 | > 5 |
| **Comment response time** | Время ответа на комментарии | < 4 часа | > 24 часа |
| **Stale PRs** | % PR без активности > 7 дней | 0% | > 10% |

---

### 2. AI-Agent Metrics (метрики AI-агентов)

Отслеживают эффективность работы AI-агентов.

#### 2.1 Effectiveness метрики

| Метрика | Описание | Target | Alert threshold |
|---------|----------|--------|-----------------|
| **Task completion rate** | % задач завершённых агентом без human intervention | > 80% | < 60% |
| **First-time quality** | % outputs принятых без major revisions | > 70% | < 50% |
| **Context usage** | Эффективность использования context window | > 80% | < 50% или > 95% |
| **Token efficiency** | Tokens per successful task | Baseline ± 20% | 2x baseline |
| **Hallucination rate** | % outputs с фактическими ошибками | < 5% | > 15% |

**Сбор метрик**:
```python
# scripts/track_agent_metrics.py
import json
import time
from dataclasses import dataclass
from pathlib import Path

@dataclass
class AgentTask:
    task_id: str
    agent_type: str  # 'claude', 'gpt', 'codex'
    task_type: str   # 'generate_requirements', 'generate_code', etc.
    start_time: float
    end_time: float
    tokens_used: int
    output_quality: str  # 'accepted', 'minor_revision', 'major_revision', 'rejected'
    human_interventions: int
    errors: list

class AgentMetricsTracker:
    def __init__(self):
        self.metrics_file = Path('.agent_metrics/metrics.jsonl')
        self.metrics_file.parent.mkdir(exist_ok=True)

    def log_task(self, task: AgentTask):
        """Логирует завершённую задачу"""
        data = {
            'task_id': task.task_id,
            'agent_type': task.agent_type,
            'task_type': task.task_type,
            'duration': task.end_time - task.start_time,
            'tokens_used': task.tokens_used,
            'output_quality': task.output_quality,
            'human_interventions': task.human_interventions,
            'errors': task.errors,
            'timestamp': time.time()
        }

        with open(self.metrics_file, 'a') as f:
            f.write(json.dumps(data) + '\n')

    def get_agent_effectiveness(self, agent_type: str) -> dict:
        """Рассчитывает эффективность агента"""
        tasks = self._load_tasks(agent_type)

        if not tasks:
            return {}

        total = len(tasks)
        accepted = sum(1 for t in tasks if t['output_quality'] == 'accepted')
        major_revision = sum(1 for t in tasks if t['output_quality'] == 'major_revision')
        rejected = sum(1 for t in tasks if t['output_quality'] == 'rejected')

        avg_tokens = sum(t['tokens_used'] for t in tasks) / total
        avg_interventions = sum(t['human_interventions'] for t in tasks) / total

        return {
            'total_tasks': total,
            'acceptance_rate': accepted / total,
            'major_revision_rate': major_revision / total,
            'rejection_rate': rejected / total,
            'avg_tokens_per_task': avg_tokens,
            'avg_human_interventions': avg_interventions
        }

    def _load_tasks(self, agent_type: str = None):
        """Загружает задачи из лога"""
        if not self.metrics_file.exists():
            return []

        tasks = []
        with open(self.metrics_file) as f:
            for line in f:
                task = json.loads(line)
                if agent_type is None or task['agent_type'] == agent_type:
                    tasks.append(task)

        return tasks

# Использование
tracker = AgentMetricsTracker()

# После завершения задачи агентом
task = AgentTask(
    task_id='REQ-001-generation',
    agent_type='claude',
    task_type='generate_requirements',
    start_time=time.time() - 120,
    end_time=time.time(),
    tokens_used=1500,
    output_quality='accepted',
    human_interventions=0,
    errors=[]
)

tracker.log_task(task)

# Получение метрик
metrics = tracker.get_agent_effectiveness('claude')
print(f"Claude effectiveness: {metrics}")
```

#### 2.2 Deviation метрики (отклонения от цели)

| Метрика | Описание | Target | Alert threshold |
|---------|----------|--------|-----------------|
| **Scope creep** | % требований добавленных после approval | < 10% | > 30% |
| **Architecture drift** | Отклонение кода от Approach | 0 | Любое отклонение |
| **Requirements violation** | Код не соответствующий требованиям | 0 | Любое нарушение |
| **Timeline deviation** | Отклонение от planned timeline | < 20% | > 50% |

**Проверка architecture drift**:
```python
# scripts/check_architecture_compliance.py
import ast
import re
from pathlib import Path

def extract_architecture_from_approach():
    """Извлекает архитектурные решения из approach.md"""
    approach_file = Path('specs/export/approach.md')
    content = approach_file.read_text()

    # Извлекаем ключевые решения
    decisions = {
        'async_processing': 'Celery' in content,
        'storage': 'S3' in content,
        'database': 'PostgreSQL' in content,
        'streaming': 'streaming' in content.lower()
    }

    return decisions

def check_code_compliance():
    """Проверяет соответствие кода архитектуре"""
    approach = extract_architecture_from_approach()

    violations = []

    # Проверяем использование Celery
    if approach['async_processing']:
        code_files = Path('src').rglob('*.py')
        celery_used = False

        for code_file in code_files:
            content = code_file.read_text()
            if 'celery' in content.lower() or 'from celery' in content:
                celery_used = True
                break

        if not celery_used:
            violations.append({
                'type': 'missing_component',
                'expected': 'Celery for async processing',
                'location': 'src/'
            })

    # Проверяем использование S3
    if approach['storage']:
        s3_used = False
        for code_file in Path('src').rglob('*.py'):
            content = code_file.read_text()
            if 's3' in content.lower() or 'boto3' in content:
                s3_used = True
                break

        if not s3_used:
            violations.append({
                'type': 'missing_component',
                'expected': 'S3 for file storage',
                'location': 'src/'
            })

    return violations

def main():
    violations = check_code_compliance()

    if violations:
        print(f"❌ Found {len(violations)} architecture violations:")
        for v in violations:
            print(f"  - {v['type']}: {v['expected']} not found in {v['location']}")
        return 1

    print("✅ Code complies with architecture")
    return 0

if __name__ == '__main__':
    exit(main())
```

#### 2.3 Learning метрики

| Метрика | Описание | Target | Alert threshold |
|---------|----------|--------|-----------------|
| **Repeated errors** | Одинаковые ошибки у одного агента | 0 | > 2 раза |
| **Pattern recognition** | % известных patterns распознанных | > 90% | < 70% |
| **Improvement rate** | Улучшение метрик за sprint | > 5% | < 0% (ухудшение) |

---

### 3. Resource Metrics (метрики ресурсов)

#### 3.1 Time метрики

| Метрика | Описание | Target | Alert threshold |
|---------|----------|--------|-----------------|
| **Human time per task** | Время человека на задачу | Baseline ± 20% | 2x baseline |
| **AI time per task** | Время AI на задачу | Baseline ± 20% | 2x baseline |
| **Review overhead** | % времени на ревью vs реализацию | < 30% | > 50% |
| **Documentation debt** | Время на поддержку документации | < 10% dev time | > 20% dev time |

#### 3.2 Cost метрики

| Метрика | Описание | Target | Alert threshold |
|---------|----------|--------|-----------------|
| **Token cost per task** | Стоимость токенов на задачу | Baseline ± 30% | 2x baseline |
| **API calls per task** | Количество API calls | Baseline ± 20% | 2x baseline |
| **Infrastructure cost** | Стоимость CI/CD для проверок | < $100/month | > $500/month |

---

## Feedback Loops (циклы обратной связи)

### 1. Автоматическая обратная связь

#### 1.1 Real-time feedback (во время работы)

**Инструмент**: Pre-commit hooks + IDE plugins

**Пример**: EARS linter в реальном времени
```json
// .vscode/settings.json
{
  "editor.codeActionsOnSave": {
    "source.fixAll.markdownlint": true
  },
  "markdownlint.config": {
    "customRules": ["./scripts/ears-linter.js"]
  }
}
```

**Результат**: Агент/человек видит ошибки сразу при написании.

#### 1.2 Post-action feedback (после действия)

**Инструмент**: GitHub Actions + Dashboard

**Пример**: Проверка после каждого PR
```yaml
# .github/workflows/quality-gate.yml
name: Quality Gate

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check requirements coverage
        id: coverage
        run: |
          python scripts/check_requirements_coverage.py
          echo "coverage=$(cat coverage.txt)" >> $GITHUB_OUTPUT

      - name: Check architecture compliance
        id: compliance
        run: |
          python scripts/check_architecture_compliance.py
          echo "compliant=$(cat compliance.txt)" >> $GITHUB_OUTPUT

      - name: Comment on PR
        uses: actions/github-script@v7
        with:
          script: |
            const coverage = '${{ steps.coverage.outputs.coverage }}';
            const compliant = '${{ steps.compliance.outputs.compliant }}';

            let message = '## 📊 Quality Gate Results\n\n';

            if (coverage < 95) {
              message += `❌ Requirements coverage: ${coverage}% (target: 95%)\n`;
            } else {
              message += `✅ Requirements coverage: ${coverage}%\n`;
            }

            if (compliant === 'false') {
              message += `❌ Architecture compliance: FAILED\n`;
            } else {
              message += `✅ Architecture compliance: PASSED\n`;
            }

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: message
            });
```

#### 1.3 Periodic feedback (еженедельно/ежемесячно)

**Инструмент**: Automated reports + Dashboards

**Пример**: Еженедельный отчёт
```python
# scripts/generate_weekly_report.py
import json
from datetime import datetime, timedelta
from pathlib import Path

def generate_weekly_report():
    """Генерирует еженедельный отчёт по метрикам"""

    # Загружаем метрики за последнюю неделю
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    metrics = load_metrics(start_date, end_date)

    report = {
        'period': f"{start_date.date()} - {end_date.date()}",
        'summary': {
            'total_tasks': metrics['total_tasks'],
            'completion_rate': metrics['completion_rate'],
            'avg_cycle_time': metrics['avg_cycle_time'],
            'ai_effectiveness': metrics['ai_effectiveness']
        },
        'issues': [],
        'improvements': [],
        'recommendations': []
    }

    # Выявляем проблемы
    if metrics['completion_rate'] < 0.8:
        report['issues'].append({
            'type': 'low_completion_rate',
            'severity': 'high',
            'description': f"Task completion rate is {metrics['completion_rate']:.1%} (target: 80%)",
            'recommendation': 'Review task complexity and agent capabilities'
        })

    if metrics['repeated_errors'] > 2:
        report['issues'].append({
            'type': 'repeated_errors',
            'severity': 'medium',
            'description': f"{metrics['repeated_errors']} repeated errors detected",
            'recommendation': 'Create checklist or improve prompt engineering'
        })

    # Выявляем улучшения
    if metrics['improvement_rate'] > 0.05:
        report['improvements'].append({
            'type': 'process_improvement',
            'description': f"Process efficiency improved by {metrics['improvement_rate']:.1%}"
        })

    # Генерируем рекомендации
    if metrics['human_interventions'] > 3:
        report['recommendations'].append({
            'area': 'AI agent training',
            'action': 'Provide more examples or improve context'
        })

    return report

def send_report(report):
    """Отправляет отчёт команде"""

    # В Slack
    slack_webhook = os.environ['SLACK_WEBHOOK']
    requests.post(slack_webhook, json={
        'text': f"📊 Weekly Report: {report['period']}",
        'attachments': [{
            'color': 'good' if not report['issues'] else 'warning',
            'fields': [
                {'title': 'Tasks', 'value': report['summary']['total_tasks'], 'short': True},
                {'title': 'Completion', 'value': f"{report['summary']['completion_rate']:.1%}", 'short': True},
                {'title': 'Issues', 'value': len(report['issues']), 'short': True}
            ]
        }]
    })

    # В dashboard
    update_dashboard(report)

if __name__ == '__main__':
    report = generate_weekly_report()
    send_report(report)
```

### 2. Ручная обратная связь

#### 2.1 Code review comments

**Инструмент**: GitHub PR comments с структурированным форматом

**Шаблон**:
```markdown
## AI Agent Output Review

### Quality Assessment
- [ ] **Correctness**: Output meets requirements
- [ ] **Completeness**: All aspects covered
- [ ] **Clarity**: Easy to understand
- [ ] **Consistency**: Follows established patterns

### Issues Found
| Severity | Issue | Suggestion |
|----------|-------|------------|
| Critical | [description] | [how to fix] |
| Major | [description] | [how to fix] |
| Minor | [description] | [how to fix] |

### Feedback for AI Agent
- **What worked well**: [positive feedback]
- **What needs improvement**: [constructive feedback]
- **Context missing**: [what context would help]

### Action Items
- [ ] Update prompt template
- [ ] Add to examples library
- [ ] Create checklist item
```

#### 2.2 Retrospectives

**Формат**: Еженедельные/ежемесячные ретроспективы

**Структура**:
```
1. Review metrics dashboard (10 min)
2. Discuss issues and patterns (20 min)
3. Identify root causes (15 min)
4. Define action items (10 min)
5. Update processes/tools (5 min)
```

**Пример ретроспективы**:
```markdown
# Retrospective: Week 42

## Metrics Summary
- Task completion rate: 72% (target: 80%) ⚠️
- Average cycle time: 3.2 days (target: 2 days) ⚠️
- AI effectiveness: 65% (target: 70%) ⚠️
- Repeated errors: 3 ⚠️

## Issues Identified

### Issue 1: AI generates incomplete requirements
**Root cause**: Prompt doesn't emphasize checking all 5 EARS patterns
**Impact**: 4 tasks required major revision
**Action**: Update prompt template to include EARS checklist

### Issue 2: Architecture drift in implementation
**Root cause**: No automated check for architecture compliance
**Impact**: 2 PRs had to be reworked
**Action**: Add architecture compliance check to CI

### Issue 3: Review bottleneck
**Root cause**: Only 2 team members doing reviews
**Impact**: Average review time 3 days
**Action**: Train 2 more team members on review process

## Action Items
- [ ] @alice: Update EARS prompt template (by Friday)
- [ ] @bob: Add architecture compliance check (by next Monday)
- [ ] @charlie: Conduct review training session (next Wednesday)

## Improvements
- ✅ Cycle time improved 15% after implementing auto-linting
- ✅ AI acceptance rate increased 10% after adding examples
```

---

## Dashboards

### 1. Team Dashboard (общий)

**Инструмент**: Grafana / Metabase / Custom

**Метрики**:
```
┌─────────────────────────────────────────────────────────────┐
│  📊 PROCESS METRICS                                          │
├─────────────────────────────────────────────────────────────┤
│  Cycle Time: 2.3 days (target: 2 days) ✅                   │
│  Requirements Coverage: 97% (target: 95%) ✅                │
│  ADR Coverage: 100% ✅                                      │
│  Documentation Freshness: 18 days ✅                        │
├─────────────────────────────────────────────────────────────┤
│  🤖 AI AGENT METRICS                                         │
├─────────────────────────────────────────────────────────────┤
│  Task Completion: 78% (target: 80%) ⚠️                      │
│  First-time Quality: 72% (target: 70%) ✅                   │
│  Token Efficiency: 1,247 tokens/task ✅                     │
│  Human Interventions: 1.3 avg (target: <1) ⚠️               │
├─────────────────────────────────────────────────────────────┤
│  📈 TRENDS (last 4 weeks)                                   │
├─────────────────────────────────────────────────────────────┤
│  Completion Rate:    65% → 72% → 75% → 78% 📈              │
│  Cycle Time:         3.5d → 3.2d → 2.8d → 2.3d 📉          │
│  AI Effectiveness:   58% → 62% → 68% → 72% 📈              │
└─────────────────────────────────────────────────────────────┘
```

**Реализация (Grafana + Prometheus)**:
```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'process_metrics'
    static_configs:
      - targets: ['metrics-exporter:8000']

  - job_name: 'agent_metrics'
    static_configs:
      - targets: ['agent-metrics:8001']

# grafana-dashboard.json
{
  "dashboard": {
    "title": "Development Process Metrics",
    "panels": [
      {
        "title": "Task Completion Rate",
        "type": "gauge",
        "targets": [
          {
            "expr": "agent_task_completion_rate",
            "legendFormat": "{{agent_type}}"
          }
        ],
        "thresholds": [
          {"value": 60, "color": "red"},
          {"value": 80, "color": "yellow"},
          {"value": 90, "color": "green"}
        ]
      }
    ]
  }
}
```

### 2. AI Agent Dashboard (для агентов)

**Инструмент**: Custom web dashboard

**Цель**: Агенты видят свою эффективность и учатся на ошибках

**Метрики**:
```
┌─────────────────────────────────────────────────────────────┐
│  🤖 AGENT: Claude (claude-3-opus)                           │
├─────────────────────────────────────────────────────────────┤
│  PERFORMANCE (last 30 days)                                  │
│  ├─ Tasks completed: 127                                     │
│  ├─ Acceptance rate: 78% ✅                                  │
│  ├─ Avg tokens per task: 1,247 ✅                            │
│  └─ Human interventions: 1.3 avg ⚠️                          │
├─────────────────────────────────────────────────────────────┤
│  📋 TASK TYPES BREAKDOWN                                     │
│  ├─ Generate Requirements: 45 tasks (82% acceptance) ✅      │
│  ├─ Generate Approach: 32 tasks (75% acceptance) ✅          │
│  ├─ Generate Code: 38 tasks (71% acceptance) ⚠️              │
│  └─ Generate Tests: 12 tasks (83% acceptance) ✅             │
├─────────────────────────────────────────────────────────────┤
│  ⚠️  RECENT ISSUES                                           │
│  ├─ 3x: Incomplete error handling in code generation         │
│  ├─ 2x: Missing edge cases in requirements                   │
│  └─ 1x: Wrong technology choice in approach                  │
├─────────────────────────────────────────────────────────────┤
│  💡 RECOMMENDATIONS                                          │
│  ├─ Use error handling checklist for code generation          │
│  ├─ Include "edge cases" section in requirements prompts     │
│  └─ Reference ADR-XXX when choosing technologies             │
└─────────────────────────────────────────────────────────────┘
```

### 3. Error Pattern Dashboard

**Цель**: Выявление повторяющихся ошибок

**Визуализация**:
```
┌─────────────────────────────────────────────────────────────┐
│  🔍 ERROR PATTERNS (last 90 days)                           │
├─────────────────────────────────────────────────────────────┤
│  Pattern 1: Missing error handling (12 occurrences)         │
│  ├─ Agents affected: Claude (8), GPT (4)                     │
│  ├─ Task types: Code generation (10), Approach (2)           │
│  ├─ Root cause: Prompts don't emphasize error scenarios      │
│  └─ Mitigation: Added error handling checklist ✅            │
├─────────────────────────────────────────────────────────────┤
│  Pattern 2: Incomplete requirements (8 occurrences)          │
│  ├─ Agents affected: Claude (6), Codex (2)                   │
│  ├─ Task types: Requirements generation                      │
│  ├─ Root cause: Missing EARS patterns                        │
│  └─ Mitigation: Updated prompt with EARS checklist ✅        │
├─────────────────────────────────────────────────────────────┤
│  Pattern 3: Architecture drift (5 occurrences)               │
│  ├─ Agents affected: All                                     │
│  ├─ Task types: Implementation                               │
│  ├─ Root cause: No compliance check                          │
│  └─ Mitigation: Added architecture linter 🔄                 │
└─────────────────────────────────────────────────────────────┘
```

---

## Prevention Patterns (предотвращение ошибок)

### 1. Checklists

#### 1.1 Pre-generation checklist (перед генерацией)

```markdown
## AI Agent Pre-Generation Checklist

### Context
- [ ] Problem statement provided
- [ ] Requirements available (if applicable)
- [ ] Approach available (if applicable)
- [ ] Previous ADRs referenced (if applicable)

### Quality Gates
- [ ] Output format specified (Markdown, EARS, Gherkin, etc.)
- [ ] Acceptance criteria defined
- [ ] Examples provided (if applicable)
- [ ] Constraints documented

### Verification Plan
- [ ] Automated checks identified (linters, tests)
- [ ] Human review points identified
- [ ] Success metrics defined
```

#### 1.2 Post-generation checklist (после генерации)

```markdown
## AI Agent Post-Generation Checklist

### Completeness
- [ ] All requirements covered
- [ ] All edge cases addressed
- [ ] Error handling included
- [ ] Documentation updated

### Quality
- [ ] Format correct (validated by linter)
- [ ] No hallucinations (verified by human)
- [ ] Consistent with existing patterns
- [ ] Follows coding standards

### Traceability
- [ ] References to requirements (REQ-XXX)
- [ ] References to approach sections
- [ ] References to ADRs (if applicable)
- [ ] Cross-references valid

### Testing
- [ ] Unit tests written (if code)
- [ ] Integration tests written (if applicable)
- [ ] BDD scenarios written (if applicable)
- [ ] All tests passing
```

### 2. Prompt Templates

#### 2.1 Улучшенный промпт с защитой от ошибок

```markdown
## Prompt Template: Generate Requirements

### Context
You are generating EARS requirements for a software feature.

### Input
- Problem Statement: {problem_statement}
- Constraints: {constraints}
- Existing Requirements: {existing_requirements} (if any)

### Output Format
Generate requirements in EARS format with:
1. REQ-<PREFIX>-<NNN> numbering
2. Pattern type tagged [Ubiquitous/State/Event/Optional/Unwanted]
3. Specific, testable language
4. Concrete values (not "fast", but "200ms")

### Quality Checklist (MUST verify before output)
- [ ] All 5 EARS patterns considered
- [ ] Non-functional requirements included (performance, security, usability)
- [ ] Edge cases and error scenarios covered
- [ ] No vague terms ("fast", "good", "easy")
- [ ] Each requirement is atomic (one concern per requirement)
- [ ] Each requirement is testable

### Examples
[Include 2-3 examples of good requirements]

### Anti-Patterns to Avoid
- ❌ "The system should be fast" → ✅ "Response time < 200ms"
- ❌ "Handle errors gracefully" → ✅ "If DB fails, retry 3x then return 503"
- ❌ Multiple concerns in one requirement → Split into separate requirements

### Verification
After generating, self-review against checklist above.
If any item fails, regenerate that section.
```

### 3. Automated Guards

#### 3.1 Pre-commit hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: check-ears-format
        name: Check EARS format
        entry: python scripts/lint_ears.py
        language: python
        files: specs/.*requirements\.md$

      - id: check-requirements-coverage
        name: Check requirements coverage
        entry: python scripts/check_requirements_coverage.py
        language: python
        files: (specs/.*requirements\.md|tests/.*\.py)$

      - id: check-architecture-compliance
        name: Check architecture compliance
        entry: python scripts/check_architecture_compliance.py
        language: python
        files: src/.*\.py$
```

#### 3.2 CI/CD quality gates

```yaml
# .github/workflows/quality-gates.yml
name: Quality Gates

on:
  pull_request:

jobs:
  quality-gates:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Gate 1: EARS Format
        run: python scripts/lint_ears.py specs/**/requirements.md
        continue-on-error: false

      - name: Gate 2: Requirements Coverage
        run: python scripts/check_requirements_coverage.py
        continue-on-error: false

      - name: Gate 3: Architecture Compliance
        run: python scripts/check_architecture_compliance.py
        continue-on-error: false

      - name: Gate 4: Test Coverage
        run: pytest --cov=src --cov-fail-under=80
        continue-on-error: false

      - name: Gate 5: AI Agent Metrics
        run: |
          python scripts/check_agent_metrics.py
          # Fail if acceptance rate < 70%
        continue-on-error: false
```

---

## Continuous Improvement Process

### 1. Weekly Review

**Участники**: Team lead + 2 developers
**Длительность**: 30 минут
**Agenda**:
1. Review dashboard metrics (10 min)
2. Identify top 3 issues (10 min)
3. Define action items (10 min)

### 2. Monthly Retrospective

**Участники**: Вся команда
**Длительность**: 1 час
**Agenda**:
1. Metrics deep dive (20 min)
2. Root cause analysis (20 min)
3. Process improvements (15 min)
4. Tool updates (5 min)

### 3. Quarterly Planning

**Участники**: Team + stakeholders
**Длительность**: 2 часа
**Agenda**:
1. Review quarterly metrics (30 min)
2. Identify strategic improvements (45 min)
3. Plan next quarter (45 min)

---

## Инструменты для сбора метрик

### 1. Metrics Collection

| Инструмент | Назначение | Ссылка |
|-----------|-----------|--------|
| **Prometheus** | Сбор time-series метрик | [prometheus.io](https://prometheus.io) |
| **Grafana** | Визуализация dashboards | [grafana.com](https://grafana.com) |
| **Metabase** | Business intelligence | [metabase.com](https://metabase.com) |
| **Custom scripts** | Специфичные метрики | In-house |

### 2. Feedback Tools

| Инструмент | Назначение | Ссылка |
|-----------|-----------|--------|
| **GitHub Actions** | Automated checks | [github.com/features/actions](https://github.com/features/actions) |
| **Slack/Teams** | Notifications | — |
| **Retool** | Custom dashboards | [retool.com](https://retool.com) |

### 3. Analysis Tools

| Инструмент | Назначение | Ссылка |
|-----------|-----------|--------|
| **Python + Pandas** | Data analysis | — |
| **Jupyter** | Interactive analysis | [jupyter.org](https://jupyter.org) |
| **dbt** | Data transformation | [getdbt.com](https://getdbt.com) |

---

## Пример: Полный workflow с метриками

### Сценарий: AI агент генерирует требования

```
Шаг 1: Agent получает задачу
────────────────────────────
Input: Problem statement
Agent: Claude
Task: Generate EARS requirements
Start time: 10:00:00

Шаг 2: Agent генерирует черновик
─────────────────────────────────
Output: 15 requirements
Tokens used: 1,247
End time: 10:02:15
Duration: 2m 15s

Шаг 3: Автоматическая проверка
───────────────────────────────
✅ EARS format: PASS
✅ Atomicity: PASS
⚠️  Completeness: 4/5 patterns (missing Unwanted)
❌ Specificity: 2 vague terms found

Шаг 4: Feedback агенту
───────────────────────
System: "Missing Unwanted pattern. Add error handling requirements."
System: "Replace 'fast' with specific value like '200ms'."

Шаг 5: Agent итерирует
───────────────────────
Output: 18 requirements (added 3 Unwanted)
Tokens used: 847 (additional)
End time: 10:03:30

Шаг 6: Автоматическая проверка (повторная)
──────────────────────────────────────────
✅ EARS format: PASS
✅ Atomicity: PASS
✅ Completeness: 5/5 patterns
✅ Specificity: All concrete values

Шаг 7: Human review
────────────────────
Reviewer: Alice
Decision: Minor revision needed
Feedback: "Add requirement for rate limiting"
Time: 10:15:00

Шаг 8: Agent финализирует
──────────────────────────
Output: 19 requirements (added rate limiting)
Tokens used: 234 (additional)
End time: 10:16:45

Шаг 9: Human approval
─────────────────────
Reviewer: Alice
Decision: Approved
Time: 10:20:00

Шаг 10: Метрики записаны
─────────────────────────
{
  "task_id": "REQ-001-generation",
  "agent": "claude",
  "duration": "20m",
  "tokens": 2328,
  "iterations": 2,
  "human_interventions": 1,
  "quality": "accepted_after_minor_revision",
  "issues": ["incomplete_patterns", "vague_terms"],
  "timestamp": "2025-01-20T10:20:00Z"
}
```

**Анализ метрик**:
- Total time: 20 минут (target: <15 мин) ⚠️
- Tokens: 2,328 (target: <2,000) ⚠️
- Iterations: 2 (target: 1) ⚠️
- Human interventions: 1 (target: 0) ⚠️

**Root cause**: Prompt не включал checklist для всех 5 EARS patterns

**Action**: Обновить prompt template

**Ожидаемый результат**:
- Iterations: 1
- Tokens: ~1,500
- Time: ~10 минут

---

## Summary

**Метрики и Dashboards** — система для:

1. **Отслеживания эффективности** процессов и AI-агентов
2. **Выявления отклонений** от целей и стандартов
3. **Предоставления обратной связи** (автоматической и ручной)
4. **Предотвращения повторения** ошибок через checklists и guards
5. **Непрерывного улучшения** через ретроспективы

**Ключевые принципы**:
- Измеряй то, что важно
- Feedback loop обязательно
- Учимся на ошибках
- Прозрачность для всех

**Инструменты**:
- Prometheus + Grafana для метрик
- GitHub Actions для автоматических проверок
- Custom скрипты для специфичных метрик
- Dashboards для визуализации
