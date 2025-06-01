# Chatterbox TTS API powered by LitServe

A high-performance Text-to-Speech API using [Chatterbox TTS](https://huggingface.co/ResembleAI/chatterbox) model powered by [LitServe](https://github.com/Lightning-AI/litserve).

## Features

- **High-Quality TTS**: Production-grade open source TTS model from Resemble AI
- **Voice Cloning**: Support for zero-shot voice cloning with reference audio
- **Emotion Control**: Built-in exaggeration/intensity control for expressive speech
- **Fast Inference**: Optimized with LitServe for high-performance serving
- **Flexible Input**: Support for both file paths and base64 encoded audio
- **MIT Licensed**: Open source and free to use

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Start the Server

```bash
python server.py
```

The server will start on `http://localhost:8000` with the API endpoint at `/speech`.

### Command Line Client

The easiest way to use the API is with the included command-line client:

```bash
# Basic text-to-speech
python client.py --text "Deploy any AI model, Lightning fast. Focus on models, not serving infrastructure."

# With voice cloning using reference audio
python client.py --text "Clone my voice!" --audio-prompt reference.wav

# Advanced options
python client.py --text "Excited speech!" --audio-prompt reference.wav --cfg 0.3 --exaggeration 0.7 --play
```

**Client Options:**
- `text`: Text to synthesize (required)
- `--audio-prompt`: Audio file path for voice cloning (optional)
- `--output`, `-o`: Output file path (default: output.wav)
- `--play`: Play audio after generation
- `--exaggeration`: Emotion level 0.0-1.0 (default: 0.5)
- `--cfg`: CFG weight 0.0-1.0 (default: 0.5)

### API Usage (Python)

#### Basic Text-to-Speech

```python
import requests

url = "http://127.0.0.1:8000/speech"
data = {
    "text": "Hello! This is a test of the Chatterbox TTS API.",
    "exaggeration": 0.5,  # Default: 0.5
    "cfg": 0.5,           # Default: 0.5  
    "temperature": 0.8    # Default: 0.8
}

response = requests.post(url, json=data)

# Save the output to a file
with open("output.wav", "wb") as f:
    f.write(response.content)
```

#### Voice Cloning with Audio File

```python
data = {
    "text": "This will sound like the reference speaker!",
    "audio_prompt": "path/to/reference/audio.wav",
    "exaggeration": 0.7,
    "cfg": 0.3
}

response = requests.post(url, json=data)
```

#### Voice Cloning with Base64 Audio

```python
import base64

# Read and encode reference audio
with open("reference.wav", "rb") as f:
    audio_data = f.read()
audio_base64 = base64.b64encode(audio_data).decode('utf-8')

data = {
    "text": "Voice cloning with base64 encoded audio!",
    "audio_prompt": audio_base64,
    "exaggeration": 0.6,
    "cfg": 0.4
}

response = requests.post(url, json=data)
```

### Request Parameters

- **text** (required): The text to synthesize
- **audio_prompt** (optional): File path, URL, or base64 encoded reference audio for voice cloning
- **exaggeration** (optional, default 0.5): Controls emotion intensity (0.0-1.0)
- **cfg** (optional, default 0.5): Controls generation quality and pacing
- **temperature** (optional, default 0.8): Controls speech rate and variability

### Tips for Best Results

#### General Use (TTS and Voice Agents)
- Default settings (`exaggeration=0.5`, `cfg=0.5`) work well for most prompts
- If reference speaker has fast speaking style, lower `cfg` to around `0.3`

#### Expressive or Dramatic Speech  
- Try lower `cfg` values (e.g. `~0.3`) and increase `exaggeration` to `0.7` or higher
- Higher `exaggeration` tends to speed up speech; reducing `cfg` helps compensate

## Testing

Run the test client to verify all functionality:

```bash
python client.py
```

This will test:
- Basic text-to-speech
- Expressive speech with high exaggeration
- Voice cloning with file paths
- Voice cloning with base64 audio
- Error handling

## Model Details

- **Model**: ResembleAI/chatterbox (0.5B parameters)
- **Backbone**: Llama architecture
- **Training Data**: 0.5M hours of cleaned audio data
- **Features**: Zero-shot TTS, emotion control, watermarked outputs
- **License**: MIT

## Performance

- **Inference Speed**: Optimized with LitServe for production workloads
- **Batch Processing**: Supports single requests (TTS typically done one at a time)
- **GPU Acceleration**: Automatic device detection (CUDA/MPS/CPU)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the Apache License - see the [LICENSE](../LICENSE) file for details.

## Acknowledgments

- [Chatterbox TTS](https://huggingface.co/ResembleAI/chatterbox) by Resemble AI
- [LitServe](https://github.com/Lightning-AI/litserve) by Lightning AI
