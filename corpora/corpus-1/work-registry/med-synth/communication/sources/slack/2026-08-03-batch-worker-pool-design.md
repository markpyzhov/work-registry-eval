**Source ID**: SRC-SLACK-30

# Slack Thread: Batch Worker Pool Design
**Channel**: #cipherdoc
**Date**: 2026-08-03

---

**[2026-08-03 11:09] Charlie**: Sketching out a worker pool model for local batch processing. It has to slot into the existing batch CLI rather than replace it.

**[2026-08-03 11:41] Bob**: Threads or separate processes? Given how CPU-heavy the redaction pass is, threads alone probably won't buy us much.

**[2026-08-03 11:43] Charlie**: Leaning toward processes for that reason. Still working out how workers get handed files without duplicating too much per-worker state.

**[2026-08-03 12:19] Alice**: Does this need to wait on anything, or can it move independently of the CLI work?

**[2026-08-03 12:36] Charlie**: It builds on top of the completed CLI, so the interface has to stay compatible, but the pool itself can be developed on its own.

**[2026-08-03 12:37] Diana**: One thing to keep in mind — if files are processed out of order across workers, the audit log ordering needs to still make sense.

**[2026-08-03 12:44] Charlie**: Good catch, I'll fold that into the design before I start wiring it up.
