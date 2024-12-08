from fastembed import TextEmbedding
from litserve import LitAPI, LitServer, OpenAIEmbeddingSpec
from litserve.specs.openai_embedding import EmbeddingRequest


class EmbeddingAPI(LitAPI):
    def setup(self, device):
        cuda = "cuda" in device
        providers = ["CUDAExecutionProvider"] if cuda else None
        self.model = TextEmbedding(
            "jinaai/jina-embeddings-v2-small-en",
            providers=providers,
            cuda=cuda,
        )  # 512 dim, 0.120 GB

    def decode_request(self, request: EmbeddingRequest, context: dict):
        documents = request.ensure_list()

        encoded_docs = self.model.model.tokenizer.encode_batch(documents)
        num_tokens = sum(map(len, encoded_docs))
        context.update({"prompt_tokens": num_tokens, "total_tokens": num_tokens})

        return documents

    def predict(self, documents):
        return list(self.model.embed(documents))

    def encode_response(self, output, context: dict):
        return {"embeddings": output, **context}


if __name__ == "__main__":
    api = EmbeddingAPI()
    server = LitServer(api, spec=OpenAIEmbeddingSpec())
    server.run(port=8000, generate_client_file=False)
