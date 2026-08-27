# Docker packaging was once treated as finished. As of **2026-09-22**, what is the authoritative status of that work, what earlier completion claim does it supersede, and what concrete size and CVE outcomes still prevent calling the image release-ready?

<!-- RESPONSE_START -->

## Answer: Docker packaging (T005 / CIPH-15) as of 2026-09-22

### 1. Authoritative status — still open, not done

Per the authoritative Work State `WS-03: Packaging, Release gating, and Security` (Last Updated **2026-09-22**, Status `in_progress`, Owner Evan, P0), Docker packaging is **reopened / active**, and the ClickUp record carries status **"Active (Reopened)"**, assignee Evan.

- The Work State Index (as-of `2026-09-22T12:00:00Z`) lists **T005 (Docker size/CVE)** under "Active / Reopened" — it is *not* in Done.
- `T005` is unchecked in the WS-03 task list: `- [ ] T005 (mapped to CIPH-15)`.
- The 2026-09-15 pre-release audit re-confirmed Docker slim-down/CVE as an open gate: "Security-gate work stays open — Docker slim-down, Windows signing... No one closes those today."
- The 2026-09-22 daily brief repeats it as the #1 priority: security-gate hold, Docker size/CVE (T005) plus Windows signing (T029), against a **hard 2026-10-15 no-ship deadline** (release board decision, not advisory).

Files: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/index.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-15-Docker-Packaging.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md`

### 2. The superseded completion claim

The superseded claim is the **2026-06-16 Google Doc "Docker Packaging — Initial Dockerfile Complete" (`SRC-GDOC-06` / DOC-2005-adjacent DOC-2006)**, which declared T005's first milestone reached with a working Dockerfile packaging both API and CLI entry points. That document itself caveated that "the image needs a size review and a CVE check. Neither has run yet against this build."

WS-03 records the supersession explicitly under Decisions and Superseded Directions: *"CIPH-15 was initially completed at ~800MB, then superseded and reopened on June 25 when OCR bundling pushed the image to 2.1GB. (S1 supersedes S3)"* — i.e., the **2026-06-25 Slack thread `SRC-SLACK-06` supersedes the 2026-06-16 release notes**. Diana reopened the task on 2026-06-25 after pulling the built image.

Files: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-06-16-Docker-Release-Notes.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-06-25-docker-size.md`

### 3. Concrete size and CVE outcomes blocking release-readiness

**Size**

| Milestone | Figure |
|---|---|
| Initial "complete" build (2026-06-16) | ~800MB |
| After OCR/Tesseract deps bundled — measured 2026-06-25 | **2.1GB** |
| GA target | **~450MB** |
| Interim RC ceiling (CISO dual-gate, `CMT-2026-06-002`) | **800MB, only once CVE-clean** |
| Verified state at 2026-08-12 (latest measurement on record) | **still over the ~450MB target** — no passing number recorded |

Evan's remediation sequence, none of which closed the gap: multi-stage build stripping build-time deps (2026-08-01/04) → base image swap from `ubuntu:22.04` to `alpine:latest` with `gcompat` for the glibc/musl issue (2026-08-04) → removal of unused OCR and runtime packages (2026-08-07). Evan's own diagnosis on 2026-08-12: *"There's still fluff in the Python site-packages layer."*

Note the **dual-gate rule** from the CISO offline review (`CMT-2026-06-002`, 2026-06-25): the 800MB RC threshold and the ~450MB GA threshold must be tracked separately and not conflated on the release checklist. Even the looser RC gate is conditional on CVE-clean, which has not been achieved.

**CVE**

- CVE verification has **never passed** against this image. It was never run against the 2026-06-16 "complete" build.
- Diana ran the scan on **2026-08-12**: *"We're still over the ~450MB target, and the CVE verification is still failing."* No specific CVE IDs or counts are recorded in the package — Evan stated he still needed "to chase down what's tripping the CVE scan."
- Diana's ruling: *"Reopened status stands until both the size and the CVE check are clean."* CIPH-15's acceptance criteria mirror this — both the size and CVE criteria are explicitly marked "(not yet met)," and the task stays Active (Reopened) until both pass.
- The distinct security work that *did* pass (T010 / CIPH-20 — CORS `*` origin fix, re-scanned clean 2026-07-15, plus a RedByte pen-test attestation letter dated 2026-07-11) is a separate gate and does **not** satisfy the Docker image CVE verification.

**Downstream consequence:** the 2026-07-12 Release Checklist names T005 as the *only* unmet dependency of the seven checklist gates (T001–T006, T010); CIPH-21 remains Active with a security-gate hold pending T005 and T029. The 2026-09-22 open follow-up is "finish Alpine/CVE Docker verification."

Files: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-06-25-docker-size.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-06.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-09.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-07-12-Release-Checklist.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-21-Release-v1-Gates.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-06-25-daily-brief.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-08-12-daily-brief.md`

### Evidence gap worth flagging

No source in the package records a **post-2026-08-12 measured image size or CVE scan result**. The 2026-09-15 audit and 2026-09-22 brief confirm the gate is still open but add no new numbers, so 2.1GB (last hard measurement) and "over ~450MB / CVE failing" (2026-08-12 verification) are the most recent quantitative facts available as of 2026-09-22.
