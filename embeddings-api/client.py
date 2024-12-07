from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:8000/v1",
    api_key="lit",
)

response = client.embeddings.create(
    model="jinaai/jina-embeddings-v2-small-en",
    input="The food was delicious and the waiter...",
    encoding_format="float",
)

print(response)