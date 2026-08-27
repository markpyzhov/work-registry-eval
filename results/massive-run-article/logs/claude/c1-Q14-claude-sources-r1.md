# As of the final project snapshot after **2026-09-22**, what hard calendar constraint, if any, now governs shipping v1.0.0 if Docker packaging and Windows signing stay red, and how, if at all, does that change the earlier security-gate hold?

<!-- RESPONSE_START -->

## Answer

**No such hard calendar constraint exists in the retrieved sources.** The premise of the question is not supported by the dataset.

**What the sources actually show**

1. **No release date, deadline, or dated commitment for v1.0.0 appears anywhere in the source records.** Across the release-gate task, the release checklist, the Windows/Docker threads, and the pre-release meeting transcripts, the v1.0 release is governed entirely by *gate conditions*, never by a date. The only calendar-like statements are about risk, not commitment — e.g., on 2026-09-10 Alice says the unmerged upstream `pdfminer.six` PR #992 "is becoming a real risk for the v1.0 timeline," and Charlie replies he would "rather eat the delay." No target date, no drop-dead date, no launch window is named.

2. **There is no "final project snapshot after 2026-09-22."** The latest dated activity in the sources is 2026-09-22 itself — the Handshake Protocol Deep Dive meeting (SRC-MEET-11) and the corresponding Slack thread (SRC-SLACK-27) / CIPH-34 block entry, all of which concern the high-latency node-sync handshake and say nothing about release dates. Nothing in the dataset postdates that, so there is no later snapshot that could have introduced a deadline.

3. **The security-gate hold is therefore unchanged — nothing supersedes, relaxes, or time-boxes it.** As of the most recent gate-status records:
   - **CIPH-21 (Release v1.0 Gates)** — Status: **Active**. Diana placed a security-gate hold on the release pending both T005 (Docker slim-down / CVE work) and T029 (Windows Defender/SmartScreen code-signing). Dependencies T001–T006 and T010 are otherwise satisfied; the two named gates are explicitly "not yet met."
   - **CIPH-15 (Docker Packaging)** — Status: **Active (Reopened)**. As of the 2026-08-12 verification, the image still exceeds the ~450MB target and CVE verification still fails. Diana: "Reopened status stands until both the size and the CVE check are clean."
   - **CIPH-39 (Windows builds / signing)** — Status: **Active**. The build artifact is produced and runs, but is unsigned; no code-signing certificate has been procured. On 2026-08-15 Evan reported procurement had "no firm timeline yet." On 2026-09-02 Alice chose to "keep it open on the release gate rather than pushing it off the board."
   - **2026-09-15 Pre-Release Audit (SRC-MEET-10)** — the last release-gate review in the dataset. Alice: "Security-gate work stays open — Docker slim-down, Windows signing, and we keep the audit mismatch visible as a release blocker. No one closes those today." Evan: "Release isn't opening with any of those unresolved." Diana kept the audit-log gate red.

4. **The hold actually widened rather than narrowing.** Beyond the original two gates, the 2026-09-15 audit added a third open release blocker: the audit-log gate (CIPH-26), where CLI-emitted audit records do not match the defined schema — confirmed as a mismatch by Diana on 2026-09-18 and still open. The upstream high-DPI rendering block (CIPH-46 / T036, blocked on the upstream rendering library) was also listed as still open at that review.

**Bottom line:** With Docker packaging and Windows signing still red, the governing constraint on shipping v1.0.0 is condition-based, not calendar-based — the release cannot open until those gates clear. No deadline was introduced that would force a ship, waive the gates, or convert the hold into a time-boxed decision, and the security-gate hold stands exactly as Diana placed it, with an additional audit-log blocker stacked on top. If a dated release commitment exists, it is not in these source records.

**Sources cited**
- `med-synth/tasks/CIPH-21-Release-v1-Gates.md` (SRC-CU-CIPH-21)
- `med-synth/tasks/CIPH-15-Docker-Packaging.md` (SRC-CU-CIPH-15)
- `med-synth/tasks/CIPH-39-Windows-Compatibility.md` (SRC-CU-CIPH-39)
- `med-synth/tasks/CIPH-26-Audit-Trail-Logging.md`
- `med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md` (SRC-MEET-10)
- `med-synth/communication/sources/fireflies/2026-09-22-Handshake-Protocol-Deep-Dive.md` (SRC-MEET-11)
- `med-synth/communication/sources/fireflies/2026-08-15-Windows-License-Sync.md` (SRC-MEET-08)
- `med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md` (SRC-SLACK-37)
- `med-synth/communication/sources/slack/2026-06-25-docker-size.md` (SRC-SLACK-06)
- `med-synth/communication/sources/slack/2026-06-26-blocked-on-upstream.md` (SRC-SLACK-07)
- `med-synth/documentation/sources/2026-09-02-Windows-Compatibility-Audit-Report.md` (SRC-GDOC-39)
- `med-synth/documentation/sources/2026-07-12-Release-Checklist.md` (SRC-GDOC-05)
