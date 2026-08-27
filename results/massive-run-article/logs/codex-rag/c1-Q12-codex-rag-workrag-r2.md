# Several streams remain blocked while others are only reopened. As of **2026-09-22**, what work can still advance in parallel, what cannot progress until an external dependency moves, and what release-checklist work is gated on packaging and Windows signing?

<!-- RESPONSE_START -->

As of 2026-09-22:

- Work that can advance in parallel: Docker slimming/CVE remediation (T005); OCR fallback and policy migration (T008/T006); quarantine workflow (T014); audit-log schema alignment (T016); the licensed PDF-parser search (T030); large-file memory fixes (T031); storage quota tolerance (T022); and remaining Windows engineering (T029). Reopened means active—not cleared or blocked by itself. `[WS-01: 280c5cc6486fd51d; WS-03: f0b9411efcd33230; WS-04: 917ecd0b3736fd18; WS-05: ec16f901e952ecd9; WS-06: b6de3e9600732a79; WS-07: bcafdf0ed04b56a6]`

- Work that cannot progress to closure until an external dependency moves:
  - T007 offset mismatch: waiting on upstream `pdfminer.six` PR #992; any workaround also needs written Legal approval.
  - T036 high-DPI rendering: blocked on upstream rendering-library scaling math; nested Form XObjects affect 12% of the pilot corpus.
  - T029 Windows distribution cannot be released until procurement obtains an Authenticode certificate, though engineering can continue.
  - T030 cannot close on engineering search alone: Legal must clear the AGPL/copyleft issue. `[WS-01: 5c8d393527944517; WS-04: 9e4ee6741c6cd253; WS-06: 3c9963caad9ee58b, b6de3e9600732a79]`

- Release-checklist work: T011 (v1.0.0 gates and docs) remains on a security-gate hold. It cannot close until:
  1. T005 produces a CVE-clean Docker image—interim RC limit 800 MB; GA target about 450 MB.
  2. T029 is green with Windows code-signing.
  3. The audit-log CLI-schema versus emitted-record mismatch is aligned.

  The release board has a no-ship cutoff after 2026-10-15 if T005 and T029 are not green. `[WS-03: f0b9411efcd33230, f9c5d923ad85c212; WS-04: 917ecd0b3736fd18]`
