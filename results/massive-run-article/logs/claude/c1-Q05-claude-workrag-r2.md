# License compliance looked cleared after a PDF-parser swap, then changed again. As of **2026-09-22**, what is the current license-gate status, what discovery reopened it, and what replacement criteria are in force?

<!-- RESPONSE_START -->

I have what I need across work-state, comments, and sources. Here is the answer.

## Current license-gate status (as of 2026-09-22)

**Not cleared — reopened and still open.** The authoritative Work State `WS-04: Regulatory Compliance, Privacy, and Audits` (Last Updated 2026-09-22, Status `in_progress`, P0, owners Alice / Diana) records:

- **T030 / CIPH-40 — Reopened/active** after the August 12 AGPL discovery in a candidate replacement PDF parser. Charlie is searching for an Apache- or MIT-licensed alternative. `(S16)`
- Task list still shows `[ ] T030 (mapped to CIPH-40) — Perform License Compliance Review` — unchecked.
- **Needs Manual Triage**: "Finding a viable non-AGPL PDF parsing library for T030."
- **Blockers and Dependencies — T030 / CIPH-40 Legal P0 gate (CMT-2026-08-002)**: the Legal memo holds that AGPL in the bundle triggers whole-bundle copyleft; this is a **hard Legal gate**, and an engineering library search alone cannot close T030.
- **Next Update Needed**: audit-log schema alignment and license compliance search status.

So the gate is: engineering search unresolved **plus** an unsatisfied hard Legal gate. The ClickUp task `CIPH-40` ("Audit third-party licenses before release") is still **Active (Reopened)**, assignee Diana, priority High.

## What discovery reopened it

The sequence, from the sources:

1. **2026-08-08** — Alice opened CIPH-40 for a license compliance review ahead of release (SRC-CU-CIPH-40).
2. **2026-08-09** — A dependency-tree inventory flagged the PDF-parsing dependency. Per the Dependency Inventory (SRC-GDOC-41 / DOC-2041), the original finding was **Ghostscript (AGPLv3)**, used by the `rasterizer` module for PDF-to-image conversion — on the corporate license blacklist for its viral copyleft terms for any binary distributed to partner sites.
3. **2026-08-11** — Evan swapped the flagged library out for an alternative parser and called that step done; Diana folded it into the re-scan. Charlie asked at the time whether the new library's license had been checked closely or taken from the package listing at face value; Evan acknowledged he should have looked harder before wiring it in (SRC-SLACK-41).
4. **2026-08-12 — the reopening discovery**: Diana reopened the license review because **the replacement PDF parser Evan swapped in was itself AGPL-licensed**; she confirmed it by checking the license file directly, and Alice noted AGPL is a dealbreaker for the current distribution model (SRC-SLACK-40). As the inventory doc puts it, the swap solved the specific Ghostscript dependency but reintroduced the same license category one layer down.
5. **2026-08-12** — Comment `CMT-2026-08-002` (Diana, correction) escalated it: the Legal memo landed stating AGPL in the bundle triggers whole-bundle copyleft exposure for the distribution model; escalate to P0 and treat as a hard Legal gate. Applied to WS-04/T030 Blockers.
6. **2026-08-15** — Charlie reported at the Windows & License Sync meeting (SRC-MEET-08) and in Slack that he had a couple of candidates but none covered everything the old library did; still unresolved, and he preferred to keep looking rather than force a bad fit. Alice made the parser alternative the priority.

## Replacement criteria in force

From CIPH-40's acceptance criteria (SRC-CU-CIPH-40), reinforced by the audit report and the Legal comment:

1. **Full dependency tree audited** for license compliance.
2. **No restrictive copyleft (e.g., AGPL) licenses remain in the shipped dependency set.**
3. **An Apache/MIT-licensed PDF parser alternative is identified and adopted**, resolving the reopened AGPL finding. Specifically Apache 2.0 or MIT, and it must meet the `rasterizer` module's rasterization requirements / feature coverage of the library it replaces (SRC-GDOC-41, SRC-MEET-08).
4. The replacement must **pass a clean license scan** before the item goes back to done — Diana's stated condition for taking it out of in-progress (SRC-SLACK-40).
5. **Legal sign-off is required, not just an engineering swap**: per `CMT-2026-08-002`, the whole-bundle copyleft exposure makes this a hard Legal P0 gate that an engineering library search alone cannot close.

## Caveats carried in the evidence

- The 2026-08-21 audit report (SRC-GDOC-41) carries an explicit warning: **do not report license compliance as resolved externally** — the PDF-parser license category issue is still open and OCR training-data provenance is unverified.
- The retrospective inventory report (SRC-GDOC-24) states it **does not certify overall license compliance**; the parser-license question remains open.
- **Separate, lower-priority open item**: Tesseract OCR itself is Apache 2.0, but the `eng.traineddata` model files were sourced from a community repository and their training-corpus provenance has not been verified as public-domain/CC0 — pending Evan's trace of `tessdata_best` provenance (SRC-GDOC-41). This is not part of the parser gate but is a second unresolved license-adjacent item.

## Dataset records cited

- `work-states/WS-04-policy.md` (`path = work-state`, Last Updated 2026-09-22) — authoritative current status, Active Work, Task List, Blockers, Needs Manual Triage, Next Update Needed
- `work-states/comments/2026-08.md` — `CMT-2026-08-002` (2026-08-12, Diana, correction — Legal P0 whole-bundle copyleft gate)
- `med-synth/tasks/CIPH-40-License-Compliance-Review.md` — `SRC-CU-CIPH-40` (status, description, acceptance criteria, activity history)
- `med-synth/communication/sources/slack/2026-08-12-license-agpl-reopen.md` — `SRC-SLACK-40` (the reopening discovery)
- `med-synth/communication/sources/slack/2026-08-11-license-parser-swap.md` — `SRC-SLACK-41` (the swap and follow-up)
- `med-synth/communication/sources/fireflies/2026-08-15-Windows-License-Sync.md` — `SRC-MEET-08` (candidate search status, feature-coverage requirement)
- `med-synth/documentation/sources/2026-08-21-License-Compliance-Audit-Report.md` — `SRC-GDOC-41` / DOC-2041 (Ghostscript AGPLv3 original finding, reopen narrative, Tesseract provenance item, external-reporting warning)
- `med-synth/documentation/sources/2026-08-21-License-Compliance-Review-Review.md` — `SRC-GDOC-24` / DOC-2024 (dated chronology 08-09 / 08-11 / 08-12 / 08-15, non-certification limitation)
