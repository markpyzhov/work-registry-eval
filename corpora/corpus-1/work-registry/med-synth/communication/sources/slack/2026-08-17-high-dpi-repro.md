**Source ID**: SRC-SLACK-56

# Slack Thread: High-DPI Repro
**Channel**: #cipherdoc
**Date**: 2026-08-17

---

**[2026-08-17 10:13] Charlie**: Finally reproduced the offset mismatch on 4K displays. It looks like we're not accounting for the device pixel ratio when calculating the bounding box for the redaction masks.

**[2026-08-17 10:15] Diana**: That explains why my screenshots were always slightly off to the left on the high-res monitor.

**[2026-08-17 10:18] Charlie**: Exactly. The internal coordinate system is in PDF points (72 DPI), but the renderer is using pixels. On a 4K screen with 200% scaling, that offset is doubled.

**[2026-08-17 10:21] Bob**: Are we doing the math in the engine or the preview UI?

**[2026-08-17 10:30] Charlie**: It's happening in the `BoundingBoxTranslator` in the engine. I need to normalize everything back to the raw PDF dimensions before we generate the mask.

**[2026-08-17 10:32] Alice**: @Charlie how long for a fix? This is blocking the final verification of the preview UI for high-res users.

**[2026-08-17 11:00] Charlie**: I'm working on the scaling math now. Should have a PR for testing by tomorrow.
