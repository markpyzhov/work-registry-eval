# Has the SDK log `Record` mutation fix in `opentelemetry-go` pull request `#7403` been released?

<!-- RESPONSE_START -->

I can't confirm this one from memory.

I don't have reliable recall of `open-telemetry/opentelemetry-go` PR **#7403** specifically — neither its exact contents nor which tag it shipped in. PR numbers in that range would put it somewhere in the late-2025 window, which is close enough to my cutoff that I'd be guessing at both the merge date and the subsequent release, and guessing a version number here would be worse than useless to you.

What I can say with reasonable confidence, as general background rather than an answer:

- The class of bug you're describing is real and recurring in `sdk/log`. `log.Record` is passed to `Processor.OnEmit` by pointer, and the SDK reuses/copies records across the processor chain. There have been several fixes over time around processors mutating a record that the caller or a downstream processor still observes — particularly with attribute slices sharing backing arrays after `AddAttributes`, and with `BatchProcessor` retaining a record whose contents were later modified. If #7403 is in that family, it would be a `sdk/log` change.
- `sdk/log` was still on a `v0.x` line at my cutoff (unstable, versioned separately from the `v1.x` trace/metric modules), released in lockstep with the stable modules on roughly a monthly cadence. So a fix merged in that window would typically appear in the very next monthly release, not be held back.

To actually resolve it, the fastest checks are:

- `CHANGELOG.md` at the repo root — entries link their PR numbers, so searching the file for `7403` gives you the release heading it falls under directly.
- `git log --oneline --grep '#7403'` then `git tag --contains <sha>` on a local clone, which is authoritative and takes a few seconds.
- The PR page itself on GitHub shows the merge commit and the tags containing it.

If you paste the PR title or the changelog entry, I can tell you whether it matches a mutation bug I recognize and what the behavioral impact was — but I won't assert a release version for #7403 without you or a lookup confirming it.
