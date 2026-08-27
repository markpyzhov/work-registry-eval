# ClickUp Task: CIPH-29
**Source ID**: SRC-CU-CIPH-29

**Task ID**: CIPH-29
**Title**: Offline auth with key rotation for air-gapped installs
**Status**: Blocked
**Assignee**: Diana
**Priority**: High
**Date Created**: 2026-08-01

## Description
Provide offline-mode authentication for air-gapped deployments, including a key-rotation flow that doesn't assume an always-on network. Testing against a local auth mock showed that key rotation cannot complete without network access in an air-gapped setting, and the task remains blocked with no resolution yet.

## Acceptance Criteria
- Authentication works fully offline for air-gapped deployment scenarios.
- Key-rotation flow completes without requiring network access.
- Blocking issue (rotation dependent on network) is resolved before the task can close.

## Activity History
- **2026-08-01**: Alice - Task Create (Open)
 - *Opened the task because air-gapped deployments require offline-mode authentication.*
- **2026-08-05**: Alice - Key Rotation Block (Blocked)
 - *Testing against a local auth mock showed key rotation cannot complete offline in an air-gapped setting, with no resolution found yet.*
