**Source ID**: SRC-SLACK-66

# Slack Thread: A11y Screen Reader
**Channel**: #cipherdoc
**Date**: 2026-08-22

---

**[2026-08-22 14:02] Diana**: Just did a trial run with a screen reader (NVDA). It's completely skipping over the file upload status.

**[2026-08-22 14:56] Evan**: I need to add an `aria-live` region for the status updates. Otherwise, the screen reader doesn't know the DOM has changed.

**[2026-08-22 14:59] Diana**: Also, the "Redact" button just says "Button" with no description of what it actually does or which file it's targeting.

**[2026-08-22 15:45] Evan**: Got it. I'll add `aria-label` attributes to all the action icons today.

**[2026-08-22 16:04] Alice**: @Diana, are there any blocking issues that would fail a basic WCAG 2.1 check?

**[2026-08-22 16:41] Diana**: The contrast on the "Success" toast notifications is too low (light green on white). I'll send Bob the hex codes for a darker version.
