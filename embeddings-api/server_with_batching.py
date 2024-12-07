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

    def predict(self, batch):
        # Flatten the batch_documents
        documents = [doc for docs in batch for doc in docs]

        # Embed the documents
        embeddings = list(self.model.embed(documents))

        # Group the embeddings back into the batch format
        start = 0
        result = []
        for size in map(len, batch):
            result.append(embeddings[start : start + size])
            start += size

        return result


if __name__ == "__main__":
    api = EmbeddingAPI()
    server = LitServer(
        api, spec=OpenAIEmbeddingSpec(), max_batch_size=8, batch_timeout=0.01
    )
    server.run(port=8000, generate_client_file=False)
