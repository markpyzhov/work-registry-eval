# License compliance looked cleared after a PDF-parser swap, then changed again. As of **2026-09-22**, what is the current license-gate status, what discovery reopened it, and what replacement criteria are in force?

<!-- RESPONSE_START -->

As of 2026-09-22, the license gate remains **Active (Reopened)**—not cleared for release. The full dependency tree still must be compliant, and the shipped set may not contain restrictive copyleft licenses. [SRC-CU-CIPH-40]

It was reopened by a follow-up license-file check: the replacement PDF parser, installed to remediate the original Ghostscript/AGPLv3 finding, was itself AGPL-licensed. That is incompatible with the current distribution model. [SRC-SLACK-40] [SRC-GDOC-41]

The replacement must:

- Be licensed under **Apache 2.0 or MIT** (i.e., non-copyleft).
- Meet the module’s required PDF parsing/rasterization functionality.
- Be adopted and pass a clean dependency-license scan, with no restrictive copyleft remaining in the shipped dependency set. [SRC-GDOC-41] [SRC-CU-CIPH-40]

No suitable replacement had been confirmed in the available sources; earlier candidates lacked full feature coverage. [SRC-SLACK-41]
