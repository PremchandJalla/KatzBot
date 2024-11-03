# query_faiss.py

import numpy as np
import faiss
import pickle
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.read_index('embeddings/faiss_index.idx')
with open('embeddings/metadata.pkl', 'rb') as f:
    metadata = pickle.load(f)

def retrieve_context(query, top_k=5):
    query_embedding = model.encode(query).astype('float32')
    distances, indices = index.search(np.array([query_embedding]), top_k)
    contexts = [metadata[idx]['text'] for idx in indices[0]]
    return contexts
