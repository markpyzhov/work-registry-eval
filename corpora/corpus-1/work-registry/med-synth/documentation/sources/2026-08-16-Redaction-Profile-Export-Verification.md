**Source ID**: SRC-GDOC-43

# Verification Note: Redaction-Profile Schema Export vs. REST API Contract
**Owner**: Diana
**Document Key**: DOC-2043
**Last Updated**: 2026-08-16

## What Was Verified
The exportable redaction-profile schema (designed by Bob, exposed via a REST endpoint) was checked against the already-completed REST API contract (T004) to confirm the export format matches what the API endpoints actually accept and return — no drift between the documented schema and live endpoint behavior.

## Method
Round-tripped a sample profile through the export endpoint, captured the emitted schema, and diffed its structure against the REST API's contract from T004. Also exercised import of the exported profile into a fresh instance to confirm no manual patching was required.

## Result
Export output matched the T004 contract on every field checked, and the round-tripped profile imported cleanly with no manual intervention. This closes the schema-export verification as Completed, dependent on T004's already-completed API work.

*Status*: Completed. Schema export confirmed consistent with the T004 REST API contract.
