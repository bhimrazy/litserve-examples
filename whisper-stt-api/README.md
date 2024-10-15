# Whisper API

Welcome to the **Whisper API**! This API leverages OpenAI's Whisper model to provide state-of-the-art speech-to-text capabilities. Follow this guide to get started quickly.

## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed:
- Python 3.8+
- `pip` (Python package installer)

### Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/bhimrazy/litserve-examples.git
    cd whisper-stt-api
    ```

2. **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

### Running the Server

1. **Navigate to the API directory:**
    ```sh
    cd whisper-stt-api
    ```

2. **Start the server:**
    ```sh
    python server.py
    ```

The server will start on `http://localhost:8000/transcribe`.

### Making a Request

To transcribe audio, send a POST request to the `/transcribe` endpoint with the audio file. Here's an example using `curl`:

```sh
curl -X POST "http://localhost:8000/transcribe" -F "audio=@path/to/your/audio/file.wav"
```

### Example Response

```json
{
    "text": "This is the transcribed text from the audio."
}
```

## 📚 Documentation

For more detailed information, refer to the following resources:
- [Whisper Documentation](https://github.com/openai/whisper)
- [LitServe Documentation](https://github.com/Lightning-AI/litserve)

## 🤝 Contributing

We welcome contributions from the community! If you'd like to contribute to this project, please read our [Contributing Guidelines](../CONTRIBUTING.md) to get started.

## 📜 License

This project is licensed under the [Apache License](../LICENSE).

---

Happy coding! 🎉