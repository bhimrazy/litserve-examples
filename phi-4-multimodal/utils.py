import base64
import concurrent.futures
import logging
import re
from io import BytesIO
from typing import List, Tuple

import numpy as np
import requests
import soundfile as sf
from litserve.specs.openai import ChatMessage
from PIL import Image


def read_image(source):
    """
    Read an image from a real image URL or a base64-encoded URL.

    Parameters:
    source (str): The image source. Can be a real image URL or a base64 URL string.

    Returns:
    Image or None: The Image object if the source is valid, otherwise None.
    """
    try:
        if re.match(r"^https?://", source):
            # It's a real image URL
            return Image.open(requests.get(source, stream=True).raw).convert("RGB")
        elif re.match(r"^data:image/.+;base64,", source):
            # It's a base64 image URL
            base64_image = source.split(",")[1]
            image_data = base64.b64decode(base64_image)
            return Image.open(BytesIO(image_data)).convert("RGB")
        else:
            return Image.open(source).convert("RGB")
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def process_image(image_url: str, max_height: int = 720):
    """Decode image URL or base64 image, resize if needed, and return a PIL Image object."""
    try:
        image = read_image(image_url)

        # Resize while maintaining aspect ratio if height exceeds MAX_HEIGHT
        width, height = image.size
        if height > max_height:
            new_width = int((max_height / height) * width)
            image = image.resize((new_width, max_height))
        return image
    except Exception as e:
        print(f"Error processing image: {e}")
        return None


def process_audio(audio: str) -> Tuple[np.ndarray, int]:
    """Decode base64-encoded audio and return the waveform data and sample rate."""
    try:
        audio_bytes = base64.b64decode(audio)  # Decode base64 audio
        audio_array, sample_rate = sf.read(BytesIO(audio_bytes))  # Read audio
        return audio_array, sample_rate
    except Exception as e:
        print(f"Error processing audio: {e}")
        return np.array([]), 0  # Return empty array and invalid sample rate on error


def process_in_parallel(func, data: List[str], max_workers: int = 16):
    """Process a list of data in parallel using ThreadPoolExecutor."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        return list(executor.map(func, data))


def parse_messages(req_messages: List[ChatMessage]):
    """
    Parse messages and also extract images and audio data from the messages.
    """
    messages = []
    images = []
    audios = []
    img_count = 1
    audio_count = 1
    for message in req_messages:
        content = message.content
        prompt = ""
        placeholder = ""

        if isinstance(content, list):
            for content_item in message.content:
                if content_item.type == "text":
                    prompt = content_item.text
                elif content_item.type == "image_url":
                    # Ensure the image URL is extracted correctly
                    url = (
                        content_item.image_url
                        if isinstance(content_item.image_url, str)
                        else content_item.image_url.url
                    )
                    images.append(url)
                    placeholder += f"<|image_{img_count}|>"
                    img_count += 1
                elif content_item.type == "input_audio":
                    # Ensure audio data is valid before appending
                    if hasattr(content_item.input_audio, "data"):
                        audios.append(content_item.input_audio.data)
                        placeholder += f"<|audio_{audio_count}|>"
                        audio_count += 1
                    else:
                        logging.warning(f"Audio data missing for item {content_item}")

            # Combine placeholder and text prompt
            content = placeholder + prompt

        messages.append({"role": message.role, "content": content})

    # Process images and audios in parallel
    images = process_in_parallel(process_image, images)
    audios = process_in_parallel(process_audio, audios)

    images = images if images else None
    audios = audios if audios else None

    return messages, images, audios
