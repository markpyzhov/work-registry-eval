**Source ID**: SRC-MEET-02

# Fireflies Transcript: Config Format Sync
**Date**: 2026-06-18
**Participants**: Alice (PM), Bob (Backend), Charlie (Engine), Diana (QA), Evan (DevOps)

## Summary
Decision: JSON for redaction policy config. Charlie implements the loader against that; YAML left as a possible later revisit.

## Transcript
**Alice**: We need to lock the redaction policy configuration format. Charlie, what's your recommendation?

**Charlie**: I'd rather we pick one format and stick to it for the loader. JSON is straightforward to parse and validate. YAML is nicer to edit by hand, but we can revisit that later if we need it.

**Bob**: I'm fine with JSON for the engine. The API can speak the same shape without translation.

**Diana**: From a QA angle, one format with clear structure beats two formats that drift apart. JSON works.

**Charlie**: Then I'll implement the loader against JSON. If we change our minds later, we change the loader — but for now it's JSON.

**Evan**: No objection from packaging. JSON configs are easy to drop into images and CI.

**Alice**: OK — JSON it is. Charlie, proceed with that.

**Bob**: Works for the API side too.
