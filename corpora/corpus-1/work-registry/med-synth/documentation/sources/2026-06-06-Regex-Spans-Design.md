**Source ID**: SRC-GDOC-01

# Financial PII Regex Detection — Implementation Start

**Owner**: Charlie
**Document Key**: DOC-2001
**Last Updated**: 2026-06-06

## Context
Implementation begins today on the regex-based financial PII detection layer (T002). This layer runs over text produced by the core redaction engine (T001), which Diana reviewed and marked Completed on 2026-06-05.

## Scope
Detection covers financial PII patterns identified during scoping at task creation — the layer matches candidate spans in the extracted text and hands them to the redaction step downstream.

## Status
Active. Acceptance requires the detection layer to pass the financial-detection test suite before dependent HIPAA pattern work (T020) can build on it.

## Open Question
No test pass has run yet against this implementation. Until it does, we don't have a read on how the initial pattern set performs against real extracted text.
