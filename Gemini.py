import google.generativeai as genai
import os

from dotenv import load_dotenv

load_dotenv()

api = os.getenv('Gemini_API_KEY')

genai.configure(api_key=api)
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])
while True:
    user_input = input("\nYou: ")

    response = chat.send_message(user_input)
    print("AI:", response.text)
