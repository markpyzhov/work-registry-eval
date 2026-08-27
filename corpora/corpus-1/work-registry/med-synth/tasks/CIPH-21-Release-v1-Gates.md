# ClickUp Task: CIPH-21
**Source ID**: SRC-CU-CIPH-21

**Task ID**: CIPH-21
**Title**: Release v1.0 Gates
**Status**: Active
**Assignee**: Evan
**Priority**: Normal
**Date Created**: 2026-07-08

## Description
Track the mandatory release gates for CipherDoc v1.0 (WS-03). The initial checklist draft depended on T001 through T006 and T010. A later prerequisite audit found the checklist still incomplete while T005 (Docker image slim-down/CVE work) and T029 (Windows code-signing) remained open, and release notes were drafted in parallel while gates stayed open. Diana placed a security-gate hold on the release pending both T005's Docker slim-down/CVE work and T029's Windows Defender/SmartScreen code-signing; the task remains Active with those two gates unresolved.

## Acceptance Criteria
- Checklist dependencies T001-T006 and T010 satisfied (met; those tasks are Completed).
- T005 (Docker image size/CVE) and T029 (Windows code-signing) gates clear (not yet met; task remains Active pending both).

## Activity History
- **2026-07-08**: Evan - Task Create (Open)
 - *Task opened to track the release gates for the v1.0 milestone.*
