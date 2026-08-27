# As of the final CipherDoc snapshot on **2026-09-22**, is the toolkit ready to ship v1.0.0? Give a clear go/no-go, name every release gate that is still open, and cite the evidence that keeps each gate from closing.

<!-- RESPONSE_START -->

## Verdict: NO-GO for v1.0.0 as of the 2026-09-22 snapshot

The release-gate work state is explicit: WS-03 is `in_progress`, `T011` (CIPH-21, "Manage Release v1.0.0 gates and docs") is unchecked and sitting under an active security-gate hold, and the 2026-09-22 daily brief still leads with "Security-gate hold remains." Nothing in the snapshot clears it.

Evidence: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/index.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-21-Release-v1-Gates.md`

---

## Open gates

### 1. T005 / CIPH-15 — Docker image size + CVE verification (formal T011 dependency)
Status **Active (Reopened)**. Reopened 2026-06-25 when the image measured 2.1GB after OCR bundling. Evan shipped a multi-stage build, swapped `ubuntu:22.04` → `alpine:latest` (with `gcompat` for glibc/musl), and stripped unused OCR/runtime packages — but Diana's 2026-08-12 check found the image **still over the ~450MB target and CVE verification still failing**. Diana: reopened status stands until both size and CVE are clean.

Note the dual threshold from the CISO review (`CMT-2026-06-002`): an interim RC may ship at 800MB **once CVE-clean**; GA target stays ~450MB. Since CVE verification is failing, even the relaxed RC threshold is unmet.

- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-15-Docker-Packaging.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-06-25-docker-size.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-06.md` (`CMT-2026-06-002`)

### 2. T029 / CIPH-39 — Windows Authenticode code-signing (formal T011 dependency)
Status **Active**. Backslash path handling is fixed and a Windows build artifact exists, but Windows Defender/SmartScreen flags the unsigned binary — "every pilot install is going to trip a warning at best, get blocked outright at worst" (Evan, 2026-09-02). Alice kept it on the release gate and took the certificate procurement. This is a **procurement dependency, not an engineering block**, so no amount of dev work closes it; budget/timeline for the cert is still in WS-06 "Needs Manual Triage."

- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-39-Windows-Compatibility.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-06-platforms.md`

### 3. T016 / CIPH-26 — Audit-trail log schema mismatch (release hold added at the pre-release audit)
Status **Active/reopened**. Bob wired SHA-256 audit-log generation into the CLI batch path on 2026-09-10; Diana's 2026-09-18 verification found the **CLI-emitted records inconsistent with the defined companion JSON schema**. At the 2026-09-15 pre-release audit Diana called it "still a hold… that undercuts the audit trail as release evidence" and said she'll keep the gate red until schema and records match. This is not a packaging problem — it is schema versus emitted records.

- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-26-Audit-Trail-Logging.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md`

### 4. T030 / CIPH-40 — License compliance (hard P0 Legal gate)
Status **Active (Reopened)**. The replacement PDF parser adopted during the initial audit turned out to be AGPL. Legal's 2026-08-12 memo escalated it to P0: AGPL in the bundle triggers **whole-bundle copyleft exposure** for the distribution model, and "engineering search alone is insufficient to close T030." Charlie is still hunting an Apache/MIT alternative; the 2026-09-22 brief still lists it as open and ranks it #3 in priority order.

- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-40-License-Compliance-Review.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-08.md` (`CMT-2026-08-002`)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md`

### 5. T031 / CIPH-41 — Large-file chunking / MedFirst OOM (explicitly tied to the T011 gate)
Status **Active (Reopened)**. Chunking merged, then reopened when files over 2GB still leaked memory; Charlie is refactoring buffer release. Bob's 2026-08-18 correction records a MedFirst pilot **OOM on a 4.7GB PDF with 8GB RAM** on a clinic workstation and instructs the team to "tie explicitly to the T011 release gate." The 2026-09-22 brief still lists T031 as "release-coupled."

- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-41-Large-File-Chunking.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-08.md` (`CMT-2026-08-003`)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-05-performance.md`

### 6. T036 / CIPH-46 — High-DPI PDF rendering (on the gate board, ship/no-ship decision unmade)
**Blocked** upstream. Redaction coordinates drift 5–10 px on 4K displays at 200% scaling; the root cause is a bug deep in `pdf-lib-core`'s C++ handling of XObject coordinates under a parent transform — Charlie: not patchable, upstream maintainers unresponsive. Diana's offline QA adds that **12% of the MedFirst pilot corpus** fails coordinate alignment on nested Form XObjects, beyond the 4K scaling bug alone. Alice explicitly deferred the call: "decide if we can ship with this limitation or if we need a different rendering library entirely." At the 2026-09-15 gate check she confirmed it "stays on the board."

- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-09-10-high-dpi-upstream-block.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-09.md` (`CMT-2026-09-001`)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-06-platforms.md`

### 7. T006 / CIPH-16 — Legacy JSON→YAML policy auto-migration (release dependency on the T011 gate)
T006 itself is checked complete (YAML loader merged), but Alice's MedFirst call recorded a residual requirement: three legacy JSON pilot policies in production **must auto-migrate before cutover**, Evan owns the JSON→YAML converter, and "migration is a release dependency tied to T006 and the T011 gate." It sits in WS-01 Active Work with no completion evidence anywhere in the snapshot.

- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-06.md` (`CMT-2026-06-001`)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-01-engine.md`

---

## The deadline that makes this urgent

The release board set a **hard no-ship after 2026-10-15** if T005 and T029 are not green — recorded as a decision, "not advisory." That leaves 23 days from the snapshot date, with a certificate procurement and a failing CVE scan on the critical path.

- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-09.md` (`CMT-2026-09-002`)

## What is *not* blocking v1.0.0

- **T009 / CIPH-19 (JWT REST auth)** — deliberately **deferred to v1.1**; v1.0.0 targets local single-machine use where auth is not a release blocker. Caveat: MedFirst's IT renewal contractually requires REST auth by 2026-03-31, so it cannot slip indefinitely. (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-02-api.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-07.md`)
- **T039 / CIPH-49 (a11y audit)** — **superseded**, folded into the CIPH-33 Preview UI overhaul which natively covers high-contrast and keyboard navigation. (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md`)
- **T010 / CIPH-20 (security audit)** — the one gate that is genuinely **closed**: the medium-severity CORS `*` origin finding was patched to configured `ALLOWED_ORIGINS`, re-scans on 2026-07-15 confirmed the fix, and a RedByte pen-test attestation letter (2026-07-11) is in the evidence pack. (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-07.md`)

Also still open but not identified as v1.0.0 gates in the snapshot: T007 (upstream `pdfminer.six` #992, earliest merge mid-October, plus a Legal sign-off requirement for any workaround), T008 (OCR fallback), T014 (OCR quarantine threshold), T019 (offline auth escrow), T022 (2GB quota baseline), T024 (zero-trust handshake at 180ms RTT), and T037 (async batch I/O race).

**Bottom line:** of the seven original checklist dependencies, six are met — but the release cannot open. Two formal gates (Docker, Windows signing) plus four additional release-coupled holds (audit-log schema, AGPL/Legal, large-file OOM, high-DPI) and one unverified migration dependency all remain unresolved, and the hardest one — the Authenticode certificate — is not something engineering can close.
