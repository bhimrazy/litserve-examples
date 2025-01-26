import time
import asyncio
import inspect
import logging
import uuid
from collections import deque
from typing import Literal, Optional, TypeAlias, Union

from fastapi import BackgroundTasks, Request, Response
from litserve import LitServer
from litserve.specs.base import LitSpec
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

SpeechModel: TypeAlias = Literal["tts-1", "tts-1-hd"]
SpeechVoice: TypeAlias = Literal["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
ResponseFormat: TypeAlias = Literal["mp3", "opus", "aac", "flac", "wav", "pcm"]


class SpeechGenerationRequest(BaseModel):
    model: Union[str, SpeechModel]
    input: str = Field(..., max_length=4096)
    voice: Union[str, SpeechVoice]
    response_format: Optional[ResponseFormat]
    speed: Optional[float] = Field(1.0, ge=0.25, le=4.0)
    stream: Optional[bool] = False


LITAPI_VALIDATION_MSG = """LitAPI.predict and LitAPI.encode_response must be a generator (use yield instead or return)
while using the OpenAISpec.

Error: {}

Please follow the below examples for guidance on how to use the spec:

If your current code looks like this:

```
import litserve as ls
from litserve.specs.openai import ChatMessage

class ExampleAPI(ls.LitAPI):
    ...
    def predict(self, x):
        return "This is a generated output"

    def encode_response(self, output: dict):
        return ChatMessage(role="assistant", content="This is a custom encoded output")
```

You should modify it to:

```
import litserve as ls
from litserve.specs.openai import ChatMessage

class ExampleAPI(ls.LitAPI):
    ...
    def predict(self, x):
        yield "This is a generated output"

    def encode_response(self, output):
        yield ChatMessage(role="assistant", content="This is a custom encoded output")
```


You can also yield responses in chunks. LitServe will handle the streaming for you:

```
class ExampleAPI(ls.LitAPI):
    ...
    def predict(self, x):
        yield from self.model(x)

    def encode_response(self, output):
        for out in output:
            yield ChatMessage(role="assistant", content=out)
```
"""


class OpenAISpeechSpec(LitSpec):
    def __init__(self):
        super().__init__()
        # register endpoint
        self.add_endpoint("/v1/audio/speech", self.speech_generation, methods=["POST"])
        self.add_endpoint(
            "/v1/audio/speech", self.options_speech_generation, methods=["OPTIONS"]
        )

    def setup(self, server: LitServer):
        from litserve import LitAPI

        super().setup(server)

        lit_api = self._server.lit_api
        if not inspect.isgeneratorfunction(lit_api.predict):
            raise ValueError(LITAPI_VALIDATION_MSG.format("predict is not a generator"))

        is_encode_response_original = (
            lit_api.encode_response.__code__ is LitAPI.encode_response.__code__
        )
        if not is_encode_response_original and not inspect.isgeneratorfunction(
            lit_api.encode_response
        ):
            raise ValueError(
                LITAPI_VALIDATION_MSG.format("encode_response is not a generator")
            )
        print("OpenAISpeech spec setup complete")

    async def speech_generation(
        self, request: SpeechGenerationRequest, background_tasks: BackgroundTasks
    ):
        response_queue_id = self.response_queue_id
        logger.debug("Received speech generation request %s", request)
        uid = uuid.uuid4()
        q = deque()
        event = asyncio.Event()
        self._server.response_buffer[uid] = (q, event)
        self._server.request_queue.put(
            (response_queue_id, uid, time.monotonic(), request)
        )

        return Response(status_code=200)

    async def options_speech_generation(self, request: Request):
        return Response(status_code=200)
