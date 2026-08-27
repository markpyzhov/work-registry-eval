**Source ID**: SRC-GDOC-28

# Custom Dictionary: CSV Loader Notes

**Owner**: Bob
**Document Key**: DOC-2028
**Last Updated**: 2026-08-29

*Retrospective note: summarizes the 2026-08-12 CSV dictionary loader for T034; written up today.*

Operators asked for org-specific redaction terms without forking the built-in pattern set. The chosen path is a user-supplied CSV dictionary that the engine can load alongside existing detection rules.

## Loader in place
On 2026-08-12 Bob implemented the CSV dictionary loader so those site-specific terms can be ingested into the pipeline. That closes the “how do we get custom terms into the process” question for the loader layer.

## What this does not cover
Matcher wiring and a formal rule-test pass are separate follow-ons. This note does not claim that custom terms already fire correctly end-to-end—only that the loader exists and T034 was Active at the time of that implementation.
