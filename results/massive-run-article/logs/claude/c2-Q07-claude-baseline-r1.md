# What did the Go SIG decide about the OTelConf RC support PR that was blocking the next release?

<!-- RESPONSE_START -->

I don't have knowledge of this. I have no information about a Go SIG decision on an "OTelConf RC support" PR, and I can't verify anything here — you've asked me to answer purely from parametric memory with no tools, and this is the kind of specific, recent project-governance detail that I would only get right by looking it up.

A few things worth flagging about the premise:

- **"OTelConf"** isn't a name I recognize as an established OpenTelemetry artifact. There is an OpenTelemetry **declarative configuration** effort (file-based config, sometimes shortened to "otelconf"), and the Go implementation lives in `go.opentelemetry.io/contrib/otelconf`. If that's what you mean, I know the general shape of the project but not the state of any specific RC-support PR or SIG decision on it.
- **Which "Go SIG"** matters too — OpenTelemetry Go SIG, Kubernetes SIG, and others all exist, and the answer would differ.
- **Cutoff timing**: even at a February 2026 cutoff, individual PR outcomes and SIG meeting decisions are rarely something I'd hold reliably. I'd rather say I don't know than reconstruct a plausible-sounding decision.

If you want a real answer, the sources that would have it are the OpenTelemetry Go SIG meeting notes (public Google Doc, linked from the community repo), the `#otel-go` CNCF Slack channel, or the PR thread itself in `open-telemetry/opentelemetry-go` or `opentelemetry-go-contrib`. I have tools available in this session — say the word and I can go look it up rather than guess.
