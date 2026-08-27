# Write a concise cross-workstream management briefing as of **2026-09-22** covering at least three workstreams: at least two completed milestones that still hold, at least three items of work that were completed then reopened, at least two durable blockers, and the top risks that should escalate before ship. Do not present reopened work as done.

<!-- RESPONSE_START -->

## Cross-Workstream Management Briefing — CipherDoc, as of 2026-09-22

All seven workstreams (WS-01 … WS-07) are `in_progress`. Nothing has shipped; v1.0 sits behind a security-gate hold.

---

### 1. Completed milestones that still hold

These are signed-off and have not been reopened:

- **WS-03 / T010 (CIPH-20) — Security audit and vulnerability scans.** The medium-severity CORS `*` origin finding from the July 6 scan was patched by restricting to configured `ALLOWED_ORIGINS`; July 15 re-scans confirmed the patch holds. Supplemented by the RedByte third-party pen-test attestation letter dated 2026-07-11 in the release evidence pack (CMT-2026-07-002).
- **WS-04 / T015 (CIPH-25) — Batch fail-closed strategy.** Atomic rename guarantees no partial output; Diana QA-validated on July 16 that no output file is written on failure and temp files are securely deleted. This milestone is load-bearing — the AES-256 crypto sign-off was explicitly withheld until it was confirmed complete.
- **WS-07 / T021 (CIPH-31) — AES-256 at-rest encryption.** Zero-leakage confirmed in cold-start audit; AES-256-GCM applied to every redacted output, keys confined to process memory, pipeline refuses to write plaintext if key material is unavailable. (Argon2id passphrase hardening on non-TPM hardware is tracked separately as a pre-v1.0 item, not a sign-off condition.)
- **WS-05 / T028 (CIPH-38) — Bare-metal benchmarks:** 500 pages/minute on standard enterprise hardware. **WS-05 / T026:** process pool scales linearly to 16 cores.
- **WS-02 / T003, T004, T012** — Batch CLI, REST API, and CLI-API parity (verified after the July 9 fix). WS-02 has no active work.
- **WS-01 / T001, T002, T006** — core parser, regex detection (100% on synthetic CC/SSN cases), YAML policy loader.

---

### 2. Work completed then reopened — **not done, do not report as shipped**

Five items were closed or believed landed, then reopened:

| Item | Workstream | What happened |
|---|---|---|
| **T005 / CIPH-15 — Docker packaging** | WS-03 | Initially completed at ~800MB, then **superseded and reopened June 25** when OCR bundling pushed the image to 2.1GB. Multi-stage builds and an Alpine swap were implemented, but as of Aug 12 the image still exceeds the ~450MB target and **CVE verification is failing**. Dual gates now apply (CMT-2026-06-002): interim RC at 800MB once CVE-clean, GA at ~450MB. |
| **T016 / CIPH-26 — Compliance audit-trail logs** | WS-04 | **Active/reopened.** SHA-256 hashing landed and CLI integration went in Sept 10, but Diana's Sept 18 verification found CLI-emitted records inconsistent with the defined schema. The audit gate is **red**. |
| **T030 / CIPH-40 — License compliance review** | WS-04 | **Reopened Aug 12** after AGPL was discovered in a candidate replacement PDF parser. Charlie is hunting an Apache/MIT alternative. |
| **T031 / CIPH-41 — Large-file stream chunking** | WS-05 | **Reopened.** Initial chunking landed, then Bob found severe memory leaks on files >2GB during long batch runs. Charlie is refactoring stream-buffer release logic. Note: this is distinct from T033 (PDF-loader leak), which *is* patched and stable after 10,000 documents. |
| **T022 / CIPH-32 — Storage quota management** | WS-07 | **Reopened.** Monitor halts processing too aggressively at ~500MB free; Bob is adding a 10% buffer tolerance. Baseline was corrected Sept 15 (CMT-2026-09-003) from 500MB to **2GB free disk**, requiring re-verification in clinic VMs. |

---

### 3. Durable blockers (open, no owner-side workaround)

