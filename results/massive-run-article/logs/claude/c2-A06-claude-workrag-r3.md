# Did the OTelConf RC support PR that the SIG agreed to merge actually ship in a release?

<!-- RESPONSE_START -->

**No — the dataset does not establish that it shipped.**

## What the SIG decided
At the OpenTelemetry Go SIG meeting of **2025-11-20** (recorded in note `SRC-NOTE-07`, `opentelemetry/meeting-notes/entry-3581463689.md`), the release was blocked on the OTelConf RC support module, and the SIG decided to:
- **Merge the OTelConf RC support PR as-is**, pending normal review
- Track the experimental API structure review (e.g. an `x` submodule to isolate experimental APIs) under the **`1.40.0`** milestone

Action items: Alex Boten to open a tracking issue for the experimental API structure and add it to the `1.40` milestone; SIG reviewers to review the RC support PR.

## Current state (authoritative Work State)
`work-states/WS-04-release-process.md` — **WS-04: Release Process**, status `in_progress`, last updated 2025-11-27:
- `T001` (OTelConf RC / experimental API) is **still unchecked**.
- Active Work: "Sources do not include that issue or the RC PR itself."
- Blockers: "As of 2025-11-20, the release was described as blocked on RC support module review. **Final merge/delivery of that PR is not in the package.**"
- Done / Evidence: "**None established in the frozen Sources** (no RC PR, no follow-up issue/PR bodies)."
- Next Update Needed: "Presence of the OTelConf RC PR outcome, Alex's tracking issue..."

The Work State Index (`work-states/index.md`) confirms: *OTelConf RC / experimental API (SIG topic) → Release Process → "decision recorded; delivery not in Sources."*

## Cross-check against release records
The only release document in the dataset is `opentelemetry/releases/release-v1.39.0.md`, and nothing in its changelog or PR list corresponds to an OTelConf RC support module. The `1.40.0` milestone the SIG pointed at has no corresponding release document in the dataset.

## One thing not to confuse it with
A separate, adjacent item exists in **WS-05: Contrib Modules** (`work-states/WS-05-contrib.md`), `T003` / contrib issue `#8059` — adding `OTEL_EXPERIMENTAL_CONFIG_FILE` support via contrib `otelconf`. That issue was **closed 2025-12-04**, but even there the linked implementation PR `#8106` "appears only as a cross-reference; merge/release not established in Sources." This is the contrib env-var config-file work, not the OTelConf RC support PR from WS-04.

## Bottom line
The merge decision is well documented, but the dataset contains **no merge event and no release record** for the OTelConf RC support PR. Answering "did it ship" would require evidence outside this frozen source package — specifically the RC PR itself and any release after `v1.39.0`.
