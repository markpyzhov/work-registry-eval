# For closing the v1.0.0 release checklist as of **2026-09-22**, which dependency gates must go green first, and for each material gate name the listed task assignee versus who owns the immediate next action when those differ?

<!-- RESPONSE_START -->

## Answer

**As of 2026-09-22, closing the v1.0.0 release checklist (T011 / CIPH-21, owner Evan) formally requires exactly two gates to go green: T005 (Docker size/CVE) and T029 (Windows code-signing).** Everything the original checklist depended on — T001–T006 and T010 — is already satisfied. A hard no-ship deadline of **2026-10-15** applies if T005 and T029 are not green by then.

Beyond those two, the 2026-09-15 pre-release audit and the work-state comments keep three further items visible as release-coupled holds (audit-log schema, MedFirst OOM, legacy-policy migration), plus a documented-limitation decision pending on high-DPI.

### Formal T011 dependencies still open

| Gate | Listed task assignee | Owner of the immediate next action | Divergence? |
|---|---|---|---|
| **T005 / CIPH-15 — Docker image size + CVE clean** (Active/Reopened; still over ~450MB target, CVE verification failing as of 2026-08-12) | **Evan** | **Evan** does the remaining engineering (trim the Python site-packages layer, chase what trips the CVE scan) — but the gate is **Diana's** to clear: she reopened it and holds "Reopened" status until both size and CVE checks are clean. Threshold definition came from CISO review: interim RC may ship at 800MB once CVE-clean, GA target stays ~450MB (CMT-2026-06-002). | No on execution; **yes on clearance** — verification/sign-off is Diana, not the assignee |
| **T029 / CIPH-39 — Windows Defender/SmartScreen code-signing** (Active; build artifact exists, path handling fixed, unsigned binary blocked) | **Evan** | **Alice** — she explicitly took the certificate chase ("I'll chase the certificate process," 2026-09-02). Evan stated this is not workable on the engineering side; WS-06 records it as a **procurement dependency, not an engineering block**, with budget/procurement timeline sitting in Needs Manual Triage. | **Yes** — assignee Evan, next action owned by Alice |

### Additional release-coupled holds (raised as blockers, not listed T011 dependencies)

| Gate | Listed task assignee | Owner of the immediate next action | Divergence? |
|---|---|---|---|
| **T016 / CIPH-26 — audit-trail logging: CLI-emitted records don't validate against the defined schema** (called out at the 2026-09-15 pre-release audit; Diana's 2026-09-18 verification found the mismatch; "remains an open release blocker") | **Diana** | **Bob** — he wired audit-log generation into the CLI on 2026-09-10 and has "another pass queued" to make emitted records match the schema. Diana only re-verifies and keeps the gate red until they match. | **Yes** — assignee Diana, next action owned by Bob |
| **T006 / CIPH-16 — legacy JSON→YAML policy auto-migration** (task itself is Completed, but CMT-2026-06-001 attaches the MedFirst migration requirement as a release dependency "tied to T006 and the T011 gate") | **Charlie** (CIPH-16 assignee) | **Evan** — explicitly owns the JSON→YAML converter for the three legacy MedFirst pilot policies. | **Yes** — assignee Charlie, next action owned by Evan |
| **T031 / CIPH-41 — large-file stream chunking / MedFirst OOM** (Reopened; CMT-2026-08-003 says "tie explicitly to the T011 release gate"; OOM on a 4.7GB PDF with 8GB clinic RAM) | **Charlie** | **Charlie** — refactoring stream-buffer release logic. (Bob raised the pilot-blocker finding; he does not own the fix.) | No |
| **T030 / CIPH-40 — third-party license audit / AGPL parser** (Reopened; escalated to P0 as a hard Legal gate — "engineering search alone is insufficient to close T030") | **Diana** | **Charlie** for the engineering step (Apache/MIT parser search, since 2026-08-15), but the close is **Legal's** — the whole-bundle copyleft memo means no engineering action alone clears it. | **Yes, twice over** — assignee Diana, execution Charlie, gate owner Legal |
| **T036 / CIPH-46 — high-DPI coordinate drift** (Blocked; named in Alice's 2026-09-15 gate check but not a T011 close dependency) | **Charlie** | **Upstream `pdf-lib-core` maintainers** (issue filed, no response), with **Alice** owning the pending ship/don't-ship decision — "decide if we can ship with this limitation or if we need a different rendering library." Diana adds that 12% of the MedFirst pilot corpus fails on nested Form XObjects, beyond the 4K scaling bug (CMT-2026-09-001). | **Yes** — assignee Charlie, but the next action is external + an Alice-owned scope decision |

### Already-green dependencies (no action needed)
T001 (core engine, Charlie), T002 (regex detection, Charlie), T003 (batch CLI, Bob), T004 (REST API, Bob), T006 (YAML policy loader, Charlie — subject to the migration caveat above), T010 (security audit, Diana; CORS `*` finding patched to `ALLOWED_ORIGINS`, re-scan 2026-07-15 confirmed, plus a RedByte pen-test attestation letter dated 2026-07-11 in the evidence pack).

### Files supporting these claims
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md` (authoritative T011/T005 state, no-ship deadline, T010 evidence)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-06-platforms.md` (T029 procurement framing, T036)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md` (T016, T030)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-05-performance.md` (T031)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-01-engine.md` (T006 migration dependency)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/index.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-21-Release-v1-Gates.md`, `CIPH-15-Docker-Packaging.md`, `CIPH-39-Windows-Compatibility.md`, `CIPH-26-Audit-Trail-Logging.md`, `CIPH-40-License-Compliance-Review.md`, `CIPH-41-Large-File-Chunking.md`, `CIPH-16-Redaction-Policy-Config.md`, `CIPH-46-High-DPI-PDF-Rendering-Fixes.md` (all under `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/`)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md`, `.../slack/2026-06-25-docker-size.md`, `.../slack/2026-09-10-high-dpi-upstream-block.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-07-12-Release-Checklist.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-06.md` (CMT-2026-06-001, -002), `.../comments/2026-08.md` (CMT-2026-08-002, -003), `.../comments/2026-09.md` (CMT-2026-09-001, -002)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md`
