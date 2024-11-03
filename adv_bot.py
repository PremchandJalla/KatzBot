# from flask import Flask, request, jsonify, send_from_directory
# from query_faiss import retrieve_context
# from utils.nvdia_api_utils import get_nvidia_client, generate_response
# from transformers import AutoModelForCausalLM, AutoTokenizer
# import os
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# # Initialize the NVIDIA API client
# API_KEY = "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"
# client = get_nvidia_client(API_KEY)

# # Define a set of stop words
# STOP_WORDS = {"racism", "sexual", "pornography", "violence", "hate", "discrimination"}

# def contains_stop_words(text):
#     # Check if any stop word is present in the text
#     return any(stop_word in text.lower() for stop_word in STOP_WORDS)

# # Uncomment the following lines to enable BERT model
# # finetuned_bert_path = "/path/to/your/finetuned_bert_model"  # Update the path
# # bert_model = AutoModelForCausalLM.from_pretrained(finetuned_bert_path)
# # bert_tokenizer = AutoTokenizer.from_pretrained(finetuned_bert_path)

# # Predefined questions and responses
# # predefined_responses = {
# #     "Who will HACKNJIT23": "The team who built the highlander bot"
# #     # Add more predefined questions and responses here
# # }

# def get_predefined_response(question):
#     """Return predefined response if question matches."""
#     # Uncomment the following line to enable predefined responses
#     # return predefined_responses.get(question.strip(), None)

# @app.route('/query', methods=['POST'])
# def query():
#     data = request.json
#     question = data.get("query", "").strip()

#     # Check for stop words in the user query
#     if contains_stop_words(question):
#         return jsonify({"answer": "I'm here to promote a positive and respectful dialogue. Let's discuss something else."})

#     # Uncomment the following lines to check for predefined responses
#     # predefined_response = get_predefined_response(question)
#     # if predefined_response:
#     #     return jsonify({"answer": predefined_response})

#     # Retrieve context from FAISS
#     contexts = retrieve_context(question, top_k=3)
#     context_text = "\n".join(contexts) if contexts else ""

#     if context_text:
#         # Use the context for generating a response with the Highlander Bot's personality
#         prompt = (
#             f"User Question: {question}\n"
#             f"Context Information:\n{context_text}\n\n"
#             "As the Highlander Bot, respond with a friendly and supportive tone, making sure to engage the user warmly."
#         )
#     else:
#         # If no context is found, respond with Highlander Bot's personality
#         prompt = "As the Highlander Bot, greet the user and ask how you can assist them today!"

#     # Generate response from NVIDIA's model using the formatted prompt
#     answer = generate_response(client, prompt, question)

#     # Validate the response for stop words
#     if contains_stop_words(answer):
#         return jsonify({"answer": "I'm here to promote a positive and respectful dialogue. Let's discuss something else."})

#     return jsonify({"answer": answer.strip()})

# @app.route('/')
# def serve_ui():
#     # Serve the HTML file for the chatbot UI
#     return send_from_directory('ui', 'index.html')

# @app.route('/<path:path>')
# def serve_static(path):
#     # Serve static files (CSS, JS)
#     return send_from_directory('ui', path)

# #if __name__ == "__main__":
# #    app.run(host="0.0.0.0", port=8000, debug=True)
