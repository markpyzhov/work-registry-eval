# As of the final project snapshot after **2026-09-22**, what hard calendar constraint, if any, now governs shipping v1.0.0 if Docker packaging and Windows signing stay red, and how, if at all, does that change the earlier security-gate hold?

<!-- RESPONSE_START -->

I have complete evidence from the assigned dataset. Here is the answer.

---

## The hard calendar constraint: a 2026-10-15 no-ship deadline

As of the final project snapshot (WS-03 "Last Updated: 2026-09-22"; Work State Index as-of 2026-09-22T12:00:00Z), shipping CipherDoc v1.0.0 is governed by a **hard no-ship date of 2026-10-15**.

The constraint is recorded in the WS-03 Blockers and Dependencies section:

> **T011 — no-ship deadline (CMT-2026-09-002)**: Release board set hard no-ship after **2026-10-15** if T005 and T029 are not green.

Its origin is comment `CMT-2026-09-002` (WS-03/T011, status_update, author Diana, dated 2026-09-15):

> Release board decision (outside Fireflies): no-ship after 2026-10-15 if T005 and T029 are not green. Hard deadline — not advisory.

Three things are worth being precise about:

- **It is conditional, not a fixed ship date.** It does not say "ship by 2026-10-15." It says that *if* T005 (Docker image size/CVE) and T029 (Windows code-signing) are not green by that date, the release does not ship. So if both stay red, the date does not force a ship — it forbids one.
- **It is explicitly binding.** Diana labelled it "Hard deadline — not advisory," and it came from a release-board decision made outside the Fireflies meeting record, so it is not merely a meeting sentiment.
- **The two named conditions were both still red at the snapshot.** T005/CIPH-15 is reopened/active — the image ballooned to 2.1GB after OCR dependencies were bundled, and as of August 12, after multi-stage builds and an Alpine swap, it still exceeded the ~450MB target with CVE verification failing. T029 is Active and held on code-signing: the Windows build artifact is produced successfully (path-handling defects fixed 2026-08-10, artifact produced 2026-08-12), but it is unsigned, tripping SmartScreen and Defender, with no code-signing certificate procured or configured. The Work State Index lists both under "Active / Reopened," with T029 annotated "held on code-signing."

## How it changes the earlier security-gate hold: it doesn't lift it — it puts a clock on it

The earlier hold is Diana's security-gate hold on CIPH-21 / T011, placed pending both T005's Docker slim-down/CVE work and T029's Windows Defender/SmartScreen code-signing. That hold remains fully in force at the snapshot. WS-03 Active Work still reads: "T011 / CIPH-21: Release gates are **active** under a security-gate hold," and CIPH-21 remains Active with both gates unresolved.

The 2026-10-15 deadline is **additive, not substitutive**. Specifically:

- **It does not relax or waive the gates.** The exit criteria are unchanged: T011 cannot close until T005 and T029 are green. There is no evidence in the dataset of any waiver, exception, conditional-ship path, or override for the unsigned binary or the oversized/CVE-failing image.
- **It does not create a ship-anyway path.** The deadline's effect runs in the restrictive direction — it converts an open-ended engineering hold into a bounded one that terminates in a no-ship rather than in an eventual ship whenever the work lands. Before 2026-09-15, the hold had no expiry; the release simply waited on the gates. After it, continued redness past 2026-10-15 means the release is cancelled/blocked outright rather than slipping indefinitely.
- **It narrows the security-gate hold's stated scope to two of three items.** This is the one substantive shift. The 2026-09-15 pre-release audit had Alice keeping three things open — Docker slim-down, Windows signing, and the audit-log schema mismatch (Diana: "I'll keep the audit-log gate red until schema and records match"). The board's no-ship condition, issued the same day, names only **T005 and T029**. So the calendar constraint is keyed to the Docker and Windows gates specifically; the audit-log mismatch remains a live release blocker per the audit but is not part of the stated 2026-10-15 trigger condition.

## Bottom line

If Docker packaging (T005) and Windows signing (T029) stay red, the operative constraint is that v1.0.0 **cannot ship at all after 2026-10-15** — the release board's hard no-ship date. It leaves Diana's security-gate hold entirely intact on its merits and adds a deadline on top: the same two gates must go green, but now by a fixed date, after which the outcome is no-ship rather than a further slip. The dataset contains no evidence of any mechanism to ship v1.0.0 with either gate red.

**Dataset records cited:** `work-states/WS-03-ops.md` (path=work-state; Blockers and Dependencies, Active Work, Task List); `work-states/comments/2026-09.md` (`CMT-2026-09-002`); `work-states/comments/2026-06.md` (`CMT-2026-06-002`, dual RC/GA size gates); `med-synth/tasks/CIPH-21-Release-v1-Gates.md` (`SRC-CU-CIPH-21`); `med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md` (`SRC-MEET-10`); `med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md` (`SRC-SLACK-37`); `med-synth/documentation/sources/2026-09-02-Windows-Compatibility-Audit-Report.md` (`SRC-GDOC-39`); `med-synth/documentation/sources/2026-07-12-Release-Checklist.md` (`SRC-GDOC-05`); `work-states/index.md` (navigation aid, as-of 2026-09-22).
