**Source ID**: SRC-GDOC-22

# Benchmark Script Authoring Notes
**Owner**: Evan
**Document Key**: DOC-2022
**Last Updated**: 2026-08-17 (retrospective, covers 2026-08-07)

Looking back at the bare-metal benchmark work under CIPH-38, from where the scripting started.

## What was authored on 2026-08-07
A set of repeatable benchmark scripts intended to produce bare-metal performance numbers for release performance claims. The scripts run a fixed batch of documents through the CLI and record throughput and latency percentiles.

## What happened after authoring
Once written, the scripts sat blocked for a stretch while a dedicated bare-metal node was provisioned — they weren't written to target shared or virtualized hardware, since noisy neighbors would make the numbers unusable for a release claim. They were rerun once that node became available, and results were published depending on the completed multi-threading baseline.

## Scope of this note
This note is about the scripts themselves and why they were written the way they were; it is not a report on the published benchmark numbers.
