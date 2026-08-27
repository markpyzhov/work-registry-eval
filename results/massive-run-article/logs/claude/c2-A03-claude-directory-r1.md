# Which release confirmed immutable releases working for Go and Go Contrib, and what is the current status of the broader work in `sig-security#164`?

<!-- RESPONSE_START -->

## Answer

**Release that confirmed it: `v1.39.0`** — for both `opentelemetry-go` and `opentelemetry-go-contrib`.

On 2025-12-11, pellared (Robert Pająk) commented on the issue: "I can confirm that it worked for Go (…/opentelemetry-go/releases/tag/v1.39.0) and Go Contrib (…/opentelemetry-go-contrib/releases/tag/v1.39.0)." In the same comment he noted the GitHub feature had gone GA (2025-10-28) and proposed adding GitHub Immutable Releases to the sig-security `docs/recommendations.md`.
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/issues/sig-security-164.md`
- The Go `v1.39.0` release itself (published 2025-12-08) is recorded at `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/releases/release-v1.39.0.md`.

**Current status of the broader `sig-security#164` work: deferred, not done** (tracked as `WS-03 / T002`, status `in_progress`, owner pellared, last updated 2026-03-11).

- Enabling immutable / signature releases for the Go repos is **deferred pending confirmation that release tooling and asset-upload ordering are safe** — the concern being that immutability blocks adding/editing release assets after publication, so any repo that uploads assets post-publish must be checked first.
- The GitHub issue was **closed 2026-01-28 by reyang** (and renamed by trask on 2026-01-07 from "Enable immutable releases where possible" to "Recommend immutable releases"), but that closure is explicitly **not** treated as delivery completion. A private follow-up between pellared and trask walked the "done" status back; the GitHub issue was deliberately left closed and not reopened.
- Next update needed: release-tooling confirmation and any later signed-release evidence for `#164`.
- Files: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-03-security-fuzzing.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/comments/2026-03.md` (`CMT-2026-03-003`, effective 2026-03-11), `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/index.md`

**Background / how it got there** (from `sig-security-164.md` and `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3479655348.md`):
- Opened 2025-08-27 by trask off the GitHub public-preview changelog; pellared validated the feature on side projects (goyek, golang-templates/seed) in Sept 2025, flagging the "assets cannot be changed after publish" caveat.
- `opentelemetry-go#7567` was merged (2025-11-03) to prepare OTel Go, after which pellared declared both Go and Go Contrib ready to enable.
- The SIG meeting recorded a decision to proceed with signature releases (in addition to existing tag signing and GPG-signed source archives), with the action item to update the releasing docs and ensure artifacts are uploaded at release time — which is the same tooling/ordering concern that later became the blocker.

Note one nuance worth flagging: the `v1.39.0` confirmation is evidence the immutability feature *worked* on those releases, but per the current Work State it does not establish that immutable/signature-release enablement is complete as a deliverable.
