**Source ID**: SRC-SLACK-11

# Slack Thread: Manual Review Threshold Design
**Channel**: #cipherdoc
**Thread opened**: 2026-06-28
**Last activity**: 2026-09-18

---

**[2026-06-28 09:08] Diana**: Starting on the manual review threshold work. We need a safety valve for when the engine isn't confident about a redaction. I'm proposing a 90% confidence threshold — anything below that gets flagged for manual review.

**[2026-06-28 09:55] Charlie**: How do we define "confidence"? Just the regex match score, or are we factoring in OCR quality too?

**[2026-06-28 10:09] Diana**: Both. If the OCR engine gives a low confidence score for a block of text, we should flag it regardless of the regex match.

**[2026-08-06 10:49] Diana**: Picking this back up — implementing the quarantine folder now. Docs that fall below the 90% threshold land there and won't be exported until a human confirms the redaction.

**[2026-08-20 13:35] Diana**: Quarantine folder alone doesn't give reviewers enough context. Designing the metadata that goes with each quarantined file: confidence score, page number, and the reason it was flagged.

**[2026-09-05 14:34] Charlie**: Added visual indicators in the UI for quarantined pages, tied to that metadata, so reviewers can see at a glance why a page was held.

**[2026-09-18 15:55] Diana**: Ran an end-to-end pass: detection -> quarantine -> metadata -> UI markers -> manual approval. The pipeline holds together, but the 90% threshold tuning itself is still in progress — I want another round of testing before I'd call it locked.

**[2026-09-18 15:58] Charlie**: Makes sense. Let me know when you want another look at the UI side once the threshold settles.
