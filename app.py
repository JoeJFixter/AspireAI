from flask import Flask, render_template
# from api.openai_api import openai_blueprint

app = Flask(__name__)

# # Register the OpenAI API blueprint
# app.register_blueprint(openai_blueprint)


import os
from swarm import Swarm, Agent
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file if you're using one
load_dotenv()


client = Swarm()

def chatbot_instructions(context_variables):
   previous_conversation = context_variables["previous_conversation"]
   prompt = f"You have been having a conversation with a user. You are an agent whose job it is to understand the long-term goals of the user. You are to collect information and ask follow up questions to get a good understanding of the user's goals. This is what you have said so far: {previous_conversation}"
   return prompt

chatbot_agent = Agent(
    name="Chatbot Agent",
    instructions=chatbot_instructions
)

def story_instructions(context_variables):
   previous_conversation = context_variables["previous_conversation"]
   prompt = f"You have had a converstion with the user discussing their goals and asperations your job is to now create a story of how they could achieve said goals and what their life would look like. This is the conversation you have had: {previous_conversation}"
   return prompt


story_agent = Agent(
    name="Story Agent",
    instructions=story_instructions
)

previous_conversation = []


def previous_conversation_to_string():
    return "\n".join(previous_conversation)

@app.route('/')
def index():
    return render_template('index.html')


# Define a route that will call the OpenAI API
@app.route('/api/chatbot_agent_api', methods=['POST'])
def call_chatbot_agent_api():
    # Get the user's input from the request data
    user_input = request.json.get('input', '')
    previous_conversation.append("User:" + user_input)


    # Make a call to the OpenAI API
    try:
        response = client.run(
            agent=chatbot_agent,
            messages=[{"role": "user", "content": user_input}],
            context_variables={"previous_conversation": previous_conversation_to_string()}
        )

        print(previous_conversation_to_string())

        result_text = response.messages[-1]["content"]
        previous_conversation.append("You: " + result_text)
     
        return jsonify({"status": "success", "response": result_text})
    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": str(e)})



# Define a route that will call the OpenAI API
@app.route('/api/story_agent_api', methods=['POST'])
def call_story_agent_api():
    # Get the user's input from the request data
    user_input = request.json.get('input', '')
    previous_conversation.append("User:" + user_input)


    # Make a call to the OpenAI API
    try:
        response = client.run(
            agent=chatbot_agent,
            messages=[{"role": "user", "content": "Make me a story"}],
            context_variables={"previous_conversation": previous_conversation_to_string()}
        )


        result_text = response.messages[-1]["content"]
     
        return jsonify({"status": "success", "response": result_text})
    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": str(e)})







if __name__ == '__main__':
    app.run(debug=True)

