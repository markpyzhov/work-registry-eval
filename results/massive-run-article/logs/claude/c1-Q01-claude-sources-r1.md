# As of the final CipherDoc snapshot on **2026-09-22**, is the toolkit ready to ship v1.0.0? Give a clear go/no-go, name every release gate that is still open, and cite the evidence that keeps each gate from closing.

<!-- RESPONSE_START -->

## Go / No-Go: **NO-GO**

As of the final CipherDoc snapshot on **2026-09-22**, the toolkit is **not ready to ship v1.0.0**. The release-gate tracker itself (`CIPH-21` / T011 "Release v1.0 Gates", owner Evan) is still **Active**, and Diana's security-gate hold on the release has never been lifted. The last full gate review (Fireflies, 2026-09-15) ended with Alice stating explicitly that no gates were being closed and Evan noting "Release isn't opening with any of those unresolved." Nothing in the dataset after that date closes any of them; the only 2026-09-22 activity is a *new* block being recorded.

---

### Release gates still open, with the evidence keeping each one from closing

**1. Docker image slim-down + CVE verification (T005 / `CIPH-15` Docker Packaging) — Active (Reopened)**
- `CIPH-15` acceptance criteria: "Image size reduced to the ~450MB target (**not yet met**)" and "CVE verification passes with no outstanding findings (**not yet met**)"; task stays Active (Reopened) until both pass. (SRC-CU-CIPH-15)
- Slack #releases, 2026-08-12 — Diana: "We're still over the ~450MB target, and the CVE verification is still failing." Evan: "not where we need to be yet… I need to chase down what's tripping the CVE scan." Diana: "Reopened status stands until both the size and the CVE check are clean." (SRC-SLACK-06). Original trigger: 2.1GB image, reopened 2026-06-25.
- Still listed as open at the 2026-09-15 pre-release audit (SRC-MEET-10). No later evidence of a passing size or CVE run.

**2. Windows code-signing / Defender + SmartScreen (T029 / `CIPH-39`) — Active**
- Compatibility Audit DOC-2039 (2026-09-02): the build artifact is **unsigned**; SmartScreen warns and Defender flags it as untrusted. Root cause: "No code-signing certificate has been procured or configured in the Windows build pipeline yet." Audit Status: Active — "signing certificate procurement is the sole open blocker," and it holds the T011 release checklist alongside the T005 slim-down. (SRC-GDOC-39)
- Slack #releases, 2026-09-02 — Evan: "We still don't have one… this isn't something we can work around on the engineering side, we need the certificate." Alice: "Let's keep it open on the release gate." (SRC-SLACK-37). Earlier, 2026-08-15: "Still waiting on the code-signing certificate to come through procurement. No firm timeline." (SRC-MEET-08)

**3. Audit-trail logging — CLI records don't validate against the schema (`CIPH-26`) — Active, explicitly an open release blocker**
- `CIPH-26` activity history, **2026-09-18** (Diana, "Audit Verify (Mismatch)"): "Verification found the CLI-emitted audit records inconsistent with the defined schema; this mismatch remains an open release blocker." Acceptance criterion "CLI-emitted audit records validate cleanly against the defined companion JSON schema" is marked *currently failing verification*. (SRC-CU-CIPH-26)
- 2026-09-15 pre-release audit — Diana: "Still a hold… That undercuts the audit trail as release evidence… I'll keep the audit-log gate red until schema and records match." Bob: "The shape coming out still isn't consistent with what the schema expects — I've got another pass queued." (SRC-MEET-10)

**4. High-DPI PDF coordinate scaling (`CIPH-46` / T036) — Blocked on upstream**
- `CIPH-46` is **Blocked** as of 2026-09-10: scaling-math error traced to a bug in the upstream rendering library, "no local fix available yet." (SRC-CU-CIPH-46)
- DOC-2049 (2026-09-10): "T036 is Blocked on that upstream library issue… cannot clear the gate until upstream scaling is corrected or an accepted local remediation is chosen." (SRC-GDOC-49)
- Slack, 2026-09-10 — Charlie: `pdf-lib-core` has a known XObject/parent-transform coordinate bug, "deep in their C++ core," upstream maintainers have not responded; flattening rejected as a workaround. Alice: "let's leave high-DPI rendering blocked for now. We need to decide if we can ship with this limitation." (SRC-SLACK-58). Named as still open at the 2026-09-15 gate review.

