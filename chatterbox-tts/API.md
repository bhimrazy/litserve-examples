# Chatterbox TTS API Documentation

## Overview

The Chatterbox TTS API provides high-quality text-to-speech synthesis with advanced features including voice cloning and emotion control. Built on top of Resemble AI's open-source Chatterbox model and powered by LitServe for optimal performance.

## Base URL

```
http://localhost:8000
```

## Endpoints

### Health Check

**GET** `/health`

Check if the API server is running and healthy.

**Response:**
```json
{
  "status": "healthy",
  "model": "Chatterbox TTS",
  "api_path": "/speech"
}
```

### Text-to-Speech Generation

**POST** `/speech`

Generate speech audio from text with optional voice cloning and emotion control.

**Request Body:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `text` | string | ✅ | - | Text to synthesize (max 5000 characters) |
| `audio_prompt_path` | string | ❌ | - | Path to reference audio file for voice cloning |
| `audio_prompt_base64` | string | ❌ | - | Base64 encoded reference audio for voice cloning |
| `exaggeration` | float | ❌ | 0.5 | Emotion intensity control (0.0-1.0) |
| `cfg` | float | ❌ | 0.5 | Generation quality control (0.0-1.0) |
| `speed` | float | ❌ | 1.0 | Speech speed control (0.1-3.0) |

**Response:**
- **Content-Type:** `audio/wav`
- **Body:** Binary audio data in WAV format

**Example Requests:**

#### Basic Text-to-Speech

```bash
curl -X POST http://localhost:8000/speech \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello! This is a test of the Chatterbox TTS API."
  }' \
  --output output.wav
```

```python
import requests

url = "http://localhost:8000/speech"
data = {
    "text": "Hello! This is a test of the Chatterbox TTS API."
}

response = requests.post(url, json=data)
with open("output.wav", "wb") as f:
    f.write(response.content)
```

#### Expressive Speech

```python
data = {
    "text": "Wow! This is absolutely amazing!",
    "exaggeration": 0.8,  # High emotion
    "cfg": 0.3,           # Better pacing for expressive speech
    "speed": 0.9          # Slightly slower for drama
}

response = requests.post(url, json=data)
```

#### Voice Cloning with File Path

```python
data = {
    "text": "This will sound like the reference speaker!",
    "audio_prompt_path": "/path/to/reference/audio.wav",
    "exaggeration": 0.6,
    "cfg": 0.4
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
    "audio_prompt_base64": audio_base64,
    "exaggeration": 0.6,
    "cfg": 0.4
}

response = requests.post(url, json=data)
```

## Parameter Guidelines

### Exaggeration Control

Controls the emotional intensity and expression in the generated speech:

- **0.0-0.3**: Calm, neutral tone
- **0.4-0.6**: Natural, moderate expression (recommended for most use cases)
- **0.7-0.9**: Highly expressive, dramatic speech
- **0.9-1.0**: Maximum emotion (use carefully)

### CFG (Classifier-Free Guidance)

Controls generation quality and pacing:

- **0.1-0.3**: Faster, more natural pacing (good for expressive speech)
- **0.4-0.6**: Balanced quality and speed (default recommendation)
- **0.7-1.0**: Higher quality, slower generation

### Speed Control

Controls speech rate:

- **0.1-0.7**: Slower speech (good for clarity)
- **0.8-1.2**: Normal speed range
- **1.3-3.0**: Faster speech

## Best Practices

### General Use Cases

For most applications (chatbots, voice agents, general TTS):
```json
{
  "exaggeration": 0.5,
  "cfg": 0.5,
  "speed": 1.0
}
```

### Expressive Content

For dramatic content, storytelling, or emotional speech:
```json
{
  "exaggeration": 0.7,
  "cfg": 0.3,
  "speed": 0.9
}
```

### Fast Speaking Style

If your reference speaker has a fast speaking style:
```json
{
  "cfg": 0.3
}
```

### Voice Cloning Tips

1. **Reference Audio Quality:**
   - Use clear, high-quality audio (16kHz+ sample rate recommended)
   - Avoid background noise
   - 3-10 seconds of speech is usually sufficient

2. **Parameter Adjustment:**
   - Start with lower `cfg` values (0.3-0.4) for voice cloning
   - Adjust `exaggeration` based on the reference speaker's style

## Error Handling

The API returns appropriate HTTP status codes and error messages:

### 400 Bad Request

```json
{
  "detail": "Text is required for speech synthesis and cannot be empty"
}
```

Common validation errors:
- Empty or missing text
- Text too long (>5000 characters)
- Invalid parameter ranges
- Invalid base64 audio data

### 500 Internal Server Error

```json
{
  "detail": "Error generating speech: [error details]"
}
```

