Feature: Data Export
  As a user
  I want to export my data
  So that I can back it up or migrate to another platform

  Background:
    Given user "alice" is authenticated
    And alice has 1000 records

  Rule: Export formats
    # REQ-EXP-001, REQ-EXP-002

    Scenario: Export as CSV
      When alice requests CSV export
      Then export is queued
      And alice receives an export ID
      And export status is "pending"

    Scenario: Export as JSON
      When alice requests JSON export
      Then export is queued
      And alice receives an export ID

    Scenario: Invalid format rejected
      When alice requests XML export
      Then response status is 400
      And error message contains "Invalid format"

  Rule: Request acknowledgment
    # REQ-EXP-005: Acknowledge within 2 seconds

    Scenario: Export request returns ID within 2 seconds
      When alice requests CSV export
      Then response status is 202
      And response contains "export_id"
      And response time is less than 2 seconds

  Rule: Progress tracking
    # REQ-EXP-009, REQ-EXP-010

    Scenario: Cannot export while another export is in progress
      Given alice has an export in progress
      When alice requests another export
      Then response status is 409
      And error message contains "Export already in progress"

    Scenario: Progress is reported during export
      Given alice has requested a CSV export
      And the export is in progress
      When alice checks the export status
      Then response contains "progress_percent"
      And progress_percent is between 0 and 100

  Rule: Completion and notification
    # REQ-EXP-006, REQ-EXP-007

    Scenario: Email sent on successful completion
      Given alice has requested a CSV export
      And the export completes successfully
      Then alice receives email notification
      And email contains download link
      And download link is valid for 7 days

    Scenario: Download file after completion
      Given alice's export has completed
      When alice clicks the download link
      Then file is served with correct Content-Type
      And file size matches export record

  Rule: Error handling
    # REQ-EXP-015, REQ-EXP-018

    Scenario: Failed export notifies user
      Given database will fail during export
      When alice requests CSV export
      Then export status becomes "failed"
      And alice receives email with error details

    Scenario: Retry on transient failure
      Given first export attempt will fail
      And second export attempt will succeed
      When alice requests CSV export
      Then export completes successfully after retry

  Rule: Large exports
    # REQ-EXP-016, REQ-EXP-021

    @slow
    Scenario: Large export uses streaming
      Given alice has 10 million records
      When alice requests CSV export
      Then system uses streaming approach
      And memory usage stays below 512MB
      And export completes within 30 minutes

    Scenario: File split for > 5GB exports
      Given alice has enough data to exceed 5GB
      When alice requests CSV export
      Then export is split into multiple files
      And alice is informed about multiple files

  Rule: Security
    # REQ-EXP-023, REQ-EXP-024

    Scenario: Cannot access other user's export
      Given bob has completed an export
      When alice tries to access bob's export
      Then response status is 403

    Scenario: Download link expires after 7 days
      Given alice's export completed 8 days ago
      When alice tries to download the export
      Then response status is 410
      And error message contains "Link expired"

  Rule: Enterprise features
    # REQ-EXP-012

    @enterprise
    Scenario: Scheduled exports for enterprise users
      Given alice has enterprise plan
      When alice schedules daily exports
      Then schedule is saved
      And first export runs at scheduled time
