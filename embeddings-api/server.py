from fastembed import TextEmbedding
from litserve import LitAPI, LitServer, OpenAIEmbeddingSpec


class EmbeddingAPI(LitAPI):
    def setup(self, device):
        cuda = "cuda" in device
        providers = ["CUDAExecutionProvider"] if cuda else None
        self.model = TextEmbedding(
            "jinaai/jina-embeddings-v2-small-en",
            providers=providers,
            cuda=cuda,
        )  # 512 dim, 0.120 GB

    def predict(self, documents):
        return list(self.model.embed(documents))


if __name__ == "__main__":
    api = EmbeddingAPI()
    server = LitServer(api, accelerator="cpu", spec=OpenAIEmbeddingSpec())
    server.run(port=8000, generate_client_file=False)
