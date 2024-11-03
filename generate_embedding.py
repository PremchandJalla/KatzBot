# generate_embeddings.py

import requests
from bs4 import BeautifulSoup
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

# URLs to scrape and embed
urls = [
    "https://www.njit.edu/",
    "https://www.njit.edu/about",
    # Add more URLs as needed
]

def scrape_text(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = " ".join(p.get_text() for p in paragraphs)
        return text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ""

data, embeddings = [], []
for url in urls:
    text = scrape_text(url)
    if text:
        data.append({'url': url, 'text': text})
        embedding = model.encode(text)
        embeddings.append(embedding)

# Convert embeddings to numpy array and create FAISS index
embedding_matrix = np.vstack(embeddings).astype('float32')
index = faiss.IndexFlatL2(embedding_matrix.shape[1])
index.add(embedding_matrix)

faiss.write_index(index, 'embeddings/faiss_index.idx')
with open('embeddings/metadata.pkl', 'wb') as f:
    pickle.dump(data, f)

print("Embeddings and FAISS index generated successfully.")
