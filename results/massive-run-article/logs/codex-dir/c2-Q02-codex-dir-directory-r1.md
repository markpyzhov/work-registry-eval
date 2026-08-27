# What did the Go SIG decide to do with Nico’s large runtime-tracer / profiling public-API proposal?

<!-- RESPONSE_START -->

The Go SIG deferred Nico’s large runtime-tracer / `pprof` public-API change: it should not be merged without prior issue discussion. They decided to keep the existing PR as a draft/proof of concept, have Nico open an issue documenting the problem, alternatives, semantics, and trade-offs, and proceed first with a smaller PR to let users disable runtime-tracer integration. The Corpus does not establish that either follow-up was filed. [WS-04-release-process.md](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-04-release-process.md:17) [meeting note](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3974113940.md:90)
