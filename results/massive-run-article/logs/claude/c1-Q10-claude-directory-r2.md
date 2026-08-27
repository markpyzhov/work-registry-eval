# Write a concise cross-workstream management briefing as of **2026-09-22** covering at least three workstreams: at least two completed milestones that still hold, at least three items of work that were completed then reopened, at least two durable blockers, and the top risks that should escalate before ship. Do not present reopened work as done.

<!-- RESPONSE_START -->

I have everything needed. Here is the briefing.

---

# CipherDoc — Cross-Workstream Management Briefing
**As of 2026-09-22** (Work State index as-of timestamp `2026-09-22T12:00:00Z`)
Workstreams covered: **WS-03 Ops/Release**, **WS-04 Policy/Compliance**, **WS-05 Performance**, **WS-06 Platforms**, **WS-07 Storage**, plus WS-01 Engine and WS-02 API for context. All seven workstreams remain `in_progress`.

## Headline

Release v1.0.0 is under a **security-gate hold** with a **hard no-ship date of 2026-10-15**. Three of the four gate items are not merely unfinished — they are work that was previously called done and then reopened. The delivered feature surface is genuinely strong; the risk is concentrated in packaging, licensing, and evidence-quality gates, not in core capability.

---

## 1. Completed milestones that still hold

These are verified complete and have not been reopened as of 2026-09-22.

| Milestone | Workstream | Evidence of durability |
|---|---|---|
| **T010 / CIPH-20 — Security audit and vulnerability patch** | WS-03 | Medium-severity CORS `*` origin finding patched to configured `ALLOWED_ORIGINS`; **re-scan on 2026-07-15 confirmed the patch holds**, and a RedByte third-party pen-test attestation letter (2026-07-11) supplements internal scan artifacts in the release evidence pack. ClickUp status `Completed`. |
| **T028 / CIPH-38 — Bare-metal performance benchmarks** | WS-05 | 500 pages/minute confirmed on standard enterprise hardware; results published 2026-08-12 on a provisioned bare-metal node. Status `Completed`. Note the earlier environment-provisioning blocker was cleared, not deferred. |
| **T021 / CIPH-31 — AES-256 local encryption at rest** | WS-07 | Redaction outputs encrypted with machine-local key; zero-leakage confirmed in cold-start audit. |
| **T027 / CIPH-37 — Air-gapped mode testing** | WS-06 | 1,000 files processed in a networking-disabled VM. |
| **T012 / CIPH-22 — CLI/API configuration parity** | WS-02 | An initial parity claim was disproved on 2026-07-09 (CLI ignored `custom_regex`); PR #52 fixed engine initialization and 2026-07-11 tests confirmed unified config loading. This one was corrected and **re-verified** — it holds. |
| **T032 / CIPH-42** and **T034 / CIPH-44** | WS-04 / WS-07 | Auditable profile schema export verified against the REST contract (2026-08-16); CSV custom dictionary matching passes the rule suite (2026-08-16). Both `Completed`, no reopen. |

Also durable: T001/T002/T006 (engine core, financial regex, YAML policy loader), T003/T004 (Batch CLI, REST endpoint), T018/T023/T035 (static binary, preview UI, Electron wrapper), T015/T017/T020/T038 (fail-closed batching, policy conflict resolution, HIPAA patterns, telemetry opt-out).

## 2. Work completed then reopened — **not done**

Each of these was closed or merged at some point and is currently open. None should be counted toward release readiness.

