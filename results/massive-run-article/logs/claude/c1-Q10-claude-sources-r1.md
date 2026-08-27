# Write a concise cross-workstream management briefing as of **2026-09-22** covering at least three workstreams: at least two completed milestones that still hold, at least three items of work that were completed then reopened, at least two durable blockers, and the top risks that should escalate before ship. Do not present reopened work as done.

<!-- RESPONSE_START -->

# CipherDoc v1.0 — Cross-Workstream Management Briefing
**As of 2026-09-22** | Sources: `tl-v1` dataset `d13efb7c…` (`path: sources`)

## Headline

v1.0 is not shippable today. The release-gate task (CIPH-21 / T011, WS-03) remains **Active** with two named gates unresolved, and a third hold (audit-trail logging) was still red at the 2026-09-15 pre-release review. Foundational engineering across WS-01/WS-02 is genuinely done and durable; the exposure is concentrated in packaging, licensing, upstream dependencies and compliance evidence.

---

## Completed milestones that still hold

These were completed and have since been re-verified or re-archived — they are not at risk.

| Milestone | Workstream | Evidence |
|---|---|---|
| **Core Redaction Engine** (CIPH-11 / T001) — Completed 2026-06-05, reviewed by Diana; completed status re-archived 2026-07-14 as release-checklist evidence, task remains Completed | WS-01 | SRC-CU-CIPH-11 |
| **Batch CLI** (CIPH-13 / T003) — Completed 2026-06-12; completed binary packaged to the release artifact store 2026-07-15 as a durable build reference | WS-02 | SRC-CU-CIPH-13 |
| **REST API Endpoints** (CIPH-14 / T004) — Completed 2026-06-17 on Diana's security check; status reconfirmed 2026-07-15 for the release evidence pack | WS-02 | SRC-CU-CIPH-14 |
| **Security Audit / vulnerability patches** (CIPH-20 / T010) — Completed 2026-07-10; Diana re-verified the CVE/CORS patch still held on 2026-07-15 | WS-03 | SRC-CU-CIPH-20, SRC-GDOC-09 |
| **Conflict-resolution union rule** (CIPH-27) — Completed 2026-06-16, archived to the compliance pack 2026-07-17, then **regression-checked 2026-08-01** against the new HIPAA patterns and confirmed unbroken | WS-04 | SRC-CU-CIPH-27, SRC-GDOC-34 |
| **Batch fail-closed strategy** (CIPH-25) — Completed 2026-06-15; QA-validated 2026-07-16 (no output on failure, temp files securely deleted) ahead of the encryption and offline work that depends on it | WS-04 | SRC-CU-CIPH-25, SRC-SLACK-12 |
| **Redaction Policy Config (YAML)** (CIPH-16 / T006) — Completed 2026-06-22 | WS-01 | SRC-CU-CIPH-16 |
| **AES-256 at-rest encryption pipeline** — signed off Completed 2026-08-07, gated on the fail-closed contract being confirmed first | WS-03 | SRC-GDOC-35 |
| **Multi-threaded batch path** (CIPH-36) Completed 2026-08-07; **bare-metal benchmarks** (CIPH-38) published 2026-08-12 on that baseline | WS-02 | SRC-CU-CIPH-36, SRC-CU-CIPH-38 |
| **Static-linked local runtime binary** (CIPH-28) — verified air-gap-clean 2026-08-05 | WS-03 | SRC-CU-CIPH-28 |
| **Preview overlay** (T023) Completed 2026-08-08; **profile schema export** (CIPH-42) Completed 2026-08-16 | WS-01 / WS-02 | SRC-GDOC-37, SRC-CU-CIPH-42 |

---

## Work that was completed and then reopened — **not done**

All five below were at some point called done. None can be counted as complete today.

**1. Docker packaging — CIPH-15 / T005 (WS-03) — Active (Reopened)** — *Evan*
Initial Dockerfile completed 2026-06-16. Diana reopened it 2026-06-25 when the built image measured **2.1 GB** against a ~450 MB target. Remediation ran through multi-stage build, Alpine base swap and removal of unused OCR/runtime packages. At the 2026-08-12 verification the image was **still over target and the CVE scan still failing**. Reopened status explicitly stands until both are clean.
*(SRC-CU-CIPH-15, SRC-SLACK-06, SRC-GDOC-05)*

