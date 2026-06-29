import pandas as pd
import numpy as np
import faiss
import pickle

from sentence_transformers import SentenceTransformer
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)
INDEX_PATH = "backend/rag/diet_index.faiss"
DOCUMENTS_PATH = "backend/rag/documents.pkl"

index = faiss.read_index(INDEX_PATH)

with open(DOCUMENTS_PATH, "rb") as f:
    documents = pickle.load(f)
def retrieve_context(query: str, k: int = 3):
    """
    Retrieves the top-k most relevant documents for a given query.
    """

    # Convert the query into an embedding
    query_embedding = model.encode([query])

    # Search the FAISS index
    distances, indices = index.search(query_embedding, k)

    # Retrieve the matching documents
    results = [documents[i] for i in indices[0]]

    return results
def get_context_string(query, k=3):
    docs = retrieve_context(query, k)
    return "\n\n---\n\n".join(docs)