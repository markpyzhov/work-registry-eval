# License compliance looked cleared after a PDF-parser swap, then changed again. As of **2026-09-22**, what is the current license-gate status, what discovery reopened it, and what replacement criteria are in force?

<!-- RESPONSE_START -->

## License gate status as of 2026-09-22

**Current status: OPEN — not cleared.** T030 / CIPH-40 ("Audit third-party licenses before release") is **Active (Reopened)**, owned by Diana with Charlie doing the parser search, and it carries a **P0 hard Legal gate**. The 2026-09-22 daily brief lists it among today's active work ("P0 Legal AGPL/whole-bundle gate still open") and ranks it #3 in the priority order ("Close Legal gate on non-AGPL parser"). The work state records no movement on it after mid-August — no viable candidate has been confirmed.

- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md` (Active Work, Blockers, Needs Manual Triage; as-of 2026-09-22)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-40-License-Compliance-Review.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/index.md` (T030 listed under Active / Reopened)

## What reopened it

The audit chain ran as follows:

1. **2026-08-09** — Diana ran a recursive third-party license audit (license-checker against dependency manifests, transitive deps included), flagging anything outside MIT/Apache/BSD. Alice's constraint: client agreements rule out shipping copyleft in the core engine. (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-09-license-audit.md`)
2. **Original finding** — `Ghostscript` (AGPLv3), used by the `rasterizer` module for PDF-to-image conversion; on the corporate license blacklist because of viral copyleft terms for binaries distributed to partner sites. (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-08-21-License-Compliance-Audit-Report.md`)
3. **2026-08-11** — Evan swapped the flagged parser out for a replacement library and marked that step done. Charlie asked whether he had checked the new library's license closely or taken the package listing at face value; Evan conceded he "should have looked harder before wiring it in." (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-11-license-parser-swap.md`)
4. **The reopening discovery — 2026-08-12** — Diana checked the replacement's license file directly and found **the replacement PDF parser is itself AGPL-licensed**. The swap removed the specific Ghostscript dependency but reintroduced the same license category one layer down. Diana put the task back in progress "until we land on a replacement that passes a clean scan." (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-12-license-agpl-reopen.md`; `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-08-21-License-Compliance-Review-Review.md`)
5. **Escalation, same day** — A Legal memo landed: AGPL in the bundle triggers **whole-bundle copyleft exposure** for CipherDoc's distribution model. Diana escalated to **P0** and recorded it as a **hard Legal gate — an engineering library search alone cannot close T030**. (`CMT-2026-08-002`, dated 2026-08-12, in `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-08.md`)

## Replacement criteria now in force

- The parser must be **Apache 2.0 or MIT licensed** — permissive only; the acceptable band from the original scan was MIT/Apache/BSD. (`2026-08-12-license-agpl-reopen.md`, `2026-08-21-License-Compliance-Audit-Report.md`, `2026-08-09-license-audit.md`)
- **No restrictive copyleft (AGPL/GPL) anywhere in the shipped dependency set**, including transitive dependencies — the acceptance criteria on CIPH-40 plus the recursive-scan scope Diana set on 08-09.
- It must **pass a clean license scan** before the task moves out of in-progress. (`2026-08-12-license-agpl-reopen.md`)
- It must **meet the rasterization/parsing feature coverage** of the library it replaces. Charlie found a couple of candidates by 2026-08-15 but "neither one covers everything the old library did," and he chose to keep looking rather than force a bad fit; feature coverage must be confirmed before another swap. (`2026-08-11-license-parser-swap.md`; `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-08-15-Windows-License-Sync.md`)
- **Legal must sign off** — because of the whole-bundle copyleft memo, identifying a permissive library is necessary but not sufficient to close the gate. (`CMT-2026-08-002`)

## Two caveats worth carrying forward

- **Do not report license compliance as resolved externally.** The audit report carries an explicit warning to that effect: the PDF-parser license category issue is still open. (`2026-08-21-License-Compliance-Audit-Report.md`)
- **Secondary open item:** Tesseract OCR itself is Apache 2.0, but the `eng.traineddata` model files came from a community repository and their training-corpus provenance is unverified as public-domain/CC0. This is tracked separately at lower priority, pending Evan's trace of `tessdata_best` provenance — so even a clean parser swap would not certify the full dependency set. (`2026-08-21-License-Compliance-Audit-Report.md`)
