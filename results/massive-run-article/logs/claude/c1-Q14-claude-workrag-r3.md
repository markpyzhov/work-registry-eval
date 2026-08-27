# As of the final project snapshot after **2026-09-22**, what hard calendar constraint, if any, now governs shipping v1.0.0 if Docker packaging and Windows signing stay red, and how, if at all, does that change the earlier security-gate hold?

<!-- RESPONSE_START -->

## Answer

**Yes — there is now a hard calendar constraint: a no-ship date of 2026-10-15.**

As of the final project snapshot (work-state index as-of `2026-09-22T12:00:00Z`; WS-03 last updated 2026-09-22):

### The constraint

- The release board decided on **2026-09-15** (recorded as comment `CMT-2026-09-002`, author Diana, type `status_update`, applied to `WS-03/T011`): **"no-ship after 2026-10-15 if T005 and T029 are not green. Hard deadline — not advisory."** The decision was taken outside the Fireflies meeting record.
- WS-03 (`work-states/WS-03-ops.md`) carries this in its Blockers and Dependencies section as **"T011 — no-ship deadline (CMT-2026-09-002)"**, alongside the standing dependency that **T011 (CIPH-21, Release v1.0.0 gates) cannot close until T005 and T029 are green** (`S9` = SRC-MEET-10 Pre-Release Audit 2026-09-15, `S10` = SRC-SLACK-37 Windows Signing Gap 2026-09-02).

The two conditions named are exactly the two "red" items in the question:
- **T005 / CIPH-15 — Docker packaging (size/CVE)**: reopened/active. Image ballooned to 2.1GB after OCR dependencies were bundled; multi-stage builds and an Alpine swap were implemented, but as of August 12 the image still exceeds the ~450MB target and CVE verification is failing. Note the dual thresholds from `CMT-2026-06-002` (CISO review): interim RC may ship at **800MB once CVE-clean**, GA target remains **~450MB** — do not conflate them.
- **T029 / CIPH-39 — Windows code-signing**: active. The path/backslash defects were fixed 2026-08-10 and a Windows build artifact was produced 2026-08-12, so packaging is no longer the blocker; the build is **unsigned**, so Defender/SmartScreen flags it. Per SRC-GDOC-39 (Windows Build Signing Gap, 2026-09-02), procuring an Authenticode certificate and wiring signing into the release build is the **sole** remaining item. WS-06 characterizes it as a **procurement dependency, not an engineering block**, and lists "Budget and procurement timeline for Windows Authenticode code-signing certificate" under Needs Manual Triage.

### How it changes the earlier security-gate hold

It **does not lift, weaken, or replace the hold — it adds a deadline on top of it, and converts an open-ended hold into a time-boxed one.**

- The earlier state (CIPH-21): **Diana placed a security-gate hold** on the release pending both T005's Docker slim-down/CVE work and T029's Windows Defender/SmartScreen code-signing. That hold was open-ended — it simply blocked shipping until both cleared, with no expiry.
- The 2026-09-15 pre-release audit reaffirmed it: Alice — security-gate work stays open (Docker slim-down, Windows signing), plus the audit-log schema mismatch kept visible as a release blocker; Diana — the audit-log gate stays red until schema and records match; Evan — release isn't opening with any of those unresolved. Nothing was closed that day.
- The board decision layers a **calendar consequence** onto the same two conditions. Before: red gates ⇒ can't ship (indefinitely). After: red gates ⇒ can't ship, **and past 2026-10-15 the release is affirmatively no-ship** rather than merely waiting. The trigger conditions are unchanged (T005 and T029 green), the gate criteria are unchanged, and CIPH-21 remains **Active** with both gates unresolved. The disposition on `CMT-2026-09-002` is explicit that it was applied to `WS-03/T011` **Blockers** — an addition, not a supersession.

One nuance worth flagging: the 2026-10-15 deadline is written in terms of **T005 and T029 only**. The September 15 audit also lists the **audit-log schema/emitted-record mismatch** (T016 / CIPH-26, WS-04) as an open release hold, and it is not named in the no-ship condition — so clearing T005 and T029 by 2026-10-15 satisfies the board's calendar test but does not on its own dispose of every blocker the pre-release audit had on the board.

### Records cited

- `work-states/WS-03-ops.md` (work-state, WS-03 Packaging/Release gating/Security; Blockers, Active Work, Task List)
- `work-states/comments/2026-09.md` — `CMT-2026-09-002`
- `work-states/comments/2026-06.md` — `CMT-2026-06-002` (dual size gates)
- `med-synth/tasks/CIPH-21-Release-v1-Gates.md` (SRC-CU-CIPH-21)
- `med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md` (SRC-MEET-10)
- `med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md` (SRC-SLACK-37)
- `med-synth/documentation/sources/2026-09-02-Windows-Compatibility-Audit-Report.md` (SRC-GDOC-39)
- `med-synth/tasks/CIPH-39-Windows-Compatibility.md` (SRC-CU-CIPH-39)
- `work-states/WS-06-platforms.md` (T029 status, procurement triage)
