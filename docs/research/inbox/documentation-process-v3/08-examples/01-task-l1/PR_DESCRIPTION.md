# PR: Fix unclear timeout error message on login

**Fixes #1234**
**Task: [task-042](tasks/042-fix-timeout-error.md)**

## What Changed

- Replaced generic "Something went wrong" with specific "Session expired. Please login again." for timeout errors
- Added "Login again" button in timeout error state
- Added i18n keys for the new message

## Why

Users couldn't distinguish session timeout from other errors, leading to confusion and support tickets. This was reported 3 times in the last month.

## How to Test

1. Login to the app
2. Wait for session to expire (or manually expire via dev tools)
3. Try to perform any action
4. Verify: See "Session expired. Please login again." with "Login again" button
5. Click "Login again" → should redirect to login page

## Screenshots

**Before:**
![Before: Generic error](screenshots/before.png)

**After:**
![After: Clear timeout message](screenshots/after.png)

## Checklist

- [x] Tests added and passing
- [x] No breaking changes
- [x] i18n keys added to all supported languages
- [x] Documentation not required (bug fix)
- [x] Linked to task-042
