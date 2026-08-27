# Several streams remain blocked while others are only reopened. As of **2026-09-22**, what work can still advance in parallel, what cannot progress until an external dependency moves, and what release-checklist work is gated on packaging and Windows signing?

<!-- RESPONSE_START -->

## As of 2026-09-22 — CipherDoc parallel-work, blocked-work, and release-gate picture

### 1. Work that can still advance in parallel (active / reopened, not externally gated)

These streams have engineering work in flight right now and do not wait on anyone outside the team:

- **T008 / CIPH-18 — OCR fallback (WS-01)**: Active. Charlie integrated multiprocessing for page-level parallelism; Diana is wiring OCR results into the main scanner pipeline; confidence tuning continues as of September.
- **T006 / CIPH-16 — legacy JSON→YAML migration (WS-01)**: Active. Evan owns the converter for the three legacy MedFirst JSON policies required before production cutover. This is itself a release dependency on the T011 gate (CMT-2026-06-001).
- **T005 / CIPH-15 — Docker packaging (WS-03)**: Reopened/active. Evan has implemented multi-stage builds and swapped to Alpine, but as of August 12 the image still exceeds the ~450MB target and CVE verification is failing. Two thresholds are tracked separately: interim RC at 800MB once CVE-clean, GA at ~450MB (CMT-2026-06-002).
- **T014 / CIPH-24 — quarantine workflow (WS-04)**: Active. 90% confidence-threshold logic is being integrated with metadata injection for visual indicators.
- **T016 / CIPH-26 — audit trail logging (WS-04)**: Active/reopened. Bob refactored the loader for SHA-256 hashing and has another pass queued; Diana is verifying emitted records match the defined schema.
- **T030 / CIPH-40 — PDF parser license search (WS-04)**: Reopened/active. Charlie is searching for an Apache- or MIT-licensed alternative after the August 12 AGPL discovery. (Engineering can proceed, but see caveat below — it cannot *close* without Legal.)
- **T031 / CIPH-41 — large-file stream chunking (WS-05)**: Reopened/active. Charlie is refactoring stream buffer release logic after Bob found severe memory leaks on files over 2GB in long batch runs. Prioritized as a MedFirst pilot blocker (clinic workstation OOM on a 4.7GB PDF with 8GB RAM) and tied to the T011 release gate (CMT-2026-08-003).
- **T022 / CIPH-32 — storage quota management (WS-07)**: Reopened/active. Bob is refactoring the halt loop for a 10% buffer tolerance; ops capacity planning has reset the production baseline to 2GB free disk rather than 500MB (CMT-2026-09-003).
- **T029 / CIPH-39 — Windows compatibility engineering (WS-06)**: Active. Backslash path handling is fixed and a Windows build artifact was produced on August 12. Engineering work continues in parallel — the signing gap is a procurement dependency, not an engineering block.

**WS-02 (REST API / Batch CLI)** has *no* active work: T003, T004 and T012 are complete, and T009 (JWT auth) is deliberately deferred to v1.1 since v1.0.0 targets local single-machine usage. Note the standing contract constraint: MedFirst IT renewal requires REST authentication no later than 2026-03-31 (CMT-2026-07-001).

### 2. Work that cannot progress until an external dependency moves

