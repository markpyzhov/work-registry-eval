# ClickUp Task: CIPH-15
**Source ID**: SRC-CU-CIPH-15

**Task ID**: CIPH-15
**Title**: Docker Packaging
**Status**: Active (Reopened)
**Assignee**: Evan
**Priority**: Normal
**Date Created**: 2026-06-11

## Description
Containerize CipherDoc's API and CLI into a Docker image (WS-03). The initial Dockerfile was completed on 2026-06-16, but Diana's size/CVE review reopened the task on 2026-06-25 after the built image measured 2.1GB. Evan is redesigning the build as multi-stage toward a ~450MB target, swapped the base image to Alpine, and removed unused OCR and runtime packages that were not needed at runtime. As of the 2026-08-12 size/CVE verification, the image still exceeds the ~450MB target and CVE verification remains outstanding. This ClickUp record was opened at task creation; the reopening and remediation steps above were tracked through engineering channels.

## Acceptance Criteria
- Image size reduced to the ~450MB target (not yet met).
- CVE verification passes with no outstanding findings (not yet met).
- Task stays Active (Reopened) until both size and CVE checks pass.

## Activity History
- **2026-06-11**: Evan - Task Create (Open)
 - *Task opened to containerize the API and CLI into a Docker image.*
