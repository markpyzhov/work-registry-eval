# Beyond Docker and Windows packaging, which compliance and audit items still hold v1.0.0 as of **2026-09-22**? For each, give current status, the concrete defect or risk, and whether engineering search alone can close it.

<!-- RESPONSE_START -->

## Answer

**Scope note.** The formal release-gate task (CIPH-21 / T011, Status: Active) names only two acceptance blockers — T005 Docker image size/CVE and T029 Windows code-signing (SRC-CU-CIPH-21). Everything below is the *compliance and audit* work that is still open around those two as of 2026-09-22. The latest evidence in the dataset runs to 2026-09-18; nothing after that date reports any of these closed.

---

### 1. Audit-trail logging — the schema/record mismatch (CIPH-26, T016)

- **Status:** Active, Priority High, assignee Diana (implementation by Bob). Explicitly recorded as "an open release blocker." Diana held the gate red at the 2026-09-15 pre-release audit and the 2026-09-18 verification pass reconfirmed the failure.
- **Defect:** The audit design requires, per processed file, a SHA-256 hash of the input stream plus a companion JSON document recording the applied redaction map. Hashing (2026-08-05), schema definition (2026-08-15) and CLI wiring (2026-09-10) all landed, but the records the CLI actually emits do not validate against the defined companion JSON schema. Charlie confirmed in the 2026-09-15 meeting that this is "schema versus emitted records," not a packaging problem. Diana's stated consequence: it "undercuts the audit trail as release evidence."
- **Can engineering search alone close it?** No — and it does not need one. There is no external dependency and nothing to look for; it is an in-house code fix to align the emitter's output shape with the schema, followed by Diana's re-verification. Bob had "another pass queued" as of 2026-09-15.
- **Sources:** SRC-CU-CIPH-26 (`med-synth/tasks/CIPH-26-Audit-Trail-Logging.md`), SRC-MEET-10 (`.../fireflies/2026-09-15-Pre-Release-Audit.md`), SRC-GDOC-11 (`.../2026-07-08-Compliance-Audit-Trail.md`).

### 2. Third-party license audit — AGPL PDF parser (CIPH-40, DOC-2041)

- **Status:** Active (Reopened), Priority High, owner Diana. Reopened 2026-08-12; unresolved as of the 2026-08-21 report, with the explicit instruction: do not report license compliance as resolved externally.
- **Defect:** The original audit flagged Ghostscript (AGPLv3, on the corporate license blacklist for viral copyleft on binaries distributed to partner sites) in the `rasterizer` module. Evan's replacement parser (swapped in 2026-08-11) turned out to be AGPL-licensed too — the swap moved the same license category problem one layer down. AGPL is a dealbreaker for the current distribution model (Alice, 2026-08-12); client agreements rule out shipping copyleft in the core engine.
- **Can engineering search alone close it?** Search is necessary but demonstrably not sufficient. Charlie has been searching for an Apache 2.0/MIT parser since 2026-08-15 and reported "a couple" of candidates, but "neither one covers everything the old library did," and he refuses to force a bad fit. Closing the item requires finding a candidate, confirming feature coverage for the module's rasterization requirements, doing the swap (rework cost unknown until candidates are compared), and passing a clean re-scan. So: engineering-owned, no external gatekeeper, but not closable by searching alone — it needs a viable replacement to exist and integration work to follow.
- **Sources:** SRC-CU-CIPH-40, SRC-GDOC-41 (`.../2026-08-21-License-Compliance-Audit-Report.md`), SRC-GDOC-24, SRC-SLACK-40, SRC-SLACK-41, SRC-MEET-08.

### 3. OCR training-data provenance — `eng.traineddata` / `tessdata_best`

- **Status:** Separate, lower-priority open item under the same license audit, pending Evan's provenance trace. Listed in the 2026-08-21 warning as still unverified.
- **Defect:** Tesseract OCR itself is Apache 2.0, but the `eng.traineddata` model files were pulled from a community repository and the training-corpus provenance has not been verified as public-domain/CC0. Until it is, the shipped model files sit outside the audited license set.
- **Can engineering search alone close it?** No. This is an external records trace — chasing the upstream community repository's corpus provenance — not a code or dependency search. If the upstream records don't establish public-domain/CC0 status, no amount of engineering effort inside the repo resolves it; the fallback would be sourcing differently or accepting/escalating the risk.
- **Source:** SRC-GDOC-41 (`.../2026-08-21-License-Compliance-Audit-Report.md`).

### 4. Telemetry privacy — unaudited Sentry crash-reporter path (DOC-2051)

- **Status:** CLI-side opt-out is verified Completed (CIPH-48; network trace 2026-08-24 confirmed zero outbound telemetry). The crash-reporter path is the remaining limitation, recorded 2026-09-06.
- **Defect:** The third-party Electron crash reporter (Sentry) has never been audited for whether it independently respects the opt-out environment variable or needs its own disable hook for minidump uploads. Stated consequence: "Full privacy compliance for air-gapped/opt-out users cannot be claimed until the Sentry crash-reporter path is audited separately." Note the precedent from the same document — the `TelemetryLogger` was found still writing payloads to a local SQLite queue while opted out, so a second egress path escaping the flag is a demonstrated failure mode, not a hypothetical one. Charlie had also flagged the risk of PII landing in crash reports (2026-08-20).
- **Can engineering search alone close it?** Effectively yes, in the sense that it is fully in-house and bounded: inspect the Sentry integration, determine whether it honours `CIPHER_TELEMETRY=0`, add a disable hook if not, and re-run a network/minidump trace. No procurement, no upstream, no external body. It is verification work rather than a hunt, and it has simply not been started.
- **Sources:** SRC-GDOC-51 (`.../2026-09-06-Telemetry-Opt-Out-Design-and-Compliance-Check.md`), SRC-CU-CIPH-48, SRC-SLACK-62, SRC-SLACK-64.

