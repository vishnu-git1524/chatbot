from flask import Flask, jsonify, render_template, request, session
import google.generativeai as genai
import os

from dotenv import load_dotenv

load_dotenv()

api = os.getenv('Gemini_API_KEY')

# Configure generative AI model and start chat
genai.configure(api_key=api)
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Initialize chat history
chat_history = []

# Index route to render chat interface
@app.route('/')
def index():
    return render_template('chat.html', chat_history=chat_history)

# Chat endpoint to handle user input
@app.route('/chat', methods=['POST'])
def chat_endpoint():
    try:
        user_input = request.json.get('user_input')

        if not user_input:
            return jsonify({"error": "No user input provided."}), 400

        # Send user input to generative AI model
        response = chat.send_message(user_input)
        chat_history.append({"user": user_input, "bot": response.text})

        # Store chat history in session
        session['chat_history'] = chat_history

        return jsonify({"response": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Clear chat history endpoint
@app.route('/clear_history', methods=['POST'])
def clear_history():
    session.pop('chat_history', None)
    chat_history.clear()
    return jsonify({"message": "Chat history cleared successfully."})

if __name__ == '__main__':
    app.run(debug=True)
