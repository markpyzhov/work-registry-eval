# Docker packaging was once treated as finished. As of **2026-09-22**, what is the authoritative status of that work, what earlier completion claim does it supersede, and what concrete size and CVE outcomes still prevent calling the image release-ready?

<!-- RESPONSE_START -->

**Answer**

**Authoritative status as of 2026-09-22: Docker packaging is NOT finished — it is Active (Reopened) and still an open release gate.**

Note on the date itself: no Docker-specific event is recorded on 2026-09-22 in the dataset (the 2026-09-22 records — SRC-MEET-11 and SRC-SLACK-27 — concern the node-sync handshake timeout, a different workstream). The authoritative Docker position standing on that date is the one carried forward from the last Docker-related evidence: the ClickUp task record and the 2026-09-15 pre-release gate review.

**1. Authoritative status**

- **CIPH-15 "Docker Packaging" (T005), owner Evan — Status: Active (Reopened)** (SRC-CU-CIPH-15). Its acceptance criteria explicitly state the task "stays Active (Reopened) until both size and CVE checks pass," and both are recorded as "not yet met."
- The most recent gate review before 2026-09-22 — the **Pre-Release Audit of 2026-09-15** (SRC-MEET-10) — confirms it is still open. Alice: "Docker slim-down and CVE work is still open... Those stay on the board," and closes with "Security-gate work stays open... No one closes those today."
- **CIPH-21 "Release v1.0 Gates" (T011) remains Active** with the Docker size/CVE gate listed as one of two unresolved blockers (alongside T029 Windows code-signing), under Diana's security-gate hold (SRC-CU-CIPH-21). The 2026-09-02 Windows audit (SRC-GDOC-39) independently confirms the release checklist is "holding on this exact signing gap alongside the T005 image slim-down."

**2. The earlier completion claim it supersedes**

The superseded claim is the **2026-06-16 document "Docker Packaging — Initial Dockerfile Complete" (SRC-GDOC-06 / DOC-2006, owner Evan)**, which announced T005's first milestone: a working Dockerfile packaging both the API and CLI entry points into a single image. That document was itself explicitly conditional — it stated that "before this can be treated as release-ready, the image needs a size review and a CVE check. Neither has run yet against this build."

That milestone was overtaken on **2026-06-25**, when Diana pulled the built image, measured it at 2.1GB, and reopened the task (SRC-SLACK-06; also reflected in the 2026-07-12 Release Checklist, SRC-GDOC-05, which marks T005 "Active (Reopened) — reopened 2026-06-25 on image size/CVE review; not yet met"). So "initial Dockerfile complete" (a build milestone) is not, and never was, "Docker packaging done."

**3. Concrete size and CVE outcomes that still prevent calling the image release-ready**

*Size:*
- Original built image measured **2.1GB** on 2026-06-25 — judged far too large for local runtime deployment.
- Agreed target: **~450MB** (so the image fits on standard dev laptops).
- Remediation attempts, none of which reached the target:
  - Multi-stage build stripping build-time dependencies from the final artifact (2026-08-01) — "the multi-stage split alone still leaves the base layer too large."
  - Base image swapped from `ubuntu:22.04` to `alpine:latest`, with `gcompat` used to resolve glibc-vs-musl issues (2026-08-04) — "didn't get us all the way there either."
  - Removal of unused OCR and runtime packages not shipped in this build (2026-08-07).
- At the **2026-08-12 verification**, Diana confirmed the image was **still over the ~450MB target**. Evan attributed the remaining bulk to "fluff in the Python site-packages layer." No later measurement showing the target met appears anywhere in the dataset.

*CVE:*
- CVE verification was **never run against the original build** (per the 2026-06-16 doc) and was still not closed out as of 2026-08-01.
- At the **2026-08-12 scan**, Diana reported the **CVE verification is still failing**; Evan had not yet identified the root cause ("I need to chase down what's tripping the CVE scan"). The specific CVEs are not identified in any retrieved source.
- CIPH-15's acceptance criterion "CVE verification passes with no outstanding findings" is recorded as **not yet met**, and CVE work was still listed as open at the 2026-09-15 pre-release audit.

Diana's standing rule (2026-08-12): "Reopened status stands until both the size and the CVE check are clean."

**Sources cited:** SRC-CU-CIPH-15 (`med-synth/tasks/CIPH-15-Docker-Packaging.md`); SRC-GDOC-06 / DOC-2006 (`med-synth/documentation/sources/2026-06-16-Docker-Release-Notes.md`); SRC-SLACK-06 (`med-synth/communication/sources/slack/2026-06-25-docker-size.md`); SRC-GDOC-05 / DOC-2005 (`med-synth/documentation/sources/2026-07-12-Release-Checklist.md`); SRC-MEET-10 (`med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md`); SRC-CU-CIPH-21 (`med-synth/tasks/CIPH-21-Release-v1-Gates.md`); SRC-GDOC-39 / DOC-2039 (`med-synth/documentation/sources/2026-09-02-Windows-Compatibility-Audit-Report.md`).
