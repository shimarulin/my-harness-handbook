---
id: spec-015
type: spec
status: approved
created: 2026-09-24
title: Event-Driven Notification System Specification
traces: [adr-0007, rfc-0031]
level: L3
---

# Spec: Event-Driven Notification System

**Related ADR:** [adr-0007](../../decisions/0007-use-kafka-for-notifications.md)
**Related RFC:** [rfc-0031](../../rfc/0031-event-driven-notifications.md)
**Status:** Approved for implementation

## Overview

Спецификация event-driven notification system на базе Apache Kafka, обеспечивающая async processing, replay capability, и independent scaling.

## Requirements (EARS)

### R1: Event Publication

**WHEN** a notification-triggering event occurs (user action, system event, schedule)
**THE SYSTEM SHALL** publish an event to Kafka topic `notifications`
**AND THE SYSTEM SHALL** include: event_type, user_id, payload, timestamp, correlation_id
**AND THE SYSTEM SHALL** use Avro schema registered in Schema Registry

### R2: Event Consumption

**WHEN** a notification event is available in Kafka topic
**THE SYSTEM SHALL** consume the event within 5 seconds
**AND THE SYSTEM SHALL** determine notification channel(s) based on user preferences
**AND THE SYSTEM SHALL** send notification via appropriate channel (email/SMS/push/in-app)
**AND THE SYSTEM SHALL** mark event as processed (commit offset)

### R3: Retry Logic

**WHEN** notification sending fails
**THE SYSTEM SHALL** retry with exponential backoff: 1s, 5s, 25s, 125s, 625s
**AND THE SYSTEM SHALL** retry maximum 5 times
**AND THE SYSTEM SHALL** move event to dead letter queue after max retries exceeded

### R4: Dead Letter Queue

**WHEN** event is moved to dead letter queue
**THE SYSTEM SHALL** store original event with failure reason
**AND THE SYSTEM SHALL** alert operations team
**AND THE SYSTEM SHALL** allow manual replay via admin interface

### R5: Replay Capability

**WHEN** operations team triggers replay for a time range
**THE SYSTEM SHALL** re-read events from Kafka for that time range
**AND THE SYSTEM SHALL** reprocess failed notifications
**AND THE SYSTEM SHALL** not send duplicate notifications (idempotency key check)

### R6: Idempotency

**WHEN** notification event is processed
**THE SYSTEM SHALL** check idempotency key (event_id + channel)
**AND THE SYSTEM SHALL** skip if already sent successfully
**AND THE SYSTEM SHALL** log skip with reason "already_sent"

### R7: Scalability

**WHEN** notification volume increases
**THE SYSTEM SHALL** scale consumers horizontally (consumer groups)
**AND THE SYSTEM SHALL** maintain processing lag < 30 seconds
**AND THE SYSTEM SHALL** handle 10,000+ notifications per second

### R8: Schema Evolution

**WHEN** event schema changes
**THE SYSTEM SHALL** validate backward compatibility via Schema Registry
**AND THE SYSTEM SHALL** reject incompatible changes
**AND THE SYSTEM SHALL** support schema versioning

### R9: Monitoring

**WHEN** notification system is running
**THE SYSTEM SHALL** expose metrics: consumer lag, processing time, success rate, DLQ size
**AND THE SYSTEM SHALL** alert if consumer lag > 60 seconds
**AND THE SYSTEM SHALL** alert if error rate > 1%

### R10: Fallback

**WHEN** Kafka is unavailable
**THE SYSTEM SHALL** fall back to sync processing (with degraded performance)
**AND THE SYSTEM SHALL** queue events locally for later publication
**AND THE SYSTEM SHALL** alert operations team immediately

## Non-functional Requirements

| Requirement | Target |
|---|---|
| End-to-end latency (event → notification sent) | < 5 minutes |
| Consumer processing latency | < 5 seconds |
| Throughput | 10,000+ events/second |
| Availability | 99.9% |
| Data retention | 7 days (Kafka) |
| Consumer lag | < 30 seconds |
| Replay time range | Up to 7 days |

## Architecture Constraints

- **Message broker:** Apache Kafka (Confluent Cloud initially)
- **Serialization:** Avro with Schema Registry
- **Consumer framework:** Kafka consumer groups
- **Deployment:** Kubernetes with HPA for consumer scaling
- **Monitoring:** Prometheus + Grafana + AlertManager

## Migration Plan

**Phase 1-4:** See [RFC §Implementation Phases](../../rfc/0031-event-driven-notifications.md#implementation-phases)

**Rollback:** Feature flag to switch between sync and async processing
