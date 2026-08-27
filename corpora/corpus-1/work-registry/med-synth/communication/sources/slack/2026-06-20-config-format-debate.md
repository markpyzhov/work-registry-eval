**Source ID**: SRC-SLACK-04

# Slack Thread: Config Format Decision (YAML vs JSON)
**Channel**: #cipherdoc
**Date**: 2026-06-20

---

**[2026-06-20 10:45] Alice**: I know we said JSON on Thursday, but I'm revisiting the redaction policy config format. Charlie still wants JSON, but I think YAML is much more user-friendly for the policy definitions.

**[2026-06-20 10:46] Charlie**: JSON is easier to validate with JSONSchema, and we don't have to worry about whitespace issues.

**[2026-06-20 10:59] Alice**: True, but these policies will be managed by compliance officers, not just devs. Reading a 200-line JSON file is a nightmare. I'm making the call to go with YAML.

**[2026-06-20 11:02] Charlie**: Yep.

**[2026-06-20 11:48] Charlie**: Swapping to `PyYAML`. It's a bit more work to get the schema validation right, but I'll use a bridge to keep our JSONSchema files as the source of truth.

**[2026-06-20 11:58] Charlie**: Done. Schema update is pushed. The engine now accepts `.yaml` for all redaction profiles. 

**[2026-06-20 11:59] Alice**: Thanks, Charlie. This looks much cleaner. Can you add a sample `default-policy.yaml` to the repo?

**[2026-06-20 12:55] Charlie**: Already there in `configs/samples/`. :rocket:
