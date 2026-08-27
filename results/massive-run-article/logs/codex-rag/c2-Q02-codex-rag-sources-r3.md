# What did the Go SIG decide to do with Nico’s large runtime-tracer / profiling public-API proposal?

<!-- RESPONSE_START -->

The Go SIG decided not to merge Nico’s large public-API proposal as-is. They would keep it as a draft/proof of concept, first open an issue documenting the profiling problem, alternatives, and trade-offs, and pursue a small incremental PR—such as allowing runtime-tracer integration to be disabled. [SRC-NOTE-08](https://github.com/open-telemetry/opentelemetry-go/issues/6648#issuecomment-3974113940)
