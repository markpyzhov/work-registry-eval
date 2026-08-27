**Source ID**: SRC-MEET-08

# Fireflies Transcript: Windows & License Sync
**Date**: 2026-08-15
**Participants**: Alice (PM), Charlie (Engine), Diana (QA), Evan (DevOps)

## Summary
Charlie opened on the AGPL PDF-parser problem and the search for an Apache/MIT alternative. Evan noted the earlier Windows path fix; code-signing cert procurement remains open.

## Transcript
**Charlie**: Licensing first — the replacement PDF parser Evan swapped in turned out to be AGPL. I've started searching for an Apache or MIT alternative. Need to confirm feature coverage before we swap again.

**Diana**: Right — AGPL isn't acceptable for how we're distributing the toolkit.

**Charlie**: Unknown how much rework another swap costs until I compare candidates. That's this week's task. I'd rather not guess.

**Evan**: Separate note while we're all here — the Windows backslash path handling fix from earlier this month has been holding up fine in the build. No regressions there.

**Alice**: Good to hear. And signing?

**Evan**: Still waiting on the code-signing certificate to come through procurement. No firm timeline yet, so I can't say when that's cleared.

**Alice**: Okay — Charlie, keep pushing on the parser alternative, that's the priority. Evan, keep chasing procurement on the cert, but no need for a deep-dive there today.
