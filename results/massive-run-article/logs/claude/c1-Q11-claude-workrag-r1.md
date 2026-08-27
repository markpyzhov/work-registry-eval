# On the critical path to clearing the security-gate hold, what are the next actions as of **2026-09-22**, and who owns each next action (not merely the listed task assignee if those differ)?

<!-- RESPONSE_START -->

## Critical path to clearing the security-gate hold — next actions and owners as of 2026-09-22

**The hold itself.** T011 / CIPH-21 ("Release v1.0 Gates," WS-03, assignee Evan) is Active under a security-gate hold that **Diana** placed. It cannot close until T005 (Docker size/CVE) and T029 (Windows code-signing) are green, and the release board set a **hard no-ship after 2026-10-15** if those two are not green (CMT-2026-09-002, authored by Diana, 2026-09-15). The 2026-09-15 pre-release audit additionally kept the audit-log schema mismatch on the board as an open release blocker.

### 1. T005 / CIPH-15 — Docker slim-down + CVE clearance
- **Next action (engineering):** strip the remaining bloat in the Python site-packages layer to get under target, and chase down what is tripping the CVE scan. Multi-stage build, Alpine base swap, and removal of unused OCR/runtime packages are already done but insufficient as of the 2026-08-12 verification.
  - **Owner: Evan** — task assignee and the person doing the work (SRC-SLACK-06, SRC-CU-CIPH-15).
- **Next action (verification / gate clearance):** re-run the size measurement and CVE scan and decide whether the gate clears; the task stays "Active (Reopened)" until both size and CVE checks are clean.
  - **Owner: Diana**, not Evan. She reopened the task, ran the 2026-08-12 size/CVE check, and stated she holds the reopened status and tracks it against the release checklist (SRC-SLACK-06).
- **Threshold nuance:** two gates must be tracked separately — interim RC may ship at **800MB once CVE-clean**, GA target remains **~450MB** (CMT-2026-06-002, Evan, from CISO review). Do not conflate them on the checklist.

### 2. T029 / CIPH-39 — Windows Defender/SmartScreen code-signing
- **Next action (the actual blocker): procure the Authenticode code-signing certificate.** This is explicitly a procurement dependency, not an engineering block — Evan stated "this isn't something we can work around on the engineering side, we need the certificate" (SRC-SLACK-37, 2026-09-02).
  - **Owner: Alice**, diverging from the task assignee. CIPH-39's assignee is **Evan**, but on 2026-09-02 Alice took the next action: "Let's keep it open on the release gate rather than pushing it off the board. I'll chase the certificate process." (Earlier, at the 2026-08-15 Windows & License Sync, Alice had asked Evan to keep chasing procurement; the 2026-09-02 thread is the later and governing assignment, with Alice taking the chase herself.)
  - **Unowned sub-item:** "Budget and procurement timeline for Windows Authenticode code-signing certificate" sits in WS-06's **Needs Manual Triage** with no owner assigned — this is the gap that has to be closed for the procurement action to move.
- **Next action (once the cert exists):** wire signing into the release build step and confirm the signed build passes Defender/SmartScreen without warnings (CIPH-39 acceptance criteria; SRC-GDOC-39 "Path to Resolution").
  - **Owner: Evan** (task assignee, DevOps, owns the build pipeline).

### 3. T016 / CIPH-26 — audit-log schema alignment (kept on the board as a release blocker)
- **Next action (remediation):** another pass on the CLI audit-log emission so the emitted records are consistent with the defined companion JSON schema. Bob stated at the 2026-09-15 audit: "I've got another pass queued."
  - **Owner: Bob**, diverging from the task assignee. **CIPH-26's listed assignee is Diana**, but Bob owns the actual remediation work (loader refactor, SHA-256 hashing, schema definition, CLI integration on 2026-09-10).
- **Next action (verification / gate clearance):** re-verify emitted records against the schema and clear the audit gate.
  - **Owner: Diana** — she found the mismatch on 2026-09-18 and said "I'll keep the audit-log gate red until schema and records match."

### Ownership divergences worth flagging explicitly
| Gate / task | Listed assignee | Owner of the actual next action |
|---|---|---|
| T005 / CIPH-15 (Docker size+CVE) | Evan | Evan (remediation) → **Diana** (verification & clearing reopened status) |
| T029 / CIPH-39 (Windows signing) | Evan | **Alice** (certificate procurement — the blocking step) → Evan (wire signing, verify) |
| T016 / CIPH-26 (audit-log schema) | **Diana** | **Bob** (remediation pass) → Diana (verification, gate clearance) |
| T011 / CIPH-21 (release gates) | Evan | Hold was placed by **Diana**; no one closes the gates until the above clear (Alice, 2026-09-15: "No one closes those today") |

### Adjacent but not on the T011 critical path
The upstream high-DPI rendering bug (T036, `pdf-lib-core`, Charlie) was listed at the same gate check and is blocked upstream with no local patch, but WS-03's Blockers tie T011 closure only to T005 and T029.

**Records cited:** `work-states/WS-03-ops.md`, `work-states/WS-06-platforms.md`, `work-states/WS-04-policy.md`, `work-states/comments/2026-09.md` (CMT-2026-09-002), `work-states/comments/2026-06.md` (CMT-2026-06-002), `med-synth/tasks/CIPH-21-Release-v1-Gates.md`, `med-synth/tasks/CIPH-15-Docker-Packaging.md`, `med-synth/tasks/CIPH-39-Windows-Compatibility.md`, `med-synth/tasks/CIPH-26-Audit-Trail-Logging.md`, `med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md` (SRC-SLACK-37), `med-synth/communication/sources/slack/2026-06-25-docker-size.md` (SRC-SLACK-06), `med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md` (SRC-MEET-10), `med-synth/communication/sources/fireflies/2026-08-15-Windows-License-Sync.md` (SRC-MEET-08), `med-synth/documentation/sources/2026-09-02-Windows-Compatibility-Audit-Report.md` (SRC-GDOC-39).
