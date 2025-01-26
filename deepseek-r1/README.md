<h1 align="center">Chat with DeepSeek-R1</h1>
<div align="center">
<a target="_blank" href="https://lightning.ai/bhimrajyadav/studios/chat-with-deepseek-r1-an-advanced-ai-reasoning-model">
  <img src="https://pl-bolts-doc-images.s3.us-east-2.amazonaws.com/app-2/studio-badge.svg" alt="Open In Studio"/>
</a>
</div>

## 🎯 Overview

✨ **Interactive AI Chat** Powered by LitServe, Streamlit, and an OpenAI-Compatible API 💡

[https://github.com/user-attachments/assets/48fcff5a-e058-4f91-ada9-042bcdc05d2a](https://github.com/user-attachments/assets/48fcff5a-e058-4f91-ada9-042bcdc05d2a)

🔥 **Why Choose This?**

- ✅ Real-time chat experience with **DeepSeek-R1**.
- ✅ Seamlessly integrate with your apps via **OpenAI-compatible APIs**.
- ✅ Effortlessly deploy and scale with **LitServe's** capabilities.

---

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have:

- **Python 3.8+** installed.
- `pip`, the Python package installer.

### Setup

Follow these steps to get started:

```bash
# Clone the repository
git clone https://github.com/bhimrazy/litserve-examples.git
cd litserve-examples/deepseek-r1

# Install required dependencies
pip install -r requirements.txt

# Start the server
python server.py

# Launch the Streamlit app
streamlit run app.py
```

> - **Server URL:** `http://localhost:8000`
> - **Streamlit App URL:** `http://localhost:8501`

---

### Usage

#### Using the Streamlit Interface

Interact with the AI using the intuitive Streamlit web app.

![image](https://github.com/user-attachments/assets/df1a5ca3-0f65-4a7f-bdf3-f895ea724862)

#### Making API Requests

**Via cURL:**

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

**Using Python Client:**

```sh
python client.py --prompt="Hello"
```

---

### Sample Response

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
        "content": "Hello! How can I assist you today? 😊"
      },
      "finish_reason": "stop"
    }
  ]
}
```

---

## 📚 Resources

Explore more with these helpful links:

- [Discover DeepSeek-R1 on Hugging Face](https://huggingface.co/deepseek-ai/DeepSeek-R1)
- [LitServe Documentation](https://lightning.ai/docs/litserve/home)

---

## 🤝 Contributing

We welcome contributions! Check out our [Contributing Guidelines](../CONTRIBUTING.md) to learn how to get involved.

---

## 📜 License

This project is licensed under the [Apache License 2.0](../LICENSE).

---

Happy coding! 🎉
Built with ❤️ using [LitServe](https://github.com/Lightning-AI/litserve).
