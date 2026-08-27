# What did the Go SIG decide to do with Nico’s large runtime-tracer / profiling public-API proposal?

<!-- RESPONSE_START -->

The Go SIG deferred Nico’s large runtime-tracer/`pprof` public-API proposal. They decided not to merge it until an issue had documented and discussed the problem, alternatives, trade-offs, and Go runtime/`pprof` semantics. The existing large PR should remain a draft/proof of concept.

Instead, Nico was to pursue a small, incremental PR that lets users disable runtime-tracer integration. The corpus does not establish that either follow-up was filed. [WS-04 release-process](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-04-release-process.md:17) [Go SIG meeting note](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3974113940.md:90)
