# As of the final project snapshot after **2026-09-22**, what hard calendar constraint, if any, now governs shipping v1.0.0 if Docker packaging and Windows signing stay red, and how, if at all, does that change the earlier security-gate hold?

<!-- RESPONSE_START -->

## Answer

**The hard calendar constraint: a no-ship date of 2026-10-15.**

As of the final snapshot (Work State Index as-of `2026-09-22T12:00:00Z`), the release board set a **hard no-ship deadline of 2026-10-15**: if T005 (Docker packaging — size/CVE) and T029 (Windows Defender/SmartScreen code-signing) are not green by that date, v1.0.0 does not ship. The record explicitly flags this as **"Hard deadline — not advisory,"** and notes the decision was taken by the release board outside the Fireflies meeting record.

- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-09.md` — `CMT-2026-09-002` (Diana, 2026-09-15): "no-ship after 2026-10-15 if T005 and T029 are not green. Hard deadline — not advisory."
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md` — Blockers: "Release board set hard no-ship after **2026-10-15** if T005 and T029 are not green."
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md` — priority 1: "Clear before 2026-10-15 or no-ship."
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-15-daily-brief.md` — same deadline recorded the day it was set.

## How it changes the earlier security-gate hold

**It does not lift, narrow, or replace the hold — it time-boxes it.** The substance is unchanged: T011 (CIPH-21, Release v1.0 Gates) remains **Active** under Diana's security-gate hold, and still cannot close until *both* T005 and T029 clear. What the deadline adds is a terminal date and a defined consequence.

- **Before:** the hold was open-ended and outcome-neutral — release stayed closed until the two gates went green, with slippage the implicit result. The 2026-07-12 checklist framing had T005 as "the only unmet dependency," and the 2026-09-15 pre-release audit re-confirmed the gates simply "stay on the board" with "no one closes those today."
- **After:** the same two gates now carry a deadline. Missing 2026-10-15 no longer means "keep waiting" — it means **no ship** for v1.0.0. The hold's *conditions* are identical; only its *expiry behavior* is new.

Supporting files: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-21-Release-v1-Gates.md` (Diana's hold pending both gates; T001–T006 and T010 dependencies already met), `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-07-12-Release-Checklist.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md` (`SRC-MEET-10`).

## Status of the two gates at the snapshot (both still red)

- **T005 / CIPH-15 — Docker packaging, Active (Reopened).** Image ballooned to 2.1GB after OCR bundling; multi-stage build and Alpine base applied, but as of the 2026-08-12 verification the image still exceeds the ~450MB target and CVE verification is outstanding. Dual thresholds apply per `CMT-2026-06-002`: interim RC at 800MB once CVE-clean, GA at ~450MB. Files: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-15-Docker-Packaging.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md`.
- **T029 / CIPH-39 — Windows signing, Active.** Path/backslash handling is fixed and a build artifact exists, but no Authenticode certificate has been procured, so Defender/SmartScreen block the unsigned build. WS-06 characterizes this as **a procurement dependency, not an engineering block** — engineering cannot work around it — and lists "budget and procurement timeline for the Authenticode certificate" under Needs Manual Triage. Files: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-39-Windows-Compatibility.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-06-platforms.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md` (`SRC-SLACK-37`).

## One important qualification

The 2026-10-15 no-ship condition names **only** T005 and T029. Other release-coupled blockers were still open at the snapshot and are not covered by that condition — so clearing the two named gates by 10-15 is necessary but not sufficient for release:

- **T016 (audit-trail logging)** — the 2026-09-15 pre-release audit kept the audit-log gate red on CLI-schema vs emitted-record mismatch (`SRC-MEET-10`; `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md`).
- **T031 (MedFirst OOM)** — still release-coupled (`CMT-2026-08-003`).
- **T030 (Legal AGPL/whole-bundle P0)** — still open (`CMT-2026-08-002`).
