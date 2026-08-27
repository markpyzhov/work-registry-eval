# Docker packaging was once treated as finished. As of **2026-09-22**, what is the authoritative status of that work, what earlier completion claim does it supersede, and what concrete size and CVE outcomes still prevent calling the image release-ready?

<!-- RESPONSE_START -->

## Answer

**Authoritative status as of 2026-09-22: still open — "Active (Reopened)".** Docker packaging (T005 / ClickUp CIPH-15, owner Evan, WS-03) is *not* complete and is not release-ready. No source record dated on or after 2026-09-15 moves it; the most recent status evidence is the 2026-09-15 pre-release audit, where Alice opened the gate check with Docker slim-down and CVE work "still open," and the team explicitly agreed nobody closes those gates. Records dated 2026-09-22 in the dataset concern the node-sync handshake, not Docker, so nothing supersedes the reopened status by that date.

**The earlier completion claim it supersedes:** the 2026-06-16 milestone document "Docker Packaging — Initial Dockerfile Complete" (SRC-GDOC-06 / DOC-2006), which announced a working Dockerfile packaging both the API and CLI entry points into a single image. That document was itself explicit that the milestone was not release-readiness — it flagged that a size review and a CVE check still needed to run, and that neither had run against that build. On 2026-06-25 Diana pulled the image, found it at 2.1GB, and reopened the task; the current CIPH-15 record and the 2026-07-12 release checklist both carry T005 as "Active (Reopened) — reopened 2026-06-25 on image size/CVE review; not yet met."

**Concrete size and CVE outcomes still blocking release-ready status:**

- **Size:** the built image measured **2.1GB** against a target of **~450MB** (set so it fits on standard dev laptops / local runtime deployments). Evan's remediation sequence — a multi-stage build stripping build-time dependencies (2026-08-01), swapping the base from `ubuntu:22.04` to `alpine:latest` with `gcompat` to bridge glibc/musl (2026-08-04), and removing unused OCR and runtime packages (2026-08-07) — did not close the gap. At Diana's 2026-08-12 verification the image was **still over the ~450MB target**, with remaining bloat identified in the Python site-packages layer.
- **CVE:** CVE verification was never closed out on the original build and **is still failing** as of the 2026-08-12 scan. Evan had not yet identified what is tripping the scan. CIPH-15's acceptance criteria require "CVE verification passes with no outstanding findings" — recorded as not yet met.
- **Gate rule:** Diana's standing position is that the reopened status holds until *both* the size and the CVE check are clean; CIPH-15 states the task stays Active (Reopened) until both pass.

**Downstream impact:** T005 is a blocking dependency for the v1.0 release checklist (T011 / CIPH-21). The 2026-07-12 checklist recorded six of seven dependency gates met with T005 the sole unmet item. CIPH-21 remains Active under Diana's security-gate hold pending both T005 (Docker size/CVE) and T029 (Windows code-signing), and the 2026-09-02 Windows compatibility audit confirms the checklist is holding on the signing gap "alongside the T005 image slim-down."

**Sources cited:** SRC-GDOC-06 (`med-synth/documentation/sources/2026-06-16-Docker-Release-Notes.md`); SRC-SLACK-06 (`med-synth/communication/sources/slack/2026-06-25-docker-size.md`); SRC-CU-CIPH-15 (`med-synth/tasks/CIPH-15-Docker-Packaging.md`); SRC-GDOC-05 (`med-synth/documentation/sources/2026-07-12-Release-Checklist.md`); SRC-CU-CIPH-21 (`med-synth/tasks/CIPH-21-Release-v1-Gates.md`); SRC-MEET-10 (`med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md`); SRC-GDOC-39 (`med-synth/documentation/sources/2026-09-02-Windows-Compatibility-Audit-Report.md`).

*Note on the as-of date:* the dataset contains no Docker-specific record dated 2026-09-22 itself. The 2026-09-22 sources (Fireflies handshake deep dive SRC-MEET-11, Slack SRC-SLACK-27, CIPH-34) cover the node-sync handshake block only. The status above is therefore the latest authoritative Docker record standing as of that date, not a record written on it.
