# Docker packaging was once treated as finished. As of **2026-09-22**, what is the authoritative status of that work, what earlier completion claim does it supersede, and what concrete size and CVE outcomes still prevent calling the image release-ready?

<!-- RESPONSE_START -->

I have sufficient evidence. Here is the complete answer.

---

## Authoritative status as of 2026-09-22

**Docker packaging (T005 / ClickUp CIPH-15, under Work State WS-03 "Packaging, Release gating, and Security") is NOT finished — it is reopened and actively in progress.**

- WS-03 (Owner: Evan, Project: CipherDoc, Priority P0, Last Updated 2026-09-22) carries `T005` as an **unchecked** task item in its Task List, and lists it under **Active Work**: "Docker packaging is **reopened/active**."
- The ClickUp record CIPH-15 (`SRC-CU-CIPH-15`) shows **Status: Active (Reopened)**, assignee Evan, with acceptance criteria explicitly marked "not yet met" and the rule that the task "stays Active (Reopened) until both size and CVE checks pass."
- The 2026-07-12 Release Checklist (`SRC-GDOC-05`) likewise lists T005 Docker Packaging as **"Active (Reopened) — reopened 2026-06-25 on image size/CVE review; not yet met,"** and calls it the single unmet dependency out of seven release gates.

## The earlier completion claim it supersedes

The superseded claim is the **2026-06-16 Docker Release Notes draft (`SRC-GDOC-06` / `S3`, DOC-2006)**, which announced that the initial Dockerfile was complete — a working Dockerfile packaging both the API and CLI entry points into a single image. That document itself flagged that "before this can be treated as release-ready, the image needs a size review and a CVE check. Neither has run yet against this build."

WS-03's **Decisions and Superseded Directions** section records the supersession explicitly:

> "**Reopened Docker Task**: CIPH-15 was initially completed at ~800MB, then superseded and reopened on June 25 when OCR bundling pushed the image to 2.1GB. `(S1 supersedes S3)`"

So the June 16 "initial Dockerfile complete" milestone (`S3`) is superseded by the June 25 Slack size-optimization thread (`SRC-SLACK-06` / `S1`), in which Diana pulled the latest `cipherdoc` image, measured **2.1GB**, called it "way too big for a local runtime deployment," and reopened the packaging task.

## Concrete size and CVE outcomes that still block release-readiness

**Size:**
- Initial completion claim sat at **~800MB**; OCR dependency bundling then pushed the built image to **2.1GB** (measured 2026-06-25) — the trigger for reopening.
- Target is **~450MB** for GA. Remediation attempts, all insufficient on their own:
  - **2026-08-01** — multi-stage build plan put in place, stripping build-time dependencies from the final artifact.
  - **2026-08-04** — multi-stage split alone still left the base layer too large; base image swapped from `ubuntu:22.04` to `alpine:latest` (glibc vs. musl issues worked around with `gcompat`).
  - **2026-08-07** — Alpine swap still fell short; unused OCR and runtime packages removed.
- **2026-08-12 verification (Diana):** the image is **still over the ~450MB target**. Evan's diagnosis: "There's still fluff in the Python site-packages layer."

**CVE:**
- CVE verification for the image was **never closed out** even at the 2.1GB stage (Evan, 2026-08-01: "we still haven't closed out the CVE verification either").
- **2026-08-12 CVE scan result: still failing.** Evan had not yet identified the cause — "I need to chase down what's tripping the CVE scan." No specific CVE identifiers are recorded in the dataset.
- CIPH-15 acceptance criterion "CVE verification passes with no outstanding findings" is marked **not yet met**; as of the 2026-08-12 verification, CVE verification "remains outstanding."
- Note the distinction: the *separate* security-audit task T010 / CIPH-20 **is** complete (medium-severity CORS `*` origin issue from the July 6 scan patched to configured `ALLOWED_ORIGINS`, re-verified 2026-07-15, plus a RedByte pen-test attestation letter dated 2026-07-11 in the evidence pack). That completion does **not** cover the Docker image CVE gate, which remains failing.

**Dual size gates (important nuance):** Per comment `CMT-2026-06-002` (Evan, 2026-06-25, applied to WS-03/T005), a CISO review established **two separate thresholds**: an interim release candidate may ship at **800MB once CVE-clean**, while the **GA target remains ~450MB**. The comment warns not to conflate the two on the release checklist. Even the interim RC gate is unreachable today because CVE verification is failing.

**Standing status per Diana (2026-08-12):** "Reopened status stands until both the size and the CVE check are clean."

## Downstream release impact

- **T011 / CIPH-21 (Release v1.0.0 gates)** cannot close until T005 (Docker size/CVE) and **T029** (Windows code-signing certificate) are green. Diana has placed a **security-gate hold** on the release.
- The **2026-09-15 pre-release audit** (`SRC-MEET-10`) confirms Docker slim-down/CVE work was still open at that date, alongside Windows signing and an audit-log schema mismatch. Alice: "Security-gate work stays open... No one closes those today."
- Comment `CMT-2026-09-002` (Diana, 2026-09-15): the release board set a **hard no-ship deadline after 2026-10-15** if T005 and T029 are not green — "Hard deadline — not advisory."
- WS-03's **Next Update Needed**: Docker multi-stage build progress, final CVE scan results, and release gate clearance.

**Caveat on recency:** the newest dated evidence for the Docker size/CVE measurements themselves is **2026-08-12**; the 2026-09-15 audit and the 2026-09-22 Work State both confirm the work remains open, but the dataset contains no post-August measurement of a specific image size or a named CVE.

## Records cited

`work-states/WS-03-ops.md` (path `work-state`, Last Updated 2026-09-22) · `med-synth/tasks/CIPH-15-Docker-Packaging.md` (`SRC-CU-CIPH-15`, S2) · `med-synth/documentation/sources/2026-06-16-Docker-Release-Notes.md` (`SRC-GDOC-06`, S3 — superseded) · `med-synth/communication/sources/slack/2026-06-25-docker-size.md` (`SRC-SLACK-06`, S1) · `med-synth/documentation/sources/2026-07-12-Release-Checklist.md` (`SRC-GDOC-05`, S7) · `med-synth/tasks/CIPH-21-Release-v1-Gates.md` (`SRC-CU-CIPH-21`, S8) · `med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md` (`SRC-MEET-10`, S9) · `med-synth/tasks/CIPH-20-Security-Audit.md` (`SRC-CU-CIPH-20`, S5) · `med-synth/communication/sources/slack/2026-07-10-security-patch.md` (`SRC-SLACK-09`, S4) · comments `CMT-2026-06-002`, `CMT-2026-07-002`, `CMT-2026-09-002`.
