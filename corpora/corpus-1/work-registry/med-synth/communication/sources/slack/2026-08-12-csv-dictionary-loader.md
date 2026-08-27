**Source ID**: SRC-SLACK-50

# Slack Thread: CSV Dictionary Loader
**Channel**: #cipherdoc
**Date**: 2026-08-12

---

**[2026-08-12 11:21] Bob**: Working on the CSV loader for custom dictionary support. I'm thinking we support a simple two-column format: `term,tag`.

**[2026-08-12 11:29] Charlie**: Can we support regex in the dictionary too, or is it strictly string matching?

**[2026-08-12 11:40] Bob**: For the first pass, I'm just doing exact string matches and case-insensitive substrings. Regex in the dictionary might blow up the processing time if the list gets huge.

**[2026-08-12 11:41] Alice**: @Bob we need to make sure this works with the existing HIPAA identifiers. If a user adds a custom name to the dictionary, it should be treated with the same priority.

**[2026-08-12 13:00] Bob**: Definitely. The `DictionaryMatcher` will run alongside the regex engine.

**[2026-08-12 13:30] Diana**: @Bob what happens if there's a comma in the term? Standard CSV escaping?

**[2026-08-12 13:32] Bob**: Yeah, I'm using the Python `csv` module with `QUOTE_MINIMAL`. I'll add a test case for quoted terms.
