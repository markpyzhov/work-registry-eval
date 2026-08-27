# Docker packaging was once treated as finished. As of **2026-09-22**, what is the authoritative status of that work, what earlier completion claim does it supersede, and what concrete size and CVE outcomes still prevent calling the image release-ready?

<!-- RESPONSE_START -->

I have everything needed. Here is the complete answer.

---

## Authoritative status as of 2026-09-22

**Docker packaging (T005, mapped to ClickUp CIPH-15) is reopened/active — not done.** This is the state recorded in the authoritative Work State `WS-03: Packaging, Release gating, and Security` (Status: `in_progress`, Priority P0, Owner: Evan, Project: CipherDoc, Last Updated 2026-09-22). In the WS-03 Task List, `T005` is an **unchecked** item; the ClickUp record CIPH-15 carries status **"Active (Reopened)"** with assignee Evan.

WS-03 as a whole remains `in_progress`, and the release gate task `T011 / CIPH-21` (Release v1.0.0 gates) is **active under a security-gate hold**, explicitly because it cannot close until T005 (Docker size/CVE) and T029 (Windows code-signing certificate) are green.

## The earlier completion claim it supersedes

The superseded claim is the **Docker Release Notes Draft of 2026-06-16** (`SRC-GDOC-06`, "Docker Packaging — Initial Dockerfile Complete", DOC-2006, owner Evan), which announced the initial Dockerfile as complete — a working Dockerfile packaging both API and CLI entry points into a single image. Notably, that same note itself warned that "before this can be treated as release-ready, the image needs a size review and a CVE check," and that neither had yet run against the build.

WS-03's "Decisions and Superseded Directions" section records this explicitly:

> **Reopened Docker Task**: CIPH-15 was initially completed at ~800MB, then superseded and reopened on June 25 when OCR bundling pushed the image to 2.1GB. `(S1 supersedes S3)`

So the ~800MB "complete" state documented on 2026-06-16 (`S3` = `SRC-GDOC-06`) is superseded by the 2026-06-25 Slack reopening thread (`S1` = `SRC-SLACK-06`), where Diana pulled the latest `cipherdoc` image, measured **2.1GB**, called it far too big for local-runtime deployment, and reopened the task.

## Concrete size and CVE outcomes still blocking release-readiness

**Size:**
- The image ballooned from ~800MB to **2.1GB** after OCR dependencies were bundled (measured 2026-06-25).
- Remediation attempts, all insufficient on their own: multi-stage build stripping build-time dependencies from the final artifact (2026-08-01); base image swapped from `ubuntu:22.04` to `alpine:latest`, working around `glibc` vs `musl` via `gcompat` (2026-08-04); removal of unused OCR and runtime packages not shipped in the build (2026-08-07).
- At the **2026-08-12** verification, Diana confirmed the image was **still over the ~450MB target**. Evan attributed the residual bloat to leftover "fluff in the Python site-packages layer."
- **Dual size gates apply** (per comment `CMT-2026-06-002`, authored by Evan 2026-06-25, from CISO review): an interim release candidate may ship at **800MB once CVE-clean**, while the **GA target remains ~450MB**. The two thresholds must be tracked separately and not conflated on the release checklist. Neither threshold is currently reported as met with a CVE-clean scan.

**CVE:**
- CVE verification for the image is **failing / outstanding**. It was never closed out even before the size regression (Evan, 2026-08-01: the CVE verification had still not been closed out), and at the 2026-08-12 scan Diana reported the **CVE verification still failing**. Evan had not yet identified what was tripping the scan.
- CIPH-15's acceptance criteria state both gates as unmet: image size reduced to the ~450MB target (**not yet met**), and CVE verification passing with no outstanding findings (**not yet met**). The task stays "Active (Reopened)" until both pass — Diana's standing rule from 2026-08-12: reopened status stands until both the size and the CVE check are clean.

**Important distinction:** the *application-level* security audit (`T010 / CIPH-20`) **is** complete and is checked off in WS-03 — the medium-severity CORS `*` origin finding from the July 6 scan report was patched by restricting to configured `ALLOWED_ORIGINS`, and July 15 re-scans confirmed the patch holds, supplemented by a RedByte pen-test attestation letter dated 2026-07-11 in the release evidence pack. That completed audit does **not** clear the separate, still-failing Docker **image** CVE verification under T005.

**Release consequence:** the September 15 pre-release audit lists Docker slim/CVE work, Windows signing, and audit-log schema alignment as open blockers. Per comment `CMT-2026-09-002`, the release board set a **hard no-ship after 2026-10-15** if T005 and T029 are not green. The July 12 release checklist likewise shows T005 as the only unmet dependency of seven — six of seven gates met.

**Next update needed** (per WS-03): Docker multi-stage build progress, final CVE scan results, and release gate clearance.

## Records cited

- `work-states/WS-03-ops.md` (path: `work-state`) — authoritative status, Task List, Active Work, Done/Evidence, Decisions and Superseded Directions, Blockers and Dependencies, Next Update Needed
- `work-states/comments/2026-06.md` (path: `comments`) — `CMT-2026-06-002` (dual RC/GA size gates)
- `med-synth/communication/sources/slack/2026-06-25-docker-size.md` — `S1` / `SRC-SLACK-06`
- `med-synth/tasks/CIPH-15-Docker-Packaging.md` — `S2` / `SRC-CU-CIPH-15`
- `med-synth/documentation/sources/2026-06-16-Docker-Release-Notes.md` — `S3` / `SRC-GDOC-06` (the superseded completion claim)
- `med-synth/documentation/sources/2026-07-12-Release-Checklist.md` — `S7` / `SRC-GDOC-05`
