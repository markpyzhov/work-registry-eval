# ClickUp Task: CIPH-39
**Source ID**: SRC-CU-CIPH-39

**Task ID**: CIPH-39
**Title**: Fix Windows builds and clear Defender/SmartScreen signing
**Status**: Active
**Assignee**: Evan
**Priority**: High
**Date Created**: 2026-08-08

## Description
Make the redaction suite compatible with Windows, including build packaging. A Windows build artifact now exists, but Windows Defender/SmartScreen blocks the unsigned build because a code-signing certificate is still missing; the task remains active pending that certificate.

## Acceptance Criteria
- Windows build artifact is produced successfully.
- Build is code-signed with a valid certificate so it is not blocked by Defender/SmartScreen.
- Signed build passes Windows Defender/SmartScreen without warnings.

## Activity History
- **2026-08-08**: Alice - Task Create (Open)
 - *Opened the task because Windows OS compatibility is required for the release gate.*
- **2026-09-02**: Evan - Signing Cert Missing (Active)
 - *Found that Windows Defender/SmartScreen blocks the unsigned build because a code-signing certificate is still missing; task remains active.*
