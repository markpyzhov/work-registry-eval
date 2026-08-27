# License compliance looked cleared after a PDF-parser swap, then changed again. As of **2026-09-22**, what is the current license-gate status, what discovery reopened it, and what replacement criteria are in force?

<!-- RESPONSE_START -->

As of 2026-09-22, the license gate (CIPH-40) remains **Active (Reopened)**—not cleared. The PDF-parser question is still open. [SRC-CU-CIPH-40; SRC-GDOC-24]

It reopened after follow-up review found that the replacement parser, initially marked complete after replacing Ghostscript, was itself **AGPL-licensed**. The team verified this by checking the license file directly; AGPL is incompatible with the current distribution model. [SRC-GDOC-41; SRC-SLACK-40]

The replacement must:

- Be Apache 2.0- or MIT-licensed (non-copyleft).
- Meet the required PDF parsing/rasterization functionality.
- Be adopted and pass a clean license scan.
- Leave no restrictive copyleft licenses, including AGPL, in the shipped dependency set, with the full dependency tree audited. [SRC-CU-CIPH-40; SRC-GDOC-41]