**2. Third-party license audit — CIPH-40 (WS-03/WS-04) — Active (Reopened)** — *Diana / Charlie*
The original Ghostscript (AGPLv3) finding was remediated by swapping in a replacement PDF parser on 2026-08-11 and **initially marked Completed**. Reopened 2026-08-12 when the replacement itself proved AGPL-licensed — the same license category one layer down. As of 2026-08-21 **no suitable Apache-2.0/MIT replacement has been confirmed**. A secondary open item (unverified provenance of Tesseract `eng.traineddata` training corpus) is tracked separately.
*(SRC-CU-CIPH-40, SRC-GDOC-41, SRC-GDOC-24, SRC-MEET-08)*

**3. Large-file stream chunking — CIPH-41 / T031 (WS-01) — Active (Reopened)** — *Charlie*
Merged to mainline 2026-08-16 and called done. Reopened 2026-08-18 after 2 GB+ files still leaked memory (QA reproduced; processes OOM-killed on larger inputs). Per-chunk buffer-release refactor is in progress — early testing on a 2.3 GB sample shows flat memory, but as of 2026-08-23 the fix is **not validated against the full large-file corpus**. Note the related loader-side leak (CIPH-43) *is* separately Completed and verified — do not read that as closing CIPH-41.
*(SRC-CU-CIPH-41, SRC-GDOC-42, SRC-SLACK-43, SRC-SLACK-44)*

**4. Storage-quota halt — CIPH-32 / T022 (WS-03) — Active (Reopened)** — *Evan / Bob*
Verified and called done 2026-08-06 against a hard 500 MB floor. **Reopened 2026-09-15** when production-like batches tripped the hard halt before doing useful work. Bob refactored to a 10% buffer tolerance on 2026-09-18 and Evan re-tested without premature halts — but the task record still carries **Active (Reopened)**; treat as pending formal re-acceptance.
*(SRC-CU-CIPH-32, SRC-SLACK-23)*

**5. Node-sync handshake validation — CIPH-34 (WS-03) — reopened into Blocked** — *Bob*
The nominal-latency validation of 2026-08-08 passed cleanly and still holds. Diana **reopened it on 2026-09-22** after the handshake timed out over a simulated high-latency link, and the task moved to **Blocked** the same day. This is the newest status change in the record.
*(SRC-SLACK-27, SRC-CU-CIPH-34, SRC-MEET-11)*

---

## Durable blockers

**A. Upstream `pdfminer.six` PR #992 — CIPH-17, coordinate/offset drift (WS-01) — blocked ~3 months**
Blocked since 2026-06-26. Rechecked 2026-08-05 and again 2026-09-10: **still unmerged, no maintainer movement**. The team formally evaluated and rejected forking on 2026-08-20 as more long-term risk than the wait. No local workaround adopted. Alice flagged it on 2026-09-10 as "a real risk for the v1.0 timeline."
*(SRC-SLACK-07, SRC-CU-CIPH-17)*

**B. Windows code-signing certificate — CIPH-39 / T029 (WS-03) — blocked since ~2026-08-12**
Engineering is finished: the path fix landed 2026-08-10 and a working, runnable Windows artifact existed by 2026-08-12. The binary is **unsigned**, so Defender/SmartScreen flag it and site IT policies will block installation outright. Root cause is **procurement, not engineering** — no certificate has been obtained and, as of 2026-08-15, no firm timeline. Reconfirmed as a release blocker 2026-09-02 and again 2026-09-15.
*(SRC-GDOC-39, SRC-SLACK-37, SRC-MEET-08, SRC-CU-CIPH-39)*

**C. Offline auth key rotation — CIPH-29 (WS-03) — blocked since 2026-08-05**
The chosen rotation design assumes a live connection; rotation cannot complete in an air-gapped setting. Bob confirmed it is a design problem, not a mock artifact. **No fix identified**, no movement recorded since.
*(SRC-CU-CIPH-29, SRC-MEET-07)*

