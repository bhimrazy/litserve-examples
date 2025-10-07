from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:8000/v1",
    api_key="lit",
)

response = client.embeddings.create(
    model="nomic-ai/modernbert-embed-base",
    input="ModernBERT Embed is an embedding model trained from ModernBERT-base, bringing the new advances of ModernBERT to embeddings!",
    encoding_format="float",
)

print(response)
