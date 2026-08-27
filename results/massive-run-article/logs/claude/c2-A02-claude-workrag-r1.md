# On what date will otelgrpc module stabilization be complete?

<!-- RESPONSE_START -->

## Answer

**There is no completion date.** The dataset does not contain a target, scheduled, or actual completion date for otelgrpc module stabilization — and the records affirmatively state that the timing is unresolved.

### What the records say

**Work State (authoritative, `work-states/WS-05-contrib.md`, WS-05: Contrib Modules, Last Updated 2026-03-08, status `in_progress`):**
- Task `T005` — "Longer-term `otelgrpc` stabilization (depends on RPC semconv + gRPC engagement)" — is **unchecked / not done**.
- Blockers section: "Depends on RPC semantic-convention stabilization and active gRPC-team engagement (described as sporadic); **not expected within 2025**."
- Done/Evidence section: "**`T005`: Stabilization timing remains unresolved.**"
- "Next Update Needed" still lists "otelgrpc stabilization progress" as an open item.

**Work State Index (`work-states/index.md`, source cutoff 2026-02-27, final state through 2026-03-11):**
- `otelgrpc` stabilization is listed under **"Blocked / deferred"** (RPC semconv + gRPC engagement).
- The coverage table records `opentelemetry-go-contrib#8078` as "restoration not planned; **stabilization timing unresolved**."

### Provenance for why no date exists

**`SRC-NOTE-06`** — OpenTelemetry Go SIG meeting note dated 2025-10-30 (`opentelemetry/meeting-notes/entry-3479655348.md`, posted 2025-11-03 by pellared):
- Blockers: RPC semantic conventions (semconv) must stabilize first; an audit of the current otelgrpc API is needed.
- David (dashpole) is willing to drive module stability **once semconv stabilizes**; gRPC-team engagement has been sporadic and driven by their internal roadmap.
- Explicit conclusion: **"Not likely to stabilize this year; set a goal to finalize a strategy next year once semconv progress is clearer."** — i.e., the SIG committed only to settling a *strategy*, not a completion date.
- Action item for David: "Monitor semconv RPC stabilization efforts; once stable, drive otelgrpc module stabilization" — a dependency-gated trigger, no date.

**`SRC-ISSUE-06`** — `opentelemetry-go-contrib#8078` (restore deprecated `UnaryClientInterceptor`), closed as **not planned** on 2025-10-31. Damien clarified that stabilizing otelgrpc does not imply restoring the removed interceptor. This closure is a separate task (`T004`, done) and is not otelgrpc stabilization itself.

**Comments (`work-states/comments/2026-03.md`):** the three post-cutoff human corrections (CMT-2026-03-001 through -003) cover WS-03/T001, WS-05/T001, and WS-03/T002. **None touches T005**, so nothing supersedes the "timing unresolved" position.

### Bottom line

Stabilization is blocked on two external prerequisites — RPC semconv stabilization and active gRPC-team involvement — neither of which has an established date in the dataset. As of the latest Work State (2026-03-08, final state through 2026-03-11), the work remains open with no completion date set.
