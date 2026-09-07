<div align='center'>
<h1>
  LitServe Examples
  <br/>
  Production-Ready AI Model Serving Made Simple
</h1>
</div>

**Production-grade examples** showcasing the power and versatility of [LitServe](https://github.com/Lightning-AI/litserve) - Lightning AI's high-performance model serving engine. From speech recognition to multimodal LLMs, learn how to deploy AI models at scale with minimal code.

Build production APIs that handle thousands of requests per second, with built-in batching, streaming, and auto-scaling.

&#160;

<div align='center'>
<pre>
✅ Production-Ready Examples    ✅ Real-World Use Cases     ✅ Minimal Setup Required
✅ Lightning Fast Inference     ✅ Enterprise Features      ✅ Open Source & Free
</pre>
</div>  

<div align='center'>

[![CI](https://github.com/bhimrazy/litserve-examples/actions/workflows/ci.yml/badge.svg)](https://github.com/bhimrazy/litserve-examples/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/bhimrazy/litserve-examples/blob/main/LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/bhimrazy/litserve-examples?style=social)](https://github.com/bhimrazy/litserve-examples/stargazers)
[![Discussions](https://img.shields.io/github/discussions/bhimrazy/litserve-examples?label=Start%20Discussion)](https://github.com/bhimrazy/litserve-examples/discussions)

</div>

<p align="center">
  <a href="#-quick-start">Quick start</a> •
  <a href="#-featured-examples">Examples</a> •
  <a href="#-use-cases">Use Cases</a> •
  <a href="#-why-litserve">Why LitServe</a> •
  <a href="#-community">Community</a> •
  <a href="https://lightning.ai/docs/litserve">Docs</a>
</p>

______________________________________________________________________

## 🚀 Quick Start

Get your first AI API running in under 2 minutes:

```bash
# Clone and enter any example
git clone https://github.com/bhimrazy/litserve-examples.git
cd litserve-examples/whisper-stt-api

# Install and run
pip install -r requirements.txt
python server.py

# Your API is live at http://localhost:8000! 🎉
```

**Test it instantly:**
```bash
curl -X POST "http://localhost:8000/transcribe" -F "audio=@path/to/your/audio/file"
```

> 💡 **Each example is self-contained** in its own folder with complete setup instructions. Just `cd` into any example directory and follow its README for detailed guidance, customization options, and advanced features.

<br/>

## 🎯 Featured Examples

### 🗣️ Speech & Audio APIs
Perfect for building conversational AI, transcription services, and voice interfaces.

| Example                                                                                                                           | Description                                         | Use Cases                                          | Complexity          |
| --------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- | -------------------------------------------------- | ------------------- |
| [**🎤 Whisper STT API**](./whisper-stt-api/)                                                                                       | OpenAI Whisper speech recognition                   | Meeting transcripts, voice commands, accessibility | **Beginner** ⭐      |
| [**📢 Parler TTS**](https://lightning.ai/bhimrajyadav/studios/deploy-a-speech-generation-api-using-parler-tts-powered-by-litserve) | High-quality text-to-speech synthesis               | Content creation, narration, chatbots              | **Intermediate** ⭐⭐ |
| [**🔊 Chatterbox TTS**](./chatterbox-tts/)                                                                                         | Production TTS with voice cloning & emotion control | Voice assistants, audiobooks, personalization      | **Advanced** ⭐⭐⭐    |

### 🤖 Conversational AI & LLMs  
Build intelligent chatbots and multimodal AI assistants.

| Example                                                                               | Description                                | Use Cases                                  | Complexity          |
| ------------------------------------------------------------------------------------- | ------------------------------------------ | ------------------------------------------ | ------------------- |
| [**🦙 Llama 3.2 Vision Chat**](https://github.com/bhimrazy/chat-with-llama-3.2-vision) | Multimodal chat with vision understanding  | Visual Q&A, image analysis, document AI    | **Advanced** ⭐⭐⭐    |
| [**🔍 Qwen2-VL Chat**](https://github.com/bhimrazy/chat-with-qwen2-vl)                 | Advanced vision-language interactions      | Visual reasoning, OCR, scene understanding | **Advanced** ⭐⭐⭐    |
| [**🧠 DeepSeek R1**](./deepseek-r1/)                                                   | Interactive AI with reasoning capabilities | Customer support, research assistance      | **Intermediate** ⭐⭐ |

### 📊 Embeddings & Search APIs
Power semantic search, RAG systems, and recommendation engines.

| Example                                                 | Description                         | Use Cases                                  | Complexity          |
| ------------------------------------------------------- | ----------------------------------- | ------------------------------------------ | ------------------- |
| [**⚡ OpenAI-Compatible Embeddings**](./embeddings-api/) | Production embeddings with batching | RAG systems, similarity search, clustering | **Beginner** ⭐      |
| [**🎯 Jina CLIP v2**](./jina-clip-v2/)                   | Multilingual multimodal embeddings  | Image search, cross-modal retrieval        | **Intermediate** ⭐⭐ |
| [**🚀 ModernBERT Embeddings**](./modernbert-embed/)      | State-of-the-art text embeddings    | Document search, recommendation systems    | **Intermediate** ⭐⭐ |

### 👁️ Computer Vision APIs
Deploy object detection, image analysis, and visual AI models.

| Example                                                      | Description                           | Use Cases                                         | Complexity       |
| ------------------------------------------------------------ | ------------------------------------- | ------------------------------------------------- | ---------------- |
| [**📷 Image Recognition**](./image-recognition-api/)          | General-purpose image classification  | Content moderation, auto-tagging, quality control | **Beginner** ⭐   |
| [**🎯 RF-DETR Object Detection**](./rfdetr-object-detection/) | Real-time object detection & tracking | Security, retail analytics, autonomous systems    | **Advanced** ⭐⭐⭐ |

<br/>

## 💼 Use Cases

### 🏢 Enterprise & Production
- **Customer Service**: Deploy AI chatbots that handle voice, text, and images
- **Content Automation**: Build TTS systems for audiobooks, training materials  
- **Document Intelligence**: Extract insights from PDFs, images, and scanned documents
- **Quality Assurance**: Automated visual inspection and defect detection

### 🚀 Startups & Innovation
- **MVP Development**: Rapid prototyping of AI-powered products
- **Market Validation**: Quick deployment for user testing and feedback
- **Cost Optimization**: Scale from zero to production without infrastructure overhead
- **Competitive Edge**: Deploy latest models faster than competitors

### 🎓 Research & Education  
- **Model Experimentation**: Easy deployment for A/B testing different models
- **Academic Research**: Serve models for research collaborations and demos
- **Educational Tools**: Interactive AI applications for learning and teaching
- **Open Source Contribution**: Share reproducible AI research with the community

<br/>

## ⚡ Why LitServe?

**Build your own inference engine with complete control.** Unlike rigid serving platforms like vLLM that lock you into specific model types, LitServe gives you the flexibility to serve **any model** - vision, audio, text, or multi-modal - exactly the way you want.

### 🎯 Unmatched Flexibility
- **🧠 Any Model Type**: LLMs, computer vision, audio processing, multi-modal
- **⚙️ Custom Logic**: Define exactly how inference works with your business rules
- **🔧 Full Control**: Batching, caching, streaming, routing, and orchestration
- **🏗️ Multiple Use Cases**: APIs, agents, chatbots, MCP servers, RAG pipelines

### 🚀 Production-Ready Performance
```python
# Simple yet powerful - serve any model in 3 lines
class MyAPI(LitAPI):
    def predict(self, x):
        return self.model(x)  # Your custom logic here


server = LitServer(MyAPI(), accelerator="auto")  # Auto-optimization included!
```

### 🏢 Perfect For
- **🤖 AI Applications**: Chatbots, virtual assistants, content generation
- **🔍 Search & RAG**: Semantic search, retrieval-augmented generation  
- **👁️ Vision Systems**: Object detection, image analysis, OCR
- **🗣️ Audio Processing**: Speech recognition, text-to-speech, audio analysis
- **🧪 Research & Prototyping**: Rapid model deployment and experimentation

**Ready to build something amazing?** → [**Get Started**](#-quick-start) | [**Learn More About LitServe**](https://github.com/Lightning-AI/LitServe?tab=readme-ov-file#why-litserve)

<br/>

## 📚 Learning Path

### 🎯 **Beginner** (New to AI APIs)
1. [**Image Recognition**](./image-recognition-api/) - Start with simple classification
2. [**Embeddings API**](./embeddings-api/) - Learn about vector representations  
3. [**Whisper STT**](./whisper-stt-api/) - Build your first speech API

### ⚡ **Intermediate** (Building Production Systems)  
1. [**ModernBERT Embeddings**](./modernbert-embed/) - Advanced text processing
2. [**Jina CLIP**](./jina-clip-v2/) - Multimodal understanding
3. [**DeepSeek R1**](./deepseek-r1/) - Reasoning and logic

### 🚀 **Advanced** (Enterprise & Scale)
1. [**Chatterbox TTS**](./chatterbox-tts/) - Production voice synthesis
2. [**RF-DETR Detection**](./rfdetr-object-detection/) - Real-time computer vision
3. [**Llama Vision Chat**](https://github.com/bhimrazy/chat-with-llama-3.2-vision) - Multimodal conversations

<br/>

## 📖 Documentation
Explore the following documentation to learn more about how to use LitServe effectively:

- [Getting Started Guide](https://lightning.ai/docs/litserve/home/get-started)
- [Installation Guide](https://lightning.ai/docs/litserve/home/install)
- [Advanced Features](https://lightning.ai/docs/litserve/features)
- [Speed up serving by 200x](https://lightning.ai/docs/litserve/home/speed-up-serving-by-200x)

## 🤝 Community

### 💬 Get Help & Connect
- 💬 [Start Discussion](https://github.com/bhimrazy/litserve-examples/discussions) - Ask questions and share ideas
- 🐛 [Report Issues](https://github.com/bhimrazy/litserve-examples/issues) - Found a bug? Let us know
- 💡 [Feature Requests](https://github.com/bhimrazy/litserve-examples/discussions/categories/ideas) - Suggest new examples
- 📧 [Lightning AI Discord](https://discord.gg/WajDThKAur) - Join the broader Lightning community

## 🤝 Contributing
We welcome contributions from the community! If you'd like to contribute to this repository, please read our [Contributing Guidelines](./CONTRIBUTING.md) to get started.


## 📜 License

This project is licensed under the [Apache License 2.0](./LICENSE) - feel free to use in commercial and open source projects.

---

*Ready to deploy your first AI API? [Get started now!](#-quick-start)*
