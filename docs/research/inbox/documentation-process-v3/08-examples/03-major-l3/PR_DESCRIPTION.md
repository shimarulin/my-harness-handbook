# PR: Migrate Notifications to Event-Driven Architecture (Kafka)

**Related RFC:** [rfc-0031](docs/rfc/0031-event-driven-notifications.md)
**Related ADR:** [adr-0007](docs/decisions/0007-use-kafka-for-notifications.md)
**Related Spec:** [spec-015](docs/specs/015-event-driven-notifications/spec.md)
**Related Tasks:** [tasks.md](docs/specs/015-event-driven-notifications/tasks.md)

## What Changed

### New Service: `notification-consumer`
- Kafka consumer for processing notification events
- Handlers for email, SMS, push, in-app notifications
- Retry with exponential backoff (1s → 625s, max 5 attempts)
- Dead letter queue for failed notifications
- Idempotency check to prevent duplicates
- Horizontal scaling via consumer groups + HPA

### API Service Changes
- Added `NotificationProducer` for publishing events to Kafka
- Dual-write mode: publish to Kafka AND sync processor (feature flag controlled)
- New feature flag: `use_kafka_notifications`

### Infrastructure
- Kafka topics: `notifications`, `notifications-dlq`, `notifications-retry`
- Avro schema registered in Schema Registry
- Monitoring: Prometheus metrics, Grafana dashboards, AlertManager rules

### Admin Interface
- View dead letter queue messages
- Replay failed notifications
- Replay time range

## Why

- **Performance:** API p95 latency at peak: 3s → 300ms (target)
- **Reliability:** 99.9% delivery within 5 minutes (vs current ~95%)
- **Scalability:** Independent scaling of notification processing
- **Compliance:** Replay capability for failed notifications (GDPR audit requirement)
- **Operations:** Reduce 20% of team time spent on notification performance issues

Detailed rationale: [RFC 0031](docs/rfc/0031-event-driven-notifications.md)

## Architecture

```
[API Service] → [Kafka: notifications topic]
                      ↓
           [Notification Consumer Service]
           ├── [Email Handler]
           ├── [SMS Handler]
           ├── [Push Handler]
           └── [In-App Handler]
                      ↓
           [Failed → Retry → DLQ]
```

## Deployment Plan

This PR implements Phases 1-3 from [RFC Implementation Phases](docs/rfc/0031-event-driven-notifications.md#implementation-phases).

**Current Phase:** Phase 3 (Consumer Implementation) — dual-write mode

**Next Steps (separate PRs):**
1. Phase 4: Validation and gradual rollout (dual-write → Kafka only)
2. Phase 5: Admin interface and runbooks

**Rollback:** Feature flag `use_kafka_notifications` can switch back to sync processing instantly.

## How to Test

### Unit Tests
- [ ] Producer: event serialization, error handling
- [ ] Consumer: event deserialization, routing, offset commit
- [ ] Handlers: idempotency, retry logic
- [ ] Retry: exponential backoff calculation
- [ ] DLQ: failure reason attachment

### Integration Tests (testcontainers)
- [ ] End-to-end: publish → consume → send notification
- [ ] Retry: simulate failure → verify retry attempts
- [ ] DLQ: simulate persistent failure → verify DLQ message
- [ ] Idempotency: publish same event twice → verify single send
- [ ] Schema evolution: publish with new schema → verify compatibility

### E2E Tests (staging)
- [ ] Dual-write: verify sync and async produce same notifications
- [ ] Load test: 10,000 events/second for 5 minutes
- [ ] Failure recovery: kill consumer → verify lag recovery
- [ ] Kafka unavailable: verify fallback to sync

## Monitoring

New dashboards and alerts:

| Dashboard | Panel | Alert Threshold |
|---|---|---|
| Consumer Lag | Per partition | > 60 seconds |
| Processing Rate | Events/second | < 100 (expected: 500+) |
| Error Rate | % failed | > 1% |
| DLQ Size | Message count | > 100 |
| Publish Latency | p95 | > 100ms |

## Checklist

- [x] All EARS requirements from spec-015 implemented
- [x] Unit tests added and passing
- [x] Integration tests with testcontainers
- [x] Feature flag for rollback
- [x] Monitoring and alerting configured
- [x] Documentation updated
- [x] Runbooks created
- [x] Team training scheduled
- [x] Linked to RFC, ADR, Spec, and Tasks
