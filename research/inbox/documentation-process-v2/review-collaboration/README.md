# Процессы ревью и коллаборации

Руководство по организации эффективного ревью документации, approval workflows, feedback loops и conflict resolution.

---

## Принципы ревью

### 1. Review is Collaboration, Not Gatekeeping
- Цель — улучшить документ, не заблокировать
- Конструктивный feedback, не критика
- Учимся друг у друга

### 2. Explicit Expectations
- Чёткие checklists для каждого типа артефакта
- Known reviewers и timelines
- Clear approval criteria

### 3. Async-First
- Ревью через PRs и комментарии
- Не требует synchronous meetings
- Время для глубокого анализа

### 4. Time-Boxed
- Ревью не должно drag on
- Default: 1 неделя для RFC, 2 дня для ADR
- Escalation если нет response

---

## Review Workflows

### Workflow 1: Lightweight Review (для small changes)

**Для**: Bug fixes, minor clarifications, typos

**Process**:
```
1. Author создает PR
   ↓
2. Self-review (checklist)
   ↓
3. Assign 1 reviewer
   ↓
4. Reviewer approves или requests changes
   ↓
5. Merge (если approved)
```

**Timeline**: 1-2 дня

**Approvers**: Любой team member

### Workflow 2: Standard Review (для most artifacts)

**Для**: Requirements, Approach, Tasks, ADR

**Process**:
```
1. Author создает PR с полной документацией
   ↓
2. Self-review (checklist)
   ↓
3. Assign 2 reviewers (1 domain expert + 1 peer)
   ↓
4. Reviewers предоставляют feedback (inline comments)
   ↓
5. Author addresses feedback
   ↓
6. Re-review (если needed)
   ↓
7. Approval (2 approvals required)
   ↓
8. Merge
```

**Timeline**: 2-5 дней

**Approvers**: 
- Domain expert (architect, tech lead)
- Peer reviewer (fellow developer)

### Workflow 3: Formal Review (для major decisions)

**Для**: RFC, PRD, major architectural changes

**Process**:
```
1. Author создает PR + announces в team channel
   ↓
2. Self-review (checklist)
   ↓
3. Assign 3+ reviewers (diverse perspectives)
   ↓
4. Review period (1 week default)
   ↓
5. Review meeting (если needed для discussion)
   ↓
6. Author addresses feedback
   ↓
7. Final review
   ↓
8. Approval (consensus or designated approver)
   ↓
9. Merge + announce decision
```

**Timeline**: 1-2 недели

**Approvers**:
- Tech Lead / Architect
- PM (для PRD)
- Security representative (если applicable)
- Affected team representatives

### Workflow 4: Architecture Review Board (для enterprise)

**Для**: Cross-team impact, compliance-related, major investments

**Process**:
```
1. Submit RFC/ADR to ARB queue
   ↓
2. Preliminary review (ARB members, 1 week)
   ↓
3. ARB meeting (presentation + Q&A, 30-60 min)
   ↓
4. ARB decision:
   - Approved
   - Approved with conditions
   - Changes requested
   - Rejected
   ↓
5. If approved: implementation
   ↓
6. Post-implementation review (3 months later)
```

**Timeline**: 2-4 недели

**Approvers**: Architecture Review Board (5-7 members)

---

## Review Checklists

### Problem Statement Review Checklist

```markdown
## Problem Statement Review

### Clarity (10 points)
- [ ] Problem clearly defined (3 pts)
- [ ] Root cause identified (3 pts)
- [ ] No solution included (2 pts)
- [ ] Concise (1-3 paragraphs) (2 pts)

### Evidence (10 points)
- [ ] Quantified impact (4 pts)
- [ ] User/business pain explained (3 pts)
- [ ] Data/sources cited (3 pts)

### Specificity (10 points)
- [ ] Success criteria measurable (4 pts)
- [ ] Scope clearly defined (3 pts)
- [ ] Non-goals stated (3 pts)

### Completeness (10 points)
- [ ] Who is affected (3 pts)
- [ ] Why now (3 pts)
- [ ] Cost of inaction (4 pts)

**Total**: ___/40 points
**Decision**: Approve (≥30) / Changes Needed (<30)
```

### Requirements (EARS) Review Checklist

