# Run rounds

Running instructions for Claude Code and Codex.

Claude Code should run subagents with `claude-opus-5` with default reasoning.

Codex should run subagents with `gpt-5.6-terra` with "High" reasoning.

Don't run more than 3 subagents simultaneously.

## Run cards

| Arm       | Information available                                                                                                | Access method   |
| --------- | -------------------------------------------------------------------------------------------------------------------- | --------------- |
| `Raw Rag` | Raw project materials                                                                                                | RAG over MCP    |
| `WR Rag`  | The full Work Registry package: Work State, Comments, linked raw Sources, Source Registry, and, for C1, Daily Briefs | RAG over MCP    |
| `WR Dir`  | The same full package as Work Registry RAG                                                                           | Local directory |

Question files:

1. `C1`: `<REPLACE_REPO_ROOT>harness/workspaces/c1-questions.md`
2. `C2`: `<REPLACE_REPO_ROOT>harness/workspaces/c2-questions.md`
3. `Baseline`: `<REPLACE_REPO_ROOT>harness/workspaces/c2-questions.md`

Directories:

1. `WR Dir` `C1`: `<REPLACE_REPO_ROOT>harness/workspaces/c1/`
2. `WR Dir` `C2`: `<REPLACE_REPO_ROOT>harness/workspaces/c2/`
3. `Baseline`: `<REPLACE_REPO_ROOT>harness/workspaces/baseline/`
4. `Raw Rag`: `<REPLACE_REPO_ROOT>harness/workspaces/raw-rag/`
5. `WR Rag`: `<REPLACE_REPO_ROOT>harness/workspaces/wr-rag/`

`tl-v1` Datasets:

| Corpus | `Raw Rag`                          | `WR Rag`                           |
| ------ | ---------------------------------- | ---------------------------------- |
| `C1`   | `REPLACE_C1_SOURCES_DATASET_ID` | `REPLACE_C1_WORK_REGISTRY_DATASET_ID` |
| `C2`   | `REPLACE_C2_SOURCES_DATASET_ID` | `REPLACE_C2_WORK_REGISTRY_DATASET_ID` |

## Send one of these prompts

Replace `<QUESTION>` with one question from the selected corpus's question file.
Replace `<C_DATASET_ID>` with the dataset ID for the selected RAG arm.

### Sources RAG

Working directory: `Raw Rag`

```text
<QUESTION>

Use only `tl-v1` MCP with `<C_DATASET_ID>` dataset to answer. Do not use web,
local files, memory, or any other MCP dataset.
```

### Work Registry RAG

Working directory: `WR Rag`

```text
<QUESTION>

Use only `tl-v1` MCP with `<C_DATASET_ID>` dataset to answer. Do not use web,
local files, memory, or any other MCP dataset.
```

### Work Registry Directory — C1

Working directory: `WR Dir` `C1`

```text
<QUESTION>

Use only `<REPLACE_REPO_ROOT>harness/workspaces/c1/` directory to
answer. Do not use web, other files, memory, or MCP.
```

### Work Registry Directory — C2

Working directory: `WR Dir` `C2`

```text
<QUESTION>

Use only `<REPLACE_REPO_ROOT>harness/workspaces/c2/` directory to
answer. Do not use web, other files, memory, or MCP.
```

### Baseline — C2

Working directory: `Baseline`

```text
<QUESTION>

Answer only from your internal/parametric knowledge.
Assume an information cutoff of 2026-02-27.
Do not use web, local files (including `memory.md`), tools, retrieval, or MCP.
```

## Parent-agent job

For each specified run, launch a fresh subagent per round with the selected prompt and wait for completion. `C1` and `C2` run `Raw Rag`, `WR Rag`, and `WR Dir`; `Baseline` runs only `C2`; each uses every question, for each round. Total rounds 3.

The parent agent does not summarize, export, or score the answer.

Permissions:

1. **Allow** full access only to the target dataset for the `Rag` arms. For example, `Raw Rag` for the `C1` questions should have full access to `REPLACE_C1_SOURCES_DATASET_ID`, but **should not have access** to `REPLACE_C1_WORK_REGISTRY_DATASET_ID`, `REPLACE_C2_SOURCES_DATASET_ID`, or `REPLACE_C2_WORK_REGISTRY_DATASET_ID`.
2. **Allow** full access to the target directory for the `WR Dir` arm. For example, `WR Dir` for the `C1` questions should have full access to `<REPLACE_REPO_ROOT>harness/workspaces/c1/`, but **should not have access** to external directories or `<REPLACE_REPO_ROOT>harness/workspaces/c2/`

Retry policy:

1. If a subagent failed because of access issue rerun it again for the same round.
2. If a subagent did not present full response in the response, but sent it to parent, rerun it again for the same round.
