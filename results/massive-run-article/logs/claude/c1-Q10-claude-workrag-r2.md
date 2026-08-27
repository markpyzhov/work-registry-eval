# Write a concise cross-workstream management briefing as of **2026-09-22** covering at least three workstreams: at least two completed milestones that still hold, at least three items of work that were completed then reopened, at least two durable blockers, and the top risks that should escalate before ship. Do not present reopened work as done.

<!-- RESPONSE_START -->

## Cross-Workstream Management Briefing — CipherDoc, as of 2026-09-22

All seven workstreams (WS-01 … WS-07) are `in_progress`. Nothing is closed out; v1.0.0 is gated.

### 1. Completed milestones that still hold

| Milestone | WS | Evidence |
|---|---|---|
| **T015 / CIPH-25 — Batch fail-closed strategy** | WS-04 | Atomic-rename design guarantees no partial output; Diana QA-validated on 2026-07-16 that no output file is written on failure and temp files are securely deleted. It has since been *depended on* by the encryption work rather than reopened. `(WS-04 S3, S8)` |
| **T021 / CIPH-31 — AES-256 at-rest encryption** | WS-07 | Crypto sign-off 2026-08-07, explicitly conditioned on T015 being complete; AES-256-GCM on every output, keys confined to process memory, pipeline refuses to write plaintext. Zero-leakage confirmed in cold-start audit. `(WS-07 S2; SRC-GDOC-35; SRC-CU-CIPH-31)` |
| **T010 / CIPH-20 — Security audit & vulnerability scans** | WS-03 | Medium-severity CORS `*` origin finding patched to configured `ALLOWED_ORIGINS`; re-scans 2026-07-15 confirmed the patch holds. Supplemented by the RedByte pen-test attestation letter (2026-07-11) in the release evidence pack. `(WS-03 S4, S5, S6; CMT-2026-07-002)` |
| *(also holding)* | WS-05 | T026 process pool scales linearly to 16 cores; T028 benchmarks confirm 500 pages/min; T033 PDF-loader leak patched, memory stable over 10,000 documents. `(WS-05 S2, S5, S9)` |

One caveat on a frequently-cited "done": **T027 / CIPH-37 air-gapped batch run** completed (1,000 files, network-denied VM), but Diana's sign-off is recorded as **preliminary only — explicitly not a compliance certification**, and it logged a 45-second remote licence-check hang as a known open issue. Do not carry it into the release pack as compliance evidence. `(SRC-GDOC-47; SRC-CU-CIPH-37)`

### 2. Completed-then-reopened — currently NOT done

These were all marked or believed complete at some point and have since been reopened. None should be reported as shipped.

1. **T005 / CIPH-15 — Docker packaging (WS-03).** Initially completed at ~800MB, then superseded and reopened 2026-06-25 when OCR bundling pushed the image to 2.1GB. Multi-stage builds and an Alpine base landed, but as of 2026-08-12 the image still exceeds the ~450MB GA target and **CVE verification is failing**. Note the dual gate from the CISO review: interim RC may ship at 800MB *once CVE-clean*; GA remains ~450MB. `(WS-03 S1, S2; CMT-2026-06-002)`
2. **T030 / CIPH-40 — License compliance review (WS-04).** Reopened 2026-08-12 after AGPL was discovered in a candidate replacement PDF parser. Charlie is hunting an Apache/MIT alternative. `(WS-04 S15, S16)`
3. **T016 / CIPH-26 — Compliance audit-trail logging (WS-04).** Active/reopened. Bob refactored the loader for SHA-256 hashing; Diana is still verifying that emitted records match the defined schema. The 2026-09-15 pre-release audit flagged the CLI-schema vs emitted-record mismatch as a **release hold**. `(WS-04 S5, S9)`
4. **T031 / CIPH-41 — Large-file stream chunking (WS-05).** Initial chunking landed, then reopened when Bob found severe memory leaks on files >2GB during long batch runs. Charlie is refactoring stream-buffer release logic. `(WS-05 S6, S7)`
5. **T022 / CIPH-32 — Storage quota management (WS-07).** Reopened: the monitor halts processing too aggressively at ~500MB free. Bob is refactoring for a 10% buffer tolerance — and the halt thresholds must be **retargeted to a 2GB production baseline**, not 500MB. `(WS-07 S4; CMT-2026-09-003)`

Related correction worth knowing: an early **CLI-API parity claim (T012) was disproved** on 2026-07-09 when the CLI was found to ignore `custom_regex` flags; PR #52 fixed it and 2026-07-11 tests confirmed unified config loading. That one *is* now genuinely closed. `(WS-02 S7, S9)`

### 3. Durable blockers

