**Source ID**: SRC-SLACK-10

# Slack Thread: CLI and API Parity Check
**Channel**: #cipherdoc
**Thread opened**: 2026-07-11
**Last activity**: 2026-07-20

---

**[2026-07-11 10:03] Bob**: Finalizing the CLI-API parity audit. I've done a full pass of the CLI arguments vs the REST API endpoints.

**[2026-07-11 10:38] Diana**: Are we sure the redaction flags are consistent? Last time I checked, the CLI was using `--mask-pii` but the API expected `mask_all`.

**[2026-07-11 10:54] Bob**: Fixed that in the last PR. Both now use the standardized `policy_name` from the YAML config.

**[2026-07-11 10:56] Bob**: Just did the final parity confirm. Both interfaces are now calling the same underlying `CoreProcessor`.

**[2026-07-11 10:57] Diana**: Great. I'll run the integration test suite one last time to confirm.

**[2026-07-11 11:08] Alice**: This is a big milestone. Parity means we can start focusing on the specialized local runtime features.

**[2026-07-20 09:28] Bob**: Writing up the parity confirmation for the release evidence pack — ties back to the batch CLI and REST API work directly.

**[2026-07-20 09:36] Diana**: Sounds right, that's the record we'll want on file before the release checklist review.
