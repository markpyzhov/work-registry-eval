# Several streams remain blocked while others are only reopened. As of **2026-09-22**, what work can still advance in parallel, what cannot progress until an external dependency moves, and what release-checklist work is gated on packaging and Windows signing?

<!-- RESPONSE_START -->

## Answer

**As of 2026-09-22, the board splits three ways: work the team can still move on its own, work parked behind an external party, and the release checklist itself, which is held by exactly two gates — Docker packaging and Windows code-signing.**

---

### 1. Work that can still advance in parallel (no external dependency)

These streams are Active and entirely under team control, so they can proceed simultaneously:

- **Docker packaging / image slim-down + CVE (T005 / CIPH-15, Evan)** — Active (Reopened). The image was 2.1GB at the 2026-06-25 reopen; a multi-stage build, an Alpine base swap, and removal of unused OCR/runtime packages have all landed, but at the 2026-08-12 verification the image still exceeded the ~450MB target and the CVE scan still failed. Evan's remaining work is named: fluff in the Python site-packages layer, and chasing down what trips the CVE scan. No external party is involved. (SRC-CU-CIPH-15, SRC-SLACK-06, SRC-GDOC-05)
- **Windows code-signing certificate procurement (T029 / CIPH-39, Evan; Alice chasing)** — Active. The build artifact exists and runs; the only remaining step is procuring a certificate and wiring signing into the release build step. Evan was explicit that this "isn't something we can work around on the engineering side." It is a procurement dependency rather than an engineering one, but it is being actively chased in parallel with everything else. (SRC-GDOC-39, SRC-SLACK-37, SRC-CU-CIPH-39)
- **Audit-trail logging schema/record reconciliation (T016 / CIPH-26, Diana owner, Bob implementing)** — Active. CLI integration landed 2026-09-10; Diana's 2026-09-18 verification found the CLI-emitted audit records inconsistent with the defined companion JSON schema. Charlie confirmed this "isn't a packaging issue — it's schema versus emitted records," and Bob has another pass queued. Purely internal, fixable now. (SRC-CU-CIPH-26, SRC-MEET-10)
- **Large-file stream chunking buffer-release refactor (T041 / CIPH-41, Charlie)** — Active (Reopened). Chunking merged 2026-08-16; files at/above 2GB still leaked because per-chunk buffers were not explicitly released. `tracemalloc` traced it to the PDF loader's page-buffer handling. Early local testing on a 2.3GB sample shows flat memory, but the fix is not yet validated against the full large-file corpus, and Diana is waiting on a build to re-run the stress case. Internal work, moves independently. (SRC-CU-CIPH-41, SRC-GDOC-42, SRC-GDOC-27, SRC-SLACK-44)
- **License-compliance replacement-parser search (Charlie)** — Active (Reopened). The Ghostscript (AGPLv3) swap reintroduced the same problem one layer down because the replacement was also AGPL. Charlie is searching for an Apache 2.0 / MIT-licensed PDF parser; a couple of candidates exist but none covers everything the old library did. Evaluation can continue in parallel. A separate lower-priority item — verifying `eng.traineddata` / `tessdata_best` provenance as public-domain/CC0 — is pending Evan and is also independent. (SRC-GDOC-41, SRC-SLACK-41)
- **OCR fallback parallelization and scan-pipeline wiring (T018 / CIPH-18, Charlie; Diana integrating)** — Active. The per-page multiprocessing pool and confidence-threshold retuning are in; Diana has begun wiring the OCR output into the scan pipeline while parallelization remains Active. Independent of every blocked stream. (SRC-CU-CIPH-18)

---

### 2. Work that cannot progress until an external dependency moves

- **Node-sync authenticated handshake (T034 / CIPH-34, Bob)** — **Blocked, reopened the same day (2026-09-22).** Diana reopened it after the handshake timed out over a simulated high-latency link, never completing the exchange, and degrading further the slower the link. Bob attributed the per-round-trip cost to the AES-256 pipeline on the output path pushing the exchange past the timeout window. In the same-day deep dive, Evan rejected a timeout bump ("bumping timeouts just hides it"), Bob had no fix that keeps the current exchange as-is, and Alice left it blocked: it depends on the encryption path, "and we're not inventing a workaround in this meeting." Diana is holding the high-latency repro in place to re-check when encryption or the handshake design changes. Note this is an *internal* dependency (the crypto path / handshake redesign), not a third party — but it is a hard block that no amount of parallel effort clears. (SRC-SLACK-27, SRC-MEET-11, SRC-CU-CIPH-34)
- **High-DPI PDF coordinate scaling (T036 / CIPH-46, Charlie)** — **Blocked on a genuinely external party.** The rotation fix works for simple cases but breaks on documents with nested Form XObjects, traced to a known bug in `pdf-lib-core`'s coordinate handling when a parent transform is applied. Charlie: it's deep in their C++ core, cannot be patched locally, and the upstream maintainers have not responded to his issue. Flattening PDFs as a workaround would inflate file size and risk losing text layers. Alice left it blocked pending a decision on shipping with the limitation or replacing the rendering library entirely; Diana will document it as a known issue affecting a small subset of complex documents. (SRC-SLACK-58, SRC-GDOC-49, SRC-CU-CIPH-46)
- **Multi-page coordinate/offset drift (T017 / CIPH-17, Charlie)** — **Blocked on upstream `pdfminer.six` PR #992**, still unmerged as of the 2026-09-10 check with no maintainer movement. Forking was formally evaluated and rejected as more long-term risk than the wait, and no local workaround was adopted. Charlie: "I'd rather eat the delay than take on a parser fork we can't maintain." Alice flagged it as a real risk to the v1.0 timeline. (SRC-SLACK-07, SRC-CU-CIPH-17)
- **Async batch job scheduler (T037 / CIPH-47, Bob)** — **Blocked** since 2026-08-25 on the concurrent I/O race between async workers and the existing multi-threaded batch pool, which cuts throughput ~10% versus the sync baseline as workers retry/serialize around corrupted manifest-write recovery. Alice: "A 10% hit is not shippable." Resolution depends on how the T026 worker pool's result-writing is serialized; Bob is holding all further async work. Diana captured repro steps for re-running against a candidate fix. (SRC-CU-CIPH-47, SRC-SLACK-61, SRC-GDOC-50)
- **Offline auth with key rotation for air-gapped installs (T029-adjacent / CIPH-29, Diana, High)** — **Blocked** since 2026-08-05: testing against a local auth mock showed key rotation cannot complete without network access in an air-gapped setting, with no resolution found. (SRC-CU-CIPH-29)

