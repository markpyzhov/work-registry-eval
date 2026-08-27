**Source ID**: SRC-SLACK-07

# Slack Thread: Blocked on Upstream PDF Library
**Channel**: #cipherdoc
**Thread opened**: 2026-06-26
**Last activity**: 2026-09-10

---

**[2026-06-26 09:10] Charlie**: Bad news on the offset mismatch fix. It's definitely coming from `pdfminer.six`. There's an open issue on their repo for the whitespace handling we're hitting.

**[2026-06-26 09:57] Alice**: Any workaround? We can't stay blocked on this forever.

**[2026-06-26 09:58] Charlie**: Leaving it blocked for now. Local patches aren't getting us a clean fix — it's too deep in the parser.

**[2026-08-05 14:18] Charlie**: Still watching upstream — there's a PR against pdfminer.six, #992, that should cover the whitespace fix, but it hasn't merged. No movement from the maintainers.

**[2026-08-20 15:58] Charlie**: Spent some time this week evaluating whether we fork pdfminer.six ourselves to get the fix in sooner.

**[2026-08-20 16:01] Alice**: What's the team's read on that?

**[2026-08-20 17:55] Charlie**: We're passing on it. Maintaining a PDF parsing fork long-term is more risk than the wait. Staying blocked on #992.

**[2026-09-10 10:24] Charlie**: Checked again — #992 is still unmerged. No safe local path that doesn't involve owning a fork, so we're leaving the offset fix blocked pending the upstream merge.

**[2026-09-10 10:41] Alice**: This is becoming a real risk for the v1.0 timeline.

**[2026-09-10 10:55] Charlie**: Agreed, but I'd rather eat the delay than take on a parser fork we can't maintain.
