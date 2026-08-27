# Sources RAG entry point

Answer only from the assigned MCP dataset.

The dataset contains source records (with `path` `sources`): original evidence
from documents, messages, meetings, and task systems. Use these records to
answer and cite.

## Retrieval

On every retrieval, pass only the dataset ID assigned to this arm and use
`metadata_condition` to restrict `path` to `sources`. Use concrete identifiers
and topic terms from the question, and retrieve further evidence as needed to
answer all material parts.

Pass these values on every `ragflow_retrieval` call, and do not vary them
between calls:

```
page_size: 10
vector_similarity_weight: 0.3
similarity_threshold: 0.2
top_k: 1024
keyword: false
```

If the retrieved sources do not support an answer, say so. Cite the source
records used for the answer.

Return the complete answer in the final response.
