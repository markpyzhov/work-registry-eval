# Several streams remain blocked while others are only reopened. As of **2026-09-22**, what work can still advance in parallel, what cannot progress until an external dependency moves, and what release-checklist work is gated on packaging and Windows signing?

<!-- RESPONSE_START -->

As of 2026-09-22:

- **Can advance in parallel:** Docker packaging remediation (reduce image to ~450MB and clear CVEs), audit-log CLI/schema alignment, the Apache/MIT PDF-parser search for license compliance, and the large-file buffer-release refactor. These are active/reopened—not formally blocked. (SRC-CU-CIPH-15, SRC-CU-CIPH-26, SRC-CU-CIPH-40, SRC-CU-CIPH-41)

- **Cannot progress until a dependency moves:**
  - **Multi-site handshake (CIPH-34):** blocked by high-latency timeouts pending the encryption/crypto path; the team explicitly rejected a timeout-bump workaround. (SRC-MEET-11, SRC-CU-CIPH-34)
  - **High-DPI coordinate scaling (CIPH-46):** blocked on the upstream rendering library’s scaling/XObject defect; there is no safe local fix. (SRC-SLACK-58, SRC-GDOC-49)
  - **Async batch scheduler (CIPH-47):** blocked by the concurrent manifest-write I/O race and its ~10% throughput regression, dependent on result-write serialization in the worker path. (SRC-GDOC-50, SRC-CU-CIPH-47)

- **Release checklist gates:** T011 cannot close until **T005 Docker packaging** clears its image-size and CVE checks, and until the **Windows compatibility/signing gate (T029/CIPH-39)** clears. Windows packaging itself is already working; the remaining external dependency is procurement of a code-signing certificate, followed by wiring signing into the release build and validating no Defender/SmartScreen warning. (SRC-GDOC-05, SRC-GDOC-39)

Additionally, the audit-log schema/emitted-record mismatch remains a separate release blocker, so release does not open with any of Docker, Windows signing, or audit logging unresolved. (SRC-MEET-10)
