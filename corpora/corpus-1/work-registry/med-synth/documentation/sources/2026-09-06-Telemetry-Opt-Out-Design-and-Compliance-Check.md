**Source ID**: SRC-GDOC-51

# Privacy Design Note: Telemetry Opt-Out Flag Semantics
**Owner**: Diana
**Document Key**: DOC-2051
**Last Updated**: 2026-09-06

## Opt-Out Behaviour Designed
The CLI and API collect anonymous usage metrics (pages processed, OCR fallback rate) to help tune the detection engine. Setting `CIPHER_TELEMETRY=0`, or the equivalent GUI toggle, is designed to immediately stop all outbound telemetry traffic to the metrics endpoint.

## Design-Time Issue Found and Patched: Pending-Queue Leak
While designing the flag semantics, testing surfaced that the opt-out flag blocked network egress correctly, but the `TelemetryLogger` kept writing event payloads to a local SQLite queue regardless. That meant re-enabling telemetry later would flush the entire backlog accumulated during the opt-out period, including events the user believed were never being recorded. The logger was patched to a no-op backend when opted out, closing that gap before the flag semantics were finalized.

## Verification (Retrospective)
A network trace on 2026-08-24 confirmed zero outbound telemetry traffic once the opt-out flag is set, closing the CLI-side verification as Completed.

## Remaining Limitation
The third-party Electron crash reporter (Sentry) has not been audited for whether it independently respects the opt-out environment variable or requires its own disable hook for minidump uploads.

*Note*: CLI-side telemetry opt-out is verified. Full privacy compliance for air-gapped/opt-out users cannot be claimed until the Sentry crash-reporter path is audited separately.
