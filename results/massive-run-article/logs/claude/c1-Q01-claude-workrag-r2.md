# As of the final CipherDoc snapshot on **2026-09-22**, is the toolkit ready to ship v1.0.0? Give a clear go/no-go, name every release gate that is still open, and cite the evidence that keeps each gate from closing.

<!-- RESPONSE_START -->

## Verdict: **NO-GO** — CipherDoc is not ready to ship v1.0.0 as of the 2026-09-22 snapshot

The authoritative Work State **WS-03: Packaging, Release gating, and Security** (`path = work-state`, Last Updated 2026-09-22) is `in_progress`, P0, owner Evan. Its release-gate task `T011 / CIPH-21` is unchecked and **active under a security-gate hold**, and `CIPH-21` itself is still **Status: Active** with the note that Diana placed a security-gate hold pending T005 and T029. Nothing in the dataset records a gate closing after the 2026-09-15 pre-release audit.

A hard backstop is also on the record: **CMT-2026-09-002** (Diana, 2026-09-15) — the release board set a **no-ship after 2026-10-15** if T005 and T029 are not green, described as "hard deadline — not advisory."

---

### Open release gates and the evidence keeping each open

**1. T005 / CIPH-15 — Docker image size and CVE verification** *(named blocker on the T011 checklist)*
- CIPH-15 is **Status: Active (Reopened)**. Acceptance criteria explicitly record "Image size reduced to the ~450MB target (**not yet met**)" and "CVE verification passes with no outstanding findings (**not yet met**)."
- The image ballooned to 2.1GB after OCR dependencies were bundled; Diana reopened it 2026-06-25 (SRC-SLACK-06). Evan's multi-stage build, Alpine base swap, and removal of unused OCR/runtime packages all failed to close it — on 2026-08-12 Diana ran the check: "We're still over the ~450MB target, and the CVE verification is still failing." Evan: "There's still fluff in the Python site-packages layer, and I need to chase down what's tripping the CVE scan." Diana: "Reopened status stands until both the size and the CVE check are clean."
- Note the **dual thresholds** (CMT-2026-06-002, Evan, 2026-06-25, CISO review): an interim release candidate may ship at **800MB once CVE-clean**; **GA target remains ~450MB**. Even the softer RC threshold is unreachable today because CVE verification is still failing.
- The 2026-07-12 Release Checklist (SRC-GDOC-05) already recorded T005 as the sole unmet dependency of seven; the situation has not improved since.

**2. T029 / CIPH-39 — Windows Authenticode code-signing** *(named blocker on the T011 checklist)*
- CIPH-39 is **Status: Active**. Acceptance criteria require a code-signed build that passes Defender/SmartScreen without warnings — not met.
- SRC-SLACK-37 (2026-09-02): Evan — "Windows Defender and SmartScreen are both flagging the build for pilot testers… We still don't have one [a certificate]. Until we do, every pilot install is going to trip a warning at best, get blocked outright at worst… this isn't something we can work around on the engineering side, we need the certificate." Alice: "Let's keep it open on the release gate rather than pushing it off the board."
- SRC-GDOC-39 (Compatibility Audit, 2026-09-02): packaging is *not* the blocker (backslash path fix landed 2026-08-10; artifact produced 2026-08-12) — the sole open blocker is certificate procurement, which "is holding… the T011 release checklist… alongside the T005 image slim-down."
- WS-06 confirms this is a **procurement dependency, not an engineering block**, and lists "Budget and procurement timeline for Windows Authenticode code-signing certificate" under Needs Manual Triage.

**3. T016 / CIPH-26 — Audit-log schema alignment** *(release hold raised at the pre-release audit)*
- CIPH-26 is **Status: Active**, priority High, with acceptance criterion "CLI-emitted audit records validate cleanly against the defined companion JSON schema (**currently failing verification**)."
- Activity history, 2026-09-18, Diana — "Verification found the CLI-emitted audit records inconsistent with the defined schema; this mismatch remains an open release blocker." This is the **latest dated evidence in the whole gate picture**, four days before the snapshot.
- SRC-MEET-10 (2026-09-15): Diana — "Still a hold. The CLI path and the log records aren't matching the schema we defined. That undercuts the audit trail as release evidence… Until those match, I can't clear the audit gate… I'll keep the audit-log gate red." WS-04 carries this as active/reopened.

**4. T036 / CIPH-46 — High-DPI PDF coordinate scaling (upstream)** *(listed as still-open at the pre-release gate check)*
- CIPH-46 is **Status: Blocked**. Alice at the 2026-09-15 audit: "we're still blocked upstream on the high-DPI rendering bug. Those stay on the board."
- SRC-GDOC-49 (2026-09-10): the defect is in the upstream `pdf-lib-core` scaling math; "No safe local fix has been identified yet." Charlie (SRC-SLACK-58): the bug is "deep in their C++ core," he opened an upstream issue, maintainers have not responded, and flattening PDFs as a workaround would inflate file size and risk losing text layers.
- CMT-2026-09-001 (Diana, 2026-09-10) widens the scope: **12% of the MedFirst pilot corpus** fails coordinate alignment due to nested Form XObjects, so an upstream scaling fix alone may not cover it.
- Ship/no-ship disposition is **undecided**: Alice — "We need to decide if we can ship with this limitation or if we need a different rendering library entirely." Diana proposed documenting it as a known issue. No decision is recorded, so it cannot be treated as waived.

