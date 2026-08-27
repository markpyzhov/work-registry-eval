# Which MultipartForm cleanup approach is being pursued for otelgin (`#5946` / `#6609`), and what is its current implementation status?

<!-- RESPONSE_START -->

The adopted fix is automatic `MultipartForm.RemoveAll()` in `otelgin`—not the reattach approach and not leaving cleanup to application users. The SIG favored default automatic deletion with no option initially; configurability would be added only if users later require it. [WS-05 Contrib](c2/work-states/WS-05-contrib.md), [SIG meeting note](c2/opentelemetry/meeting-notes/entry-3479584781.md)

Implementation is complete locally: conflicts were resolved and tests finished for PR #6609, so the work is treated as internally done. It has not yet been published: the final commits are unpushed, and issue #5946 and PR #6609 remain open and unmerged on GitHub. [WS-05 Contrib](c2/work-states/WS-05-contrib.md), [work-state correction](c2/work-states/comments/2026-03.md)
