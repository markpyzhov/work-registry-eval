# Several streams remain blocked while others are only reopened. As of **2026-09-22**, what work can still advance in parallel, what cannot progress until an external dependency moves, and what release-checklist work is gated on packaging and Windows signing?

<!-- RESPONSE_START -->

## Answer

### Snapshot as of 2026-09-22

The board splits three ways: streams that are genuinely unblocked and can run concurrently, streams held by a dependency the team does not control, and the v1.0 release checklist, which is pinned by two named gates plus a live audit-log mismatch.

---

### 1. Work that can still advance in parallel

**Docker image slim-down / CVE remediation (T005, CIPH-15 — Active (Reopened), Evan).** Reopened 2026-06-25 after the image measured 2.1GB. Multi-stage build, Alpine base swap, and removal of unused OCR/runtime packages are all done; the 2026-08-12 verification still showed the image over the ~450MB target with CVE verification failing. Evan named the remaining work himself: fluff still in the Python site-packages layer, and chasing down what trips the CVE scan. Nothing external gates this — it is engineering effort that can proceed today. *(SRC-CU-CIPH-15, SRC-SLACK-06, SRC-GDOC-05)*

**Large-file stream chunking buffer-release refactor (T041, CIPH-41 — Active (Reopened), Charlie).** Chunking merged to mainline 2026-08-16, then reopened when files at and above 2GB leaked memory because per-chunk buffers were not released. Charlie is refactoring the stream-chunk handler to release eagerly after each chunk; a 2.3GB local sample already shows flat memory instead of the previous linear climb, but the fix is not yet validated against the full large-file corpus. Independent of every blocked stream. *(SRC-GDOC-42, SRC-SLACK-44, SRC-CU-CIPH-41)*

**Memory-leak patching in the PDF loader.** The identification pass (Bob, from 2026-08-17; unblocked 2026-08-21 when Charlie switched to stdlib `tracemalloc` after the usual profiler proved unavailable in the offline lab) traced retained allocations to the loader's page-buffer handling across chunk boundaries. Patching the loader is explicitly scoped as separate follow-up work and can run. *(SRC-GDOC-27)*

**Audit-trail logging (T016, CIPH-26 — Active, Diana/Bob).** Loader refactor, SHA-256 input hashing, schema definition, and CLI wiring (2026-09-10) are all done. Verification on 2026-09-18 found CLI-emitted records inconsistent with the defined schema. Bob has "another pass queued." Charlie confirmed at the 2026-09-15 audit that this is schema-versus-emitted-records, **not** a packaging problem — so it advances independently of the packaging and signing gates, even though it is itself a release blocker. *(SRC-CU-CIPH-26, SRC-MEET-10)*

**OCR fallback (CIPH-18 — Active, Charlie).** Tesseract POC succeeded; the page-serial loop bottleneck was addressed with a per-page multiprocessing pool and retuned confidence thresholds. Diana has begun wiring OCR fallback output into the scan pipeline while parallelization work continues. Two people working concurrently on the same stream. *(SRC-CU-CIPH-18)*

**License-compliance parser search (Charlie).** The Ghostscript (AGPLv3) swap was reopened when the replacement parser turned out to also be AGPL — same license category, one layer down. Charlie is comparing Apache 2.0 / MIT candidates against the rasterizer module's requirements; Alice named this the priority at the 2026-08-15 sync. The evaluation work proceeds now, though *confirming* a replacement depends on a suitable library existing. *(SRC-GDOC-41, SRC-MEET-08)*

**Exportable redaction-profile schema (T032).** Design pass complete as of 2026-08-12; implementing the schema-export API and verifying it against the REST contract remain open and unclaimed. *(SRC-GDOC-26)*

**Static-linking study for the air-gapped local runtime (Evan).** Full-static versus hybrid bundling of `re2` and the C dependencies; tracked by the release checklist alongside the Docker slim-down. *(SRC-SLACK-14)*

**Sentry crash-reporter privacy audit.** CLI-side telemetry opt-out was verified Completed by network trace on 2026-08-24; the third-party Electron crash reporter has not been audited for whether it independently respects the opt-out variable. Separate, actionable. *(SRC-GDOC-51)*

**Release notes.** Explicitly drafted in parallel while the gates stayed open — the sources record this as accepted practice, not a violation. *(SRC-CU-CIPH-21)*

---

### 2. Work that cannot progress until an external dependency moves

**High-DPI PDF coordinate scaling (T036, CIPH-46 — Blocked, Charlie).** Charlie's rotation fix works for simple cases but breaks completely on documents with nested Form XObjects. Root cause is a known bug in the upstream rendering library `pdf-lib-core` — how it handles XObject coordinates when a parent transform is applied. Charlie's assessment: "It's deep in their C++ core." He opened an issue with the upstream maintainers and they have not responded. The PDF-flattening workaround Evan proposed would blow up file size and risk losing text layers, so it was not adopted. Alice's 2026-09-10 call was to leave it blocked and decide whether to ship with the limitation or replace the rendering library entirely; Diana noted it affects only a small subset of complex documents and should be documented as a known issue. Still listed as open at the 2026-09-15 pre-release audit. *(SRC-SLACK-58, SRC-CU-CIPH-46, SRC-GDOC-49, SRC-MEET-10)*

