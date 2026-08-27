# Docker packaging was once treated as finished. As of **2026-09-22**, what is the authoritative status of that work, what earlier completion claim does it supersede, and what concrete size and CVE outcomes still prevent calling the image release-ready?

<!-- RESPONSE_START -->

## Answer

**Authoritative status as of 2026-09-22: Docker packaging (T005 / ClickUp CIPH-15, "Docker Packaging", WS-03, owner Evan) is *Active (Reopened)* — not complete, not release-ready.**

A caveat on the date: no source record in this dataset carries a Docker-specific update dated exactly 2026-09-22 (the only 2026-09-22 records concern the node-sync handshake block, CIPH-34 / SRC-MEET-11 / SRC-SLACK-27). The latest Docker-bearing evidence standing as of that date is the 2026-09-15 pre-release audit and the CIPH-15 task record, both of which keep the task open.

**What the current status supersedes**

The reopened status supersedes the earlier completion claim of **2026-06-16**, when DOC-2006 ("Docker Packaging — Initial Dockerfile Complete", SRC-GDOC-06) declared T005's first milestone done: a working Dockerfile packaging both the API and CLI entry points into a single image. That same document already qualified the claim — before the image could be treated as release-ready it still needed a size review and a CVE check, and "neither has run yet against this build."

On **2026-06-25** Diana pulled the built `cipherdoc` image, measured it at **2.1GB**, and reopened the task on size/CVE review. Every downstream record since then carries the reopened status rather than the June completion: the 2026-07-12 release checklist (DOC-2005 / SRC-GDOC-05) lists T005 as "**Active (Reopened)** — reopened 2026-06-25 on image size/CVE review; not yet met," and calls it the *only* unmet dependency among T001–T006 and T010 (six of seven gates met).

**Concrete size and CVE outcomes still blocking release-readiness**

Two acceptance criteria on CIPH-15 remain explicitly *not yet met*:

1. **Size** — the target is **~450MB** (set by Evan on 2026-08-01 against the 2.1GB baseline, agreed by Diana as the threshold that would fit standard dev laptops). Four successive remediation steps failed to reach it:
   - 2026-08-01: multi-stage build plan stripping build-time dependencies out of the final artifact.
   - 2026-08-04: multi-stage split alone left the base layer too large → base swapped from `ubuntu:22.04` to `alpine:latest` (glibc vs. musl issues worked around with `gcompat`).
   - 2026-08-07: Alpine swap still insufficient → unused OCR and runtime packages removed.
   - **2026-08-12 verification (Diana):** the image is **still over the ~450MB target**. Evan attributes the remaining bloat to "fluff in the Python site-packages layer."
2. **CVE verification** — **still failing** as of the 2026-08-12 scan. Evan had not yet identified the cause ("I need to chase down what's tripping the CVE scan"). No passing CVE result appears anywhere later in the dataset; the criterion "CVE verification passes with no outstanding findings" remains unmet, and the specific CVEs are not identified in any source record.

Diana's ruling on 2026-08-12: "Reopened status stands until both the size and the CVE check are clean."

**Release impact**

T005 is not an isolated open item. The v1.0 release gate task (CIPH-21 / T011, Active) is held on a Diana security-gate hold pending *both* T005's Docker slim-down/CVE work and T029's Windows Defender/SmartScreen code-signing. The 2026-09-02 Windows compatibility audit (DOC-2039) confirms the release checklist "is holding on this exact signing gap alongside the T005 image slim-down." At the **2026-09-15** pre-release audit (SRC-MEET-10), Alice restated the gate check: "Docker slim-down and CVE work is still open," Windows signing still open, high-DPI still blocked upstream, plus an audit-log schema mismatch — "No one closes those today."

**Sources cited**

- SRC-CU-CIPH-15 — ClickUp task CIPH-15 "Docker Packaging" (`med-synth/tasks/CIPH-15-Docker-Packaging.md`) — status, acceptance criteria, remediation history
- SRC-GDOC-06 — DOC-2006, "Docker Packaging — Initial Dockerfile Complete," 2026-06-16 (`med-synth/documentation/sources/2026-06-16-Docker-Release-Notes.md`) — the superseded completion claim
- SRC-SLACK-06 — Slack #releases, "Docker Image Size Optimization," 2026-06-25 → 2026-08-12 (`med-synth/communication/sources/slack/2026-06-25-docker-size.md`) — 2.1GB, ~450MB target, remediation steps, 2026-08-12 size/CVE failure
- SRC-GDOC-05 — DOC-2005, "Release Checklist — v1.0 Gate Status (Draft)," 2026-07-12 (`med-synth/documentation/sources/2026-07-12-Release-Checklist.md`) — T005 as sole unmet dependency
- SRC-CU-CIPH-21 — ClickUp task CIPH-21 "Release v1.0 Gates" (`med-synth/tasks/CIPH-21-Release-v1-Gates.md`) — security-gate hold
- SRC-MEET-10 — Fireflies, "Pre-Release Audit," 2026-09-15 (`med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md`) — latest confirmation the gate is open
- SRC-GDOC-39 — DOC-2039, "Compatibility Audit: Windows Build Signing Gap," 2026-09-02 (`med-synth/documentation/sources/2026-09-02-Windows-Compatibility-Audit-Report.md`) — checklist held on signing gap alongside T005 slim-down
