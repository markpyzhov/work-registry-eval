**Source ID**: SRC-SLACK-14

# Slack Thread: Local Runtime Static Linking Study
**Channel**: #cipherdoc
**Date**: 2026-08-02

---

**[2026-08-02 08:54] Alice**: For the air-gapped local runtime work, we need a binary that doesn't pull in dynamic cloud or runtime dependencies at startup. Evan, can you look at static linking options?

**[2026-08-02 09:32] Evan**: On it. Studying whether we can statically link `re2` and the rest of the C dependencies so the binary doesn't need anything from the host beyond libc.

**[2026-08-02 09:39] Evan**: A few options on the table — full static compile, or a hybrid where only the riskiest dynamic deps get bundled. Leaning toward full static for the cleanest air-gap story.

**[2026-08-02 09:42] Diana**: Any concerns with the C++ engine core specifically?

**[2026-08-02 09:48] Evan**: That's the trickiest part, but nothing that rules it out. I'll have a recommendation once I've tried a static build end to end.

**[2026-08-02 09:51] Alice**: Keep this moving — the release checklist is tracking the static-link work alongside the Docker slim-down.
