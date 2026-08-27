# For closing the v1.0.0 release checklist as of **2026-09-22**, which dependency gates must go green first, and for each material gate name the listed task assignee versus who owns the immediate next action when those differ?

<!-- RESPONSE_START -->

## Short answer

As of **2026-09-22**, the v1.0.0 release checklist (**T011 / CIPH-21**, "Release v1.0 Gates", assignee **Evan**) is Active under a security-gate hold. Its original dependency set (T001–T006 + T010) is satisfied **except T005**, and **T029** was added later as a second hard gate. The pre-release audit and the work-state comments attach three further release-coupled holds. A hard **no-ship date of 2026-10-15** applies if T005 and T029 are not green.

---

## 1. Gates that must go green — authoritative set

From `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md` (as-of 2026-09-22, the authoritative Work State) and `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-21-Release-v1-Gates.md`:

**Already green** (no action needed): T001 Core engine, T002 Financial regex, T003 Batch CLI, T004 REST API, T006 Policy config, T010 Security audit — confirmed Completed in `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-07-12-Release-Checklist.md` and WS-03 "Done / Evidence" (T010 re-scan 2026-07-15 plus RedByte pen-test attestation, CMT-2026-07-002).

**Hard, must-clear-first gates:**

| Gate | State as of 2026-09-22 | Green condition |
|---|---|---|
| **T005 / CIPH-15 — Docker image size + CVE** | Active (Reopened) since 2026-06-25; 2026-08-12 check still over the ~450MB target and CVE verification still failing | Size target met **and** CVE scan clean. Note the dual threshold from CMT-2026-06-002: interim RC may ship at **800MB once CVE-clean**; **GA target ~450MB** — do not conflate them |
| **T029 / CIPH-39 — Windows Defender/SmartScreen code-signing** | Active; build artifact produced and running (2026-08-12), but unsigned binary is blocked by SmartScreen/Defender | Authenticode certificate procured, signing wired into the release build step |

Both are named in `WS-03-ops.md` Blockers: "T011 cannot close until T005 (Docker size/CVE) and T029 (Windows code-signing certificate) are green," with CMT-2026-09-002 setting the **2026-10-15 no-ship** (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-09.md`).

## 2. Additional release-coupled holds on the same board

- **T016 / CIPH-26 — Audit-trail logging schema mismatch.** The 2026-09-15 pre-release audit keeps it "visible as a release blocker": CLI-emitted audit records do not validate against the defined companion JSON schema; Diana's 2026-09-18 verification pass confirmed the mismatch. Sources: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-26-Audit-Trail-Logging.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md`.
- **T031 / CIPH-41 — Large-file chunking memory leak.** Explicitly tied to the T011 gate by CMT-2026-08-003 (MedFirst clinic OOM on a 4.7GB PDF with 8GB RAM, "pilot-blocker"). See `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-05-performance.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-41-Large-File-Chunking.md`.
- **T006 legacy JSON→YAML migration.** T006 itself is Completed, but CMT-2026-06-001 records that MedFirst's three legacy JSON policies must auto-migrate before cutover and treats that migration as "a release dependency tied to T006 and the T011 gate" (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-06.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-01-engine.md`).
- **T030 / CIPH-40 — Licence compliance (AGPL).** P0 Legal gate on whole-bundle copyleft (CMT-2026-08-002); listed third in the 2026-09-22 brief's priority order. Not named in WS-03 as a T011 dependency, but it is an open pre-release compliance gate.
- **T036 / CIPH-46 — High-DPI rendering.** Alice listed it in the 2026-09-15 gate check as still on the board, but the 2026-09-10 direction was to leave it blocked and decide whether to ship with a documented known-issue limitation — so it is a ship decision, not a confirmed hard gate.

## 3. Listed assignee vs owner of the immediate next action

| Gate | ClickUp assignee | Owner of the immediate next action | Divergence? |
|---|---|---|---|
| **T011 / CIPH-21** release checklist | **Evan** | Evan holds the checklist, but he cannot close it himself — Diana holds the security-gate hold and keeps the audit gate red | Partial: closure authority sits with Diana/the release board |
| **T005 / CIPH-15** Docker size + CVE | **Evan** | **Evan** — trim the remaining Python site-packages fluff and chase what trips the CVE scan; **Diana** owns the verification pass that flips it green | Same doer; verification owner differs (Diana) |
| **T029 / CIPH-39** Windows signing | **Evan** | **Alice** — on 2026-09-02 Evan stated "this isn't something we can work around on the engineering side, we need the certificate," and Alice replied "I'll chase the certificate process" | **Yes — clearest divergence.** Assignee Evan, next action Alice; it is a procurement dependency, not an engineering block (WS-06 says exactly that). Task was also *created* by Alice on 2026-08-08 |
| **T016 / CIPH-26** audit-log schema | **Diana** | **Bob** — he wired audit-log generation into the CLI on 2026-09-10 and has "another pass queued" on the shape mismatch; Diana then re-verifies and holds the gate red until schema and records match | **Yes** — Diana is assignee/verifier, Bob owns the fix |
| **T031 / CIPH-41** chunking leak | **Charlie** | **Charlie** — buffer-release refactor after each chunk (started 2026-08-20) | No (Bob reopened it, Diana reproduces in QA; task created by Alice) |
| **T006 legacy JSON migration** | **Charlie** (CIPH-16, Completed) | **Evan** — CMT-2026-06-001: "Evan owns the JSON→YAML converter" | **Yes** — the residual release dependency sits with Evan, not the task's assignee |
| **T030 / CIPH-40** licence/AGPL | **Diana** | **Charlie** for the Apache/MIT parser search (from 2026-08-15); but **Legal** owns closure — CMT-2026-08-002 states engineering search alone is insufficient | **Yes — double divergence** (assignee Diana, doer Charlie, gate-closer Legal) |
| **T036 / CIPH-46** high-DPI | **Charlie** | Upstream `pdf-lib-core` maintainers (unresponsive); locally, **Alice/Diana** own the ship-with-known-issue decision | **Yes** — no internal owner can make it green |

## Bottom line

To close the checklist you need **T005 and T029 green** (hard, deadline 2026-10-15), plus clearance of the **T016 audit-log schema mismatch**, the **T031 large-file leak**, the **legacy JSON migration**, and the **T030 Legal AGPL gate**. The two gates where the paper assignee is *not* the person who can move it next are **T029** (assignee Evan → Alice owns certificate procurement) and **T016** (assignee Diana → Bob owns the schema fix, Diana only verifies); **T030** and the **T006 migration** carry the same split in weaker form (Diana → Charlie/Legal; Charlie → Evan).
