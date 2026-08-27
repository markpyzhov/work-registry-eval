# Did the OTelConf RC support PR that the SIG agreed to merge actually ship in a release?

<!-- RESPONSE_START -->

No — the package does not show it shipping, and the evidence stops well short of a release.

**What was agreed**

At the 2025-11-20 Go SIG call (notes posted 2025-11-26), the decision was recorded: "Merge OTelConf RC support PR as-is (pending normal review)," with experimental API structure (e.g., an `x` submodule) tracked under the `1.40.0` milestone. Action items assigned Alex Boten to open a tracking issue and SIG reviewers to review the RC support PR. The release itself was described as blocked on that RC support module pending reviews.
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3581463689.md` (`SRC-NOTE-07`)

**What the Work State says (authoritative)**

`WS-04-release-process` still lists `T001` (OTelConf RC / experimental API) as **unchecked / in_progress**, with "Done / Evidence: None established in the frozen Sources (no RC PR, no follow-up issue/PR bodies)." It explicitly notes the Sources do not include Alex's tracking issue or the RC PR itself, and that "Final merge/delivery of that PR is not in the package." Next update needed: "Presence of the OTelConf RC PR outcome."
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-04-release-process.md`

The index concurs: "OTelConf RC / experimental API (SIG topic) | Release Process | **decision recorded; delivery not in Sources**," and lists it under active/open items.
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/index.md`

**Corroborating checks**

- The only release source in the package, opentelemetry-go `v1.39.0` (published 2025-12-08), contains no otelconf/RC-support entry.  `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/releases/release-v1.39.0.md`
- The `v1.40.0` milestones (go and contrib) are closed with no description or item detail that would establish the RC PR landing.  `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/milestones/milestone-13661613.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/milestones/milestone-14282228.md`
- No `CMT-*` correction touches WS-04; the three post-cutoff comments cover WS-03/T001, WS-05/T001, and WS-03/T002 only.  `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/comments/2026-03.md`

**One disambiguation worth flagging**

There is a *separate* otelconf item that is easy to conflate: `opentelemetry-go-contrib#8059` (`OTEL_EXPERIMENTAL_CONFIG_FILE` support via contrib `otelconf`, `WS-05`/`T003`). That issue was closed 2025-12-04 by MrAlias after cross-reference to PR `#8106`, but that PR's merge and any release containing it are likewise not in the Sources. That is not the OTelConf RC support PR from the 2025-11-20 release discussion.
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-05-contrib.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/issues/opentelemetry-go-contrib-8059.md`

**Bottom line:** the merge decision is documented, but the package contains neither the RC PR record, a merge event, nor a release note carrying it. Whether it shipped cannot be answered from this evidence — as of the final Work State (through 2026-03-11) it remains tracked as open.