```markdown
## Requirements Review

### EARS Format (20 points)
- [ ] All 5 patterns considered (5 pts)
- [ ] Correct syntax for each pattern (5 pts)
- [ ] System name consistent (5 pts)
- [ ] "shall" used consistently (5 pts)

### Quality (20 points)
- [ ] Specific and testable (5 pts)
- [ ] Atomic (one concern per requirement) (5 pts)
- [ ] No vague terms (5 pts)
- [ ] Traceable to problem (5 pts)

### Completeness (20 points)
- [ ] Functional requirements covered (5 pts)
- [ ] Non-functional requirements covered (5 pts)
- [ ] Error handling (Unwanted pattern) (5 pts)
- [ ] Edge cases considered (5 pts)

### Traceability (20 points)
- [ ] REQ-IDs used consistently (5 pts)
- [ ] Linked to Problem Statement (5 pts)
- [ ] Can be traced to tests (5 pts)
- [ ] Can be traced to code (5 pts)

### Organization (20 points)
- [ ] Logical grouping (5 pts)
- [ ] No duplicates (5 pts)
- [ ] Prioritized (5 pts)
- [ ] Clear naming (5 pts)

**Total**: ___/100 points
**Decision**: Approve (≥80) / Changes Needed (<80)
```

### ADR Review Checklist

```markdown
## ADR Review

### Context (20 points)
- [ ] Problem clearly stated (5 pts)
- [ ] Forces/drivers identified (5 pts)
- [ ] Background sufficient (5 pts)
- [ ] Scope clear (5 pts)

### Decision (20 points)
- [ ] Decision clearly stated (5 pts)
- [ ] Justification provided (5 pts)
- [ ] Active voice used (5 pts)
- [ ] Specific (not vague) (5 pts)

### Alternatives (20 points)
- [ ] At least 2 alternatives considered (5 pts)
- [ ] Fair evaluation of each (5 pts)
- [ ] "Do nothing" considered (5 pts)
- [ ] Reasons for rejection clear (5 pts)

### Consequences (20 points)
- [ ] Positive consequences listed (5 pts)
- [ ] Negative consequences listed (5 pts)
- [ ] Risks identified (5 pts)
- [ ] Honest assessment (5 pts)

### Quality (20 points)
- [ ] Concise (1-2 pages) (5 pts)
- [ ] Well-organized (5 pts)
- [ ] No jargon (5 pts)
- [ ] Actionable (5 pts)

**Total**: ___/100 points
**Decision**: Approve (≥80) / Changes Needed (<80)
```

### RFC Review Checklist

```markdown
## RFC Review

### Problem Definition (20 points)
- [ ] Problem clearly stated (5 pts)
- [ ] Impact quantified (5 pts)
- [ ] Motivation clear (5 pts)
- [ ] Scope defined (5 pts)

### Proposal (20 points)
- [ ] Solution clearly described (5 pts)
- [ ] Architecture diagrams (5 pts)
- [ ] Technical details sufficient (5 pts)
- [ ] Feasible (5 pts)

### Alternatives (20 points)
- [ ] At least 3 alternatives (5 pts)
- [ ] Fair evaluation (5 pts)
- [ ] "Do nothing" included (5 pts)
- [ ] Clear rejection reasons (5 pts)

### Trade-offs (20 points)
- [ ] Trade-offs identified (5 pts)
- [ ] Risks assessed (5 pts)
- [ ] Mitigations proposed (5 pts)
- [ ] Honest about downsides (5 pts)

### Implementation (20 points)
- [ ] Migration plan (5 pts)
- [ ] Timeline realistic (5 pts)
- [ ] Resource estimate (5 pts)
- [ ] Success metrics (5 pts)

**Total**: ___/100 points
**Decision**: 
- Approve (≥85)
- Approve with conditions (70-84)
- Changes needed (<70)
```

### Approach (Technical Design) Review Checklist

```markdown
## Approach Review

### Completeness (25 points)
- [ ] All requirements covered (10 pts)
- [ ] Architecture complete (5 pts)
- [ ] Data flow clear (5 pts)
- [ ] Error handling covered (5 pts)

### Technical Soundness (25 points)
- [ ] Architecture sound (10 pts)
- [ ] Scalability considered (5 pts)
- [ ] Performance addressed (5 pts)
- [ ] Security considered (5 pts)

### Feasibility (25 points)
- [ ] Technically feasible (10 pts)
- [ ] Resource estimate realistic (5 pts)
- [ ] Timeline realistic (5 pts)
- [ ] Risks identified (5 pts)

### Clarity (25 points)
- [ ] Well-organized (10 pts)
- [ ] Diagrams clear (5 pts)
- [ ] Examples provided (5 pts)
- [ ] No ambiguity (5 pts)

**Total**: ___/100 points
**Decision**: Approve (≥80) / Changes Needed (<80)
```