**D. Async scheduler concurrent I/O race — CIPH-47 / T037 (WS-02) — blocked since 2026-08-25**
Concurrent workers appending to a shared results manifest corrupt the JSON; recovery-path serialization measurably cuts batch throughput ~**10%** versus the expected async speedup. Blocks further scheduler rollout.
*(SRC-CU-CIPH-47, SRC-GDOC-50)*

**E. High-DPI coordinate scaling — CIPH-46 / T036 (WS-01) — blocked 2026-09-10**
Charlie's rotation fix works on simple documents but breaks entirely on nested Form XObjects, traced to a known bug deep in `pdf-lib-core`'s C++ core. Upstream issue opened; **no maintainer response**. Flattening as a workaround was rejected (file-size blowup, text-layer loss). Alice left it blocked pending a decision.
*(SRC-SLACK-58, SRC-CU-CIPH-46, SRC-GDOC-49)*

**F. Audit-trail logging schema mismatch — CIPH-26 (WS-04) — open release blocker**
CLI wiring landed 2026-09-10; Diana's 2026-09-18 verification found the CLI-emitted records **inconsistent with the defined schema**. She is holding the audit gate red until they match, because the mismatch undercuts the audit trail as release evidence.
*(SRC-CU-CIPH-26, SRC-MEET-10)*

---

## Top risks to escalate before ship

1. **The release gate has no credible close date.** CIPH-21 is Active on two named gates (T005 Docker slim-down/CVE, T029 Windows signing), *plus* the audit-log hold. On 2026-09-15 Alice explicitly directed that none be closed. One of the three (signing) is not solvable by engineering at all. **Escalate: the v1.0 date is unsupported by the current gate state.**
2. **Legal/distribution exposure from AGPL in the shipped dependency set.** Client agreements rule out copyleft in the core engine; two consecutive remediation attempts have failed, and no compliant parser has been identified. This is the highest-severity *unbounded* item — the search has no completion estimate.
3. **Two independent upstream libraries hold WS-01 hostage** (`pdfminer.six` #992 and `pdf-lib-core`), both with unresponsive maintainers and no ETA. Forking was already rejected once. **A ship-with-known-limitation vs. replace-the-renderer decision is overdue and has been deferred twice.**
4. **Code-signing certificate procurement needs executive action, not engineering.** It has sat without a timeline for ~6 weeks and blocks every pilot install.
5. **Compliance evidence is weaker than it looks.** Three artifacts carry explicit self-limiting caveats that should not be presented as certification: the offline batch sign-off is "preliminary… not a compliance certification" and carries an unresolved **45-second startup licence-check hang** (SRC-SLACK-33, SRC-CU-CIPH-37); the HIPAA pattern report confirms a regression check only and "is not a HIPAA compliance certification" (SRC-GDOC-34); telemetry opt-out is verified CLI-side only, with the **Sentry Electron crash-reporter path unaudited** (SRC-GDOC-51).
6. **Large-file reliability is unproven at scale.** CIPH-41's fix is unvalidated against the full corpus, and a 10,000-page re-merge stress test flagged as needed on 2026-08-14 has no recorded result (SRC-GDOC-25). Chunking also knowingly breaks regex matches spanning page boundaries — a **detection-correctness trade-off** that does not appear to have been escalated as such.
7. **Watch for premature closure.** Five items have already been called done and walked back. The pattern (Docker, licensing, chunking, quota, handshake) suggests acceptance criteria are being signed off on narrow happy-path evidence. Recommend no gate closes on a single-condition test.

---

**Scope note:** WS-01 (detection/engine), WS-02 (CLI/API interfaces), WS-03 (packaging, release, security) and WS-04 (compliance/policy) are the workstream labels used in the source records. REST API authentication (CIPH-19, WS-02) is **Deferred** to v1.1 by decision, not blocked — v1.0 scope is local-network-only, and that deferral was reconfirmed.
