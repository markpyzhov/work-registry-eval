**Source ID**: SRC-GDOC-21

# Test Note: Air-Gapped Mode Execution
**Owner**: Diana
**Document Key**: DOC-2021
**Last Updated**: 2026-08-06

## Isolated Test Setup
To simulate a strictly offline deployment, we deployed the CLI on a fresh Ubuntu 22.04 VM with the virtual network adapter explicitly disabled (no loopback to host, no NAT). We transferred the application bundle and a 200-document test corpus via a simulated USB mount.

## What Worked
- The core regex engine and OCR pipeline initialized perfectly without attempting to phone home for license verification or telemetry updates.
- The local TPM-based volume encryption successfully mounted the temporary storage drives using the pre-seeded hardware key.
- Redaction throughput remained identical to the networked baseline.

## Test Limitation
This run built and smoke-tested the harness itself; it did not yet execute a full batch to completion or produce a sign-off. That full run — depending on the already-completed AES-256 encryption pipeline — is the next step and is not reported on here.
