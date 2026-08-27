# License compliance looked cleared after a PDF-parser swap, then changed again. As of **2026-09-22**, what is the current license-gate status, what discovery reopened it, and what replacement criteria are in force?

<!-- RESPONSE_START -->

As of 2026-09-22, the license gate is **not cleared**: CIPH-40 remains **Active (Reopened)**, and the parser-license question is explicitly unresolved. [SRC-CU-CIPH-40] [SRC-GDOC-24]

It reopened after a follow-up review of the PDF-parser replacement: Diana checked its license file directly and confirmed it was **AGPL-licensed**—unshippable under the current distribution model. The initial swap had removed the original Ghostscript AGPLv3 dependency but reintroduced the same prohibited copyleft category through the replacement. [SRC-SLACK-40] [SRC-GDOC-41]

The replacement must:

- Be Apache 2.0 or MIT licensed (non-copyleft).
- Cover the required parsing/rasterization capabilities; candidates lacking full feature coverage are not acceptable.
- Be adopted and pass a clean rescan.
- Leave the full shipped dependency tree free of restrictive copyleft licenses such as AGPL. [SRC-CU-CIPH-40] [SRC-SLACK-41]
