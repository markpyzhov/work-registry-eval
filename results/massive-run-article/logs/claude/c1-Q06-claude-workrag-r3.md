# For closing the v1.0.0 release checklist as of **2026-09-22**, which dependency gates must go green first, and for each material gate name the listed task assignee versus who owns the immediate next action when those differ?

<!-- RESPONSE_START -->

## Which gates must go green before the v1.0.0 release checklist (T011 / CIPH-21) can close — status as of 2026-09-22

**Bottom line:** T011 / CIPH-21 is **Active**, under a security-gate hold, inside WS-03 (in_progress, P0, owner Evan). Two gates are formally binding, a third is being enforced in practice by QA, and two more are attached to T011 by work-state comments.

### Already green (no longer gating)
The checklist's original dependency list — T001–T006 plus T010 — is satisfied except for T005. Per the July 12 checklist draft (SRC-GDOC-05, DOC-2005): T001 Core Redaction Engine (Completed 2026-06-05), T002 Financial Regex Detection (2026-06-08), T003 Batch CLI (2026-06-12), T004 REST API Endpoints (2026-06-17), T006 Redaction Policy Config (2026-06-22), T010 Security Audit (2026-07-10). Note that this same document's summary line ("six of seven gates met; T005 the only unmet dependency") is **stale** as of 2026-09-22 — it predates the T029 signing gap and the audit-log hold.

### The two binding gates

**Gate 1 — T005 / CIPH-15, Docker image size + CVE verification**
- Status: **Active (Reopened)**. Image hit 2.1GB after OCR bundling; multi-stage build and Alpine swap were done, but as of the 2026-08-12 check the image still exceeds the ~450MB target and CVE verification is still failing.
- Two thresholds apply, don't conflate them: per CMT-2026-06-002 (CISO review), interim RC may ship at **800MB once CVE-clean**; **GA target remains ~450MB**.
- **Listed assignee: Evan** (ClickUp CIPH-15).
- **Immediate next action — split, and it diverges:** the remaining engineering step is Evan's ("still fluff in the Python site-packages layer, and I need to chase down what's tripping the CVE scan", 2026-08-12), but the action that actually turns the gate green is **Diana's** — she runs the size check and CVE scan, and stated "Reopened status stands until both the size and the CVE check are clean. I'll keep tracking it against the release checklist." (SRC-SLACK-06). The assignee cannot close his own gate.

**Gate 2 — T029 / CIPH-39, Windows Defender/SmartScreen code-signing**
- Status: **Active**. Backslash path handling was fixed 2026-08-10 and a Windows build artifact was produced 2026-08-12, so packaging is no longer the blocker — the artifact is simply **unsigned**, and no Authenticode code-signing certificate has been procured or wired into the build pipeline (SRC-GDOC-39, DOC-2039).
- **Listed assignee: Evan** (ClickUp CIPH-39, Priority High; opened by Alice 2026-08-08).
- **Immediate next action owner: Alice — this is the clearest divergence.** Evan explicitly disclaimed it: "this isn't something we can work around on the engineering side, we need the certificate." Alice took it: **"I'll chase the certificate process"** (SRC-SLACK-37, 2026-09-02). WS-06 classifies the signing gap as a **procurement dependency, not an engineering block**, and carries "Budget and procurement timeline for Windows Authenticode code-signing certificate" as an unassigned Needs-Manual-Triage item.

### Third gate held in practice: audit-log schema alignment (T016 / CIPH-26)
Not in T011's original dependency list, but the 2026-09-15 pre-release audit (SRC-MEET-10) put it on the board alongside the other two, and WS-03 records it as an open blocker on T011. Diana: "Until those match, I can't clear the audit gate… I'll keep the audit-log gate red until schema and records match." Alice confirmed all three stay open.
- **Listed assignee: Diana** (ClickUp CIPH-26, Priority High) — she opened it and owns verification; her 2026-09-18 pass found CLI-emitted records inconsistent with the defined schema.
- **Immediate next action owner: Bob — diverges from the assignee.** Bob did the loader refactor, SHA-256 hashing, schema definition, and the 2026-09-10 CLI integration, and at the audit said "I've got another pass queued." Diana verifies; Bob fixes.

### Two further release dependencies tied to T011 by comment
- **Legacy JSON→YAML policy migration (CMT-2026-06-001, author Alice):** MedFirst's three legacy JSON pilot policies must auto-migrate before cutover, "treat migration as a release dependency tied to T006 and the T011 gate." **Divergence:** T006/CIPH-16 is Completed and sits in WS-01 under Charlie, but **Evan owns the JSON→YAML converter**.
- **T031 / CIPH-41 large-file memory (CMT-2026-08-003, author Bob):** MedFirst clinic workstation OOM on a 4.7GB PDF with 8GB RAM — "prioritize T031 ahead of nice-to-have perf work and tie explicitly to the T011 release gate." Status Active (Reopened). Here assignee and next action **do not** diverge: **Charlie** is the assignee and is the one refactoring the stream buffer-release logic.

### Hard deadline
Per CMT-2026-09-002 (author Diana, 2026-09-15, release board decision): **no-ship after 2026-10-15 if T005 and T029 are not green. Hard deadline, not advisory.**

### Summary of assignee vs. next-action owner

| Gate | Listed assignee | Owns the immediate next action | Diverges? |
|---|---|---|---|
| T005 / CIPH-15 Docker size + CVE | Evan | Evan (site-packages trim, CVE root cause) → **Diana** (re-scan and clear reopened status) | Yes — clearance is Diana's |
| T029 / CIPH-39 Windows code-signing | Evan | **Alice** (certificate procurement) | Yes — procurement, not engineering |
| T016 / CIPH-26 audit-log schema | Diana | **Bob** (next CLI emission pass) | Yes |
| T006 legacy JSON migration (comment) | T006 completed under Charlie/WS-01 | **Evan** (JSON→YAML converter) | Yes |
| T031 / CIPH-41 large-file memory (comment) | Charlie | Charlie (buffer-release refactor) | No |
| T011 / CIPH-21 checklist itself | Evan | Blocked — hold placed by **Diana**; release board (Alice/board) governs the 2026-10-15 no-ship | Yes — Evan cannot close it unilaterally |

**Records cited:** `work-states/WS-03-ops.md`, `work-states/WS-04-policy.md`, `work-states/WS-05-performance.md`, `work-states/WS-06-platforms.md`, `work-states/WS-01-engine.md`, `work-states/index.md`; comments `CMT-2026-06-001`, `CMT-2026-06-002`, `CMT-2026-08-003`, `CMT-2026-09-002`; sources `SRC-CU-CIPH-21`, `SRC-CU-CIPH-15`, `SRC-CU-CIPH-39`, `SRC-CU-CIPH-26`, `SRC-CU-CIPH-41`, `SRC-GDOC-05`, `SRC-GDOC-39`, `SRC-SLACK-06`, `SRC-SLACK-37`, `SRC-MEET-10`.
