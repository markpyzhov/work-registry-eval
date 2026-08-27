# What did the Go SIG decide about the OTelConf RC support PR that was blocking the next release?

<!-- RESPONSE_START -->

## Answer

At the **OpenTelemetry Go SIG meeting of 2025-11-20** (notes posted 2025-11-26 by pellared), the SIG decided to **merge the OTelConf RC support PR as-is, pending only normal review** — i.e., not to hold it for the additional changes that had been requested.

### The decision

- **Merge the OTelConf RC support PR as-is** (subject to ordinary review approvals).
- **Track the experimental API structure review separately** (e.g., a possible `x` submodule) under the **`1.40.0` milestone**, rather than blocking the current PR on it.

### Reasoning recorded in the discussion ("Next Go release & OTelConf RC support")

- The next Go release was **blocked on the RC support module**; the PR just needed reviews.
- **Requested changes from Alex Boten do not need to be in the current PR.**
- The module is **`0.x`**, so **breaking changes are acceptable later** — which is what made merging as-is safe.
- Caveat agreed on: **avoid exposing public API that is already known to be removed immediately.**
- On experimental features: a `WithExperimentalFeatures`-style flag was judged **likely unhelpful**; a dedicated **`x` submodule to isolate experimental APIs** was seen as the better option, aligning with the OTel-wide push toward opt-in experimental features.

### Resulting action items

- **Alex Boten** — open an issue to track evaluation of the experimental API structure for the OTelConf RC module, and add it to the **`1.40` milestone**.
- **SIG reviewers** — review the OTelConf RC support PR (the remaining gate to unblocking the release).

### Attendees at that meeting

Tyler Yahn, Owen Williams, Sam Xie, Alex Boten, David Ashpole, Bryan Boreham (Robert Pająk mentioned).

### Sources cited

- **[SRC-NOTE-07]** — Meeting Note: OpenTelemetry Go SIG, meeting date 2025-11-20, posted 2025-11-26 by pellared. `https://github.com/open-telemetry/opentelemetry-go/issues/6648#issuecomment-3581463689` (dataset document: `opentelemetry/meeting-notes/entry-3581463689.md`) — carries the Discussions, Decisions, and Action Items quoted above.

Supporting background (earlier context on how otelconf RC/config-file work got here, not the decision itself):

- **[SRC-NOTE-05]** — Go SIG note for 2025-10-23, `https://github.com/open-telemetry/opentelemetry-go/issues/6648#issuecomment-3479626706` (`opentelemetry/meeting-notes/entry-3479626706.md`) — contrib-first `otelconf` approach preferred over SDK-level support in the short term.
- **[SRC-ISSUE-05]** — `otelconf: add support for OTEL_EXPERIMENTAL_CONFIG_FILE variable`, open-telemetry/opentelemetry-go-contrib#8059 (`opentelemetry/issues/opentelemetry-go-contrib-8059.md`) — the related config-file feature issue, since closed as completed.
