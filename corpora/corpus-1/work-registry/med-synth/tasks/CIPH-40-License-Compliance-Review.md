# ClickUp Task: CIPH-40
**Source ID**: SRC-CU-CIPH-40

**Task ID**: CIPH-40
**Title**: Audit third-party licenses before release
**Status**: Active (Reopened)
**Assignee**: Diana
**Priority**: High
**Date Created**: 2026-08-08

## Description
Audit third-party licenses across the dependency tree before release. An initial audit led to swapping the PDF parser library, but the task was reopened when the replacement parser turned out to be AGPL-licensed; the team is now searching for an Apache/MIT-licensed alternative.

## Acceptance Criteria
- Full dependency tree is audited for license compliance.
- No restrictive copyleft (e.g., AGPL) licenses remain in the shipped dependency set.
- Apache/MIT-licensed PDF parser alternative is identified and adopted, resolving the reopened AGPL finding.

## Activity History
- **2026-08-08**: Alice - Task Create (Open)
 - *Opened the task for a license compliance review ahead of release.*
- **2026-08-15**: Charlie - Apache/MIT Search (Active (Reopened))
 - *Searching for an Apache/MIT-licensed alternative PDF parser after the task was reopened when the replacement parser turned out to be AGPL-licensed.*
