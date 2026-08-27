# As of the final CipherDoc snapshot on **2026-09-22**, is the toolkit ready to ship v1.0.0? Give a clear go/no-go, name every release gate that is still open, and cite the evidence that keeps each gate from closing.

<!-- RESPONSE_START -->

I have enough evidence to answer definitively.

---

## NO-GO — CipherDoc is not ready to ship v1.0.0 as of 2026-09-22

The release gate task **T011 / CIPH-21 "Release v1.0 Gates"** is still **Active** and sits under an explicit **security-gate hold placed by Diana**. WS-03 (Packaging, Release gating, and Security) is `in_progress`, P0, owner Evan, last updated 2026-09-22, and its blocker section states plainly: *"T011 cannot close until T005 (Docker size/CVE) and T029 (Windows code-signing certificate) are green."* The 2026-09-15 pre-release audit closed with Alice's statement that security-gate work stays open and "No one closes those today," and Evan's "Release isn't opening with any of those unresolved."

There is also a hard deadline attached: the release board set a **no-ship after 2026-10-15** if T005 and T029 are not green (`CMT-2026-09-002`).

### Gates still open

**1. T005 / CIPH-15 — Docker image size and CVE verification** (hard gate on T011)
- CIPH-15 status: **Active (Reopened)**. Initially completed ~800MB, reopened 2026-06-25 after Diana's size/CVE review measured the built image at **2.1GB** once OCR dependencies were bundled.
- Evan implemented multi-stage builds and swapped the base to Alpine, but as of the **2026-08-12 size/CVE verification the image still exceeds the ~450MB target and CVE verification remains outstanding**. Both acceptance criteria are marked "not yet met."
- Dual thresholds are in play (`CMT-2026-06-002`): CISO review defines an interim RC at 800MB once CVE-clean; GA remains ~450MB. Neither is currently satisfied.
- The July 12 Release Checklist (DOC-2005, SRC-GDOC-05) already named T005 as the sole unmet dependency of seven: *"This checklist cannot close until that gate clears."*

**2. T029 / CIPH-39 — Windows code-signing certificate** (hard gate on T011)
- CIPH-39 status: **Active**. Windows backslash path handling was fixed 2026-08-10 and a Windows build artifact was produced by 2026-08-12 — packaging is no longer the blocker.
- The produced artifact is **unsigned**, triggering SmartScreen warnings and Defender flagging it as untrusted. The Windows Compatibility Audit (DOC-2039, 2026-09-02) records the root cause as *"No code-signing certificate has been procured or configured in the Windows build pipeline yet,"* and notes site IT policies commonly block unsigned binaries outright.
- Slack #releases, 2026-09-02: Evan — *"this isn't something we can work around on the engineering side, we need the certificate."* Alice kept it open on the release gate and took the certificate chase. This is a **procurement dependency, not an engineering block**; WS-06 lists "Budget and procurement timeline for Windows Authenticode code-signing certificate" under Needs Manual Triage.

**3. T016 / CIPH-26 — Compliance audit-trail log schema alignment** (QA release hold)
- CIPH-26 status: **Active**, assignee Diana, priority High. Bob wired audit-log generation into the CLI on 2026-09-10, but Diana's **2026-09-18 verification pass found the CLI-emitted audit records inconsistent with the defined companion JSON schema**; the record states this "remains an open release blocker."
- At the 2026-09-15 pre-release audit Diana said the mismatch *"undercuts the audit trail as release evidence"* and committed to keeping the audit-log gate **red until schema and records match**. Alice explicitly kept it visible as a release blocker alongside the two WS-03 gates.

**4. T036 / CIPH-46 — High-DPI PDF coordinate scaling** (on the gate board, unresolved)
- CIPH-46 status: **Blocked**. Traced to a defect in the upstream `pdf-lib-core` rendering library's coordinate handling for nested Form XObjects under a parent transform; Charlie confirmed there is no local patch ("It's deep in their C++ core"), and the upstream maintainers have not responded.
- Impact: redaction coordinates drift 5–10 pixels on 4K displays at 200% scaling; offline QA found **12% of the MedFirst pilot corpus fails** due to nested Form XObjects, beyond the upstream 4K scaling issue alone (`CMT-2026-09-001`).
- Alice listed it in the 2026-09-15 gate check as still open and left it blocked pending a decision on whether to ship with the limitation as a documented known issue or replace the rendering library. **That ship/no-ship decision has not been recorded as made.**