### 5. Air-gapped/offline mode — no compliance certification, only a preliminary pass (CIPH-37, DOC-2047, DOC-2046)

- **Status:** The offline batch run is Completed and signed off (2026-08-10) — but the sign-off is explicitly and repeatedly labelled preliminary and "not a compliance certification." The harness itself (T027, DOC-2046) is Active.
- **Defects/risks, three distinct ones:**
  - **Certification scope gap.** The sign-off covers functional completion of one offline batch run only. It explicitly does not cover side-channel analysis, physical security, or any regulatory attestation. No patient records or clinical data were used in the test.
  - **45-second licence-check hang.** The HTTP client still reaches for a remote endpoint to verify the license key before timing out and falling back to the cached local license, adding ~45s of startup delay. Diana logged it as "noted, not resolved" and declined to touch it because it sits in the encryption-pipeline path. For an air-gapped deployment claim, a component that tries to phone home at startup is exactly the behaviour the harness was built to surface.
  - **Harness not in CI.** It runs manually, so the offline claim cannot be continuously re-verified — which was the original justification for building the harness instead of hand-configuring a VM.
- **Can engineering search alone close it?** Split. The hang and the CI wiring are ordinary engineering work, no search needed. The certification gap is not closable by engineering at all — regulatory attestation, side-channel analysis and physical security are outside what the team can self-certify; that requires an external process and a decision about whether v1.0.0 ships making the air-gapped claim on a preliminary pass.
- **Sources:** SRC-CU-CIPH-37, SRC-GDOC-47 (`.../2026-08-10-Air-Gapped-Mode-Offline-Signoff.md`), SRC-GDOC-46 (`.../2026-08-06-Air-Gapped-Mode-Harness-Design.md`), SRC-SLACK-33.

### 6. Passphrase-derived key hardening — Argon2id (DOC-2035)

- **Status:** Tracked separately as a **pre-v1.0 hardening item**, flagged by Diana at the AES-256 at-rest sign-off (2026-08-07). Explicitly not a sign-off condition — the AES-256 pipeline itself is signed off Completed — but it is scoped to land before v1.0.
- **Defect:** On machines without a hardware TPM, the volume key is still derived from a user passphrase via PBKDF2-HMAC-SHA256 at 100k iterations. Moving to Argon2id would materially raise the cost of offline brute-force against weak passphrases on non-TPM hardware.
- **Can engineering search alone close it?** Yes, in the sense that it is a self-contained in-house implementation change with a known target algorithm — nothing to search for, nothing external to wait on. It is the cheapest item on this list.
- **Source:** SRC-GDOC-35 (`.../2026-08-07-Local-Encryption-at-Rest-Security-Evaluation.md`).

---

### Two documented caveats that are not gates but constrain what can be claimed

- **HIPAA coverage is not certified.** The expanded HIPAA identifier patterns were merged 2026-08-08 and passed a regression check against the financial-PII baseline, but the report states plainly that it "is not a HIPAA compliance certification and does not assess coverage completeness against every HIPAA identifier category in production data" (SRC-GDOC-34). Engineering cannot close this by itself; it is a certification question.
- **REST API auth is deferred, not resolved.** CIPH-19 is Deferred to v1.1; v1.0 assumes a trusted local network, and Alice reconfirmed that scope on 2026-08-20. Diana's original concern — "Given the PII involved, something robust would be nice" — was accepted as manageable *only if* deployments stay local-network-only. That assumption is a deliberate risk carried into v1.0.0, not a defect (SRC-SLACK-08, SRC-CU-CIPH-19). Relatedly, CIPH-29 (offline auth with key rotation for air-gapped installs) remains **Blocked** — key rotation cannot complete without network access, with no resolution found (SRC-CU-CIPH-29).

### Summary table

| Item | Status | Closable by engineering search alone? |
|---|---|---|
| Audit-trail schema mismatch (CIPH-26) | Active, High — open release blocker | No search needed; in-house code fix + re-verify |
| AGPL PDF parser (CIPH-40) | Active (Reopened), High | Search is the current activity but insufficient — needs a viable candidate + swap + clean re-scan |
| OCR `tessdata` provenance | Open, lower priority | No — external provenance trace, may be unresolvable |
| Sentry crash-reporter audit | Not started | Yes — bounded in-house audit/test |
| Air-gapped compliance certification | Preliminary sign-off only | Partly — hang and CI are engineering; attestation is not |
| Argon2id key hardening | Open pre-v1.0 item | Yes — self-contained implementation change |

**Bottom line:** three of the six are fully within engineering's control (audit-log schema, Sentry audit, Argon2id). One is a search that has already stalled on feature coverage (AGPL parser). Two cannot be closed by engineering at all — the OCR training-data provenance trace depends on upstream records that may not exist, and the air-gapped compliance certification requires an external attestation process the team has explicitly declined to self-certify. Combined with the Windows code-signing certificate sitting in procurement with "no firm timeline," the v1.0.0 critical path runs through at least three non-engineering dependencies, not just the two gates CIPH-21 formally tracks.
