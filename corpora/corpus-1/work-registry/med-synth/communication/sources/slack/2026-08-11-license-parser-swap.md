**Source ID**: SRC-SLACK-41

# Slack Thread: License Parser Swap
**Channel**: #cipherdoc
**Thread opened**: 2026-08-11
**Last activity**: 2026-08-15

---

**[2026-08-11 10:16] Evan**: Finished the parser swap the audit flagged — pulled out the problem library and dropped in a replacement. Calling that step done.

**[2026-08-11 10:18] Diana**: Nice turnaround. I'll fold it into the re-scan.

**[2026-08-11 10:21] Charlie**: Did you check the new one's license closely, or just take the package listing at face value?

**[2026-08-11 10:22] Evan**: Fair question — I should have looked harder before wiring it in.

**[2026-08-15 09:54] Charlie**: Following up on this — since the replacement turned out to be AGPL, I'm searching for an Apache or MIT alternative that can do the same parsing.

**[2026-08-15 09:56] Diana**: Any candidates yet?

**[2026-08-15 09:58] Charlie**: A couple, but neither one covers everything the old library did. Still unresolved as of today — going to keep looking rather than force a bad fit.

**[2026-08-15 10:22] Alice**: Let me know as soon as one of those candidates looks viable — don't want this dragging past the rest of the release work.
