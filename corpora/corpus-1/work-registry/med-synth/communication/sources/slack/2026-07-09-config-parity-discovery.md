**Source ID**: SRC-SLACK-13

# Slack Thread: Regex Flags Bug Discovery
**Channel**: #cipherdoc
**Date**: 2026-07-09

---

**[2026-07-09 08:56] Bob**: @Charlie, I found a discrepancy while running the CLI-API parity audit. The CLI is matching case-insensitive by default, but the REST API is case-sensitive for the same patterns.

**[2026-07-09 09:11] Charlie**: That's a bug in how the `ConfigLoader` passes flags to the engine. It should be pulling the `ignore_case` bit from the YAML.

**[2026-07-09 10:08] Bob**: Investigating now. Looks like the `RedactionRequest` Pydantic model in the API layer is defaulting `regex_flags` to 0 instead of reading the global config.

**[2026-07-09 10:11] Bob**: Found it. PR #52 is up. I've standardized the flag inheritance so the API and CLI use the exact same initialization logic.

**[2026-07-09 10:14] Charlie**: Nice catch. This would have caused some major headaches in production if some files were being missed because of casing.

**[2026-07-09 10:51] Bob**: PR #52 merged and verified. I've added a test case to the parity suite that checks `NAME` vs `name` across both interfaces.

**[2026-07-09 11:12] Diana**: Verified on my end too. Parity is holding up.
