# As of the final project snapshot after **2026-09-22**, what hard calendar constraint, if any, now governs shipping v1.0.0 if Docker packaging and Windows signing stay red, and how, if at all, does that change the earlier security-gate hold?

<!-- RESPONSE_START -->

I have everything needed. Here is the complete answer.

---

## The hard calendar constraint

Yes — as of the final snapshot (work-state index as-of **2026-09-22T12:00:00Z**), there is now a hard calendar constraint on shipping v1.0.0:

**No-ship after 2026-10-15 if T005 and T029 are not green.**

This comes from a release board decision recorded as **CMT-2026-09-002** (author: Diana, dated 2026-09-15, taken outside the Fireflies meeting), and it is carried in the authoritative Work State **WS-03: Packaging, Release gating, and Security** under *Blockers and Dependencies*:

> **T011 — no-ship deadline (CMT-2026-09-002)**: Release board set hard no-ship after **2026-10-15** if T005 and T029 are not green.

The comment itself is explicit that this is **"Hard deadline — not advisory."**

The two named gates map exactly onto the two red items in the question:
- **T005 / CIPH-15 — Docker packaging.** Reopened/active. Image ballooned to 2.1GB after OCR dependencies were bundled; multi-stage builds and an Alpine swap were implemented, but as of August 12 the image still exceeds the ~450MB target and CVE verification is failing. Note the dual thresholds from CMT-2026-06-002 (CISO review): an interim release candidate may ship at **800MB once CVE-clean**, while **GA remains ~450MB** — the two must not be conflated on the release checklist.
- **T029 / CIPH-39 — Windows code-signing.** Active. Backslash path handling was fixed (2026-08-10) and a Windows build artifact was produced (2026-08-12), so packaging is no longer the blocker; the artifact is **unsigned**, tripping SmartScreen/Defender. No Authenticode code-signing certificate has been procured or wired into the build pipeline. WS-06 characterizes this as **a procurement dependency, not an engineering block**, and lists "budget and procurement timeline for Windows Authenticode code-signing certificate" under Needs Manual Triage.

## How this changes the earlier security-gate hold

It does **not** lift, weaken, or supersede the hold — it puts a clock on it and converts an open-ended block into a dated decision point.

- **The hold itself is unchanged and still in force.** Diana's security-gate hold on CIPH-21 (Release v1.0 Gates) remains: the task is still **Active** with both gates unresolved, and WS-03 still records T011 as "active under a security-gate hold." The September 15 pre-release audit reaffirmed it — Alice: "Security-gate work stays open… No one closes those today," and Diana kept the audit-log gate red pending schema/record alignment. Nothing in the dataset shows the hold being released, waived, or made conditional.
- **What changed is the consequence of the hold persisting.** Before CMT-2026-09-002, the hold was open-ended: T011 simply could not close until T005 and T029 were green, with no date attached (the earlier 2026-07-12 Release Checklist named T005 as the sole unmet dependency, no deadline). After it, the same two gates now carry a terminal date: if they are not green by **2026-10-15**, the release does not ship at all — the outcome flips from "wait until the gates clear" to "no-ship."
- **The gating criteria are also narrowed on paper.** The formal no-ship condition names only **T005 and T029**. The September 15 audit tracked a third open item — the **audit-log schema/records mismatch** (Bob's CLI-emitted records not matching the defined schema, T016), which Diana held red as release evidence — plus the upstream high-DPI rendering block (T036). These remain open blockers in WS-03's Active Work and on the board, but they are not part of the stated 2026-10-15 no-ship trigger. So clearing T005 and T029 alone satisfies the calendar constraint's literal condition without necessarily clearing every item the security-gate hold covers.
- **Practical implication:** the binding path to the deadline runs partly outside engineering. T029 is blocked on certificate **procurement** (Alice took the certificate-chasing action on 2026-09-02), and T005 needs both size reduction and a clean CVE verification — with the 800MB CVE-clean RC threshold as the more attainable near-term target versus the ~450MB GA target.

## Records cited

- `work-states/WS-03-ops.md` (path = work-state) — Blockers and Dependencies; Active Work; Task List
- `work-states/comments/2026-09.md` — **CMT-2026-09-002** (WS-03/T011, status_update, 2026-09-15, Diana)
- `work-states/comments/2026-06.md` — **CMT-2026-06-002** (WS-03/T005, dual RC/GA size gates)
- `work-states/WS-06-platforms.md` — T029 / CIPH-39 Active Work and Needs Manual Triage
- `work-states/index.md` — as-of timestamp 2026-09-22T12:00:00Z; T005/T011/T029 listed Active
- `med-synth/tasks/CIPH-21-Release-v1-Gates.md` (SRC-CU-CIPH-21) — security-gate hold, Active status
- `med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md` (SRC-MEET-10)
- `med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md` (SRC-SLACK-37)
- `med-synth/documentation/sources/2026-09-02-Windows-Compatibility-Audit-Report.md` (SRC-GDOC-39)
- `med-synth/documentation/sources/2026-07-12-Release-Checklist.md` (SRC-GDOC-05) — pre-deadline baseline
