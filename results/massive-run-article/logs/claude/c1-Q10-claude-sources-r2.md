# Write a concise cross-workstream management briefing as of **2026-09-22** covering at least three workstreams: at least two completed milestones that still hold, at least three items of work that were completed then reopened, at least two durable blockers, and the top risks that should escalate before ship. Do not present reopened work as done.

<!-- RESPONSE_START -->

## CipherDoc — Cross-Workstream Management Briefing
**As of 2026-09-22.** Sourced only from the `tl-v1` dataset `d13efb7c8a9a11f197db2303d7337e37` (path: `sources`).

---

### 1. Bottom line

Four workstreams are in play — WS-01 (core redaction engine & detection), WS-02 (interfaces: batch CLI / REST API / async batch), WS-03 (packaging & release readiness), WS-04 (compliance, policy & audit) — plus a local/air-gapped deployment track. Foundation work is genuinely done and has survived re-verification. **The release gate itself (CIPH-21 / T011) is not closeable**: three items that were once "called done" are back open, five items are hard-blocked (two of them on upstream code we have chosen not to own), and Diana's security-gate hold is standing. Ship date is at risk on packaging, signing, licensing and audit evidence — not on core engine capability.

---

### 2. Completed milestones that still hold

These are Completed **and** have been re-checked after later work landed on top of them:

| Milestone | Workstream | Evidence it still holds |
|---|---|---|
| **Overlapping-policy conflict resolution (union rule)** — CIPH-27, Completed 2026-06-16 | WS-01 | Recorded in the compliance pack 2026-07-17 as durable evidence; **regression-checked 2026-08-01** against the new HIPAA pattern updates and the union merge was confirmed unbroken (SRC-CU-CIPH-27). |
| **Security audit & vulnerability patches** — CIPH-20 / T010, Completed 2026-07-10 | WS-03 | The 2026-07-06 scan's medium-severity CORS wildcard finding was patched, and Diana **re-verified the CVE/CORS patch on 2026-07-15** for release evidence (SRC-CU-CIPH-20, SRC-GDOC-09). |
| **Batch CLI processing tool** — CIPH-13 / T003, Completed 2026-06-12 | WS-02 | Binary packaged to the release artifact store 2026-07-15; still load-bearing — the Electron desktop wrapper's IPC bridge was accepted against it on 2026-08-18 (SRC-CU-CIPH-13, SRC-GDOC-48). |
| **AES-256 at-rest encryption pipeline**, signed off Completed 2026-08-07 | WS-03 | Sign-off was deliberately withheld until fail-closed deletion (T015) was confirmed Completed (QA pass 2026-07-16); pipeline verified to refuse plaintext writes if key material is unavailable (SRC-GDOC-35, SRC-SLACK-21, SRC-SLACK-12). |
| **Redaction preview overlay** — T023, Completed 2026-08-08 | WS-01/UI | The 2026-08-10 acceptance audit re-confirms the closure and explicitly states it does **not** reopen for unrelated rendering issues tracked elsewhere; it later absorbed the a11y audit scope (SRC-GDOC-37, SRC-GDOC-17, SRC-GDOC-33). |
| **Statically linked air-gap runtime binary** — CIPH-28, Completed | Local runtime | Verified 2026-08-05 to run with no external shared-library dependencies, meeting the air-gap packaging requirement (SRC-CU-CIPH-28). |
| **Bare-metal performance benchmarks** — CIPH-38, Completed 2026-08-12 | WS-03 | The provisioning block cleared 2026-08-11; results rerun on the dedicated node and published against the completed multi-threading baseline (SRC-CU-CIPH-38, SRC-SLACK-35). |

---

### 3. Completed → reopened (do **not** count these as done)

**a. Docker packaging — CIPH-15 / T005 — Active (Reopened), Evan.** Initial Dockerfile Completed 2026-06-16; Diana reopened it 2026-06-25 when the built image measured **2.1GB**. Multi-stage rebuild, Alpine base swap and removal of unused OCR/runtime packages followed. At the **2026-08-12** verification the image was *still* over the ~450MB target **and CVE verification was still failing**. Confirmed still open at the 2026-09-15 pre-release audit. (SRC-CU-CIPH-15, SRC-SLACK-06, SRC-MEET-10)

**b. Large-file stream chunking — CIPH-41 / T031 — Active (Reopened), Charlie.** Merged to mainline 2026-08-16 and "called done"; reopened 2026-08-18 when files ≥2GB still leaked memory (peak memory climbing linearly with file size). Buffer-release refactor is in progress — a 2.3GB local sample shows flat memory, but as of the 2026-08-23 review it is **not yet validated against the full large-file corpus**. Note a distinct, genuinely closed item: the PDF loader's page-object cache leak was patched and verified Completed 2026-08-23 — that is a *different* defect and does not close T031. (SRC-CU-CIPH-41, SRC-GDOC-42, SRC-SLACK-43/44, SRC-GDOC-44)

**c. Third-party license audit — CIPH-40 — Active (Reopened), Diana.** Ghostscript (AGPLv3) was swapped out and the swap was **initially marked Completed** (2026-08-11); reopened 2026-08-12 when the replacement PDF parser turned out to be AGPL-licensed too — same license category, one layer down. Charlie's search for an Apache-2.0/MIT alternative had not concluded as of 2026-08-21. Secondary open item: `eng.traineddata` provenance unverified. (SRC-CU-CIPH-40, SRC-GDOC-41, SRC-GDOC-24)

