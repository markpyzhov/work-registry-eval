# On the critical path to clearing the security-gate hold, what are the next actions as of **2026-09-22**, and who owns each next action (not merely the listed task assignee if those differ)?

<!-- RESPONSE_START -->

## Answer

**What the hold is.** Diana placed a security-gate hold on the v1.0 release (T011 / CIPH-21). It cannot clear until **T005** (Docker image slim-down + CVE) and **T029** (Windows code-signing) are green, against a hard **no-ship after 2026-10-15** release-board decision. The 2026-09-15 pre-release audit kept a third item — the **T016 audit-log schema mismatch** — explicitly visible as a release blocker in the same gate review, so it sits on the same critical path even though it is not part of the formal no-ship pair.

### Gate 1 — T005 / CIPH-15: Docker size + CVE

| Next action | Owner |
|---|---|
| Strip the remaining bloat in the Python site-packages layer to get the image under target (dual gates: interim RC may ship at **800MB once CVE-clean**, GA target ~**450MB** — must not be conflated) | **Evan** (also the listed assignee) |
| Chase down what is tripping the CVE scan and get a clean scan | **Evan** |
| Re-run the size + CVE verification and lift the "Reopened" status / update the release checklist | **Diana** — she owns the verification pass and explicitly holds the reopened status ("Reopened status stands until both the size and the CVE check are clean. I'll keep tracking it against the release checklist"), even though CIPH-15's assignee is Evan |

Last verification (2026-08-12) failed on both size and CVE; nothing later supersedes it.

### Gate 2 — T029 / CIPH-39: Windows Authenticode signing

| Next action | Owner |
|---|---|
| Procure the code-signing certificate (the sole open blocker; explicitly a **procurement** dependency, not an engineering one — Evan: "this isn't something we can work around on the engineering side") | **Alice** — on 2026-09-02 she took it: "I'll chase the certificate process." This supersedes the 2026-08-15 direction that Evan keep chasing procurement. **CIPH-39's listed assignee is Evan**, so owner ≠ assignee here |
| Settle budget and procurement timeline for the certificate | **Unassigned** — sitting in WS-06 "Needs Manual Triage"; no owner named in the package |
| Once the cert lands: wire signing into the release build step and produce a signed artifact that passes Defender/SmartScreen without warnings | **Evan** (assignee; also the audit doc's owner) |
| Confirm the gate green on the release board | **Diana** (gate holder) / **Alice** (release board) |

Windows packaging itself is no longer a blocker — the backslash path fix landed 2026-08-10 and a build artifact was produced 2026-08-12.

### Gate 3 — T016 / CIPH-26: audit-log schema vs emitted records (held open in the same review)

| Next action | Owner |
|---|---|
| Another pass to make the CLI-emitted audit records validate against the defined companion JSON schema ("I've got another pass queued") | **Bob** — **CIPH-26's listed assignee is Diana**, so owner ≠ assignee here too |
| Re-verify records against schema and clear (or keep red) the audit gate | **Diana** — "I'll keep the audit-log gate red until schema and records match"; her 2026-09-18 verify found the mismatch |

### Gate-level ownership

- **T011 / CIPH-21** is assigned to **Evan**, but the hold itself is **Diana's** to release, and the no-ship deadline is an **Alice**-run release-board decision (`CMT-2026-09-002`, 2026-09-15). Alice's standing instruction from the audit: no one closes these today.

### Adjacent, tied to the T011 gate but not to the security-gate hold

- Legacy **JSON→YAML policy auto-migration** for the MedFirst pilot — a release dependency tied to T006 and the T011 gate; **Evan** owns the converter (`CMT-2026-06-001`).
- **T031** MedFirst 4.7GB-PDF OOM — Bob asked that it be tied explicitly to the T011 release gate (`CMT-2026-08-003`).

### Evidence limits

The package names no procurement counterparty, vendor, cost, or ETA for the Authenticode certificate — only that Alice is chasing it and that budget/timeline remain untriaged. No evidence dated after 2026-09-22 changes any of the above.

### Files cited

- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-06-platforms.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-01-engine.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/index.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-09.md` (CMT-2026-09-002)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-08.md` (CMT-2026-08-003)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-06.md` (CMT-2026-06-001, CMT-2026-06-002)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md` (SRC-MEET-10)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-08-15-Windows-License-Sync.md` (SRC-MEET-08)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md` (SRC-SLACK-37)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-06-25-docker-size.md` (SRC-SLACK-06)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-21-Release-v1-Gates.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-15-Docker-Packaging.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-39-Windows-Compatibility.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-26-Audit-Trail-Logging.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-09-02-Windows-Compatibility-Audit-Report.md` (SRC-GDOC-39)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-07-12-Release-Checklist.md` (SRC-GDOC-05)
