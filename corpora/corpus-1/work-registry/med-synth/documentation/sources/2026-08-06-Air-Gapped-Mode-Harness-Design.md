**Source ID**: SRC-GDOC-46

# Design Note: Reproducible Offline Test Harness
**Owner**: Diana
**Document Key**: DOC-2046
**Last Updated**: 2026-08-06

## Why a Harness, Not a One-Off VM
An earlier air-gapped check (see the manual single-VM USB-transfer test) proved the CLI *can* run offline, but it wasn't repeatable — every run required hand-configuring a disconnected machine. T027 calls for a harness that reliably and automatically denies network access on every run, so the offline claim can be re-verified continuously rather than checked once by hand.

## Harness Design
- Runs the batch CLI inside a dedicated Linux network namespace (`ip netns`) with no interfaces attached except loopback, rather than relying on a physically air-gapped machine.
- A wrapper script asserts the namespace has zero routable interfaces before invoking the CLI, and fails the harness run outright — rather than silently proceeding — if any route to the outside world is detected.
- Harness output is a pass/fail plus a captured syscall-level network-attempt log, so any code path that *tries* to reach the network, even if it degrades gracefully, is visible for follow-up.

## Status
Denies network access reliably and repeatably across local test runs. The harness is not yet wired into CI (it currently runs manually), and it validates network denial only — it does not itself certify the full offline batch run for compliance purposes; that sign-off is a separate step.

*Status*: Active. Harness reliably enforces network denial; CI integration and any compliance certification are separate, not-yet-complete steps.
