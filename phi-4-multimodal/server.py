from threading import Thread

import litserve as ls
import torch
from litserve.specs.openai import ChatCompletionRequest
from transformers import (
    AutoModelForCausalLM,
    AutoProcessor,
    BitsAndBytesConfig,
    GenerationConfig,
    TextIteratorStreamer,
)

from utils import parse_messages


class Phi4MultimodalAPI(ls.LitAPI):
    def setup(self, device):
        model_path = "microsoft/Phi-4-multimodal-instruct"
        quantization_config = BitsAndBytesConfig(
            # load_in_4bit=True,
            # bnb_4bit_quant_type="nf4",
            # bnb_4bit_compute_dtype=torch.bfloat16,
            # or
            load_in_8bit=True
        )
        self.processor = AutoProcessor.from_pretrained(
            model_path, trust_remote_code=True
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            device_map=device,
            trust_remote_code=True,
            torch_dtype="auto",
            attn_implementation="flash_attention_2",  # eager
            # _attn_implementation="flash_attention_2",
            # quantization_config=quantization_config, # getting error with quantization
        )
        # eval mode
        self.model.eval()

        self.generation_config = GenerationConfig.from_pretrained(model_path)
        self.streamer = TextIteratorStreamer(
            self.processor.tokenizer,
            skip_prompt=True,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False,
        )
        self.device = device

    def decode_request(self, request: ChatCompletionRequest):
        messages, images, audios = parse_messages(request.messages)
        prompt = self.processor.tokenizer.apply_chat_template(
            messages, tools=request.tools, tokenize=False, add_generation_prompt=True
        )
        print("prompt", prompt)
        inputs = self.processor(
            prompt, images=images, audios=audios, return_tensors="pt"
        ).to(self.device)
        return inputs

    def predict(self, inputs, context: dict):
        with torch.no_grad():
            generation_kwargs = dict(
                **inputs,
                streamer=self.streamer,
                do_sample=True,
                generation_config=self.generation_config,
                temperature=context.get("temperature") or 0.7,
                max_new_tokens=context.get("max_new_tokens") or 2048,
            )
            thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
            thread.start()
            for text in self.streamer:
                yield text


if __name__ == "__main__":
    api = Phi4MultimodalAPI()
    server = ls.LitServer(api, spec=ls.OpenAISpec())
    server.run(port=8000, generate_client_file=False)
