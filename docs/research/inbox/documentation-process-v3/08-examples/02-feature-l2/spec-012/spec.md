---
id: spec-012
type: spec
status: approved
created: 2026-09-22
title: Data Export Specification
traces: [prd-005]
level: L2
---

# Spec: Data Export to CSV

**Related PRD:** [prd-005](../../prd/005-data-export.md)
**Status:** Approved for implementation

## Overview

Система предоставляет возможность пользователям экспортировать их данные в CSV формате через async processing с email notification.

## Requirements (EARS)

### R1: Export Initiation

**WHEN** a user clicks "Export my data" button in Settings
**THE SYSTEM SHALL** display export options (data categories selection)
**AND THE SYSTEM SHALL** allow user to select: Profile, Activity, Settings, All

### R2: Export Processing

**WHEN** a user confirms export request
**THE SYSTEM SHALL** create an export job with unique ID
**AND THE SYSTEM SHALL** process the export asynchronously
**AND THE SYSTEM SHALL** limit processing time to 5 minutes for typical users

### R3: Export Completion

**WHEN** export processing completes successfully
**THE SYSTEM SHALL** send email notification to user
**AND THE SYSTEM SHALL** include download link valid for 24 hours
**AND THE SYSTEM SHALL** include file size in the notification

### R4: Export Failure

**WHEN** export processing fails
**THE SYSTEM SHALL** send email notification to user
**AND THE SYSTEM SHALL** include error reason (without technical details)
**AND THE SYSTEM SHALL** suggest retry after 1 hour

### R5: Rate Limiting

**WHEN** a user requests more than 3 exports in 24 hours
**THE SYSTEM SHALL** reject the request
**AND THE SYSTEM SHALL** display message "Export limit reached. Try again tomorrow."

### R6: File Format

**WHEN** export file is generated
**THE SYSTEM SHALL** use CSV format with UTF-8 encoding
**AND THE SYSTEM SHALL** include headers row
**AND THE SYSTEM SHALL** escape special characters properly
**AND THE SYSTEM SHALL** limit file size to 100MB

### R7: Data Categories

**WHEN** user selects "Profile" category
**THE SYSTEM SHALL** include: username, email, created_at, updated_at, preferences

**WHEN** user selects "Activity" category
**THE SYSTEM SHALL** include: all user actions with timestamps (last 12 months)

**WHEN** user selects "Settings" category
**THE SYSTEM SHALL** include: all user settings with current values

### R8: Security

**WHEN** download link is accessed
**THE SYSTEM SHALL** verify user authentication
**AND THE SYSTEM SHALL** verify link has not expired (24 hours)
**AND THE SYSTEM SHALL** log the download event

## Acceptance Criteria

### Scenario: Successful export
- **GIVEN** user is logged in
- **WHEN** user clicks "Export my data" → selects "All" → confirms
- **THEN** system creates export job
- **AND** user sees "Export in progress" message
- **AND** email arrives within 5 minutes with download link
- **AND** downloaded CSV contains all user data

### Scenario: Rate limit exceeded
- **GIVEN** user has already done 3 exports today
- **WHEN** user clicks "Export my data"
- **THEN** system displays "Export limit reached" message
- **AND** no new export job is created

### Scenario: Expired link
- **GIVEN** user has an export download link from 25 hours ago
- **WHEN** user clicks the link
- **THEN** system displays "Link expired" message
- **AND** suggests creating new export

## Non-functional Requirements

| Requirement | Target |
|---|---|
| Export processing time (typical user) | < 5 minutes |
| Export processing time (power user with 1M records) | < 30 minutes |
| Download link validity | 24 hours |
| File encoding | UTF-8 |
| Max file size | 100MB |
| Rate limit | 3 per 24 hours |

## Technical Constraints

- Must use existing email notification system
- Must integrate with current user authentication
- CSV generation: server-side (no client-side)
- Storage: use existing file storage (S3-compatible)
