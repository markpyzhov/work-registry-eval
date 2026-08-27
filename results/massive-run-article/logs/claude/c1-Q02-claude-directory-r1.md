# Docker packaging was once treated as finished. As of **2026-09-22**, what is the authoritative status of that work, what earlier completion claim does it supersede, and what concrete size and CVE outcomes still prevent calling the image release-ready?

<!-- RESPONSE_START -->

## Answer — Docker packaging (T005 / CIPH-15) as of 2026-09-22

### 1. Authoritative status: reopened and still active — not done

The authoritative Work State for this area is **WS-03: Packaging, Release gating, and Security** (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md`, Last Updated 2026-09-22; index as-of timestamp 2026-09-22T12:00:00Z in `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/index.md`).

- `T005` (mapped to CIPH-15) is an **unchecked/open** task in WS-03's task list, listed under Active Work as **"reopened/active"**. Owner: **Evan**; area priority **P0**.
- The ClickUp record agrees: CIPH-15 status is **"Active (Reopened)"**, assignee Evan (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-15-Docker-Packaging.md`).
- The index's "Active / Reopened" line explicitly names **T005 (Docker size/CVE)** (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/index.md`).
- The 2026-09-22 daily brief still carries it as an open security gate against the release (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md`), with the follow-up action "Secure Authenticode cert and finish Alpine/CVE Docker verification."

### 2. The earlier completion claim it supersedes

The superseded claim is the **June 16, 2026 "Docker Packaging — Initial Dockerfile Complete" release-notes draft** (SRC-GDOC-06 / DOC-2006, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-06-16-Docker-Release-Notes.md`), which declared T005's first milestone complete — a working Dockerfile packaging both API and CLI entry points. That document itself conceded that neither a size review nor a CVE check had yet been run against the build.

WS-03's "Decisions and Superseded Directions" records the reversal explicitly: **"CIPH-15 was initially completed at ~800MB, then superseded and reopened on June 25 when OCR bundling pushed the image to 2.1GB. `(S1 supersedes S3)`"** — i.e., the Slack size-review thread (SRC-SLACK-06, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-06-25-docker-size.md`) supersedes the June 16 completion notes. Diana pulled the image on 2026-06-25, measured **2.1GB**, and reopened the task.

### 3. Concrete size and CVE outcomes still blocking release-readiness

**Size — two separate gates, neither met.** Per CISO offline review recorded in `CMT-2026-06-002` (2026-06-25, author Evan, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-06.md`), there are **dual size gates**: an interim release candidate may ship at **800MB but only once CVE-clean**, while the **GA target remains ~450MB**. The comment warns not to conflate the two thresholds on the release checklist; WS-03 says to track both separately.

Remediation history and outcome (SRC-SLACK-06, CIPH-15):
- 2.1GB after OCR/Tesseract dependency bundling (full `ubuntu:22.04` base identified as much of the bloat).
- Evan added a **multi-stage build** (build-time deps stripped from the final artifact) — still left the base layer too large.
- Swapped base to **`alpine:latest`** (glibc/musl issues worked around with `gcompat`) — "didn't get us all the way there either."
- Removed unused **OCR and runtime packages** not shipped in this build.
- **2026-08-12 verification (Diana): still over the ~450MB target**, with remaining "fluff in the Python site-packages layer." No later size measurement exists in the package, so 2026-08-12 remains the last recorded measurement as of 2026-09-22.

**CVE — verification still failing.** The same 2026-08-12 check found **CVE verification still failing**, with Evan yet to identify what trips the scan. WS-03 states as of August 12 that "the image still exceeds the ~450MB target and CVE verification is failing." CIPH-15's acceptance criteria are unmet on both counts: image size reduced to ~450MB (**not met**) and CVE verification passes with no outstanding findings (**not met**); the task "stays Active (Reopened) until both size and CVE checks pass." Diana: reopened status stands until both size and CVE are clean.

Note the interaction: because the 800MB RC allowance is conditional on being **CVE-clean**, the failing CVE scan means *neither* the RC nor the GA gate can be claimed today.

### 4. Downstream consequence — the release itself

- **T011 / CIPH-21 (Release v1.0 gates)** is active under a **security-gate hold** and cannot close until T005 (Docker size/CVE) and T029 (Windows code-signing) are green (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-21-Release-v1-Gates.md`; `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md`).
- The **2026-09-15 pre-release audit** (SRC-MEET-10, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md`) keeps Docker slim/CVE open alongside Windows signing and the audit-log schema mismatch: "Release isn't opening with any of those unresolved."
- **Hard deadline**: `CMT-2026-09-002` (Diana, 2026-09-15, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-09.md`) records a release-board decision of **no-ship after 2026-10-15** if T005 and T029 are not green — explicitly "not advisory."
- The **July 12 release checklist** (SRC-GDOC-05, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-07-12-Release-Checklist.md`) already listed T005 as the only unmet dependency among T001–T006 and T010.

### Bottom line
As of 2026-09-22, Docker packaging is **not finished** — it is **Active (Reopened)** under Evan, superseding the 2026-06-16 "initial Dockerfile complete" release-notes claim (~800MB milestone), which was overturned on 2026-06-25 when the OCR-bundled image measured **2.1GB**. Multi-stage builds, the Alpine base swap, and OCR/runtime package removal reduced it, but the last recorded verification (2026-08-12) shows the image **still above the ~450MB GA target with CVE verification failing** — and since the 800MB RC allowance requires a CVE-clean image, neither gate is satisfied. This keeps the v1.0 release under a security-gate hold against a hard **2026-10-15 no-ship deadline**.
