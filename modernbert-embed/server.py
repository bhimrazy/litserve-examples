from litserve import LitAPI, LitServer, OpenAIEmbeddingSpec
from litserve.specs.openai_embedding import EmbeddingRequest
from sentence_transformers import SentenceTransformer


class ModernBertEmbeddingAPI(LitAPI):
    def setup(self, device):
        self.model_name = "nomic-ai/modernbert-embed-base"
        self.model = SentenceTransformer(self.model_name)  # 768 dim
        self.prefix = "search_query: "

    def decode_request(self, request: EmbeddingRequest):
        documents = request.ensure_list()
        prefixed_documents = [self.prefix + doc for doc in documents]
        return prefixed_documents

    def predict(self, documents):
        return list(self.model.encode(documents))


if __name__ == "__main__":
    api = ModernBertEmbeddingAPI(spec=OpenAIEmbeddingSpec())
    server = LitServer(api)
    server.run(port=8000)
