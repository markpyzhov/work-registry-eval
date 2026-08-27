# Write a concise cross-workstream management briefing as of **2026-09-22** covering at least three workstreams: at least two completed milestones that still hold, at least three items of work that were completed then reopened, at least two durable blockers, and the top risks that should escalate before ship. Do not present reopened work as done.

<!-- RESPONSE_START -->

## CipherDoc — Cross-Workstream Management Briefing
**As of 2026-09-22** (Work State index as-of `2026-09-22T12:00:00Z`). Source of truth: the seven Work States in `work-states/`; provenance from `SRC-*` / `CMT-*` records. Root for all paths below: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/`

---

### 1. Headline

All seven workstreams are `in_progress`. A meaningful body of v1.0.0 capability is genuinely finished and stable, but the release itself is gated by **five open items, three of which are re-openings of work that was previously declared complete**, and by a **hard no-ship date of 2026-10-15**. Two of the gating items (Windows code-signing, License/AGPL) cannot be closed by engineering at all — they are procurement and Legal dependencies.

---

### 2. Completed milestones that still hold

These are closed in their Work States and no later record reopens them.

| Milestone | Workstream | Evidence |
|---|---|---|
| **T010 / CIPH-20 — Security audit & vulnerability scans** | WS-03 Ops | Medium-severity CORS `*` origin finding patched to configured `ALLOWED_ORIGINS`; re-scans on 2026-07-15 confirmed the patch holds. Supplemented by the RedByte third-party pen-test attestation letter (2026-07-11) in the release evidence pack. `WS-03`, `CMT-2026-07-002` |
| **T021 / CIPH-31 — AES-256 local encryption at rest** | WS-07 Storage | Outputs encrypted with a machine-local AES-256 key; zero-leakage confirmed in cold-start audit. `WS-07` |
| **T033 / CIPH-43 — PDF loader memory-leak patch** | WS-05 Perf | Loader leak patched; consumption stable after 10,000 documents. Tooling decision: cloud profiler superseded by native `tracemalloc` for air-gapped use. `WS-05` |
| **T027 / CIPH-37 — Air-gapped mode testing** | WS-06 Platforms | 1,000 files processed in a networking-disabled VM. `WS-06` |
| **T015 / CIPH-25 — Batch fail-closed** | WS-04 Policy | Atomic rename ensures no partial output; Diana QA-validated "no output file on failure" plus secure temp deletion on 2026-07-16. `WS-04` |
| **T012 / CIPH-22 — CLI/API configuration parity** | WS-02 API | Note the history: an *initial* parity claim was disproved 2026-07-09 (CLI ignored `custom_regex`); PR #52 fixed engine initialization and 2026-07-11 tests confirmed unified config loading. **This one was corrected and re-verified — it now holds.** `WS-02` |

Also closed and holding: T001/T002/T006 (core engine, financial regex, YAML policy loader — WS-01), T003/T004 (Batch CLI, REST endpoint — WS-02), T013/T017/T020/T032/T038 (policy matrix, conflict resolution, HIPAA dictionary, auditable profile export, telemetry opt-out — WS-04), T026/T028 (16-core process pool, 500 pages/min benchmark — WS-05), T018/T023/T035 (static binary, preview UI, Electron wrapper — WS-06), T025/T034 (ephemeral cleanup, CSV dictionaries — WS-07).

---

### 3. Work completed and then reopened — **NOT done**

Each of the following was declared complete at some point and is now open again. None should appear as "done" in any status roll-up.

**1. T005 / CIPH-15 — Docker packaging (WS-03 Ops) — `Active (Reopened)`**
Initial Dockerfile completed 2026-06-16 at ~800MB. Diana reopened it 2026-06-25 when the built image measured **2.1GB** after OCR dependencies were bundled. Evan applied multi-stage builds, swapped `ubuntu:22.04` → `alpine:latest` (via `gcompat`), and removed unused OCR/runtime packages. As of the **2026-08-12** verification the image is **still over the ~450MB target and CVE verification is still failing**; Diana explicitly stated reopened status stands until both are clean. Note the dual gate from CISO review: an interim RC may ship at **800MB once CVE-clean**, GA target remains ~450MB — do not conflate them. `WS-03`, `SRC-SLACK-06`, `SRC-CU-CIPH-15`, `CMT-2026-06-002`

**2. T030 / CIPH-40 — License compliance review (WS-04 Policy) — `Active (Reopened)`, P0**
An initial audit was closed by swapping the PDF parser. Reopened **2026-08-12** when the replacement parser was found to be **AGPL-licensed**. Charlie is searching for an Apache/MIT alternative. Engineering search alone cannot close this (see risks). `WS-04`, `SRC-SLACK-40`, `SRC-CU-CIPH-40`, `CMT-2026-08-002`

**3. T031 / CIPH-41 — Large-file stream chunking (WS-05 Perf) — `Active (Reopened)`**
Chunking merged, then reopened **2026-08-18** when Bob found memory still leaking on files >2GB during long batch runs — something retains references so buffers are never freed; Diana reproduced the process being OOM-killed in QA. Charlie is refactoring stream buffer release. **This is distinct from the closed T033 loader-leak fix — do not treat T033's completion as covering T031.** `WS-05`, `SRC-SLACK-43`, `SRC-CU-CIPH-41`, `CMT-2026-08-003`

**4. T022 / CIPH-32 — Storage quota management (WS-07 Storage) — `Active (Reopened)`**
Verified and called done 2026-08-06 against a 500MB floor. Reopened **2026-09-15** — production-like batches tripped the hard halt before doing useful work. Bob's 10% buffer-tolerance refactor landed 2026-09-18 and Evan re-tested cleanly, **but the item remains reopened/active in WS-07**: Ops capacity planning has since retargeted the production baseline to **2GB free disk (not 500MB)** plus the 10% buffer, and re-verification in clinic VMs against the new baseline has not been recorded. `WS-07`, `SRC-SLACK-23`, `SRC-CU-CIPH-32`, `CMT-2026-09-003`

**5. T016 / CIPH-26 — Compliance audit-trail logging (WS-04 Policy) — `active/reopened`**
SHA-256 hashing and schema definition landed; CLI wiring completed 2026-09-10. Diana's **2026-09-18** verification found CLI-emitted audit records inconsistent with the defined schema. The 2026-09-15 pre-release audit holds the audit gate red — it undercuts the audit trail as release evidence. `WS-04`, `SRC-CU-CIPH-26`, `SRC-MEET-10`

---

### 4. Durable blockers (long-running, not resolvable this sprint)

**T007 / CIPH-17 — Multi-page PDF offset mismatch (WS-01 Engine) — blocked since June.**
Blocked on upstream `pdfminer.six` issue/PR **#992**. Charlie monitored the repo through August and evaluated a local fork in late August; the team **rejected maintaining a parser fork**. As of 2026-09-10 the PR remains unmerged and no safe local workaround exists. Maintainer DM puts earliest realistic merge at **mid-October**, and any pre-normalization workaround additionally requires **written Legal sign-off**. `WS-01`, `CMT-2026-06-003`

**T019 / CIPH-29 — Offline mode authentication (WS-04 Policy) — blocked.**
Key rotation is impossible in a strictly air-gapped environment without a centralized authority; only local mockups exist. InfoSec approved a split master-key escrow design (USB token at clinic + HQ HSM) and Bob is spiking it — the architecture question is settled, but **escrow remains unimplemented**, so the item stays blocked. `WS-04`, `SRC-SLACK-17`, `CMT-2026-08-001`

**T024 / CIPH-34 — Zero-trust node sync handshake (WS-07 Storage) — blocked.**
Nominal-latency validation passed, but high-latency simulation times out — the handshake never completes on slow links. The 2026-09-22 deep-dive **explicitly declined a timeout bump** ("bumping timeouts just hides it") and left the item blocked pending encryption-path stabilization; the high-latency repro stays in place for re-check. `WS-07`, `SRC-MEET-11`, `SRC-SLACK-27`

**T036 / CIPH-46 — High-DPI PDF rendering (WS-06 Platforms) — blocked.**
Redaction coordinates drift 5–10 pixels on 4K displays at 200% scaling, rooted in upstream rendering-library scaling math. Diana's offline QA adds scope: **12% of the MedFirst pilot corpus fails on nested Form XObjects**, which the upstream scaling fix may not cover. `WS-06`, `SRC-SLACK-58`, `CMT-2026-09-001`

**T037 / CIPH-47 — Async batch scheduler (WS-05 Perf) — blocked.**
Concurrent manifest-write race cuts throughput ~10% and can corrupt JSON under load. `WS-05`, `SRC-SLACK-61`

---

### 5. Top risks to escalate before ship

1. **The 2026-10-15 no-ship deadline is a hard board decision, and one of its two conditions is outside engineering control.** T011 cannot close until T005 (Docker size/CVE) and T029 (Windows Authenticode certificate) are green. As of 2026-09-02 the certificate is still not procured; Evan's position is explicit — "this isn't something we can work around on the engineering side." Windows path handling is fixed; only signing holds it. **Escalate the certificate purchase as a procurement item with a named owner and date.** `WS-03`, `WS-06`, `CMT-2026-09-002`, `SRC-SLACK-37`

2. **T030 AGPL exposure is a Legal P0, not a library-shopping exercise.** The Legal memo states AGPL in the bundle triggers **whole-bundle copyleft exposure** for the current distribution model, and that an engineering search alone is insufficient to close it. This compounds with T007 — the parser layer is simultaneously blocked upstream and license-constrained. `CMT-2026-08-002`, `WS-04`

3. **The audit-log gate is red and is compliance evidence, not a nice-to-have.** T016's CLI-vs-schema mismatch (found 2026-09-18) was named in the pre-release audit as a release hold alongside Docker and Windows, yet it does **not** appear in the index's Key Blockers line. Confirm it is tracked on the release board with the same weight as T005/T029. `SRC-MEET-10`, `SRC-CU-CIPH-26`

4. **MedFirst pilot is exposed on two fronts.** T031's OOM on a 4.7GB PDF with 8GB RAM is a designated pilot-blocker tied explicitly to the T011 gate; T036's Form XObject failures hit 12% of the same pilot corpus. Additionally, T006's legacy JSON→YAML auto-migration (three production pilot policies, Evan owning the converter) is a release dependency on the T011 gate that is easy to lose behind the "T006 done" checkbox. `CMT-2026-08-003`, `CMT-2026-09-001`, `CMT-2026-06-001`

5. **Unresolved direction conflict on T024 needs a decision owner.** The Singapore field trial reports failure at 180ms RTT with the 5s prototype timeout and asks for a **30s timeout budget**; the same-day deep-dive refused any timeout bump pending encryption-path work. Both are open records; neither supersedes the other. Flagged for manual triage in WS-07 — it will not resolve itself. `CMT-2026-09-004` vs `SRC-MEET-11`

6. **Deferred-but-contractual: T009 REST JWT auth.** Deferred to v1.1 on the reasoning that v1.0.0 targets local single-machine use — but MedFirst's enterprise IT renewal requires REST authentication **no later than 2026-03-31**. This is a roadmap commitment that must not be lost when v1.0.0 ships. `WS-02`, `CMT-2026-07-001`

**Also note, so it isn't mistaken for open work:** T039 / CIPH-49 (standalone a11y audit) is **superseded**, not pending — the Preview UI overhaul (CIPH-33) natively covers high-contrast and keyboard navigation. `WS-04`, `SRC-SLACK-67`

---

### Sources cited (absolute paths)

Work States and index: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/index.md`, `.../work-states/WS-01-engine.md`, `WS-02-api.md`, `WS-03-ops.md`, `WS-04-policy.md`, `WS-05-performance.md`, `WS-06-platforms.md`, `WS-07-storage.md`
Comments: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-06.md` (CMT-2026-06-001/-002/-003), `.../comments/2026-07.md` (CMT-2026-07-001/-002), `.../comments/2026-08.md` (CMT-2026-08-001/-002/-003), `.../comments/2026-09.md` (CMT-2026-09-001/-002/-003/-004)
Brief: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md`
Tasks: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-15-Docker-Packaging.md`, `CIPH-21-Release-v1-Gates.md`, `CIPH-26-Audit-Trail-Logging.md`, `CIPH-32-Storage-Quota-Management.md`, `CIPH-39-Windows-Compatibility.md`, `CIPH-40-License-Compliance-Review.md`, `CIPH-41-Large-File-Chunking.md`, `CIPH-47-Async-Batch-Processing.md`
Meetings: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md`, `.../fireflies/2026-09-22-Handshake-Protocol-Deep-Dive.md`
Slack: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-06-25-docker-size.md`, `.../slack/2026-08-06-storage-quota-halt.md`, `.../slack/2026-08-12-license-agpl-reopen.md`, `.../slack/2026-08-18-large-file-chunking-reopen.md`, `.../slack/2026-09-02-windows-signing-gap.md`, `.../slack/2026-09-10-high-dpi-upstream-block.md`, `.../slack/2026-08-25-async-batch-io-race.md`, `.../slack/2026-08-04-offline-auth-mock-block.md`, `.../slack/2026-08-08-node-sync-handshake-validation.md`, `.../slack/2026-08-24-a11y-superseded.md`