1. **T005 / CIPH-15 — Docker packaging** (WS-03). Initial Dockerfile **completed 2026-06-16**, then **reopened 2026-06-25** when Diana's size/CVE review measured the built image at **2.1GB** after OCR dependencies were bundled. Evan moved to multi-stage builds and an Alpine base and stripped unused runtime packages, but as of the 2026-08-12 verification the image **still exceeds the ~450MB GA target and CVE verification is still failing**. ClickUp status: `Active (Reopened)`. Note the dual gate: interim RC may ship at **800MB once CVE-clean**, GA target remains **~450MB** — do not conflate the two on the checklist.
2. **T030 / CIPH-40 — License compliance review** (WS-04). The initial audit completed and drove a PDF parser swap; the task was **reopened on 2026-08-12** when the replacement parser turned out to be **AGPL-licensed**. Charlie has been searching for an Apache/MIT alternative since 2026-08-15. Status: `Active (Reopened)`.
3. **T031 / CIPH-41 — Large-file stream chunking** (WS-05). Chunking **was merged**, then reopened when Bob found severe memory leaks on files exceeding 2GB during long batch runs (2026-08-18). Charlie is refactoring stream buffer release logic (from 2026-08-20). Status: `Active (Reopened)`.
4. **T022 / CIPH-32 — Storage quota management** (WS-07). Original hard-halt behavior shipped, then reopened as too aggressive on production-like batches — it halts with ~500MB free. Bob refactored to a 10% buffer tolerance on 2026-09-18, and the target was retargeted to a **2GB production baseline** (not 500MB) on 2026-09-15. Refactor is in progress, **not verified in clinic VMs**. Status: `Active (Reopened)`.
5. **T016 / CIPH-26 — Compliance audit-trail logging** (WS-04). SHA-256 hashing and schema were built and **CLI integration landed 2026-09-10**, but Diana's **2026-09-18 verification found emitted CLI records inconsistent with the defined schema**. Described in WS-04 as active/reopened; Diana is holding the audit gate red. This is a release blocker, not a completed deliverable.

A related correction worth flagging: **T033 / CIPH-43 (PDF loader memory leak profiling) is genuinely `Completed`** — consumption stable after 10,000 documents. It is easy to confuse with T031's 2GB+ leak, which is a *different, still-open* leak. Do not let T033's completion be read as closing the large-file memory problem.

Separately, **T039 / CIPH-49 (a11y audit) is superseded**, not delivered — folded into the CIPH-33 Preview UI overhaul, which natively covers high-contrast and keyboard navigation.

## 3. Durable blockers

These have persisted across multiple reporting cycles and none has a confirmed clear date.

- **T007 / CIPH-17 — multi-page PDF offset mismatch** (WS-01). Blocked on upstream `pdfminer.six` #992 since June. The maintainer indicated **earliest realistic merge mid-October**; as of 2026-09-10 the PR remains unmerged. The team **evaluated and rejected maintaining a parser fork**, and any pre-normalization workaround requires **written Legal sign-off** in addition to the upstream merge. Blocked roughly three months with a dual upstream+Legal gate.
- **T024 / CIPH-34 — Zero-trust node sync handshake** (WS-07). Nominal-latency validation passed, but the 2026-09-22 high-latency simulation never completes the handshake. The team **explicitly declined a timeout-bump workaround** pending encryption-path stabilization ("bumping timeouts just hides it"). Blocked on the AES-256 wire path — a cross-workstream dependency, so it cannot be unblocked inside WS-07.
- **T019 / CIPH-29 — Offline mode authentication** (WS-04). Key rotation is impossible in a strictly air-gapped environment without a centralized authority. InfoSec **approved** a split master-key escrow design (USB token at clinic + HQ HSM) on 2026-08-05 and Bob is spiking it — but it **remains blocked until built**. The architecture question is closed; the implementation is not.
- **T036 / CIPH-46 — High-DPI PDF rendering** (WS-06). Blocked on upstream rendering-library scaling math; coordinates drift 5–10 pixels on 4K displays at 200% scaling. Compounded on 2026-09-10: **12% of the MedFirst pilot corpus fails due to nested Form XObjects**, a defect class the upstream scaling fix may not cover at all.
- **T037 / CIPH-47 — Async batch scheduler** (WS-05). Concurrent manifest-write race cuts throughput ~10% and **can corrupt JSON under load**.
- **T029 / CIPH-39 — Windows compatibility** (WS-06). Path backslash handling is fixed; the build is held because Defender/SmartScreen flags the unsigned binary. Categorize this correctly: it is a **procurement dependency (Authenticode certificate), not an engineering block** — and there is no budget or timeline on record for the certificate.

