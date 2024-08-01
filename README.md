# Flask Chatbot with Gemini API

This project is a simple chatbot built using the Flask framework and Gemini API. It handles user inputs and responds with appropriate answers using the Gemini API.

## Features

- Handles user inputs via HTTP requests.
- Integrates with Gemini API to fetch responses.
- Provides a user-friendly chat interface using HTML, CSS, and JavaScript.
- Displays loading animation while processing user inputs.
- Auto-scrolls chat area for better user experience.
- Allows clearing of chat history.

## Requirements

- Python 3.6 or higher
- Flask
- Requests
- Dotenv

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/vishnu-git1524/chatbot.git
    cd chatbot
    ```

2. Create and activate a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file and add your Gemini API key:

    ```
    Gemini_API_KEY=your_gemini_api_key_here
    ```

## Usage

1. Run the Flask app:

    ```bash
    python app.py
    ```

2. Open your web browser and go to `http://127.0.0.1:5000`.

## Project Structure

- `app.py`: The main Flask application file.
- `templates/chat.html`: The HTML file for the chat interface.
- `.env`: Environment file for storing API keys.

## Code

### `app.py`

```python
import google.generativeai as genai
import os
from flask import Flask, jsonify, render_template, request, session
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
