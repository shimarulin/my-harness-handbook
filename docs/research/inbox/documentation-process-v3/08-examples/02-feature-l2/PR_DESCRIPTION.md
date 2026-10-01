# PR: Add Data Export to CSV Feature

**Related PRD:** [prd-005](docs/prd/005-data-export.md)
**Related Spec:** [spec-012](docs/specs/012-data-export/spec.md)
**Related Tasks:** [tasks.md](docs/specs/012-data-export/tasks.md)

## What Changed

### Backend
- New `export_jobs` database table with migration
- `ExportService` with async processing, CSV generation, rate limiting
- Three new API endpoints:
  - `POST /api/export` — create export job
  - `GET /api/export/{jobId}` — check status
  - `GET /api/export/{jobId}/download` — download file

### Frontend
- "Export my data" button in Settings
- Export options modal with category selection
- Export status display with download link
- User-friendly error handling

### Infrastructure
- Email templates for export ready/failed notifications
- Metrics and monitoring for export jobs
- S3 integration for file storage

## Why

- **GDPR compliance:** Article 20 requires data portability
- **User trust:** 23 feature requests in 6 months
- **Support load:** Reduce 5 manual export requests/week to <1

## How to Test

### Prerequisites
- Test user with data in all categories (profile, activity, settings)

### Test Scenarios

1. **Basic Export:**
   - Login → Settings → "Export my data"
   - Select "All" → Confirm
   - Verify: "Export in progress" message
   - Wait for email (should arrive < 5 min)
   - Click download link → CSV file downloads
   - Verify CSV contains all data categories

2. **Rate Limiting:**
   - Perform 3 exports
   - Try 4th export
   - Verify: "Export limit reached" message

3. **Selective Export:**
   - Select only "Profile"
   - Verify CSV contains only profile data

4. **Expired Link:**
   - Complete export
   - Wait 25 hours (or manually expire)
   - Try download link
   - Verify: "Link expired" message

## Screenshots

| Export Modal | Export Status | Email Notification |
|---|---|---|
| ![Modal](screenshots/export-modal.png) | ![Status](screenshots/export-status.png) | ![Email](screenshots/export-email.png) |

## API Changes

### New Endpoints

```yaml
# OpenAPI additions
/api/export:
  post:
    summary: Create data export job
    requestBody:
      categories: [profile, activity, settings]  # or "all"
    responses:
      202:
        jobId: string
        status: pending
      429:
        message: "Export limit reached"

/api/export/{jobId}:
  get:
    summary: Get export job status
    responses:
      200:
        status: pending | processing | completed | failed
        downloadUrl?: string
        expiresAt?: string

/api/export/{jobId}/download:
  get:
    summary: Download export file
    responses:
      200:
        content: text/csv
      404:
        message: "Link expired or not found"
```

## Checklist

- [x] All EARS requirements implemented
- [x] Unit tests added and passing
- [x] Integration tests added and passing
- [x] E2E tests for all scenarios
- [x] Rate limiting verified
- [x] Email notifications working
- [x] Performance targets met
- [x] API documentation updated (OpenAPI)
- [x] User help docs updated
- [x] Monitoring and metrics added
- [x] Linked to PRD, Spec, and Tasks