## 4. Top risks to escalate before ship

**Ranked by proximity to the 2026-10-15 no-ship deadline.**

1. **The release gate is 23 days out and none of its blockers is green.** T011 cannot close until T005 (Docker size/CVE) and T029 (Windows signing) are both green; the release board set a **hard, non-advisory no-ship after 2026-10-15**. T005 has been reopened since June with no size or CVE pass yet, and T029 waits on a certificate no one has budgeted. *Escalate:* procurement authority for the Authenticode certificate, and an explicit decision on whether to ship the **RC at the 800MB gate** once CVE-clean rather than holding for the ~450MB GA target.
2. **The AGPL exposure is a Legal gate that engineering cannot close.** Legal's 2026-08-12 memo holds that AGPL in the bundle triggers **whole-bundle copyleft exposure for our distribution model** — escalated to P0. Charlie's library search has run six weeks without a named replacement. *Escalate:* this needs a Legal-side decision path (license exception, distribution-model change, or a funded parser migration), not more searching. This is the item most likely to be underestimated because it looks like an engineering task on the board.
3. **The audit trail — our compliance evidence — does not validate.** T016's CLI-emitted records do not match the defined schema (2026-09-18). Diana's framing is the risk: this "undercuts the audit trail as release evidence." For a HIPAA-facing product, shipping with an unvalidated audit log is a compliance risk, not just a bug. It is a fourth open gate flagged in the pre-release audit alongside Docker and Windows.
4. **MedFirst pilot is exposed on three independent fronts.** OOM on a 4.7GB PDF with 8GB RAM (T031, pilot-blocker, explicitly tied to the T011 gate); 12% of the pilot corpus failing High-DPI coordinate alignment (T036); and three legacy JSON policies that must auto-migrate to YAML before cutover (T006 dependency, Evan owns the converter). *Escalate:* a single consolidated MedFirst readiness view — these are tracked in three different workstreams and no one owns the aggregate.
5. **Zero-trust node sync has contradictory guidance that no one has reconciled.** The Singapore field trial reports failures at 180ms RTT and asks for a **30s timeout budget**; the same-day handshake deep-dive **declined any timeout bump** pending encryption-path work. Both are on the record as of 2026-09-22 and they point opposite ways. This is flagged for manual triage and remains unresolved — it needs a decision, not another repro.
6. **Two contractual/deferral commitments are drifting off the release board.** JWT REST auth (T009) is deferred to v1.1, but **MedFirst's enterprise renewal requires REST authentication no later than 2026-03-31** — a contractual exception that must stay on the roadmap. And T008 (OCR fallback) plus T014 (90%-confidence manual review quarantine) are still active with confidence tuning ongoing, gating the scanned-document use case.

---

**Sources:** `work-states/index.md`, `WS-01-engine.md`, `WS-02-api.md`, `WS-03-ops.md`, `WS-04-policy.md`, `WS-05-performance.md`, `WS-06-platforms.md`, `WS-07-storage.md`; `work-states/comments/2026-06.md`, `2026-07.md`, `2026-08.md`, `2026-09.md`; `briefs/2026-09-22-daily-brief.md`; tasks `CIPH-15`, `CIPH-20`, `CIPH-21`, `CIPH-26`, `CIPH-32`, `CIPH-38`, `CIPH-39`, `CIPH-40`, `CIPH-41`, `CIPH-42`, `CIPH-43`, `CIPH-44`; transcripts `2026-09-15-Pre-Release-Audit.md`, `2026-09-22-Handshake-Protocol-Deep-Dive.md` — all under `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/`.
