**Source ID**: SRC-GDOC-12

# Local Runtime — Static Linking Options Study

**Owner**: Evan
**Document Key**: DOC-2012
**Last Updated**: 2026-08-02

T018 needs the redaction engine packaged as a local runtime binary that runs in air-gapped environments with no dynamic dependency on external shared libraries or cloud services.

## Options Under Study
Evaluating static-linking approaches for compiling the runtime binary so it carries its own dependencies instead of relying on shared libraries present (or missing) on the target machine.

## Status
Active — study in progress. No build approach has been finalized yet.

## Next Step
Select an approach and move to a static compile attempt; verification against the air-gap requirement follows once a build exists.
