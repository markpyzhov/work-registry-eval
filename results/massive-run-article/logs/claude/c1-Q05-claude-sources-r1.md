# License compliance looked cleared after a PDF-parser swap, then changed again. As of **2026-09-22**, what is the current license-gate status, what discovery reopened it, and what replacement criteria are in force?

<!-- RESPONSE_START -->

## License-gate status as of 2026-09-22

**Current status: still open — Active (Reopened), not cleared.**

The most recent evidence in the dataset on this item is dated **2026-08-21**; there is no source record after that date showing the license gate closing, a replacement parser being adopted, or the audit item resolving. So as of 2026-09-22, the last documented state stands: CIPH-40 "Audit third-party licenses before release" (owner Diana, Priority High) remains **Active (Reopened)**, and the 2026-08-21 audit carries an explicit warning: *do not report license compliance as resolved externally* — the PDF-parser license category issue is still open and OCR training-data provenance is unverified.

## What happened, in order

1. **2026-08-08** — Alice opened CIPH-40, a third-party license compliance review across the full dependency tree ahead of release.
2. **2026-08-09** — Diana ran the inventory using license-checker against the dependency manifests, flagging anything outside MIT/Apache/BSD, and doing a **recursive pass over transitive dependencies**, not just direct ones (Bob specifically asked for this). Alice's constraint: client agreements rule out shipping copyleft code in the core engine.
3. **Original finding** — `Ghostscript`, used by the `rasterizer` module for PDF-to-image conversion, is **AGPLv3** and on the corporate license blacklist because its viral copyleft terms apply to any binary distributed to partner sites.
4. **2026-08-11** — Evan swapped Ghostscript out for an alternative PDF parser library and called that step done; the swap was initially marked Completed. Charlie asked whether the new library's license had been checked closely or just taken from the package listing at face value; Evan acknowledged he "should have looked harder before wiring it in."

## The discovery that reopened it

**On 2026-08-12, Diana reopened the review after checking the replacement library's license file directly and finding the replacement parser is itself AGPL-licensed.** The swap solved the specific Ghostscript dependency but reintroduced the same license category problem one layer down. Alice called AGPL "a dealbreaker for how we distribute this"; Diana confirmed it cannot ship under the current distribution model and put the item back in progress "until we land on a replacement that passes a clean scan."

## Replacement criteria now in force

From CIPH-40's acceptance criteria and the audit document:

- The **full dependency tree** must be audited for license compliance — recursive, including transitive dependencies, not just top-level manifests.
- **No restrictive copyleft (e.g. AGPL) licenses may remain in the shipped dependency set.** The scan baseline is permissive-only: MIT / Apache / BSD; anything outside that is flagged.
- An **Apache 2.0- or MIT-licensed PDF parser alternative must be identified and adopted**, resolving the reopened AGPL finding.
- The candidate must **meet the `rasterizer` module's rasterization/parsing requirements** — Charlie stated feature coverage must be confirmed before swapping again, and refused to force a bad fit.
- The replacement must **pass a clean license scan** before the gate closes (Diana's condition on reopening).

**Search state as of the last record (2026-08-15):** Charlie had a couple of candidates, but neither covered everything the old library did, so the search was deliberately left unresolved rather than forcing a poor fit. Alice asked to be told as soon as a candidate looked viable. Charlie also noted rework cost for another swap is unknown until he finishes comparing candidates.

## Related open item (separate, lower priority)

Tesseract OCR itself is Apache 2.0, but the `eng.traineddata` model files were sourced from a community repository and their **training-corpus provenance has not been verified as public-domain/CC0**. This remains open pending Evan's trace of the `tessdata_best` provenance.

## Caveat on the as-of date

The question asks about 2026-09-22, but the dataset's license-related records stop at 2026-08-21. September sources exist for other workstreams (Windows code-signing on 09-02, storage quota on 09-15/09-18, a pre-release audit meeting on 09-15) — and notably, the **2026-09-15 pre-release gate review lists Docker slim-down/CVE, Windows signing, high-DPI rendering, and the audit-log schema mismatch as the open release blockers without mentioning the license gate one way or the other.** That is an absence of evidence, not a closure: no record shows CIPH-40 resolving, and the standing instruction not to report license compliance as resolved externally has not been retracted in any available source.

## Sources cited

- `med-synth/tasks/CIPH-40-License-Compliance-Review.md` (SRC-CU-CIPH-40) — status, assignee, acceptance criteria, activity history
- `med-synth/documentation/sources/2026-08-21-License-Compliance-Audit-Report.md` (SRC-GDOC-41, DOC-2041) — Ghostscript AGPLv3 finding, reopen narrative, unresolved status, Tesseract provenance item, external-reporting warning
- `med-synth/documentation/sources/2026-08-21-License-Compliance-Review-Review.md` (SRC-GDOC-24, DOC-2024) — retrospective timeline of 08-09 inventory, 08-11 swap, 08-12 reopen, 08-15 status
- `med-synth/communication/sources/slack/2026-08-09-license-audit.md` (SRC-SLACK-39) — scan methodology, MIT/Apache/BSD baseline, transitive-dependency pass
- `med-synth/communication/sources/slack/2026-08-11-license-parser-swap.md` (SRC-SLACK-41) — swap execution and candidate search follow-up
- `med-synth/communication/sources/slack/2026-08-12-license-agpl-reopen.md` (SRC-SLACK-40) — the reopen and the clean-scan condition
- `med-synth/communication/sources/fireflies/2026-08-15-Windows-License-Sync.md` (SRC-MEET-08) — feature-coverage requirement, priority confirmation
- `med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md` (SRC-MEET-10) — September gate review context
