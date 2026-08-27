# ClickUp Task: CIPH-17
**Source ID**: SRC-CU-CIPH-17

**Task ID**: CIPH-17
**Title**: Fix Coordinate/Offset Drift in Multi-Page PDFs
**Status**: Blocked
**Assignee**: Charlie
**Priority**: High
**Date Created**: 2026-06-19

## Description
Investigate and fix a coordinate/offset drift where redaction masks do not line up with target text across multi-page PDFs (WS-01). Debugging traced the drift to a whitespace-handling issue that is blocked on upstream `pdfminer.six` issue/PR #992, which remains unmerged. Maintaining a local fork of the fix was evaluated and rejected due to long-term maintenance risk. The team has decided to leave this task Blocked pending an upstream merge, with no local workaround adopted.

## Acceptance Criteria
- Coordinate drift root cause confirmed (whitespace handling in `pdfminer.six`).
- Upstream `pdfminer.six` PR #992 merges, or an accepted local remediation is adopted (neither has occurred; task remains Blocked).

## Activity History
- **2026-06-19**: Bob - Task Create (Open)
 - *Task opened to investigate the coordinate/offset drift in multi-page PDF redaction.*
