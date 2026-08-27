# On the critical path to clearing the security-gate hold, what are the next actions as of **2026-09-22**, and who owns each next action (not merely the listed task assignee if those differ)?

<!-- RESPONSE_START -->

## Answer

**As of 2026-09-22, the security-gate hold is Diana's hold on the v1.0 release gates task (CIPH-21 / T011), and it is pending exactly two gates: T005 Docker image slim-down + CVE, and T029 Windows Defender/SmartScreen code-signing** (SRC-CU-CIPH-21). A third item, the audit-log schema mismatch, was explicitly kept "visible as a release blocker" alongside the security-gate work at the 2026-09-15 pre-release audit and is still failing verification as of 2026-09-18, so it sits on the same critical path to actually opening the release.

### Critical path 1 — T005 / CIPH-15 Docker image slim-down + CVE (task assignee: Evan)

Last verification: 2026-08-12, Diana checked size and ran the CVE scan — still over the ~450MB target and CVE verification still failing (SRC-SLACK-06, SRC-CU-CIPH-15).

- **Next action A:** strip the remaining "fluff" in the Python site-packages layer to get under the ~450MB target. **Owner: Evan** (he stated it himself on 2026-08-12; multi-stage build, Alpine base swap and OCR/runtime package removal have already been tried and did not close the gap).
- **Next action B:** chase down what is tripping the CVE scan and fix it. **Owner: Evan** (same message).
- **Next action C:** re-run the size check and CVE scan and clear or hold the gate. **Owner: Diana** — this is the ownership that diverges from the task assignee. CIPH-15 is assigned to Evan, but Diana is the one who reopened it, holds the verification, and said "Reopened status stands until both the size and the CVE check are clean. I'll keep tracking it against the release checklist" (SRC-SLACK-06).

### Critical path 2 — T029 / CIPH-39 Windows code-signing (task assignee: Evan)

Windows packaging is done — the path fix landed 2026-08-10 and a working, sanity-checked build artifact existed by 2026-08-12. The sole open blocker is the missing code-signing certificate (SRC-GDOC-39, SRC-SLACK-38, SRC-SLACK-37).

- **Next action A:** procure the code-signing certificate through the procurement process. **Owner: Alice**, not the task assignee. Evan stated on 2026-09-02 that "this isn't something we can work around on the engineering side, we need the certificate," and Alice closed the thread with "I'll chase the certificate process" (SRC-SLACK-37). Note the ownership shifted: at the 2026-08-15 sync Alice had told Evan to "keep chasing procurement on the cert" (SRC-MEET-08); the later 2026-09-02 exchange has Alice taking it. No firm timeline has ever been given.
- **Next action B:** once the certificate exists, wire signing into the Windows release build step and produce a signed artifact. **Owner: Evan** (DevOps/pipeline owner; SRC-GDOC-39 names "procuring a code-signing certificate and wiring signing into the release build step" as the only remaining items).
- **Next action C:** confirm the signed build passes Defender/SmartScreen without warnings — the acceptance criterion on CIPH-39 (SRC-CU-CIPH-39).

### Critical path 3 — Audit-log gate / CIPH-26 (task assignee: Diana)

- **Next action A:** the queued rework pass on the CLI audit-log emission so the records the CLI emits validate against the defined companion JSON schema. **Owner: Bob**, not the task assignee. CIPH-26 is assigned to Diana, but Bob did the schema definition (2026-08-15) and CLI integration (2026-09-10) and said on 2026-09-15 "the shape coming out still isn't consistent with what the schema expects — I've got another pass queued" (SRC-MEET-10, SRC-CU-CIPH-26).
- **Next action B:** re-run audit verification and clear the gate once schema and records match. **Owner: Diana** — "Until those match, I can't clear the audit gate… I'll keep the audit-log gate red until schema and records match." Her 2026-09-18 verification pass found the mismatch still present (SRC-CU-CIPH-26 activity history).

### Final step — clearing the hold itself

- **Next action:** lift the security-gate hold and close the T011 release checklist once T005 and T029 clear. **Owner: Diana** for lifting the hold (she placed it and owns the QA/security sign-off), with **Evan** as the CIPH-21 assignee who closes out the checklist document (SRC-CU-CIPH-21, SRC-GDOC-05, SRC-GDOC-39). Alice, as PM, is the one who ruled on 2026-09-15 that none of these close until resolved.

### Ownership vs. assignee summary

| Gate | Task assignee | Next action | Actual next-action owner |
|---|---|---|---|
| T005 Docker size/CVE (CIPH-15) | Evan | Trim site-packages layer; fix CVE-scan trigger | Evan |
| T005 verification | Evan | Re-run size + CVE scan, clear/hold | **Diana** |
| T029 Windows signing (CIPH-39) | Evan | Procure code-signing certificate | **Alice** |
| T029 signing (CIPH-39) | Evan | Wire signing into release build once cert lands | Evan |
| Audit-log (CIPH-26) | Diana | Rework CLI emission to match schema | **Bob** |
| Audit-log (CIPH-26) | Diana | Re-verify records vs. schema, clear gate | Diana |
| Release gates (CIPH-21) | Evan | Lift security-gate hold once both clear | **Diana** |

### Not on this critical path

The high-DPI rendering bug (blocked on an unresponsive upstream `pdf-lib-core` issue) and the AGPL PDF-parser license item (Charlie searching for an Apache/MIT alternative) are open release-board items but are not part of Diana's security-gate hold. The pdfminer.six offset fix is likewise blocked pending upstream PR #992, with Charlie having decided against forking.

### Caveat

The dataset contains no source records dated between 2026-09-19 and 2026-09-22. The latest evidence points are the 2026-09-15 pre-release audit transcript and Diana's 2026-09-18 audit-verify mismatch entry; the above reflects the state as carried forward from those.

**Sources cited:** SRC-CU-CIPH-21 (CIPH-21 Release v1.0 Gates), SRC-CU-CIPH-15 (CIPH-15 Docker Packaging), SRC-CU-CIPH-39 (CIPH-39 Windows Compatibility), SRC-CU-CIPH-26 (CIPH-26 Audit Trail Logging), SRC-MEET-10 (2026-09-15 Pre-Release Audit), SRC-MEET-08 (2026-08-15 Windows & License Sync), SRC-SLACK-37 (2026-09-02 Windows Signing Gap), SRC-SLACK-38 (2026-08-12 Windows Build Artifact), SRC-SLACK-06 (2026-06-25→2026-08-12 Docker Image Size Optimization), SRC-GDOC-39 (DOC-2039 Windows Build Signing Gap audit), SRC-GDOC-05 (DOC-2005 Release Checklist).
