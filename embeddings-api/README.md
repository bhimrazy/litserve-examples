<!-- curl http://localhost:8000/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "input": "A beautiful sunset over the beach",
    "model": "jinaai/jina-embeddings-v2-small-en",
    "encoding_format": "float"
  }'

Output:
{
    "data": [
        {
            "index": 0,
            "embedding": [
                0.05936763063073158,
                ...,
                0.01047902274876833,
            ],
            "object": "embedding",
        }
    ],
    "model": "jinaai/jina-embeddings-v2-small-en",
    "object": "list",
    "usage": {"prompt_tokens": 0, "total_tokens": 0},
} -->
