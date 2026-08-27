# What did the Go SIG decide to do with Nico’s large runtime-tracer / profiling public-API proposal?

<!-- RESPONSE_START -->

## Answer

The SIG declined to take the large PR as-is and told Nico Hertz to break it up and document the design first.

**What was proposed (Nico's PR):** Go runtime profiling (`pprof`) integration control. Today every span creates a runtime tracing *task*, which adds noise to profiles. His PR added public-API control over task/region creation with several modes — **Default** (task only for the root span), **Auto** (task for root span, regions for child spans), **Manual** (explicit user instrumentation) — plus an optional async-style hint for spans crossing goroutines.

**Concerns raised:**
- Tasks can span multiple goroutines, but regions must stay within a single goroutine.
- Changing public tracing APIs is sensitive and tightly coupled to the OTel specification.
- Risk of breaking changes for existing instrumentation (e.g., Kafka libraries).

**Decisions:**
- Do **not** merge large public API changes without prior issue discussion.
- Proceed incrementally, starting with a small change — e.g., the ability to disable the runtime tracer integration.
- Open an issue documenting the profiling proposal before continuing with API changes.
- Keep the current large PR as a **draft / proof of concept**.

**Action items for Nico:**
- Open an issue describing the runtime profiling problem and proposal (modes, semantics, trade-offs), including problem statement, alternatives, pros/cons, and links to Go runtime and `pprof` semantics.
- Create a smaller PR to allow disabling the runtime tracer integration.
- Explore flaky test issues in `contrib` (he had asked for smaller starter tasks).

Maintainers also offered onboarding support (buddy/help via Slack) and reiterated general guidance to prefer atomic PRs — "if a PR contains 'and', it likely should be split."

**Source:** [SRC-NOTE-08] — Meeting Note: OpenTelemetry Go SIG, meeting dated 2025-11-27 (posted 2026-02-27 by pellared), attendees Robert Pająk, Damien Mathieu, Nico Hertz, Michal Jarmolkiewicz, Bryan Boreham. `opentelemetry/meeting-notes/entry-3974113940.md`, canonical URL https://github.com/open-telemetry/opentelemetry-go/issues/6648#issuecomment-3974113940

The dataset contains no later record showing whether the follow-up issue or the smaller "disable" PR was actually opened, so the outcome beyond this meeting isn't covered.