---

## Providing Effective Feedback

### Feedback Framework

#### SBI Model (Situation-Behavior-Impact)

```markdown
**Situation**: В section "Error Handling"
**Behavior**: Описан только happy path, нет error scenarios
**Impact**: Implementers не будут знать как handle failures, 
            что приведёт к production issues

**Suggestion**: Добавить Unwanted requirements (If/Then) для:
- Database connection failures
- S3 upload timeouts
- Email service unavailable
```

#### Specific vs Vague

```markdown
❌ Vague: "This section needs work"
✅ Specific: "Section 3.2 lacks concrete values. 
             Replace 'fast' with '200ms p95 latency'"

❌ Vague: "Bad example"
✅ Specific: "Example in Section 4 uses synchronous processing, 
             but ADR-001 specifies async (Celery). 
             Update to match architecture decision."

❌ Vague: "Too long"
✅ Specific: "Section 5 is 3 pages. Consider splitting into:
             - 5.1: Happy path (1 page)
             - 5.2: Error paths (1 page)
             - 5.3: Edge cases (1 page)"
```

### Comment Etiquette

#### Do's

```markdown
✅ Be specific and actionable
✅ Provide examples when helpful
✅ Explain the "why" behind feedback
✅ Acknowledge good parts
✅ Ask questions if unclear
✅ Suggest alternatives
```

#### Don'ts

```markdown
❌ Nitpick style (use linters for that)
❌ Be vague ("this is wrong")
❌ Make it personal ("you should...")
❌ Demand changes without explanation
❌ Block on minor issues
❌ Rewrite instead of suggest
```

### Example: Good vs Bad Feedback

#### Bad Feedback

```markdown
This is wrong. Fix it.
```

**Problems**:
- Не specific
- Не actionable
- Не constructive

#### Good Feedback

```markdown
**Issue**: REQ-EXP-005 uses vague language

**Current**:
"When user requests export, system should be fast"

**Problem**:
"Fast" is not testable. How fast is fast enough?

**Suggestion**:
"When user requests export, system shall acknowledge 
within 2 seconds and return export ID"

**Why**:
- Specific (2 seconds)
- Testable (can measure response time)
- Aligns with REQ-EXP-020 performance requirement

**Example test**:
```python
def test_export_acknowledgment_speed():
    start = time.time()
    response = client.post('/exports', {...})
    elapsed = time.time() - start
    
    assert elapsed < 2.0
    assert response.status_code == 202
```
```

---

## Approval Workflows

### Pattern 1: Unanimous Consent

**Когда использовать**: Critical decisions, cross-team impact

**Process**:
```
Все назначенные reviewers должны approve.
Если один rejects → changes needed.
```

**Pros**:
- High quality bar
- Full consensus

**Cons**:
- Slow
- One person can block

**Use for**: RFC, major ADR, PRD

### Pattern 2: Majority Vote

**Когда использовать**: Time-sensitive decisions, good enough solutions

**Process**:
```
2 из 3 reviewers must approve.
Dissenting opinion documented.
```

**Pros**:
- Faster than unanimous
- Prevents blocking

**Cons**:
- May miss important concerns

**Use for**: Standard ADR, Approach

### Pattern 3: Designated Approver

**Когда использовать**: Clear ownership, domain expertise required

**Process**:
```
Один designated approver (tech lead, architect).
Others provide feedback, но не block.
```

**Pros**:
- Fast
- Clear accountability

**Cons**:
- Bottleneck on one person
- May miss perspectives

**Use for**: Requirements, Tasks, minor changes

### Pattern 4: Lazy Consensus

**Когда использовать**: Low-risk changes, well-established patterns

**Process**:
```
PR открыт для N дней (default: 3).
Если нет objections → auto-approve.
```

**Pros**:
- Very fast
- Reduces review burden

**Cons**:
- May miss issues
- Requires trust

**Use for**: Typos, clarifications, examples

---

## Conflict Resolution

### Types of Conflicts

#### 1. Technical Disagreement

**Example**: 
- Person A: "Use PostgreSQL"
- Person B: "Use MongoDB"

