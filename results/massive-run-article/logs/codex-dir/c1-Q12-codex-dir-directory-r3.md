# Several streams remain blocked while others are only reopened. As of **2026-09-22**, what work can still advance in parallel, what cannot progress until an external dependency moves, and what release-checklist work is gated on packaging and Windows signing?

<!-- RESPONSE_START -->

As of Sep 22:

- **Can advance in parallel:** continue the release checklist/evidence and release-notes work; the completed prerequisite gates (T001–T006, T010) are already satisfied. Continue Docker remediation/CVE verification and prepare the Windows signing step. [CIPH-21](c1/med-synth/tasks/CIPH-21-Release-v1-Gates.md:12)
- **Cannot advance to closure until the external dependency arrives:** T029 cannot clear until procurement supplies an Authenticode certificate; then the build must be signed and pass Defender/SmartScreen. The build artifact and packaging already work—certificate procurement is the remaining blocker. [Windows audit](c1/med-synth/documentation/sources/2026-09-02-Windows-Compatibility-Audit-Report.md:9) [T029](c1/med-synth/tasks/CIPH-39-Windows-Compatibility.md:12)
- **Release-checklist gate:** T011 remains active and cannot close/release until both T005’s Docker size/CVE gate and T029’s Windows-signing gate are green; no-ship after **2026-10-15** if either remains open. [WS-03](c1/work-states/WS-03-ops.md:31) [Sep 22 brief](c1/briefs/2026-09-22-daily-brief.md:7)
