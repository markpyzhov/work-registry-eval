**Source ID**: SRC-GDOC-41

# Dependency Inventory: License Compliance Audit (Q3) — Reopened
**Owner**: Diana
**Document Key**: DOC-2041
**Last Updated**: 2026-08-21 (reflects reopen activity through 2026-08-15)

## Original Finding: Ghostscript (AGPLv3)
The initial audit flagged `Ghostscript`, used by the `rasterizer` module for PDF-to-image conversion, as AGPLv3-licensed — on the corporate license blacklist because of its viral copyleft terms for any binary distributed to partner sites.

## First Remediation and Reopen
The team swapped in an alternative PDF parser library to replace the Ghostscript dependency, and that swap was initially marked Completed. On follow-up review, however, the replacement library itself turned out to also be AGPL-licensed — the swap solved the specific Ghostscript dependency but reintroduced the same license category problem one layer down. The task was reopened.

## Current Status: Unresolved
Charlie is now searching for an Apache 2.0 or MIT-licensed PDF parser alternative that meets the module's rasterization requirements. No suitable replacement has been confirmed yet, so this audit item remains **Active (Reopened)** — not resolved.

## Secondary Open Item
Tesseract OCR itself is Apache 2.0, but the `eng.traineddata` model files were sourced from a community repository and their training-corpus provenance has not been verified as public-domain/CC0. This remains a separate, lower-priority open item pending Evan's trace of the `tessdata_best` provenance.

*Warning*: Do not report license compliance as resolved externally. The PDF-parser license category issue is still open, and OCR training-data provenance is unverified.
