import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = Flask(__name__)

def openai_gpt_reply(current_user_input):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("No OpenAI API key found in environment variables")

    try:
        client = OpenAI(api_key=api_key)
        stream = client.chat.completions.create(
            messages=[
                {"role": "system", 'content': 'You are a helpful assistant'},
                {"role": "user", "content": current_user_input}
            ],
            model='gpt-3.5-turbo',
            stream=True,
            temperature=0.2,
        )
        response_text = ""

        for chunk in stream:
            response_text += (chunk.choices[0].delta.content or "")

        return response_text 
    except Exception as e:
        return str(e)

@app.route('/ask', methods=['POST'])
def ask_question():
    user_input = request.data.decode('utf-8')
    if not user_input:
        return jsonify({"error": "No question provided"}), 400

    reply = openai_gpt_reply(user_input)
    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run()