---

### 3. Release-checklist work gated on packaging and Windows signing

The release checklist is **T011 / CIPH-21 (Release v1.0 Gates, Evan)** — status **Active**, held open by **exactly two unresolved gates**:

1. **T005 — Docker packaging slim-down / CVE verification.** Six of seven original checklist dependencies (T001–T004, T006, T010) are Completed; T005 was the sole unmet one at the 2026-07-12 draft and remains unmet. The checklist cannot close until image size and CVE both come clean.
2. **T029 — Windows Defender/SmartScreen code-signing.** Diana placed a security-gate hold on the release pending both items.

An important distinction on the packaging question: **Windows *packaging* is no longer a blocker.** The backslash path-handling defects were fixed 2026-08-10 and a working, sanity-check-passing Windows build artifact was produced 2026-08-12. Evan was careful at the time not to call Windows compatibility closed — "code-signing is a separate item we haven't even started on yet." The Windows audit (DOC-2039) states that procuring a code-signing certificate and wiring signing into the release build step is the *sole* remaining item before T029 clears, "and, by extension, the T011 release checklist, which is holding on this exact signing gap alongside the T005 image slim-down." So the packaging gate on the checklist is the **Docker** image (T005), not the Windows build.

Two further release-gate facts as of the 2026-09-15 pre-release audit:

- **Release notes were drafted in parallel while the gates stayed open** — that drafting was allowed to proceed and is not itself blocked. (SRC-CU-CIPH-21)
- **The audit-log mismatch is being kept visible as a release blocker** alongside the two formal gates, even though it is not one of the T005/T029 acceptance criteria. Evan: "That stacks on top of the Docker and Windows holds." Alice: "No one closes those today." Diana is keeping the audit-log gate red until schema and records match. Alice also listed the upstream high-DPI block as staying on the board at that review. (SRC-MEET-10)

**Net:** release cannot open on any of Docker slim-down/CVE, Windows signing, the audit-log schema mismatch, or the upstream high-DPI issue. Of those four, three are internally actionable right now and can run concurrently; only high-DPI (and the related pdfminer.six offset drift) genuinely waits on an unresponsive third party. Windows signing is actionable but sits with procurement rather than engineering.

---

### Sources cited

`SRC-MEET-11` (2026-09-22 Handshake Protocol Deep Dive) · `SRC-SLACK-27` (Node Sync Handshake Validation, last activity 2026-09-22) · `SRC-CU-CIPH-34` · `SRC-MEET-10` (2026-09-15 Pre-Release Audit) · `SRC-GDOC-39` / DOC-2039 (Windows Build Signing Gap) · `SRC-SLACK-37` (Windows Signing Gap) · `SRC-SLACK-38` (Windows Build Artifact) · `SRC-CU-CIPH-39` · `SRC-CU-CIPH-21` (Release v1.0 Gates) · `SRC-GDOC-05` / DOC-2005 (Release Checklist draft + gate table) · `SRC-CU-CIPH-15` / `SRC-SLACK-06` / `SRC-GDOC-06` (Docker packaging) · `SRC-CU-CIPH-26` / `SRC-GDOC-11` (Audit Trail Logging) · `SRC-SLACK-58` / `SRC-GDOC-49` / `SRC-CU-CIPH-46` (High-DPI upstream block) · `SRC-SLACK-07` / `SRC-CU-CIPH-17` (pdfminer.six #992) · `SRC-CU-CIPH-47` / `SRC-SLACK-61` / `SRC-GDOC-50` / `SRC-GDOC-31` (Async batch scheduler) · `SRC-CU-CIPH-41` / `SRC-GDOC-42` / `SRC-GDOC-27` / `SRC-SLACK-44` (Large-file chunking + leak) · `SRC-GDOC-41` / `SRC-SLACK-41` (License compliance audit) · `SRC-CU-CIPH-18` (OCR fallback) · `SRC-CU-CIPH-29` (Offline auth) · `SRC-CU-CIPH-31` / `SRC-GDOC-35` / `SRC-SLACK-21` (AES-256 pipeline, Completed 2026-08-07)
