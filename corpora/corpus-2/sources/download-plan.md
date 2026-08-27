# Corpus 2 source collection

What was collected for Corpus 2, and how. The evidence itself lives in
`github-sources/` (raw payloads) and `../work-registry/opentelemetry/`
(converted Sources); the totals are in the repository `README.md`.

## Origin

Everything comes from the public
[`open-telemetry/opentelemetry-go`](https://github.com/open-telemetry/opentelemetry-go)
repository. Its [SIG meeting-notes issue `#6648`](https://github.com/open-telemetry/opentelemetry-go/issues/6648)
keeps roughly weekly minutes as comments that cross-link the issues and pull
requests discussed, so one work item's state is spread across a meeting note,
an issue, a PR, and a later release.

That spread is the point. GitHub's `open`, `closed`, and `merged` fields make
plain status questions too easy, so the questions were selected to need
evidence from more than one Source: merged versus released, blockers named only
in the notes, and later evidence superseding an earlier statement.

## What was downloaded from GitHub

| Setting | Value |
| --- | --- |
| Meeting-notes issue | `open-telemetry/opentelemetry-go#6648` |
| Entries selected | 8, from `2025-10-10T12:53:12Z` to `2026-02-27T17:20:46Z` |
| Collected at | `2026-07-14T14:35:41Z` |

From those entries, the collection followed:

- every issue and pull request they reference, anywhere in the
  `open-telemetry` org — each with its comments, reviews, inline review
  comments, and timeline events;
- the milestones attached to those items;
- release notes for every referenced version tag.

References outside the org sit outside the GitHub issue API and were not
downloaded. `github-sources/referenced-external.txt` logs the three that
appeared, in `golang/go` and `grpc/grpc-go`.

The run produced 26 payloads under `github-sources/`:

| Directory | Files |
| --- | --- |
| `meeting-notes/` | 8 |
| `issues/` | 6 |
| `pulls/` | 7 |
| `milestones/` | 4 |
| `releases/` | 1 |

Each file is a `{source, document}` envelope: the GitHub payload plus canonical
URL, artifact type, author, created and updated dates, and collection date.
`manifest.json` indexes all 26. The `_*.txt` and `_*.uniq` files are the
reference-resolution scratch kept from the run.

## What was converted to Markdown

Each envelope became one Markdown Source in
`../work-registry/opentelemetry/`, mirroring the subdirectories above. Every
Source:

- stitches description, discussion, reviews, and significant timeline events
  into a single readable document;
- carries a stable `SRC-*` ID, numbered per artifact type by creation time
  (`SRC-NOTE-01`, `SRC-ISSUE-01`, …);
- has a row in the Source Registry `../work-registry/integrations/github.md`,
  mapping the ID to its path and canonical URL.
