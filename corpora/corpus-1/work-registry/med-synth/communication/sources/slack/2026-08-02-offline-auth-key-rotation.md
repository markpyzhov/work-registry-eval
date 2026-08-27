**Source ID**: SRC-SLACK-16

# Slack Thread: Offline Mode Authentication Design
**Channel**: #cipherdoc
**Date**: 2026-08-02

---

**[2026-08-02 11:14] Diana**: Starting on offline-mode auth design. If we're running air-gapped, we can't call home for license validation or user auth, so key rotation can't assume an always-on network either.

**[2026-08-02 11:16] Alice**: Right — whatever we design has to keep working with no connection for extended stretches.

**[2026-08-02 11:22] Diana**: I'm sketching a rotation flow built around a locally held key rather than one that needs a live call to rotate.

**[2026-08-02 13:00] Alice**: How do we actually rotate it if the site is air-gapped?

**[2026-08-02 14:24] Diana**: Still working that part out — that's the piece I'm least confident about. I'll have a first draft of the design by Wednesday.

**[2026-08-02 14:27] Diana**: I'll loop in Bob once the draft's ready so he can start mocking it for testing.
