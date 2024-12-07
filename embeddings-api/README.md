<h1 align="center">Build and Scale Embeddings API Like a Pro using OpenAI EmbeddingSpec with LitServe</h1>
<div align="center">
<a target="_blank" href="https://lightning.ai/bhimrajyadav/studios/deploy-jina-clip-v2-a-guide-to-multilingual-multimodal-embeddings-api-with-litserve">
  <img src="https://pl-bolts-doc-images.s3.us-east-2.amazonaws.com/app-2/studio-badge.svg" alt="Open In Studio"/>
</a>
</div>

## 🎯 Overview

A production-ready embeddings API that combines:

- 🚀 **LitServe** - High-performance API infrastructure
- 🔌 **OpenAI Embedding Spec** - Industry-standard API compatibility 
- ⚡ **FastEmbed** - Efficient embedding generation

![embeddings-api-using-openai-embedding-spec](https://github.com/user-attachments/assets/acbb61c6-74e5-4d8a-a69e-5c78a3de2485)


## 🚀 Quick Start

### Prerequisites

Ensure you have the following installed:
- Python 3.8+
- `pip` (Python package installer)

### Setup

```bash
# Clone repository
git clone https://github.com/bhimrazy/litserve-examples.git
cd embeddings-api

# Install dependencies
pip install -r requirements.txt

# Start server
python server.py
```

> The server will start on `http://localhost:8000/v1/embeddings`.

### Usage

Generate embeddings using cURL:

```sh

curl http://localhost:8000/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "input": "A beautiful sunset over the beach",
    "model": "jinaai/jina-embeddings-v2-small-en",
    "encoding_format": "float"
  }'
```

Or using the Python client:
```sh
python client.py
```

### Response Format

```json
{
    "data": [{
        "index": 0,
        "embedding": [0.059, ..., 0.010],
        "object": "embedding"
    }],
    "model": "jinaai/jina-embeddings-v2-small-en",
    "object": "list",
    "usage": {
        "prompt_tokens": 0,
        "total_tokens": 0
    }
}
```
## 📚 Resources

For more detailed information, refer to the following resources:
- [FastEmbed Documentation](https://qdrant.github.io/fastembed/)
- [LitServe Documentation](https://lightning.ai/docs/litserve/home)

## 🤝 Contributing

We welcome contributions from the community! If you'd like to contribute to this project, please read our [Contributing Guidelines](../CONTRIBUTING.md) to get started.

## 📜 License

This project is licensed under the [Apache License](../LICENSE).

---

Happy coding! 🎉
Built with ❤️ using [LitServe](https://github.com/Lightning-AI/litserve)