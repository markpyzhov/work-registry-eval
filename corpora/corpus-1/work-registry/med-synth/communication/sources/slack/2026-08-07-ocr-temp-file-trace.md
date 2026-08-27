**Source ID**: SRC-SLACK-28

# Slack Thread: OCR Temp File Trace
**Channel**: #cipherdoc
**Date**: 2026-08-07

---

**[2026-08-07 10:03] Charlie**: Tracing every place the OCR branch writes a temp file. We can't add cleanup hooks until we know all the sites that actually create one.

**[2026-08-07 10:06] Alice**: How many sites so far?

**[2026-08-07 10:19] Charlie**: More than I expected. Some go through the library's default temp handling, some are paths we wrote ourselves. They're not consistent.

**[2026-08-07 11:49] Diana**: QA saw a batch fail last week and leave a pile of orphaned temp files behind — that's probably one of the ones you haven't found yet.

**[2026-08-07 11:56] Charlie**: Probably. I'm building the full inventory now so nothing gets missed once the hooks go in.

**[2026-08-07 13:58] Evan**: Once you've got the list, want a second pass to confirm nothing's hiding behind a library default?

**[2026-08-07 13:59] Charlie**: Yeah, that'd help. I'll share the inventory once it's done.
