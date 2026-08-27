# Several streams remain blocked while others are only reopened. As of **2026-09-22**, what work can still advance in parallel, what cannot progress until an external dependency moves, and what release-checklist work is gated on packaging and Windows signing?

<!-- RESPONSE_START -->

## Answer

As of **2026-09-22** (the day the handshake block was confirmed), the board splits into three groups.

---

### 1. Work that can still advance in parallel

None of these depends on a blocked stream, and each has an owner actively pushing it:

| Item | State on 2026-09-22 | Next move available |
|---|---|---|
| **CIPH-15 / T005 — Docker Packaging** | Active (Reopened) since 2026-06-25 | Evan continues the slim-down: multi-stage build in place, Alpine base swapped, unused OCR/runtime packages removed. As of the 2026-08-12 check the image is still over the ~450MB target and the CVE scan still fails; remaining work is the Python site-packages layer and chasing the CVE finding (SRC-CU-CIPH-15, SRC-SLACK-06) |
| **CIPH-26 / T016 — Audit Trail Logging** | Active; CLI-emitted records fail schema validation (Diana's 2026-09-18 verify) | Bob explicitly has "another pass queued" to reconcile emitted records with the defined companion JSON schema. Purely internal — Charlie confirmed on 2026-09-15 this is "schema versus emitted records," not a packaging issue (SRC-MEET-10, SRC-CU-CIPH-26) |
| **CIPH-32 — Storage Quota Management** | Active (Reopened 2026-09-15, refactored 2026-09-18) | Already moving: Bob replaced the hard 500MB halt with a 10% buffer tolerance; Evan re-tested on 2026-09-18 with no premature halts (SRC-SLACK-23) |
| **CIPH-41 — Stream-chunk multi-GB PDF loads** | Active (Reopened) | Charlie's buffer-release refactor continues; acceptance is no leak on files ≥2GB (SRC-CU-CIPH-41) |
| **CIPH-24 — Manual Review Threshold (low-confidence OCR)** | Active | Quarantine folder, metadata and UI markers hold together end-to-end (2026-09-18 pass); the 90% confidence-threshold tuning needs another round of testing (SRC-SLACK-11, SRC-CU-CIPH-24) |
| **CIPH-18 — OCR Fallback** | Active | Per-page multiprocessing pool and confidence retuning are being integrated into the scan pipeline (SRC-CU-CIPH-18) |
| **T018 — Local runtime static linking** | Active (study) | Evan still to select an approach and attempt an end-to-end static compile; Alice flagged it as tracked "alongside the Docker slim-down" (SRC-GDOC-12, SRC-SLACK-14) |
| **T032 — Exportable redaction-profile schema** | Active | Design shape defined; the export API and REST-contract verification are unstarted and unblocked (SRC-GDOC-26) |

---

### 2. Work that cannot progress until an external dependency moves

**Genuinely external (a third party must act):**

- **CIPH-46 / T036 — High-DPI PDF coordinate scaling.** Blocked 2026-09-10. Root cause is a bug deep in the C++ core of the upstream `pdf-lib-core` rendering library (coordinate handling for nested Form XObjects under a parent transform). Charlie confirmed it cannot be patched locally, opened an upstream issue, and the maintainers **have not responded**. The flattening workaround was rejected (file-size blow-up, possible loss of text layers). Alice's decision: leave it blocked and decide whether to ship with the limitation or replace the rendering library; Diana to document it as a known issue. (SRC-SLACK-58, SRC-GDOC-49, SRC-CU-CIPH-46)
- **CIPH-17 — Coordinate/offset drift in multi-page PDFs.** Blocked pending upstream `pdfminer.six` PR #992, still unmerged. A local fork was evaluated and rejected on maintenance risk, and no local workaround was adopted. (SRC-CU-CIPH-17)
- **CIPH-39 / T029 — Windows code-signing.** Blocked on procuring a code-signing certificate — an external/procurement dependency, not engineering. Evan on 2026-09-02: "this isn't something we can work around on the engineering side, we need the certificate." Alice took the certificate process. (SRC-SLACK-37, SRC-GDOC-39)

**Blocked, but on internal dependencies (no external actor):**

- **CIPH-34 — Authenticated handshake for multi-site node sync.** Blocked 2026-09-22. Nominal-latency validation passed back on 2026-08-08, but Diana's simulated high-latency run never completes the exchange. Bob attributes it to per-packet AES-256 overhead on the output path pushing the exchange past the timeout window. The team explicitly **refused a timeout bump** ("bumping timeouts just hides it" — Evan), refused to invent a workaround in the meeting, and left the high-latency repro standing to re-check when the encryption path or handshake design changes. Multi-site rollout cannot proceed until this clears. (SRC-MEET-11, SRC-SLACK-27, SRC-CU-CIPH-34)
- **CIPH-47 / T037 — Async job scheduler.** Blocked since 2026-08-25 on a confirmed concurrent manifest-write race that costs ~10% throughput; resolution depends on how the T026 worker pool serializes result writing. Not production-stable until fixed. (SRC-GDOC-50, SRC-CU-CIPH-47)
- **CIPH-29 — Offline auth with key rotation.** Blocked since 2026-08-05: key rotation cannot complete without network access in an air-gapped setting; no resolution found. (SRC-CU-CIPH-29)

---

### 3. Release-checklist work gated on packaging and Windows signing

**CIPH-21 / T011 — Release v1.0 Gates (Evan, Active).** The original dependency set (T001–T006, T010) is satisfied except for one item, and two gates hold the checklist open:

1. **Packaging gate — T005 Docker image slim-down/CVE.** T005 is the only unmet dependency from the original checklist (reopened 2026-06-25 at 2.1GB). Image size is still over the ~450MB target and CVE verification still fails as of the 2026-08-12 review. Diana: reopened status stands until both size and CVE are clean.
2. **Windows signing gate — T029.** Note the distinction: **Windows packaging is no longer the blocker.** The backslash path defects were fixed 2026-08-10, a build artifact was produced and ran clean on Windows by 2026-08-12, and Evan confirmed the engineering work for the build itself is complete. What remains is solely the missing code-signing certificate — the unsigned binary trips SmartScreen and gets flagged by Defender, and site IT policies would block execution outright on target workstations. Procuring the certificate and wiring signing into the release build step is the one remaining item to clear T029 and, by extension, T011.

Diana placed a **security-gate hold** on the release pending both of these. Confirmed again at the 2026-09-15 pre-release audit: Docker slim-down/CVE open, Windows signing open, high-DPI blocked upstream — "no one closes those today."

Also riding on the checklist, though not a packaging or signing item: the **audit-log gate stays red** (CIPH-26) because CLI-emitted records don't validate against the defined schema, which undercuts the audit trail as release evidence. Evan's summary: "Release isn't opening with any of those unresolved." Release notes were drafted in parallel while all gates stayed open.

---

### Sources cited

`SRC-MEET-11` (2026-09-22 Handshake Protocol Deep Dive) · `SRC-SLACK-27` (Node Sync Handshake Validation) · `SRC-CU-CIPH-34` · `SRC-MEET-10` (2026-09-15 Pre-Release Audit) · `SRC-CU-CIPH-21` (Release v1.0 Gates) · `SRC-GDOC-05` (Release Checklist DOC-2005) · `SRC-GDOC-39` (Windows Build Signing Gap DOC-2039) · `SRC-CU-CIPH-39` · `SRC-SLACK-37` (Windows Signing Gap) · `SRC-SLACK-38` (Windows Build Artifact) · `SRC-CU-CIPH-15` / `SRC-SLACK-06` / `SRC-GDOC-06` (Docker packaging) · `SRC-CU-CIPH-26` / `SRC-GDOC-11` (Audit Trail Logging) · `SRC-CU-CIPH-46` / `SRC-GDOC-49` / `SRC-SLACK-58` / `SRC-GDOC-30` (High-DPI) · `SRC-CU-CIPH-17` (pdfminer.six drift) · `SRC-CU-CIPH-47` / `SRC-GDOC-50` (async scheduler) · `SRC-CU-CIPH-29` (offline auth) · `SRC-SLACK-23` / `SRC-GDOC-16` (storage quota) · `SRC-CU-CIPH-41` (large-file chunking) · `SRC-CU-CIPH-24` / `SRC-SLACK-11` (manual review threshold) · `SRC-CU-CIPH-18` (OCR fallback) · `SRC-GDOC-12` / `SRC-SLACK-14` (static linking) · `SRC-GDOC-26` (profile export) · `SRC-CU-CIPH-31` / `SRC-GDOC-35` (AES-256, Completed 2026-08-07)
