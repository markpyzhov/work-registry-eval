# Work State Index

**Source cutoff**: 2026-02-27T17:20:46Z
**Final Work State through**: 2026-03-11

**Source link scheme:** paths are relative to the final handoff location
`work-registry/work-states/` → `../opentelemetry/...`. In the curator package, resolve the
same paths via the `opentelemetry` → `work-registry/opentelemetry` symlink (no content rewrite
at handoff).

| Area | Description | Status |
|---|---|---|
| [WS-01-sdk-logs](./WS-01-sdk-logs.md) | SDK log `Record` mutation fix | completed |
| [WS-02-metrics-performance](./WS-02-metrics-performance.md) | Metrics SDK performance and temporality-selector configuration | in_progress |
| [WS-03-security-fuzzing](./WS-03-security-fuzzing.md) | OSS-Fuzz notification path and release signing / immutable releases | in_progress |
| [WS-04-release-process](./WS-04-release-process.md) | OTelConf RC support, experimental API structure, runtime profiling | in_progress |
| [WS-05-contrib](./WS-05-contrib.md) | Contrib instrumentation (otelgin, otelhttp, otelgrpc, otelconf) and Explorer proposal | in_progress |

## Item coverage (primary references)

| Primary reference | Workstream | As-of state |
| --- | --- | --- |
| `opentelemetry-go#7403` | SDK Logs | merged and released in `v1.39.0` |
| `opentelemetry-go#7427` | Metrics Performance | merged and released in `v1.39.0` |
| `opentelemetry-go#7443` | Metrics Performance | merged; release not established |
| `opentelemetry-go#7474` | Metrics Performance | merged; release not established |
| Temporality-selector configuration (SIG topic) | Metrics Performance | custom parsing rejected; selector functions released in `v1.39.0` |
| `opentelemetry-go#7549` | Security and Fuzzing | maintainers mailing-list + trial complete; public auto-filing deferred; GitHub issue still open |
| `sig-security#164` | Security and Fuzzing | deferred pending release-tooling confirmation; GitHub issue still closed |
| OTelConf RC / experimental API (SIG topic) | Release Process | decision recorded; delivery not in Sources |
| Runtime-tracer / profiling (SIG topic) | Release Process | deferred pending issue + smaller PR |
| `opentelemetry-go-contrib#5946` / `#6609` | Contrib | `RemoveAll()` adopted and local work complete; final commits unpushed; GitHub issue/PR open |
| `opentelemetry-go-contrib#7254` | Contrib | closed; release not established |
| `opentelemetry-go-contrib#8059` | Contrib | closed; linked PR `#8106` merge not in Sources |
| `opentelemetry-go-contrib#8078` | Contrib | restoration not planned; stabilization timing unresolved |
| `community#3000` | Contrib | proposal merged; Explorer delivery not established |
| `opentelemetry-go-contrib#8014` | Contrib | closed without merge |

## Key blockers and active items

- **Active / open**: publication of the completed local otelgin cleanup (`#5946` / `#6609`); OTelConf RC / experimental API tracking; runtime profiling follow-ups; `#8014` closed without merge (not done).
- **Completed internally, external record pending**: otelgin `RemoveAll()` cleanup; OSS-Fuzz maintainers mailing-list + trial-monitoring path.
- **Merged but unreleased**: `#7443`, `#7474` (moved to `v1.40.0`; no `v1.40.0` release Source).
- **Blocked / deferred**: immutable/signature-release enablement (release-tooling confirmation); `otelgrpc` stabilization (RPC semconv + gRPC engagement); public OSS-Fuzz GitHub auto-filing; large runtime-profiling API change.
