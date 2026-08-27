# Corpus RAG parent job

Running instructions for Codex.

Run every listed profile, question, and dataset combination. Each profile must
use `gpt-5.6-terra` with High reasoning.

Command to run a child process:

```shell
codex exec --ephemeral --json --profile <profile> -C <Work Directory> "<prompt>"
```

`<profile>`, `<Work Directory>`, and `<prompt>` described below.

Rules:

- Run at most three children concurrently.
- Never combine questions, rounds, or answers.
- Complete round 1 for all 60 profile/question combinations, then verify that every child exited successfully and produced a complete final response before starting round 2. Repeat that check before round 3.
- Retry every failed, inaccessible, or incomplete child as the same round with a fresh child process. Do not count a run as complete unless it exits successfully and presents its full final response.
- The parent agent does not summarize, export, or score the answer.
- Every question and dataset should run separately for three rounds, using a fresh child process each time

## Preserve and review output

Keep every child artifact; never overwrite or delete a prior attempt. Store each
child's full final response and its `--json` event stream separately, with a
name that includes corpus, question, arm, and round (for example,
`c1-q01-raw-r2.final.md` and `c1-q01-raw-r2.jsonl`). Keep a separate status
file with the exit code. For a retry, add a retry suffix instead of replacing
the original files.

Review `*.final.md` for the answer, `*.jsonl` for the complete child event and
retrieval log, and `*.status` for the exit code. A child that has no final
answer file is complete only when its JSONL log contains its complete final
agent response; otherwise retry it.

Profiles and variables:

1. `profile`: `c1-raw-rag`:
    - `Work Directory`: `<REPLACE_REPO_ROOT>harness/workspaces/raw-rag/`
    - Question files: `<REPLACE_REPO_ROOT>harness/workspaces/c1-questions.md`
    - `C_DATASET_ID`: `REPLACE_C1_SOURCES_DATASET_ID`
2. `profile`: `c1-wr-rag`:
    - `Work Directory`: `<REPLACE_REPO_ROOT>harness/workspaces/wr-rag/`
    - Question files: `<REPLACE_REPO_ROOT>harness/workspaces/c1-questions.md`
    - `C_DATASET_ID`: `REPLACE_C1_WORK_REGISTRY_DATASET_ID`
3. `profile`: `c2-raw-rag`:
    - `Work Directory`: `<REPLACE_REPO_ROOT>harness/workspaces/raw-rag/`
    - Question files: `<REPLACE_REPO_ROOT>harness/workspaces/c2-questions.md`
    - `C_DATASET_ID`: `REPLACE_C2_SOURCES_DATASET_ID`
4. `profile`: `c2-wr-rag`:
    - `Work Directory`: `<REPLACE_REPO_ROOT>harness/workspaces/wr-rag/`
    - Question files: `<REPLACE_REPO_ROOT>harness/workspaces/c2-questions.md`
    - `C_DATASET_ID`: `REPLACE_C2_WORK_REGISTRY_DATASET_ID`

`prompt` for `c1-raw-rag` and `c2-raw-rag`:

```text
<QUESTION>

Use only `tl-v1` MCP with `<C_DATASET_ID>` dataset to answer. Do not use web,
local files, memory, or any other MCP dataset.
```

`prompt` for `c1-wr-rag` and `c2-wr-rag`:

```text
<QUESTION>

Use only `tl-v1` MCP with `<C_DATASET_ID>` dataset to answer. Do not use web,
local files, memory, or any other MCP dataset.
```
