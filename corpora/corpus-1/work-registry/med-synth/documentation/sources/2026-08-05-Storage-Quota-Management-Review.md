**Source ID**: SRC-GDOC-16

# Storage Quota — Disk-Usage Monitor

**Owner**: Evan
**Document Key**: DOC-2016
**Last Updated**: 2026-08-05 (retrospective of 2026-08-04)

Large batch runs can exhaust local disk if nothing caps write volume. T022 opened to add a storage quota for that reason.

## Monitor loop
On 2026-08-04 Evan landed a live disk-usage monitor that watches free space during batch processing and is meant to stop further writes once a configured quota is crossed. The loop is in place; it is not yet a signed-off gate.

## Still open
Nobody has yet confirmed that the monitor actually halts writes at the configured threshold. Until that check lands, T022 stays Active.
