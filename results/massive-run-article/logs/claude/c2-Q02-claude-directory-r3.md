# What did the Go SIG decide to do with Nico’s large runtime-tracer / profiling public-API proposal?

<!-- RESPONSE_START -->

## Answer

The OpenTelemetry Go SIG **deferred the large public-API change and told Nico Hertz to break it up**, rather than merging it.

### What the proposal was
Nico Hertz had an open PR integrating Go runtime profiling (`pprof`) with tracing. The problem: every span currently creates a runtime tracing **task**, which adds noise to profiles. His proposal added control over task/region creation via modes — **default** (task only for the root span), **auto** (task for root span, regions for child spans), and **manual** (explicit user instrumentation) — plus an optional async-style hint for spans crossing goroutines. (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3974113940.md`)

### The decision (SIG meeting of 2025-11-27, notes posted 2026-02-27)
1. **Do not merge large public API changes without prior issue discussion.**
2. **Keep the existing large PR as a draft / proof of concept.**
3. **Proceed incrementally** — start with a small change, e.g. the ability to *disable* the runtime tracer integration.
4. **Open an issue first** documenting the profiling proposal (problem statement, alternatives, pros/cons, links to Go runtime and `pprof` semantics) before continuing with API changes.

The stated concerns driving this: tasks can span multiple goroutines while regions must stay within one; changing public tracing APIs is sensitive and tightly coupled to the specification; and there is risk of breaking existing instrumentation (Kafka libraries were named). (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3974113940.md`)

### Action items assigned to Nico
- Open an issue describing the runtime profiling problem and proposal (modes, semantics, trade-offs).
- Create a smaller PR allowing the runtime tracer integration to be disabled.
- (Separately) explore flaky test issues in `contrib`, as a smaller starter task he had asked for.

### Current status
Tracked as task `T002` in `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-04-release-process.md` (status: in_progress, P1). Both follow-ups remain **unchecked** — the work state notes explicitly that "Sources do not establish that either follow-up was filed," and no issue or smaller PR body is present in the package. The registry index lists the topic as "deferred pending issue + smaller PR," with the large runtime-profiling API change under blocked/deferred items (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/index.md`).
