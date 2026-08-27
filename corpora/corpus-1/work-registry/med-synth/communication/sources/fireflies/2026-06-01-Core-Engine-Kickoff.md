**Source ID**: SRC-MEET-01

# Fireflies Transcript: Core Engine Kickoff
**Date**: 2026-06-01
**Participants**: Alice (PM), Bob (Backend), Charlie (Engine), Diana (QA), Evan (DevOps)

## Summary
Kickoff for the core redaction engine. Charlie owns the first detect-and-mask pass on text-layer PDFs; Diana reviews the first commit. API and packaging stay out of scope for now.

## Transcript
**Alice**: We're kicking off the core redaction engine today. This is the foundation for the rest of the toolkit, so I want a clear owner and a first deliverable. Charlie, can you take the initial implementation?

**Charlie**: Yes. I'll start with a basic detect-and-mask path on text-layer PDFs. Nothing fancy yet — just enough to prove the engine can find spans and apply masks.

**Bob**: Do you need anything from the API side for this first pass?

**Charlie**: Not yet. Keep the API work separate until there's something stable to call into. If that changes I'll ping you.

**Diana**: Once there's a first commit, I'll pick up review. Don't wait on a full test suite for that initial push.

**Evan**: Same from packaging — no Docker or release concerns until the engine exists.

**Alice**: Sounds good. Charlie, go ahead and open the task on your side; Diana reviews when there's something to look at. We'll expand from there.

**Charlie**: Will do.