**Resolution Process**:
```
1. Each side presents evidence (10 min each)
   ↓
2. Identify decision criteria (5 min)
   ↓
3. Evaluate options against criteria (15 min)
   ↓
4. Decision:
   - Consensus reached
   - Escalate to architect/tech lead
   - Prototype both (time-boxed)
```

#### 2. Scope Disagreement

**Example**:
- PM: "Include feature X in v1"
- Engineer: "Feature X should be v2"

**Resolution Process**:
```
1. Identify constraints (time, resources)
   ↓
2. Evaluate impact of including vs deferring
   ↓
3. Decision criteria:
   - Customer impact
   - Technical risk
   - Business value
   ↓
4. Decision by PM (product owner)
```

#### 3. Priority Disagreement

**Example**:
- Team A: "Our feature is priority #1"
- Team B: "Our feature is priority #1"

**Resolution Process**:
```
1. Each team presents business case (10 min each)
   ↓
2. Evaluate against strategic objectives
   ↓
3. Decision by:
   - Product leadership (if product conflict)
   - Engineering leadership (if technical conflict)
   - Executive sponsor (if strategic conflict)
```

### Escalation Path

```
Level 1: Direct discussion (author + reviewer)
    ↓ (не resolved за 24h)
Level 2: Tech Lead / Team Lead
    ↓ (не resolved за 48h)
Level 3: Engineering Manager / Director
    ↓ (не resolved за 1 week)
Level 4: VP Engineering / CTO
```

### Decision Documentation

Когда conflict resolved, **задокументировать решение**:

```markdown
# Decision: Database Choice

## Context
Disagreement between PostgreSQL (Alice) and MongoDB (Bob)

## Decision Criteria
1. Query performance (complex JOINs)
2. Schema flexibility
3. Team expertise
4. Operational complexity

## Evaluation

### PostgreSQL
- Query performance: ⭐⭐⭐⭐⭐ (excellent JOINs)
- Schema flexibility: ⭐⭐⭐ (fixed schema)
- Team expertise: ⭐⭐⭐⭐ (3 years experience)
- Operational complexity: ⭐⭐⭐⭐ (familiar)

### MongoDB
- Query performance: ⭐⭐ (poor JOINs)
- Schema flexibility: ⭐⭐⭐⭐⭐ (very flexible)
- Team expertise: ⭐⭐ (6 months)
- Operational complexity: ⭐⭐⭐ (learning curve)

## Decision
**PostgreSQL** chosen because:
- Query performance critical for our use case
- Team has more experience
- Lower operational risk

## Dissenting Opinion (Bob)
"MongoDB would be better if schema flexibility becomes critical.
Revisit if requirements change significantly."

## Decided By
Tech Lead (Charlie), 2026-03-15
```

---

## Time Management

### Review SLAs

| Artifact Type | Max Review Time | Escalation |
|---------------|----------------|------------|
| **Problem Statement** | 2 days | Tech Lead |
| **Requirements** | 3 days | Tech Lead |
| **ADR** | 2 days | Architect |
| **RFC** | 1 week | Engineering Manager |
| **PRD** | 1 week | Product Director |
| **Approach** | 3 days | Tech Lead |
| **Tasks** | 2 days | Tech Lead |

### Avoiding Review Bottlenecks

#### Problem: Too Many Reviews, Too Few Reviewers

**Solutions**:
```
1. Expand reviewer pool
   - Train more people to review
   - Rotate reviewers
   - Cross-team reviewers

2. Reduce review burden
   - Use lazy consensus for low-risk
   - Automate what can be automated
   - Batch similar reviews

3. Prioritize reviews
   - Critical path first
   - Time-sensitive first
   - High-impact first
```

#### Problem: Reviews Taking Too Long

**Solutions**:
```
1. Time-box reviews
   - Set max review time
   - Auto-approve if no response
   - Escalate if blocked

2. Improve review quality
   - Better checklists
   - Clearer artifacts
   - Smaller PRs

3. Parallel reviews
   - Assign multiple reviewers
   - First 2 approvals sufficient
   - Don't wait for all
```

### Meeting-Based Reviews (когда needed)

**Когда использовать**:
- Complex technical decisions
- High disagreement
- Cross-team impact
- Need for real-time discussion

**Format** (60 min):
```
00-10: Author presents (10 min)
10-25: Questions and clarifications (15 min)
25-45: Discussion of concerns (20 min)
45-55: Decision making (10 min)
55-60: Action items and next steps (5 min)
```

