# What did the Go SIG decide to do with Nico’s large runtime-tracer / profiling public-API proposal?

<!-- RESPONSE_START -->

No comments touch this topic. Here's the answer.

## Decision: deferred, not merged — split into a smaller incremental change first

At the **OpenTelemetry Go SIG meeting of 2025-11-27** (attendees: Robert Pająk, Damien Mathieu, Nico Hertz, Michal Jarmolkiewicz, Bryan Boreham), the SIG declined to take Nico Hertz's large runtime-tracer / `pprof` profiling public-API PR as-is.

**What the proposal was**
- Problem: every span currently creates a Go runtime tracing **task**, which adds noise to profiles.
- Proposed: more control over task/region creation via modes — **Default** (task only for the root span), **Auto** (task for root span, regions for child spans), **Manual** (explicit user instrumentation) — plus an optional async-style hint for spans crossing goroutines.

**Why the SIG held off**
- Changing public tracing APIs is sensitive and tightly coupled to the specification.
- Risk of breaking changes for existing instrumentation (e.g. Kafka libraries).
- Semantic constraint: tasks can span goroutines, but regions must stay within one goroutine.

**The decisions recorded**
1. Do **not** merge large public API changes without prior issue discussion.
2. Keep the current large PR as a **draft / proof of concept**.
3. Open an issue first documenting the problem statement, alternatives, pros/cons, and links to Go runtime and `pprof` semantics.
4. Proceed incrementally — start with a small change, e.g. the ability to **disable** the runtime tracer integration.

**Action items on Nico Hertz:** open the proposal issue, create the smaller disablement PR, and (separately) look at flaky tests in `contrib` as starter work.

**Current status:** tracked as `T002` in WS-04 (Release Process), which is `in_progress`, with the item listed as **"deferred pending issue + smaller PR"** and the large runtime-profiling API change listed under blocked/deferred. The package does not establish that either follow-up (the issue or the smaller disablement PR) was actually filed; that is the open "next update needed."

**Sources**
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3974113940.md` (`SRC-NOTE-08`)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-04-release-process.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/index.md`
