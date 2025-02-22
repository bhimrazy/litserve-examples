from typing import List, Literal, Union

from litserve.specs.openai import (
    ChatCompletionRequest as BaseChatCompletionRequest,
)
from litserve.specs.openai import (
    ChatMessage as BaseChatMessage,
)
from litserve.specs.openai import (
    ImageContent,
    TextContent,
)
from pydantic import BaseModel


class MediaContent(BaseModel):
    type: Literal["image", "audio", "video"]
    url: str


class ChatMessage(BaseChatMessage):
    content: Union[str, List[Union[TextContent, ImageContent, MediaContent]]]


class ChatCompletionRequest(BaseChatCompletionRequest):
    messages: List[ChatMessage]
