# utils/embedding_utils.py

from sentence_transformers import SentenceTransformer

def get_embedding_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

def encode_text(model, text):
    return model.encode(text)
