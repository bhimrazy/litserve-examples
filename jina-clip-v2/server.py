# server.py
from typing import List, Tuple

import litserve as ls
from model import Embedding, EmbeddingRequest, EmbeddingResponse, Usage
from sentence_transformers import SentenceTransformer
from utils import parse_inputs


class EmbeddingAPI(ls.LitAPI):
    def setup(self, device):
        """Setup the model."""
        self.truncate_dim = 512
        self.model = SentenceTransformer(
            "jinaai/jina-clip-v2",
            trust_remote_code=True,
            truncate_dim=self.truncate_dim,
        )

    def decode_request(
        self, request: EmbeddingRequest, context: dict
    ) -> Tuple[List[str], List[str], List[str]]:
        """Decode the incoming request and prepare it for prediction."""
        # Update the context with request metadata
        context.update(
            {
                "model": request.model,
                "normalized": request.normalized,
            }
        )
        # Parse the inputs into text and image lists
        return parse_inputs(request.input)

    def predict(
        self, inputs: Tuple[List[str], List[str], List[str]], context: dict
    ) -> List[List[float]]:
        """Generate embeddings for text and image inputs, preserving the input
        order."""

        sentences, image_urls, input_types = inputs
        text_embeddings, image_embeddings = [], []

        # Encode text and images
        text_embeddings = self.model.encode(
            sentences, normalize_embeddings=context["normalized"]
        )
        if image_urls:
            image_embeddings = self.model.encode(
                image_urls, normalize_embeddings=context["normalized"]
            )

        # Create an iterator for embeddings to preserve input order
        text_iterator = iter(text_embeddings)
        image_iterator = iter(image_embeddings)

        # Combine embeddings based on input types
        combined_embeddings = [
            next(text_iterator) if input_type == "text" else next(image_iterator)
            for input_type in input_types
        ]
        return combined_embeddings

    def encode_response(
        self, output: List[List[float]], context: dict
    ) -> EmbeddingResponse:
        """Encode the embedding output into the response model."""
        embeddings = [
            Embedding(embedding=embedding, index=i)
            for i, embedding in enumerate(output)
        ]
        return EmbeddingResponse(
            data=embeddings,
            model=context["model"],
            usage=Usage(),  # TODO: Add usage statistics
        )


if __name__ == "__main__":
    api = EmbeddingAPI(api_path="/v1/embeddings")
    server = ls.LitServer(api, accelerator="auto")

    server.run(port=8000)
