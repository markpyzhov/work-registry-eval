# As of the final project snapshot after **2026-09-22**, what hard calendar constraint, if any, now governs shipping v1.0.0 if Docker packaging and Windows signing stay red, and how, if at all, does that change the earlier security-gate hold?

<!-- RESPONSE_START -->

## Answer

**No hard calendar constraint exists.** The dataset contains no ship date, release deadline, launch window, or any other date-based commitment for v1.0.0 — not in the final snapshot after 2026-09-22, and not at any earlier point. The premise of the question is not supported by the sources: v1.0.0 in this project is gated by *conditions*, never by a calendar.

### What the record actually shows

**The gating is condition-based, not date-based.** CIPH-21 "Release v1.0 Gates" (SRC-CU-CIPH-21) remains **Active**, and its acceptance criteria are stated purely as gate-clearance conditions, with no due date:
- Checklist dependencies T001–T006 and T010 satisfied — **met**
- T005 (Docker image size/CVE) and T029 (Windows code-signing) gates clear — **not yet met; task remains Active pending both**

Diana's security-gate hold on the release is likewise pending both T005's Docker slim-down/CVE work and T029's Windows Defender/SmartScreen code-signing — again with no date attached.

**Both gates are still red at the last recorded checks.**
- Docker (CIPH-15, SRC-CU-CIPH-15): **Active (Reopened)**. At the 2026-08-12 verification the image still exceeded the ~450MB target and CVE verification remained outstanding (SRC-SLACK-06). Diana: reopened status stands until both size and CVE are clean.
- Windows signing (CIPH-39, SRC-CU-CIPH-39; DOC-2039, SRC-GDOC-39): **Active**. Packaging is no longer the blocker — a working artifact was produced 2026-08-12 — but the artifact is unsigned and no code-signing certificate has been procured or configured. Alice kept it open on the release gate and took on chasing procurement (SRC-SLACK-37, 2026-09-02).

**The one place a timeline is even discussed, it is explicitly absent.** In the 2026-08-15 Windows & License Sync (SRC-MEET-08), Evan says the code-signing certificate is still waiting on procurement with **"no firm timeline yet,"** so he cannot say when it clears. That is the closest the corpus comes to a calendar item, and it is a statement that no date exists.

**The last pre-release review reaffirms the hold and adds to it, without setting a date.** At the 2026-09-15 Pre-Release Audit (SRC-MEET-10), Alice's gate check lists Docker slim-down/CVE open, Windows signing open, and the high-DPI rendering bug still blocked upstream. Diana keeps the audit-log gate **red** because CLI-emitted records don't match the defined schema (confirmed 2026-09-18 in CIPH-26's history as an open release blocker). Evan: release isn't opening with any of those unresolved; Alice: security-gate work stays open, no one closes those. Time pressure is acknowledged only qualitatively — Alice on 2026-09-10 calls the upstream pdfminer.six block "a real risk for the v1.0 timeline" (SRC-SLACK-07) — but no date is ever named, and Charlie's response is that he'd rather eat the delay.

### Effect on the earlier security-gate hold

**None. The hold is unchanged and unconditional.** Because there is no deadline in evidence, nothing in the final snapshot creates schedule pressure that could override, time-box, or convert the hold into a ship-anyway decision. The hold survives the 2026-09-22 snapshot exactly as Diana set it: release blocked pending both T005 and T029, with the audit-log mismatch stacked on top as a third open blocker and high-DPI blocked upstream. The record contains no waiver, no exception, no go/no-go with a date, and no decision to ship with the gates red.

The only activity dated 2026-09-22 is unrelated to the release gates: the authenticated node-sync handshake (CIPH-34) moved to **Blocked** after high-latency timeouts, with the team explicitly refusing a timeout-bump workaround (SRC-MEET-11, SRC-SLACK-27). That adds a blocker; it does not introduce a date.

### Caveat

If a hard calendar constraint was recorded somewhere outside the `sources` records in this dataset, it is not retrievable here — every gate document, task record, Slack thread, and meeting transcript I retrieved expresses release readiness in terms of gate conditions only.

### Sources cited
- `med-synth/tasks/CIPH-21-Release-v1-Gates.md` (SRC-CU-CIPH-21)
- `med-synth/tasks/CIPH-15-Docker-Packaging.md` (SRC-CU-CIPH-15)
- `med-synth/tasks/CIPH-39-Windows-Compatibility.md` (SRC-CU-CIPH-39)
- `med-synth/tasks/CIPH-26-Audit-Trail-Logging.md`
- `med-synth/tasks/CIPH-34-Zero-Trust-Node-Sync.md` (SRC-CU-CIPH-34)
- `med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md` (SRC-MEET-10)
- `med-synth/communication/sources/fireflies/2026-09-22-Handshake-Protocol-Deep-Dive.md` (SRC-MEET-11)
- `med-synth/communication/sources/fireflies/2026-08-15-Windows-License-Sync.md` (SRC-MEET-08)
- `med-synth/documentation/sources/2026-09-02-Windows-Compatibility-Audit-Report.md` (SRC-GDOC-39 / DOC-2039)
- `med-synth/documentation/sources/2026-07-12-Release-Checklist.md` (SRC-GDOC-05 / DOC-2005)
- `med-synth/communication/sources/slack/2026-06-25-docker-size.md` (SRC-SLACK-06)
- `med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md` (SRC-SLACK-37)
- `med-synth/communication/sources/slack/2026-06-26-blocked-on-upstream.md` (SRC-SLACK-07)
