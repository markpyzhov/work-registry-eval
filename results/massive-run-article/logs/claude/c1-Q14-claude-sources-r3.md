# As of the final project snapshot after **2026-09-22**, what hard calendar constraint, if any, now governs shipping v1.0.0 if Docker packaging and Windows signing stay red, and how, if at all, does that change the earlier security-gate hold?

<!-- RESPONSE_START -->

## Answer

**No such hard calendar constraint exists in the sources.** The premise that a dated deadline "now governs" shipping v1.0.0 as of a post-2026-09-22 snapshot is not supported by any record in the assigned dataset, and nothing in the sources changes the earlier security-gate hold.

**1. There is no post-2026-09-22 project snapshot in the sources.** The most recent records in the corpus are dated 2026-09-22: the Fireflies transcript *Handshake Protocol Deep Dive* (SRC-MEET-11), and the matching 2026-09-22 activity entry on CIPH-34 (Diana — Handshake Timeout Block). Both concern the multi-site handshake, not release scheduling. No source is dated later than 2026-09-22, so there is no "final snapshot after 2026-09-22" that could carry a new constraint.

**2. No source anywhere states a release date, deadline, launch window, or dated commitment for v1.0.0.** The v1.0 release is governed exclusively by *condition-based* gates, never by a calendar:
- **CIPH-21 / T011 "Release v1.0 Gates"** (SRC-CU-CIPH-21) lists acceptance criteria purely as gate-clearance conditions: dependencies T001–T006 and T010 satisfied (met), and T005 (Docker image size/CVE) and T029 (Windows code-signing) clear (not met). The task remains Active. No due date is recorded.
- The **Release Checklist draft** (SRC-GDOC-05, DOC-2005, last updated 2026-07-12) states the checklist "cannot close until that gate clears" — again a condition, not a date.
- The **Windows signing audit** (SRC-GDOC-39, DOC-2039, 2026-09-02) says certificate procurement "is the only remaining item" before T029 and, by extension, the T011 checklist clear. Evan explicitly reported on 2026-08-15 (SRC-MEET-08) that there is **"no firm timeline yet"** on the certificate coming through procurement — the closest the corpus comes to scheduling, and it is an explicit absence of one.

**3. Timeline pressure is mentioned, but never as a fixed date.** On 2026-09-10 (SRC-SLACK-07) Alice says the unmerged upstream pdfminer.six PR #992 "is becoming a real risk for the v1.0 timeline," and Charlie replies he'd "rather eat the delay." That is qualitative schedule risk with an explicit willingness to slip — the opposite of a hard calendar constraint. Similarly, on 2026-09-10 (SRC-SLACK-58) Evan says "we can't wait for an upstream fix if we're hitting the release gate," but Alice's decision was to leave high-DPI rendering blocked and consider documenting it as a known issue — no date was set.

**4. Consequently, the earlier security-gate hold is unchanged — it neither expires, converts to a date-driven ship decision, nor is overridden.** The last substantive statement of the hold is the 2026-09-15 Pre-Release Audit (SRC-MEET-10), one week before the corpus ends:
- Alice: Docker slim-down/CVE open, Windows signing open, high-DPI still blocked upstream.
- Evan: "Release isn't opening with any of those unresolved."
- Alice: "Security-gate work stays open... No one closes those today."
- Diana: audit-log gate stays red until schema and emitted records match.

That 2026-09-15 position is corroborated by the standing task records, which remain in that state through the end of the corpus: CIPH-21 Active on both gates; CIPH-39 Active pending the code-signing certificate (SRC-CU-CIPH-39, last activity 2026-09-02); CIPH-26 audit-log mismatch flagged by Diana on 2026-09-18 as "an open release blocker."

**Bottom line:** if Docker packaging and Windows signing stay red, the sources say v1.0.0 simply does not ship — the release is gated on those conditions clearing (plus, per 2026-09-15/09-18, the audit-log schema mismatch), with no deadline that would force or authorize shipping regardless. Diana's security-gate hold therefore stands exactly as placed; nothing in the record modifies, time-boxes, or supersedes it.

### Sources cited
- SRC-CU-CIPH-21 — `med-synth/tasks/CIPH-21-Release-v1-Gates.md`
- SRC-MEET-10 — `med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md`
- SRC-MEET-11 — `med-synth/communication/sources/fireflies/2026-09-22-Handshake-Protocol-Deep-Dive.md`
- SRC-CU-CIPH-34 — `med-synth/tasks/CIPH-34-Zero-Trust-Node-Sync.md`
- SRC-GDOC-05 (DOC-2005) — `med-synth/documentation/sources/2026-07-12-Release-Checklist.md`
- SRC-GDOC-39 (DOC-2039) — `med-synth/documentation/sources/2026-09-02-Windows-Compatibility-Audit-Report.md`
- SRC-CU-CIPH-39 — `med-synth/tasks/CIPH-39-Windows-Compatibility.md`
- SRC-CU-CIPH-26 — `med-synth/tasks/CIPH-26-Audit-Trail-Logging.md`
- SRC-MEET-08 — `med-synth/communication/sources/fireflies/2026-08-15-Windows-License-Sync.md`
- SRC-SLACK-06 — `med-synth/communication/sources/slack/2026-06-25-docker-size.md`
- SRC-SLACK-07 — `med-synth/communication/sources/slack/2026-06-26-blocked-on-upstream.md`
- SRC-SLACK-37 — `med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md`
- SRC-SLACK-58 — `med-synth/communication/sources/slack/2026-09-10-high-dpi-upstream-block.md`
