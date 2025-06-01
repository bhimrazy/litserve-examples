from typing import List, Literal

from litserve import LitAPI
from litserve.specs.openai_embedding import (
    EmbeddingRequest as BaseEmbeddingRequest,
)
from litserve.specs.openai_embedding import (
    EmbeddingResponse,
)
from transformers import AutoModel, AutoTokenizer


class EmbeddingRequest(BaseEmbeddingRequest):
    model: str = Literal["jina-embeddings-v3"]
    task: str = Literal[
        "retrieval.query",
        "retrieval.passage",
        "text-matching",
        "classification",
        "separation",
    ]
    dimensions: int = 1024
    late_chunking: bool = False


class JinaEmbeddingAPI(LitAPI):
    def setup(self, device):
        self.tokenizer = AutoTokenizer.from_pretrained(
            "jinaai/jina-embeddings-v3", trust_remote_code=True
        )
        self.model = AutoModel.from_pretrained(
            "jinaai/jina-embeddings-v3", device=device, trust_remote_code=True
        )

    def decode_request(self, request: EmbeddingRequest, context: dict) -> List[str]:
        document = request.ensure_list()
        context.update(
            {
                "task": request.task,
                "dimensions": request.dimensions,
                "late_chunking": request.late_chunking,
            }
        )
        inputs = self.tokenizer(
            document, return_tensors="pt", return_offsets_mapping=True
        )

    def predict(self, inputs) -> List[List[float]]:
        # Tokenize the input text
        inputs = self.tokenizer(
            document,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt",
        )

        # Generate embeddings
        with torch.no_grad():
            outputs = self.model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1).tolist()

        return embeddings

    def encode_response(self, output) -> EmbeddingResponse:
        return EmbeddingResponse(data=output)
