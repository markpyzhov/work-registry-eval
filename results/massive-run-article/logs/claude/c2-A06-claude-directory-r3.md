# Did the OTelConf RC support PR that the SIG agreed to merge actually ship in a release?

<!-- RESPONSE_START -->

## Answer: No — the package does not establish that it shipped

The evidence records the SIG's decision to merge, but contains no PR record and no release containing it.

**The decision (2025-11-20 SIG call)**
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3581463689.md` (`SRC-NOTE-07`, posted by pellared 2025-11-26): the next Go release was "blocked on RC support module; PR needs reviews." Decision recorded: "Merge OTelConf RC support PR as-is (pending normal review)." Also decided to track the experimental API structure question (e.g. an `x` submodule) under the `1.40.0` milestone. Action items: **Alex Boten** to open a tracking issue for experimental API structure and add it to `1.40`; **SIG reviewers** to review the RC support PR. Alex's requested changes were explicitly deemed not required in that PR.

**Current state (authoritative)**
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-04-release-process.md` — `T001` (OTelConf RC / experimental API) is still **unchecked / in_progress**. Active Work states plainly: "Sources do not include that issue or the RC PR itself." Blockers: "Final merge/delivery of that PR is not in the package." **Done / Evidence: "None established in the frozen Sources (no RC PR, no follow-up issue/PR bodies)."** Next Update Needed: "Presence of the OTelConf RC PR outcome, Alex's tracking issue…"
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/index.md` — item coverage row: "OTelConf RC / experimental API (SIG topic) | Release Process | **decision recorded; delivery not in Sources**", and it is listed under "Active / open".

**Release check**
- The only release Source in the package is `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/releases/release-v1.39.0.md` (`v1.39.0`, published 2025-12-08). Its changelog contains **no otelconf or RC-support entry**. There is no `v1.40.0` release Source, even though the `v1.40.0` milestones exist and are closed (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/milestones/milestone-13661613.md`, `.../milestone-14282228.md`) — closed milestones alone don't establish that this PR shipped.
- No `CMT-*` correction touches WS-04; the three comments in `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/comments/2026-03.md` cover WS-03 and WS-05 only.

**Don't confuse it with the adjacent otelconf item**: `opentelemetry-go-contrib#8059` (`OTEL_EXPERIMENTAL_CONFIG_FILE` support via otelconf) is a *different* thread — issue closed 2025-12-04 by MrAlias, cross-referenced to PR `#8106`, whose merge is likewise not in Sources (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/issues/opentelemetry-go-contrib-8059.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-05-contrib.md`).

Bottom line: as of the final Work State (2026-03-11, source cutoff 2026-02-27), the merge was agreed but neither the PR's merge nor its inclusion in any release is supported by the available evidence. Answering "yes, it shipped" would require sources this package doesn't contain.
