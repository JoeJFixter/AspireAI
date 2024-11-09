import os
import openai
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file if you're using one
load_dotenv()

# Set up the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define a blueprint for this API module
openai_blueprint = Blueprint('openai_api', __name__)

# Instantiate an OpenAI client
client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))

# Define a route that will call the OpenAI API
@openai_blueprint.route('/api/openai_api', methods=['POST'])
def call_openai_api():
    # Get the user's input from the request data
    user_input = request.json.get('input', '')

    # Make a call to the OpenAI API
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_input,
                }
            ],
            model="gpt-3.5-turbo",
        )
        # Extract the response text
        result_text = response.choices[0].message.content.strip()

        return jsonify({"status": "success", "response": result_text})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
