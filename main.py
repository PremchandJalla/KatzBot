# main.py

from utils.nvdia_api_utils import get_nvidia_client, generate_response
from query_faiss import retrieve_context
import os

# Set your NVIDIA API key here
API_KEY = "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"
client = get_nvidia_client(API_KEY)

def main():
    query = input("Enter your question: ")
    
    # Retrieve context from FAISS
    contexts = retrieve_context(query, top_k=3)
    context_text = "\n".join(contexts)
    
    # Generate response using NVIDIA model
    answer = generate_response(client, context_text, query)
    print("Answer:", answer)

if __name__ == "__main__":
    main()
