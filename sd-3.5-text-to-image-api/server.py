from io import BytesIO

import torch
from diffusers import (
    BitsAndBytesConfig,
    SD3Transformer2DModel,
    StableDiffusion3Pipeline,
)
from fastapi import Response
from litserve import LitAPI, LitServer
from pydantic import BaseModel


class ImageGenerationRequest(BaseModel):
    prompt: str
    num_inference_steps: int = 40
    guidance_scale: float = 4.5
    max_sequence_length: int = 512


class StableDiffusionAPI(LitAPI):
    def setup(self, device):
        model_id = "stabilityai/stable-diffusion-3.5-medium"
        nf4_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
        )
        model_nf4 = SD3Transformer2DModel.from_pretrained(
            model_id,
            subfolder="transformer",
            quantization_config=nf4_config,
            torch_dtype=torch.bfloat16,
        )

        self.pipe = StableDiffusion3Pipeline.from_pretrained(
            model_id, transformer=model_nf4, torch_dtype=torch.bfloat16
        )
        self.pipe = self.pipe.to(device)

    def decode_request(self, request: ImageGenerationRequest, context: dict):
        prompt = request.prompt
        context["generation_kwargs"] = {
            "num_inference_steps": request.num_inference_steps,
            "guidance_scale": request.guidance_scale,
            "max_sequence_length": request.max_sequence_length,
        }
        return prompt

    def predict(self, prompt: str, context: dict):
        generation_kwargs = context["generation_kwargs"]
        with torch.no_grad():
            images = self.pipe(prompt, **generation_kwargs).images
            image = images[0]
        return image

    def encode_response(self, image):
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return Response(
            content=buffered.getvalue(), headers={"Content-Type": "image/png"}
        )


if __name__ == "__main__":
    api = StableDiffusionAPI()
    server = LitServer(api, api_path="/generate", timeout=False)
    server.run(port=8000)
