**Source ID**: SRC-SLACK-05

# Slack Thread: Offset Mismatch Debugging
**Channel**: #cipherdoc
**Date**: 2026-06-23

---

**[2026-06-23 08:56] Charlie**: @Diana, I'm seeing weird behavior in the test cases. The redaction masks are shifted by a character or two in some PDF exports.

**[2026-06-23 09:01] Diana**: Multi-column layouts? I told you pdfminer output was injecting spaces.

**[2026-06-23 09:43] Charlie**: It's not just the spaces. The engine sees the text at one offset, but the PDF coordinates are different after the cleaning phase.

**[2026-06-23 10:51] Diana**: Are you seeing this on all viewers? Sometimes Acrobat renders overlays differently than Chrome's PDF viewer.

**[2026-06-23 10:52] Charlie**: Looking at the raw coordinate output for now. Whitespace normalization looks like the culprit — non-breaking spaces keep showing up in the extracted text.

**[2026-06-23 10:53] Charlie**: Still stuck. Tried mapping cleaned offsets back to raw ones, but the math falls apart on dense pages.

**[2026-06-23 12:40] Diana**: Can we get most of the standard text aligned and park the edge cases?

**[2026-06-23 12:42] Charlie**: Not really — on dense docs it's closer to half the spans. Starting to look like an upstream pdfminer.six issue. I'm going to check their tracker.

**[2026-06-23 12:45] Alice**: Status?

**[2026-06-23 12:47] Charlie**: No. Offline tonight.
