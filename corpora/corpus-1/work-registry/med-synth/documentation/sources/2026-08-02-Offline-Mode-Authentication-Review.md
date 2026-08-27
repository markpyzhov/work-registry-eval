**Source ID**: SRC-GDOC-13

# Offline-Mode Authentication — Key-Rotation Design

**Owner**: Diana
**Document Key**: DOC-2013
**Last Updated**: 2026-08-02

**Constraint**: T019 must support authentication for air-gapped deployments where an always-on network cannot be assumed.

## Design Focus
Working out a key-rotation flow that does not depend on continuous network reachability, since the target deployments are air-gapped.

## Open Question
How rotation behaves for a workstation that stays offline for an extended period has not been validated yet — that check is expected once a local auth mock exists.

## Status
Active — design stage.
