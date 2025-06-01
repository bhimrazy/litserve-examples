import base64
import io
import re
import tempfile
from typing import Optional, Tuple

import requests
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS
from fastapi.responses import Response
from litserve import LitAPI, LitServer
from pydantic import BaseModel, Field, field_validator


class TTSRequest(BaseModel):
    text: str = Field(
        ..., min_length=1, max_length=500, description="Input text to synthesize"
    )
    audio_prompt: Optional[str] = Field(
        None, description="Base64 audio, URL, or file path"
    )
    exaggeration: float = Field(0.5, ge=0.0, le=1.0)
    cfg: float = Field(0.5, ge=0.0, le=1.0)
    temperature: float = Field(0.8, ge=0.0, le=1.0)

    @field_validator("audio_prompt")
    def validate_audio_prompt(cls, v):
        if v is None:
            return v

        is_url = re.match(r"^https?://", v)
        is_base64 = re.match(r"^[A-Za-z0-9+/=]+\Z", v)

        if is_url or is_base64:
            return v

        raise ValueError(
            "audio_prompt must be a base64 string or a valid http/https URL"
        )

    def get_audio_tempfile(self) -> Optional[tempfile.NamedTemporaryFile]:
        if self.audio_prompt is None:
            return None

        if re.match(r"^https?://", self.audio_prompt):
            # Download from URL
            resp = requests.get(self.audio_prompt)
            resp.raise_for_status()
            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".audio")
            tmp_file.write(resp.content)
            tmp_file.flush()
            return tmp_file

        # Assume base64 string
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".audio")
        padded = self.audio_prompt + "=" * (-len(self.audio_prompt) % 4)
        decoded = base64.b64decode(padded)
        tmp_file.write(decoded)
        tmp_file.flush()
        return tmp_file


class ChatterboxTTSAPI(LitAPI):
    """
    LitServe API for Chatterbox TTS model.
    Supports both text-to-speech and voice cloning with audio prompts.
    """

    def setup(self, device):
        """Initialize the Chatterbox TTS model."""
        self.model = ChatterboxTTS.from_pretrained(device=device)

    def decode_request(self, request: TTSRequest) -> Tuple:
        """Decode request using TTSRequest model."""
        text, exaggeration, cfg, temperature = request
        audio_prompt = request.get_audio_tempfile()
        return text, audio_prompt, exaggeration, cfg, temperature

    def predict(self, inputs: Tuple) -> bytes:
        """Generate speech audio using Chatterbox TTS."""
        text, audio_prompt, exaggeration, cfg, temperature = inputs
        wav = self.model.generate(
            text,
            audio_prompt_path=audio_prompt,
            exaggeration=exaggeration,
            cfg_weight=cfg,
            temperature=temperature,
        )
        # Convert to bytes
        buffer = io.BytesIO()
        ta.save(buffer, wav, self.model.sr, format="wav")
        audio_bytes = buffer.getvalue()
        return audio_bytes

    def encode_response(self, output: bytes) -> Response:
        """Package the generated audio data into a response."""
        return Response(
            content=output,
            headers={
                "Content-Type": "audio/wav",
                "Content-Disposition": "attachment; filename=generated_speech.wav",
            },
        )


if __name__ == "__main__":
    # Set up API service and server
    api = ChatterboxTTSAPI()
    server = LitServer(api, accelerator="auto", api_path="/speech", timeout=100)
    server.run(port=8000)
