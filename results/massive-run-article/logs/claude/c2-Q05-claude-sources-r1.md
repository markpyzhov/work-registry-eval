# Is custom temporality-selector configuration supported in OpenTelemetry Go `v1.39.0`, and what related selector API did that release ship?

<!-- RESPONSE_START -->

## Answer

Two related but distinct things, and the sources separate them cleanly.

**Custom temporality-selector *configuration* — not supported.** The proposal to expose temporality-selector *parsing* functions (a string-based "temporality select" for configuration snippets) was rejected and its PR closed:

- SIG 2025-09-25 [SRC-NOTE-01]: "PR exists; default temporality aggregation functions were not exposed; proposal includes a string-based 'temporality select.'" Concern: "Replacing functions via string selector raised concerns."
- SIG 2025-10-09 [SRC-NOTE-03]: Decision — "Not recommended for inclusion in SDK. Users should use full OpenTelemetry configuration file format instead of custom configuration snippets." Rationale: "Want to standardize on OTel configuration format rather than supporting fragmented approaches."
- SIG 2025-10-16 [SRC-NOTE-04]: "Tyler noted that a previous SIG meeting concluded this PR was API pollution and should be closed. He will draft a comment and close it today." Also listed as a Tyler Yahn action item.

So the sanctioned path for config-driven temporality is the OTel declarative configuration file format (`OTEL_EXPERIMENTAL_CONFIG_FILE`), which was itself being pursued in contrib/`otelconf` rather than the SDK [SRC-NOTE-05, SRC-ISSUE-05].

**What v1.39.0 *did* ship — plain selector functions.** From the release notes [SRC-REL-01], under Added:

> Add temporality selector functions `DeltaTemporalitySelector`, `CumulativeTemporalitySelector`, `LowMemoryTemporalitySelector` to `go.opentelemetry.io/otel/sdk/metric`. (#7434)

The changelog entry lists it as "Add temporality selector functions by @dprotaso" in PR [#7434](https://github.com/open-telemetry/opentelemetry-go/pull/7434). Release v1.39.0/v0.61.0/v0.15.0/v0.0.14, tagged and published 2025-12-08 by MrAlias.

## The distinction worth noting

The naming is confusingly close, so be careful reading the two together: the *closed* item was "Expose temporality selector functions" (the string-parsing/config layer), while the *merged* #7434 shipped the three ready-made selector functions with no string-based configuration surface. The sources state both outcomes as fact; that the merged PR is the objection-free subset of the original proposal is a reasonable inference from the two records, but no source in this dataset explicitly narrates the relationship between the closed PR and #7434.

Net: in v1.39.0 you can pass `DeltaTemporalitySelector`, `CumulativeTemporalitySelector`, or `LowMemoryTemporalitySelector` programmatically from `sdk/metric`, but there is no supported string/config-snippet mechanism for selecting temporality — use the OTel config file format for that.

## Sources cited

- `opentelemetry/releases/release-v1.39.0.md` [SRC-REL-01]
- `opentelemetry/meeting-notes/entry-3389930076.md` [SRC-NOTE-01], SIG 2025-09-25
- `opentelemetry/meeting-notes/entry-3390010099.md` [SRC-NOTE-03], SIG 2025-10-09
- `opentelemetry/meeting-notes/entry-3479584781.md` [SRC-NOTE-04], SIG 2025-10-16
- `opentelemetry/meeting-notes/entry-3479626706.md` [SRC-NOTE-05], SIG 2025-10-23
- `opentelemetry/issues/opentelemetry-go-contrib-8059.md` [SRC-ISSUE-05]
