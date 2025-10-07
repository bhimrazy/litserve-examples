import base64
import concurrent.futures
import logging
import os
import re
from io import BytesIO
from typing import List, Tuple

import numpy as np
import requests
import soundfile as sf
from litserve.specs.openai import ChatMessage
from PIL import Image

IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"]
AUDIO_EXTENSIONS = [".wav", ".mp3", ".ogg", ".flac", ".m4a", ".aac"]
VIDEO_EXTENSIONS = [".mp4", ".mkv", ".mov", ".avi", ".flv", ".wmv", ".webm", ".m4v"]


def get_file_extension(filename):
    return os.path.splitext(filename)[1].lower()


def is_image(filename):
    return get_file_extension(filename) in IMAGE_EXTENSIONS


def is_audio(filename):
    return get_file_extension(filename) in AUDIO_EXTENSIONS


def is_video(filename):
    return get_file_extension(filename) in VIDEO_EXTENSIONS


def determine_file_type_and_absolute_path(file_path: str) -> dict:
    """
    Determine the type and absolute path of a file.

    Args:
        file_path (str): The relative or absolute path to the file.

    Returns:
        dict: A dictionary containing the file type and absolute path.

    Raises:
        ValueError: If the file type is unsupported.
    """
    # Convert to absolute path if not a URL
    absolute_path = (
        file_path if file_path.startswith("http") else os.path.abspath(file_path)
    )

    # Determine file type
    if is_image(absolute_path):
        file_type = "image"
    elif is_audio(absolute_path):
        file_type = "audio"
    elif is_video(absolute_path):
        file_type = "video"
    else:
        raise ValueError(f"Unsupported file type: {file_path}")

    return file_type, absolute_path


def get_file_object(file_path: str) -> dict:
    """
    Get the file object for a given file path.

    Args:
        file_path (str): The relative or absolute path to the file.

    """
    file_type, absolute_path = determine_file_type_and_absolute_path(file_path)
    if file_type == "image":
        encoded_image = encode_image(absolute_path)
        return {"type": "image_url", "image_url": {"url": encoded_image}}
    elif file_type == "audio":
        with open(absolute_path, "rb") as f:
            audio_data = base64.b64encode(f.read()).decode("utf-8")
        return {
            "type": "input_audio",
            "input_audio": {"data": audio_data, "format": "wav"},
        }
    else:
        raise ValueError(f"Unsupported file type: {file_path}")


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


def encode_image(image_source, max_size=720):
    """Encode an image to a base64 data URL based object.

    Args:
        image_source (str or Image): The image source. Can be a real image URL, an Image instance, or a base64 URL string.
        max_size (int): The maximum size of the image. Defaults to 720.

    Returns:
    str or None: The base64-encoded data URL of the image if successful, otherwise None.
    """
    try:
        image = Image.open(image_source).convert("RGB")

        if max(image.size) > max_size:
            w, h = image.size
            if w > h:
                new_w = max_size
                new_h = int(h * max_size / w)
            else:
                new_h = max_size
                new_w = int(w * max_size / h)
            image = image.resize((new_w, new_h), resample=Image.BICUBIC)

        buffered = BytesIO()
        # Use image format or default to "JPEG"
        image_format = image.format if image.format else "JPEG"
        image.save(buffered, format=image_format)
        mime_type = f"image/{image_format.lower()}"
        encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
        url = f"data:{mime_type};base64,{encoded_image}"
        return url
    except Exception as e:
        print(f"Error encoding image: {e}")
        return None
