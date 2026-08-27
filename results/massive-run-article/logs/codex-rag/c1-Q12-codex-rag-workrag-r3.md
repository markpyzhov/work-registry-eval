# Several streams remain blocked while others are only reopened. As of **2026-09-22**, what work can still advance in parallel, what cannot progress until an external dependency moves, and what release-checklist work is gated on packaging and Windows signing?

<!-- RESPONSE_START -->

As of 2026-09-22, these streams can advance in parallel:

- **Engine:** legacy JSON→YAML migration (T006) and OCR fallback integration/tuning (T008). `WS-01 / CMT-2026-06-001, S8–S9`
- **Packaging:** Docker slimming and CVE remediation (T005) is reopened and active; track the CVE-clean **800 MB RC** threshold separately from the roughly **450 MB GA** target. `WS-03 / CMT-2026-06-002, S1–S2`
- **Compliance:** manual-review workflow (T014), audit-log schema alignment (T016), and the search for a non-AGPL parser replacement (T030) are active/reopened. `WS-04 / S5, S7, S9, S16`
- **Performance/storage:** large-file chunking and buffer-release fixes (T031), plus storage-quota tolerance refactoring (T022). `WS-05 / CMT-2026-08-003, S6–S7`; `WS-07 / CMT-2026-09-003, S4`
- **Windows:** T029 engineering continues—the backslash issue is fixed—while signing is a procurement dependency rather than an engineering block. `WS-06 / S7–S9`

Work that cannot close/progress pending an external move:

- **T007 offset mismatch:** waiting on upstream `pdfminer.six` PR #992; no safe local workaround. A pre-normalization workaround also needs written Legal approval. `WS-01 / S6–S7, CMT-2026-06-003`
- **T036 High-DPI rendering:** blocked by the upstream rendering library’s scaling fix; nested Form XObjects affect 12% of the pilot corpus. `WS-06 / S14, CMT-2026-09-001`
- **T030 license review:** engineering can keep evaluating replacements, but Legal must clear the AGPL whole-bundle copyleft gate before it can close. `WS-04 / CMT-2026-08-002`
- **Windows release readiness:** an Authenticode certificate must be budgeted/procured; unsigned binaries trigger SmartScreen. `WS-06 / S9`

Release-checklist impact:

- **T011 (v1.0.0 release gates and docs) is active but cannot close until both T005 Docker size/CVE and T029 Windows signing are green.** Audit-log schema alignment is also an open pre-release blocker. `WS-03 / S7–S10`
- The release board set a **no-ship after 2026-10-15** if T005 and T029 remain ungreen. `WS-03 / CMT-2026-09-002`
- Separately, the checklist is also exposed to the legacy-policy migration (T006) and the 4.7 GB/8 GB workstation large-file OOM fix (T031), both identified as release dependencies. `WS-01 / CMT-2026-06-001`; `WS-05 / CMT-2026-08-003`
