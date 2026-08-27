**Source ID**: SRC-GDOC-32

# Telemetry Opt-Out Flag Semantics
**Owner**: Diana
**Document Key**: DOC-2032
**Last Updated**: 2026-09-06 (retrospective, covers 2026-08-20)

Retrospective decision note on the opt-out flag semantics settled 2026-08-20 for CIPH-48 (Telemetry Opt-Out).

## Decision
The CLI accepts an explicit `--no-telemetry` flag. When present, it must suppress every outbound telemetry call for that invocation, including startup pings and error reports — not just usage-metric events.

## Why "explicit" matters
The flag was deliberately specified as opt-out rather than opt-in-by-default-off, since the goal was to give privacy-sensitive users a clear, discoverable switch rather than relying on a config file most users would never find.

## Note
This record settles the flag's expected behavior. Confirming that behavior against an actual network trace was a separate verification step and is not part of this decision note.
