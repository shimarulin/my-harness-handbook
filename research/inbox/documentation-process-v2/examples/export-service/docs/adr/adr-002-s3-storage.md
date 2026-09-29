# ADR 002: Use S3 for Export File Storage

- **Status**: Accepted
- **Date**: 2025-01-22
- **Deciders**: @bob, @diana
- **RFC**: [RFC-001](../rfc/rfc-001-export-architecture.md)

## Context and Problem Statement

Export files need persistent storage that:
- Handles files up to 5GB
- Supports automatic cleanup (7-day expiry)
- Provides encryption at rest
- Scales with usage

## Decision Drivers

* File sizes: 1KB to 5GB
* Retention: 7 days automatic cleanup
* Security: AES-256 encryption required
* Cost: minimize storage costs
* Scalability: no upper limit

## Considered Options

* AWS S3
* Local filesystem
* Database BLOBs
* EFS/NFS

## Decision Outcome

Chosen option: "AWS S3", because:
- Cheap object storage at scale
- Built-in lifecycle policies for auto-cleanup
- Server-side encryption (AES-256)
- No disk management required
- Highly available and durable

### Consequences

* Good, because scalable with no management
* Good, because lifecycle policies automate cleanup
* Good, because encryption built-in
* Good, because signed URLs for secure access
* Bad, because network latency vs local disk
* Bad, because S3 costs grow with usage

### Confirmation

* [ ] S3 bucket created with lifecycle policy
* [ ] Encryption configured
* [ ] Signed URL generation working
* [ ] Cost monitoring in place

## More Information

* [ADR-001](./adr-001-async-processing.md) - Async processing decision
* [S3 Lifecycle Policies](https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-expire-general-considerations.html)