**Preparation**:
- Author: Send materials 24h before
- Reviewers: Read materials beforehand
- Facilitator: Prepare agenda

**Follow-up**:
- Meeting notes within 24h
- Decision documented in ADR/RFC
- Action items assigned

---

## Automation for Review

### Pre-Review Automation

```yaml
# .github/workflows/pre-review-checks.yml
name: Pre-Review Checks

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  automated-checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check EARS format
        run: python scripts/lint_ears.py specs/**/requirements.md
      
      - name: Check ADR format
        run: python scripts/validate_adr_format.py docs/adr/**/*.md
      
      - name: Check cross-references
        run: python scripts/check_links.py
      
      - name: Check requirements coverage
        run: python scripts/check_requirements_coverage.py
      
      - name: Auto-assign reviewers
        uses: kentaro-m/auto-assign-action@v1.2.0
        with:
          repo-token: "${{ secrets.GITHUB_TOKEN }}"
          configuration-path: ".github/auto-assign.yml"
```

### Auto-Assign Configuration

```yaml
# .github/auto-assign.yml
addReviewers:
  # Default reviewers for all PRs
  - alice
  - bob

addAssignees: author

reviewGroups:
  # Specialized reviewers by area
  architecture:
    - charlie
    - diana
  security:
    - eve
    - frank
  product:
    - grace

runOn:
  - pull_request

# Auto-assign based on files changed
reviewers:
  docs/adr/**:
    - architecture
  docs/rfc/**:
    - architecture
  specs/**/requirements.md:
    - product
  specs/**/approach.md:
    - architecture
```

### Review Reminders

```python
# scripts/review_reminder.py
import requests
from datetime import datetime, timedelta
from github import Github

def send_review_reminders():
    """Отправляет reminders для PRs ожидающих review"""
    
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo("org/repo")
    
    stale_threshold = datetime.now() - timedelta(days=2)
    
    for pr in repo.get_pulls(state='open'):
        # Check if PR has been open > 2 days without review
        if pr.created_at < stale_threshold:
            if len(pr.get_reviews()) == 0:
                send_reminder(pr)

def send_reminder(pr):
    """Отправляет reminder в Slack"""
    
    message = f"""
    🔔 *Review Reminder*
    
    PR #{pr.number}: {pr.title}
    Author: {pr.user.login}
    Open for: {(datetime.now() - pr.created_at).days} days
    
    Reviewers: {', '.join([r.login for r in pr.requested_reviewers])}
    
    Link: {pr.html_url}
    
    _Please review or reassign if unavailable_
    """
    
    requests.post(
        SLACK_WEBHOOK,
        json={"text": message}
    )

if __name__ == '__main__':
    send_review_reminders()
```

### Auto-Approval Rules

