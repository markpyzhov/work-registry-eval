# As of the final project snapshot after **2026-09-22**, what hard calendar constraint, if any, now governs shipping v1.0.0 if Docker packaging and Windows signing stay red, and how, if at all, does that change the earlier security-gate hold?

<!-- RESPONSE_START -->

I have the complete picture. Here's the answer.

---

## Answer

**The hard calendar constraint: a no-ship date of 2026-10-15.**

As of the final snapshot (Work State Index as-of timestamp **2026-09-22T12:00:00Z**), the release board set a hard no-ship deadline: **v1.0.0 cannot ship after 2026-10-15 if T005 (Docker packaging — size/CVE) and T029 (Windows code-signing) are not green.** The decision was recorded by Diana on 2026-09-15 and is explicitly flagged as "Hard deadline — not advisory," made at the release board outside of Fireflies.

- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-09.md` — `CMT-2026-09-002`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md` — Blockers and Dependencies: "Release board set hard no-ship after **2026-10-15** if T005 and T029 are not green."
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md` — priority 1: "Clear before 2026-10-15 or no-ship."

**How it changes the earlier security-gate hold: it does not lift, replace, or soften it — it time-bounds it.**

The two conditions are stacked, not substituted:

1. **The security-gate hold still stands.** Diana's hold on the release pending both T005's Docker slim-down/CVE work and T029's Defender/SmartScreen code-signing remains in force, and T011 (CIPH-21) is still **Active** with both gates unresolved. WS-03 as of 2026-09-22 still reads "Release gates are **active** under a security-gate hold," and "T011 cannot close until T005 (Docker size/CVE) and T029 (Windows code-signing certificate) are green." The 2026-09-15 pre-release audit closed with Alice's explicit "No one closes those today."
2. **What the deadline adds is an expiry, not a waiver.** Before 2026-09-15 the hold was open-ended — it simply blocked the release until the gates cleared, with no date attached. The board decision converts that open-ended hold into a deadline-bounded one: the same two gates must go green *by 2026-10-15*, and if they are still red on that date the outcome is no-ship rather than continued slip. Crucially, the deadline is not an escape hatch — it does not authorize shipping with the gates red; it forecloses shipping at all.

Sources: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-21-Release-v1-Gates.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md` (`SRC-MEET-10`), `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md`.

**Status of the two gates at the snapshot (both still red):**

- **T005 / CIPH-15 Docker packaging** — Active (Reopened). Image ballooned to 2.1GB after OCR bundling; multi-stage build and Alpine swap done, but as of the 2026-08-12 verification the image still exceeds the ~450MB GA target and CVE verification is still failing. Note the dual thresholds tracked separately: interim RC at 800MB once CVE-clean, GA at ~450MB (`CMT-2026-06-002`). Files: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-15-Docker-Packaging.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md`.
- **T029 / CIPH-39 Windows signing** — Active, held on code-signing. Windows path/backslash handling is fixed and a build artifact exists, but Defender and SmartScreen flag the unsigned binary for pilot testers. This is a **procurement dependency, not an engineering block** — the Authenticode certificate does not exist yet and Alice took the action to chase the certificate process; budget and procurement timeline are still in Needs Manual Triage. Files: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-39-Windows-Compatibility.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-06-platforms.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md`.

This asymmetry matters for the deadline: the Docker gate is engineering work that can be driven to green internally, whereas the Windows gate depends on an external certificate purchase that had not started as of the snapshot — so the 2026-10-15 date is most at risk from the procurement side.

**One scoping caveat worth flagging.** The 2026-10-15 deadline is worded to cover **only** T005 and T029. The 2026-09-15 pre-release audit kept a **third** item red — the audit-log schema mismatch (T016 / CIPH-26), where the CLI path and emitted log records don't match the defined schema, which Diana said "undercuts the audit trail as release evidence" and which she will keep red until they match. Evan's summary in that meeting was that the audit hold "stacks on top of the Docker and Windows holds." No calendar constraint is attached to T016 in the record, and it is not named in `CMT-2026-09-002`. So clearing T005 and T029 by 2026-10-15 satisfies the stated deadline condition but does not by itself open the release while the audit-log gate stays red. Files: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md` (T016 active/reopened), `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md`.
