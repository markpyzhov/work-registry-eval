**Source ID**: SRC-GDOC-38

# Node Sync Handshake Prototype — Architecture Note

**Owner**: Bob
**Document Key**: DOC-2038
**Last Updated**: 2026-08-15 (retrospective, covers 2026-08-06)

Multi-site local deployments need authenticated node sync without assuming a shared network password. T024 opened for a distributed zero-trust sync path; the first concrete deliverable was a replication handshake between peers.

## Prototype (2026-08-06)
Bob implemented a node-replication handshake so each side must authenticate before accepting sync traffic from the other. That put an Active prototype on the board for T024.

## What this note does not claim
Nominal-latency validation and any later high-latency failure modes are outside this write-up. As of 2026-08-06 the task was Active on the strength of the prototype alone.
