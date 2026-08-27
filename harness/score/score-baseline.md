# Score the no-retrieval baseline

Use the same units, rules, and output files as `score-rounds.md`, with these
details:

- Baseline sessions have `arm = baseline`, belong to Corpus 2, and join the
  `sources` key group.
- Grade them against the C2 Sources answer key. Never supply the Work Registry
  key.
- Generation allowed internal/parametric knowledge only, assumed an information
  cutoff of 2026-02-27, and forbade files, tools, retrieval, and MCP.
- If an answer matches the Sources key, grade it normally. Retrieval was
  forbidden during generation, not during scoring.
