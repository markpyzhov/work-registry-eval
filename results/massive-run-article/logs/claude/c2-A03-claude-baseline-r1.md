# Which release confirmed immutable releases working for Go and Go Contrib, and what is the current status of the broader work in `sig-security#164`?

<!-- RESPONSE_START -->

I can't answer this one reliably from parametric knowledge — I'd be guessing, and a wrong release number here would be worse than no answer.

What I can and can't say:

**Not recalled with confidence:**
- The specific release tag that first confirmed immutable releases working for OpenTelemetry Go and Go Contrib. I don't have a dependable memory of which version (e.g. a particular `v1.3x.0` / `v0.6x.0` pair) was the one where it was verified working.
- The current open/closed status, checklist state, or remaining blockers of `sig-security#164`. I don't have issue-level recall for that repo's tracker at that number.

**General context I do hold (may be useful framing, not an answer):**
- "Immutable releases" here almost certainly refers to GitHub's immutable-releases feature, which prevents release tags and their attached assets from being altered after publication. It moved through public preview during 2025 and became something OSS orgs began enabling repo-by-repo.
- `open-telemetry/sig-security` is OpenTelemetry's Security SIG repo, and it does host cross-repo supply-chain hardening tracking issues — enabling immutable releases across all OTel repos is exactly the shape of work that lands there, typically as an umbrella issue with a per-repo checklist. Go and Go Contrib being confirmed first is consistent with those being among the most actively released OTel repos.
- The reason Go/Go Contrib is a meaningful "confirmation" is that both use tag-driven multi-module release automation, so they exercise the feature's interaction with release tooling more than a single-module repo would.

**Suggested way to get the real answer** (all outside what I was allowed to use here): the issue body of `open-telemetry/sig-security#164` should carry the umbrella checklist and current status, and the confirming release would be identifiable from the first `open-telemetry/opentelemetry-go` release published after immutability was enabled on that repo — visible in the release's GitHub metadata.

I'd rather flag the gap than hand you a plausible-looking version number.
