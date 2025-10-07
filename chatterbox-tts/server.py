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
        is_base64 = (
            re.match(r"^[A-Za-z0-9+/=]+\Z", v) and len(v) > 100
        )  # Basic base64 check

        if is_url or is_base64:
            return v

        raise ValueError("audio_prompt must be a base64 string or valid http/https URL")

    def get_audio_tempfile(self) -> Optional[str]:
        if self.audio_prompt is None:
            return None

        if re.match(r"^https?://", self.audio_prompt):
            # Download from URL
            resp = requests.get(self.audio_prompt)
            resp.raise_for_status()
            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            tmp_file.write(resp.content)
            tmp_file.close()
            return tmp_file.name

        if (
            re.match(r"^[A-Za-z0-9+/=]+\Z", self.audio_prompt)
            and len(self.audio_prompt) > 100
        ):
            # Base64 string
            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            padded = self.audio_prompt + "=" * (-len(self.audio_prompt) % 4)
            decoded = base64.b64decode(padded)
            tmp_file.write(decoded)
            tmp_file.close()
            return tmp_file.name

        # Assume local file path
        return self.audio_prompt


class ChatterboxTTSAPI(LitAPI):
    """
    LitServe API for Chatterbox TTS model.
    Supports both text-to-speech and voice cloning with audio prompts.
    """

    def setup(self, device):
        """Initialize the Chatterbox TTS model."""
        self.model = ChatterboxTTS.from_pretrained(device=device)
        self.temp_files = []  # Track temp files for cleanup

    def decode_request(self, request: TTSRequest) -> Tuple:
        """Decode request using TTSRequest model."""
        audio_prompt_path = request.get_audio_tempfile()

        # Track temp files for cleanup
        if audio_prompt_path and audio_prompt_path != request.audio_prompt:
            self.temp_files.append(audio_prompt_path)

        return (
            request.text,
            audio_prompt_path,
            request.exaggeration,
            request.cfg,
            request.temperature,
        )

    def predict(self, inputs: Tuple) -> bytes:
        """Generate speech audio using Chatterbox TTS."""
        text, audio_prompt_path, exaggeration, cfg, temperature = inputs

        try:
            wav = self.model.generate(
                text,
                audio_prompt_path=audio_prompt_path,
                exaggeration=exaggeration,
                cfg_weight=cfg,
                temperature=temperature,
            )
            # Convert to bytes
            buffer = io.BytesIO()
            ta.save(buffer, wav, self.model.sr, format="wav")
            audio_bytes = buffer.getvalue()
            return audio_bytes
        finally:
            # Clean up temp files
            self._cleanup_temp_files()

    def _cleanup_temp_files(self):
        """Clean up temporary files."""
        import os

        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
            except OSError:
                pass
        self.temp_files.clear()

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
    api = ChatterboxTTSAPI(api_path="/speech")
    server = LitServer(api, accelerator="auto", timeout=100)
    server.run(port=8000)
