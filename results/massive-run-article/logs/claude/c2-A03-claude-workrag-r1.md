# Which release confirmed immutable releases working for Go and Go Contrib, and what is the current status of the broader work in `sig-security#164`?

<!-- RESPONSE_START -->

## The release: v1.39.0

On 2025-12-11, pellared (Robert Pająk) commented in `sig-security#164`: he confirmed immutable releases worked for **OTel Go v1.39.0** and **OTel Go Contrib v1.39.0** (`https://github.com/open-telemetry/opentelemetry-go/releases/tag/v1.39.0` and `.../opentelemetry-go-contrib/releases/tag/v1.39.0`).

Preparation context from the same issue: PR `opentelemetry-go#7567` was merged (2025-11-03) to ready OTel Go for enabling immutable releases; trask noted the terraform-provider-github issue need not block, pointing to `open-telemetry/admin#346`.

## Current status of the broader work: deferred, not done

The authoritative Work State is `WS-03: Security and Fuzzing` (status `in_progress`, P1, owner pellared, last updated 2026-03-11). Task `T002`, mapped to `sig-security#164`:

- **Immutable/signature-release enablement is deferred, not done**, pending confirmation that the release tooling and asset-upload ordering are safe.
- The GitHub issue is **closed (completed)** as of 2026-01-28 (title renamed 2026-01-07 from "Enable immutable releases where possible" to "Recommend immutable releases"), but **closure is explicitly not delivery completion**. The closure is recorded as historical evidence only.
- The walk-back came from `CMT-2026-03-003` (pellared, effective 2026-03-11): after a private follow-up with trask, treating `#164` as done was reversed; the GitHub issue was deliberately left closed and not reopened.
- **Blocker**: release-tooling and asset-upload ordering must be confirmed safe before enablement. This traces to the underlying caution in the issue — assets cannot be added, edited, or removed after an immutable release is published, so any repo that uploads assets post-publish must have its release process checked first.
- **Next update needed**: release-tooling confirmation and any later signed-release evidence for `#164`.

The Work State Index likewise lists immutable/signature-release enablement under "Blocked / deferred."

Note the scope distinction: the v1.39.0 confirmation is evidence that the mechanism worked on those two repos; the broader `#164` work (org-wide recommendation plus enablement for the Go repos) remains deferred.

## Dataset records cited

- `opentelemetry/issues/sig-security-164.md` (`SRC-ISSUE-03`, path `sources`) — v1.39.0 confirmation, PR #7567, issue state/rename/timeline, asset-immutability caution
- `work-states/WS-03-security-fuzzing.md` (path `work-state`) — Task List, Active Work, Blockers, Decisions, Done/Evidence, Next Update Needed
- `work-states/comments/2026-03.md` (`CMT-2026-03-003`, path `comments`) — the deferral correction
- `opentelemetry/meeting-notes/entry-3479655348.md` (`SRC-NOTE-06`, path `sources`) — action item assigning Robert to enable GitHub signature releases, update releasing docs, and ensure artifacts are uploaded at release time
- `work-states/index.md` (path `work-state-index`, navigation only) — corroborates WS-03 `in_progress` and the deferred classification
