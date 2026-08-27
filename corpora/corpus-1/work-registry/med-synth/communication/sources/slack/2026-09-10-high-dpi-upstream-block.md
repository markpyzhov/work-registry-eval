**Source ID**: SRC-SLACK-58

# Slack Thread: High-DPI Upstream Block
**Channel**: #cipherdoc
**Date**: 2026-09-10

---

**[2026-09-10 10:41] Diana**: Bad news on the high-DPI rendering fix. The rotation fix Charlie pushed works for simple cases, but it's completely breaking on documents with nested Form XObjects.

**[2026-09-10 10:43] Charlie**: Yeah, I looked into it. The underlying rendering library we're using (`pdf-lib-core`) has a known bug in how it handles coordinates for XObjects when a parent transform is applied.

**[2026-09-10 10:55] Alice**: Can we patch it?

**[2026-09-10 10:56] Charlie**: No.

**[2026-09-10 11:35] Charlie**: It's deep in their C++ core. I've opened an issue with the upstream maintainers, but they haven't responded.

**[2026-09-10 11:37] Evan**: We can't wait for an upstream fix if we're hitting the release gate. Can we work around it by flattening the PDFs first?

**[2026-09-10 11:51] Charlie**: Flattening might work but it'll blow up the file size and we might lose some text layers.

**[2026-09-10 12:29] Alice**: @Diana, @Charlie, let's leave high-DPI rendering blocked for now. We need to decide if we can ship with this limitation or if we need a different rendering library entirely.

**[2026-09-10 12:32] Diana**: Agreed. It only affects a small subset of complex documents, but we should document it as a known issue.
