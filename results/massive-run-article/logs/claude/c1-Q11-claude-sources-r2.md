# On the critical path to clearing the security-gate hold, what are the next actions as of **2026-09-22**, and who owns each next action (not merely the listed task assignee if those differ)?

<!-- RESPONSE_START -->

## Answer

**As of 2026-09-22, the security-gate hold is still in force and nothing on its critical path has closed.**

The hold itself: Diana placed a security-gate hold on the CipherDoc v1.0 release (CIPH-21 / T011 "Release v1.0 Gates", Status Active, assignee Evan) pending two gates — T005 Docker image slim-down/CVE work and T029 Windows Defender/SmartScreen code-signing. All other checklist dependencies (T001–T006 except T005, plus T010) are Completed [SRC-CU-CIPH-21; SRC-GDOC-05 / DOC-2005]. At the 2026-09-15 pre-release audit Alice confirmed "Security-gate work stays open — Docker slim-down, Windows signing," and added the audit-log schema mismatch as a third item kept visible as a release blocker [SRC-MEET-10].

### Critical path 1 — T005 / CIPH-15 Docker image (size + CVE)
Status: Active (Reopened) since 2026-06-25; at the 2026-08-12 verification the image was still over the ~450MB target and CVE verification was still failing [SRC-CU-CIPH-15; SRC-SLACK-06].

- **Next action (engineering):** strip the remaining bloat in the Python site-packages layer to reach ~450MB, and chase down what is tripping the CVE scan. **Owner: Evan** — this matches the task assignee, and Evan committed to it himself on 2026-08-12 ("There's still fluff in the Python site-packages layer, and I need to chase down what's tripping the CVE scan") [SRC-SLACK-06].
- **Next action (verification):** re-run the size check and the CVE scan; the Reopened status stands until both are clean. **Owner: Diana**, not the task assignee — she runs the size/CVE verification and said "Reopened status stands until both the size and the CVE check are clean. I'll keep tracking it against the release checklist" [SRC-SLACK-06; SRC-CU-CIPH-15].

### Critical path 2 — T029 / CIPH-39 Windows code-signing
Status: Active, High priority, assignee Evan. The Windows build artifact exists and runs (packaging was unblocked by the 2026-08-10 path fix, artifact produced 2026-08-12); the sole open blocker is that no code-signing certificate has been procured or configured [SRC-CU-CIPH-39; SRC-GDOC-39 / DOC-2039; SRC-SLACK-38].

- **Next action (the actual gating step):** procure the code-signing certificate through the procurement process. **Owner: Alice, not the task assignee.** On 2026-09-02 Alice took this over explicitly: "Let's keep it open on the release gate rather than pushing it off the board. I'll chase the certificate process" [SRC-SLACK-37]. (Earlier, on 2026-08-15, Alice had told Evan to "keep chasing procurement on the cert," with Evan reporting "no firm timeline yet" [SRC-MEET-08]; the 2026-09-02 exchange is the later and controlling assignment.) Evan is explicit that this cannot be worked around on the engineering side: "we need the certificate" [SRC-SLACK-37].
- **Next action once the certificate exists:** wire signing into the release build step / Windows build pipeline and produce a signed artifact. **Owner: Evan** (task assignee and audit owner) [SRC-GDOC-39].
- **Acceptance/verification:** signed build must pass Defender/SmartScreen without warnings before T029 clears — and only then does T011 clear on this item [SRC-CU-CIPH-39; SRC-GDOC-39].

### Critical path 3 — audit-log gate (CIPH-26 / Audit Trail Logging)
Not one of the two originally named gates, but Alice folded it into the open security-gate work on 2026-09-15 and it is an open release blocker as of 2026-09-18 — so it sits on the same critical path to opening the release. Task Status Active, High priority, **assignee Diana** [SRC-CU-CIPH-26; SRC-MEET-10].

- **Next action:** another pass on the CLI audit-log emission so the emitted records validate against the defined companion JSON schema. **Owner: Bob, not the task assignee** — Bob did the 2026-09-10 CLI integration and stated on 2026-09-15 "The shape coming out still isn't consistent with what the schema expects — I've got another pass queued" [SRC-MEET-10; SRC-CU-CIPH-26 activity history].
- **Next action (verification/clearance):** re-verify records against schema and clear the audit gate. **Owner: Diana** — her 2026-09-18 verification found the CLI-emitted records inconsistent with the schema, and she stated "I'll keep the audit-log gate red until schema and records match" [SRC-CU-CIPH-26 activity history, 2026-09-18; SRC-MEET-10].

### Final step on the path
- **Close out the T011/CIPH-21 release checklist** once T005 and T029 clear. **Owner: Evan** (task assignee and owner of the release-checklist document DOC-2005) [SRC-CU-CIPH-21; SRC-GDOC-05].
- **Lift the security-gate hold.** **Owner: Diana** — she placed the hold and is the only party the sources show clearing security gates [SRC-CU-CIPH-21; SRC-MEET-10].

### Where owner ≠ listed assignee (direct answer to the second half of the question)
| Next action | Listed task assignee | Actual owner of the next action |
|---|---|---|
| Procure Windows code-signing certificate | Evan (CIPH-39) | **Alice** (took over chasing procurement, 2026-09-02) |
| Fix CLI-emitted audit records to match schema | Diana (CIPH-26) | **Bob** (has the next pass queued) |
| Re-run Docker size/CVE verification | Evan (CIPH-15) | **Diana** (runs and gates the verification) |
| Docker image slim-down / CVE root-cause | Evan (CIPH-15) | Evan (same) |
| Wire signing into the release build | Evan (CIPH-39) | Evan (same) |

### Caveats
- The dataset contains no source dated 2026-09-19 through 2026-09-22. The most recent relevant records are the 2026-09-15 pre-release audit [SRC-MEET-10] and Diana's 2026-09-18 audit-verify mismatch entry [SRC-CU-CIPH-26]; the answer above is the state carried forward from those.
- No source gives a timeline or expected date for the code-signing certificate ("No firm timeline yet" — Evan, 2026-08-15) [SRC-MEET-08].
- The 2026-09-15 meeting also lists an upstream high-DPI rendering bug as open, but it is tracked as a separate release-board item, not part of the security-gate hold [SRC-MEET-10].

### Sources cited
- `med-synth/tasks/CIPH-21-Release-v1-Gates.md` (SRC-CU-CIPH-21)
- `med-synth/tasks/CIPH-15-Docker-Packaging.md` (SRC-CU-CIPH-15)
- `med-synth/tasks/CIPH-39-Windows-Compatibility.md` (SRC-CU-CIPH-39)
- `med-synth/tasks/CIPH-26-Audit-Trail-Logging.md` (SRC-CU-CIPH-26)
- `med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md` (SRC-MEET-10)
- `med-synth/communication/sources/fireflies/2026-08-15-Windows-License-Sync.md` (SRC-MEET-08)
- `med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md` (SRC-SLACK-37)
- `med-synth/communication/sources/slack/2026-06-25-docker-size.md` (SRC-SLACK-06)
- `med-synth/communication/sources/slack/2026-08-12-windows-build-artifact.md` (SRC-SLACK-38)
- `med-synth/documentation/sources/2026-09-02-Windows-Compatibility-Audit-Report.md` (SRC-GDOC-39 / DOC-2039)
- `med-synth/documentation/sources/2026-07-12-Release-Checklist.md` (SRC-GDOC-05 / DOC-2005)
