# What is the status of the otelgin MultipartForm temporary-file cleanup work tracked by `opentelemetry-go-contrib` issue `#5946` and pull request `#6609`?

<!-- RESPONSE_START -->

The cleanup is **not merged or complete**.

- Issue [#5946](https://github.com/open-telemetry/opentelemetry-go-contrib/issues/5946) is displayed as **open**, but was marked **duplicate** on 2025-07-02. It tracks the request-cloning behavior that prevents the original HTTP request from owning the parsed `MultipartForm` cleanup. [SRC-ISSUE-01]
- PR [#6609](https://github.com/open-telemetry/opentelemetry-go-contrib/pull/6609) remains **open** (updated 2025-11-13). It proposes calling `MultipartForm.RemoveAll()` and includes expanded tests for upstream/downstream middleware behavior. [SRC-PR-01]
- Review discussion has not fully converged: reviewers agree cleanup is needed, but the unresolved concern is that `RemoveAll()` makes the uploaded temporary file unavailable to outer middleware during unwinding. A prototype alternative was discussed, but reviewers questioned whether it fixes the underlying lifecycle issue. [SRC-PR-01]
- The Go SIG characterized this as a broader HTTP-middleware/request-cloning problem, not exclusively Gin; no upstream Go solution was available in the discussion. [SRC-NOTE-04]

So: **a tested workaround exists in #6609, but it is still awaiting resolution/merge; #5946 itself has been superseded administratively as a duplicate.**