**d. Storage-quota halt — CIPH-32 — Active (Reopened), Evan.** Diana verified the 500MB hard halt and "called this done" 2026-08-06; Evan reopened it **2026-09-15** because production-like batches tripped the hard halt before doing useful work. Bob refactored to a 10% buffer tolerance on 2026-09-18 and Evan re-tested the previously failing batches clean the same day — but the task record still stands as **Active (Reopened)**; no formal re-closure is recorded. Treat as "fix verified in channel, closure pending". (SRC-CU-CIPH-32, SRC-SLACK-23)

---

### 4. Durable blockers (long-lived, no owned path to resolution)

1. **Upstream `pdfminer.six` whitespace/offset fix — blocked since 2026-06-26 (≈3 months).** Depends on upstream PR **#992**, still unmerged at the 2026-09-10 recheck. The team evaluated forking on 2026-08-20 and **deliberately declined** ("maintaining a PDF parsing fork long-term is more risk than the wait"). Alice on 2026-09-10: "This is becoming a real risk for the v1.0 timeline." (SRC-SLACK-07)
2. **Offline auth with key rotation — CIPH-29, Blocked since 2026-08-05, Diana/Bob, High.** The chosen rotation design *assumes a network connection*; testing against a local auth mock proved rotation cannot complete air-gapped. No fix identified. This is a design-level, not a bug-level, block. (SRC-CU-CIPH-29, SRC-MEET-07)
3. **High-DPI coordinate scaling — T036, Blocked (2026-09-10).** Misalignment reproduces consistently at 150% and 200% display scale; root cause traced to a defect in the **upstream rendering library's** scaling math, with no safe local fix identified. Still listed as open at the 2026-09-15 gate review. (SRC-GDOC-49, SRC-GDOC-30, SRC-MEET-10)
4. **Async batch scheduler — CIPH-47 / T037, Blocked since 2026-08-25.** Concurrent async workers racing with the existing multi-threaded pool on the shared results manifest corrupt JSON writes and cut throughput ~10% versus the sync baseline. Alice: "A 10% hit is not shippable." All further async work is held. (SRC-CU-CIPH-47, SRC-GDOC-50, SRC-SLACK-61)
5. **Multi-site node-sync handshake — CIPH-34, Blocked, reconfirmed today (2026-09-22), High.** Nominal latency passes; on a simulated high-latency link the handshake never completes. The team explicitly rejected a timeout bump as masking the problem and left it blocked pending movement on the encryption path. (SRC-CU-CIPH-34, SRC-MEET-11)

---

### 5. Top risks to escalate before ship

**R1 — The v1.0 release gate cannot close (CIPH-21 / T011, Active).** Diana holds a security gate pending **both** T005 Docker slim-down/CVE **and** T029 Windows code-signing, with the audit-log mismatch kept visible as a third release blocker. Alice, 2026-09-15: "No one closes those today." Escalate: this is the critical path, and none of its three legs moved in September. (SRC-CU-CIPH-21, SRC-MEET-10)

**R2 — Windows code-signing certificate has not been procured.** Packaging itself is fixed (build artifact produced 2026-08-12), but the binary is unsigned, triggering SmartScreen/Defender flags. Site IT policies commonly block unsigned binaries outright, which would **prevent installation on target deployment workstations**. Root cause is procurement, not engineering — this is escalatable today and resolvable with a purchase decision. (SRC-GDOC-39)

**R3 — AGPL code is still in the shipped dependency set.** Client agreements rule out shipping copyleft in the core engine; two successive remediation attempts have failed and no compliant parser has been confirmed. This is a contractual/legal exposure, not a schedule slip, and it has been open since 2026-08-08. (SRC-CU-CIPH-40, SRC-SLACK-39)

**R4 — Audit trail fails its own schema.** CIPH-26 remains Active: the 2026-09-18 verification found CLI-emitted audit records inconsistent with the defined JSON schema. Diana: this "undercuts the audit trail as release evidence" and the gate stays red until schema and records match. For a redaction product sold on compliance, defective audit evidence is a category risk, not a bug. (SRC-CU-CIPH-26, SRC-MEET-10)

**R5 — Two blockers sit in code we don't own and have chosen not to fork** (pdfminer.six #992; the high-DPI rendering library). There is currently no internal lever on either. Recommend a dated decision point: accept the slip, ship with a documented limitation, or revisit the fork decision.

**R6 — Memory safety on the largest inputs is unproven.** The 2GB+ buffer-release fix has only local-sample evidence; the full large-file corpus run has not happened. Shipping on partial validation risks field OOM kills of the type QA already reproduced.

**R7 — Scope risk carried into v1.0: REST API authentication is Deferred to v1.1** (CIPH-19), with v1.0 resting on a "trusted local network" assumption reconfirmed 2026-08-20. Given the PII in scope, this assumption should be an explicit, signed customer-facing statement rather than an internal one. Related hardening item: on non-TPM hardware the volume key is still PBKDF2-derived; Argon2id migration is tracked as a pre-v1.0 hardening item, not a sign-off condition. (SRC-CU-CIPH-19, SRC-SLACK-08, SRC-GDOC-35)

---

### 6. Suggested asks

- **Procure the Windows code-signing certificate now** (R2) — the only gate leg with a same-week resolution path.
- **Set a decision date on the two upstream blocks** (R5) — fork, workaround, or documented limitation.
- **Get legal/commercial sign-off on the AGPL exposure** and consider funding a parser evaluation (R3).
- **Do not report Docker packaging, large-file chunking, license audit, or storage-quota halt as complete** in any external status — all four are reopened, and only the quota fix has verification evidence behind it.

**Sources cited:** SRC-CU-CIPH-13/15/19/20/21/23/26/27/28/29/32/34/38/40/41/47; SRC-GDOC-05/06/09/17/22/24/30/33/35/37/39/41/42/44/48/49/50; SRC-SLACK-06/07/08/12/21/23/35/39/43/44/61; SRC-MEET-05/07/09/10/11.
