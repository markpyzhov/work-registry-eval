**Source ID**: SRC-SLACK-18

# Slack Thread: HIPAA Identifier Enumeration
**Channel**: #cipherdoc
**Date**: 2026-08-03

---

**[2026-08-03 14:08] Charlie**: Kicking off the HIPAA pattern work. Compliance wants coverage beyond financial PII, so we need to expand detection to the HIPAA identifier set. Right now we're mainly on names, SSNs, and birthdays.

**[2026-08-03 14:32] Diana**: Do you have the full identifier list yet, or still mapping it?

**[2026-08-03 15:12] Charlie**: Mapping it now. Plenty of these will be noisier than the financial patterns — need to be careful what we actually put in the dictionary.

**[2026-08-03 15:26] Alice**: Stay on enumeration for this pass. Dictionary update can follow once the list is solid.

**[2026-08-03 15:27] Charlie**: Will do. Goal today is a clean identifier inventory, not the merge.
