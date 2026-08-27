# As of the final CipherDoc snapshot on **2026-09-22**, is the toolkit ready to ship v1.0.0? Give a clear go/no-go, name every release gate that is still open, and cite the evidence that keeps each gate from closing.

<!-- RESPONSE_START -->

## Verdict: NO-GO — CipherDoc v1.0.0 is not ready to ship as of the 2026-09-22 snapshot

The authoritative release-gating Work State, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md` (Last Updated 2026-09-22), records T011 / CIPH-21 as **Active under a security-gate hold**, and the index (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/index.md`, as-of 2026-09-22T12:00:00Z) lists T011 among active/reopened items. A hard **no-ship after 2026-10-15** applies if the two named gates aren't green (`CMT-2026-09-002`).

---

### Tier 1 — The two gates named in CIPH-21's acceptance criteria (both open)

**1. T005 / CIPH-15 — Docker image size + CVE verification**
- CIPH-21 acceptance criteria explicitly list this as "not yet met": `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-21-Release-v1-Gates.md`
- Task status "Active (Reopened)"; image ballooned to 2.1GB after OCR bundling; as of the 2026-08-12 verification it still exceeds the ~450MB target and CVE verification remains outstanding: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-15-Docker-Packaging.md`
- Diana, 2026-08-12: still over the ~450MB target and CVE scan still failing; "Reopened status stands until both the size and the CVE check are clean" — `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-06-25-docker-size.md` (SRC-SLACK-06)
- Note the **dual thresholds** (`CMT-2026-06-002`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-06.md`): an interim RC may ship at **800MB once CVE-clean**; GA target remains **~450MB**. Even the RC path is blocked because CVE verification is failing.
- It is also the sole unmet dependency on the July checklist: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-07-12-Release-Checklist.md`

**2. T029 / CIPH-39 — Windows code-signing (Authenticode)**
- Windows path handling is fixed, but release is held: Defender/SmartScreen flag the unsigned binary; the certificate is still not procured — `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md` (SRC-SLACK-37, Evan: "we need the certificate"; Alice: "keep it open on the release gate").
- Task remains Active pending the certificate: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-39-Windows-Compatibility.md`; corroborated in `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-06-platforms.md` (procurement dependency, not an engineering block; budget/timeline sits in Needs Manual Triage).

### Tier 2 — Additional release blockers held open at the 2026-09-15 pre-release audit / by comments

**3. T016 / CIPH-26 — Compliance audit-trail log gate (QA hold, red)**
- Pre-release audit: Diana keeps the audit gate red until CLI-emitted records match the defined schema; Evan: "Release isn't opening with any of those unresolved" — `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md` (SRC-MEET-10)
- 2026-09-18 verification found CLI records inconsistent with the schema; "remains an open release blocker" — `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-26-Audit-Trail-Logging.md`; also `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md` (T016 active/reopened).

**4. T030 / CIPH-40 — License compliance, P0 hard Legal gate**
- Legal memo: AGPL in the bundle triggers whole-bundle copyleft exposure; escalated to P0, "engineering search alone is insufficient to close T030" — `CMT-2026-08-002` in `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-08.md`
- Task reopened after the replacement PDF parser turned out AGPL; Charlie still searching for an Apache/MIT alternative — `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-40-License-Compliance-Review.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md` (Needs Manual Triage), and the 2026-09-22 brief lists it as a still-open P0 Legal gate: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md`

**5. T031 / CIPH-41 — Large-file memory leak, explicitly tied to the T011 gate**
- `CMT-2026-08-003`: MedFirst pilot OOM on a 4.7GB PDF with 8GB RAM; "tie explicitly to the T011 release gate" — `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-08.md`
- Reopened; buffer-release refactor still in flight — `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-41-Large-File-Chunking.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-05-performance.md`; 2026-09-22 brief still lists it as "release-coupled".

**6. T006 legacy JSON→YAML policy migration — release dependency tied to the T011 gate**
- `CMT-2026-06-001`: MedFirst's three legacy JSON production policies "must auto-migrate before we cut over… treat migration as a release dependency tied to T006 and the T011 gate"; Evan owns the converter. No later record shows the converter delivered — `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-06.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-01-engine.md` (still under Active Work).

**7. T036 / CIPH-46 — High-DPI PDF rendering (open on the pre-release board; ship-with-known-issue decision not made)**
- Alice's gate check on 2026-09-15 keeps it "on the board" — SRC-MEET-10 (path above).
- Blocked on upstream `pdf-lib-core`; no local patch possible; maintainers unresponsive; Alice: decide whether to ship with the limitation or swap the rendering library — `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-09-10-high-dpi-upstream-block.md` (SRC-SLACK-58)
- Scope is wider than the 4K scaling bug: 12% of the MedFirst pilot corpus fails on nested Form XObjects — `CMT-2026-09-001` (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-09.md`), `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-06-platforms.md`

---

### Open work not named as a v1.0 release gate (context, not gating per the records)
T007 (upstream `pdfminer.six` #992, earliest mid-October, plus written Legal sign-off — `CMT-2026-06-003`, WS-01), T008 OCR fallback and T014 OCR quarantine (WS-01, WS-04), T019 offline-auth key escrow (Blocked, `CMT-2026-08-001`, WS-04), T022 storage quota 2GB baseline refactor (`CMT-2026-09-003`, WS-07), T024 zero-trust handshake at high latency (Blocked, `CMT-2026-09-004`, SRC-MEET-11, WS-07), T037 async batch I/O race (Blocked, WS-05). T009 (REST auth) is deferred to v1.1 and T039 (a11y) is superseded — neither gates v1.0 (index.md, WS-04).

### Bottom line
Two contractual CIPH-21 gates (Docker size/CVE, Windows signing) plus four more release-coupled holds (audit-log schema, AGPL Legal gate, large-file OOM, MedFirst policy migration) are open, with high-DPI rendering unresolved pending a ship/no-ship-with-known-issue decision. Nothing in the 2026-09-22 records clears any of them. Ship date is constrained by the hard 2026-10-15 no-ship boundary.
