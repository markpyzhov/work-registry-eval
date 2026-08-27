# For closing the v1.0.0 release checklist as of **2026-09-22**, which dependency gates must go green first, and for each material gate name the listed task assignee versus who owns the immediate next action when those differ?

<!-- RESPONSE_START -->

## Answer

**Scope note:** "the v1.0.0 release checklist" is T011 / CIPH-21 (*Release v1.0 Gates*, assignee **Evan**, still **Active** as of 2026-09-22). Its formal dependency list was T001–T006 plus T010; six of those are Completed and only T005 was open in the original draft, but a later prerequisite audit added T029, and the 2026-09-15 pre-release gate review put two further items on the board as explicit release blockers. All of them are still open on 2026-09-22.

### Gates that must go green

**1. T005 — Docker Packaging (CIPH-15), Active (Reopened)**
- Listed task assignee: **Evan**
- Immediate next action: split. Evan owns the remediation still outstanding — trimming the Python site-packages layer and chasing down what trips the CVE scan (multi-stage build, Alpine base swap and OCR/runtime package removal all failed to reach the ~450MB target). But the gate is not Evan's to close: **Diana** reopened it on 2026-06-25, ran the failing 2026-08-12 size/CVE verification, and stated the reopened status stands until both size and CVE are clean, tracking it against the release checklist. So: **assignee Evan, clearing verification owned by Diana.**

**2. T029 — Windows Defender/SmartScreen code-signing (CIPH-39), Active, High**
- Listed task assignee: **Evan**
- Immediate next action owner: **Alice**. This is the sharpest divergence. The build itself is fine (backslash path fix 2026-08-10, working artifact 2026-08-12); the sole remaining blocker is procuring a code-signing certificate and wiring signing into the release build. Evan stated on 2026-09-02 that "this isn't something we can work around on the engineering side, we need the certificate," and Alice replied "I'll chase the certificate process." She had already told him on 2026-08-15 to keep chasing procurement. So: **assignee Evan, but the next action — certificate procurement — sits with Alice/procurement, not with the assignee.**

**3. Audit-trail logging (T016 / CIPH-26), Active, High — declared an open release blocker**
- Listed task assignee: **Diana**
- Immediate next action owner: **Bob**. Bob did the loader refactor, SHA-256 hashing, schema definition, and the 2026-09-10 CLI integration, and at the 2026-09-15 review said he has "another pass queued" to make the emitted records match the schema. Diana's 2026-09-18 verification found CLI-emitted audit records inconsistent with the defined schema, and she said she will keep the audit gate red until schema and records match. So: **assignee Diana (who owns the verification/hold), next engineering action owned by Bob.**

**4. High-DPI coordinate scaling (T036 / CIPH-46), Blocked — listed by Alice in the 2026-09-15 gate check**
- Listed task assignee: **Charlie**
- Immediate next action owner: **Alice** (with Diana). There is no engineering next step available to Charlie — the scaling-math defect is inside the upstream `pdf-lib-core` C++ core, Charlie filed an upstream issue with no maintainer response, and flattening was rejected as a workaround. On 2026-09-10 Alice directed that it stay blocked pending a decision on whether to ship with the limitation or replace the rendering library entirely; Diana took the action to document it as a known issue. So: **assignee Charlie, but the next action is a PM-level ship-or-swap decision, not assignee work.**

### Where assignee and next-action owner coincide
Nowhere cleanly. On T005 the assignee at least holds part of the next action (the remaining slim-down/CVE work) even though the sign-off is Diana's; on T029, CIPH-26 and CIPH-46 the next action sits entirely outside the listed assignee.

### Adjacent, not named in the gate list
- **CIPH-40 (third-party license audit), Active (Reopened)** — assignee **Diana**, but the live next action is **Charlie** searching for an Apache/MIT PDF parser after the replacement turned out to be AGPL. Framed as a pre-release audit item rather than a named T011 gate.
- **CIPH-17 (multi-page offset drift), Blocked** — Charlie, blocked on unmerged upstream `pdfminer.six` PR #992; Alice called it "a real risk for the v1.0 timeline" on 2026-09-10 but it is not listed as a checklist dependency gate.
- **CIPH-19 (REST API auth)** — Deferred to v1.1, reconfirmed out of v1.0 scope on 2026-08-20, so not a gate.
- **CIPH-34 (node-sync handshake)** — Blocked on 2026-09-22 for high-latency timeouts, but tied to multi-site rollout, not the v1.0.0 checklist.

### Sources
- `med-synth/tasks/CIPH-21-Release-v1-Gates.md` (SRC-CU-CIPH-21)
- `med-synth/documentation/sources/2026-07-12-Release-Checklist.md` (SRC-GDOC-05, DOC-2005)
- `med-synth/tasks/CIPH-15-Docker-Packaging.md` (SRC-CU-CIPH-15)
- `med-synth/communication/sources/slack/2026-06-25-docker-size.md` (SRC-SLACK-06)
- `med-synth/tasks/CIPH-39-Windows-Compatibility.md` (SRC-CU-CIPH-39)
- `med-synth/documentation/sources/2026-09-02-Windows-Compatibility-Audit-Report.md` (SRC-GDOC-39, DOC-2039)
- `med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md` (SRC-SLACK-37)
- `med-synth/communication/sources/fireflies/2026-08-15-Windows-License-Sync.md` (SRC-MEET-08)
- `med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md` (SRC-MEET-10)
- `med-synth/tasks/CIPH-26-Audit-Trail-Logging.md` (SRC-CU-CIPH-26)
- `med-synth/tasks/CIPH-46-High-DPI-PDF-Rendering-Fixes.md` (SRC-CU-CIPH-46)
- `med-synth/communication/sources/slack/2026-09-10-high-dpi-upstream-block.md` (SRC-SLACK-58)
- `med-synth/documentation/sources/2026-09-10-High-DPI-PDF-Rendering-Coordinates-Report.md` (SRC-GDOC-49, DOC-2049)
- `med-synth/tasks/CIPH-40-License-Compliance-Review.md` (SRC-CU-CIPH-40)
- `med-synth/tasks/CIPH-17-Fix-Offset-Mismatch.md` (SRC-CU-CIPH-17)
- `med-synth/communication/sources/slack/2026-06-28-defer-auth.md` (SRC-SLACK-08)
