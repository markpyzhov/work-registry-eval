**Source ID**: SRC-GDOC-30

# Document: High-DPI-Coordinate-Misalignment-Repro
**Owner**: Charlie
**Document Key**: DOC-2030
**Last Updated**: 2026-09-02 (retrospective, covers 2026-08-17)

## Test Logs
Reproduction notes for the high-DPI coordinate misalignment reported for CIPH-46, first reproduced 2026-08-17.

## Repro steps
1. Open a PDF on a display reporting a scale factor above 1.0 (tested at 150% and 200%).
2. Compare the redaction preview overlay's reported box coordinates against the coordinates the rendering library reports for the same region.
3. At scale factors above 1.0, the overlay box is offset from the actual text region, with the offset growing as scale factor increases.

## Result
The misalignment reproduces consistently at both tested scale factors. It does not reproduce at 100% scale.

## Status
Root cause has not been isolated as part of this reproduction pass; this note only establishes that the defect reproduces and under which display conditions.
