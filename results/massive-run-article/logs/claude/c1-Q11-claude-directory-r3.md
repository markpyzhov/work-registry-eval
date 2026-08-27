# On the critical path to clearing the security-gate hold, what are the next actions as of **2026-09-22**, and who owns each next action (not merely the listed task assignee if those differ)?

<!-- RESPONSE_START -->

## Critical path as of 2026-09-22

The security-gate hold sits on **T011 / CIPH-21 (Release v1.0 Gates)** — Diana placed the hold, and it cannot be lifted until the gate items below go green. Hard constraint: the release board set a **no-ship after 2026-10-15** if T005 and T029 aren't green (`CMT-2026-09-002`, not advisory).

Sources: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-21-Release-v1-Gates.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-09.md`.

### 1. T005 / CIPH-15 — Docker image size + CVE (formal blocker #1)
- **Next action A (highest leverage): clear the failing CVE scan.** Evan's own words on 2026-08-12: still over the ~450MB target and "I need to chase down what's tripping the CVE scan." Per `CMT-2026-06-002` (CISO review), CVE-clean alone unlocks an **interim RC at 800MB**; ~450MB is only the GA gate — so CVE clearance, not size, is what moves the release forward first. Do not conflate the two thresholds.
- **Next action B: strip the remaining Python site-packages layer** to drive size toward the GA target.
- **Owner of the work:** Evan — and here the listed ClickUp assignee (Evan) and the actual doer coincide.
- **Owner of clearing the gate:** **Diana**, not Evan. She runs the size/CVE verification and stated "Reopened status stands until both the size and the CVE check are clean." Evan cannot mark this green himself.
- Files: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-15-Docker-Packaging.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-06-25-docker-size.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-06.md`.

### 2. T029 / CIPH-39 — Windows code-signing (formal blocker #2)
- **Next action: procure the Authenticode code-signing certificate.** This is the whole gate — Evan: "this isn't something we can work around on the engineering side, we need the certificate." WS-06 classifies it as a **procurement dependency, not an engineering block**; the backslash/path work is already fixed.
- **Owner of the next action: Alice (PM), not the task assignee.** CIPH-39 is assigned to Evan, but on 2026-09-02 Alice took it explicitly: "Let's keep it open on the release gate rather than pushing it off the board. **I'll chase the certificate process.**"
- **Owner of the follow-on step (after cert arrives):** Evan — sign the Windows build and re-verify it passes Defender/SmartScreen without warnings.
- **Open prerequisite for Alice:** budget and procurement timeline for the certificate is still in WS-06 "Needs Manual Triage."
- Files: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-39-Windows-Compatibility.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-06-platforms.md`.

### 3. T016 / CIPH-26 — Audit-log schema mismatch (third gate item on the release hold)
- **Next action: Bob's queued pass to make CLI-emitted audit records validate against the defined companion JSON schema.** Bob wired audit-log generation into the CLI on 2026-09-10; Diana's 2026-09-18 verification found the emitted records inconsistent with the schema. Charlie confirmed at the audit this is schema-vs-emitted-records, not a packaging issue.
- **Owner of the next action: Bob**, even though **CIPH-26's listed assignee is Diana**. Bob: "I've got another pass queued."
- **Owner of clearing the gate: Diana** — "I'll keep the audit-log gate red until schema and records match."
- **Status nuance:** the Sept 15 pre-release audit lists this alongside Docker and Windows signing as an open release blocker, but the formal T011 dependency and the 2026-10-15 no-ship trigger name only **T005 and T029**. So the audit-log item blocks the release opening but is not part of the dated no-ship condition.
- Files: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-26-Audit-Trail-Logging.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md`.

### 4. T011 / CIPH-21 itself — gate bookkeeping
- **Next action: keep the release checklist current and close it once the gates clear.** All other checklist dependencies (T001–T006, T010) are already satisfied; T005 was the only unmet one at the last checklist revision, with T029 added later.
- **Owner:** Evan is the CIPH-21 assignee and the Release Checklist document owner. But **the hold is Diana's to lift** (she placed the security-gate hold), and **Alice runs the gate decision** — "Security-gate work stays open... No one closes those today."
- Files: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-07-12-Release-Checklist.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-21-Release-v1-Gates.md`.

### Summary — where listed assignee ≠ next-action owner
| Gate item | Listed assignee | Actual next-action owner | Gate-clearance owner |
|---|---|---|---|
| T005 Docker CVE + size | Evan | Evan (CVE root-cause, then size) | **Diana** (verification) |
| T029 Windows signing | **Evan** | **Alice** (certificate procurement) | Evan signs/re-tests, then Diana/Alice |
| T016 Audit-log schema | **Diana** | **Bob** (fix CLI-emitted records) | **Diana** (re-verify) |
| T011 Release gates | Evan | Evan (checklist) | **Diana** lifts hold; **Alice** calls the gate |

The 2026-09-22 brief's own follow-up line matches this: "Secure Authenticode cert and finish Alpine/CVE Docker verification," with WS-03 / T005 + T029 ranked priority 1 against the 2026-10-15 deadline.
