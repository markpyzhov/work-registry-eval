# What did the Go SIG decide to do with Nico’s large runtime-tracer / profiling public-API proposal?

<!-- RESPONSE_START -->

The Go SIG deferred Nico’s large runtime-tracer/profiling public-API proposal. They decided not to merge it without prior issue discussion, to keep the existing PR as a draft/proof of concept, and to first:

- open an issue documenting the problem, modes, semantics, alternatives, and trade-offs; and
- make a smaller change allowing runtime-tracer integration to be disabled.

The work state remains “deferred pending issue + smaller PR.” [WS-04 Release Process, T002; SRC-NOTE-08]
