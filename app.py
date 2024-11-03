from flask import Flask, request, jsonify, send_from_directory
from utils.nvdia_api_utils import get_nvidia_client, generate_response
import os
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize the NVIDIA API client
API_KEY = "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"
client = get_nvidia_client(API_KEY)

# Define a set of stop words
STOP_WORDS = {"racism", "sexual", "pornography", "violence", "hate", "discrimination"}

# Define predefined questions and responses
PREDEFINED_QUESTIONS = {
    "What are the library hours?": "The NJIT Library is open from 8 AM to 10 PM on weekdays, and from 10 AM to 6 PM on weekends. During exams, hours may be extended.",
    "Where can I find tutoring services?": "NJIT offers tutoring services through the Learning Center, located on the second floor of the Campus Center. You can also access online resources.",
    "How do I access the gym?": "Students can access the NJIT Wellness and Events Center (WEC) with a valid student ID. The gym is open daily with varying hours. Check the WEC website for the latest schedule.",
    "When is the next career fair?": "The NJIT Career Development Services (CDS) hosts several career fairs each year. Visit the CDS website or check your student email for upcoming dates.",
    "What is NJIT's academic calendar?": "You can find the NJIT academic calendar on the official website. It includes important dates like semester start and end, holidays, and exam periods."
}

def contains_stop_words(text):
    # Check if any stop word is present in the text
    return any(stop_word in text.lower() for stop_word in STOP_WORDS)

def clean_text(text):
    """Remove punctuation and convert to lowercase for consistent comparison."""
    return re.sub(r'[^\w\s]', '', text).lower()

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    question = data.get("query", "").strip()
    cleaned_question = clean_text(question)

    # Check for stop words in the user query
    if contains_stop_words(question):
        return jsonify({"answer": "I'm here to promote a positive and respectful dialogue. Let's discuss something else."})

    # Check for predefined questions
    for predefined_question, predefined_answer in PREDEFINED_QUESTIONS.items():
        if clean_text(predefined_question) == cleaned_question:
            return jsonify({"answer": predefined_answer})

    # Simulate context retrieval (without actually querying FAISS)
    context_text = ""  # Set empty context since we're skipping FAISS
    # Constructing the prompt to reflect a university-friendly personality
    prompt = (
        f"User Question: {question}\n"
        f"Context Information:\n{context_text}\n\n"
        "As the NJIT Highlander Bot, respond with a friendly, student-focused tone. Engage the user warmly, provide helpful information, and support their academic and campus life needs. "
        "Offer guidance on university resources, study tips, or NJIT events if relevant. Be supportive and encouraging!"
    )

    # Generate response from NVIDIA's model using the formatted prompt
    answer = generate_response(client, prompt, question)

    # Validate the response for stop words
    if contains_stop_words(answer):
        return jsonify({"answer": "I'm here to promote a positive and respectful dialogue. Let's discuss something else."})

    return jsonify({"answer": answer.strip()})

@app.route('/')
def serve_ui():
    # Serve the HTML file for the chatbot UI
    return send_from_directory('ui', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    # Serve static files (CSS, JS)
    return send_from_directory('ui', path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
