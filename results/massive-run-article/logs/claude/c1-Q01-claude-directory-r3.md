# As of the final CipherDoc snapshot on **2026-09-22**, is the toolkit ready to ship v1.0.0? Give a clear go/no-go, name every release gate that is still open, and cite the evidence that keeps each gate from closing.

<!-- RESPONSE_START -->

## Verdict: **NO-GO** — CipherDoc is not ready to ship v1.0.0 as of the 2026-09-22 snapshot

The release-gate task itself (`T011` / CIPH-21) is still **Active** under a security-gate hold, and the release board has attached a **hard no-ship deadline of 2026-10-15** if the primary gates are not green. Work State index as-of timestamp: `2026-09-22T12:00:00Z`.

Evidence: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-21-Release-v1-Gates.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/index.md`

---

### Tier 1 — The two hard no-ship gates (T011's stated blocking dependencies)

**1. T005 / CIPH-15 — Docker image size + CVE verification — Active (Reopened)**
- Image ballooned to 2.1GB after OCR dependencies were bundled; reopened 2026-06-25. Evan applied multi-stage builds, swapped Ubuntu → Alpine, and stripped unused OCR/runtime packages, but at the **2026-08-12 verification the image was still over the ~450MB target and the CVE scan was still failing**. Diana: reopened status stands until both size and CVE checks are clean.
- Complication: **dual size gates** — interim RC may ship at 800MB *once CVE-clean*; GA target remains ~450MB. Neither threshold is currently satisfied because CVE verification itself is failing.
- Files: `work-states/WS-03-ops.md`, `med-synth/tasks/CIPH-15-Docker-Packaging.md`, `med-synth/communication/sources/slack/2026-06-25-docker-size.md` (SRC-SLACK-06), `work-states/comments/2026-06.md` (CMT-2026-06-002)

**2. T029 / CIPH-39 — Windows Authenticode code-signing — Active**
- Windows path/backslash handling is fixed and a Windows build artifact exists, but **Defender and SmartScreen flag the unsigned binary** — pilot installs warn at best, get blocked at worst. Evan (2026-09-02): "this isn't something we can work around on the engineering side, we need the certificate." Alice kept it on the release gate and is chasing procurement.
- This is a **procurement dependency, not an engineering one** — no amount of dev work closes it. Budget/timeline for the cert is still in Needs Manual Triage.
- Files: `work-states/WS-06-platforms.md`, `med-synth/tasks/CIPH-39-Windows-Compatibility.md`, `med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md` (SRC-SLACK-37)

**Deadline evidence:** Release board decision (Diana, 2026-09-15): no-ship after **2026-10-15** if T005 and T029 are not green — "Hard deadline — not advisory." — `work-states/comments/2026-09.md` (CMT-2026-09-002)

---

### Tier 2 — Additional gates explicitly held open as release blockers

**3. T016 / CIPH-26 — Compliance audit-trail logging — Active, gate held RED**
- Bob wired audit-log generation into the CLI on 2026-09-10, but Diana's **2026-09-18 verification found CLI-emitted records inconsistent with the defined companion JSON schema**. Diana at the 2026-09-15 pre-release audit: "That undercuts the audit trail as release evidence… I'll keep the audit-log gate red until schema and records match." Charlie confirmed it's schema-vs-emitted-records, not packaging.
- Files: `med-synth/tasks/CIPH-26-Audit-Trail-Logging.md`, `med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md` (SRC-MEET-10), `work-states/WS-04-policy.md`

**4. T030 / CIPH-40 — License compliance / AGPL — Active (Reopened), P0 hard Legal gate**
- The replacement PDF parser adopted after the initial audit turned out to be **AGPL-licensed**. Legal memo (2026-08-12): AGPL in the bundle triggers **whole-bundle copyleft exposure** for the distribution model; escalated to P0 and treated as a hard Legal gate — "engineering search alone is insufficient to close T030." Charlie is still searching for an Apache/MIT alternative; none found as of the 2026-09-22 brief.
- Files: `med-synth/tasks/CIPH-40-License-Compliance-Review.md`, `work-states/comments/2026-08.md` (CMT-2026-08-002), `work-states/WS-04-policy.md`

**5. T031 / CIPH-41 — Large-file stream chunking / memory leak — Active (Reopened), explicitly tied to T011**
- Chunking merged, then reopened: files over 2GB still leak memory during long batch runs. **MedFirst pilot hit OOM on a 4.7GB PDF on an 8GB-RAM clinic workstation.** Bob's instruction: "tie explicitly to the T011 release gate." Charlie is still refactoring stream-buffer release logic; the 2026-09-22 brief still lists it as "release-coupled."
- Files: `med-synth/tasks/CIPH-41-Large-File-Chunking.md`, `work-states/comments/2026-08.md` (CMT-2026-08-003), `work-states/WS-05-performance.md`

**6. T036 / CIPH-46 — High-DPI PDF rendering coordinates — Blocked (ship/no-ship decision unmade)**
- Alice at the pre-release audit listed it among gates that "stay on the board." Redaction coordinates drift 5–10px on 4K displays at 200% scaling; root cause is a bug deep in the `pdf-lib-core` C++ core that Charlie says cannot be patched locally, and upstream maintainers have not responded. Scope then widened: offline QA found **12% of the MedFirst pilot corpus fails coordinate alignment due to nested Form XObjects** — beyond the upstream scaling bug, so the upstream fix alone may not cover it. Flattening was floated and rejected (file-size blowup, text-layer loss).
- The open decision — "ship with this limitation as a documented known issue, or swap rendering libraries" — is **still unmade**, which is what keeps this gate ambiguous rather than closed.
- Files: `med-synth/communication/sources/slack/2026-09-10-high-dpi-upstream-block.md` (SRC-SLACK-58), `work-states/comments/2026-09.md` (CMT-2026-09-001), `work-states/WS-06-platforms.md`

---

### Tier 3 — One easily-missed release dependency

**7. T006 legacy JSON → YAML policy migration**
- T006 (policy config loading) is marked complete, **but a separate migration requirement rides on it**: MedFirst has three legacy JSON pilot policies in production that must auto-migrate before cutover. Alice: "treat migration as a release dependency tied to T006 **and the T011 gate**." Evan owns the JSON→YAML converter; the package contains no evidence the converter shipped or was verified.
- Files: `work-states/comments/2026-06.md` (CMT-2026-06-001), `work-states/WS-01-engine.md`

---

### Not gates, but open — context for the go/no-go

These are open items the snapshot does *not* tie to the v1.0.0 release gate, so they don't independently block ship:

- **T007** (offset mismatch) — Blocked on upstream `pdfminer.six` #992, earliest merge mid-October; any pre-normalization workaround also needs **written Legal sign-off** (`work-states/WS-01-engine.md`, CMT-2026-06-003)
- **T024** (zero-trust node sync) — Blocked; Singapore field trial fails at 180ms RTT with the 5s prototype timeout, needs a 30s budget, but the 2026-09-22 deep-dive declined a timeout bump pending encryption-path stabilization (`work-states/WS-07-storage.md`, CMT-2026-09-004, SRC-MEET-11)
- **T019** (offline auth) — Blocked; split master-key escrow approved by InfoSec but unimplemented
- **T037** (async batch scheduler) — Blocked on a concurrent manifest-write race that can corrupt JSON under load
- **T008** (OCR fallback), **T014** (OCR manual-review quarantine), **T022** (quota buffer, retargeted to a 2GB baseline) — all still active
- **T009** (REST JWT auth) — deliberately **deferred to v1.1**; not a v1.0.0 blocker, though MedFirst's contract requires it by 2026-03-31
- **T039** (a11y audit) — **superseded**, folded into the CIPH-33 Preview UI overhaul

### What *is* green
T001–T004, T006, T010, T012 (the original checklist dependencies T001–T006 + T010 are all satisfied per CIPH-21's acceptance criteria and the 2026-07-12 Release Checklist), plus T013, T015, T017, T018, T020, T021, T023, T025–T028, T032–T035, T038. The security audit (T010) is complete with the CORS finding patched and re-scan-confirmed, backed by a RedByte pen-test attestation letter in the evidence pack.

### Bottom line
Six of seven original checklist dependencies were already met back in July; the release has been held ever since on gates that were *added* or reopened after that draft. **Two gates are formally no-ship (T005, T029), four more are held open as release blockers (T016, T030, T031, T036), and one release dependency (T006 legacy-policy migration) has no closure evidence.** Two of the blockers — the Windows certificate and the AGPL parser — cannot be closed by engineering effort at all; they need procurement and Legal respectively. With 23 days to the 2026-10-15 no-ship date, ship v1.0.0: **no**.
