# License compliance looked cleared after a PDF-parser swap, then changed again. As of **2026-09-22**, what is the current license-gate status, what discovery reopened it, and what replacement criteria are in force?

<!-- RESPONSE_START -->

As of **2026-09-22**, the license gate is **not cleared**: T030/CIPH-40 is **Active (Reopened)**, P0, and remains a hard Legal gate requiring manual triage. It must not be reported as resolved. [WS-04 work state; `SRC-CU-CIPH-40`]

It reopened because the PDF-parser replacement—initially swapped in to clear the earlier audit finding—was discovered on direct license-file review to be **AGPL-licensed**. That is unacceptable for CipherDoc’s distribution model because it creates whole-bundle copyleft exposure. [Slack AGPL Reopen, 2026-08-12; `SRC-SLACK-40`; Legal comment `CMT-2026-08-002`]

The enforced replacement criteria are:

- Audit the **full, transitive dependency tree**.
- Ship with **no restrictive copyleft**, including AGPL.
- Select and adopt an **Apache-2.0 or MIT** PDF parser.
- Confirm it provides the needed parsing/rasterization feature coverage and passes a **clean license scan**.
- Legal clearance is required; an engineering search alone cannot close the gate. [CIPH-40 acceptance criteria; `SRC-CU-CIPH-40`; license audit report `SRC-GDOC-41`]
