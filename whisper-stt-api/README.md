<h1 align="center">Whisper Speech to Text (STT) API</h1>

Welcome to the **Whisper STT API**! This API leverages OpenAI's Whisper model to provide state-of-the-art speech-to-text capabilities. Follow this guide to get started quickly.
> Automatic Speech Recognition (ASR), also known as Speech to Text (STT), is the task of transcribing a given audio to text. It has many applications, such as voice user interfaces.

![image](https://github.com/user-attachments/assets/1e5b83be-7ddc-4920-bf94-fc3fa7a5a68c)

## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed:
- Python 3.8+
- `pip` (Python package installer)

### Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/bhimrazy/litserve-examples.git
    cd litserve-examples/whisper-stt-api
    ```

2. **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

    It also requires the command-line tool ffmpeg to be installed on your system, which is available from most package managers: [Readmore](https://github.com/openai/whisper?tab=readme-ov-file#setup)
    ```sh
    # on Ubuntu or Debian
    sudo apt update && sudo apt install ffmpeg

    # on Arch Linux
    sudo pacman -S ffmpeg

    # on MacOS using Homebrew (https://brew.sh/)
    brew install ffmpeg

    # on Windows using Chocolatey (https://chocolatey.org/)
    choco install ffmpeg

    # on Windows using Scoop (https://scoop.sh/)
    scoop install ffmpeg
    ```



### Running the Server
    ```sh
    python server.py
    ```

The server will start on `http://localhost:8000/transcribe`.

### Making a Request

To transcribe audio, send a POST request to the `/transcribe` endpoint with the audio file. Here's an example using `curl`:

```sh
curl -X POST "http://localhost:8000/transcribe" -F "audio=@path/to/your/audio/file"

# eg: curl -X POST "http://localhost:8000/transcribe" -F "audio=nova.wav"
```

Test using python client
```sh
python client.py -a path/to/your/audio/file
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
