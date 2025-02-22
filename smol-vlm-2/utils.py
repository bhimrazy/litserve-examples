import base64
import os
from io import BytesIO
from typing import Dict, List
from models import ChatMessage

from PIL import Image

IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"]
VIDEO_EXTENSIONS = [".mp4", ".mkv", ".mov", ".avi", ".flv", ".wmv", ".webm", ".m4v"]


def get_file_extension(filename):
    return os.path.splitext(filename)[1].lower()


def is_image(filename):
    return get_file_extension(filename) in IMAGE_EXTENSIONS


def all_images(files):
    return all(is_image(file.name) for file in files)


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
    elif is_video(absolute_path):
        file_type = "video"
    else:
        raise ValueError(f"Unsupported file type: {file_path}")

    return file_type, absolute_path


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


def format_messages(
    messages: List[ChatMessage],
) -> List[Dict[str, List[Dict[str, str]]]]:
    """
    Format messages for tokenization.
    """
    _messages = []
    for message in messages:
        if isinstance(message.content, str):
            # If the message content is a string, format it accordingly
            formatted_message = {
                "role": message.role,
                "content": [{"type": "text", "text": message.content}],
            }
        else:
            content = []
            for item in message.content:
                if item.type in ("image", "video"):
                    path = item.url or (
                        item.image_url
                        if isinstance(item.image_url, str)
                        else item.image_url.url
                    )
                    content.append({"type": item.type, "path": path})
                else:
                    content.append({"type": "text", "text": item.text})
            formatted_message = {
                "role": message.role,
                "content": content,
            }

        _messages.append(formatted_message)

    return _messages
