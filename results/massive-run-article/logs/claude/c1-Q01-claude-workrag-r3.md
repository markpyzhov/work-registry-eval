# As of the final CipherDoc snapshot on **2026-09-22**, is the toolkit ready to ship v1.0.0? Give a clear go/no-go, name every release gate that is still open, and cite the evidence that keeps each gate from closing.

<!-- RESPONSE_START -->

## Verdict: **NO-GO** — CipherDoc v1.0.0 is not ready to ship as of the 2026-09-22 snapshot

The release-gate work stream **WS-03 (Packaging, Release gating, and Security)** is `in_progress`, P0, owner Evan, last updated 2026-09-22. Its release-gate task `T011 / CIPH-21` is **Active under a security-gate hold**, and the ClickUp record for CIPH-21 is explicitly "Active with those two gates unresolved." The Work State Index (as-of 2026-09-22T12:00:00Z) lists T011 among Active/Reopened items. Nothing in the dataset records any gate being cleared after that date.

There is also a hard stop attached: **CMT-2026-09-002** (Diana, 2026-09-15) records a release-board decision of **no-ship after 2026-10-15 if T005 and T029 are not green — "Hard deadline — not advisory."**

---

### Formal release gates still open (CIPH-21 acceptance criteria)

**1. T005 / CIPH-15 — Docker image size + CVE verification**
CIPH-15 status is **Active (Reopened)**; both acceptance criteria are explicitly "not yet met." The image ballooned to 2.1GB after OCR dependencies were bundled, reopening the task on 2026-06-25 after Diana's size/CVE review (SRC-SLACK-06). Evan applied multi-stage builds, swapped `ubuntu:22.04` → `alpine:latest`, and stripped unused OCR/runtime packages, but at the 2026-08-12 verification Diana confirmed "We're still over the ~450MB target, and the CVE verification is still failing," with Evan noting residual bloat in the Python site-packages layer and an unidentified CVE-scan trigger. Diana: "Reopened status stands until both the size and the CVE check are clean."
Note the **dual thresholds** from **CMT-2026-06-002** (CISO review): an interim release candidate may ship at **800MB once CVE-clean**, while **GA remains ~450MB** — the two must not be conflated on the checklist. Neither threshold is met, and CVE is not clean, so neither the RC nor the GA variant of this gate closes.

**2. T029 / CIPH-39 — Windows Authenticode code-signing certificate**
CIPH-39 is **Active**, priority High. Packaging is no longer the problem: backslash path handling was fixed 2026-08-10 and a Windows build artifact was produced by 2026-08-12 (SRC-GDOC-39). The blocker is that **no code-signing certificate has been procured or configured** in the Windows build pipeline, so Defender/SmartScreen flags the unsigned binary as untrusted — and site IT policies commonly block unsigned binaries outright. Evan (2026-09-02): "this isn't something we can work around on the engineering side, we need the certificate." Alice: "Let's keep it open on the release gate rather than pushing it off the board." WS-06 characterizes this as a **procurement dependency, not an engineering block**; budget/procurement timeline is sitting in WS-06's Needs Manual Triage.

---

### Additional gate flagged as an open release blocker by the 2026-09-15 pre-release audit

**3. T016 / CIPH-26 — Audit-trail log schema vs. CLI-emitted records**
CIPH-26 is **Active**, priority High, owner Diana. Bob wired audit-log generation into the CLI on 2026-09-10, but on **2026-09-18 Diana's verification found the CLI-emitted audit records inconsistent with the defined companion JSON schema**, and the record states "this mismatch remains an open release blocker." At the 2026-09-15 pre-release audit Diana said it "undercuts the audit trail as release evidence" and "I'll keep the audit-log gate red until schema and records match"; Alice confirmed "we keep the audit mismatch visible as a release blocker. No one closes those today." WS-04 carries this as active/reopened as of 2026-09-22.

---

### Further release dependencies tied to the T011 gate by comments (also unmet)

**4. T030 / CIPH-40 — AGPL license compliance (hard Legal P0 gate)**
**Reopened/active**. The Ghostscript (AGPLv3) removal was undone in effect when the replacement PDF parser turned out to also be AGPL-licensed (discovered 2026-08-12). **CMT-2026-08-002** escalates this to **P0 and a hard Legal gate**: AGPL in the bundle triggers whole-bundle copyleft exposure for the distribution model, and "engineering search alone is insufficient to close T030." Charlie is still searching for an Apache/MIT alternative; no suitable replacement confirmed. A secondary open item: `eng.traineddata` provenance for Tesseract is unverified.

