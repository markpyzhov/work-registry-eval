# Which release confirmed immutable releases working for Go and Go Contrib, and what is the current status of the broader work in `sig-security#164`?

<!-- RESPONSE_START -->

**The release: `v1.39.0`.**

On 2025-12-11 (17:43:19Z), pellared (Robert Pająk) commented on `sig-security#164`: he confirmed immutable releases worked for OTel Go (`opentelemetry-go` tag `v1.39.0`) and Go Contrib (`opentelemetry-go-contrib` tag `v1.39.0`). Source: `opentelemetry/issues/sig-security-164.md` (`SRC-ISSUE-03`).

**Current status of `sig-security#164` (Work State WS-03, last updated 2026-03-11): deferred, not done.**

- Tracked as `WS-03: Security and Fuzzing` / task `T002`, owner pellared, status of the workstream `in_progress`, priority P1. `T002` is an unchecked task: immutable/signature-release enablement is deferred pending release-tooling and asset-upload confirmation.
- The GitHub issue itself remains **closed** (closed 2026-01-28T22:16:50Z by reyang, after being renamed 2026-01-07 from "Enable immutable releases where possible" to "Recommend immutable releases"), but per the Work State that closure is historical evidence, **not** delivery completion.
- Cause of the walk-back: comment `CMT-2026-03-003` (2026-03-11, pellared) — after a private follow-up with trask, the team walked back treating `sig-security#164` as done. Enablement for the Go repos is deferred until the release tooling and asset-upload order are confirmed safe. The GitHub issue was deliberately left closed / not reopened.
- **Blocker:** release-tooling and asset-upload ordering must be confirmed safe before enablement. This traces back to the caution raised in the issue itself — once a release is published, assets cannot be added/edited/removed, so any repo that uploads assets after publishing must have its release process checked first.
- **Next update needed:** release-tooling confirmation and any later signed-release evidence for `#164`.

Relevant chronology from the issue (`SRC-ISSUE-03`): opened 2025-08-27 by trask; pellared validated the feature on side projects (goyek v2.3.0, golang-templates/seed v0.22.0) in Sept 2025; feature went GA 2025-10-28; `opentelemetry-go#7567` merged to prepare OTel Go (2025-11-03); trask confirmed the terraform-provider-github gap need not block (2025-11-07); v1.39.0 confirmation 2025-12-11.

Dataset records cited: `opentelemetry/issues/sig-security-164.md` (`SRC-ISSUE-03`, path=sources), `work-states/WS-03-security-fuzzing.md` (path=work-state), `work-states/comments/2026-03.md` (`CMT-2026-03-003`, path=comments), `opentelemetry/meeting-notes/entry-3479655348.md` (`SRC-NOTE-06`, path=sources).
