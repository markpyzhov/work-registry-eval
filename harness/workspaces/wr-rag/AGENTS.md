# Work Registry RAG entry point

Answer only from the assigned MCP dataset.

For current-status or “as of” questions, the relevant Work State
(`path = work-state`) is authoritative and already incorporates its Sources and
Comments. Do not recompute its state from them. Use Sources (`path = sources`)
and Comments (`path = comments`) for provenance, facts, history, causes,
chronology, assignees, next actions, and supporting details.

Chunks with `path = work-state-index` or `path = source-index` are navigation
aids, not evidence.

## Retrieval

On every retrieval, pass only the dataset ID assigned to this arm. Use concrete
identifiers and topic terms from the question, and retrieve further evidence as
needed to answer all material parts.

Pass these values on every `ragflow_retrieval` call, and do not vary them
between calls:

```
page_size: 10
vector_similarity_weight: 0.3
similarity_threshold: 0.2
top_k: 1024
keyword: false
```

If the retrieved evidence does not support an answer, say so. Cite the dataset
records used for material claims.

Return the complete answer in the final response.
