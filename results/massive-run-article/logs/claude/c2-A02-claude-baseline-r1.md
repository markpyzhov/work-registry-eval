# On what date will otelgrpc module stabilization be complete?

<!-- RESPONSE_START -->

I don't have a specific date for this in my knowledge, and I don't believe one has been publicly committed to.

What I can say from memory (as of the stated Feb 2026 cutoff):

- `otelgrpc` (the gRPC instrumentation in `opentelemetry-go-contrib`, at `instrumentation/google.golang.org/grpc/otelgrpc`) was still shipping under `v0.x` version numbers, i.e. not stable.
- Its stabilization has been gated primarily on the **RPC semantic conventions** reaching stable status in the OpenTelemetry specification. That semconv work (RPC/gRPC spans and metrics) was still in progress and has slipped repeatedly, so downstream module stabilization has had no firm date attached to it.
- The OpenTelemetry Go/contrib maintainers have generally tracked this via a "stabilize otelgrpc" issue/milestone rather than a calendar date, and milestones there are typically untimed.

If your question comes from a particular source — a project plan, roadmap doc, or an internal tracker — the date is likely stated there rather than in anything I'd have memorized. I answered without consulting files or the web per your instructions, so if you want, point me at the document and I can pull the exact date from it.