Server-side errors:
- Model loading failures
- Audio generation errors
- System resource issues

## Rate Limits

Default configuration allows:
- 60 requests per minute per client
- Maximum 120 seconds timeout per request
- Maximum 5000 characters per text input
- Maximum 10MB audio file size

## Audio Output Format

- **Format:** WAV (Waveform Audio File Format)
- **Sample Rate:** 24kHz (model default)
- **Bit Depth:** 16-bit
- **Channels:** Mono
- **Encoding:** PCM

## Security Features

### Watermarking

All generated audio includes Resemble AI's Perth watermarking for responsible AI usage. The watermarks are:
- Imperceptible to human listeners
- Survive MP3 compression and audio editing
- Near 100% detection accuracy

### Input Validation

- Text length limits prevent abuse
- Audio file size limits prevent memory issues
- Parameter range validation ensures stable generation

## Performance Considerations

### Response Times

Typical response times (on modern hardware):
- Short text (< 50 chars): 2-5 seconds
- Medium text (50-200 chars): 5-15 seconds  
- Long text (200+ chars): 15-60 seconds
- Voice cloning: +20-50% overhead

### Concurrent Requests

The API handles requests sequentially by default. For higher throughput:
- Deploy multiple instances behind a load balancer
- Use queue-based processing for batch jobs

### Resource Usage

- **CPU Mode:** 2-4 GB RAM, 2+ CPU cores
- **GPU Mode:** 4-8 GB VRAM, CUDA-compatible GPU
- **Storage:** Model cache requires ~1-2 GB

## SDK Examples

### Python SDK

```python
import requests
import base64
from pathlib import Path

class ChatterboxTTSClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.speech_url = f"{base_url}/speech"
    
    def generate_speech(self, text, **kwargs):
        """Generate speech from text."""
        data = {"text": text, **kwargs}
        response = requests.post(self.speech_url, json=data)
        response.raise_for_status()
        return response.content
    
    def clone_voice(self, text, reference_audio_path, **kwargs):
        """Generate speech with voice cloning."""
        with open(reference_audio_path, "rb") as f:
            audio_data = f.read()
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        data = {
            "text": text,
            "audio_prompt_base64": audio_base64,
            **kwargs
        }
        
        response = requests.post(self.speech_url, json=data)
        response.raise_for_status()
        return response.content

# Usage
client = ChatterboxTTSClient()

# Basic TTS
audio = client.generate_speech("Hello world!")
Path("output.wav").write_bytes(audio)

# Voice cloning
audio = client.clone_voice(
    "This sounds like the reference!",
    "reference.wav",
    exaggeration=0.6
)
Path("cloned_output.wav").write_bytes(audio)
```

### JavaScript SDK

```javascript
class ChatterboxTTSClient {
    constructor(baseUrl = 'http://localhost:8000') {
        this.baseUrl = baseUrl;
        this.speechUrl = `${baseUrl}/speech`;
    }
    
    async generateSpeech(text, options = {}) {
        const response = await fetch(this.speechUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text, ...options })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.arrayBuffer();
    }
    
    async cloneVoice(text, referenceAudioFile, options = {}) {
        const audioData = await this.fileToBase64(referenceAudioFile);
        
        const response = await fetch(this.speechUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text,
                audio_prompt_base64: audioData,
                ...options
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.arrayBuffer();
    }
    
    fileToBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => {
                const base64 = reader.result.split(',')[1];
                resolve(base64);
            };
            reader.onerror = error => reject(error);
        });
    }
}

// Usage
const client = new ChatterboxTTSClient();

// Basic TTS
const audio = await client.generateSpeech("Hello world!");
const blob = new Blob([audio], { type: 'audio/wav' });
const url = URL.createObjectURL(blob);

// Play audio
const audioElement = new Audio(url);
audioElement.play();
```

## Troubleshooting

### Common Issues

1. **"Text is required" error**
   - Ensure the `text` field is included and not empty

2. **"Audio prompt file not found" error**
   - Check the file path in `audio_prompt_path`
   - Use `audio_prompt_base64` for remote deployments

3. **Long response times**
   - Reduce text length
   - Lower `cfg` values for faster generation
   - Use GPU acceleration if available

4. **Audio quality issues**
   - Increase `cfg` for better quality
   - Ensure reference audio is high quality (for voice cloning)
   - Check parameter ranges

### Debug Mode

Enable debug logging by modifying `config.py`:

```python
LOGGING_CONFIG = {
    "level": "DEBUG"
}
```

## Support

For issues and questions:
- Check the [troubleshooting guide](./DEPLOYMENT.md#troubleshooting)
- Run the test suite: `python test_suite.py`
- Review server logs for error details
