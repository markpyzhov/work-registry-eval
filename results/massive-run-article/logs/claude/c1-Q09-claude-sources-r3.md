# Beyond Docker and Windows packaging, which compliance and audit items still hold v1.0.0 as of **2026-09-22**? For each, give current status, the concrete defect or risk, and whether engineering search alone can close it.

<!-- RESPONSE_START -->

## Answer

Setting aside the two packaging gates (T005 Docker slim-down/CVE and T029/CIPH-39 Windows code-signing), the dataset shows **one hard compliance blocker** plus **five open compliance/audit items** that constrain what can be claimed for v1.0.0 as of 2026-09-22. No source in the dataset is dated later than 2026-09-18, so every status below is the latest recorded position going into 2026-09-22.

---

### A. Hard release blocker

**1. Audit-trail logging — CLI records don't validate against the schema (CIPH-26 / T016)**

- **Status:** Active, High priority, owner Diana (implementation by Bob). Explicitly held open as a release blocker.
- **Defect:** The design requires a SHA-256 hash of each input stream paired with a companion JSON document recording the redaction map, wired into the CLI batch path. Bob defined the schema on 2026-08-15 and wired CLI integration on 2026-09-10, but Diana's verification pass on **2026-09-18** found the CLI-emitted audit records inconsistent with the defined schema. At the 2026-09-15 pre-release audit Diana stated this "undercuts the audit trail as release evidence" and said she would keep the audit-log gate red until schema and records match; Alice confirmed it stays visible as a release blocker. Bob has "another pass queued."
- **Risk if shipped:** The audit trail — the artifact that ties a redacted output back to a specific input — is not usable as release/compliance evidence.
- **Can engineering close it alone?** **Yes.** This is purely internal: reconcile the emitter with the defined companion JSON schema (or vice versa) and re-run verification. Charlie confirmed in the 2026-09-15 meeting that it "isn't a packaging issue — it's schema versus emitted records." No external party, vendor, or procurement is involved.
- **Sources:** SRC-CU-CIPH-26; SRC-MEET-10 (2026-09-15 Pre-Release Audit); SRC-GDOC-11 (DOC-2011).

---

### B. Open compliance/audit items (not formally listed on the CIPH-21 gate list, but each blocks a compliance claim)

**2. Third-party license audit — AGPL still in the shipped dependency set (CIPH-40 / DOC-2041, DOC-2024)**

- **Status:** **Active (Reopened)**, High priority, owner Diana, search led by Charlie. Last recorded activity 2026-08-15; the 2026-08-21 report states no suitable replacement has been confirmed.
- **Defect:** The initial audit flagged `Ghostscript` (AGPLv3), used by the `rasterizer` module for PDF-to-image conversion, as blacklisted because its viral copyleft terms attach to any binary distributed to partner sites. Evan swapped in a replacement parser on 2026-08-11 and it was marked Completed — but on 2026-08-12 Diana found the replacement was **itself AGPL-licensed**, reintroducing the same license category one layer down. The task was reopened. Alice: AGPL "is a dealbreaker for how we distribute this"; client agreements rule out shipping copyleft in the core engine.
- **Risk:** Shipping v1.0.0 would distribute AGPL code under a distribution model that contractually cannot carry it. The 2026-08-21 report carries an explicit warning: do not report license compliance as resolved externally.
- **Can engineering search alone close it?** **No — search is necessary but not sufficient.** Charlie reported on 2026-08-15 that he had "a couple" of Apache/MIT candidates but "neither one covers everything the old library did," and he explicitly declined to force a bad fit. Closing this needs either (a) a candidate that actually meets the rasterization feature requirements plus the rework to adopt it (Charlie noted the rework cost is unknown until candidates are compared), or (b) a licensing/distribution decision above engineering. A pure search can fail to terminate.
- **Sources:** SRC-CU-CIPH-40; SRC-GDOC-41 (DOC-2041); SRC-GDOC-24 (DOC-2024); SRC-SLACK-40; SRC-SLACK-41; SRC-MEET-08.

**3. OCR training-data provenance unverified (`eng.traineddata` / `tessdata_best`)**

- **Status:** Open, separate and lower-priority sub-item of the license audit, pending Evan's provenance trace. No completion recorded.
- **Defect:** Tesseract OCR itself is Apache 2.0, but the `eng.traineddata` model files were sourced from a community repository and their **training-corpus provenance has not been verified as public-domain/CC0**.
- **Risk:** An unverified-provenance model file ships inside the binary; license compliance cannot be certified while it stands. The audit report names this alongside the parser issue in its "do not report as resolved externally" warning.
- **Can engineering search alone close it?** **No.** This is a documentary provenance trace of a third-party community artifact, not a code or dependency search. Either upstream provenance evidence exists and must be obtained, or the model must be replaced with one having a clean, documented corpus.
- **Sources:** SRC-GDOC-41 (DOC-2041).

**4. Sentry/Electron crash-reporter path not audited against telemetry opt-out (DOC-2051)**