- **T007 / CIPH-17 — Multi-page PDF offset mismatch (WS-01, P0).** Blocked on upstream `pdfminer.six` #992 since June. Maintainer DM: earliest realistic merge is **mid-October**. The team rejected maintaining a parser fork; as of 2026-09-10 no safe local workaround exists, and any pre-normalization workaround additionally requires **written Legal sign-off**. `(WS-01 S6, S7; CMT-2026-06-003)`
- **T019 / CIPH-29 — Offline-mode authentication (WS-04, P0).** Key rotation is impossible in a strictly air-gapped environment without a central authority. InfoSec has approved a split master-key escrow design (USB token at clinic + HQ HSM) and Bob is spiking it, but it **remains blocked until built**. `(WS-04 S11, S12; CMT-2026-08-001)`
- **T024 / CIPH-34 — Zero-trust node sync (WS-07).** Nominal-latency handshake validation passed, but high-latency simulation on 2026-09-22 times out entirely. Singapore field trial fails at 180ms RTT against the 5s prototype timeout; a **30s timeout budget** is required. Team declined the timeout-bump workaround pending encryption-path stabilization. `(WS-07 S6, S7; CMT-2026-09-004)`
- **T036 / CIPH-46 — High-DPI rendering (WS-06).** Blocked on upstream rendering-library scaling math: redaction coordinates drift 5–10 px on 4K displays at 200% scaling. Worse, offline QA found **12% of the MedFirst pilot corpus fails on nested Form XObjects** — a scope beyond the upstream 4K fix, so the upstream merge alone will not clear it. `(WS-06 S14; CMT-2026-09-001)`
- **T037 / CIPH-47 — Async batch scheduler (WS-05).** Blocked on a concurrent manifest-write race that cuts throughput ~10% and can **corrupt JSON under load**. `(WS-05 S11, S12)`

### 4. Top risks to escalate before ship

1. **Hard no-ship deadline, 2026-10-15.** The release board set a firm (not advisory) no-ship if T005 (Docker size/CVE) and T029 (Windows code-signing) are not green. T011 cannot close until both are. That is roughly three weeks out with T005 still failing CVE verification. **Escalate first.** `(CMT-2026-09-002; WS-03 S9, S10)`
2. **Windows code-signing is a procurement, not engineering, dependency.** Path/backslash handling is fixed, but Defender SmartScreen flags unsigned binaries until an Authenticode certificate is purchased. Engineering cannot unblock this — it needs a purchasing decision now, since it is one of the two gates on the 10-15 deadline. `(WS-06 S8, S9)`
3. **AGPL exposure is a Legal P0, not a library-swap task.** The Legal memo states AGPL in the bundle triggers **whole-bundle copyleft exposure** for the distribution model. Charlie's search for an Apache/MIT parser is necessary but not sufficient — T030 cannot close without Legal. `(CMT-2026-08-002)`
4. **Two P0 items sit behind third parties with October-or-later ETAs.** T007 depends on an upstream merge no earlier than mid-October (plus Legal sign-off for any workaround), and T036's blocker is only partly upstream. Both are outside the team's control and both bracket the ship date.
5. **MedFirst pilot exposure is compounding.** Four separate pilot-driven risks are open: the 4.7GB-PDF OOM on 8GB clinic workstations (T031, explicitly tied to the T011 gate), the 12% Form XObject rendering failure (T036), three legacy JSON policies requiring auto-migration before cutover (Evan owns the JSON→YAML converter, a release dependency on T006/T011), and a contractual REST-API-auth requirement that the record dates 2026-03-31 despite JWT being deferred to v1.1. That last item's date reads as inconsistent with a 2026-09-22 as-of and should be re-confirmed with MedFirst IT. `(CMT-2026-08-003; CMT-2026-09-001; CMT-2026-06-001; CMT-2026-07-001)`
6. **Audit-log schema mismatch is an unresolved release hold** in its own right (T016), independent of packaging — the pre-release audit lists it alongside Docker/CVE and Windows signing. `(WS-04 S5, S9; WS-03 S9)`

**Deferred / superseded, for completeness:** T009 JWT auth deferred to v1.1 (v1.0.0 targets local single-machine use) — but see the MedFirst contractual exception above. T039 standalone a11y audit superseded by the Preview UI overhaul (CIPH-33), which natively covers high-contrast and keyboard navigation. `(WS-02 S5; WS-04 S22)`

Sources: `work-states/index.md`, `WS-01-engine.md`, `WS-02-api.md`, `WS-03-ops.md`, `WS-04-policy.md`, `WS-05-performance.md`, `WS-06-platforms.md`, `WS-07-storage.md`, and `work-states/comments/2026-06.md` … `2026-09.md`, with cited underlying ClickUp/Slack/Fireflies/GDoc records.