### Pre-release items that are not yet clean (would compromise the release even though not named in the CIPH-21 acceptance criteria)

**5. T030 / CIPH-40 — Third-party license compliance review**
- Status: **Active (Reopened)**, priority High. The task exists precisely to clear licenses "before release." The PDF parser swapped in on 2026-08-11 to clear the original finding turned out to be **AGPL-licensed** — Alice: *"AGPL is a dealbreaker for how we distribute this."* Reopened 2026-08-12; as of 2026-08-15 Charlie was still searching for an Apache/MIT alternative and none covered the required parsing. The license inventory report (DOC-2024) states flatly: *"This report does not certify overall license compliance. The parser-license question remains open."* WS-04 lists finding a viable non-AGPL parser under Needs Manual Triage.

**6. T007 / CIPH-17 — Multi-page coordinate/offset drift** (correctness risk carried into release)
- Status: **Blocked** on upstream `pdfminer.six` PR #992, still unmerged as of 2026-09-10. A local fork was evaluated and rejected as unmaintainable. A maintainer DM indicates #992 lands mid-October at the earliest, and any pre-normalization workaround requires **written Legal sign-off in addition to the upstream merge** (`CMT-2026-06-003`). Alice on 2026-09-10: *"This is becoming a real risk for the v1.0 timeline."*

### What is green

For fairness to the release board: the CIPH-21 checklist dependencies **T001–T006 and T010 are satisfied** (those tasks are Completed) — except that T005 itself sits in that range and is the reopened item. T010 / CIPH-20 security scans are complete: the medium-severity CORS `*` origin finding from the July 6 scan was patched to configured `ALLOWED_ORIGINS`, and July 15 re-scans confirmed the patch holds, supplemented by a RedByte pen-test attestation letter dated 2026-07-11 in the evidence pack (`CMT-2026-07-002`). REST API authentication (T009 / CIPH-19) is a **deliberate deferral to v1.1**, not an open gate — v1.0.0 assumes a trusted local network, rechecked and confirmed by Alice on 2026-08-20. (Note the downstream commitment: MedFirst IT renewal requires REST authentication no later than 2026-03-31, per `CMT-2026-07-001`.)

### Bottom line

Four gates are open on the release board (Docker size/CVE, Windows code-signing, audit-log schema, high-DPI rendering), two of which are formal blocking dependencies of CIPH-21 and one of which is a QA hold Diana refuses to clear. Two further pre-release obligations — license compliance certification and the blocked offset-drift fix — are also unresolved. Nothing in the dataset records any of these being cleared, waived, or superseded on or before 2026-09-22. **v1.0.0 cannot ship.**

**Records cited:** `work-states/WS-03-ops.md`, `work-states/WS-04-policy.md`, `work-states/WS-06-platforms.md`, `work-states/WS-01-engine.md`, `work-states/index.md`, `work-states/comments/2026-09.md`; sources `SRC-CU-CIPH-21`, `SRC-CU-CIPH-15`, `SRC-CU-CIPH-39`, `SRC-CU-CIPH-26`, `SRC-CU-CIPH-46`, `SRC-CU-CIPH-40`, `SRC-CU-CIPH-17`, `SRC-GDOC-05` (DOC-2005), `SRC-GDOC-39` (DOC-2039), `SRC-GDOC-24`, `SRC-GDOC-49`, `SRC-MEET-10`, `SRC-SLACK-37`, `SRC-SLACK-58`, `SRC-SLACK-40`, `SRC-SLACK-07`, `SRC-SLACK-08`; comments `CMT-2026-06-002`, `CMT-2026-06-003`, `CMT-2026-09-001`, `CMT-2026-09-002`, `CMT-2026-07-001`, `CMT-2026-07-002`.