- **Status:** Partially closed. The CLI-side item (CIPH-48) is **Completed** — a 2026-08-24 network trace confirmed zero outbound telemetry with the opt-out flag set, and a design-time pending-queue leak (the `TelemetryLogger` writing to a local SQLite queue during opt-out, which would flush the backlog on re-enable) was patched to a no-op backend. The **crash-reporter path remains unaudited** as of the 2026-09-06 note.
- **Defect:** The third-party Electron crash reporter (Sentry) has not been checked for whether it independently respects the opt-out environment variable or requires its own disable hook for minidump uploads.
- **Risk:** An opted-out or air-gapped user could still emit minidumps. The document states plainly that full privacy compliance for air-gapped/opt-out users **cannot be claimed** until this path is audited separately. Note also Charlie's standing concern that crash reports must not carry PII, which is the whole point of the tool.
- **Can engineering close it alone?** **Yes.** This is an in-house audit of a bundled component plus, if needed, wiring a disable hook. No external dependency.
- **Sources:** SRC-GDOC-51 (DOC-2051); SRC-CU-CIPH-48; SRC-SLACK-62; SRC-SLACK-64.

**5. Air-gapped/offline sign-off is preliminary, not a compliance certification (CIPH-37 / DOC-2047, DOC-2046)**

- **Status:** CIPH-37 is **Completed**, but deliberately scoped. Diana: "I'll close this out, but I want to be clear this is a preliminary offline pass — not a compliance certification." Two residual gaps sit underneath it:
  - **45-second licence-check hang:** the HTTP client reaches for a remote licence server at startup before timing out and falling back to the cached local licence. Logged as a known issue, explicitly **not waived** by the sign-off, and not resolved.
  - **Harness not in CI (DOC-2046, Active):** the network-denial harness runs manually, is not wired into CI, and validates network denial only — it does not itself certify the offline batch run.
- **Risk:** The air-gapped claim rests on a one-off manual pass. The sign-off explicitly does not cover side-channel analysis, physical security, or any regulatory attestation.
- **Can engineering close it alone?** **Split.** The 45-second hang and the CI integration are ordinary engineering work and closable in-house. The **compliance certification / regulatory attestation is not** — that requires an external assessor, and no amount of engineering search produces it.
- **Sources:** SRC-GDOC-47 (DOC-2047); SRC-GDOC-46 (DOC-2046); SRC-CU-CIPH-37; SRC-SLACK-33.

**6. HIPAA pattern coverage verified only against a regression baseline, not certified (CIPH-30 / DOC-2034)**

- **Status:** CIPH-30 is **Completed** — the expanded HIPAA regex dictionary was merged 2026-08-08 and regression-checked against the financial-PII baseline, which passed. But the verification report is explicitly bounded.
- **Gap:** The report "is not a HIPAA compliance certification and does not assess coverage completeness against every HIPAA identifier category in production data." Charlie had flagged during enumeration that many HIPAA identifiers are noisier than the financial patterns.
- **Risk:** Detection coverage across the 18 HIPAA identifier categories is unmeasured against real production data; a coverage claim made on this evidence would overstate what was tested.
- **Can engineering close it alone?** **Partly.** Engineering can build a production-representative coverage assessment; it cannot self-issue a HIPAA certification. Note also that DOC-2047 records no patient records or clinical data were used in testing, so a production-data coverage assessment would additionally need a compliant data source.
- **Sources:** SRC-GDOC-34 (DOC-2034); SRC-CU-CIPH-30; SRC-SLACK-18.

---

### Also noted (adjacent, flagged pre-v1.0)

**Argon2id key-derivation hardening.** At the 2026-08-07 AES-256 at-rest sign-off, Diana signed the pipeline off as Completed but flagged that on machines without a hardware TPM the volume key is still derived from a user passphrase via PBKDF2-HMAC-SHA256 at 100k iterations. Moving to Argon2id would meaningfully raise the cost of offline brute-force against weak passphrases. This is tracked as a **pre-v1.0 hardening item, explicitly not a sign-off condition** — so it is not blocking, but it is an open pre-v1.0 security item and is fully closable by engineering alone. (SRC-GDOC-35 / DOC-2035.)

---

### Summary table

| # | Item | Status | Engineering alone can close? |
|---|---|---|---|
| 1 | Audit-trail CLI/schema mismatch (CIPH-26) | Active — **hard blocker** | **Yes** |
| 2 | AGPL PDF parser in dependency set (CIPH-40) | Active (Reopened) | **No** — search may not terminate; needs feature-viable candidate + rework, or a licensing decision |
| 3 | OCR `eng.traineddata` provenance | Open, lower priority | **No** — documentary provenance / replacement |
| 4 | Sentry crash-reporter vs. opt-out | Unaudited | **Yes** |
| 5 | Air-gapped sign-off preliminary (45s hang; harness not in CI; no attestation) | Task Completed, gaps open | **Partly** — hang + CI yes; certification no |
| 6 | HIPAA coverage not certified / not assessed on production data | Task Completed, gap open | **Partly** — assessment yes; certification no |
| — | Argon2id KDF hardening | Pre-v1.0 item, non-blocking | **Yes** |

**Bottom line:** exactly one compliance item is a formal release blocker beyond packaging — the audit-trail schema mismatch — and it is fully within engineering's control. The item most likely to slip the date is the AGPL parser replacement, because it depends on an ecosystem candidate that did not exist as of the last recorded search. Three further items (OCR provenance, offline compliance certification, HIPAA certification) cannot be closed by engineering search at all; they require external evidence or an external assessor.
