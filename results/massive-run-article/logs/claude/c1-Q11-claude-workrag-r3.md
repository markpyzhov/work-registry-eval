# On the critical path to clearing the security-gate hold, what are the next actions as of **2026-09-22**, and who owns each next action (not merely the listed task assignee if those differ)?

<!-- RESPONSE_START -->

## Answer

**Critical path.** The security-gate hold is on **T011 / CIPH-21 — Release v1.0 Gates** (WS-03, owner Evan, status Active). Diana placed the hold, and per WS-03 *Blockers and Dependencies*, **T011 cannot close until T005 (Docker size/CVE) and T029 (Windows code-signing certificate) are green**. The 2026-09-15 pre-release audit additionally keeps the **audit-log schema mismatch (T016 / CIPH-26)** visible as a release blocker on the same gate review. A hard **no-ship after 2026-10-15** applies if T005 and T029 are not green (CMT-2026-09-002, Diana, release-board decision).

### Next actions and their owners (as of 2026-09-22)

**1. T005 / CIPH-15 — Docker image slim-down + CVE clearance** (task assignee: Evan)
- **Strip the remaining bloat from the Python site-packages layer and chase down what is tripping the CVE scan** — owner: **Evan**. He stated this explicitly on 2026-08-12 after the multi-stage build, Alpine base swap, and OCR/runtime package removal still left the image over target with CVE verification failing.
- **Re-verify size and re-run the CVE scan, and keep the item tracked against the release checklist** — owner: **Diana** (QA), not Evan. She ran the 2026-08-12 size/CVE check and stated the Reopened status stands until both the size and CVE checks are clean.
- Thresholds to verify against are dual (CMT-2026-06-002, CISO review): interim RC may ship at **800MB once CVE-clean**; **GA target remains ~450MB**. These must be tracked separately.

**2. T029 / CIPH-39 — Windows Defender/SmartScreen code-signing** (task assignee: Evan)
- **Procure the Authenticode code-signing certificate** — owner: **Alice (PM)**, which differs from the task assignee. On 2026-09-02 Evan stated this is not workable on the engineering side ("we need the certificate"), and Alice took it: she said she would keep it open on the release gate and **chase the certificate process** herself. This supersedes the earlier 2026-08-15 position, where Alice had told Evan to keep chasing procurement. WS-06 also carries **"Budget and procurement timeline for the Windows Authenticode code-signing certificate"** as an open *Needs Manual Triage* item with no engineering owner — the work state characterises the signing gap as a **procurement dependency, not an engineering block**.
- **Wire signing into the release build step once the certificate exists, and confirm the signed build passes Defender/SmartScreen without warnings** — owner: **Evan** (DevOps; CIPH-39 assignee, and owner of the 2026-09-02 compatibility audit DOC-2039). Windows packaging itself is already cleared (path fix 2026-08-10, artifact produced 2026-08-12).

**3. T016 / CIPH-26 — Audit-log schema alignment** (task assignee: **Diana**)
- **Run the queued pass to make the CLI-emitted audit records match the defined companion JSON schema** — owner: **Bob**, not the task assignee. Bob wired audit-log generation into the CLI on 2026-09-10 and stated on 2026-09-15 that the emitted shape still isn't consistent with the schema and that he has **another pass queued**.
- **Re-verify emitted records against the schema and clear (or keep red) the audit gate** — owner: **Diana**. Her 2026-09-18 verification found the mismatch; she stated she will keep the audit-log gate red until schema and records match, and that she cannot clear the gate until then.

**4. T011 / CIPH-21 — the gate itself**
- **Hold stays closed; no gate may be closed until the above are green** — decision owner: **Alice (PM)**, who directed on 2026-09-15 that security-gate work stays open and "no one closes those today"; **hold/clearance authority sits with Diana** (she placed the security-gate hold and clears the audit gate). **Evan** is the CIPH-21 assignee and WS-03 owner, responsible for driving the checklist to closure and reporting the outstanding update: Docker multi-stage build progress, final CVE scan results, and release-gate clearance.

### Where assignee and next-action owner diverge
| Gate item | Listed task assignee | Actual next-action owner |
|---|---|---|
| T029 certificate procurement | Evan (CIPH-39) | **Alice** (chasing the certificate process) |
| T029 signing wired into build | Evan (CIPH-39) | Evan (unchanged) |
| T016 audit-log schema fix | Diana (CIPH-26) | **Bob** (queued CLI emission pass) |
| T016 gate verification/clearance | Diana (CIPH-26) | Diana (unchanged) |
| T005 size/CVE remediation | Evan (CIPH-15) | Evan (unchanged) |
| T005 size/CVE verification | Evan (CIPH-15) | **Diana** (re-check and re-scan) |

### Records cited
- `work-states/WS-03-ops.md` (path = work-state) — Active Work, Blockers and Dependencies, Next Update Needed, Task List
- `work-states/WS-06-platforms.md` (path = work-state) — T029 Active Work, Needs Manual Triage, Next Update Needed
- `work-states/WS-04-policy.md` (path = work-state) — T016 Active Work, Next Update Needed
- `work-states/comments/2026-09.md` — CMT-2026-09-002 (no-ship deadline)
- `work-states/comments/2026-06.md` — CMT-2026-06-002 (dual RC/GA size gates)
- `med-synth/tasks/CIPH-21-Release-v1-Gates.md` (SRC-CU-CIPH-21), `med-synth/tasks/CIPH-15-Docker-Packaging.md` (SRC-CU-CIPH-15), `med-synth/tasks/CIPH-39-Windows-Compatibility.md` (SRC-CU-CIPH-39), `med-synth/tasks/CIPH-26-Audit-Trail-Logging.md` (SRC-CU-CIPH-26)
- `med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md` (SRC-MEET-10), `med-synth/communication/sources/fireflies/2026-08-15-Windows-License-Sync.md` (SRC-MEET-08)
- `med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md` (SRC-SLACK-37), `med-synth/communication/sources/slack/2026-06-25-docker-size.md` (SRC-SLACK-06)
- `med-synth/documentation/sources/2026-09-02-Windows-Compatibility-Audit-Report.md` (SRC-GDOC-39)
