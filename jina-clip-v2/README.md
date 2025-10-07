<h1 align="center">Jina CLIP v2 Multilingual Multimodal Embeddings API</h1>
<div align="center">
<a target="_blank" href="https://lightning.ai/bhimrajyadav/studios/deploy-jina-clip-v2-a-guide-to-multilingual-multimodal-embeddings-api-with-litserve">
  <img src="https://pl-bolts-doc-images.s3.us-east-2.amazonaws.com/app-2/studio-badge.svg" alt="Open In Studio"/>
</a>
</div>

Welcome to the **Jina CLIP V2 API**! This API leverages the cutting-edge Jina CLIP V2 model to provide multilingual and multimodal (text and image) embeddings. With support for 89 languages, high-resolution image processing, and advanced embedding capabilities, this API is perfect for powering neural information retrieval and multimodal GenAI applications.

> Multimodal embeddings enable the seamless understanding and retrieval of data across text and image modalities through unified representations.

![image](https://github.com/user-attachments/assets/d078f4a3-3b7a-4932-b69d-1fdf8ceb0031)

## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed:
- Python 3.8+
- `pip` (Python package installer)

### Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/bhimrazy/litserve-examples.git
    cd jina-clip-v2
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
    "model": "jina-clip-v2",
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
  "object": "list",
  "data": [
    {
      "object": "embedding",
      "embedding": [
        0.0023064255,
        -0.009327292,
        ...
        -0.0028842222
      ],
      "index": 0
    }
  ],
  "model": "jina-clip-v2",
  "usage": {
    "prompt_tokens": 6,
    "total_tokens": 6
  }
}

```

## ⚙️ Model Features
- Multilingual Support: Supports 89 languages for text and image retrieval.
- High-Resolution Image Processing: Accepts 512x512 images for better feature extraction.
- Matryoshka Representations: Flexible embedding dimensions (1024 → 64) to optimize performance and storage.
- Improved Retrieval Performance: Outperforms v1 by 3% in both text-text and text-image retrieval tasks.

## 📚 Documentation

For more detailed information, refer to the following resources:
- [Jina CLIP V2 Blog](https://jina.ai/news/jina-clip-v2-multilingual-multimodal-embeddings-for-text-and-images/)
- [Jina CLIP V2 Huggingface](https://huggingface.co/jinaai/jina-clip-v2)
- [LitServe Documentation](https://github.com/Lightning-AI/litserve)

## 🤝 Contributing

We welcome contributions from the community! If you'd like to contribute to this project, please read our [Contributing Guidelines](../CONTRIBUTING.md) to get started.

## 📜 License

This project is licensed under the [Apache License](../LICENSE).

---

Happy coding! 🎉
