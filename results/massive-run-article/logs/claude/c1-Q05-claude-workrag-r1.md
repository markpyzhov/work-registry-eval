# License compliance looked cleared after a PDF-parser swap, then changed again. As of **2026-09-22**, what is the current license-gate status, what discovery reopened it, and what replacement criteria are in force?

<!-- RESPONSE_START -->

I have sufficient evidence. Here is the complete answer.

---

## License gate status as of 2026-09-22

**Not cleared — still open, and now a P0 hard Legal gate.**

Per the authoritative Work State `WS-04: Regulatory Compliance, Privacy, and Audits` (Last Updated 2026-09-22, Status `in_progress`, P0, Owner Alice / Diana, Project CipherDoc):

- **T030 / CIPH-40 — Perform License Compliance Review** is listed as **Reopened/active**, and remains **unchecked** in the WS-04 Task List.
- It appears under **Blockers and Dependencies** as: *"T030 / CIPH-40 — Legal P0 gate (CMT-2026-08-002): Legal memo: AGPL in bundle triggers whole-bundle copyleft; hard Legal gate — engineering library search alone cannot close T030."*
- It also appears under **Needs Manual Triage**: *"Finding a viable non-AGPL PDF parsing library for T030."*
- WS-04's **Next Update Needed** explicitly names "license compliance search status" as still outstanding.
- The source ClickUp task CIPH-40 (`SRC-CU-CIPH-40`, assignee Diana, Priority High) carries status **Active (Reopened)**.

So the apparent clearance after the parser swap was premature: the swap was marked Completed, then undone by a follow-up finding. Note also the audit report's explicit caution — do not report license compliance as resolved externally, since the PDF-parser license category issue is still open (`SRC-GDOC-41`).

## What discovery reopened it

**The replacement PDF parser turned out to itself be AGPL-licensed.** Chronology from the sources:

1. **2026-08-08** — Alice opened CIPH-40 for a pre-release license compliance review (`SRC-CU-CIPH-40`).
2. **2026-08-09** — Dependency-tree inventory run; the PDF-parsing dependency's license was flagged (`SRC-GDOC-24`). The specific original finding was **Ghostscript (AGPLv3)**, used by the `rasterizer` module for PDF-to-image conversion, on the corporate license blacklist for its viral copyleft terms on any binary distributed to partner sites (`SRC-GDOC-41`).
3. **2026-08-11** — Evan swapped out Ghostscript and dropped in a replacement parser, calling that step done; Charlie asked whether he had checked the new library's license closely or taken the package listing at face value, and Evan conceded he should have looked harder before wiring it in (`SRC-SLACK-41`). The swap was initially marked Completed (`SRC-GDOC-41`).
4. **2026-08-12** — **Reopen.** Diana reopened the license review after checking the replacement's license file directly and confirming it is AGPL-licensed; Alice called AGPL a dealbreaker for the current distribution model, and Diana put the item back in progress until a replacement passes a clean scan (`SRC-SLACK-40`). As the audit report puts it, the swap solved the specific Ghostscript dependency but reintroduced the same license category problem one layer down (`SRC-GDOC-41`).
5. **2026-08-12** — Escalation via comment **CMT-2026-08-002** (author Diana, WS-04/T030, type: correction): a Legal memo landed stating AGPL in the bundle triggers **whole-bundle copyleft exposure** for the distribution model; escalate to **P0** and treat as a **hard Legal gate** — engineering search alone is insufficient to close T030.
6. **2026-08-15** — Charlie began the search for an Apache/MIT alternative (`SRC-CU-CIPH-40`, `SRC-SLACK-41`, `SRC-MEET-08`). He had a couple of candidates but **neither covered everything the old library did**, and he opted to keep looking rather than force a bad fit. Alice asked to be told as soon as a candidate looked viable, so this doesn't drag past the rest of the release work.

## Replacement criteria in force

From CIPH-40's acceptance criteria (`SRC-CU-CIPH-40`), reinforced by the audit report and the Legal comment:

1. **Full dependency tree audited** for license compliance.
2. **No restrictive copyleft (e.g., AGPL) licenses remain in the shipped dependency set** — this is the category-level bar, not just removal of the one named library. The whole-bundle copyleft exposure identified by Legal is what makes it category-level (CMT-2026-08-002).
3. **An Apache 2.0- or MIT-licensed PDF parser alternative must be identified and adopted**, resolving the reopened AGPL finding.
4. **The alternative must meet the `rasterizer` module's rasterization requirements** / cover the same parsing feature set as the outgoing library (`SRC-GDOC-41`, `SRC-MEET-08`) — Charlie explicitly requires confirming feature coverage before swapping again.
5. **The replacement must pass a clean license scan** before the item goes back to done (`SRC-SLACK-40`).
6. **Legal sign-off is required, not just an engineering fix** — per CMT-2026-08-002, an engineering library search alone cannot close T030.

## Related open item (adjacent, not the gate itself)

Tesseract OCR is itself Apache 2.0, but the `eng.traineddata` model files were sourced from a community repository and their training-corpus provenance has **not been verified as public-domain/CC0**. This is tracked as a separate, lower-priority open item pending Evan's trace of the `tessdata_best` provenance (`SRC-GDOC-41`).

## Records cited

- `work-states/WS-04-policy.md` (path = work-state) — authoritative current status, Active Work, Blockers and Dependencies, Task List, Needs Manual Triage, Next Update Needed
- `work-states/comments/2026-08.md` — CMT-2026-08-002 (WS-04/T030, Diana, 2026-08-12)
- `med-synth/tasks/CIPH-40-License-Compliance-Review.md` — `SRC-CU-CIPH-40`
- `med-synth/documentation/sources/2026-08-21-License-Compliance-Audit-Report.md` — `SRC-GDOC-41` / DOC-2041
- `med-synth/documentation/sources/2026-08-21-License-Compliance-Review-Review.md` — `SRC-GDOC-24` / DOC-2024
- `med-synth/communication/sources/slack/2026-08-11-license-parser-swap.md` — `SRC-SLACK-41`
- `med-synth/communication/sources/slack/2026-08-12-license-agpl-reopen.md` — `SRC-SLACK-40` (WS-04 `S16`)
- `med-synth/communication/sources/fireflies/2026-08-15-Windows-License-Sync.md` — `SRC-MEET-08`
