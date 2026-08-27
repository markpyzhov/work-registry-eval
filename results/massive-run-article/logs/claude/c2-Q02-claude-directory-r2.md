# What did the Go SIG decide to do with Nico’s large runtime-tracer / profiling public-API proposal?

<!-- RESPONSE_START -->

## Decision: defer the large public-API change; go incremental instead

At the OpenTelemetry Go SIG meeting on **2025-11-27** (attendees: Robert Pająk, Damien Mathieu, Nico Hertz, Michal Jarmolkiewicz, Bryan Boreham), the SIG reviewed Nico Hertz's PR integrating Go runtime tracing / `pprof` profiling with spans and decided **not to merge it as-is**.

**What was decided** (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3974113940.md`, `SRC-NOTE-08`):
- Do **not** merge large public API changes without prior issue discussion.
- Keep the current large PR as a **draft / proof of concept**.
- Open an issue documenting the profiling proposal (problem statement, alternatives, pros/cons, links to Go runtime and `pprof` semantics) before continuing with API changes.
- Proceed **incrementally**, starting with a small change — the ability to **disable the runtime tracer integration**.

**The proposal itself** covered: today each span creates a runtime tracing *task*, which adds noise to profiles; Nico proposed more control over task/region creation with modes — *default* (task only for the root span), *auto* (task for root span, regions for child spans), *manual* (explicit user instrumentation) — plus an optional async-style hint for spans crossing goroutines.

**Why it was held back**: tasks can span multiple goroutines while regions must stay within one; changing public tracing APIs is sensitive and tightly coupled to the specification; and there was risk of breaking existing instrumentation (e.g., Kafka libraries).

**Action items assigned to Nico Hertz**: open the issue describing the runtime-profiling problem and proposal (modes, semantics, trade-offs), and create the smaller PR allowing the runtime tracer integration to be disabled. (He also asked for smaller starter tasks and was pointed at flaky tests in `opentelemetry-go-contrib`.)

**Current status** — tracked as `T002` in `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-04-release-process.md` (status `in_progress`, last updated 2025-11-27): the task is still open, and the sources **do not establish that either follow-up (the issue or the smaller disablement PR) was actually filed**. The index confirms the item as "deferred pending issue + smaller PR," with the large runtime-profiling API change listed under blocked/deferred items (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/index.md`).

No later human corrections touch this workstream — the 2026-03 comments file only affects WS-03 and WS-05 (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/comments/2026-03.md`).
