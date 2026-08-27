**Source ID**: SRC-GDOC-35

# Crypto Sign-off: AES-256 At-Rest Encryption Pipeline
**Owner**: Diana
**Document Key**: DOC-2035
**Last Updated**: 2026-08-07

## Sign-off Basis
Security sign-off on the AES-256 at-rest pipeline was withheld until the fail-closed deletion behavior for interrupted redaction runs (T015) was confirmed Completed — an unencrypted partial output left on disk after a crash would have undermined the encryption guarantee entirely. With that dependency cleared, the sign-off proceeded against the pipeline as implemented.

## What Was Reviewed
- AES-256-GCM authenticated encryption applied to every redacted output file before it is written to its final location.
- Key handling confined to process memory; no plaintext key material written to disk or logs.
- Confirmed the pipeline degrades safely (refuses to write plaintext) if key material is unavailable, consistent with the fail-closed contract from T015.

## Follow-up Noted at Sign-off
On machines without a hardware TPM, the volume key is still derived from a user passphrase via PBKDF2-HMAC-SHA256 at 100k iterations. This is not a blocker for the AES-256 pipeline sign-off itself, but Diana flagged it as a hardening follow-up: moving to Argon2id would meaningfully raise the cost of offline brute-force against weak passphrases on non-TPM hardware.

*Status*: AES-256 at-rest pipeline signed off as Completed. Passphrase-derived key hardening (Argon2id) tracked separately as a pre-v1.0 hardening item, not a sign-off condition.
