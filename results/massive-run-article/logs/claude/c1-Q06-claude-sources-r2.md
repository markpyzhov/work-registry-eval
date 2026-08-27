# For closing the v1.0.0 release checklist as of **2026-09-22**, which dependency gates must go green first, and for each material gate name the listed task assignee versus who owns the immediate next action when those differ?

<!-- RESPONSE_START -->

## Answer

**Sources consulted (all `path: sources`, dataset `d13efb7c8a9a11f197db2303d7337e37`)**

SRC-CU-CIPH-21 (`med-synth/tasks/CIPH-21-Release-v1-Gates.md`), SRC-GDOC-05 (`.../2026-07-12-Release-Checklist.md`), SRC-CU-CIPH-15 (`.../CIPH-15-Docker-Packaging.md`), SRC-SLACK-06 (`.../2026-06-25-docker-size.md`), SRC-CU-CIPH-39 (`.../CIPH-39-Windows-Compatibility.md`), SRC-GDOC-39 (`.../2026-09-02-Windows-Compatibility-Audit-Report.md`), SRC-SLACK-37 (`.../2026-09-02-windows-signing-gap.md`), SRC-MEET-08 (`.../2026-08-15-Windows-License-Sync.md`), SRC-CU-CIPH-26 (`.../CIPH-26-Audit-Trail-Logging.md`), SRC-MEET-10 (`.../2026-09-15-Pre-Release-Audit.md`), SRC-CU-CIPH-46 (`.../CIPH-46-High-DPI-PDF-Rendering-Fixes.md`), SRC-GDOC-49 (`.../2026-09-10-High-DPI-PDF-Rendering-Coordinates-Report.md`), SRC-SLACK-58 (`.../2026-09-10-high-dpi-upstream-block.md`), SRC-CU-CIPH-40 (`.../CIPH-40-License-Compliance-Review.md`), SRC-CU-CIPH-17 (`.../CIPH-17-Fix-Offset-Mismatch.md`), SRC-SLACK-07 (`.../2026-06-26-blocked-on-upstream.md`).

The latest evidence in the dataset is dated 2026-09-18; nothing records a change between then and 2026-09-22, so the position below is the state carried into that date.

### The formal dependency list is already clear except one item

The release checklist (T011 / CIPH-21, **assignee Evan**) lists dependencies T001–T006 and T010. Per SRC-GDOC-05, T001 (Core Redaction Engine), T002 (Financial Regex Detection), T003 (Batch CLI), T004 (REST API Endpoints), T006 (Redaction Policy Config) and T010 (Security Audit) are all **Completed**. Only **T005 is unmet** on that original list. CIPH-21's acceptance criteria then add a second named gate, **T029**, which the later prerequisite audit surfaced.

### Material gates that must go green — listed assignee vs. owner of the immediate next action

**1. T005 — Docker image slim-down + CVE verification (CIPH-15, Active/Reopened)**
- Listed assignee: **Evan**.
- Immediate next action: **Evan** — trim the remaining bloat in the Python site-packages layer and chase down what is tripping the CVE scan (SRC-SLACK-06, 2026-08-12).
- Divergence to note: the *gate-flipping* action is not Evan's. **Diana** reopened the task on 2026-06-25 and owns the size/CVE re-verification; she stated the reopened status stands until both the size and CVE checks are clean and that she is tracking it against the release checklist. So the remediation is Evan's, the clearance is Diana's.

**2. T029 — Windows Defender/SmartScreen code-signing (CIPH-39, Active, High)**
- Listed assignee: **Evan**.
- Immediate next action owner: **Alice**. This is the sharpest divergence. Evan stated on 2026-09-02 that "this isn't something we can work around on the engineering side, we need the certificate," and Alice replied "I'll chase the certificate process" (SRC-SLACK-37). Alice had already told Evan on 2026-08-15 to keep chasing procurement, and Evan reported "no firm timeline yet" (SRC-MEET-08). SRC-GDOC-39 confirms the build itself is sound — packaging was cleared by the 2026-08-10 path fix and a working artifact existed by 2026-08-12 — so certificate procurement is the sole open blocker, and it sits with Alice/procurement, not with the task's engineering assignee.

**3. Audit-trail logging gate (CIPH-26, Active, High)**
- Listed assignee: **Diana**.
- Immediate next action owner: **Bob**. Diana's 2026-09-18 verification found the CLI-emitted audit records inconsistent with the defined JSON schema and recorded it as an open release blocker; at the 2026-09-15 pre-release audit she said she cannot clear the gate and will keep it red until schema and records match. Bob, who did the schema definition (2026-08-15) and CLI integration (2026-09-10), said he has "another pass queued" on the emitted record shape. So the task is assigned to the person holding the gate, while the work that unblocks it belongs to Bob.
- This gate is not on the original T001–T006/T010 dependency list, but Alice explicitly kept it "visible as a release blocker" alongside Docker and Windows at the 2026-09-15 gate check.

**4. High-DPI coordinate scaling (CIPH-46 / T036, Blocked)**
- Listed assignee: **Charlie**.
- Immediate next action owner: effectively **outside the team — the upstream `pdf-lib-core` maintainers**, who have not responded to Charlie's issue; the internal next action is a **decision owned by Alice** (with Diana), namely whether to ship with the limitation as a documented known issue or replace the rendering library. Charlie confirmed there is no local patch — the defect is deep in the library's C++ core (SRC-SLACK-58, 2026-09-10; SRC-GDOC-49). Alice listed this among the gates still open at the 2026-09-15 review, but Diana's position is that it affects only a small subset of complex documents and should be documented as a known issue — i.e., it is the one gate with a plausible ship-with-limitation path rather than a fix.

### Two further open items that bear on release but are not named checklist gates

- **CIPH-40, third-party license audit ("before release"), Active (Reopened), High** — listed assignee **Diana**, but the immediate next action is **Charlie's**: finding an Apache/MIT-licensed PDF parser after the replacement turned out to be AGPL (activity dated 2026-08-15; Alice told Charlie it was the priority). Another assignee/next-action split.
- **CIPH-17, multi-page coordinate/offset drift, Blocked** — assignee **Charlie**; blocked on unmerged upstream `pdfminer.six` PR #992. The team deliberately rejected forking, so there is no internal next action. Alice called this "a real risk for the v1.0 timeline" on 2026-09-10, but it is not listed as a checklist dependency.

### Summary table

| Gate | Status | Listed assignee | Owner of immediate next action | Split? |
|---|---|---|---|---|
| T005 Docker size/CVE (CIPH-15) | Active (Reopened) | Evan | Evan (remediation); Diana owns the verification that clears it | Partial |
| T029 Windows code-signing (CIPH-39) | Active | Evan | **Alice** (chasing certificate procurement) | **Yes** |
| Audit-trail logging (CIPH-26) | Active | Diana | **Bob** (next pass on CLI-emitted records) | **Yes** |
| High-DPI scaling (CIPH-46/T036) | Blocked | Charlie | Upstream maintainers; internally an **Alice/Diana** ship-or-swap decision | **Yes** |
| License audit (CIPH-40) | Active (Reopened) | Diana | **Charlie** (Apache/MIT parser search) | **Yes** |

**Bottom line:** the checklist cannot close until T005 and T029 clear (the two gates CIPH-21 names explicitly), and in practice also the audit-log mismatch, which Diana is holding red as of 2026-09-18. Of these, only T005's remediation sits with its listed assignee. T029 is assigned to Evan but its next action is Alice's procurement chase; the audit-log gate is assigned to Diana but its next action is Bob's; and the license audit is assigned to Diana but its next action is Charlie's.