**5. T030 / CIPH-40 — Third-party license (AGPL) compliance** *(hard Legal gate)*
- CIPH-40 is **Status: Active (Reopened)**; acceptance requires "No restrictive copyleft (e.g., AGPL) licenses remain in the shipped dependency set."
- CMT-2026-08-002 (Diana, 2026-08-12): "Legal memo landed: AGPL in the bundle triggers whole-bundle copyleft exposure for our distribution model. Escalate to P0 and treat as a hard Legal gate — engineering search alone is insufficient to close T030."
- Charlie (SRC-SLACK-41, 2026-08-15) had candidate replacements but "neither one covers everything the old library did. Still unresolved." WS-04 still lists "Finding a viable non-AGPL PDF parsing library for T030" under Needs Manual Triage.

**6. T031 / CIPH-41 — Large-file chunking / memory leak** *(explicitly tied to the T011 gate)*
- CIPH-41 is **Status: Active (Reopened)** — chunking merged, then reopened after files over 2GB were found to still leak memory; buffer-release logic is being refactored.
- CMT-2026-08-003 (Bob, 2026-08-18): MedFirst pilot hit OOM on a 4.7GB PDF with 8GB RAM on a clinic workstation — "This is a pilot-blocker — prioritize T031… and tie explicitly to the T011 release gate."

**7. T006 / CIPH-16 — Legacy JSON→YAML policy auto-migration** *(release dependency tied to the T011 gate)*
- The T006 task itself is checked complete (YAML policy loader merged), but CMT-2026-06-001 (Alice, 2026-06-21) adds a separate obligation: MedFirst has three legacy JSON pilot policies in production that "must auto-migrate before we cut over. Evan owns the JSON→YAML converter; treat migration as a release dependency tied to T006 and the T011 gate." It sits in WS-01 Active Work with no completion evidence anywhere in the dataset.

---

### What is already green (for contrast)
- **T010 / CIPH-20 — Security audit and vulnerability scans**: Completed. The medium-severity CORS `*` origin finding was patched to configured `ALLOWED_ORIGINS`, and 2026-07-15 re-scans confirmed the patch holds. CMT-2026-07-002 adds a RedByte pen-test attestation letter (2026-07-11) to the release evidence pack.
- Checklist dependencies T001–T004 and T006 are recorded as satisfied on CIPH-21; the 2026-07-12 checklist had six of seven dependency gates met.
- REST API authentication is **deliberately out of v1.0 scope**, not an open gate — Alice re-confirmed on 2026-08-20 that auth stays deferred to post-v1.0.0 under the trusted-local-network assumption (SRC-SLACK-08). Separately, CMT-2026-07-001 flags that MedFirst's enterprise renewal requires REST auth by 2026-03-31 — a roadmap commitment, not a v1.0.0 gate.

### Adjacent risk, not formally a v1.0 gate
`T007 / CIPH-17` (multi-page offset mismatch) is **Blocked** on upstream `pdfminer.six` PR #992, still unmerged as of 2026-09-10, with the team having rejected maintaining a fork. CMT-2026-06-003 notes #992 is expected mid-October at the earliest and that any pre-normalization workaround needs written Legal sign-off. Alice on 2026-09-10: "This is becoming a real risk for the v1.0 timeline." It is not named on the T011 checklist, but it constrains the same schedule.

---

### Bottom line
Two gates are formally named on the release checklist (Docker size/CVE, Windows signing) and both remain red; the 2026-09-15 pre-release audit added the audit-log schema mismatch and the high-DPI upstream block to the open board; and comment-layer decisions attach three more hard dependencies (AGPL Legal gate, large-file OOM, legacy JSON migration) to the same T011 gate. Evan's summary at the audit stands as the operative position: "Release isn't opening with any of those unresolved." With a hard no-ship date of 2026-10-15 roughly three weeks out and no gate having moved to green, **v1.0.0 cannot ship**.

**Dataset records cited:** `work-states/WS-03-ops.md`, `work-states/WS-01-engine.md`, `work-states/WS-04-policy.md`, `work-states/WS-05-performance.md`, `work-states/WS-06-platforms.md`, `work-states/comments/2026-06.md`, `work-states/comments/2026-07.md`, `work-states/comments/2026-08.md`, `work-states/comments/2026-09.md`, `med-synth/tasks/CIPH-15-Docker-Packaging.md`, `CIPH-20-Security-Audit.md`, `CIPH-21-Release-v1-Gates.md`, `CIPH-26-Audit-Trail-Logging.md`, `CIPH-39-Windows-Compatibility.md`, `CIPH-40-License-Compliance-Review.md`, `CIPH-41-Large-File-Chunking.md`, `CIPH-46-High-DPI-PDF-Rendering-Fixes.md`, `med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md`, `slack/2026-06-25-docker-size.md`, `slack/2026-06-26-blocked-on-upstream.md`, `slack/2026-06-28-defer-auth.md`, `slack/2026-08-11-license-parser-swap.md`, `slack/2026-09-02-windows-signing-gap.md`, `slack/2026-09-10-high-dpi-upstream-block.md`, `med-synth/documentation/sources/2026-07-12-Release-Checklist.md`, `2026-09-02-Windows-Compatibility-Audit-Report.md`, `2026-09-10-High-DPI-PDF-Rendering-Coordinates-Report.md`.
