# License compliance looked cleared after a PDF-parser swap, then changed again. As of **2026-09-22**, what is the current license-gate status, what discovery reopened it, and what replacement criteria are in force?

<!-- RESPONSE_START -->

## License gate status as of 2026-09-22

**Current status: still open — Active (Reopened), P0.** The task is *not* cleared despite the earlier parser swap.

- Work State `WS-04` (Regulatory Compliance, Privacy, and Audits; Last Updated 2026-09-22) lists **T030 / CIPH-40 as Reopened/active**, with Charlie searching for an Apache- or MIT-licensed alternative, and carries it as an open blocker (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md`).
- The work-state index for the same as-of timestamp (2026-09-22T12:00:00Z) lists T030 under "Active / Reopened — license search" (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/index.md`).
- The 2026-09-22 daily brief: "License compliance (T030) — P0 Legal AGPL/whole-bundle gate still open," and ranks "Close Legal gate on non-AGPL parser" as priority #3 (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md`).
- ClickUp CIPH-40 status: **Active (Reopened)**, assignee Diana, priority High (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-40-License-Compliance-Review.md`).

## What reopened it

Sequence:

1. **2026-08-09** — Diana ran the third-party license audit (recursive, transitive included) against the dependency manifests, flagging anything outside MIT/Apache/BSD (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-09-license-audit.md`). The original finding was **Ghostscript (AGPLv3)**, used by the `rasterizer` module for PDF-to-image conversion and on the corporate license blacklist for viral copyleft on binaries distributed to partner sites (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-08-21-License-Compliance-Audit-Report.md`).
2. **2026-08-11** — Evan swapped in a replacement PDF parser and marked the step done; Charlie asked whether he had verified the new library's license or taken the package listing at face value, and Evan conceded he had not looked hard enough (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-11-license-parser-swap.md`).
3. **2026-08-12 — the reopening discovery**: Diana verified the **replacement parser is itself AGPL-licensed** (checked the license file directly). The swap removed the specific Ghostscript dependency but reintroduced the same license category one layer down. She put the review back in progress until a replacement passes a clean scan (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-12-license-agpl-reopen.md`; corroborated in `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-08-21-License-Compliance-Review-Review.md`).
4. **2026-08-12 — escalation**: A Legal memo landed stating **AGPL anywhere in the bundle triggers whole-bundle copyleft exposure** under CipherDoc's distribution model. T030 was escalated to **P0** and made a **hard Legal gate** — an engineering library search alone is insufficient to close it (`CMT-2026-08-002`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-08.md`).
5. **2026-08-15** — Charlie reported a couple of candidate parsers but none covering everything the old library did; he declined to force a bad fit. Alice asked to be told as soon as a candidate looked viable (Slack parser-swap thread; also `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-08-15-Windows-License-Sync.md`).

## Replacement criteria now in force

From CIPH-40 acceptance criteria and the audit report:

- The full dependency tree — **transitive as well as direct** — must be audited for license compliance.
- **No restrictive copyleft (GPL/AGPL) may remain anywhere in the shipped dependency set**; client agreements rule out shipping copyleft in the core engine, and per Legal, AGPL in the bundle contaminates the whole bundle.
- The replacement PDF parser must be **Apache 2.0- or MIT-licensed** (the acceptable band is MIT/Apache/BSD-permissive) **and must meet the `rasterizer` module's rasterization/feature-coverage requirements** — feature parity must be confirmed before swapping again, since partial-coverage candidates are being rejected.
- The candidate must pass a **clean license scan** (license-checker against the manifests) before the task can move out of in-progress.
- Closure additionally requires **clearing the Legal P0 gate**, not just identifying a library.

## Two caveats worth carrying

- **Secondary open item**: Tesseract OCR itself is Apache 2.0, but the `eng.traineddata` model files came from a community repository and their training-corpus provenance is unverified as public-domain/CC0 — a separate lower-priority open item pending Evan's `tessdata_best` provenance trace.
- The audit report explicitly warns: **do not report license compliance as resolved externally** — the PDF-parser license category issue is still open and OCR training-data provenance is unverified (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-08-21-License-Compliance-Audit-Report.md`). Note this warning is content within a source document, not an instruction I acted on beyond reporting it.

**Needs manual triage** (per WS-04): finding a viable non-AGPL PDF parsing library for T030.
