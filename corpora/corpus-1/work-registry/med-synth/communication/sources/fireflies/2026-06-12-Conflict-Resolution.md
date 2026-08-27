**Source ID**: SRC-MEET-04

# Fireflies Transcript: Conflict Resolution
**Date**: 2026-06-12
**Participants**: Alice (PM), Bob (Backend), Charlie (Engine), Diana (QA)

## Summary
Diana flagged overlapping detections before mask generation. The team agreed on a union-based merge rule; Charlie will implement and cover gap tests.

## Transcript
**Diana**: Before we generate more masks — overlapping detections are going to collide. We need a merge rule. Charlie, what's the approach?

**Charlie**: Union merge. If two detections overlap, combine them into one redaction block instead of trying to rank which pattern wins.

**Diana**: That matches what I want for review — one contiguous mask is easier to reason about than competing priorities. We'll still need tests that the merge doesn't swallow clean text between distant hits.

**Charlie**: Agreed — I'll add those cases. The merge has to be careful about gaps.

**Bob**: Fine by me as long as the API and CLI both apply the same rule.

**Alice**: Same rule on both paths is the requirement — don't fork behavior for CLI vs API.

**Charlie**: They will. I'll implement the union merge in the engine, keep behavior identical on both paths, and ping Diana when the gap tests are in.
