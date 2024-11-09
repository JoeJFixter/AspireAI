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
    first_name = context_variables["first_name"]
    last_name = context_variables["last_name"]
    gender = context_variables["gender"]
    age = context_variables["age"]
    prompt = f"You have had a conversation with the user discussing their goals and asperations your job is to now create a story of how the users life would look like in the future if they achieved these goals. This is the conversation you have had: {previous_conversation} The user's first name is {first_name}, last name is {last_name} the users gender is {gender} and they are currently {age} years old. Include this information in the story. Do not talk about anyone else. Do not hallucinate."
    # prompt = "Write response in spanish"
    return prompt


story_agent = Agent(
    name="Story Agent",
    instructions=story_instructions
)

previous_conversation = []

first_name = ""
last_name = ""
gender = ""
age = ""


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
            agent=story_agent,
            messages=[{"role": "user", "content": "Make me a story given the information I have provided. Do not ask for any more information."}],
            context_variables={"previous_conversation": previous_conversation_to_string(), "first_name": first_name, "last_name": last_name, "gender":gender, "age": age}
        )

        result_text = response.messages[-1]["content"]
     
        return jsonify({"status": "success", "response": result_text})
    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": str(e)})



@app.route('/api/add_basic_info', methods=['POST'])
def add_basic_info():
    global first_name, last_name, gender, age
    first_name = request.json.get('firstName', '')
    last_name = request.json.get('lastName', '')
    gender = request.json.get('gender', '')
    age = request.json.get('age', '')

    print(first_name, last_name, gender, age)
    print("Helloooo")

    # You can now use these variables as needed
    return jsonify({"status": "success", "message": "Basic info received"})



if __name__ == '__main__':
    app.run(debug=True)