**Coordinate/offset drift in multi-page PDFs (CIPH-17 — Blocked, Charlie).** Traced to whitespace handling in upstream `pdfminer.six`, pending PR #992. Charlie re-checked on 2026-09-10: still unmerged, no maintainer movement. Forking pdfminer.six was formally evaluated and rejected on 2026-08-20 — long-term maintenance risk of owning a PDF parser exceeds the cost of waiting. Alice flagged this as "a real risk for the v1.0 timeline"; Charlie's position was he would rather eat the delay. No local workaround adopted. *(SRC-SLACK-07, SRC-CU-CIPH-17)*

**Windows code-signing (T029, CIPH-39 — Active, Evan).** Gated on procurement, not engineering. Evan is unambiguous: "this isn't something we can work around on the engineering side, we need the certificate." As of 2026-08-15 he was still waiting on procurement with no firm timeline. Alice took the action to chase the certificate process. *(SRC-SLACK-37, SRC-GDOC-39, SRC-MEET-08)*

**Tesseract `eng.traineddata` provenance.** A separate, lower-priority open item pending Evan's trace of the `tessdata_best` training-corpus provenance against public-domain/CC0 — dependent on an external community repository's records. *(SRC-GDOC-41)*

*Distinguish these from internally blocked streams,* which are stuck but not on an outside party:
- **Authenticated node-sync handshake (CIPH-34 — Blocked, reopened 2026-09-22).** Diana reopened it that morning: over a simulated high-latency link the handshake times out and never completes, degrading as the link slows. Bob traced it to the AES-256 pipeline on the output path adding per-packet overhead that pushes the exchange past the timeout window. Evan rejected a timeout bump as concealment ("if the link is slow enough, we still fail"), and Bob has no fix that preserves the current exchange. Alice's ruling: stays blocked, no workaround invented in the meeting; revisit when the crypto path moves. Diana left the high-latency repro in place. *(SRC-SLACK-27, SRC-MEET-11, SRC-CU-CIPH-34)*
- **Async batch job scheduler (T037, CIPH-47 — Blocked, Bob).** Concurrent async workers sharing I/O with the existing multi-threaded pool corrupt the shared results manifest; recovery-path retries cut throughput ~10% versus the sync baseline. Alice: "A 10% hit is not shippable." *(SRC-CU-CIPH-47, SRC-SLACK-61, SRC-GDOC-50)*
- **Offline auth with key rotation (CIPH-29 — Blocked, High, Diana).** Key rotation cannot complete without network access in an air-gapped setting; no resolution found. *(SRC-CU-CIPH-29)*

---

### 3. Release-checklist work gated on packaging and Windows signing

**T011 / CIPH-21 "Release v1.0 Gates" is Active, owner Evan, with a security-gate hold placed by Diana.**

The original dependency set (T001–T006, T010) is six-sevenths satisfied — Core Redaction Engine, Financial Regex Detection, Batch CLI, REST API Endpoints, Redaction Policy Config, and Security Audit are all Completed. **T005 Docker Packaging is the one unmet dependency from that original list.**

Two gates hold the checklist:

| Gate | Nature of block | Status |
|---|---|---|
| **T005 — Docker image slim-down / CVE** | Packaging. Image over ~450MB target; CVE verification failing | Active (Reopened) since 2026-06-25 |
| **T029 — Windows Defender/SmartScreen code-signing** | Procurement, not engineering | Active; certificate not procured |

**The critical distinction on the Windows side: packaging is no longer the blocker there.** The backslash path-handling defects that broke Windows builds were fixed 2026-08-10, and a build artifact was successfully produced 2026-08-12 — it installs on a Windows box and passes the same sanity checks run on Linux. Evan drew the line explicitly at the time: the engineering work for the Windows build is complete, but code-signing is a separate item not yet started, so he would not call the whole thing closed. Procuring a code-signing certificate and wiring signing into the release build step is "the only remaining item" before T029 clears — and, by extension, before T011 clears, since the checklist holds on this exact signing gap alongside the T005 image slim-down.

So the packaging half of the gating is **entirely Docker**, not Windows. The unsigned artifact triggers SmartScreen warnings and Defender flagging; site IT policies commonly block unsigned binaries outright, which would prevent installation on target deployment workstations without a manual security-policy override.

**Beyond the two formal gates,** the 2026-09-15 pre-release audit added the audit-log schema mismatch as a visible release blocker — Diana is keeping that gate red until schema and emitted records match — and kept the upstream high-DPI bug on the board. Evan's summary of the stack: "Release isn't opening with any of those unresolved." Alice closed the meeting with "No one closes those today."

---

### Bottom line

Roughly nine streams can run concurrently right now, and they cluster on the two people with unblocked capacity: Evan on Docker size/CVE and static linking, Charlie on the buffer-release refactor, OCR parallelization, and the license-safe parser search, with Bob on the audit-schema pass and loader leak patch. Four items wait on outsiders — two upstream PDF libraries (`pdf-lib-core` unresponsive, `pdfminer.six` #992 unmerged), a code-signing certificate stuck in procurement, and Tesseract model provenance. Release v1.0 opens on exactly two gates, and only one of them (Docker) is engineering-addressable; the other (Windows signing) will move when procurement does, no sooner.
