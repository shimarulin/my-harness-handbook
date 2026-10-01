# ADR 001: Use Celery for Async Task Processing

- **Status**: Accepted
- **Date**: 2025-01-20
- **Deciders**: @bob, @charlie
- **RFC**: [RFC-001](../rfc/rfc-001-export-architecture.md)

## Context and Problem Statement

Export operations can take 10 seconds to 30 minutes. We need async task processing that:
- Handles long-running tasks
- Provides retry mechanism
- Scales horizontally
- Integrates with Python/FastAPI stack

## Decision Drivers

* Task duration: 10 seconds to 1 hour
* Reliability: automatic retries needed
* Scalability: dynamic worker scaling
* Team familiarity: Python expertise
* Infrastructure: Redis already in use

## Considered Options

* Celery + Redis
* RQ (Redis Queue)
* AWS SQS + Lambda
* Custom background workers
* Dramatiq

## Decision Outcome

Chosen option: "Celery + Redis", because:
- Mature, battle-tested (10+ years)
- Rich feature set (retries, scheduling, monitoring)
- Excellent Python integration
- Uses existing Redis infrastructure
- Flower UI for monitoring

### Consequences

* Good, because well-documented with large community
* Good, because Flower provides monitoring UI
* Good, because supports task priorities and routing
* Bad, because operational complexity
* Bad, because steeper learning curve than RQ

### Confirmation

* [ ] Celery workers deployed to staging
* [ ] Export tasks processed successfully
* [ ] Flower UI accessible
* [ ] Retry mechanism tested
* [ ] Memory usage monitored

## More Information

* [Celery Documentation](https://docs.celeryq.dev)
* [ADR-002](./adr-002-s3-storage.md) - S3 storage decision
