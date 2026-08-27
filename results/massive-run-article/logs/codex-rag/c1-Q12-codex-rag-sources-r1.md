# Several streams remain blocked while others are only reopened. As of **2026-09-22**, what work can still advance in parallel, what cannot progress until an external dependency moves, and what release-checklist work is gated on packaging and Windows signing?

<!-- RESPONSE_START -->

As of 2026-09-22:

- Work that can advance in parallel: finish the reopened Docker image slim-down and CVE remediation (T005); correct the CLI audit-log output to match its JSON schema and re-verify it; and continue drafting release notes/evidence. 【SRC-SLACK-06】【SRC-CU-CIPH-26】【SRC-CU-CIPH-21】
- Work that cannot advance yet:
  - Multi-site authenticated handshake (CIPH-34) remains blocked: it times out under high latency and must wait for the encryption/crypto path to settle; increasing timeouts was explicitly rejected. 【SRC-MEET-11】【SRC-CU-CIPH-34】
  - High-DPI rendering for nested Form XObjects remains blocked on the upstream `pdf-lib-core` defect (or a later product decision to accept the limitation/change renderer). 【SRC-SLACK-58】
  - Windows signing cannot complete until procurement supplies a code-signing certificate. 【SRC-SLACK-37】【SRC-GDOC-39】

Release checklist status: T011/CIPH-21 remains active and cannot close until both **T005 Docker packaging** clears its image-size/CVE gate and **T029 Windows compatibility** clears code signing/Defender–SmartScreen validation. Windows packaging itself is already working; the remaining Windows gate is certificate procurement, wiring signing into the release build, and validating the signed artifact. The audit-log schema mismatch is an additional release blocker. 【SRC-CU-CIPH-21】【SRC-GDOC-39】【SRC-MEET-10】
