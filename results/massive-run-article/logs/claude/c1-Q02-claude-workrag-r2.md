# Docker packaging was once treated as finished. As of **2026-09-22**, what is the authoritative status of that work, what earlier completion claim does it supersede, and what concrete size and CVE outcomes still prevent calling the image release-ready?

<!-- RESPONSE_START -->

I have complete evidence. Here is the answer.

---

## Authoritative status as of 2026-09-22

**Docker packaging (T005, mapped to ClickUp CIPH-15) is NOT complete — it is reopened and active, and it remains an open P0 item.**

The governing Work State is **WS-03: Packaging, Release gating, and Security** (Status: `in_progress`, Priority: P0, Owner: Evan, Project: CipherDoc, Last Updated: 2026-09-22). In its task list, `T005` is explicitly unchecked, and its Active Work section states that Docker packaging is "**reopened/active**." The underlying ClickUp record CIPH-15 carries status **Active (Reopened)**, assigned to Evan, with acceptance criteria stating that the task "stays Active (Reopened) until both size and CVE checks pass."

## The earlier completion claim it supersedes

The superseded claim is the **Docker Release Notes Draft of 2026-06-16** (`SRC-GDOC-06` / DOC-2006, "Docker Packaging — Initial Dockerfile Complete"), which announced that T005 had reached its first milestone with a working Dockerfile packaging both the API and CLI entry points into a single image. Notably, even that document conceded the caveat: before it could be treated as release-ready, the image needed a size review and a CVE check, and "neither has run yet against this build."

WS-03's **Decisions and Superseded Directions** section records the supersession explicitly:

> "**Reopened Docker Task**: CIPH-15 was initially completed at ~800MB, then superseded and reopened on June 25 when OCR bundling pushed the image to 2.1GB. `(S1 supersedes S3)`"

So the June 16 completion note (S3) is superseded by the June 25 Slack thread on Docker image size optimization (S1, `SRC-SLACK-06`), in which Diana pulled the latest `cipherdoc` image, found it at 2.1GB, and reopened the packaging task. The 2026-07-12 Release Checklist (`SRC-GDOC-05`) reflects the same reversal, listing T005 as "**Active (Reopened)** — reopened 2026-06-25 on image size/CVE review; not yet met," and calling it the single unmet dependency out of seven gates for T011.

## Concrete size and CVE outcomes still preventing release-readiness

**Size outcomes — target still missed:**
- Original "complete" build measured **~800MB**.
- Image then ballooned to **2.1GB** after OCR dependencies were bundled — the trigger for reopening on 2026-06-25.
- Evan's remediation sequence, all of which fell short: a **multi-stage build** stripping build-time dependencies from the final artifact (2026-08-01); a **base image swap from `ubuntu:22.04` to `alpine:latest`** using `gcompat` to resolve glibc-vs-musl issues (2026-08-04); and **removal of unused OCR and runtime packages** not shipped in the build (2026-08-07).
- At the **2026-08-12** verification, Diana confirmed the image was **still over the ~450MB target**. Evan attributed the remaining bulk to "fluff in the Python site-packages layer."
- **Two distinct size thresholds apply** and must not be conflated (per CMT-2026-06-002, a CISO review recorded by Evan on 2026-06-25): an **interim release candidate may ship at 800MB once CVE-clean**, while the **GA target remains ~450MB**. WS-03 directs that both thresholds be tracked separately. Neither gate is cleared, because the CVE precondition on the 800MB RC path is itself unmet.

**CVE outcomes — verification still failing:**
- CVE verification was never closed out against the packaged image; Evan flagged on 2026-08-01 that it remained outstanding alongside the size problem.
- At the **2026-08-12** scan, Diana reported the **CVE verification was still failing**, and Evan had yet to identify what was tripping the scan.
- CIPH-15's acceptance criteria record both gates as unmet: image size reduced to ~450MB — **not yet met**; CVE verification passing with no outstanding findings — **not yet met**.
- Diana's ruling stands: "Reopened status stands until both the size and the CVE check are clean."

**Important distinction:** the separate security-audit task **T010 / CIPH-20 is complete** (a medium-severity CORS `*` origin issue found in the 2026-07-06 scan report was patched by restricting to configured `ALLOWED_ORIGINS`, with re-scans on July 15 confirming the fix, supplemented by a RedByte pen-test attestation letter dated 2026-07-11). That completed application-security audit does **not** discharge the image-level CVE verification gate on T005, which remains failing.

## Downstream release impact

Because T005 is unmet, the v1.0.0 release gate **T011 / CIPH-21** is active under a security-gate hold. The 2026-09-15 pre-release audit (`SRC-MEET-10`) confirmed that "Docker slim-down and CVE work is still open," alongside Windows signing and an audit-log schema mismatch; Alice closed that meeting with "No one closes those today." T011 cannot close until T005 (Docker size/CVE) and T029 (Windows code-signing certificate) are green, and the release board has set a **hard no-ship after 2026-10-15** if both are not green (CMT-2026-09-002, Diana, 2026-09-15 — recorded as a hard deadline, not advisory). WS-03's "Next Update Needed" is precisely "Docker multi-stage build progress, final CVE scan results, and release gate clearance."

**Bottom line:** the image cannot be called release-ready because it is still above the ~450MB GA target with no measured post-remediation size on record, its CVE verification is actively failing as of the last recorded check (2026-08-12), and the 800MB interim-RC concession is gated on CVE-cleanliness that has not been achieved.

---

**Dataset records cited:** `work-states/WS-03-ops.md` (Task List, Active Work, Decisions and Superseded Directions, Blockers and Dependencies, Done/Evidence, Next Update Needed); `med-synth/tasks/CIPH-15-Docker-Packaging.md` (SRC-CU-CIPH-15); `med-synth/documentation/sources/2026-06-16-Docker-Release-Notes.md` (SRC-GDOC-06); `med-synth/communication/sources/slack/2026-06-25-docker-size.md` (SRC-SLACK-06); `med-synth/documentation/sources/2026-07-12-Release-Checklist.md` (SRC-GDOC-05); `med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md` (SRC-MEET-10); `work-states/comments/2026-06.md` (CMT-2026-06-002); `work-states/comments/2026-09.md` (CMT-2026-09-002).
