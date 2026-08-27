# As of the final CipherDoc snapshot on **2026-09-22**, is the toolkit ready to ship v1.0.0? Give a clear go/no-go, name every release gate that is still open, and cite the evidence that keeps each gate from closing.

<!-- RESPONSE_START -->

**No-go — CipherDoc is not ready to ship v1.0.0 as of 2026-09-22.** The release board’s gate task is still active; it cannot close until Docker/CVE and Windows signing are green, and the pre-release audit also keeps audit-log alignment and high-DPI rendering open. `[WS-03; SRC-CU-CIPH-21; SRC-MEET-10]`

Open release gates/holds:

- **Docker image size and CVE cleanliness (T005 / CIPH-15):** GA requires an approximately 450 MB image; it still exceeds that target and CVE verification is failing. The interim 800 MB RC threshold also requires a clean CVE result. `[WS-03; SRC-CU-CIPH-15; SRC-SLACK-06]`

- **Windows code signing (T029 / CIPH-39):** The build is unsigned because no Authenticode certificate has been procured/configured. Defender/SmartScreen flags it as untrusted, potentially blocking installation. `[WS-03; WS-06; SRC-CU-CIPH-39; SRC-SLACK-37]`

- **Audit-log schema alignment (T016 / CIPH-26):** CLI-emitted audit records do not match the defined schema. QA explicitly keeps the audit gate red until they match. `[WS-04; SRC-CU-CIPH-26; SRC-MEET-10]`

- **High-DPI PDF coordinate alignment (T036 / CIPH-46):** The issue is blocked on an upstream rendering-library defect; nested Form XObjects fail in 12% of the pilot corpus, and no accepted workaround exists. `[WS-06; SRC-CU-CIPH-46; SRC-SLACK-58]`

- **Multi-page PDF offset/coordinate drift (T007 / CIPH-17):** The upstream `pdfminer.six` PR #992 remains unmerged; the rejected local-fork approach leaves no safe workaround. Any pre-normalization workaround also requires written Legal sign-off. `[WS-01; SRC-CU-CIPH-17]`

- **Third-party license compliance (T030 / CIPH-40):** This is a hard Legal P0 gate: the candidate PDF parser is AGPL-licensed, which triggers whole-bundle copyleft. An Apache/MIT replacement must be identified and adopted; engineering research alone cannot close the gate. `[WS-04; SRC-CU-CIPH-40]`

- **Air-gapped key escrow/rotation (T019 / CIPH-29):** Offline key rotation cannot complete without centralized authority. InfoSec has approved a split master-key escrow design, but it remains blocked until built. `[WS-04; SRC-CU-CIPH-29; SRC-SLACK-17]`

The CORS/security scan gate is cleared, and REST API auth is explicitly deferred to v1.1 rather than a v1.0 blocker. `[WS-03; SRC-CU-CIPH-20; WS-02]`
