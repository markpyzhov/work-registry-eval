# Write a concise cross-workstream management briefing as of **2026-09-22** covering at least three workstreams: at least two completed milestones that still hold, at least three items of work that were completed then reopened, at least two durable blockers, and the top risks that should escalate before ship. Do not present reopened work as done.

<!-- RESPONSE_START -->

## CipherDoc — Cross-Workstream Management Briefing (as of 2026-09-22)

Scope note: the dataset labels workstreams WS-01 (detection/redaction engine), WS-02 (CLI + REST API interfaces), WS-03 (packaging, security, release gates), WS-04 (batch processing and review). A fifth cluster — local/air-gapped deployment and performance — appears in the sources without an explicit WS label; it is reported separately below.

---

### 1. Completed milestones that still hold

| Milestone | Workstream | Evidence |
|---|---|---|
| **Batch CLI** completed 2026-06-12; completed binary packaged to the release artifact store 2026-07-15 | WS-02 | SRC-CU-CIPH-13, SRC-GDOC-02 |
| **REST API endpoints** completed 2026-06-17 (passed Diana's security check); Completed status reconfirmed 2026-07-15 for the release evidence pack | WS-02 | SRC-CU-CIPH-14 |
| **CLI–API parity** confirmed 2026-07-11, documented for the release pack 2026-07-20 | WS-02 | SRC-CU-CIPH-22 |
| **Security audit / vulnerability patches (T010)** completed 2026-07-10; post-patch CVE/CORS re-verification confirmed it held 2026-07-15 | WS-03 | SRC-CU-CIPH-20, SRC-GDOC-05, SRC-GDOC-09 |
| **Redaction-policy configuration (YAML, T006)** completed 2026-06-22 | WS-01 | SRC-CU-CIPH-16, SRC-GDOC-03 |
| **Conflict resolution (union rule)** completed 2026-06-16, archived as compliance evidence 2026-07-17, regression-checked against the HIPAA pattern update 2026-08-01 without breaking | WS-01 | SRC-CU-CIPH-27, SRC-GDOC-34 |
| **Batch fail-closed strategy** implemented 2026-06-15, QA-validated 2026-07-16 (no output on failure, temp files securely deleted) | WS-04 | SRC-CU-CIPH-25, SRC-SLACK-12 |
| **AES-256 at-rest encryption pipeline** signed off 2026-08-07 | Security/crypto | SRC-GDOC-35, SRC-SLACK-21 |
| **Redaction preview overlay (T023)** accepted 2026-08-08 | GUI/preview | SRC-CU-CIPH-33, SRC-GDOC-37 |
| **Multi-threaded batch path** completed 2026-08-07; **bare-metal benchmarks** published 2026-08-12; **statically linked runtime binary** verified 2026-08-05; **Electron GUI package test** passed 2026-08-18; **PDF-loader leak patch** completed/soak-tested 2026-08-23 | Local deployment / performance | SRC-CU-CIPH-36, -38, -28, SRC-GDOC-48, SRC-CU-CIPH-43 |

Two carry explicit caveats that do **not** reverse the completion but limit what can be claimed: the AES-256 sign-off flagged PBKDF2-derived keys on non-TPM hardware as a pre-v1.0 hardening follow-up (Argon2id), and the HIPAA pattern-merge report states it is **not** a HIPAA compliance certification (SRC-GDOC-35, SRC-GDOC-34).

---

### 2. Work completed then reopened — **not done**

1. **Docker packaging (T005 / CIPH-15) — Active (Reopened), WS-03.** Initial Dockerfile completed 2026-06-16; reopened 2026-06-25 when the built image measured 2.1GB. Multi-stage build, Alpine base swap, and removal of unused OCR/runtime packages have all landed, but the 2026-08-12 verification found the image **still over the ~450MB target and CVE verification still failing**. Both acceptance criteria remain unmet. (SRC-CU-CIPH-15, SRC-SLACK-06, SRC-GDOC-05/06)
2. **Large-file stream chunking (T031 / CIPH-41) — Active (Reopened).** Merged to mainline and called done 2026-08-16; reopened 2026-08-18 after 2GB+ files kept leaking memory and QA reproduced processes being killed. Charlie's per-chunk buffer-release refactor shows flat memory on a 2.3GB local sample but, per the 2026-08-23 design review, is **not yet validated against the full large-file test corpus**. (SRC-CU-CIPH-41, SRC-SLACK-43/44, SRC-GDOC-42)
3. **Third-party license audit (CIPH-40) — Active (Reopened), high priority.** The Ghostscript/AGPLv3 finding was remediated by swapping the PDF parser (2026-08-11) and marked Completed; reopened 2026-08-12 when the replacement parser proved **also AGPL-licensed**. No Apache/MIT replacement confirmed as of the 2026-08-21 report. A secondary item — unverified provenance of the Tesseract `eng.traineddata` corpus — is still open. The audit report carries an explicit warning not to report license compliance as resolved externally. (SRC-CU-CIPH-40, SRC-GDOC-41/24, SRC-SLACK-40)
4. **Storage-quota halt (CIPH-32) — Active (Reopened), WS-04.** Verified and "called done" 2026-08-06; reopened 2026-09-15 because the flat 500MB hard halt tripped production-like batches before useful work. A 10% buffer-tolerance refactor landed 2026-09-18 and Evan re-tested with no premature halts — but the task record still stands at **Active (Reopened)**; no formal re-closure is recorded. (SRC-CU-CIPH-32, SRC-SLACK-23)

---

### 3. Durable blockers

- **Upstream `pdfminer.six` whitespace bug — CIPH-17 (WS-01), blocked since 2026-06-26.** PR #992 still unmerged as of the 2026-09-10 check. Forking was formally evaluated and rejected as unmaintainable; **no local workaround adopted**, so the coordinate/offset drift stays open indefinitely. Alice flagged it on 2026-09-10 as "a real risk for the v1.0 timeline." (SRC-CU-CIPH-17, SRC-SLACK-07)
- **Upstream `pdf-lib-core` high-DPI scaling — CIPH-46, Blocked 2026-09-10.** The rotation fix broke on nested Form XObjects; root cause sits in the vendor's C++ core, the upstream issue is unanswered, and PDF-flattening as a workaround would inflate file size and risk losing text layers. Open decision: ship with a documented limitation or replace the rendering library. (SRC-CU-CIPH-46, SRC-SLACK-58, SRC-GDOC-49)
- **Offline auth key rotation — CIPH-29, Blocked since 2026-08-05, high priority.** The chosen rotation design assumes a network connection; rotation cannot complete in an air-gapped install and no fix exists. (SRC-CU-CIPH-29, SRC-MEET-07)
- **Multi-site node-sync handshake — CIPH-34, Blocked, reaffirmed 2026-09-22.** Nominal latency passes; the handshake never completes on a simulated high-latency link. The team explicitly rejected a timeout bump as masking the defect and will revisit only when the encryption/handshake design moves. (SRC-CU-CIPH-34, SRC-MEET-11)
- **Async batch scheduler — CIPH-47, Blocked since 2026-08-25.** A confirmed concurrent manifest-write race corrupts the shared results JSON and measurably cuts batch throughput ~10% versus the expected async speedup; this blocks further scheduler rollout. (SRC-CU-CIPH-47, SRC-GDOC-50)
- **Windows code-signing certificate (T029), open since 2026-09-02.** Packaging is fixed and a Windows artifact builds, but the binary is unsigned; Defender/SmartScreen flag it and site IT policies commonly block unsigned installs outright. Not solvable in engineering — it needs certificate procurement. (SRC-GDOC-39, SRC-SLACK-37)

---

### 4. Top risks to escalate before ship

1. **The v1.0 release gate cannot close.** CIPH-21 remains Active with Diana's security-gate hold on **both** T005 (Docker size/CVE) and T029 (Windows signing). At the 2026-09-15 pre-release audit all parties agreed nothing closes until those clear. Escalate as the single critical-path item. (SRC-CU-CIPH-21, SRC-MEET-10)
2. **Audit-trail gate is red — compliance-facing.** On 2026-09-18 Diana's verification found CLI-emitted audit records inconsistent with the defined JSON schema. This undercuts the audit trail as release evidence for a redaction product sold on auditability. CIPH-26 is Active with another Bob pass queued. (SRC-CU-CIPH-26, SRC-MEET-10)
3. **Legal/distribution exposure from AGPL dependencies.** An AGPL parser in the shipped set is described as a dealbreaker for the current distribution model, with no replacement identified and OCR training-data provenance unverified. Highest-severity non-engineering risk; needs a legal decision path, not just an engineering search. (SRC-GDOC-41, SRC-SLACK-40)
4. **Two upstream blockers with no owner-controlled remedy** (pdfminer.six #992, pdf-lib-core). Both have been open for weeks with fork/workaround options explicitly rejected. Force an explicit ship-with-known-issue decision now rather than carrying them into the release window.
5. **Large-file reliability is unproven at scale.** The 2GB+ leak fix has not been validated end-to-end; QA previously saw processes killed on large inputs. Do not treat chunking as delivered until the full-corpus stress run passes.
6. **Concurrency throughput regression.** The ~10% async-path regression from the manifest-write race sits directly against published performance claims (benchmarks were published 2026-08-12 off the multi-threading baseline).
7. **Over-claiming risk on air-gap and compliance.** The offline batch sign-off is explicitly **preliminary** — not a compliance certification, no side-channel or regulatory attestation — and logs a ~45-second remote licence-check hang at startup. The offline harness is also still manual, not wired into CI. External messaging should not describe air-gapped operation as certified. (SRC-GDOC-47, SRC-GDOC-46, SRC-CU-CIPH-37)
8. **Scope assumption to confirm:** REST API authentication (CIPH-19) is Deferred to v1.1 on the basis that v1.0 is local-network-only. If any pilot deployment is not local-network-only, this deferral is invalid. (SRC-CU-CIPH-19)

---

**Bottom line:** the engine, interface, and crypto foundations are genuinely done and holding. Release is gated by two unmet packaging/signing criteria, a red audit-log gate, and an unresolved AGPL license exposure — none of which are close to closing. Four items that were previously reported as complete (Docker, chunking, license audit, quota halt) are reopened and should not be counted as delivered; six blockers, four of them outside the team's direct control, remain live.
