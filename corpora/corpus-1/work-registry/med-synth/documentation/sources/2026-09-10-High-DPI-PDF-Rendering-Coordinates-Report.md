**Source ID**: SRC-GDOC-49

# Technical Report: High-DPI Coordinate Scaling — Upstream Block
**Owner**: Diana
**Document Key**: DOC-2049
**Last Updated**: 2026-09-10

## Background
Earlier work (2026-08-17) reproduced misalignment on 4K displays. Follow-on scaling math (2026-08-19) was checked against the Completed preview-overlay coordinates from T023.

## Finding
The scaling error points to a defect in the upstream rendering library's scaling math. No safe local fix has been identified yet.

## Current Status: Blocked
T036 is Blocked on that upstream library issue. Local coordinate work remains dependent on T023's overlay path but cannot clear the gate until upstream scaling is corrected or an accepted local remediation is chosen.

*Status*: Blocked on upstream rendering-library scaling math.
