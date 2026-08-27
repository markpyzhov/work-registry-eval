# Several streams remain blocked while others are only reopened. As of **2026-09-22**, what work can still advance in parallel, what cannot progress until an external dependency moves, and what release-checklist work is gated on packaging and Windows signing?

<!-- RESPONSE_START -->

## CipherDoc status as of 2026-09-22

All seven work states (WS-01 through WS-07) carry a **Last Updated** of 2026-09-22, and the Work State Index is stamped `2026-09-22T12:00:00Z`, so the picture below is current rather than inferred.

---

### 1. Work that can still advance in parallel

These items are active or reopened and are not waiting on anyone outside the team. They can all be pushed simultaneously by different owners:

| Item | Stream | Owner | What is moving |
|---|---|---|---|
| **T005 / CIPH-15** — Docker packaging | WS-03 | Evan | Reopened/active. Image ballooned to 2.1GB after OCR deps were bundled; multi-stage builds and an Alpine swap are in. As of Aug 12 it still exceeds the ~450MB target and CVE verification is failing. Two thresholds are tracked separately: interim RC at 800MB once CVE-clean, GA at ~450MB (CMT-2026-06-002). |
| **T008 / CIPH-18** — OCR fallback | WS-01 | Charlie / Diana | Active. Multiprocessing for page-level parallelism integrated; Diana is wiring OCR results into the main scanner pipeline, confidence tuning continues through September. |
| **T014 / CIPH-24** — Quarantine workflow | WS-04 | Alice / Diana | Active. 90% confidence-threshold logic being integrated with metadata injection for visual indicators. |
| **T016 / CIPH-26** — Audit-trail logging | WS-04 | Bob / Diana | Active/reopened. Loader refactored for SHA-256 hashing; Diana verifying emitted records against the defined schema. Bob has another pass queued. |
| **T022 / CIPH-32** — Storage quota monitor | WS-07 | Bob | Reopened/active. Refactoring the halt loop for 10% buffer tolerance. Note the production baseline was reset to **2GB** free disk, not 500MB (CMT-2026-09-003). |
| **T029 / CIPH-39** — Windows compatibility | WS-06 | Diana / Evan | Active. Backslash path handling fixed and a Windows build artifact produced by Aug 12. Engineering work continues in parallel — the remaining gap is procurement, not code. |
| **T030 / CIPH-40** — License-clean parser search | WS-04 | Charlie | Reopened/active after the Aug 12 AGPL discovery; searching for an Apache/MIT alternative. Engineering can proceed, but see the caveat below. |
| **T031 / CIPH-41** — Large-file chunking | WS-05 | Charlie / Bob | Reopened/active. Chunking landed, then severe memory leaks appeared on files >2GB during long batch runs; Charlie is refactoring stream-buffer release logic. Tied to the MedFirst pilot OOM (4.7GB PDF on an 8GB clinic workstation) and to the T011 gate. |
| **T006 / CIPH-16** — Legacy JSON→YAML migration | WS-01 | Evan | The YAML policy loader is merged; Evan owns the converter for the three legacy MedFirst JSON policies required before production cutover. |

Nothing in this set blocks another item in this set, so they are genuinely parallelizable across Charlie, Bob, Diana, Evan and Alice.

---

### 2. Work that cannot progress until an external dependency moves

Five items are hard-blocked. In each case the unblocking event is outside the team's direct control:

- **T007 / CIPH-17 — Offset mismatch (WS-01, Charlie).** Blocked on upstream `pdfminer.six` Issue/PR #992. Charlie monitored the repo through August and evaluated a local fork in late August, but the team **rejected maintaining a parser fork**. As of September 10 the PR is still unmerged and no safe local workaround exists. The maintainer indicated #992 lands **mid-October at the earliest**, and any pre-normalization workaround would additionally require **written Legal sign-off** on top of the upstream merge (CMT-2026-06-003).

- **T036 / CIPH-46 — High-DPI PDF rendering (WS-06, Diana / Evan).** Blocked by upstream rendering-library scaling math; redaction coordinates drift 5–10 pixels on 4K displays at 200% scaling. Worse, offline QA found **12% of the MedFirst pilot corpus** fails because of nested Form XObjects — a scope beyond the upstream 4K scaling fix alone (CMT-2026-09-001). Even when upstream lands, an engine-side workaround may still be needed; that possibility sits in Needs Manual Triage.

- **T019 / CIPH-29 — Key rotation / escrow (WS-04, Bob).** Blocked. Local key-rotation mockups exist, but rotation is impossible in a strictly air-gapped environment without a centralized authority. InfoSec approved a split master-key escrow design (USB token + HQ HSM) and Bob is spiking it, but the item **remains blocked until that is actually built** (CMT-2026-08-001).

- **T024 / CIPH-34 — Zero-trust node sync handshake (WS-07, Bob).** Blocked. Nominal-latency validation passed on a single LAN segment, but the September 22 high-latency simulation times out — the handshake never completes on slow links. The team explicitly **declined a timeout-bump workaround**, pending encryption-path stabilization, on the grounds that bumping timeouts only hides the failure. The Singapore field trial fails at 180ms RTT against the 5s prototype timeout; a **30s timeout budget** is required for high-latency links, and a nominal-latency pass must not be treated as sufficient for field sign-off (CMT-2026-09-004). Diana is holding the high-latency repro in place for re-check when the crypto path moves.

