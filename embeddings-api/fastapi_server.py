from typing import List, Literal, Union

from fastapi import FastAPI
from fastembed import TextEmbedding
from pydantic import BaseModel

app = FastAPI()
model = TextEmbedding("jinaai/jina-embeddings-v2-small-en")


class EmbeddingRequest(BaseModel):
    input: Union [str, List[str]]
    model: str
    encoding_format: str


class Embedding(BaseModel):
    index: int
    embedding: List[float]
    object: Literal["embedding"] = "embedding"


class EmbeddingResponse(BaseModel):
    data: List[Embedding]
    model: str
    object: str


@app.get("/")
async def read_root():
    return {"message": "Welcome to the embeddings API"}


@app.post("/v1/embeddings", response_model=EmbeddingResponse)
async def get_embeddings(request: EmbeddingRequest):
    docs = [request.input] if isinstance(request.input, str) else request.input
    embeddings = model.embed(docs)

    response_data = [
        Embedding(index=i, embedding=embedding)
        for i, embedding in enumerate(embeddings)
    ]

    return EmbeddingResponse(data=response_data, model=request.model, object="list")
