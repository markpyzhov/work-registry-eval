**Source ID**: SRC-SLACK-57

# Slack Thread: High-DPI Scaling Math
**Channel**: #cipherdoc
**Date**: 2026-08-19

---

**[2026-08-19 13:51] Charlie**: Okay, I've updated the scaling math to use the `pdf-renderer`'s internal viewport dimensions instead of raw screen pixels, and cross-checked it against the preview-overlay coordinates from the redaction preview work — that's where the scale-factor error was showing up most.

**[2026-08-19 14:26] Diana**: I'm still seeing a 1-2 pixel drift on some documents. It's better, but not perfect.

**[2026-08-19 14:31] Charlie**: Are those documents rotated? I might need to check the rotation matrix too.

**[2026-08-19 14:34] Diana**: Yeah, the one that's drifting is a landscape scan.

**[2026-08-19 14:39] Charlie**: Got it. The coordinate transform for rotated pages in PDF is notorious. I'll add a check for the `/Rotate` key in the page dictionary.

**[2026-08-19 14:41] Bob**: @Charlie do we need to worry about different DPIs between monitors in a multi-head setup?

**[2026-08-19 14:44] Charlie**: Hopefully not if we stay in PDF point-space. I'll verify that tomorrow.
