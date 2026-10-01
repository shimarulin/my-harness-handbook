# RFC-001: Export Architecture

- **Status**: Approved
- **Author**: Bob Smith (Engineering Lead)
- **Created**: 2025-01-18
- **Review deadline**: 2025-01-25
- **Related PRD**: [docs/prd/export-feature.md](../prd/export-feature.md)
- **Related Requirements**: [specs/export/requirements.md](../../specs/export/requirements.md)

---

## Summary

We propose an **async, event-driven architecture** for the data export feature. Exports will be processed via a task queue (Celery + Redis), files stored in S3, and notifications sent via email. This approach handles large datasets efficiently while keeping API responses fast.

## Context and Problem

### Current State
- No export functionality exists
- Manual exports take 3-5 days via support team
- No standardized process or audit trail

### Requirements Summary
See [requirements.md](../../specs/export/requirements.md) for full list. Key constraints:
- **REQ-EXP-005**: Acknowledge request within 2 seconds
- **REQ-EXP-020**: Complete export within 30 seconds for <10K records
- **REQ-EXP-021**: Complete export within 30 minutes for >1M records
- **REQ-EXP-022**: Handle 1000 concurrent exports

### Why Async?
Export operations can take **10 seconds to 30 minutes**. Synchronous processing would:
- Block API responses (violates REQ-EXP-005)
- Timeout on large exports (violates REQ-EXP-021)
- Require horizontal scaling of API servers (expensive)

## Proposal

### Architecture Overview

```mermaid
graph TD
    A[User] -->|POST /exports| B[API Gateway]
    B --> C[Export API]
    C -->|Enqueue task| D[Redis Queue]
    C -->|Return 202 + export_id| A
    D --> E[Celery Worker]
    E -->|Stream data| F[PostgreSQL]
    E -->|Upload file| G[S3]
    E -->|Send notification| H[Email Service]
    E -->|Update status| F
    A -->|GET /exports/{id}| C
    A -->|Click download link| I[S3 Signed URL]
```

### Key Components

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Export API** | FastAPI | HTTP endpoints for requests |
| **Task Queue** | Redis + Celery | Async task processing |
| **Workers** | Celery workers | Process export tasks |
| **Database** | PostgreSQL | Store export metadata |
| **File Storage** | S3 | Store export files |
| **Email** | SendGrid | Send notifications |

### Design Decisions

1. **Async processing** via Celery (see ADR-001)
2. **S3 for file storage** with 7-day lifecycle (see ADR-002)
3. **Streaming** for large exports (>1M records)
4. **Signed URLs** for secure downloads

## Alternatives Considered

### Alternative 1: Synchronous Processing

**Description**: Process export directly in API request, return file when done.

**Pros**:
- Simple to implement
- No additional infrastructure

**Cons**:
- ❌ Blocks API response for duration of export
- ❌ Timeout issues for large exports
- ❌ Requires horizontal scaling of API servers
- ❌ Violates REQ-EXP-005 (2-second response)

**Why rejected**: Fundamental incompatibility with performance requirements.

### Alternative 2: AWS SQS + Lambda

**Description**: Use AWS managed services for async processing.

**Pros**:
- Fully managed, auto-scaling
- No worker management

**Cons**:
- ❌ Lambda 15-minute timeout (exports can take 30 min)
- ❌ Cold start latency
- ❌ Vendor lock-in to AWS
- ❌ More expensive at scale

**Why rejected**: Timeout limitation and vendor lock-in concerns.

### Alternative 3: Custom Background Workers

**Description**: Build custom async processing with Python threading/multiprocessing.

**Pros**:
- Full control
- No external dependencies

**Cons**:
- ❌ Reinventing the wheel
- ❌ Need to build monitoring, retries, scaling
- ❌ High maintenance burden
- ❌ Team must maintain forever

**Why rejected**: Unjustified complexity vs mature alternatives.

### Alternative 4: Do Nothing

**Pros**:
- Zero effort
- No risk of regression

**Cons**:
- ❌ Problem persists (GDPR violation)
- ❌ Revenue loss continues
- ❌ Support burden grows

**Why rejected**: Unacceptable business and legal risk.

## Trade-offs and Risks

### Trade-offs

| Aspect | Gain | Loss |
|--------|------|------|
| **Async processing** | Fast API response, scalability | Additional infrastructure (Redis) |
| **S3 storage** | Cheap, scalable, reliable | Network latency, S3 costs |
| **Signed URLs** | Secure, time-limited | Extra request to get URL |
| **Streaming** | Handles large datasets | More complex implementation |

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Queue overflow under load | Medium | High | Auto-scale workers, rate limiting |
| S3 upload failures | Low | High | Retry 3x, alert on failure |
| Email service outage | Medium | Medium | Queue notifications, retry 24h |
| Memory exhaustion on large exports | Medium | Critical | Streaming with chunked processing |

## Migration Plan

Since this is a greenfield feature, no migration needed. Rollout plan:

1. **Phase 1**: Deploy to staging (1 week)
2. **Phase 2**: Beta to 5% users (1 week)
3. **Phase 3**: Full production rollout

## Open Questions

- [x] Celery vs RQ vs Dramatiq? → **Celery** (see ADR-001)
- [x] S3 bucket structure? → **Flat with user prefixes** (see ADR-002)
- [ ] Max concurrent exports per user? → **10** (pending confirmation)

## Timeline

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| RFC Review | 1 week | Approved/rejected |
| Implementation | 3 weeks | Working code |
| Testing | 1 week | QA sign-off |
| Beta rollout | 1 week | 5% users |
| GA | — | Full release |

## References

- [PRD: Export Feature](../prd/export-feature.md)
- [Requirements](../../specs/export/requirements.md)
- [ADR-001: Async Processing](../adr/adr-001-async-processing.md)
- [ADR-002: S3 Storage](../adr/adr-002-s3-storage.md)
- [Celery Documentation](https://docs.celeryq.dev)
