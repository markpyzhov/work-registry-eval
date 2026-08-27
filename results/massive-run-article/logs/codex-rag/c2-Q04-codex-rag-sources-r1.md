# What is the status of the otelgin MultipartForm temporary-file cleanup work tracked by `opentelemetry-go-contrib` issue `#5946` and pull request `#6609`?

<!-- RESPONSE_START -->

The cleanup work is **not completed or merged**.

- Issue [#5946 / SRC-ISSUE-01](https://github.com/open-telemetry/opentelemetry-go-contrib/issues/5946) is listed as **open**, though its timeline says it was marked **duplicate** on 2025-07-02. The underlying bug is that `otelgin` replaces the request context, so Go’s server cleanup does not see the `MultipartForm` that holds the upload temp files.
- PR [#6609 / SRC-PR-01](https://github.com/open-telemetry/opentelemetry-go-contrib/pull/6609) remains **open** (updated 2025-11-13), with +95/-0 changes across three files—so the fix has not landed.
- The working direction was `MultipartForm.RemoveAll()` in `otelgin`, with cleanup enabled by default and no configuration unless users later request it. Conflicts were resolved and the author reported package tests passing.
- It then returned to review over middleware-chain behavior: tests were expanded, a prototype alternative (#8161) was raised, and reviewers debated whether deletion after middleware returns is the intended behavior. The latest discussion did not record a final approval or merge decision.

In short: there is a tested, default-cleanup proposal, but it is still awaiting final agreement on behavior and merge.
