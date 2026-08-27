# License compliance looked cleared after a PDF-parser swap, then changed again. As of **2026-09-22**, what is the current license-gate status, what discovery reopened it, and what replacement criteria are in force?

<!-- RESPONSE_START -->

## License gate status as of 2026-09-22

**Current status: still open — Active (Reopened), P0, unresolved.** License compliance is *not* cleared, and the 2026-09-22 daily brief still lists it as an open item with priority #3 on the board ("Close Legal gate on non-AGPL parser").

- Work item: **T030 / CIPH-40 — "Audit third-party licenses before release"**, tracked under WS-04 (Regulatory Compliance, Privacy, and Audits). Status `Active (Reopened)`, assignee **Diana**, priority **High/P0**, with **Charlie** doing the replacement-parser search.
- WS-04 lists T030 as unchecked, in Active Work as "Reopened/active after August 12 AGPL discovery," and under Needs Manual Triage as "Finding a viable non-AGPL PDF parsing library."
- The audit document carries an explicit warning: do not report license compliance as resolved externally.

## What reopened it

1. **2026-08-09** — Diana ran the third-party license audit across the dependency tree (`license-checker` against the manifests, recursive so transitive deps were included). It flagged **Ghostscript (AGPLv3)**, used by the `rasterizer` module for PDF-to-image conversion, as blacklisted for viral copyleft on binaries distributed to partner sites.
2. **2026-08-11** — Evan swapped the flagged PDF parser out for a replacement and called that step done; Diana folded it into the re-scan. Charlie asked at the time whether the new library's license had been checked closely or taken from the package listing at face value; Evan conceded he "should have looked harder before wiring it in."
3. **2026-08-12 (the reopening discovery)** — Diana reopened the review: **the replacement PDF parser was itself AGPL-licensed**. She verified it by reading the license file directly, not the package metadata. The swap removed the specific Ghostscript dependency but reintroduced the same license category one layer down.
4. **2026-08-12 (escalation)** — Diana's correction comment `CMT-2026-08-002` recorded a **Legal memo**: AGPL in the bundle triggers **whole-bundle copyleft exposure** for CipherDoc's distribution model. T030 was escalated to **P0** and made a **hard Legal gate** — an engineering library search alone is insufficient to close it.

## Replacement criteria in force

- **License must be Apache 2.0 or MIT.** This is the standing requirement from the reopen (broader original scan criterion was anything outside MIT/Apache/BSD gets flagged).
- **No restrictive copyleft (AGPL/GPL) anywhere in the shipped dependency set**, and the check must be recursive — transitive dependencies count, since a clean top-level library can pull in something restrictive underneath (Bob's point on 2026-08-09; Alice's client agreements rule out shipping copyleft in the core engine).
- **Feature coverage must be confirmed before swapping again.** Charlie: "Need to confirm feature coverage before we swap again." As of 2026-08-15 he had a couple of candidates but "neither one covers everything the old library did," and chose to keep looking rather than force a bad fit. The alternative must meet the `rasterizer` module's rasterization requirements.
- **Must pass a clean scan** — Diana kept the task in progress "until we land on a replacement that passes a clean scan."
- **Legal sign-off is required to close.** Because of the whole-bundle copyleft memo, finding a library is necessary but not sufficient; the P0 Legal gate must be cleared.

## Related still-open item

A **secondary, lower-priority open item**: Tesseract OCR itself is Apache 2.0, but the `eng.traineddata` model files came from a community repository and their training-corpus provenance has not been verified as public-domain/CC0. Pending Evan's trace of `tessdata_best` provenance.

## Evidence

- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md` (authoritative current state, last updated 2026-09-22)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/index.md` (as-of 2026-09-22T12:00:00Z; T030 listed under Active/Reopened)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-08.md` (`CMT-2026-08-002`, Legal P0 escalation)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-40-License-Compliance-Review.md` (`SRC-CU-CIPH-40`)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-09-license-audit.md` (`SRC-SLACK-39`)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-11-license-parser-swap.md` (`SRC-SLACK-41`)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-12-license-agpl-reopen.md` (`SRC-SLACK-40`)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-08-15-Windows-License-Sync.md` (`SRC-MEET-08`)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-08-21-License-Compliance-Audit-Report.md` (`SRC-GDOC-41`)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-08-21-License-Compliance-Review-Review.md` (`SRC-GDOC-24`)

One gap worth flagging: the corpus contains no license-specific update between 2026-08-21 and 2026-09-22. The 2026-09-22 state is carried forward from the August record (the 09-15 pre-release audit covered Docker, Windows signing, high-DPI, and audit logs but did not touch licensing), so there is no evidence of progress on the Apache/MIT parser search in the last five weeks.
