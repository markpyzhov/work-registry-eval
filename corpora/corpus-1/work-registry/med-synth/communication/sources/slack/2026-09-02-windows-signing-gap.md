**Source ID**: SRC-SLACK-37

# Slack Thread: Windows Signing Gap
**Channel**: #releases
**Date**: 2026-09-02

---

**[2026-09-02 09:14] Evan**: Windows Defender and SmartScreen are both flagging the build for pilot testers — unsigned binaries get treated as untrusted by default.

**[2026-09-02 10:13] Alice**: Is the missing code-signing certificate the actual blocker here?

**[2026-09-02 10:14] Evan**: Yes. We still don't have one. Until we do, every pilot install is going to trip a warning at best, get blocked outright at worst.

**[2026-09-02 10:16] Diana**: Release blocker?

**[2026-09-02 10:17] Bob**: Copy.

**[2026-09-02 10:18] Evan**: It stays open as far as I'm concerned — this isn't something we can work around on the engineering side, we need the certificate.

**[2026-09-02 10:59] Alice**: Let's keep it open on the release gate rather than pushing it off the board. I'll chase the certificate process.
