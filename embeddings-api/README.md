<h1 align="center">Build and Scale Embeddings API Like a Pro using OpenAI EmbeddingSpec with LitServe</h1>
<div align="center">
<a target="_blank" href="https://lightning.ai/bhimrajyadav/studios/deploy-jina-clip-v2-a-guide-to-multilingual-multimodal-embeddings-api-with-litserve">
  <img src="https://pl-bolts-doc-images.s3.us-east-2.amazonaws.com/app-2/studio-badge.svg" alt="Open In Studio"/>
</a>
</div>

Welcome to the Embeddings API! This project demonstrates how to build and scale an embeddings API using the OpenAI Embedding Spec with LitServe.

## Overview

This API combines three powerful tools to deliver fast and flexible embedding services:

- 🚀 **LitServe** - Powers the API infrastructure ([GitHub](https://github.com/Lightning-AI/litserve))
- 🔌 **OpenAI Embedding Spec** - Ensures API compatibility
- ⚡ **FastEmbed** - Generates high-quality embeddings ([GitHub](https://github.com/qdrant/fastembed))

> FastEmbed is a lightweight, fast, Python library built for embedding generation. 

Get started quickly with any embedding model using our OpenAI-compatible API interface!

![embeddings-api-using-openai-embedding-spec](https://github.com/user-attachments/assets/acbb61c6-74e5-4d8a-a69e-5c78a3de2485)


## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed:
- Python 3.8+
- `pip` (Python package installer)

### Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/bhimrazy/litserve-examples.git
    cd embeddings-api
    ```

2. **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

### Running the Server
    ```sh
    python server.py
    ```

The server will start on `http://localhost:8000/v1/embeddings`.

### Making a Request

To generate embeddings, send a POST request to the `/v1/embeddings` endpoint with the required inputs. Here's an example using `curl`:
**Text Embedding**
```sh
curl http://localhost:8000/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "input": "A beautiful sunset over the beach",
    "model": "jinaai/jina-embeddings-v2-small-en",
    "encoding_format": "float"
  }'
```

Test using python client
```sh
python client.py
```

### Example Response

```json
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
}
```
## 📚 Documentation

For more detailed information, refer to the following resources:
- [FastEmbed Documentation](https://qdrant.github.io/fastembed/)
- [LitServe Documentation](https://github.com/Lightning-AI/litserve)

## 🤝 Contributing

We welcome contributions from the community! If you'd like to contribute to this project, please read our [Contributing Guidelines](../CONTRIBUTING.md) to get started.

## 📜 License

This project is licensed under the [Apache License](../LICENSE).

---

Happy coding! 🎉