**Genuinely external (outside the team's control):**

- **T007 / CIPH-17 — multi-page PDF offset mismatch (WS-01)**: Blocked on upstream `pdfminer.six` Issue/PR #992. Charlie monitored the repo through August and evaluated a local fork in late August, but the team rejected maintaining a parser fork. As of September 10 the PR remains unmerged and no safe local workaround exists. The maintainer's DM indicates #992 lands mid-October at the earliest, and any pre-normalization workaround would additionally require **written Legal sign-off** (CMT-2026-06-003).
- **T036 / CIPH-46 — High-DPI PDF rendering (WS-06)**: Blocked by upstream rendering-library scaling math; redaction coordinates drift 5–10 pixels on 4K displays at 200% scaling. Scope is now larger than the upstream fix alone — offline QA found 12% of the MedFirst pilot corpus fails due to nested Form XObjects (CMT-2026-09-001).
- **T029 signing certificate (WS-06/WS-03)**: Waiting on procurement of an Authenticode code-signing certificate from a CA. No certificate has been procured or configured in the Windows build pipeline.
- **T030 / CIPH-40 legal clearance (WS-04)**: A hard Legal P0 gate. The Legal memo states AGPL in the bundle triggers whole-bundle copyleft — the engineering library search alone **cannot** close T030 (CMT-2026-08-002).

**Blocked on internal dependencies rather than outside parties (still cannot advance on their own):**

- **T024 / CIPH-34 — Zero-Trust node sync (WS-07)**: Blocked. Nominal-latency handshake validation passed, but the September 22 high-latency simulation times out — the handshake never completes on slow links. The team explicitly declined a timeout-bump workaround ("bumping timeouts just hides it"), leaving the path dependent on the encryption workstream. Field data: the Singapore trial fails at 180ms RTT against the 5s prototype timeout; a 30s timeout budget is required, and nominal-latency pass must not be treated as sufficient for field sign-off (CMT-2026-09-004). Open triage question: whether 30s resolves it without redesigning the handshake exchange count, and whether the root cause is latency or encryption overhead on the wire path.
- **T019 / CIPH-29 — offline key rotation in air-gapped environments (WS-04)**: Blocked. Local key-rotation mockups exist, but rotation is impossible in a strictly air-gapped environment without a centralized authority. InfoSec approved a split master-key escrow (USB token + HQ HSM) and Bob is spiking the implementation, but it remains blocked until built (CMT-2026-08-001).
- **T037 / CIPH-47 — Async Batch API Scheduler (WS-05)**: Blocked. A concurrent manifest-write race reduces throughput ~10% and can corrupt JSON under load.

### 3. Release-checklist work gated on packaging and Windows signing

**T011 / CIPH-21 (Release v1 Gates, WS-03, owner Evan) is the gated item.** It is active but under a security-gate hold and **cannot close until both T005 (Docker size/CVE) and T029 (Windows code-signing certificate) are green.**

- **Hard deadline**: the release board set a **no-ship after 2026-10-15** if T005 and T029 are not green (CMT-2026-09-002).
- **Packaging side (T005)**: the image ballooned to 2.1GB after OCR dependencies were bundled; multi-stage builds and Alpine have not yet brought it under the ~450MB GA target, and CVE verification is still failing. CIPH-15 had originally been completed at ~800MB and was superseded/reopened on June 25.
- **Windows side (T029)**: packaging itself is no longer the blocker — path-handling defects were fixed 2026-08-10 and an artifact was produced 2026-08-12. The artifact is **unsigned**, triggering SmartScreen warnings and Defender flagging the binary as untrusted; site IT policies commonly block unsigned binaries outright, preventing installation on target deployment workstations without a manual security-policy override. Procuring the certificate and wiring signing into the release build step is the **sole remaining item** to clear the T029 gate, and by extension T011.
- **Also on the release checklist alongside packaging and signing**: the September 15 pre-release audit listed Docker slim/CVE work, Windows signing, **and audit-log schema alignment (T016)** as open blockers, with the upstream high-DPI bug (T036) also still on the board. Diana is holding the audit gate red until the CLI schema and emitted records match — Evan's summary was that release does not open with any of those unresolved.
- **Feeding into the same gate**: T006's legacy JSON→YAML migration is a release dependency on T011, and T031's large-file memory work is tied to the T011 gate as a MedFirst pilot blocker.

**Next update needed on WS-03**: Docker multi-stage build progress, final CVE scan results, and release gate clearance.

---

**Dataset records cited**: `work-states/index.md`; `work-states/WS-01-engine.md`; `work-states/WS-02-api.md`; `work-states/WS-03-ops.md`; `work-states/WS-04-policy.md`; `work-states/WS-05-performance.md`; `work-states/WS-06-platforms.md`; `work-states/WS-07-storage.md`; `work-states/comments/2026-09.md` (CMT-2026-09-004); `med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md` (SRC-MEET-10); `med-synth/communication/sources/fireflies/2026-09-22-Handshake-Protocol-Deep-Dive.md` (SRC-MEET-11); `med-synth/documentation/sources/2026-09-02-Windows-Compatibility-Audit-Report.md` (SRC-GDOC-39); plus referenced comment records CMT-2026-06-001, CMT-2026-06-002, CMT-2026-06-003, CMT-2026-07-001, CMT-2026-08-001, CMT-2026-08-002, CMT-2026-08-003, CMT-2026-09-001, CMT-2026-09-002, CMT-2026-09-003.