- **T007 / CIPH-17 — multi-page offset mismatch (WS-01, P0).** Blocked on upstream `pdfminer.six` #992. Maintaining a local parser fork was evaluated and **rejected**; as of Sept 10 the PR is unmerged and no safe workaround exists. Maintainer indicates **mid-October at the earliest**, and any pre-normalization workaround additionally requires **written Legal sign-off** (CMT-2026-06-003).
- **T019 / CIPH-29 — offline mode authentication (WS-04, P0).** Key rotation is impossible in a strictly air-gapped environment without a centralized authority; this is a design limitation, not a mock bug. InfoSec approved a split master-key escrow (USB token + HQ HSM); Bob is spiking it, and it **remains blocked until built** (CMT-2026-08-001).
- **T036 / CIPH-46 — high-DPI rendering (WS-06).** Blocked on upstream rendering-library scaling math; coordinates drift 5–10px on 4K at 200% scaling. **Scope has widened**: 12% of the MedFirst pilot corpus fails on nested Form XObjects, which the upstream fix alone may not cover (CMT-2026-09-001).
- **T024 / CIPH-34 — zero-trust node sync (WS-07).** Nominal-latency handshake passed, but the Sept 22 high-latency simulation times out. Singapore field trial fails at 180ms RTT against the 5s prototype timeout; a **30s budget** is needed (CMT-2026-09-004). The team declined a timeout-bump workaround pending encryption-path stabilization.
- **T037 / CIPH-47 — async batch scheduler (WS-05).** Concurrent manifest-write race cuts throughput ~10% and **can corrupt JSON under load**.

Also open but not engineering-blocked: **T029 (WS-06)** — Windows path handling is fixed and a build artifact was produced Aug 12, but the binary is unsigned; SmartScreen/Defender flag it. This is a **procurement dependency** (no code-signing certificate has been obtained), which is exactly why it is a schedule risk rather than a coding task.

---

### 4. Top risks to escalate before ship

1. **Hard no-ship date of 2026-10-15.** The release board ruled (CMT-2026-09-002) that if **T005 and T029 are not green**, the release does not go — explicitly a hard deadline, not advisory. Both are currently red, and one of them (the code-signing certificate) cannot be solved by engineering effort. **This is the single highest escalation item.**
2. **Three stacked P0 gates on T011.** The Sept 15 pre-release audit confirmed Docker slim/CVE, Windows signing, and audit-log schema alignment all remain open, with Alice stating none would be closed. Any one of them keeps the release shut; they are not being worked serially against a deadline that is now ~3 weeks out.
3. **AGPL exposure is a Legal gate, not an engineering one.** The Legal memo (CMT-2026-08-002) states AGPL in the bundle triggers **whole-bundle copyleft**, and that the engineering library search alone **cannot close T030**. Escalate to Legal for a decision path, not just to Charlie for a library swap.
4. **The audit trail is release *evidence*, and it is currently unreliable.** Diana will keep the gate red until emitted records match schema. A compliance product shipping with an inconsistent audit trail is a regulatory exposure, not just a bug.
5. **MedFirst pilot is exposed on two fronts.** Clinic workstations OOM on a 4.7GB PDF with 8GB RAM (T031, tied to the T011 gate per CMT-2026-08-003), and 12% of the pilot corpus mis-aligns on Form XObjects (T036). Pilot credibility is at risk independent of the GA date.
6. **Two upstream dependencies with no owned resolution.** T007 (`pdfminer.six` #992, mid-October at best plus a Legal sign-off) and T036 (rendering library) are both outside team control; a fork was already considered and rejected for T007. Escalate a contingency decision now rather than at the deadline.
7. **Secondary contractual exposure:** REST API auth (T009) was deferred to v1.1, but MedFirst's enterprise renewal contractually requires it (CMT-2026-07-001) — worth confirming this is still consciously accepted.

---

**Bottom line:** the foundations hold — engine, CLI/API, encryption, fail-closed, security scanning. What is at risk is the *release*, and the two items gating it against a hard 2026-10-15 date are a reopened Docker/CVE task and a certificate that has to be procured, not built. Reopened work (T005, T016, T030, T031, T022) should not be counted as delivered in any status roll-up.

*Sources: work-states/index.md; WS-01 through WS-07 work-state records; comments CMT-2026-06-002/003, CMT-2026-07-001/002, CMT-2026-08-001/002/003, CMT-2026-09-001/002/003/004; SRC-MEET-10 (2026-09-15 Pre-Release Audit), SRC-MEET-07, SRC-SLACK-37, SRC-SLACK-40, SRC-SLACK-43, SRC-SLACK-12, SRC-CU-CIPH-21, SRC-CU-CIPH-26, SRC-CU-CIPH-37, SRC-GDOC-35, SRC-GDOC-39, SRC-GDOC-47.*
