import argparse

from openai import OpenAI
from utils import get_file_object

client = OpenAI(
    base_url="http://127.0.0.1:8000/v1",
    api_key="lit",
)


def send_request(file_path: str, prompt: str, max_tokens: int) -> None:
    encoded_file_object = get_file_object(file_path)
    stream = client.chat.completions.create(
        model="microsoft/Phi-4-multimodal-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    encoded_file_object,
                    {"type": "text", "text": prompt},
                ],
            }
        ],
        max_tokens=max_tokens,
        stream=True,
    )
    for chunk in stream:
        print(
            f"\033[92m{chunk.choices[0].delta.content or ''}\033[0m", end="", flush=True
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Send request to SmolVLM2 API server and receive a response."
    )
    parser.add_argument(
        "--file_path", required=True, help="Path for the image or video file"
    )
    parser.add_argument("--prompt", required=True, help="Prompt about the image")
    parser.add_argument(
        "--max_tokens", type=int, default=1024, help="Max tokens for completion"
    )
    args = parser.parse_args()

    send_request(args.file_path, args.prompt, args.max_tokens)
