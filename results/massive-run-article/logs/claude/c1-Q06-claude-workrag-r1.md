# For closing the v1.0.0 release checklist as of **2026-09-22**, which dependency gates must go green first, and for each material gate name the listed task assignee versus who owns the immediate next action when those differ?

<!-- RESPONSE_START -->

## Closing the CipherDoc v1.0.0 release checklist — dependency gates as of 2026-09-22

The release checklist is tracked as **T011 / CIPH-21 "Release v1.0 Gates"** under **WS-03 (Packaging, Release gating, and Security)**, owner Evan, status `in_progress`, P0, last updated 2026-09-22. The task itself is **Active** and sitting under a **security-gate hold placed by Diana**.

### 1. Gates already green (no longer blocking)

The checklist's original dependency set — **T001 through T006 and T010** — is satisfied. CIPH-21's acceptance criteria record these as "met; those tasks are Completed," and WS-03 confirms **T010 / CIPH-20** (security audit and vulnerability scans) is done: the medium-severity CORS `*` origin finding from the July 6 scan was patched to configured `ALLOWED_ORIGINS`, and July 15 re-scans confirmed the patch holds. A RedByte pen-test attestation letter dated 2026-07-11 (CMT-2026-07-002) supplements the internal scan artifacts in the release evidence pack.

Note that the July 12 checklist draft (SRC-GDOC-05 / DOC-2005) says "six of seven dependency gates are met; T005 remains the only unmet dependency." **That document is stale.** A later prerequisite audit widened the blocking set, and the current work state supersedes it.

### 2. Gates that must go green first

**Formal close conditions per WS-03 "Blockers and Dependencies":** T011 cannot close until **T005 and T029 are green**.

| Gate | What must clear | Status |
|---|---|---|
| **T005 / CIPH-15** — Docker image size + CVE | Image down to the ~450MB target **and** CVE verification passing with no outstanding findings | **Active (Reopened)**. Reopened 2026-06-25 when the image hit 2.1GB after OCR dependencies were bundled. Multi-stage build, Alpine base swap, and removal of unused OCR/runtime packages have not closed the gap — as of the 2026-08-12 verification the image still exceeds ~450MB and CVE verification is still failing. |
| **T029 / CIPH-39** — Windows code-signing | An Authenticode code-signing certificate procured and wired into the release build step, so the build passes Defender/SmartScreen without warnings | **Active**, held on code-signing. Backslash path defects were fixed 2026-08-10 and a Windows build artifact was produced by 2026-08-12 — packaging is no longer the blocker. The artifact is unsigned; no certificate has been procured or configured. |

**A third gate is material but sits outside that formal two-item list:**

| Gate | What must clear | Status |
|---|---|---|
| **T016 / CIPH-26** — Compliance audit-trail logging | CLI-emitted audit records must validate cleanly against the defined companion JSON schema (SHA-256 input hash + redaction map) | **Active/reopened**. The 2026-09-15 pre-release audit listed audit-log schema alignment alongside Docker and Windows signing as an open blocker, and Diana's 2026-09-18 verification found CLI-emitted records inconsistent with the schema. Diana: "I'll keep the audit-log gate red until schema and records match." |

I flag the distinction explicitly: WS-03's dependency clause names only T005 and T029 as T011's close conditions, but the September 15 pre-release audit — the most recent gate-level review — treats the audit-log mismatch as an equally live release blocker that Alice directed be kept visible on the board. Anyone planning the close should treat it as a third gate.

Two dated constraints attach to this:
- **Dual size gates (CMT-2026-06-002)**: CISO review defines an interim RC threshold of **800MB once CVE-clean**, with GA remaining at **~450MB**. These are tracked separately — an RC can clear at 800MB that would not clear GA.
- **No-ship deadline (CMT-2026-09-002)**: the release board set a hard no-ship after **2026-10-15** if T005 and T029 are not green.

### 3. Listed assignee vs. owner of the immediate next action

