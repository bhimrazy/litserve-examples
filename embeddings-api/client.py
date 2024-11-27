from openai import OpenAI

client = OpenAI()

client.embeddings.create(
    model="text-embedding-ada-002",
    input="The food was delicious and the waiter...",
    encoding_format="float",
)
