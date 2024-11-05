import torch
from litserve import LitServer, LitAPI
from diffusers import StableDiffusion3Pipeline
from pydantic import BaseModel
from io import BytesIO
from fastapi import Response


class ImageGenerationRequest(BaseModel):
    prompt: str
    num_inference_steps: int = 40
    guidance_scale: float = 4.5
    max_sequence_length: int = 512


class StableDiffusionAPI(LitAPI):
    def setup(self, device):
        self.pipe = StableDiffusion3Pipeline.from_pretrained(
            "stabilityai/stable-diffusion-3.5-medium", torch_dtype=torch.bfloat16
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
