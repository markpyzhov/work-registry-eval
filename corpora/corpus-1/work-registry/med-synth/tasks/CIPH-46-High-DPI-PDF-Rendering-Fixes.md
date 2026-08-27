# ClickUp Task: CIPH-46
**Source ID**: SRC-CU-CIPH-46

**Task ID**: CIPH-46
**Title**: Correct high-DPI PDF coordinate scaling
**Status**: Blocked
**Assignee**: Charlie
**Priority**: Normal
**Date Created**: 2026-08-15

## Description
Fix coordinate misalignment defects reported on high-DPI displays. The scaling-math error was traced to a bug in the upstream rendering library, and the task is blocked with no local fix available yet.

## Acceptance Criteria
- Coordinate alignment on high-DPI displays matches the preview overlay coordinates.
- Root cause of the scaling-math error is fixed (currently blocked on an upstream library bug).

## Activity History
- **2026-08-15**: Alice - Task Create (Open)
 - *Opened the task because high-DPI PDF coordinate alignment defects were reported.*
- **2026-09-10**: Diana - Upstream Scaling Bug Block (Blocked)
 - *Blocked after tracing the scaling-math error to a bug in the upstream rendering library, with no local fix yet.*