**5. Third-party license compliance — AGPL dependency (`CIPH-40`) — Active (Reopened)**
- `CIPH-40` acceptance criteria require "No restrictive copyleft (e.g., AGPL) licenses remain in the shipped dependency set" and adoption of an Apache/MIT parser — unmet. The Ghostscript (AGPLv3) swap was reversed in effect when the replacement parser turned out to also be AGPL (reopened 2026-08-12). (SRC-CU-CIPH-40, SRC-SLACK-40)
- DOC-2041 (2026-08-21): "No suitable replacement has been confirmed yet, so this audit item remains **Active (Reopened)** — not resolved," and carries an explicit warning: "Do not report license compliance as resolved externally. The PDF-parser license category issue is still open, and OCR training-data provenance is unverified." (SRC-GDOC-41; corroborated by SRC-GDOC-24: "that search had not concluded")
- Alice, 2026-08-09: "Our client agreements rule out shipping copyleft code in the core engine"; Alice, 2026-08-12: "AGPL is a dealbreaker for how we distribute this." (SRC-SLACK-39, SRC-SLACK-40). Last status, 2026-08-15: "Still unresolved as of today." (SRC-SLACK-41)
- Sub-item: the Tesseract `eng.traineddata` provenance has not been verified as public-domain/CC0 — a separate, lower-priority open item pending Evan's `tessdata_best` trace. (SRC-GDOC-41)

**6. Multi-page PDF coordinate/offset drift (`CIPH-17`) — Blocked on upstream `pdfminer.six` PR #992**
- `CIPH-17` (High priority) is **Blocked**: acceptance requires PR #992 to merge or an accepted local remediation — "neither has occurred." A local fork was evaluated and rejected. (SRC-CU-CIPH-17)
- Slack, 2026-09-10 — Charlie: "#992 is still unmerged. No safe local path that doesn't involve owning a fork, so we're leaving the offset fix blocked." Alice: "This is becoming a real risk for the v1.0 timeline." (SRC-SLACK-07)

**7. The release checklist itself (`CIPH-21` / T011) — Active**
- T001–T006 and T010 dependencies are satisfied except T005; the checklist "cannot close until that gate clears" (DOC-2005, SRC-GDOC-05), and `CIPH-21` records that release notes were drafted in parallel *while gates stayed open* — drafted notes are not evidence of a cleared gate. (SRC-CU-CIPH-21)

---

### Adjacent open work that further undercuts a v1.0.0 ship (not named as formal gates)

- **`CIPH-34` authenticated multi-site handshake — Blocked on 2026-09-22** (the snapshot date itself): handshake times out on high-latency links; AES-256 per-packet overhead pushes the exchange past the timeout window. Team explicitly refused a timeout-bump workaround. (SRC-CU-CIPH-34, SRC-MEET-11, SRC-SLACK-27)
- **`CIPH-29` offline auth with key rotation for air-gapped installs — Blocked**: rotation cannot complete without network access. (SRC-CU-CIPH-29)
- **`CIPH-47` async batch scheduler — Blocked**: confirmed concurrent I/O race corrupting the shared manifest, ~10% throughput regression. (SRC-CU-CIPH-47, SRC-GDOC-50)
- **Privacy**: CLI telemetry opt-out is verified, but "Full privacy compliance for air-gapped/opt-out users cannot be claimed until the Sentry crash-reporter path is audited separately." (SRC-GDOC-51)
- **Crypto hardening**: on non-TPM hardware the volume key is PBKDF2-HMAC-SHA256 (100k iterations); Argon2id migration is tracked as a **pre-v1.0 hardening item**. (SRC-GDOC-35)
- **Known issue, unresolved**: ~45-second startup hang in the offline license check; the offline batch sign-off is explicitly "preliminary… not a compliance certification." (SRC-GDOC-47, SRC-SLACK-33)

### What is *not* a blocker
- **REST API authentication (`CIPH-19`)** is a deliberate, reconfirmed **deferral to v1.1** — Alice rechecked release scope on 2026-08-20: "auth stays deferred to post-v1.0.0. Trusted-network assumption still holds." v1.0 ships local-network-only. (SRC-CU-CIPH-19, SRC-SLACK-08)
- Cleared gates on record: core redaction engine, financial regex detection, batch CLI, REST API endpoints, redaction policy config, security audit/CVE-CORS patch (re-verified 2026-07-15), fail-closed batch behavior, AES-256 at-rest pipeline sign-off, Windows path-handling fix and build production, published benchmarks.

**Bottom line:** six release gates remain open — Docker size/CVE, Windows code-signing, audit-log schema conformance, high-DPI coordinate scaling, AGPL license compliance, and multi-page offset drift — two of them (high-DPI, offset drift) blocked on third parties with no committed timeline, and one (code-signing) blocked on procurement. Ship v1.0.0 only after these close, or after an explicit, documented decision to descope/accept the upstream-blocked defects as known issues; the license and code-signing gates are not descopable given the stated distribution and site-IT constraints.
