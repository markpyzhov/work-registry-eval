# ClickUp Task: CIPH-44
**Source ID**: SRC-CU-CIPH-44

**Task ID**: CIPH-44
**Title**: Load org-specific redaction terms from CSV
**Status**: Completed
**Assignee**: Bob
**Priority**: Normal
**Date Created**: 2026-08-10

## Description
Let users supply organization-specific redaction terms via a CSV dictionary. The CSV dictionary path was wired into the detection matcher, and the rule test suite passes, depending on the already-completed financial-detection baseline.

## Acceptance Criteria
- Users can load custom redaction terms from a CSV dictionary.
- CSV dictionary terms are matched by the detection engine alongside built-in rules.
- Rule test suite passes for CSV dictionary matches against the completed detection baseline.

## Activity History
- **2026-08-10**: Alice - Task Create (Open)
 - *Opened the task because custom CSV redaction dictionary support was requested.*
- **2026-08-16**: Diana - Rule Test Pass (Completed)
 - *Confirmed the rule test passes for CSV dictionary matches, depending on the completed financial-detection baseline.*
