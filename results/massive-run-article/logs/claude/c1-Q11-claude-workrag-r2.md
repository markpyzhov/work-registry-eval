# On the critical path to clearing the security-gate hold, what are the next actions as of **2026-09-22**, and who owns each next action (not merely the listed task assignee if those differ)?

<!-- RESPONSE_START -->

## Critical path to clearing the security-gate hold — next actions and owners (as of 2026-09-22)

**Context.** The hold sits on **T011 / CIPH-21 "Release v1.0 Gates"** (WS-03, ClickUp assignee **Evan**). **Diana** placed the security-gate hold, and per the work state T011 **cannot close until T005 (Docker size/CVE) and T029 (Windows code-signing) are green**. The 2026-09-15 pre-release audit adds a third open item kept visible as a release blocker: **audit-log schema alignment (T016 / CIPH-26)**. A hard **no-ship after 2026-10-15** applies if T005 and T029 are not green (CMT-2026-09-002, authored by Diana).

### 1. T005 / CIPH-15 — Docker image slim-down + CVE clearance
- **Next action (engineering):** strip the remaining bloat out of the Python site-packages layer and track down what is tripping the CVE scan. **Owner: Evan** — also the task assignee (stated by Evan himself on 2026-08-12, SRC-SLACK-06). Multi-stage build, Alpine base swap and OCR/runtime package removal are already done but insufficient.
- **Next action (verification/gate):** re-run the size check and CVE scan and decide whether the reopened status lifts. **Owner: Diana**, *not* the assignee Evan — she reopened the task on 2026-06-25, ran the failing 2026-08-12 verification, and stated the reopened status stands until both size and CVE are clean (SRC-SLACK-06, SRC-CU-CIPH-15).
- **Constraint on what "green" means:** dual thresholds must be tracked separately — interim RC may ship at **800MB once CVE-clean**, GA target remains **~450MB** (CMT-2026-06-002, CISO review, logged by Evan). Do not conflate them on the release checklist.

### 2. T029 / CIPH-39 — Windows Defender/SmartScreen code-signing
- **Next action (the actual blocker):** chase the **Authenticode code-signing certificate through procurement**. **Owner: Alice** — this diverges from the listed assignee **Evan** on CIPH-39. On 2026-09-02 Evan stated explicitly that this "isn't something we can work around on the engineering side," and Alice took it: she would keep it on the release gate and **chase the certificate process** (SRC-SLACK-37). This supersedes the earlier 2026-08-15 arrangement where Alice had asked Evan to keep chasing procurement (SRC-MEET-08). WS-06 records the signing gap as a **procurement dependency, not an engineering block**.
- **Open sub-item with no named owner:** **budget and procurement timeline** for the certificate sits unresolved in WS-06 "Needs Manual Triage" — it needs an owner assigned.
- **Next action once the certificate lands:** wire signing into the release build step and confirm the signed build passes Defender/SmartScreen without warnings. **Owner: Evan** (assignee of CIPH-39; per SRC-GDOC-39 the remaining item is "procuring a certificate **and** wiring signing into the release build step," and per CIPH-39 acceptance criteria).

### 3. T016 / CIPH-26 — Audit-log schema alignment (third blocker named at the 09-15 audit)
- **Next action (fix):** another pass on the CLI-side audit-log generation so the **emitted records match the defined companion JSON schema**. **Owner: Bob** — this diverges from the listed assignee **Diana** on CIPH-26. Bob wired audit-log generation into the CLI on 2026-09-10 and said on 2026-09-15 he has "another pass queued" (SRC-MEET-10, SRC-CU-CIPH-26).
- **Next action (verification/gate):** re-verify emitted records against the schema and clear the audit gate. **Owner: Diana** (here the assignee and the gate owner coincide) — her 2026-09-18 verification found the mismatch, and she stated she will keep the audit-log gate **red until schema and records match**.

### 4. T011 / CIPH-21 — closing the gate itself
- **Next action:** lift the security-gate hold and close the release checklist once the above are green. **Owner: Diana** for lifting the hold (she placed it, per SRC-CU-CIPH-21); **Evan** owns the T011 checklist/task itself as assignee (SRC-GDOC-05, SRC-CU-CIPH-21); **Alice** owns keeping the items on the release board and the release-board no-ship decision (SRC-MEET-10, CMT-2026-09-002).

### Where owner ≠ listed assignee (the divergences asked about)
| Next action | Listed task assignee | Actual owner of the next action |
|---|---|---|
| Procure Windows code-signing certificate (T029 / CIPH-39) | Evan | **Alice** (took the procurement chase on 2026-09-02) |
| Re-fix CLI audit-log emission to match schema (T016 / CIPH-26) | Diana | **Bob** |
| Re-run size/CVE verification and lift the reopened Docker status (T005 / CIPH-15) | Evan | **Diana** (verification/gate authority) |
| Lift the security-gate hold on the release (T011 / CIPH-21) | Evan | **Diana** (she placed the hold) |
| Budget/procurement timeline for the certificate | — | **Unassigned** — sits in WS-06 "Needs Manual Triage" |

**Records used:** `work-states/WS-03-ops.md` (work state, as-of 2026-09-22); `work-states/WS-06-platforms.md`; `work-states/WS-04-policy.md`; `work-states/comments/2026-09.md` (CMT-2026-09-002), `work-states/comments/2026-06.md` (CMT-2026-06-002); `med-synth/tasks/CIPH-21-Release-v1-Gates.md`, `CIPH-15-Docker-Packaging.md`, `CIPH-39-Windows-Compatibility.md`, `CIPH-26-Audit-Trail-Logging.md`; `med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md` (SRC-SLACK-37), `2026-06-25-docker-size.md` (SRC-SLACK-06); `med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md` (SRC-MEET-10), `2026-08-15-Windows-License-Sync.md` (SRC-MEET-08); `med-synth/documentation/sources/2026-09-02-Windows-Compatibility-Audit-Report.md` (SRC-GDOC-39), `2026-07-12-Release-Checklist.md` (SRC-GDOC-05).
