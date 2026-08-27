# RAG configuration

This document describes the RAG and MCP configuration to run the evaluations.

## Stack

- RAGFlow `v0.26.4`, local Docker.
- Embedding: `text-embedding-3-large`.
- No reranker, RAPTOR, or GraphRAG.
- Retrieval: RAGFlow MCP tool `ragflow_retrieval`.

## 1. Required RAGFlow fixes

As of the current version, RAGFlow has the following issues:

1. The MCP server doesn't support `metadata_condition`, which should help agents to search across only specific subsets of data.
2. The Token Chunker cannot ingest from the Title Chunker, so long documents with no headers could not be split into observable chunks.
3. Delimiters typed in the UI were ignored.
4. "Token size" mode ignored the token size whenever a delimiter existed.

These fixes were implemented in the fork: [markpyzhov/ragflow:cf9e404](https://github.com/markpyzhov/ragflow/commit/cf9e404d1623393772a11db68bddc111831b9165) (branch `metadata-delimiter-extension`).

To run MCP via `docker compose`, follow [docker-compose.yml instructions](https://github.com/markpyzhov/ragflow/blob/cf9e404d1623393772a11db68bddc111831b9165/docker/docker-compose.yml#L28).

*Note, these fixes were tested only for the evaluation use cases and may not work as expected in cases beyond these workflows.*

## 2. Configure Pipeline

`File → Parser → TitleChunker → TokenChunker → Tokenizer`

| Setting | Value |
| --- | --- |
| Parser output | `json` |
| `flatten_media_to_text` | `false` |
| Title method / level / rule | `hierarchy` / `2` / `0` |
| `root_chunk_as_heading` | `true` |
| `include_heading_content` | `false` |
| Chunk size / overlap | `512` / `0` |
| Delimiter mode / delimiter | `token_size` / `` `\n` `` (including backticks) |
| Filename embedding weight | `0.3` |
| Search | embedding + full text |

Dataset settings: similarity threshold `0.2`, vector weight `0.3`, pagerank
`0`, auto-keywords `0`, auto-questions `0`.

Retrieval settings: page size `10`, top-k `1024`, similarity threshold `0.2`,
vector weight `0.3`, keyword extraction off, no reranker. These settings are included in the `AGENTS.md` manifest.

## 3. Create Datasets

The published evaluation uses four datasets.

| Dataset | RAGFlow dataset ID | Imported package | Codex profile |
| --- | --- | --- | --- |
| C1 Sources | `REPLACE_C1_SOURCES_DATASET_ID` | `corpora/corpus-1/work-registry/med-synth/` | `c1-raw-rag` |
| C1 Work Registry | `REPLACE_C1_WORK_REGISTRY_DATASET_ID` | `corpora/corpus-1/work-registry/` | `c1-wr-rag` |
| C2 Sources | `REPLACE_C2_SOURCES_DATASET_ID` | `corpora/corpus-2/work-registry/opentelemetry/` | `c2-raw-rag` |
| C2 Work Registry | `REPLACE_C2_WORK_REGISTRY_DATASET_ID` | `corpora/corpus-2/work-registry/` | `c2-wr-rag` |

Create the datasets, process the files via the pipeline, and flag the files with the metadata below.

The corpora's files to upload are located at the following paths:

- C1: `corpora/corpus-1/work-registry/`
- C2: `corpora/corpus-2/work-registry/`

1. Arms: Sources RAG:

    - **Sources.** Files: `med-synth/*` for C1 and `opentelemetry/*` for C2

        Metadata: `path = sources`
    - **Source Index.** Files: `integrations/*`

        Metadata: `path = source-index`

2. Arms: Work Registry RAG:

    - **Sources.** Files: `med-synth/*` for C1 and `opentelemetry/*` for C2

        Metadata: `path = sources`
    - **Source Index.** Files: `integrations/*`

        Metadata: `path = source-index`
    - **Work States.** Files: `work-states/WS-*`

        Metadata: `path = work-state`
    - **Source Index.** Files: `work-states/comments/*`

        Metadata: `path = comments`
    - **Source Index.** Files: `work-states/index.md`

        Metadata: `path = work-state-index`

Do not upload `ground-truth/` and `sources/` files.

**Important:** once the datasets are created, replace "RAGFlow dataset ID" from the table above with the actual IDs across all files in the `harness/` directory.

## 4. Validate

Validate the number of documents, chunks, and the largest chunk to ensure the files were processed correctly.

| Dataset | Documents | Chunks | Largest chunk |
| --- | ---: | ---: | ---: |
| C1 Sources | 172 | 192 | 4,308 |
| C1 Work Registry | 184 | 282 | 4,308 |
| C2 Sources | 27 | 237 | 2,247 |
| C2 Work Registry | 34 | 277 | 2,247 |

## 5. Configure MCP integration from AI agents

The following are instructions to configure MCP integration if the server is running at `http://127.0.0.1:9382/mcp`.

## Claude Code

Init claude projects in the RAG arms workspaces:

1. Sources RAG: `harness/workspaces/raw-rag`
2. Work Registry RAG: `harness/workspaces/wr-rag`

Then add the MCP server:

```shell
claude mcp add --transport http tl-v1 http://127.0.0.1:9382/mcp
```

## Codex

Since July 2026, Codex may still read files even though the instructions restrict it for the RAG arms, so the most reliable configuration should be done via `codex-profiles`.

1. Ensure the `harness/workspaces/codex-profiles/*-rag.config.toml` use the right MCP host.
2. Copy the four files in `codex-profiles/` to `$CODEX_HOME` (normally
   `~/.codex`):

   ```shell
   EVAL_CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
   mkdir -p "$EVAL_CODEX_HOME"
   cp harness/workspaces/codex-profiles/c1-raw-rag.config.toml "$EVAL_CODEX_HOME/c1-raw-rag.config.toml"
   cp harness/workspaces/codex-profiles/c1-wr-rag.config.toml "$EVAL_CODEX_HOME/c1-wr-rag.config.toml"
   cp harness/workspaces/codex-profiles/c2-raw-rag.config.toml "$EVAL_CODEX_HOME/c2-raw-rag.config.toml"
   cp harness/workspaces/codex-profiles/c2-wr-rag.config.toml "$EVAL_CODEX_HOME/c2-wr-rag.config.toml"
   ```

3. Verify one with:

    ```shell
    codex --profile c1-raw-rag mcp list
    ```