- **T037 / CIPH-47 — Async batch processing (WS-05, Bob).** Blocked on a concurrent manifest-write race: workers finish out of order and interleaved appends can corrupt the JSON manifest. Concurrency testing on August 25 confirmed the race is real, measurably cutting batch throughput ~10% versus the expected async speedup. This blocks further rollout of the async scheduler; the fix depends on how the T026 worker-pool result-writing is serialized.

**A partial case worth separating out:** **T030 (license search)** is listed as active/reopened, and Charlie's library search can proceed — but the Legal memo makes clear that AGPL in the bundle triggers whole-bundle copyleft, so this is a **hard Legal P0 gate: engineering library search alone cannot close T030** (CMT-2026-08-002). Similarly, **T029** is engineering-active but its gate closure is a procurement dependency.

**Deferred rather than blocked:** T009 / CIPH-19 (REST API auth) was deferred to v1.1 / past the v1.0.0 general launch — but MedFirst IT renewal requires REST authentication **no later than 2026-03-31** (CMT-2026-07-001), so this is a dated commitment, not an indefinite deferral.

---

### 3. Release-checklist work gated on packaging and Windows signing

**T011 / CIPH-21 (Release v1 gates, WS-03, Evan)** is the release checklist, and it is active under a **security-gate hold**. It **cannot close until both T005 (Docker size/CVE) and T029 (Windows code-signing certificate) are green.**

The September 15 pre-release audit enumerated the open blockers on the board as:
1. **Docker slim-down / CVE work** (T005) — still open;
2. **Windows signing** (T029) — still open;
3. **Audit-log schema alignment** (T016) — Diana is holding the audit-log gate red until the CLI schema and the emitted records match, on the grounds that a mismatch undercuts the audit trail as release evidence;
4. **Upstream high-DPI rendering** (T036) — still blocked upstream.

Alice's direction in that meeting was explicit: security-gate work stays open and nothing gets closed — "Release isn't opening with any of those unresolved," in Evan's words.

**On the Windows signing gap specifically:** packaging is *not* the blocker. The backslash path-handling defects that previously broke Windows builds were fixed on 2026-08-10, and a Windows build artifact was successfully produced by 2026-08-12. The remaining problem is that the produced artifact is **unsigned**, which triggers a SmartScreen warning and causes Defender to flag the binary as untrusted. Site IT policies commonly block execution of unsigned/SmartScreen-flagged binaries outright, which would prevent installation on target deployment workstations without a manual security-policy override. Root cause: no code-signing certificate has been procured or configured in the Windows build pipeline. Procuring an Authenticode certificate and wiring signing into the release build step is the **sole remaining item** before T029 clears — and by extension before T011 clears, alongside the T005 image slim-down. **Budget and procurement timeline for the certificate is sitting in WS-06's Needs Manual Triage**, unresolved.

**Hard deadline:** the release board set a **hard no-ship after 2026-10-15** if T005 and T029 are not green (CMT-2026-09-002). That leaves roughly three weeks from the as-of date, against a Docker image that as of August 12 still exceeded target with CVE verification failing, and a certificate that has not been procured.

Note the awkward interaction: T007's upstream fix is expected **mid-October at the earliest**, which lands essentially on top of the October 15 no-ship deadline.

**Next update needed for WS-03:** Docker multi-stage build progress, final CVE scan results, and release gate clearance.

---

### Records cited

`work-states/index.md`; `work-states/WS-01-engine.md`; `work-states/WS-03-ops.md`; `work-states/WS-04-policy.md`; `work-states/WS-05-performance.md`; `work-states/WS-06-platforms.md`; `work-states/WS-07-storage.md`; `work-states/comments/2026-09.md`; `med-synth/documentation/sources/2026-09-02-Windows-Compatibility-Audit-Report.md` (SRC-GDOC-39); `med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md` (SRC-MEET-10); `med-synth/communication/sources/fireflies/2026-09-22-Handshake-Protocol-Deep-Dive.md` (SRC-MEET-11); `med-synth/communication/sources/slack/2026-08-08-node-sync-handshake-validation.md` (SRC-SLACK-27); `med-synth/documentation/sources/2026-09-04-Async-Batch-Processing-Queue-Review.md` (SRC-GDOC-50); `med-synth/tasks/CIPH-34-Zero-Trust-Node-Sync.md` (SRC-CU-CIPH-34); `med-synth/documentation/sources/2026-08-15-Zero-Trust-Node-Sync-Review.md` (SRC-GDOC-18). Comment records: CMT-2026-06-001, CMT-2026-06-002, CMT-2026-06-003, CMT-2026-07-001, CMT-2026-08-001, CMT-2026-08-002, CMT-2026-08-003, CMT-2026-09-001, CMT-2026-09-002, CMT-2026-09-003, CMT-2026-09-004.
