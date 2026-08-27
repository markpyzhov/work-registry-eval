**Source ID**: SRC-SLACK-52

# Slack Thread: CSV Dictionary Matcher Wiring
**Channel**: #cipherdoc
**Date**: 2026-08-14

---

**[2026-08-14 10:16] Charlie**: Starting to wire the CSV terms into the detection matcher. Want the `DictionaryMatcher` to run inline with the regex engine, not as a separate pass.

**[2026-08-14 10:22] Bob**: Loader's ready on my end — it emits normalized `(term, tag)` tuples, so you can just merge those into whatever internal structure the regex engine already uses.

**[2026-08-14 10:48] Charlie**: That works. I'll key it the same way we key the HIPAA patterns so priority handling stays consistent.

**[2026-08-14 10:54] Diana**: Once it's wired, I want to run the merged HIPAA + CSV rule set through the standard test file. Should catch anything obviously broken.

**[2026-08-14 10:58] Charlie**: Sounds good. Should have it wired by end of day, then you can start on that test pass.
