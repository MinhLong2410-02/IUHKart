import json
from sentence_transformers import SentenceTransformer
from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import torch

model = SentenceTransformer('all-MiniLM-L6-v2')
model.to(torch.device('cpu'))
if torch.cuda.is_available():
    model.to(torch.device('cuda'))

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {
        "description": "This is an API for embedding slug-name",
        "endpoints": {
            "/health": {"method": "GET", "description": "Check the health of the API"},
            "/embedding": {"method": "GET", "description": "Get the embedding of a sentence 384 dim"},
            "/device": {"method": "GET", "description": "Check using device cpu or gpu"}
        },
        "how_to_use": {
            "/embedding": {"method": "GET", "description": "Get the embedding of a sentence 384 dim", "params": {"q": "string"}},
        }
    }

@app.get("/health")
def read_health():
    return {"status": "ok"}

@app.get("/embedding")
def read_embedding(q: Union[str, None] = None):
    sentences = [q]
    sentence_embeddings = model.encode(sentences)
    return {"q": q, "embedding": sentence_embeddings[0].tolist()}

@app.get("/device")
def read_device():
    '''
    Check using device cpu or gpu
    '''
    return {"device": "cuda" if torch.cuda.is_available() else "cpu"}