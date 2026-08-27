# As of **2026-09-22**, which CipherDoc tasks are blocked, and for each is the block upstream/external or internal? State the root cause and the listed task assignee.

<!-- RESPONSE_START -->

As of 2026-09-22, five CipherDoc tasks are explicitly **Blocked**:

- **T007 / CIPH-17 — Charlie:** **Upstream/external.** `pdfminer.six` whitespace-handling issue/PR #992 remains unmerged; the team rejected maintaining a local parser fork. *(WS-01; SRC-CU-CIPH-17)*

- **T019 / CIPH-29 — Diana:** **Internal.** The air-gapped key-rotation design requires centralized authority/network access; the approved split master-key escrow implementation is not yet built. *(WS-04; SRC-CU-CIPH-29)*

- **T024 / CIPH-34 — Bob:** **Internal.** Authenticated node handshakes time out on high-latency links; resolution depends on stabilizing the encryption path, and the timeout-bump workaround was declined. *(WS-07; SRC-CU-CIPH-34)*

- **T036 / CIPH-46 — Charlie:** **Upstream/external.** An upstream rendering-library scaling-math bug causes 5–10 px redaction-coordinate drift on 4K displays at 200% scaling. *(WS-06; SRC-CU-CIPH-46)*

- **T037 / CIPH-47 — Bob:** **Internal.** A concurrent manifest-write/I/O race reduces throughput by about 10% and can corrupt JSON under load; it depends on the multi-threading work. *(WS-05; SRC-CU-CIPH-47)*

`T030 / CIPH-40` has a hard Legal gate, but its authoritative Work State status is **reopened/active**, not Blocked. *(WS-04; SRC-CU-CIPH-40)*
