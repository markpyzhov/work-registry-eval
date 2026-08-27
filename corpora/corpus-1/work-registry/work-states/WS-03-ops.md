# WS-03: Packaging, Release gating, and Security
**Status**: in_progress
**Priority**: P0
**Owner**: Evan
**Project**: CipherDoc
**Last Updated**: 2026-09-22

## Sources
- `S1` — `SRC-SLACK-06` — [Slack Thread: Docker Image Size Optimization](../med-synth/communication/sources/slack/2026-06-25-docker-size.md)
- `S2` — `SRC-CU-CIPH-15` — [ClickUp Task CIPH-15: Docker Packaging](../med-synth/tasks/CIPH-15-Docker-Packaging.md)
- `S3` — `SRC-GDOC-06` — [Docker Release Notes Draft](../med-synth/documentation/sources/2026-06-16-Docker-Release-Notes.md)
- `S4` — `SRC-SLACK-09` — [Slack Thread: Security Patch - CORS Issue](../med-synth/communication/sources/slack/2026-07-10-security-patch.md)
- `S5` — `SRC-CU-CIPH-20` — [ClickUp Task CIPH-20: Security Audit](../med-synth/tasks/CIPH-20-Security-Audit.md)
- `S6` — `SRC-GDOC-09` — [Vulnerability Scan Report](../med-synth/documentation/sources/2026-07-06-Vulnerability-Scan.md)
- `S7` — `SRC-GDOC-05` — [Release Checklist](../med-synth/documentation/sources/2026-07-12-Release-Checklist.md)
- `S8` — `SRC-CU-CIPH-21` — [ClickUp Task CIPH-21: Release v1 Gates](../med-synth/tasks/CIPH-21-Release-v1-Gates.md)
- `S9` — `SRC-MEET-10` — [Fireflies Transcript: Pre-Release Audit](../med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md)
- `S10` — `SRC-SLACK-37` — [Slack Thread: Windows Signing Gap](../med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md)

## Request / Context
Operationalization of CipherDoc: Docker packaging for offline deployment, security vulnerability scans, and v1.0.0 release gate management.

## Task List
- [ ] `T005` (mapped to CIPH-15) — Create Docker image packaging for local runtime. `(S1, S2, S3)`
- [x] `T010` (mapped to CIPH-20) — Perform security audit and vulnerability scans. `(S4, S5, S6)`
- [ ] `T011` (mapped to CIPH-21) — Manage Release v1.0.0 gates and docs. `(S7, S8, S9, S10)`

## Active Work
- **T005 / CIPH-15 — dual size gates (CMT-2026-06-002)**: CISO review defines interim RC at 800MB once CVE-clean; GA remains ~450MB. Track both thresholds separately. `(CMT-2026-06-002)`
- **T005 / CIPH-15**: Docker packaging is **reopened/active**. Image ballooned to 2.1GB after OCR dependencies were bundled (`S1`). Evan implemented multi-stage builds and swapped to Alpine (`S1`), but as of August 12 the image still exceeds the ~450MB target and CVE verification is failing. `(S1, S2)`
- **T011 / CIPH-21**: Release gates are **active** under a security-gate hold. The September 15 pre-release audit lists Docker slim/CVE work, Windows signing, and audit-log schema alignment as open blockers (`S9`). T011 depends on T005 and T029 (Windows signing gap per `S10`). `(S7, S8, S9, S10)`

## Blockers and Dependencies
- **T011 — no-ship deadline (CMT-2026-09-002)**: Release board set hard no-ship after **2026-10-15** if T005 and T029 are not green. `(CMT-2026-09-002)`
- T011 cannot close until T005 (Docker size/CVE) and T029 (Windows code-signing certificate) are green. `(S9, S10)`

## Decisions and Superseded Directions
- **Reopened Docker Task**: CIPH-15 was initially completed at ~800MB, then superseded and reopened on June 25 when OCR bundling pushed the image to 2.1GB. `(S1 supersedes S3)`

## Done / Evidence
- **T010 — external attestation (CMT-2026-07-002)**: RedByte pen-test attestation letter dated 2026-07-11 supplements internal scan artifacts in the release evidence pack. `(CMT-2026-07-002)`
- `T010 / CIPH-20` — Security scans complete. A medium-severity CORS `*` origin issue was identified in the July 6 scan report (`S6`, a dated pre-patch snapshot) and patched by restricting to configured `ALLOWED_ORIGINS` (`S4`). Re-scans on July 15 confirmed the patch holds. `(S4, S5, S6)`

## Needs Manual Triage
_(none)_

## Next Update Needed
Docker multi-stage build progress, final CVE scan results, and release gate clearance.
