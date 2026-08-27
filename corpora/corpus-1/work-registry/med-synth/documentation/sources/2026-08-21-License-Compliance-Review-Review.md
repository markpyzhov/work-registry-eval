**Source ID**: SRC-GDOC-24

# Third-Party License Inventory Report
**Owner**: Diana
**Document Key**: DOC-2024
**Last Updated**: 2026-08-21 (retrospective, covers 2026-08-09; notes status through 2026-08-15)

Retrospective report on the third-party license audit under CIPH-40.

## Scope of the 2026-08-09 inventory
An audit of the dependency tree was run to catalog every third-party license in use ahead of release, flagging anything more restrictive than a permissive license.

## Finding and immediate action
The PDF-parsing dependency's license was flagged as a concern, and the team swapped it for a different parser library as a direct result of this inventory.

## Status as of 2026-08-15
Because this report is written retrospectively on 2026-08-21, it can note the later developments: the replacement parser adopted from the 08-09 finding was swapped in on 2026-08-11, then the task reopened on 2026-08-12 when that replacement turned out itself to be AGPL-licensed, which is not acceptable for the shipped dependency set. By 2026-08-15 the team was searching for an Apache- or MIT-licensed alternative; that search had not concluded as of this writing.

## Limitation
This report does not certify overall license compliance. The parser-license question remains open.
