from threading import Thread

import litserve as ls
import torch
from models import ChatCompletionRequest
from transformers import (
    AutoModelForImageTextToText,
    AutoProcessor,
    TextIteratorStreamer,
)
from utils import format_messages


class SmolVLM2API(ls.LitAPI):
    def setup(self, device):
        self.device = device
        self.dtype = torch.bfloat16

        model_id = "HuggingFaceTB/SmolVLM2-500M-Video-Instruct"

        self.processor = AutoProcessor.from_pretrained(model_id)
        self.model = AutoModelForImageTextToText.from_pretrained(
            model_id,
            torch_dtype=self.dtype,
            _attn_implementation="flash_attention_2",
        ).to(self.device)

        self.streamer = TextIteratorStreamer(
            self.processor,
            skip_prompt=True,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=True,
        )

    def decode_request(self, request: ChatCompletionRequest, context: dict):
        # Update context with generation arguments
        context["generation_args"] = {
            "temperature": request.temperature or 0.7,
            "max_new_tokens": request.max_completion_tokens or 1024,
        }

        # Prepare messages for tokenization
        messages = format_messages(request.messages)

        # Tokenize messages and prepare input IDs
        inputs = self.processor.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
            # video_load_backend="decord",
        ).to(self.device, self.dtype)

        # Return model inputs
        return inputs

    def predict(self, inputs: dict, context: dict):
        generation_kwargs = dict(
            **inputs,
            streamer=self.streamer,
            do_sample=True,
            eos_token_id=self.processor.tokenizer.eos_token_id,
            pad_token_id=self.processor.tokenizer.pad_token_id,
            **context["generation_args"],
        )
        # Start generation in a separate thread
        generation_thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
        generation_thread.start()

        # Yield generated text from the streamer
        for text in self.streamer:
            # print(f"\033[92m{text or ''}\033[0m", end="", flush=True)
            yield text

        # Ensure the generation thread has finished
        generation_thread.join()


if __name__ == "__main__":
    server = ls.LitServer(SmolVLM2API(), spec=ls.OpenAISpec())
    server.run(port=8000)
