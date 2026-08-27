**Source ID**: SRC-GDOC-26

# Exportable Redaction-Profile Schema (Design)

**Owner**: Bob
**Document Key**: DOC-2026
**Last Updated**: 2026-08-25

Looking back at the 2026-08-12 design pass for T032: compliance needs a machine-readable export of the active redaction profile so reviewers can inspect and reuse the same rules outside a single running instance.

## Why a schema first
Without a stable export shape, any later API or CLI dump would drift. Bob started by defining what an exportable profile must carry—enough structure to represent the active redaction rules in a portable, auditable form—before wiring an endpoint.

## Boundary of this note
This is the design step only. Implementing a schema-export API and verifying it against the REST contract were not part of the 2026-08-12 work and are not claimed here. As of that date the task remained Active.
