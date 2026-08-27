# What did the Go SIG decide to do with Nico’s large runtime-tracer / profiling public-API proposal?

<!-- RESPONSE_START -->

## Answer

The SIG declined to take the large PR as-is and told Nico to break the work down.

**Context (OpenTelemetry Go SIG, meeting dated 2025-11-27):** Nico Hertz asked for reviews on his PR adding Go runtime profiling (`pprof`) integration control. The problem: today every span creates a runtime tracing **task**, which adds noise to profiles. His proposal introduced modes — **Default** (task only for the root span), **Auto** (task for root span, regions for child spans), **Manual** (explicit user task/region instrumentation) — plus an optional async-style hint for spans crossing goroutines.

**Concerns raised:**
- Tasks can span multiple goroutines, but regions must stay within one goroutine.
- Changing public tracing APIs is sensitive and tightly coupled to the OTel specification.
- Risk of breaking changes for existing instrumentation (e.g., Kafka libraries).

**Decisions:**
- Do **not** merge large public API changes without prior issue discussion.
- Proceed incrementally, starting with a small change — e.g., the ability to disable the runtime tracer integration.
- Open an issue documenting the profiling proposal (problem statement, alternatives, pros/cons, links to Go runtime and `pprof` semantics) before continuing with API changes.
- Keep the current large PR as a **draft / proof of concept**.

**Action items for Nico:** open the issue describing the problem and proposal (modes, semantics, trade-offs); create a smaller PR to allow disabling the runtime tracer integration; and (separately) explore flaky test issues in `contrib`. Maintainers were to provide onboarding/buddy support via Slack.

**Source:** [SRC-NOTE-08] — Meeting Note: OpenTelemetry Go SIG, `opentelemetry/meeting-notes/entry-3974113940.md`, author pellared, https://github.com/open-telemetry/opentelemetry-go/issues/6648#issuecomment-3974113940

Note: the dataset contains no later record showing whether the follow-up issue or smaller PR was actually filed, so the outcome beyond this meeting is not covered.
