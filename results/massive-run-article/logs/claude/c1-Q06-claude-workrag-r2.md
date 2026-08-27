# For closing the v1.0.0 release checklist as of **2026-09-22**, which dependency gates must go green first, and for each material gate name the listed task assignee versus who owns the immediate next action when those differ?

<!-- RESPONSE_START -->

## Answer

### The gates that must go green before the v1.0.0 release checklist (T011 / CIPH-21) can close, as of 2026-09-22

**Authoritative position (WS-03 work state, last updated 2026-09-22):** T011 cannot close until **two** gates are green:

| Gate | What must clear |
|---|---|
| **T005 / CIPH-15 — Docker packaging** | Image size *and* CVE verification. Dual thresholds apply: interim RC may ship at **800 MB once CVE-clean**, GA target remains **~450 MB** — the two must not be conflated (CMT-2026-06-002). As of the 2026-08-12 check the image still exceeds ~450 MB and CVE verification is still failing. |
| **T029 / CIPH-39 — Windows code-signing** | An Authenticode code-signing certificate must be procured and wired into the release build step so Defender/SmartScreen stop flagging the binary. Packaging itself is already clear — the Windows backslash path defects were fixed 2026-08-10 and a build artifact was produced 2026-08-12. |

The **original checklist dependency set (T001–T006 and T010) is fully satisfied** — all of those are Completed (T001 06-05, T002 06-08, T003 06-12, T004 06-17, T006 06-22, T010 07-10). The July 12 draft checklist that says "T005 is the only unmet dependency" is a stale snapshot; T029 was added later as a gate.

**Hard deadline:** the release board set a no-ship after **2026-10-15** if T005 and T029 are not green — recorded as a hard, not advisory, deadline (CMT-2026-09-002, Diana, 2026-09-15).

**Also held open against the release, though not a formal T011 dependency in the work state:** the **T016 / CIPH-26 audit-log gate**. The 2026-09-15 pre-release audit listed Docker slim/CVE, Windows signing, **and** audit-log schema alignment as open blockers, and Diana's 2026-09-18 verification found CLI-emitted records still inconsistent with the defined schema.

### Listed assignee vs. owner of the immediate next action

| Gate | Listed task assignee | Owner of the immediate next action | Divergence |
|---|---|---|---|
| **T005 / CIPH-15** (Docker size/CVE) | **Evan** | **Evan** for remediation (trim the remaining Python site-packages layer, chase down what trips the CVE scan) — but **Diana** owns the verification that clears it; she re-ran the size/CVE check on 08-12 and stated the Reopened status stands until both checks are clean, tracking it against the release checklist. | Partial: execution Evan, clearance Diana |
| **T029 / CIPH-39** (Windows signing) | **Evan** | **Alice** — on 2026-09-02 she said she would chase the certificate process. Evan explicitly stated this is not workable on the engineering side ("we need the certificate"), and WS-06 classifies it as a **procurement dependency, not an engineering block**. WS-06 also carries an unassigned Needs-Manual-Triage item: *budget and procurement timeline for the Windows Authenticode certificate*. | **Yes — the clearest split.** Task sits with Evan; the action that actually unblocks it sits with Alice/procurement. |
| **T016 / CIPH-26** (audit-log schema, release hold) | **Diana** | **Bob** — he wired audit-log generation into the CLI on 09-10 and has "another pass queued" to make emitted records match the schema. Diana keeps the gate red and owns the clearance decision. | **Yes** — assignee Diana, next action Bob. |
| **T011 / CIPH-21** (the checklist itself) | **Evan** | **Diana** holds the security-gate hold on the release and the release board owns the 10-15 no-ship call; Alice ruled at the 09-15 audit that no one closes those gates. Evan cannot close his own task until the two upstream gates clear. | **Yes** — owner Evan, gate authority Diana/release board |
| **T006 / CIPH-16 rider** (legacy JSON→YAML migration) | **Charlie** (CIPH-16, Completed 06-22) | **Evan** — CMT-2026-06-001 records that Evan owns the JSON→YAML converter and that auto-migration of MedFirst's three legacy JSON policies is a release dependency tied to T006 **and the T011 gate**. | **Yes** — the task is closed under Charlie, but a live release-tied obligation sits with Evan |

One further comment-only tie worth flagging: CMT-2026-08-003 (Bob, 2026-08-18) instructs that **T031** (large-file memory leak; MedFirst OOM on a 4.7 GB PDF with 8 GB RAM) be prioritized and **tied explicitly to the T011 release gate** as a pilot blocker. It is not listed in the WS-03 Blockers section as a T011 dependency, so treat it as an escalation attached by comment rather than a formal gate.

### Records cited
- `work-states/WS-03-ops.md` (work-state; Blockers and Dependencies, Active Work, Done/Evidence) — authoritative as of 2026-09-22
- `work-states/WS-06-platforms.md` (work-state; T029 Active Work, Needs Manual Triage)
- `work-states/WS-04-policy.md` (work-state; T016 Active Work)
- `work-states/WS-01-engine.md` (work-state; T006 legacy JSON migration)
- `work-states/index.md` (as-of 2026-09-22T12:00:00Z)
- Comments: CMT-2026-06-001, CMT-2026-06-002, CMT-2026-08-003, CMT-2026-09-002
- Sources: SRC-CU-CIPH-21, SRC-CU-CIPH-15, SRC-CU-CIPH-39, SRC-CU-CIPH-26, SRC-CU-CIPH-16, SRC-GDOC-05, SRC-GDOC-39, SRC-SLACK-06, SRC-SLACK-37, SRC-MEET-10, SRC-MEET-08
