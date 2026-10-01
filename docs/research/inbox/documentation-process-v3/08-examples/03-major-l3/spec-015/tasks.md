---
id: spec-015-tasks
type: tasks
status: draft
created: 2026-09-25
title: Event-Driven Notifications Implementation Tasks
traces: [spec-015]
---

# Tasks: Event-Driven Notifications Implementation

**Related Spec:** [spec-015](spec.md)
**Related ADR:** [adr-0007](../../decisions/0007-use-kafka-for-notifications.md)

## Phase 1: Infrastructure (Week 1-2)

### 1.1 Kafka Setup
- [ ] Provision Confluent Cloud Kafka cluster (3 brokers)
- [ ] Configure replication factor: 3
- [ ] Set up SASL/SSL authentication
- [ ] Create topics:
  - `notifications` (partitions: 12, retention: 7 days)
  - `notifications-dlq` (partitions: 3, retention: 30 days)
  - `notifications-retry` (partitions: 6, retention: 7 days)
- [ ] Verify topic creation and configuration

### 1.2 Schema Registry
- [ ] Set up Schema Registry (Confluent Cloud)
- [ ] Define Avro schema for notification event:
  ```json
  {
    "type": "record",
    "name": "NotificationEvent",
    "fields": [
      {"name": "event_id", "type": "string"},
      {"name": "event_type", "type": "string"},
      {"name": "user_id", "type": "string"},
      {"name": "payload", "type": "string"},
      {"name": "timestamp", "type": "long"},
      {"name": "correlation_id", "type": "string"}
    ]
  }
  ```
- [ ] Register schema with backward compatibility mode
- [ ] Test schema evolution (add optional field)

### 1.3 Monitoring Setup
- [ ] Set up Prometheus scraper for Kafka metrics
- [ ] Create Grafana dashboards:
  - Consumer lag per partition
  - Processing throughput
  - Error rates by type
  - DLQ size
- [ ] Configure alerts:
  - Consumer lag > 60 seconds
  - Error rate > 1%
  - DLQ size > 100 messages

## Phase 2: Producer Implementation (Week 3-4)

### 2.1 Kafka Producer Library
- [ ] Add Kafka producer dependency (confluent-kafka-go / confluent-kafka-python)
- [ ] Implement `NotificationProducer` interface:
  - `PublishEvent(event NotificationEvent) error`
  - `PublishBatch(events []NotificationEvent) error`
- [ ] Configure producer:
  - Acks: all (wait for all replicas)
  - Retries: 3
  - Compression: snappy
- [ ] Add error handling and logging

### 2.2 Event Schema Integration
- [ ] Implement Avro serialization/deserialization
- [ ] Integrate with Schema Registry for schema validation
- [ ] Add schema version to event metadata
- [ ] Unit tests for serialization roundtrip

### 2.3 API Service Integration
- [ ] Identify all notification-triggering code paths in API service
- [ ] Add dual-write: publish to Kafka AND call sync processor
- [ ] Add feature flag: `use_kafka_notifications` (default: false)
- [ ] Add metrics: publish success rate, publish latency
- [ ] Integration tests with testcontainers Kafka

### 2.4 Monitoring for Producers
- [ ] Add producer metrics: publish rate, error rate, latency
- [ ] Add logging for failed publishes
- [ ] Set up alerting for publish failures

## Phase 3: Consumer Implementation (Week 5-6)

### 3.1 Consumer Service Skeleton
- [ ] Create new service: `notification-consumer`
- [ ] Set up Kubernetes deployment with HPA
- [ ] Configure consumer group: `notification-processors`
- [ ] Implement graceful shutdown (drain connections)

### 3.2 Event Consumption
- [ ] Implement Kafka consumer loop
- [ ] Deserialize Avro events
- [ ] Route to appropriate notification handler based on event_type
- [ ] Implement offset commit strategy (after successful processing)
- [ ] Add consumer lag monitoring

### 3.3 Notification Handlers
- [ ] Implement `EmailNotificationHandler`
  - Use existing email service
  - Add idempotency check (event_id + "email")
  - Add retry logic
- [ ] Implement `SmsNotificationHandler`
  - Use existing SMS service
  - Add idempotency check (event_id + "sms")
  - Add retry logic
- [ ] Implement `PushNotificationHandler`
  - Use existing push service
  - Add idempotency check (event_id + "push")
  - Add retry logic
- [ ] Implement `InAppNotificationHandler`
  - Write to database
  - Add idempotency check (event_id + "inapp")
  - No retry needed (database write)

### 3.4 Retry and DLQ
- [ ] Implement retry with exponential backoff: 1s, 5s, 25s, 125s, 625s
- [ ] Implement max retry limit: 5 attempts
- [ ] Implement DLQ publishing after max retries
- [ ] Add failure reason to DLQ message
- [ ] Add alerting when message goes to DLQ

### 3.5 Idempotency
- [ ] Create idempotency store (Redis with TTL)
- [ ] Implement check: `event_id + channel` → already sent?
- [ ] Implement mark: `event_id + channel` → sent successfully
- [ ] Set TTL: 7 days (match Kafka retention)
- [ ] Handle Redis unavailability (fallback to in-memory)

## Phase 4: Cutover (Week 7-8)

### 4.1 Validation Phase
- [ ] Enable dual-write for 10% of traffic
- [ ] Monitor: compare sync vs async notification delivery
- [ ] Verify: no data loss, no duplicates
- [ ] Measure: async latency vs sync latency
- [ ] Document any discrepancies

### 4.2 Gradual Rollout
- [ ] Increase dual-write to 50% of traffic
- [ ] Monitor for 2 days
- [ ] Increase to 100% dual-write
- [ ] Monitor for 2 days
- [ ] Verify all metrics healthy

### 4.3 Cutover
- [ ] Switch flag: `use_kafka_notifications = true` (Kafka only)
- [ ] Monitor for 24 hours
- [ ] Keep sync code path for rollback (1 week)
- [ ] After 1 week: remove sync code path

### 4.4 Rollback Plan
- [ ] Document rollback procedure
- [ ] Test rollback in staging
- [ ] Ensure feature flag can switch back instantly
- [ ] Define criteria for rollback (e.g., error rate > 5%)

## Phase 5: Admin & Operations (Week 9)

### 5.1 Admin Interface
- [ ] Create admin endpoint: view DLQ messages
- [ ] Create admin endpoint: replay DLQ messages
- [ ] Create admin endpoint: replay time range
- [ ] Add authentication/authorization for admin endpoints
- [ ] Add audit logging for admin actions

### 5.2 Runbooks
- [ ] Create runbook: "Kafka consumer lag high"
- [ ] Create runbook: "DLQ has messages"
- [ ] Create runbook: "Kafka cluster unavailable"
- [ ] Create runbook: "Schema incompatibility detected"
- [ ] Train on-call engineers

## Verification Checklist

- [ ] All EARS requirements from spec-015 implemented
- [ ] Dual-write validation passed (no data loss)
- [ ] Cutover completed successfully
- [ ] Rollback tested
- [ ] Monitoring dashboards live
- [ ] Alerts configured
- [ ] Admin interface functional
- [ ] Runbooks documented
- [ ] Team trained on new architecture
