**Source ID**: SRC-GDOC-47

# Sign-off Note: Offline Batch Run (Preliminary)
**Owner**: Diana
**Document Key**: DOC-2047
**Last Updated**: 2026-08-10

## What Was Run
A full batch redaction run was executed under the offline test harness (T027) with network access denied, using a local sample document set. The run depended on the completed AES-256 at-rest encryption pipeline (T021), since offline output still needs to be encrypted without any network-based key service.

## Result
The batch completed successfully end-to-end with the network denied: no network-dependent call blocked the run, and local policy parsing worked entirely from bundled definitions.

## Noted Issue: 45-Second Licence-Check Hang
The run was not clean — the HTTP client attempted to verify the license key against a remote server before timing out and falling back to the cached local license, adding roughly 45 seconds of startup delay. This is logged as a known issue, not something this sign-off waives.

## Scope of This Sign-off
This sign-off is **preliminary** and covers functional completion of a batch run offline only. It is explicitly **not** a compliance certification — it does not cover side-channel analysis, physical security, or any regulatory attestation. No patient records or clinical data were used in this test run.
