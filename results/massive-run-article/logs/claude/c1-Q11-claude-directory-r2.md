# On the critical path to clearing the security-gate hold, what are the next actions as of **2026-09-22**, and who owns each next action (not merely the listed task assignee if those differ)?

<!-- RESPONSE_START -->

## Critical path to clearing the security-gate hold — as of 2026-09-22

The hold is Diana's security-gate hold on **T011 / CIPH-21 (Release v1.0 Gates)**, which cannot close until **T005 (Docker size/CVE)** and **T029 (Windows code-signing)** are green. The same 2026-09-15 pre-release audit also keeps the **T016 audit-log schema mismatch** open as a release blocker. Hard no-ship date: **2026-10-15**.
(`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md` lines 31, 34–35; `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-21-Release-v1-Gates.md`; `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-09.md` CMT-2026-09-002)

### 1. T005 / CIPH-15 — Docker image slim-down + CVE verification
- **Next action:** Strip the remaining bloat in the Python site-packages layer and diagnose what is tripping the CVE scan (multi-stage build, Alpine base swap, and OCR/runtime package removal have all landed but the image is still over the ~450MB target and CVE verification still fails as of the 2026-08-12 check).
- **Owner of the next action:** **Evan** — also the listed assignee, so no divergence here.
- **Owner of the clearing/verification step:** **Diana** — she runs the size/CVE check and explicitly holds the reopened status open until both are clean ("Reopened status stands until both the size and the CVE check are clean"). Evan cannot self-close this gate.
- **Watch-out:** dual thresholds apply — an interim RC may ship at 800MB **once CVE-clean**, while GA remains ~450MB. The two must not be conflated on the release checklist, so an RC-level clear could unblock T011 earlier than the 450MB target implies.
- Files: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-06-25-docker-size.md`; `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-15-Docker-Packaging.md`; `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-06.md` (CMT-2026-06-002); `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md` lines 29–30

### 2. T029 / CIPH-39 — Windows Authenticode code-signing
- **Next action:** Procure the Authenticode code-signing certificate (settle budget and procurement timeline). This is the sole open blocker; the Windows build artifact itself is produced fine after the 2026-08-10 backslash path fix.
- **Owner of the next action:** **Alice (PM)** — *not* the listed assignee. CIPH-39 is assigned to Evan, but on 2026-09-02 Evan stated it "isn't something we can work around on the engineering side" and Alice took it: "I'll chase the certificate process." This supersedes the 2026-08-15 arrangement where Alice had asked Evan to keep chasing procurement. WS-06 records it as a procurement dependency, not an engineering block, and the 2026-09-02 brief books "budget/process for Authenticode certificate" to Alice.
- **Owner of the follow-on action:** **Evan** — once the cert exists, wire signing into the Windows release build step and confirm the signed build passes Defender/SmartScreen without warnings.
- Files: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md`; `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-09-02-Windows-Compatibility-Audit-Report.md`; `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-39-Windows-Compatibility.md`; `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-06-platforms.md` lines 36, 53; `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-08-15-Windows-License-Sync.md`

### 3. T016 / CIPH-26 — Audit-log schema vs emitted records (third open release blocker from the same audit)
- **Next action:** The queued pass to make CLI-emitted audit records validate cleanly against the defined companion JSON schema (hash + redaction map). Diana's 2026-09-18 verification found them inconsistent.
- **Owner of the next action:** **Bob** — *not* the listed assignee. CIPH-26 is assigned to Diana, but every implementation step (loader refactor, SHA-256 hashing, schema definition, CLI integration) is Bob's, and at the audit he said "I've got another pass queued."
- **Owner of the clearing step:** **Diana** — "I'll keep the audit-log gate red until schema and records match."
- Files: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-26-Audit-Trail-Logging.md`; `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md` line 50; `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md`

### 4. T011 / CIPH-21 — the hold itself
- **Next action:** Keep the checklist open and re-run gate clearance once T005 and T029 turn green, before 2026-10-15.
- **Owner:** **Evan** holds the task and the checklist document (DOC-2005), and is WS-03 owner — but **Diana** owns releasing the hold (she placed the security-gate hold and relayed the release-board no-ship decision), and **Alice** chairs the gate review that decides nothing closes without all three items resolved.
- Files: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-21-Release-v1-Gates.md`; `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-07-12-Release-Checklist.md`; `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md`

### Where next-action owner differs from the listed assignee
| Item | Listed assignee | Actual owner of the next action |
|---|---|---|
| T029 cert procurement | Evan (CIPH-39) | **Alice** (took over the cert chase on 2026-09-02) |
| T016 schema/record fix | Diana (CIPH-26) | **Bob** (queued implementation pass); Diana owns re-verification |
| T005 Docker | Evan (CIPH-15) | Evan (no divergence); **Diana** owns the size/CVE clearance |

Longest-pole risk against 2026-10-15: T029, because its next action is procurement with no firm timeline recorded anywhere in the package, and it depends on an external certificate authority rather than engineering effort.
