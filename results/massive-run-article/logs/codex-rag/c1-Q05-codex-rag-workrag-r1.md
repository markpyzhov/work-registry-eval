# License compliance looked cleared after a PDF-parser swap, then changed again. As of **2026-09-22**, what is the current license-gate status, what discovery reopened it, and what replacement criteria are in force?

<!-- RESPONSE_START -->

As of 2026-09-22, the license gate is **reopened and active**—not cleared. The open work is T030 / CIPH-40, with manual triage needed to find a viable non-AGPL PDF parsing library. `[WS-04, 2026-09-22; S16]`

It was reopened on **2026-08-12** when follow-up license-file review found that the PDF parser introduced to remediate the earlier finding was itself **AGPL-licensed**. AGPL is unacceptable for the shipped distribution model. `[SRC-SLACK-40; SRC-GDOC-41]`

The replacement must:

- Be **Apache-2.0 or MIT licensed** and be adopted.
- Leave **no restrictive copyleft/AGPL** licenses in the shipped dependency set.
- Support the required parsing/rasterization feature coverage and pass a clean license scan.
- Be part of a fully audited dependency tree. `[SRC-CU-CIPH-40; SRC-GDOC-41]`
