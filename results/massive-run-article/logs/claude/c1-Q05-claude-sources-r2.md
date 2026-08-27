# License compliance looked cleared after a PDF-parser swap, then changed again. As of **2026-09-22**, what is the current license-gate status, what discovery reopened it, and what replacement criteria are in force?

<!-- RESPONSE_START -->

## License gate status as of 2026-09-22

**Current status: NOT cleared — Active (Reopened), unresolved.**

The license-compliance gate is tracked under **ClickUp task CIPH-40, "Audit third-party licenses before release"** (owner/assignee Diana, Priority High, created 2026-08-08). Its status in the sources is **Active (Reopened)**, and the most recent evidence in the dataset carries it through 2026-08-21 with no later record of resolution. No source shows the gate being closed, so as of 2026-09-22 it must be treated as still open. The audit report is explicit on this point: *"Do not report license compliance as resolved externally. The PDF-parser license category issue is still open, and OCR training-data provenance is unverified."*

### What reopened it

The sequence, reconstructed from the source records:

1. **2026-08-09 — initial audit.** Diana ran a recursive license scan across the dependency tree (license-checker against the dependency manifests, flagging anything outside MIT/Apache/BSD, including transitive dependencies). Alice's constraint: client agreements rule out shipping GPL/AGPL copyleft code in the core engine.
2. **Original finding: Ghostscript (AGPLv3)** — used by the `rasterizer` module for PDF-to-image conversion, on the corporate license blacklist because of its viral copyleft terms for any binary distributed to partner sites.
3. **2026-08-11 — first remediation.** Evan swapped out Ghostscript and dropped in a replacement PDF parser library, calling that step done. Charlie asked at the time whether the new library's license had been checked closely or taken at face value from the package listing; Evan acknowledged he "should have looked harder before wiring it in."
4. **2026-08-12 — the reopening discovery.** Diana checked the replacement's license file directly and found **the replacement parser was itself AGPL-licensed**. The swap removed the specific Ghostscript dependency but reintroduced the same license category one layer down. Alice called AGPL "a dealbreaker for how we distribute this," and Diana put the task back in progress "until we land on a replacement that passes a clean scan."
5. **2026-08-15 — still unresolved.** Charlie reported at the Windows & License Sync meeting and in Slack that he was searching for an Apache or MIT alternative: a couple of candidates existed, but **neither covered everything the old library did**, and he preferred to keep looking rather than force a bad fit. Rework cost of another swap was unknown pending candidate comparison. Alice made the parser alternative the priority.

### Replacement criteria in force

From CIPH-40's acceptance criteria and the audit report:

- **Full dependency tree audited** for license compliance — recursive, covering transitive dependencies, not just direct ones.
- **No restrictive copyleft (e.g., AGPL) licenses remain** in the shipped dependency set. Scanning targets anything outside MIT/Apache/BSD.
- **An Apache 2.0 or MIT-licensed PDF parser alternative must be identified and adopted**, resolving the reopened AGPL finding.
- The candidate must **meet the `rasterizer` module's rasterization requirements** / cover the same parsing feature set as the library it replaces — feature coverage must be confirmed before swapping again (this is what disqualified the 2026-08-15 candidates).
- The replacement must **pass a clean license scan** before the item can be closed.

### Related open item

A separate, lower-priority open item sits under the same audit: **Tesseract OCR is itself Apache 2.0, but the `eng.traineddata` model files were sourced from a community repository and their training-corpus provenance has not been verified as public-domain/CC0.** This is pending Evan's trace of the `tessdata_best` provenance and is also unverified in the sources.

### Caveat on the as-of date

The dataset contains no source record dated after 2026-08-21 that touches CIPH-40 or the parser-license question. Other workstreams do have September activity (Windows signing gap, 2026-09-02; upstream pdfminer.six block, 2026-09-10; storage quota, 2026-09-18), so the absence is specific to this item rather than a general gap in coverage. The status above is therefore the last recorded state carried forward, not a positively confirmed 2026-09-22 reading.

### Sources cited

- `med-synth/tasks/CIPH-40-License-Compliance-Review.md` (SRC-CU-CIPH-40) — task status, acceptance criteria, activity history
- `med-synth/documentation/sources/2026-08-21-License-Compliance-Audit-Report.md` (SRC-GDOC-41, DOC-2041) — Ghostscript AGPLv3 finding, reopen narrative, current unresolved status, Tesseract traineddata item, do-not-report-as-resolved warning
- `med-synth/documentation/sources/2026-08-21-License-Compliance-Review-Review.md` (SRC-GDOC-24, DOC-2024) — retrospective timeline of 08-09 inventory, 08-11 swap, 08-12 reopen, 08-15 status
- `med-synth/communication/sources/slack/2026-08-09-license-audit.md` (SRC-SLACK-39) — scan methodology and MIT/Apache/BSD criterion
- `med-synth/communication/sources/slack/2026-08-11-license-parser-swap.md` (SRC-SLACK-41) — the swap, the missed license check, the 08-15 candidate gap
- `med-synth/communication/sources/slack/2026-08-12-license-agpl-reopen.md` (SRC-SLACK-40) — the reopening discovery
- `med-synth/communication/sources/fireflies/2026-08-15-Windows-License-Sync.md` (SRC-MEET-08) — feature-coverage requirement and priority direction
