# License compliance looked cleared after a PDF-parser swap, then changed again. As of **2026-09-22**, what is the current license-gate status, what discovery reopened it, and what replacement criteria are in force?

<!-- RESPONSE_START -->

I have the full picture. Here is the answer.

---

## License-gate status as of 2026-09-22

**Status: still open — Active (Reopened), not resolved.** The license compliance gate (ClickUp task **CIPH-40**, "Audit third-party licenses before release", owner Diana, priority High, created 2026-08-08) has not been cleared. The most recent license-specific evidence in the dataset is dated **2026-08-21**, and it explicitly states the item remains **Active (Reopened)** with no suitable replacement confirmed. Nothing in the September records (through 2026-09-15) reports the item as closed, so as of 2026-09-22 the last recorded state stands: unresolved.

The 2026-08-21 audit report carries an explicit caution: do not report license compliance as resolved externally — the PDF-parser license category issue is still open, and OCR training-data provenance is unverified. The companion inventory report likewise states it does not certify overall license compliance.

## What reopened it

The sequence:

1. **2026-08-09** — Diana ran the third-party license audit across the dependency tree (recursive, covering transitive deps, not just direct ones), scanning with `license-checker` against the dependency manifests to flag anything outside MIT/Apache/BSD. Alice's constraint: client agreements rule out shipping copyleft code in the core engine.
2. **Original finding** — `Ghostscript`, used by the `rasterizer` module for PDF-to-image conversion, was flagged as **AGPLv3**, on the corporate license blacklist because of its viral copyleft terms for any binary distributed to partner sites.
3. **2026-08-11** — Evan swapped out the flagged library and dropped in a replacement PDF parser, calling that step done; the swap was initially marked Completed. Charlie asked at the time whether the new library's license had been checked closely or just taken from the package listing at face value; Evan acknowledged he should have looked harder before wiring it in.
4. **The discovery that reopened it — 2026-08-12** — On follow-up review, Diana checked the replacement's license file directly and found **the replacement parser is itself AGPL-licensed**. The swap solved the specific Ghostscript dependency but reintroduced the same license category one layer down. Alice called AGPL a dealbreaker for the current distribution model; Diana put the task back in progress.
5. **2026-08-15** — Charlie took over the search for an alternative. He had a couple of candidates, but neither covered everything the old library did; he chose to keep looking rather than force a bad fit. Alice made the parser alternative the priority.

## Replacement criteria now in force

From CIPH-40's acceptance criteria and the reopened audit document:

- **Full dependency tree audited** for license compliance — recursive/transitive, not just direct dependencies.
- **No restrictive copyleft (e.g., AGPL) licenses remain in the shipped dependency set.** More broadly, the scan flags anything outside **MIT / Apache / BSD**.
- **An Apache 2.0- or MIT-licensed PDF parser alternative must be identified and adopted**, resolving the reopened AGPL finding.
- The alternative must **meet the `rasterizer` module's rasterization requirements** — feature coverage must be confirmed before another swap (Charlie's stated precondition; his rejected candidates failed exactly this test).
- The replacement must **pass a clean scan** before the task moves out of "in progress" (Diana's condition on reopening).

## Secondary open item on the same gate

Tesseract OCR itself is Apache 2.0, but the `eng.traineddata` model files were sourced from a community repository and their training-corpus provenance has **not been verified as public-domain/CC0**. This is tracked as a separate, lower-priority open item pending Evan's trace of the `tessdata_best` provenance.

## Sources cited

- `med-synth/tasks/CIPH-40-License-Compliance-Review.md` (SRC-CU-CIPH-40)
- `med-synth/documentation/sources/2026-08-21-License-Compliance-Audit-Report.md` (SRC-GDOC-41, DOC-2041)
- `med-synth/documentation/sources/2026-08-21-License-Compliance-Review-Review.md` (SRC-GDOC-24, DOC-2024)
- `med-synth/communication/sources/slack/2026-08-09-license-audit.md` (SRC-SLACK-39)
- `med-synth/communication/sources/slack/2026-08-11-license-parser-swap.md` (SRC-SLACK-41)
- `med-synth/communication/sources/slack/2026-08-12-license-agpl-reopen.md` (SRC-SLACK-40)
- `med-synth/communication/sources/fireflies/2026-08-15-Windows-License-Sync.md` (SRC-MEET-08)
- `med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md` (SRC-MEET-10) — latest pre-release gate review; does not report the license item as cleared

**Caveat on the as-of date:** the dataset contains no license-compliance record dated after 2026-08-21. The 2026-09-22 status above is the last recorded state carried forward, not a fresh September confirmation.
