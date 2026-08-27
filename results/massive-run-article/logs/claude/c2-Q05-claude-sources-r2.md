# Is custom temporality-selector configuration supported in OpenTelemetry Go `v1.39.0`, and what related selector API did that release ship?

<!-- RESPONSE_START -->

## Answer

**Custom (string-based) temporality-selector configuration is not supported in v1.39.0.** What v1.39.0 shipped instead is a small set of three predefined, exported temporality selector functions.

### What was rejected

The Go SIG explicitly declined the custom-configuration part of the proposal:

- **2025-09-25 SIG** — the PR proposed a string-based "temporality select" so users could replace the default temporality aggregation functions via configuration. Concern was raised specifically about "replacing functions via string selector." Status at the time: no recent activity, likely to be moved out of the milestone. (`opentelemetry/meeting-notes/entry-3389930076.md`, SRC-NOTE-01)
- **2025-10-09 SIG** — Decision: "Not recommended for inclusion in SDK. Users should use full OpenTelemetry configuration file format instead of custom configuration snippets." Rationale: standardize on the OTel configuration format rather than support fragmented approaches. (`opentelemetry/meeting-notes/entry-3390010099.md`, SRC-NOTE-03)
- **2025-10-16 SIG** — Tyler Yahn noted a prior SIG had concluded the "Exposed Temporality Selector Function" PR was **API pollution and should be closed**; his action item was to draft a cohesive comment and close it. (`opentelemetry/meeting-notes/entry-3479584781.md`, SRC-NOTE-04)

### What v1.39.0 actually shipped

The v1.39.0 release notes (published 2025-12-08, tag `v1.39.0`) list under **Added**:

> Add temporality selector functions `DeltaTemporalitySelector`, `CumulativeTemporalitySelector`, `LowMemoryTemporalitySelector` to `go.opentelemetry.io/otel/sdk/metric`. (#7434)

The changelog also credits "Add temporality selector functions by @dprotaso in .../pull/7434". (`opentelemetry/releases/release-v1.39.0.md`, SRC-REL-01)

### Net effect

v1.39.0 exposes the three canonical selectors as named Go functions you pass directly in code (delta, cumulative, low-memory) — the previously unexported defaults. The configuration-driven mechanism for choosing/replacing them via string identifiers was cut; the SIG's stated alternative is the full OpenTelemetry configuration file format.

Caveat on the record: the sources show the SIG deciding to close the "exposed temporality selector function" work while the release notes show #7434 merged and shipped. The consistent reading is that the string-selector/custom-configuration portion was dropped and only the three exported preset functions landed, but no retrieved source states that reconciliation explicitly.

### Sources cited
- `/opentelemetry/releases/release-v1.39.0.md` — SRC-REL-01
- `/opentelemetry/meeting-notes/entry-3389930076.md` — SRC-NOTE-01 (SIG 2025-09-25)
- `/opentelemetry/meeting-notes/entry-3390010099.md` — SRC-NOTE-03 (SIG 2025-10-09)
- `/opentelemetry/meeting-notes/entry-3479584781.md` — SRC-NOTE-04 (SIG 2025-10-16)
