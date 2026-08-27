# For closing the v1.0.0 release checklist as of **2026-09-22**, which dependency gates must go green first, and for each material gate name the listed task assignee versus who owns the immediate next action when those differ?

<!-- RESPONSE_START -->

I have everything needed. Here is the complete answer.

---

## Closing the v1.0.0 release checklist (T011 / CIPH-21) as of 2026-09-22

**T011 is Active under a security-gate hold, owned by Evan, with a hard no-ship date of 2026-10-15** if the two formal gates are not green (`work-states/WS-03-ops.md`; `med-synth/tasks/CIPH-21-Release-v1-Gates.md`; `work-states/comments/2026-09.md` → CMT-2026-09-002; `briefs/2026-09-22-daily-brief.md`).

### Gates already green (no action)
The original checklist dependency set was T001–T006 plus T010; six of seven were satisfied — T001 Core Engine, T002 Regex Detection, T003 Batch CLI, T004 REST API, T006 Policy Config, T010 Security Audit (`med-synth/documentation/sources/2026-07-12-Release-Checklist.md`; `work-states/WS-01-engine.md`; `work-states/WS-03-ops.md`). T010's external attestation (RedByte pen-test letter, 2026-07-11) is in the evidence pack (CMT-2026-07-002 via `work-states/WS-03-ops.md`).

### Gates that must go green first

**1. T005 / CIPH-15 — Docker image size + CVE verification (formal dependency, no-ship-linked)**
- Status: Active (Reopened) since 2026-06-25; image ballooned to 2.1GB, multi-stage + Alpine + package pruning applied, but as of the 2026-08-12 check it still exceeds the ~450MB target and CVE verification still fails (`med-synth/tasks/CIPH-15-Docker-Packaging.md`; `med-synth/communication/sources/slack/2026-06-25-docker-size.md`).
- Note the dual threshold: interim RC may ship at 800MB once CVE-clean; GA target stays ~450MB — do not conflate them on the checklist (CMT-2026-06-002, `work-states/comments/2026-06.md`).
- **Listed assignee: Evan.** **Immediate next action: also Evan** — trim the Python site-packages layer and chase down what trips the CVE scan. **But the gate does not flip on Evan's word:** Diana holds the reopened status and runs the size/CVE verification against the release checklist, so clearance is hers (`2026-06-25-docker-size.md`, 2026-08-12 entries).

**2. T029 / CIPH-39 — Windows Defender/SmartScreen code-signing (formal dependency, no-ship-linked)**
- Status: Active. Windows build artifact exists and backslash path handling is fixed; the block is the missing Authenticode code-signing certificate, so unsigned pilot installs get warned or blocked (`med-synth/tasks/CIPH-39-Windows-Compatibility.md`; `med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md`; `work-states/WS-06-platforms.md`).
- **Listed assignee: Evan. Immediate next action owner: Alice.** This is the sharpest divergence: Evan stated it "isn't something we can work around on the engineering side, we need the certificate," and Alice said she would chase the certificate process. WS-06 records it explicitly as "a procurement dependency, not an engineering block," with budget/procurement timeline sitting in Needs Manual Triage.

**3. T016 / CIPH-26 — Audit-trail log schema alignment (release blocker raised at the pre-release audit, not in the original T011 dependency list)**
- Status: Active. CLI-emitted audit records do not validate against the defined companion JSON schema; Diana's 2026-09-18 verification found the mismatch and it stands as an open release blocker. The 2026-09-15 pre-release audit listed it alongside Docker and Windows, with Alice's instruction to keep it visible as a release blocker (`med-synth/tasks/CIPH-26-Audit-Trail-Logging.md`; `med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md`; `work-states/WS-04-policy.md`).
- **Listed assignee: Diana. Immediate next action owner: Bob** — he did the loader refactor, SHA-256 hashing, schema definition, and 2026-09-10 CLI wiring, and has "another pass queued" on the record shape. Diana's role is the re-verification/clearance: she said she will keep the gate red until schema and records match.

**4. T031 / CIPH-41 — Large-file stream chunking memory leak (explicitly tied to the T011 gate by comment)**
- Status: Active (Reopened). Chunking merged, then reopened when files over 2GB still leaked; buffer-release refactor in flight. Bob's 2026-08-18 comment escalated it as a MedFirst pilot-blocker (OOM on a 4.7GB PDF with 8GB RAM) and tied it "explicitly to the T011 release gate" (CMT-2026-08-003, `work-states/comments/2026-08.md`; `med-synth/tasks/CIPH-41-Large-File-Chunking.md`; `work-states/WS-05-performance.md`; still listed as release-coupled in the 2026-09-22 brief).
- **Listed assignee: Charlie. Immediate next action: also Charlie** (stream buffer release refactor) — no divergence. Note the related T033/CIPH-43 loader-leak profiling (assignee Bob) is Completed; T031 is the open one.

**5. T006 legacy JSON→YAML policy migration (release dependency layered onto an otherwise-closed gate)**
- T006/CIPH-16 is Completed and shows on the checklist as met, but Alice's MedFirst call added a condition: three legacy JSON pilot policies must auto-migrate before production cutover, treated as "a release dependency tied to T006 and the T011 gate" (CMT-2026-06-001, `work-states/comments/2026-06.md`; `work-states/WS-01-engine.md`).
- **Listed assignee on CIPH-16: Charlie** (who implemented the YAML loader, 2026-06-22). **Immediate next action owner: Evan** — the comment assigns him the JSON→YAML converter. Divergence.

### Summary of assignee vs. next-action-owner divergences

| Gate | Listed task assignee | Immediate next action owner | Nature of the split |
|---|---|---|---|
| T005 Docker size/CVE | Evan | Evan (remediation); **Diana** for verification/clearance | Doer vs. verifier |
| T029 Windows signing | Evan | **Alice** | Engineering vs. procurement |
| T016 Audit-log schema | Diana | **Bob** | Owner/verifier vs. implementer |
| T031 Large-file chunking | Charlie | Charlie | None |
| T006 legacy JSON migration | Charlie | **Evan** | Original implementer vs. converter owner |

### Caveats worth flagging
- Only **T005 and T029** are the no-ship-linked gates in T011's own acceptance criteria and CMT-2026-09-002. T016, T031, and the T006 migration are release blockers/dependencies recorded elsewhere (pre-release audit and work-state comments) rather than lines in the original 2026-07-12 checklist — treat them as material but distinct in category.
- T007 (upstream `pdfminer.six` #992, Legal sign-off gate) and T036 (upstream High-DPI, plus the Form XObject subset) were named at the 2026-09-15 audit and in the index as open, but neither appears in T011's dependency list; T036 was described as a gate-check item that "stays on the board" rather than a T011 dependency (`work-states/WS-01-engine.md`, `work-states/WS-06-platforms.md`, `work-states/index.md`).
- T030 (AGPL/Legal P0) is a separate P0 in the priority order, not a listed T011 dependency (`work-states/WS-04-policy.md`; CMT-2026-08-002).
