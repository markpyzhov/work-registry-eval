# Merge score cards

Run this only after generation, collection validation, and all three scorers.
Implemented by `merge_score_cards.py`.

## Inputs

- `<run>/usage.csv`;
- `<run>/scores/{claude,codex,cursor}.csv`;
- optional `<run>/scores/human.csv`.

Each scorer file must contain every manifest session exactly once. The merge
fails before writing if a file, session, or value is invalid.

## Outputs

- `<run>/score-cards-long.csv`: every raw scorer judgment;
- `<run>/score-cards.csv`: one merged row per session.

Numeric fields use the three-scorer median. A valid `human.csv` row supersedes
only final correctness; raw scorer diagnostics remain visible.

```shell
python3 harness/score/validate_score_run.py --run-dir <run>
python3 harness/score/merge_score_cards.py --run-dir <run>
```
