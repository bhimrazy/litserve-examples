from model import ImageInput, TextInput


def parse_inputs(
    inputs: str | list[str | TextInput | ImageInput],
) -> tuple[list[str], list[str], list[str]]:
    """Parse the input data into separate lists of text and image URLs.

    Args:
        inputs: Input data, either a string or a list of mixed types (str, TextInput, ImageInput, dict).

    Returns:
        Tuple[List[str], List[str], List[str]]:
        - List of text inputs (sentences).
        - List of image URLs.
        - List of input types (sequence of "text" or "image").
    """
    texts: list[str] = []
    images: list[str] = []
    input_types: list[str] = []

    normalized_inputs = inputs if isinstance(inputs, list) else [inputs]

    for item in normalized_inputs:
        if isinstance(item, str):
            if item.startswith("http"):
                images.append(item)
                input_types.append("image")
            else:
                texts.append(item)
                input_types.append("text")
        elif isinstance(item, TextInput):
            texts.append(item.text)
            input_types.append("text")
        elif isinstance(item, ImageInput):
            images.append(str(item.image))
            input_types.append("image")

    return texts, images, input_types
