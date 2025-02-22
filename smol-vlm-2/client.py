import argparse
import json
from typing import Dict, Generator, List, Optional, Union

import requests
from utils import determine_file_type_and_absolute_path


def chat(
    messages: List[Dict[str, Union[str, List[Dict[str, str]]]]],
    model: str = None,
    max_completion_tokens: Optional[int] = None,
    response_format: Optional[Dict[str, str]] = None,
    seed: Optional[int] = None,
    temperature: float = 0.7,
    tools: Optional[List[Dict[str, Union[str, dict]]]] = None,
    stream: bool = False,
    base_url="http://127.0.0.1:8000/v1",
    api_key="lit",
) -> Optional[Union[str, List[str], Generator[str, None, None]]]:
    """
    Sends a chat request to the model API and returns the streaming response.

    # Hamel also has a similar fn:
    https://github.com/hamelsmu/hamel-site/blob/master/notes/llm/openai/tools.py

    Args:
        messages (List[Dict[str, Union[str, List[Dict[str, str]]]]]): Conversation history with roles and content.
        model (str): Model identifier (default: None).
        max_completion_tokens (Optional[int]): Maximum number of completion tokens (default: None).
        response_format (Optional[Dict[str, str]]): Format for the response (default: None).
        seed (Optional[int]): Random seed for reproducibility (default: None).
        temperature (float): Sampling temperature (default: 0.7).
        tools (Optional[List[Dict]]): Optional tools/plugins for the model.
        stream (bool): Stream the response (default: False).
        base_url (str): API endpoint base URL.
        api_key (str): API key for authentication.

    Returns:
        Optional[str]: Model response as a string, or None if an error occurs.
    """
    try:
        if not base_url or not api_key:
            raise ValueError("Base URL and API key are required.")

        if not messages:
            raise ValueError("Messages are required.")

        response = requests.post(
            url=f"{base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "messages": messages,
                "model": model,
                "max_completion_tokens": max_completion_tokens,
                "response_format": response_format,
                "seed": seed,
                "temperature": temperature,
                "tools": tools,
                "stream": stream,
            },
        )
        response.raise_for_status()
        if stream:
            for chunk in response.iter_content(chunk_size=None):
                if chunk:
                    decoded_chunk = chunk.decode("utf-8")
                    # Split the chunk into individual lines
                    lines = decoded_chunk.splitlines()
                    for line in lines:
                        line = line.strip()
                        if line.startswith("data: ") and line.strip() != "data: [DONE]":
                            json_str = line[6:].strip()  # Remove "data: " prefix
                            chunk_data = json.loads(json_str)
                            yield chunk_data
        else:
            return response.json()["choices"][0]["message"]["content"]
    except requests.RequestException as e:
        print(f"Request error: {e}")
    except KeyError:
        print("Unexpected response format.")
    return None


def send_request(file_path: str, prompt: str, max_tokens: int) -> None:
    file_type, path = determine_file_type_and_absolute_path(file_path)
    stream = chat(
        model="smol-vlm-2",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": [
                    {"type": file_type, "url": path},
                    {"type": "text", "text": prompt},
                ],
            },
        ],
        max_completion_tokens=max_tokens,
        temperature=0.7,
        stream=True,
    )
    for chunk in stream:
        print(
            f"\033[92m{chunk['choices'][0]['delta']['content'] or ''}\033[0m",
            end="",
            flush=True,
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
