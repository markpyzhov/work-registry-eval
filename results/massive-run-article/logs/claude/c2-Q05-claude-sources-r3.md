# Is custom temporality-selector configuration supported in OpenTelemetry Go `v1.39.0`, and what related selector API did that release ship?

<!-- RESPONSE_START -->

## Answer

**Custom temporality-selector configuration: not supported in v1.39.0.** The proposal to expose temporality-selector *parsing* functions so users could configure temporality from a custom config snippet (a string-based "temporality select") was reviewed by the Go SIG and rejected.

- SIG call 2025-10-09 (`opentelemetry/meeting-notes/entry-3390010099.md`, SRC-NOTE-03): "Expose temporality selector functions" — decision was **not recommended for inclusion in the SDK**; users should use the full OpenTelemetry configuration file format instead of custom configuration snippets, the rationale being standardization on the OTel config format rather than fragmented approaches.
- SIG call 2025-09-25 (`opentelemetry/meeting-notes/entry-3389930076.md`, SRC-NOTE-01): the PR's proposal "includes a string-based 'temporality select'"; replacing functions via a string selector "raised concerns."
- SIG call 2025-10-16 (`opentelemetry/meeting-notes/entry-3479584781.md`, SRC-NOTE-04): during the v1.39.0 milestone check-in, Tyler Yahn noted a previous SIG meeting concluded the "Exposed Temporality Selector Function" PR was **API pollution and should be closed**; his action item was to draft a comment and close it.

**What v1.39.0 did ship: three predefined temporality selector functions.** From the release notes (`opentelemetry/releases/release-v1.39.0.md`, SRC-REL-01, tag `v1.39.0`, published 2025-12-08), under Added:

> Add temporality selector functions `DeltaTemporalitySelector`, `CumulativeTemporalitySelector`, `LowMemoryTemporalitySelector` to `go.opentelemetry.io/otel/sdk/metric`. (#7434)

The same release's commit list credits this to PR #7434, "Add temporality selector functions" by @dprotaso.

**Net:** v1.39.0 exposes the three standard selector functions in `sdk/metric` so you can pick delta / cumulative / low-memory programmatically, but it deliberately does **not** ship the string/config-driven selector-parsing API — that path was closed as API pollution, with the OTel configuration file format as the sanctioned route.

One caveat worth flagging: the retrieved sources describe the closed "expose temporality selector functions" milestone item and the merged #7434 without explicitly reconciling them, so the most defensible reading is that the config-parsing/string-selection portion was dropped while the three named functions were merged.

**Sources cited** (all `path: sources`, dataset `74f29ea88a9c11f197db2303d7337e37`):
- `opentelemetry/releases/release-v1.39.0.md` [SRC-REL-01]
- `opentelemetry/meeting-notes/entry-3390010099.md` [SRC-NOTE-03]
- `opentelemetry/meeting-notes/entry-3389930076.md` [SRC-NOTE-01]
- `opentelemetry/meeting-notes/entry-3479584781.md` [SRC-NOTE-04]
