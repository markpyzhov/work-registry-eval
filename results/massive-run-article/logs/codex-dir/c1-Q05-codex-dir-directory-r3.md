# License compliance looked cleared after a PDF-parser swap, then changed again. As of **2026-09-22**, what is the current license-gate status, what discovery reopened it, and what replacement criteria are in force?

<!-- RESPONSE_START -->

As of 2026-09-22, compliance is **not cleared**: CIPH-40 remains Active (Reopened), a P0 Legal whole-bundle AGPL gate. The initial Ghostscript removal was prematurely treated as complete; the replacement parser was later verified AGPL, so it recreated the disallowed copyleft exposure. [Audit report](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-08-21-License-Compliance-Audit-Report.md:8) [Sep. 22 status](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md:11)

Reopen discovery for a parser that is **Apache-2.0 or MIT**, covers the rasterizer/PDF-to-image requirements, and passes a recursive shipped-bundle dependency scan with no restrictive copyleft. Legal must close the gate; a library search alone is insufficient. Also retain the separate lower-priority check on `eng.traineddata` provenance. [Acceptance criteria](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-40-License-Compliance-Review.md:13) [Legal gate](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md:51)
