**Source ID**: SRC-SLACK-24

# Slack Thread: Redaction Preview UI Overlay Design
**Channel**: #cipherdoc
**Date**: 2026-08-04

---

**[2026-08-04 11:18] Diana**: Starting on the redaction preview overlay. Users need to see what's being redacted before the final export. I'm proposing a UI overlay that shows the bounding boxes of detected PII.

**[2026-08-04 11:19] Charlie**: How are we rendering that? If we're using Electron, we can put an SVG layer over the PDF preview.

**[2026-08-04 12:54] Diana**: Got a mockup — semi-transparent red blocks for high-confidence matches, yellow for low-confidence ones that need manual review.

**[2026-08-04 14:19] Charlie**: Scroll sync needs to be exact. If the overlay drifts from the text, the whole thing is useless.

**[2026-08-04 14:32] Diana**: Using the `pdf.js` coordinate system to map the bounding boxes directly onto the viewport.

**[2026-08-04 14:36] Alice**: Can users click a box to un-redact it?

**[2026-08-04 15:00] Diana**: Not in the first version — it's just a preview for now. Toggling redactions will be part of the manual review workflow.

**[2026-08-04 15:39] Diana**: I'll share the CSS for the highlighter blocks shortly.
