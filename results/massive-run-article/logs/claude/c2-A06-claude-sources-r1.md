# Did the OTelConf RC support PR that the SIG agreed to merge actually ship in a release?

<!-- RESPONSE_START -->

## Answer: the dataset does not support a yes-or-no answer — it can't be confirmed that it shipped

**What the sources do establish**

The SIG decision itself is recorded in the meeting note for the OpenTelemetry Go SIG call of **2025-11-20** (published 2025-11-26 by pellared, [SRC-NOTE-07], `opentelemetry/meeting-notes/entry-3581463689.md`, https://github.com/open-telemetry/opentelemetry-go/issues/6648#issuecomment-3581463689):

- Discussion: "Next Go release & OTelConf RC support — Release blocked on RC support module; PR needs reviews. Requested changes from Alex do not need to be in the current PR. Module is `0.x`; breaking changes acceptable later."
- Decision: "**Merge OTelConf RC support PR as-is (pending normal review).**"
- Action item: "SIG reviewers: Review the OTelConf RC support PR." — still unchecked in the note.
- A companion decision tracked the experimental-API-structure review (`x` submodule) under the `1.40.0` milestone.

**Why shipment can't be confirmed**

1. **No source record exists for the PR itself.** The dataset's `pulls/` records are contrib #6609, contrib #8014, community #3000, and opentelemetry-go #7403, #7427, #7443, #7474. None is the OTelConf RC support PR, so there is no merge state or merge date for it.
2. **No contrib release notes are in the dataset.** The only release record is `opentelemetry/releases/release-v1.39.0.md` — tag `v1.39.0`, published **2025-12-08T16:45:46Z** — and that is the **opentelemetry-go core** repo. `otelconf` lives in **opentelemetry-go-contrib**, so this release would not carry it in any case. Searching that release document for otelconf / declarative configuration returns nothing relevant; its "Added" section lists observability metrics, OTLP insecure env vars (#7608), the `Processor.Enabled` method (#7639), and semconv v1.38.0 (#7648) — no config-module entry.
3. **The milestone records are counts only.** `opentelemetry-go-contrib` milestone v1.40.0 (`milestones/milestone-14282228.md`) is closed with 169 closed / 0 open, and opentelemetry-go v1.39.0 (`milestone-13145551.md`) closed with 335 closed / 0 open — neither enumerates items, so neither can be tied to this PR.

**Adjacent but not the same thing.** A related otelconf item, issue contrib **#8059** ("otelconf: add support for `OTEL_EXPERIMENTAL_CONFIG_FILE`", `issues/opentelemetry-go-contrib-8059.md`), is **closed (completed)**, last updated 2026-04-03, with contrib PR #8106 cross-referenced. That is the env-var/config-file feature discussed on the 2025-10-23 call, not the RC support module the SIG voted to merge on 2025-11-20 — so it should not be read as evidence the RC support PR shipped.

**Bottom line:** the sources confirm the SIG agreed on 2025-11-20 to merge the OTelConf RC support PR as-is, and that the next Go release was blocked on it, but they contain no record of the PR being merged and no contrib release notes in which its shipment could be verified.

Sources used: `opentelemetry/meeting-notes/entry-3581463689.md` [SRC-NOTE-07]; `opentelemetry/meeting-notes/entry-3479626706.md` [SRC-NOTE-05]; `opentelemetry/issues/opentelemetry-go-contrib-8059.md` [SRC-ISSUE-05]; `opentelemetry/releases/release-v1.39.0.md`; `opentelemetry/milestones/milestone-14282228.md` [SRC-MILE-04]; `opentelemetry/milestones/milestone-13145551.md` [SRC-MILE-02].
