# Several streams remain blocked while others are only reopened. As of **2026-09-22**, what work can still advance in parallel, what cannot progress until an external dependency moves, and what release-checklist work is gated on packaging and Windows signing?

<!-- RESPONSE_START -->

As of 2026-09-22, these reopened/active items can proceed in parallel:

- Engine: T006 legacy JSON→YAML migration and T008 OCR-fallback integration/tuning. 【WS-01, Active Work】
- Packaging: T005 Docker slimming and CVE remediation. It is reopened—not externally blocked. 【WS-03, Active Work】
- Compliance: T014 quarantine workflow, T016 audit-log schema alignment, and T030 licensed-parser alternative search. 【WS-04, Active Work】
- Performance/storage: T031 large-file stream-buffer refactor and T022 quota-monitor tolerance refactor. 【WS-05, Active Work; WS-07, Active Work】
- Windows: T029 engineering can continue; path handling is fixed. The release hold is procurement, not an engineering block. 【WS-06, Active Work】
- REST/CLI has no active work; REST authentication is deferred to v1.1. 【WS-02, Active Work; Decisions】

Work that cannot advance to completion until an outside dependency moves:

- T007 offset-mismatch fix: blocked on upstream `pdfminer.six` #992; the rejected fork means no safe local workaround. Any workaround also needs written Legal sign-off. 【WS-01, Blockers and Dependencies】
- T036 High-DPI rendering: blocked on upstream rendering-library scaling math; nested Form XObjects affect 12% of the pilot corpus. 【WS-06, Blockers and Dependencies】
- Windows releaseability: T029 requires procurement of an Authenticode certificate; unsigned binaries trigger SmartScreen. 【WS-06, Active Work】
- T030 cannot be closed by engineering search alone: it remains subject to the Legal P0 gate on AGPL/copyleft exposure. 【WS-04, Blockers and Dependencies】

Release-checklist impact:

- T011/CIPH-21—the v1.0.0 release gates and docs—cannot close until both T005 and T029 are green. 【WS-03, Blockers and Dependencies】
- For T005, the interim RC threshold is 800 MB only if CVE-clean; GA remains approximately 450 MB. 【WS-03, Active Work】
- The release audit also holds on audit-log schema alignment, so T016 should run alongside packaging and certificate procurement. 【WS-03, Active Work; WS-04, Active Work】
- There is a hard no-ship outcome after **2026-10-15** if T005 and T029 are not green. 【WS-03, Blockers and Dependencies】
