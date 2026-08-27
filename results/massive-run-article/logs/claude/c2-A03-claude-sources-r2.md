# Which release confirmed immutable releases working for Go and Go Contrib, and what is the current status of the broader work in `sig-security#164`?

<!-- RESPONSE_START -->

## Answer

**Release that confirmed it: v1.39.0** — both `opentelemetry-go` and `opentelemetry-go-contrib`.

On 2025-12-11T17:43:19Z, pellared (Robert Pająk) commented in the issue: "I can confirm that it worked for Go (.../opentelemetry-go/releases/tag/v1.39.0) and Go Contrib (.../opentelemetry-go-contrib/releases/tag/v1.39.0)."

Lead-up in the same issue:
- 2025-11-03: pellared opened opentelemetry-go PR #7567 to prepare OTel Go for immutable releases; edited later to note it merged and that both Go and Go Contrib were ready to enable the feature.
- pellared flagged a possible dependency on `integrations/terraform-provider-github#2746` and asked trask whether it was a blocker; trask replied on 2025-11-07 that it need not block, pointing at open-telemetry/admin PR #346 as the pattern to follow.

**Status of sig-security#164: closed (completed).**

- Title: "Recommend immutable releases" (renamed by trask on 2026-01-07 from "Enable immutable releases where possible").
- Issue created 2025-08-27 by trask; last updated 2026-01-28T22:16:50Z; **closed by reyang on 2026-01-28T22:16:50Z**.
- The closing work was sig-security PR #219 (cross-referenced by pellared on 2026-01-28T11:30:57Z). The scope pellared proposed, after GitHub immutable releases went GA on 2025-10-28, was to add GitHub Immutable Releases to `sig-security/docs/recommendations.md`; he asked to be assigned on 2026-01-07.
- Other repos tracked against the issue via cross-references: opentelemetry-dotnet (PR #6646, issue #6748), opentelemetry-go (issue #6648, PR #7567), and opentelemetry-ebpf-instrumentation (issue #13).
- Related open question resolved along the way: trask asked whether the "Release attestation (json)" asset replaces per-artifact attestation (sig-security#79); pellared said he thinks it can.

Caveats recorded in the issue that shaped adoption: once a release is published, assets cannot be added/edited/removed, so each repo's release process must be checked before enabling; and `gh release verify` cannot verify the auto-generated source zip/tarball, since those are created only on download.

## Sources

All from the assigned dataset, `path: sources`:
- `opentelemetry/issues/sig-security-164.md` — [SRC-ISSUE-03], "Recommend immutable releases" (open-telemetry/sig-security#164). Primary source for both the v1.39.0 confirmation and the closed/completed status.
- `opentelemetry/meeting-notes/entry-3479655348.md` — [SRC-NOTE-06], OTel Go SIG notes (meeting 2025-10-30). Corroborates the decision to proceed and the action item on Robert referencing sig-security #164.

Note: the dataset contains no record for sig-security PR #219 itself, so its merge state is known only indirectly from the issue's timeline. `opentelemetry/releases/release-v1.39.0.md` exists in the dataset but the retrieved chunks cover dependency changelog entries, not immutability metadata.