```yaml
# .github/workflows/auto-approve.yml
name: Auto-Approve Low-Risk Changes

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  auto-approve:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check if auto-approvable
        id: check
        run: |
          # Auto-approve if:
          # 1. Only typo fixes (< 10 lines changed)
          # 2. Documentation examples
          # 3. README updates
          
          FILES_CHANGED=$(git diff --name-only origin/main...HEAD)
          LINES_CHANGED=$(git diff --stat origin/main...HEAD | tail -1 | awk '{print $4}')
          
          if [[ $LINES_CHANGED -lt 10 ]] && [[ $FILES_CHANGED == *"README.md"* ]]; then
            echo "auto_approve=true" >> $GITHUB_OUTPUT
          else
            echo "auto_approve=false" >> $GITHUB_OUTPUT
          fi
      
      - name: Auto-approve
        if: steps.check.outputs.auto_approve == 'true'
        uses: hmarr/auto-approve-action@v3
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

---

## Metrics for Review Process

### Review Efficiency Metrics

| Метрика | Target | Alert Threshold |
|---------|--------|-----------------|
| **Average review time** | < 2 days | > 5 days |
| **Review iterations** | < 2 | > 3 |
| **First-time approval rate** | > 70% | < 50% |
| **Reviewer workload** | < 5 PRs/week | > 10 PRs/week |
| **Stale PRs** | < 5% | > 15% |

### Review Quality Metrics

| Метрика | Target | Alert Threshold |
|---------|--------|-----------------|
| **Post-merge issues** | < 5% | > 15% |
| **Rework rate** | < 10% | > 25% |
| **Checklist coverage** | 100% | < 80% |
| **Feedback specificity** | > 80% | < 60% |

### Dashboard Example

```
┌─────────────────────────────────────────────────────────────┐
│  📊 REVIEW PROCESS METRICS                                     │
├─────────────────────────────────────────────────────────────┤
│  Average Review Time: 1.8 days (target: <2 days) ✅         │
│  First-time Approval: 73% (target: >70%) ✅                 │
│  Review Iterations: 1.6 (target: <2) ✅                     │
│  Stale PRs: 8% (target: <10%) ✅                            │
├─────────────────────────────────────────────────────────────┤
│  👥 REVIEWER WORKLOAD (this week)                           │
├─────────────────────────────────────────────────────────────┤
│  Alice:   4 reviews (2 pending) ✅                          │
│  Bob:     7 reviews (5 pending) ⚠️                          │
│  Charlie: 3 reviews (1 pending) ✅                          │
│  Diana:   11 reviews (8 pending) ❌ (overloaded)            │
├─────────────────────────────────────────────────────────────┤
│  📈 TRENDS (last 4 weeks)                                   │
├─────────────────────────────────────────────────────────────┤
│  Review Time:      2.5d → 2.2d → 2.0d → 1.8d 📉            │
│  Approval Rate:    65% → 68% → 70% → 73% 📈                 │
│  Post-merge Issues: 12% → 10% → 8% → 6% 📉                 │
└─────────────────────────────────────────────────────────────┘
```

---

## Anti-Patterns

### ❌ Rubber Stamp Reviews

**Проблема**: Reviewers approve без reading  
**Симптомы**: High approval rate, but many post-merge issues  
**Решение**: Require checklist completion, track review quality

### ❌ Nitpick Central

**Проблема**: Reviewer blocks на style issues  
**Симптомы**: Long review cycles, author frustration  
**Решение**: Automate style checks (linters), focus on substance

### ❌ Drive-By Reviews

**Проблема**: Superficial reviews от people без context  
**Симптомы**: Unhelpful feedback, rework  
**Решение**: Assign reviewers с relevant expertise

### ❌ Endless Review Cycles

**Проблема**: Review → Changes → Review → Changes → ...  
**Симптомы**: PRs open for weeks  
**Решение**: Time-box iterations, escalate after 2 rounds

### ❌ Ghost Reviewers

**Проблема**: Assigned reviewers не respond  
**Симптомы**: PRs stalled  
**Решение**: Reminders, reassignment, auto-approve

### ❌ Review Theater

**Проблема**: Reviews для show, не для quality  
**Симптомы**: Checkbox mentality, no real feedback  
**Решение**: Measure review quality, not just completion

---

## Tools for Collaboration

### GitHub/GitLab Features

**Pull Requests**:
- Inline comments
- Suggested changes
- Review requests
- Approval workflows

**Discussions**:
- RFC debates
- Architecture discussions
- Q&A

**Issues**:
- Track improvements
- Feature requests
- Bug reports

**Projects**:
- Kanban boards
- Milestone tracking
- Automation

### Slack/Teams Integrations

```yaml
# Slack notifications
notifications:
  - event: pr.opened
    channel: #engineering
    message: "📝 New PR: {title} by {author}"
  
  - event: pr.review_requested
    channel: direct
    message: "🔔 Review requested: {title}"
  
  - event: pr.approved
    channel: #engineering
    message: "✅ PR approved: {title}"
  
  - event: pr.merged
    channel: #engineering
    message: "🎉 PR merged: {title}"
```

### Documentation Platforms

**Notion**:
- Collaborative editing
- Comments и mentions
- Database views
- Templates

**Confluence**:
- Enterprise features
- Integration с Jira
- Version history
- Permissions

**GitBook**:
- Git-based
- Beautiful UI
- Collaboration
- Versioning

---

## Summary

**Процессы ревью и коллаборации** — это:

1. **4 workflows** от lightweight до formal
2. **Checklists** для каждого типа артефакта
3. **Effective feedback** через SBI model
4. **Approval patterns** для разных scenarios
5. **Conflict resolution** с escalation path
6. **Time management** с SLAs
7. **Automation** для pre-review checks
8. **Metrics** для continuous improvement

**Ключевые принципы**:
- Review is collaboration
- Explicit expectations
- Async-first
- Time-boxed
