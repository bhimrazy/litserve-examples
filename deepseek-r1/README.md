<h1 align="center">Chat with DeepSeek-R1</h1>

## 🎯 Overview
✨ Interactive AI Chat Powered by LitServe, Streamlit, and an OpenAI-Compatible API 💡

🔥 With this setup, you get:
 ✅ Effortlessly chat with DeepSeek-R1 in real time.
 ✅ Leverage OpenAI-compatible APIs for seamless integration with your apps.
 ✅ Deploy quickly and scale efficiently using the power of LitServe.


## 🚀 Quick Start

### Prerequisites

Ensure you have the following installed:
- Python 3.8+
- `pip` (Python package installer)

### Setup

```bash
# Clone repository
git clone https://github.com/bhimrazy/litserve-examples.git
cd deepseek-r1

# Install dependencies
pip install -r requirements.txt

# Start server
python server.py

# Start streamlit app
streamlit run app.py
```

> The server will start on `http://localhost:8000`.
> The streamlit app will start on: `http://localhost:8501`.

### Usage

Generate response using cURL:

```sh
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-r1",
    "messages": [
      {
        "role": "user",
        "content": "Hello!"
      }
    ]
  }'

```

Using the Python client:
```sh
python client.py --prompt="Hello"
```

### Response

```json
{
  "id": "chatcmpl-597906",
  "object": "chat.completion",
  "created": 1737869840,
  "model": "deepseek-r1",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "<think>\n\n</think>\n\nHello! How can I assist you today? 😊",
      },
      "finish_reason": "stop"
    }
  ]
}
```
## 📚 Resources

For more detailed information, refer to the following resources:
- [Discover DeepSeek-R1](https://huggingface.co/deepseek-ai/DeepSeek-R1)
- [LitServe Documentation](https://lightning.ai/docs/litserve/home)

## 🤝 Contributing

We welcome contributions from the community! If you'd like to contribute to this project, please read our [Contributing Guidelines](../CONTRIBUTING.md) to get started.

## 📜 License

This project is licensed under the [Apache License](../LICENSE).

---

Happy coding! 🎉
Built with ❤️ using [LitServe](https://github.com/Lightning-AI/litserve)
