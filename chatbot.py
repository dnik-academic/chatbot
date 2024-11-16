from flask import Flask, request, jsonify
import openai
import os

# Initialize Flask app
app = Flask(__name__)

# Set OpenAI API Key (set your actual API key here or as an environment variable)
openai.api_key = os.getenv("OPENAI_API_KEY", "your-api-key-here")

@app.route("/")
def home():
    return "Chatbot is running!"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Parse user input from the request
        user_message = request.json.get("message", "")
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        # OpenAI GPT-4-turbo call
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",  # Specify GPT-4-turbo model
            messages=[
                {"role": "system", "content": "You are a helpful assistant specializing in web development, digital marketing, and content creation."},
                {"role": "user", "content": user_message},
            ],
            max_tokens=500,  # Limit response length
            temperature=0.7,  # Control creativity
        )

        # Extract and return the assistant's reply
        bot_reply = response["choices"][0]["message"]["content"]
        return jsonify({"response": bot_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