**5. T031 / CIPH-41 — Large-file stream chunking**
Still unchecked in WS-05 and listed as Active/Reopened in the index. **CMT-2026-08-003** (Bob, 2026-08-18) ties it **explicitly to the T011 release gate** after the MedFirst pilot hit OOM on a 4.7GB PDF with 8GB RAM, calling it a pilot-blocker. (The related loader-leak work, T033/CIPH-43, *is* Completed and verified — that is not the open piece.)

**6. Legacy JSON → YAML policy auto-migration (T006-linked)**
T006/CIPH-16 itself is Completed (2026-06-22) and satisfies the original checklist dependency, but **CMT-2026-06-001** (Alice, 2026-06-21) adds a later requirement: MedFirst's three legacy JSON pilot policies "must auto-migrate before we cut over," with Evan owning the JSON→YAML converter, and instructs that migration be treated as "a release dependency tied to T006 and the T011 gate." It sits in WS-01 Active Work as of 2026-09-22 with no completion recorded.

---

### Open ship/no-ship decision, not yet resolved

**7. T036 / CIPH-46 — High-DPI PDF coordinate alignment**
**Blocked** on an upstream `pdf-lib-core` scaling-math defect; redaction coordinates drift 5–10 pixels on 4K displays at 200% scaling, and Charlie confirmed no local patch is possible ("It's deep in their C++ core"). **CMT-2026-09-001** widens the scope: 12% of the MedFirst pilot corpus fails alignment due to nested Form XObjects, so an upstream fix alone may not cover it. Alice at the 2026-09-15 audit listed high-DPI among items that "stay on the board," and on 2026-09-10 stated the team still needs "to decide if we can ship with this limitation or if we need a different rendering library entirely." That decision is unrecorded, so the release cannot be declared clean on this axis either — at minimum it requires an explicit accepted-limitation sign-off plus a documented known issue.

---

### What *is* green (so the no-go is narrow, not systemic)

- **T010 / CIPH-20 — Security audit and vulnerability scans: Complete.** The medium-severity CORS `*` origin finding in the 2026-07-06 scan report was patched by restricting to configured `ALLOWED_ORIGINS`, and 2026-07-15 re-scans confirmed the patch holds. **CMT-2026-07-002** adds a RedByte third-party pen-test attestation letter (2026-07-11) to the release evidence pack.
- The original checklist dependencies **T001–T004, T006, T010 are Completed** (per the 2026-07-12 Release Checklist); six of seven were met even then, with T005 the lone unmet item at that point.
- REST API auth (T009) is a **deliberate deferral to v1.1**, not a blocker — v1.0 assumes a trusted local network, re-confirmed by Alice on 2026-08-20. (Separately, CMT-2026-07-001 flags a MedFirst contractual auth deadline for the roadmap, not for v1.0.0.)
- The AES-256 at-rest encryption pipeline was signed off (Argon2id hardening tracked separately, explicitly not a sign-off condition).

---

### Bottom line

**No-go.** Two gates block by formal CIPH-21 acceptance criteria (Docker size/CVE, Windows code-signing), one more is held red by QA on release-evidence grounds (audit-log schema mismatch), a hard Legal P0 gate is unresolved (AGPL copyleft), two comment-added release dependencies are unmet (large-file chunking/OOM, legacy JSON auto-migration), and the high-DPI ship-with-limitation decision has never been made. The release checklist (DOC-2005) itself remains **Active (Draft)** and cannot close. Release notes were drafted in parallel while gates stayed open, which should not be mistaken for readiness. The board's hard no-ship date of **2026-10-15** applies if T005 and T029 are not green.

**Evidence cited:** `work-states/WS-03-ops.md`, `work-states/WS-04-policy.md`, `work-states/WS-05-performance.md`, `work-states/WS-06-platforms.md`, `work-states/WS-01-engine.md`, `work-states/index.md`; `work-states/comments/2026-06.md` (CMT-2026-06-001, CMT-2026-06-002), `work-states/comments/2026-08.md` (CMT-2026-08-002, CMT-2026-08-003), `work-states/comments/2026-09.md` (CMT-2026-09-001, CMT-2026-09-002), `work-states/comments/2026-07.md` (CMT-2026-07-002); sources `SRC-CU-CIPH-21`, `SRC-CU-CIPH-15`, `SRC-CU-CIPH-26`, `SRC-CU-CIPH-39`, `SRC-CU-CIPH-46`, `SRC-CU-CIPH-43`, `SRC-MEET-10` (2026-09-15 Pre-Release Audit), `SRC-SLACK-06`, `SRC-SLACK-37`, `SRC-SLACK-58`, `SRC-SLACK-08`, `SRC-GDOC-05`, `SRC-GDOC-39`, `SRC-GDOC-41`, `SRC-GDOC-44`, `SRC-GDOC-49`, `SRC-GDOC-11`, `SRC-GDOC-23`, `SRC-GDOC-35`.
