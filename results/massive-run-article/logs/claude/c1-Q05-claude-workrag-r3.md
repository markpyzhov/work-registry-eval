# License compliance looked cleared after a PDF-parser swap, then changed again. As of **2026-09-22**, what is the current license-gate status, what discovery reopened it, and what replacement criteria are in force?

<!-- RESPONSE_START -->

## License-gate status as of 2026-09-22 (CipherDoc, WS-04 / T030 / CIPH-40)

**Current status: NOT cleared — reopened and active, and now under a hard Legal gate.**

The work state `WS-04: Regulatory Compliance, Privacy, and Audits` (Last Updated 2026-09-22, Status `in_progress`, P0, Owner Alice / Diana) records T030 / CIPH-40 ("Perform License Compliance Review") as **Reopened/active**, unchecked in the task list, with "Finding a viable non-AGPL PDF parsing library for T030" sitting in **Needs Manual Triage**. The work state's "Next Update Needed" explicitly names "license compliance search status" as still outstanding.

### What reopened it

The chronology, from the source records:

1. **2026-08-08** — CIPH-40 opened by Alice for a pre-release license compliance review of the full dependency tree (`SRC-CU-CIPH-40`).
2. **2026-08-09** — Dependency-tree inventory run. It flagged `Ghostscript` (AGPLv3), used by the `rasterizer` module for PDF-to-image conversion, as on the corporate license blacklist because of viral copyleft terms for any binary distributed to partner sites (`SRC-GDOC-24` / DOC-2024, `SRC-GDOC-41` / DOC-2041).
3. **2026-08-11** — Evan swapped the flagged parser out for a replacement library and called that step done; Diana folded it into the re-scan. Charlie asked at the time whether the new library's license had actually been checked or just taken from the package listing — Evan acknowledged he "should have looked harder before wiring it in" (`SRC-SLACK-41`).
4. **2026-08-12 — the discovery that reopened it**: Diana checked the replacement's license file directly and found **the replacement PDF parser was itself AGPL-licensed** (`SRC-SLACK-40`). The swap removed the specific Ghostscript dependency but reintroduced the same license category one layer down. Alice called AGPL "a dealbreaker for how we distribute this"; Diana put the task back in progress "until we land on a replacement that passes a clean scan."
5. **2026-08-12 — escalation** (`CMT-2026-08-002`, Diana): a **Legal memo** landed finding that AGPL anywhere in the bundle triggers **whole-bundle copyleft exposure** for CipherDoc's distribution model. T030 was escalated to **P0** and is now treated as a **hard Legal gate** — the work state records explicitly that "engineering library search alone cannot close T030."
6. **2026-08-15** — Charlie began searching for an Apache/MIT alternative (`SRC-MEET-08`, `SRC-SLACK-41`, `SRC-CU-CIPH-40`). He had a couple of candidates but **neither covered everything the old library did**, and he declined to force a bad fit. Alice made the parser alternative the priority. As of the 2026-08-21 audit write-ups, the search had not concluded, and nothing later in the record supersedes that.

### Replacement criteria in force

To close CIPH-40 / T030, a candidate parser must satisfy all of the following:

- **License**: Apache 2.0 or MIT. Explicitly no restrictive copyleft — no AGPL (and no viral copyleft generally) may remain anywhere in the shipped dependency set (`SRC-CU-CIPH-40` acceptance criteria; `SRC-GDOC-41`).
- **Scope of audit**: the **full dependency tree** must be audited for license compliance, not just the parser slot — the reopen proved the problem can hide one layer down.
- **Functional coverage**: the alternative must meet the `rasterizer` module's rasterization/parsing requirements — feature coverage must be confirmed *before* another swap (Charlie, `SRC-MEET-08`). This is the current sticking point: candidates so far are functionally incomplete.
- **Verification method**: the license must be verified from the license file directly, not from package-listing metadata (the failure mode that caused the reopen), and the replacement must **pass a clean scan** (`SRC-SLACK-40`, `SRC-SLACK-41`).
- **Legal sign-off**: because of the whole-bundle copyleft memo, adoption of a replacement is a Legal gate, not purely an engineering decision (`CMT-2026-08-002`).

### Two caveats worth flagging

- **Do not report license compliance as resolved externally.** The 2026-08-21 audit report carries an explicit warning to that effect, and the retrospective inventory report states it "does not certify overall license compliance."
- **Separate open item**: Tesseract OCR itself is Apache 2.0, but the `eng.traineddata` model files came from a community repository and their training-corpus provenance has not been verified as public-domain/CC0. This is a lower-priority open item pending Evan's trace of `tessdata_best` provenance (`SRC-GDOC-41`).

### Records cited

`work-states/WS-04-policy.md` (work-state, Last Updated 2026-09-22) · `work-states/comments/2026-08.md` (CMT-2026-08-002) · `med-synth/tasks/CIPH-40-License-Compliance-Review.md` (SRC-CU-CIPH-40) · `med-synth/communication/sources/slack/2026-08-12-license-agpl-reopen.md` (SRC-SLACK-40) · `med-synth/communication/sources/slack/2026-08-11-license-parser-swap.md` (SRC-SLACK-41) · `med-synth/communication/sources/fireflies/2026-08-15-Windows-License-Sync.md` (SRC-MEET-08) · `med-synth/documentation/sources/2026-08-21-License-Compliance-Audit-Report.md` (SRC-GDOC-41 / DOC-2041) · `med-synth/documentation/sources/2026-08-21-License-Compliance-Review-Review.md` (SRC-GDOC-24 / DOC-2024)
