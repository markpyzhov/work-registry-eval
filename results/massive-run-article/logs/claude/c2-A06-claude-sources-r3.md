# Did the OTelConf RC support PR that the SIG agreed to merge actually ship in a release?

<!-- RESPONSE_START -->

## Answer: the sources don't show it — the dataset can't confirm the OTelConf RC support PR shipped in any release.

**What the sources do establish**

- The decision exists. The OpenTelemetry Go SIG meeting of **2025-11-20** (written up 2025-11-26) recorded under "Decisions": *"Merge OTelConf RC support PR as-is (pending normal review)"*, with a matching action item *"SIG reviewers: Review the OTelConf RC support PR."* The same note says the **next Go release was blocked on the RC support module**, that the module is `0.x` (breaking changes acceptable later), and that experimental-API structure review (e.g. an `x` submodule) would be tracked under the `1.40.0` milestone, with Alex Boten to open the tracking issue.
  - Source: [SRC-NOTE-07] — `opentelemetry/meeting-notes/entry-3581463689.md` (https://github.com/open-telemetry/opentelemetry-go/issues/6648#issuecomment-3581463689)

**What is missing**

- The dataset contains **no record of the PR itself** — no pull-request document for the OTelConf/otelconf RC support change, so there is no merge state, merge date, or milestone for it.
- The only release record in the dataset is **opentelemetry-go v1.39.0** (tag published 2025-12-08, [SRC-REL-01] `opentelemetry/releases/release-v1.39.0.md`). That is the core `opentelemetry-go` repo; its changelog and "What's Changed" list contain **no otelconf entry**. The otelconf module lives in `opentelemetry-go-contrib`, and there is **no contrib release document** in the dataset at all.
- The related milestone records ([SRC-MILE-02] opentelemetry-go v1.39.0, [SRC-MILE-03] opentelemetry-go v1.40.0, [SRC-MILE-04] opentelemetry-go-contrib v1.40.0) are all closed with 0 open items, but they list no individual items, so they cannot tie the PR to a shipped version.

**Nearest adjacent evidence (does not answer the question)**

- A contrib release did happen in that window: pellared confirmed on 2025-12-11 that immutable releases worked for both `opentelemetry-go` **and** `opentelemetry-go-contrib` at tag **v1.39.0** ([SRC-ISSUE-03] `opentelemetry/issues/sig-security-164.md`). But nothing in the sources says the OTelConf RC support change was part of that contrib release.
- The adjacent otelconf work item, `OTEL_EXPERIMENTAL_CONFIG_FILE` support (contrib issue #8059, [SRC-ISSUE-05]), is marked **closed (completed)**, last updated 2026-04-03, with PR #8106 cross-referenced. This is a *different* item from the RC support PR, its milestone is "untracked", and no release is named — so it does not establish shipment either.

**Bottom line:** the SIG did agree on 2025-11-20 to merge the OTelConf RC support PR as-is pending normal review, but the assigned dataset contains neither the PR record nor any contrib release notes, so whether it actually shipped in a release cannot be determined from these sources.
