# License compliance looked cleared after a PDF-parser swap, then changed again. As of **2026-09-22**, what is the current license-gate status, what discovery reopened it, and what replacement criteria are in force?

<!-- RESPONSE_START -->

As of 2026-09-22, the license gate is **reopened and active**, not cleared. Charlie is still seeking a compliant PDF-parser replacement. (WS-04, T030/CIPH-40; `SRC-CU-CIPH-40`)

It reopened after follow-up review found that the parser swapped in to replace the original flagged dependency was itself **AGPL-licensed**—confirmed from its license file—so it could not be shipped under the current distribution model. (`SRC-SLACK-40`; `SRC-GDOC-41`)

The replacement must:

- Be **Apache 2.0 or MIT licensed**.
- Meet the required PDF parsing/rasterization feature coverage.
- Pass a clean license scan.
- Be adopted only after a **full, recursive dependency-tree audit** confirms no restrictive copyleft (including AGPL) remains in the shipped set. (`SRC-CU-CIPH-40`; `SRC-GDOC-41`)
