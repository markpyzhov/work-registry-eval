# WS-04: Release Process
**Status**: in_progress
**Priority**: P1
**Owner**: Tyler Yahn (SIG lead context); actions on Alex Boten / Nico Hertz
**Project**: opentelemetry-go
**Last Updated**: 2025-11-27

## Sources
- `SRC-NOTE-07` — [entry-3581463689.md](../opentelemetry/meeting-notes/entry-3581463689.md)
- `SRC-NOTE-08` — [entry-3974113940.md](../opentelemetry/meeting-notes/entry-3974113940.md)

## Request / Context
Unblock the next Go release around OTelConf RC support / experimental API layout, and decide how to handle a large runtime-tracer / `pprof` profiling API proposal.

## Task List
- [ ] `T001` (mapped to OTelConf RC / experimental API) — Merge OTelConf RC support after normal review; track experimental API structure (e.g. `x` submodule) under `1.40.0`. `(SRC-NOTE-07)`
- [ ] `T002` (mapped to runtime profiling) — Document profiling proposal in an issue; start with a smaller change to allow disabling runtime tracer integration (large public API change deferred). `(SRC-NOTE-08)`

## Active Work
- **`T001`**: Assigned action for **Alex Boten** to open an issue tracking evaluation of experimental API structure for the OTelConf RC module and add it to the `1.40` milestone; SIG reviewers to review the RC support PR `(SRC-NOTE-07)`. Sources do not include that issue or the RC PR itself.
- **`T002`**: Assigned actions for **Nico Hertz** to open an issue describing the runtime profiling problem/proposal and to create a smaller PR allowing disablement of runtime tracer integration `(SRC-NOTE-08)`. Sources do not establish that either follow-up was filed.

## Blockers and Dependencies
- **`T001`**: As of 2025-11-20, the release was described as blocked on RC support module review `(SRC-NOTE-07)`. Final merge/delivery of that PR is not in the package.

## Decisions and Superseded Directions
- **OTelConf RC (`T001`)**: On 2025-11-20, merge the OTelConf RC support PR as-is (pending normal review); track experimental API structure review under `1.40.0` `(SRC-NOTE-07)`.
- **Runtime profiling API (`T002`)**: On 2025-11-27, do not merge the large public-API change without prior issue discussion; keep the existing PR as draft/proof of concept; begin with a smaller disablement change `(SRC-NOTE-08)`.

## Done / Evidence
- None established in the frozen Sources (no RC PR, no follow-up issue/PR bodies).

## Needs Manual Triage
- None.

## Next Update Needed
- Presence of the OTelConf RC PR outcome, Alex’s tracking issue, and Nico’s issue / smaller disablement PR.
