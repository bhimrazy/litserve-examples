from typing import List, Literal, Union

from pydantic import BaseModel, HttpUrl


class TextInput(BaseModel):
    text: str


class ImageInput(BaseModel):
    image: HttpUrl


class EmbeddingRequest(BaseModel):
    input: Union[str, List[Union[str, TextInput, ImageInput]]]
    model: Literal["jina-clip-v2"]
    encoding_format: Literal["float"] = "float"
    dimensions: int = 512
    normalized: bool = True


# Model to represent a single embedding
class Embedding(BaseModel):
    embedding: List[float]
    index: int
    object: Literal["embedding"] = "embedding"


# Model to represent usage statistics
class Usage(BaseModel):
    prompt_tokens: int = -1
    total_tokens: int = -1


# Response model for embedding request
class EmbeddingResponse(BaseModel):
    data: List[Embedding]
    model: Literal["jina-clip-v2"]
    object: Literal["list"] = "list"
    usage: Usage
