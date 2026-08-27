# Docker packaging was once treated as finished. As of **2026-09-22**, what is the authoritative status of that work, what earlier completion claim does it supersede, and what concrete size and CVE outcomes still prevent calling the image release-ready?

<!-- RESPONSE_START -->

I have the full picture. Here is the answer.

## Authoritative status as of 2026-09-22

**Docker packaging (T005 / CIPH-15) is NOT finished — it is Active (Reopened), and it has been continuously reopened since 2026-06-25.** The authoritative Work State is `WS-03: Packaging, Release gating, and Security` (P0, owner Evan, last updated 2026-09-22), where T005 remains an unchecked task item.
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md` (lines 24, 29–31, 38)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-15-Docker-Packaging.md` — status "Active (Reopened)", explicitly stays reopened until both size and CVE checks pass.
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md` — the 09-22 brief still lists Docker size/CVE (T005) as open, and puts "WS-03 / T005 + T029" at #1 in priority order.

## What earlier completion claim it supersedes

The superseded claim is the **2026-06-16 "Docker Packaging — Initial Dockerfile Complete" release-notes draft (`SRC-GDOC-06`, DOC-2006, owner Evan)**, which declared the initial Dockerfile done for T005. That document itself conceded no size review and no CVE check had yet run against the build.

WS-03 records this explicitly under Decisions and Superseded Directions: CIPH-15 "was initially completed at ~800MB, then superseded and reopened on June 25 when OCR bundling pushed the image to 2.1GB," with provenance `S1 supersedes S3` — i.e. Diana's 2026-06-25 Slack review (`SRC-SLACK-06`) supersedes the 06-16 completion doc.
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-06-16-Docker-Release-Notes.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-06-25-docker-size.md`

## Concrete size and CVE outcomes still blocking release-readiness

**Size**
- Reopen trigger: the built image measured **2.1GB** when Diana pulled it on 2026-06-25 — attributed to bundled OCR/Tesseract dependencies plus the full Ubuntu base.
- Target: **~450MB** GA. A CISO offline review on 2026-06-25 (`CMT-2026-06-002`) added a **dual gate** — an interim release candidate may ship at **800MB once CVE-clean**, while GA stays at ~450MB; the two thresholds must be tracked separately and not conflated on the release checklist.
- Remediation attempted, none sufficient: multi-stage build (2026-08-01/04), base swap `ubuntu:22.04` → `alpine:latest` with `gcompat` for the glibc/musl issue (2026-08-04), removal of unused OCR and runtime packages (2026-08-07).
- Latest measured outcome — **2026-08-12 verification: still over the ~450MB target.** Evan attributes remaining bloat to "fluff in the Python site-packages layer." No newer size measurement exists in the record, so the 08-12 result stands as of 09-22.

**CVE**
- **CVE verification is still failing / outstanding** as of the same 2026-08-12 check; Evan had not yet identified what trips the scan. Note this is distinct from the completed T010 security audit (CIPH-20), where the medium-severity CORS `*` origin finding was patched to `ALLOWED_ORIGINS` and confirmed by 2026-07-15 re-scans — that closure does **not** cover the image CVE gate.
- Diana's standing rule: reopened status holds until **both** size and CVE are clean.

**Release consequence**
- T005 is a hard dependency of T011 (Release v1.0 gates, `CIPH-21`), which sits under a security-gate hold alongside T029 Windows code-signing. The 2026-09-15 pre-release audit (`SRC-MEET-10`) reconfirmed Docker slim/CVE as an open blocker, and the release board set a **hard no-ship after 2026-10-15** if T005 and T029 are not green (`CMT-2026-09-002`, non-advisory).
- The 09-22 brief's follow-up action is still "finish Alpine/CVE Docker verification."

Supporting files: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-06.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-09.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-21-Release-v1-Gates.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-07-12-Release-Checklist.md`.