**T005 / CIPH-15 (Docker size/CVE) — assignee Evan; next action also Evan, but sign-off is Diana's.**
Evan holds both the ticket and the immediate work: trimming remaining bulk in the Python site-packages layer and diagnosing what is tripping the CVE scan. The divergence here is on *clearance* rather than execution — Diana runs the size/CVE verification and controls whether the gate flips. Her position on 2026-08-12: reopened status stands until both the size and the CVE check are clean, and she is tracking it against the release checklist. So: **doing = Evan, clearing = Diana.**

**T029 / CIPH-39 (Windows code-signing) — assignee Evan; immediate next action owned by Alice. This is the material divergence.**
The ticket is assigned to Evan, but the remaining work is not engineering work. Evan on 2026-09-02: this "isn't something we can work around on the engineering side, we need the certificate." Alice took the next action in the same thread: "Let's keep it open on the release gate rather than pushing it off the board. I'll chase the certificate process." WS-06 corroborates this — the signing gap is characterized as **a procurement dependency, not an engineering block**, and "budget and procurement timeline for Windows Authenticode code-signing certificate" sits in WS-06's *Needs Manual Triage*. Once the certificate exists, the next action reverts to Evan to wire signing into the release build step.

One wrinkle worth noting: on 2026-08-15 Alice had told Evan to "keep chasing procurement on the cert," which would put the next action with Evan. The 2026-09-02 exchange is later and moves it to Alice. I read Alice as the current owner, but the record is not perfectly clean on this point.

**T016 / CIPH-26 (audit-log schema) — assignee Diana; immediate next action owned by Bob.**
CIPH-26 is assigned to Diana (High priority, created 2026-07-08), and WS-04's owners are Alice / Diana. But the entire implementation trail is Bob's — loader refactor (07-11), SHA-256 hashing (08-05), schema definition (08-15), CLI integration (09-10) — and Bob holds the next action: at the September 15 audit he said the emitted shape still isn't consistent with what the schema expects and he has "another pass queued." Diana's role is verification and gate clearance; her 2026-09-18 pass found the mismatch. So: **assignee Diana, next action Bob, clearance Diana.**

**T011 / CIPH-21 itself — assignee Evan; hold owned by Diana, board owned by Alice.**
Evan is the assignee and WS-03 owner, but he cannot close his own task: Diana placed the security-gate hold pending both T005 and T029, and Alice chairs the gate decision ("Security-gate work stays open... No one closes those today"). WS-03's *Next Update Needed* is Docker multi-stage build progress, final CVE scan results, and release gate clearance.

### Summary of the divergences

- **T005**: assignee Evan / next action Evan / clearance Diana — no assignee-vs-next-action split, only a verification split.
- **T029**: assignee Evan / **next action Alice** (certificate procurement) — a genuine split, and the one that matters most, because the remaining work is procurement rather than engineering and cannot be accelerated by the assignee.
- **T016**: assignee Diana / **next action Bob** (another pass on CLI-emitted records) / clearance Diana — also a genuine split.
- **T011**: assignee Evan / hold held by Diana / board decision Alice.

### Sources

`work-states/WS-03-ops.md` (authoritative work state, last updated 2026-09-22); `work-states/WS-04-policy.md`; `work-states/WS-06-platforms.md`; `work-states/index.md` (as-of 2026-09-22T12:00:00Z); `SRC-CU-CIPH-21`; `SRC-CU-CIPH-15`; `SRC-CU-CIPH-39`; `SRC-CU-CIPH-26`; `SRC-CU-CIPH-20`; `SRC-SLACK-06` (Docker Image Size Optimization); `SRC-SLACK-37` (Windows Signing Gap); `SRC-MEET-10` (2026-09-15 Pre-Release Audit); `SRC-MEET-08` (2026-08-15 Windows & License Sync); `SRC-GDOC-39` (Windows Build Signing Gap audit); `SRC-GDOC-05` (2026-07-12 Release Checklist — superseded); comments `CMT-2026-06-002`, `CMT-2026-09-002`, `CMT-2026-07-002`.
