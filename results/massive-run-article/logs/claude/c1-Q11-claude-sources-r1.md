# On the critical path to clearing the security-gate hold, what are the next actions as of **2026-09-22**, and who owns each next action (not merely the listed task assignee if those differ)?

<!-- RESPONSE_START -->

## Answer

**What the hold is.** Per ClickUp CIPH-21 "Release v1.0 Gates" (SRC-CU-CIPH-21, Status: Active, Assignee: Evan), **Diana placed a security-gate hold on the CipherDoc v1.0 release**, pending two gates: **T005** (Docker image slim-down / CVE work, tracked as CIPH-15) and **T029** (Windows Defender/SmartScreen code-signing, tracked as CIPH-39). At the 2026-09-15 pre-release audit (SRC-MEET-10) Alice restated that "security-gate work stays open — Docker slim-down, Windows signing," and additionally kept the **audit-log schema mismatch** (CIPH-26/T026) visible as a release blocker in the same breath. So the critical path as of 2026-09-22 has two mandatory gate branches plus the audit-log blocker that is grouped with them.

### Branch 1 — T029 Windows code-signing (CIPH-39, task assignee: Evan)

The Windows build itself is done: the backslash path fix landed 2026-08-10 and a runnable artifact was produced 2026-08-12 (SRC-SLACK-36, SRC-SLACK-38, SRC-GDOC-23). Per the compatibility audit (SRC-GDOC-39, 2026-09-02), "procuring a code-signing certificate and wiring signing into the release build step is the only remaining item."

1. **Procure the code-signing certificate — owner: Alice (PM), not Evan.** Evan stated on 2026-09-02 that "this isn't something we can work around on the engineering side, we need the certificate," and Alice replied "I'll chase the certificate process" (SRC-SLACK-37). This is a handoff: on 2026-08-15 Alice had told Evan to "keep chasing procurement on the cert" (SRC-MEET-08), and Evan reported "no firm timeline yet." The 09-02 thread supersedes that, putting procurement with Alice. The listed assignee on CIPH-39 remains Evan.
2. **Wire signing into the Windows release build step and re-verify against Defender/SmartScreen — owner: Evan (DevOps).** This is gated on step 1 and cannot start until the certificate exists. Acceptance criteria on CIPH-39: build code-signed with a valid certificate and passing Defender/SmartScreen without warnings (SRC-CU-CIPH-39).

### Branch 2 — T005 Docker slim-down / CVE (CIPH-15, task assignee: Evan)

Status is Active (Reopened); at Diana's 2026-08-12 verification the image was still over the ~450MB target and CVE verification was still failing, after a multi-stage rebuild, an Alpine base swap, and removal of unused OCR/runtime packages (SRC-SLACK-06, SRC-CU-CIPH-15).

3. **Strip the remaining bloat from the Python site-packages layer to get under ~450MB, and diagnose what is tripping the CVE scan — owner: Evan.** These are his own stated next steps from 2026-08-12: "There's still fluff in the Python site-packages layer, and I need to chase down what's tripping the CVE scan" (SRC-SLACK-06). Owner and assignee coincide here.
4. **Re-run the size check and CVE scan and clear the gate — owner: Diana (QA), not Evan.** Diana is the one who runs the size/CVE verification and controls the reopened status: "Reopened status stands until both the size and the CVE check are clean. I'll keep tracking it against the release checklist" (SRC-SLACK-06). Both acceptance criteria must pass before the task leaves Active (Reopened).

### Branch 3 — Audit-log gate (CIPH-26, task assignee: Diana)

Grouped with the security-gate work at the 2026-09-15 review and the most recently updated item in the dataset.

5. **Another pass on CLI audit-log emission so records match the defined JSON schema — owner: Bob (Backend), not Diana.** CIPH-26's listed assignee is Diana, but Bob is the one doing the work: he wired audit-log generation into the CLI on 2026-09-10 and said on 2026-09-15 "the shape coming out still isn't consistent with what the schema expects — I've got another pass queued" (SRC-MEET-10, SRC-CU-CIPH-26).
6. **Re-verify the CLI-emitted records against the schema and clear the audit gate — owner: Diana.** Her 2026-09-18 verification found the emitted records still inconsistent with the schema, and it "remains an open release blocker"; she stated "I'll keep the audit-log gate red until schema and records match" (SRC-CU-CIPH-26 activity history, SRC-MEET-10).

### Branch 4 — Closing out

7. **Close the T011/CIPH-21 release checklist once T005 and T029 clear — owner: Evan** (assignee of CIPH-21 and owner of the release-checklist doc DOC-2005, SRC-GDOC-05).
8. **Lift the security-gate hold — owner: Diana.** She placed it and is the only one who clears the underlying QA/security verifications (SRC-CU-CIPH-21).

### Where owner ≠ listed task assignee

| Next action | Task / listed assignee | Actual owner of the next action |
|---|---|---|
| Procure code-signing certificate | CIPH-39 / Evan | **Alice** (took it over 2026-09-02) |
| Re-run Docker size + CVE verification | CIPH-15 / Evan | **Diana** |
| Fix CLI audit-record emission to match schema | CIPH-26 / Diana | **Bob** |
| Lift the security-gate hold | CIPH-21 / Evan | **Diana** |

### Sequencing and caveats

The certificate procurement (Alice) is the longest pole and the only item with no owner inside engineering — Evan flagged "no firm timeline" on 2026-08-15 and no source in the dataset records the certificate arriving. Branch 2 (Evan's image trimming) can proceed in parallel. Nothing in the dataset is dated after **2026-09-18** (Diana's audit-verify mismatch), so all of the above is the state carried into 2026-09-22; no source shows any of the three gates clearing. Separately, the 2026-09-15 review also lists an upstream high-DPI rendering bug as open, but it is not part of the security-gate hold.

**Sources cited:** SRC-CU-CIPH-21, SRC-CU-CIPH-15, SRC-CU-CIPH-39, SRC-CU-CIPH-26, SRC-MEET-10 (2026-09-15 Pre-Release Audit), SRC-MEET-08 (2026-08-15 Windows & License Sync), SRC-SLACK-37 (2026-09-02 Windows Signing Gap), SRC-SLACK-06 (Docker Image Size Optimization), SRC-SLACK-38 (2026-08-12 Windows Build Artifact), SRC-SLACK-36 (2026-08-10 Windows Path Handling), SRC-GDOC-39 (DOC-2039), SRC-GDOC-05 (DOC-2005), SRC-GDOC-23 (DOC-2023).
