# As of the final project snapshot after **2026-09-22**, what hard calendar constraint, if any, now governs shipping v1.0.0 if Docker packaging and Windows signing stay red, and how, if at all, does that change the earlier security-gate hold?

<!-- RESPONSE_START -->

## Answer

**As of the final snapshot in the package (Work State index as-of `2026-09-22T12:00:00Z`; latest brief `2026-09-22`), the governing hard calendar constraint is a release-board no-ship date of 2026-10-15: if T005 (Docker packaging size/CVE) and T029 (Windows code-signing) are not green by then, v1.0.0 does not ship.**

### The constraint

- Recorded as `CMT-2026-09-002` (author Diana, dated 2026-09-15, a release-board decision taken outside Fireflies): "no-ship after 2026-10-15 if T005 and T029 are not green. **Hard deadline — not advisory.**" — `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-09.md`
- It is carried into the authoritative Work State as a blocker on T011: "Release board set hard no-ship after **2026-10-15** if T005 and T029 are not green." — `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md`
- Still live in the final 2026-09-22 brief: T011 "depends on T005 and T029; hard 2026-10-15 deadline," and priority #1 is "Clear before 2026-10-15 or no-ship." — `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md`

Scope note: the deadline is tied to exactly two items — T005 and T029. It is not stated to cover the other open release-adjacent blockers (audit-log schema mismatch, upstream high-DPI/Form XObjects, T031 MedFirst OOM, T030 AGPL legal gate), which remain open on their own terms.

### Effect on the earlier security-gate hold

**It does not lift, weaken, or replace the hold — it puts an expiry date on it.**

- The earlier hold is Diana's security-gate hold on the release, pending *both* T005's Docker slim-down/CVE work and T029's Defender/SmartScreen code-signing; CIPH-21 remains **Active** with both gates unresolved. — `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-21-Release-v1-Gates.md`
- WS-03 still describes release gates as "**active** under a security-gate hold" in the same final snapshot that carries the deadline, so the two coexist. The 2026-09-15 pre-release audit reaffirmed the hold ("Release isn't opening with any of those unresolved… No one closes those today"). — `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md`
- The change is in kind, not in content: the hold was previously **open-ended and condition-based** ("release doesn't open until these clear," with no date — see the 2026-07-12 release checklist, which simply says it "cannot close until that gate clears"). The board decision converts it into a **dated, terminal pass/fail**: the same two conditions, but with a fixed cutoff after which the outcome is no-ship rather than continued waiting. No gate was added, removed, or relaxed; nothing in the package authorizes shipping with either gate red. — `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-07-12-Release-Checklist.md`

### State of the two gates at the snapshot

- **T005 / CIPH-15 (Docker)** — Active (Reopened). Image ballooned to 2.1GB after OCR bundling; multi-stage build and Alpine base applied, but as of the 2026-08-12 verification the image still exceeds the ~450MB target and CVE verification is still failing. Dual thresholds apply per `CMT-2026-06-002`: interim RC at 800MB once CVE-clean, GA at ~450MB. — `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-15-Docker-Packaging.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md`
- **T029 / CIPH-39 (Windows signing)** — Active. Build artifact exists and path handling is fixed; the residual blocker is a missing Authenticode code-signing certificate, so Defender/SmartScreen flags or blocks pilot installs. WS-06 characterizes this explicitly as "a procurement dependency, not an engineering block" — meaning the 2026-10-15 date is at risk on certificate procurement timelines rather than dev capacity. — `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-39-Windows-Compatibility.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-06-platforms.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md`

The final brief's follow-up item states the required action directly: "Secure Authenticode cert and finish Alpine/CVE Docker verification."

No record in the package dates later than 2026-09-22, and none modifies or supersedes the 2026-10-15 no-ship date or the security-gate hold.
