# What did the Go SIG decide to do with Nico’s large runtime-tracer / profiling public-API proposal?

<!-- RESPONSE_START -->

## Answer

The Go SIG declined to take Nico Hertz's large PR as-is and asked him to break the work down, starting with a design issue and a much smaller code change.

**What was proposed (Nico Hertz's PR)**

Go runtime profiling (`pprof`) integration. Today every span creates a runtime tracing **task**, which adds noise to profiles. Nico's PR would give users more control over task/region creation via modes:
- **Default** — task only for the root span
- **Auto** — task for root span, regions for child spans
- **Manual** — explicit task/region instrumentation by the user
- Plus an optional async-style hint for spans that cross goroutines

**Concerns raised**
- Tasks can span multiple goroutines, but regions must stay within a single goroutine.
- Changing public tracing APIs is sensitive and tightly coupled to the OTel specification.
- Risk of breaking changes for existing instrumentation (e.g. Kafka libraries).

**Decisions (Go SIG meeting of 2025-11-27)**
1. Do **not** merge large public API changes without prior issue discussion.
2. Proceed incrementally — start with a small change, e.g. the ability to **disable** the runtime tracer integration.
3. Open an issue documenting the profiling proposal (problem statement, alternatives, pros/cons, links to Go runtime and `pprof` semantics) **before** continuing with API changes.
4. Keep the current large PR as a **draft / proof of concept**.

**Action items assigned to Nico Hertz**
- Open an issue describing the runtime profiling problem and proposal (modes, semantics, trade-offs).
- Create a smaller PR allowing the runtime tracer integration to be disabled.
- Explore flaky test issues in `contrib` (as a smaller starter task he had asked for).

Related general guidance from the same meeting: prefer atomic PRs, one change per PR — "if a PR contains 'and', it likely should be split."

**Source**
- `opentelemetry/meeting-notes/entry-3974113940.md` — [SRC-NOTE-08], "Meeting Note: OpenTelemetry Go SIG", meeting date 2025-11-27, posted by pellared at https://github.com/open-telemetry/opentelemetry-go/issues/6648#issuecomment-3974113940 (attendees: Robert Pająk, Damien Mathieu, Nico Hertz, Michal Jarmolkiewicz, Bryan Boreham)

Note: this meeting note is the only record of the decision in the dataset. It contains no follow-up showing whether the issue or the smaller "disable" PR was actually opened or merged.
