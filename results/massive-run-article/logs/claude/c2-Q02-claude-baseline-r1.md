# What did the Go SIG decide to do with Nico’s large runtime-tracer / profiling public-API proposal?

<!-- RESPONSE_START -->

I don't have anything on this in my parametric knowledge, and I'd be making it up if I gave you a decision.

Specifically, nothing matches on any of the three pieces:

- **"Go SIG"** — the upstream Go project doesn't use SIGs (that's a Kubernetes convention). Go's own process runs through the proposal process and the proposal review committee, with the runtime/diagnostics work discussed in the diagnostics working group. So "Go SIG" reads to me like a group internal to your org or another project entirely, not something in public Go history I'd know about.
- **"Nico"** — I can't place a Nico attached to a major runtime-tracer or profiling public-API proposal. The upstream work in that area I do know is associated with other people (e.g. Michael Knyszek on the trace v2 rewrite and the `runtime/trace` flight recorder, Felix Geisendörfer on profiling/tracing contributions). I have no record of a Nico-authored proposal there, and I don't want to guess that one of those is who you mean.
- **The decision itself** — no recollection of an outcome (accept / decline / split into smaller proposals / hold for a release cycle), so I can't even give you a hedged version.

Two likely explanations: this is an internal decision from your own group's meetings, or it's public work that landed after my cutoff or is too niche to have registered.

If it's the former, the material almost certainly exists in your meeting transcripts, Slack, or ClickUp — I have connectors for all three and could pull the actual decision, but you've asked me not to use tools here, so say the word if you want me to go look. If it's public Go work, point me at the proposal number or issue and I can tell you whether I know anything about it.
