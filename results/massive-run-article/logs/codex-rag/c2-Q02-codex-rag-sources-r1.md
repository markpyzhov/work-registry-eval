# What did the Go SIG decide to do with Nico’s large runtime-tracer / profiling public-API proposal?

<!-- RESPONSE_START -->

The Go SIG decided **not to merge the large public-API proposal as submitted**. They wanted an incremental path instead:

- Keep the current PR as a draft/proof of concept.
- First add a small, focused change—such as allowing runtime-tracer integration to be disabled.
- Have Nico open an issue documenting the profiling problem, alternatives, semantics, and trade-offs before further API work.

[Source record: SRC-NOTE-08](https://github.com/open-telemetry/opentelemetry-go/issues/6648#issuecomment-3974113940)
