# What is the status of the otelgin MultipartForm temporary-file cleanup work tracked by `opentelemetry-go-contrib` issue `#5946` and pull request `#6609`?

<!-- RESPONSE_START -->

The work is **not merged or complete** in the dataset.

- PR [#6609](https://github.com/open-telemetry/opentelemetry-go-contrib/pull/6609) remains **open** (last updated 2025-11-13), with a +95/−0 proposed `otelgin` change and tests. It implements cleanup via `MultipartForm.RemoveAll()` after middleware processing. [SRC-PR-01](https://github.com/open-telemetry/opentelemetry-go-contrib/pull/6609)
- The key unresolved concern is compatibility: cleanup deletes the temporary files before an outer/upstream middleware returning later can read them. The PR gained tests demonstrating that behavior, but reviewers were still seeking agreement that it is the intended contract. A reattach-the-form alternative and prototype PR #8161 were raised; maintainers questioned whether that alternative fixes the underlying cloned-request cleanup problem. [SRC-PR-01](https://github.com/open-telemetry/opentelemetry-go-contrib/pull/6609)
- The Go SIG had recommended that middleware clean up temporary resources, and the discussion favored keeping this PR narrowly scoped to `otelgin`; similar risks may exist in other HTTP middleware. [SRC-PR-01](https://github.com/open-telemetry/opentelemetry-go-contrib/pull/6609), [SRC-NOTE-04](https://github.com/open-telemetry/opentelemetry-go/issues/6648#issuecomment-3479584781)
- Issue [#5946](https://github.com/open-telemetry/opentelemetry-go-contrib/issues/5946) is recorded as **open** in the dataset, though its timeline also says it was marked as a duplicate on 2025-07-02. It remains cross-referenced to #6609. [SRC-ISSUE-01](https://github.com/open-telemetry/opentelemetry-go-contrib/issues/5946)

So: there is an implemented, actively reviewed cleanup patch, but it is stalled pending final agreement on the `RemoveAll` behavior and has not landed.
