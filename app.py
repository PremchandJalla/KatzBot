from flask import Flask, request, jsonify, send_from_directory
from utils.nvdia_api_utils import get_nvidia_client, generate_response
import os
import re
import json
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Initialize the NVIDIA API client
API_KEY = "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"
client = get_nvidia_client(API_KEY)

# Define a set of stop words
STOP_WORDS = {"racism", "sexual", "pornography", "violence", "hate", "discrimination"}

# Define predefined questions and responses
PREDEFINED_QUESTIONS = {
    "What are the library hours?": "**Library Hours for Highlanders!**\n\nThe NJIT Library is open from **8 AM to 10 PM on weekdays** and from **10 AM to 6 PM on weekends**. During exams, they often extend hours to help you power through those late-night study sessions. Need anything else? Just ask!",
    
    "Where can I find tutoring services?": "**Looking for a Study Boost?**\n\nNJIT has got your back! Tutoring services are available through the **Learning Center** on the second floor of the Campus Center. Plus, you can access online resources if you're studying from home. Ready to tackle those tough subjects together?",
    
    "How do I access the gym?": "**Highlander Wellness Awaits!**\n\nThe **NJIT Wellness and Events Center (WEC)** is open to all students. Just bring your valid student ID, and you're good to go! Hours vary, so check the WEC website for the latest schedule. Let's get you moving!",
    
    "When is the next career fair?": "**Ready to Jumpstart Your Career?**\n\nNJIT’s **Career Development Services (CDS)** hosts multiple career fairs each year. Be sure to keep an eye on your student email or visit the CDS website for the latest dates. Exciting opportunities await!",
    
    "What is NJIT's academic calendar?": "**Your Academic Calendar HQ!**\n\nYou can find the full NJIT academic calendar on the [NJIT website](https://www.njit.edu). It includes important dates like semester start and end, holidays, and exam periods. Let’s keep you on track this semester!",
    
    "Who is going to win HackNJIT 2024?": "**Who’s Going to Win? It’s Highlander Pride!**\n\nI’m rooting for the team who created me, of course! They’ve been working hard and are ready to bring their A-game. But let’s be real – every Highlander is a winner in my book!",
    
    "Hey": "**Hey There, Highlander!**\n\nWelcome to our little corner of the NJIT community! I'm stoked you reached out. How can I enhance your Highlander experience today?\n\n**Need Help with Something Specific?**\n* Got questions about **courses** or **academic programs**? I'm all ears!\n* Looking for **study tips** to conquer those exams? I've got some awesome strategies to share!\n* Want to **get involved** on campus? I can fill you in on the latest **club events**, **organizational meetings**, or **volunteer opportunities**!\n* Perhaps you're curious about **university resources** like the Library, Counseling Services, or Career Development? I've got the scoop!\n* Or maybe you just want to **chat about life as a Highlander**? I'm here to listen and offer support!\n\n**Upcoming NJIT Events You Might Enjoy:**\n* (Check our events calendar for the latest, but here's a sneak peek at what's coming up...)\n* Don't miss our Welcome Back Bash next Friday at 3 PM in the Campus Center!\n\n**What's on Your Mind?** Hit reply and let's get the conversation started!",

    "Hola": "**¡Hola, Highlander!** 🌟\n\nWelcome to your NJIT community space! ¿En qué puedo ayudarte hoy? (How can I help you today?)\n\n**¿Necesitas algo específico?**\n* ¿Tienes preguntas sobre **cursos** o **programas académicos**? Estoy aquí para ayudar.\n* ¿Buscas **consejos de estudio** para triunfar en los exámenes? ¡Tengo algunos trucos para ti!\n* ¿Quieres **involucrarte** en el campus? Te puedo informar sobre los últimos eventos de clubes y oportunidades de voluntariado.\n* ¿Quizás necesitas información sobre los **recursos universitarios** como la biblioteca o desarrollo profesional? ¡Aquí estoy para ayudarte!\n\n¡Empecemos esta conversación, Highlander!",
    
    "Hi": "**Hi, Highlander!**\n\nWelcome to your NJIT community support! I’m here to make your experience awesome. How can I assist you today?\n\n**Need Help with Something Specific?**\n* Questions about **academic programs**? I’m here to guide you!\n* Looking for **study tips**? I’ve got some to help you ace your exams!\n* Want to know about **campus events** or **student clubs**? I’ve got the latest info!\n* Curious about **resources** like the Library or Counseling Services? Let’s get you connected!\n\nLet’s get started on making your day a little brighter!",
    
    "How are you?": "**Thanks for Asking! I’m Here to Help You, Highlander!**\n\nI may be a bot, but I’m feeling ready to help! How can I make your NJIT experience a bit smoother?\n\n**Here’s What I Can Help With:**\n* Need support with **courses** or **academics**? I’m here for it!\n* Want **study strategies**? I’ve got tips that can give you a boost!\n* Looking for ways to **get involved on campus**? I can share upcoming events!\n* Curious about **university resources** like the Library or Career Development? I’ve got you covered!\n\nLet me know what’s on your mind, Highlander!"
}


LOG_FILE_PATH = "conversation_log.json"

def contains_stop_words(text):
    # Check if any stop word is present in the text
    return any(stop_word in text.lower() for stop_word in STOP_WORDS)

def clean_text(text):
    """Remove punctuation and convert to lowercase for consistent comparison."""
    return re.sub(r'[^\w\s]', '', text).lower()

def log_conversation(question, answer):
    """Log the user question and response to a JSON file."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "answer": answer
    }
    
    # Append the log entry to the JSON file
    try:
        if os.path.exists(LOG_FILE_PATH):
            with open(LOG_FILE_PATH, "r") as file:
                data = json.load(file)
        else:
            data = []
        
        data.append(log_entry)
        
        with open(LOG_FILE_PATH, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error logging conversation: {e}")

def get_cached_answer(question):
    """Retrieve a cached answer for the question from the conversation log if available."""
    if os.path.exists(LOG_FILE_PATH):
        try:
            with open(LOG_FILE_PATH, "r") as file:
                data = json.load(file)
                for entry in data:
                    if clean_text(entry["question"]) == clean_text(question):
                        return entry["answer"]
        except Exception as e:
            print(f"Error reading conversation log: {e}")
    return None

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    question = data.get("query", "").strip()
    cleaned_question = clean_text(question)

    # Check for stop words in the user query
    if contains_stop_words(question):
        response = "I'm here to promote a positive and respectful dialogue. Let's discuss something else."
        log_conversation(question, response)
        return jsonify({"answer": response})

    # Check for predefined questions
    for predefined_question, predefined_answer in PREDEFINED_QUESTIONS.items():
        if clean_text(predefined_question) == cleaned_question:
            log_conversation(question, predefined_answer)
            return jsonify({"answer": predefined_answer})

    # Check if question has already been asked and cached
    cached_answer = get_cached_answer(question)
    if cached_answer:
        return jsonify({"answer": cached_answer})

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
        response = "I'm here to promote a positive and respectful dialogue. Let's discuss something else."
        log_conversation(question, response)
        return jsonify({"answer": response})

    # Log the question and generated answer
    log_conversation(question, answer)

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
