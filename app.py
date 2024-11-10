from flask import Flask, render_template
# from api.openai_api import openai_blueprint

app = Flask(__name__, template_folder='templates')

# # Register the OpenAI API blueprint
# app.register_blueprint(openai_blueprint)


from os import environ as env 
from swarm import Swarm, Agent
from flask import Blueprint, request, jsonify, redirect, render_template, session, url_for
from dotenv import load_dotenv, find_dotenv
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth

app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)
oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

# \\\\\\\\\\\\\\\\\\\\\ Auth0 login ///////////////////////// 

@app.route("/login")
def login():
    print("login")
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.route("/home")
def dashboard():
    if "user" not in session:
        print("user not in session")
        return redirect(url_for("index.html"))
    return render_template("home.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))


# \\\\\\\\\\\\\\\\\\\\\ Auth0 login  end /////////////////////////






# Load environment variables from .env file if you're using one
load_dotenv()

previous_conversation = []
story_text = ""

first_name = ""
last_name = ""
gender = ""
age = ""
country = ""
occupation = ""
employmentType = ""


json_format = '''"summary": "Hackathon Meeting",
    "location": "Online",
    "description": "Discuss project updates.",
    "start": {
        "dateTime": "2024-11-10T10:00:00-07:00",
        "timeZone": "America/Los_Angeles",
    },
    "end": {
        "dateTime": "2024-11-10T11:00:00-07:00",
        "timeZone": "America/Los_Angeles",
    },
    '''

client = Swarm()

def previous_conversation_to_string():
    return "\n".join(previous_conversation)

@app.route('/')
def index():
    return render_template('index.html')


# ======= Chatbot Agent =======

def chatbot_instructions(context_variables):
   previous_conversation = context_variables["previous_conversation"]
   prompt = f"You have been having a conversation with a user. You are an agent whose job it is to understand the long-term goals of the user. You are to collect information and ask follow up questions to get a good understanding of the user's goals. This is what you have said so far: {previous_conversation}. Do not try to give advice on how they could achieve these goals. You should only be collecting information from the user on their goals. Keep responses short, but collected as much relevant information as possible. You will be having a lengthy conversation with the user, so you can collect this information over multiple prompts"
   return prompt

chatbot_agent = Agent(
    name="Chatbot Agent",
    instructions=chatbot_instructions
)

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

        # print(previous_conversation_to_string())

        result_text = response.messages[-1]["content"]
        previous_conversation.append("You: " + result_text)
     
        return jsonify({"status": "success", "response": result_text})
    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": str(e)})
    


# ======= Story Agent =======   

def story_instructions(context_variables):
    previous_conversation = context_variables["previous_conversation"]
    first_name = context_variables["first_name"]
    last_name = context_variables["last_name"]
    gender = context_variables["gender"]
    age = context_variables["age"]
    country = context_variables["country"]
    occupation = context_variables["occupation"]
    employmentType = context_variables["employmentType"]
    prompt = f"You have had a conversation with the user discussing their goals and aspirations your job is to now create a story of how the users life would look like in the future if they achieved these goals. Do not talk about the present. Assume they are older than they are now, and they have achieved their goals, living their dream life. This is the conversation you have had: {previous_conversation} The user's first name is {first_name}, last name is {last_name} the users gender is {gender} and they are currently {age} years old and live in {country}. They work as {occupation} and are contracted to {employmentType} hours. Include this information in the story. Do not talk about anyone else. Do not hallucinate."
    return prompt


story_agent = Agent(
    name="Story Agent",
    instructions=story_instructions
)


# Define a route that will call the OpenAI API
@app.route('/api/story_agent_api', methods=['POST'])
def call_story_agent_api():
    global story_text
    # Get the user's input from the request data
    user_input = request.json.get('input', '')
    previous_conversation.append("User:" + user_input)


    # Make a call to the OpenAI API
    try:
        response = client.run(
            agent=story_agent,
            messages=[{"role": "user", "content": "Make me a story given the information I have provided. Do not ask for any more information."}],
            context_variables={"previous_conversation": previous_conversation_to_string(), "first_name": first_name, "last_name": last_name, "gender":gender, "age": age, "country": country, "occupation": occupation, "employmentType": employmentType}
        )

        result_text = response.messages[-1]["content"]
        story_text = result_text
     
        return jsonify({"status": "success", "response": result_text})
    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": str(e)})



# ======= Add Basic Info =======
@app.route('/api/add_basic_info', methods=['POST'])
def add_basic_info():
    global first_name, last_name, gender, age, country, occupation, employmentType
    first_name = request.json.get('firstName', '')
    last_name = request.json.get('lastName', '')
    gender = request.json.get('gender', '')
    age = request.json.get('age', '')
    country = request.json.get('country', '')
    occupation = request.json.get('occupation', '')
    employmentType = request.json.get('employmentType', '')

    # You can now use these variables as needed
    return jsonify({"status": "success", "message": "Basic info received"})


# ======= Generate tasks for the user =======
def task_instructions(context_variables):
    previous_conversation = context_variables["previous_conversation"]
    first_name = context_variables["first_name"]
    last_name = context_variables["last_name"]
    gender = context_variables["gender"]
    age = context_variables["age"]
    country = context_variables["country"]
    story_text = context_variables["story_text"]
    occupation = context_variables["occupation"]
    employmentType = context_variables["employmentType"]
    prompt = f"You have been having a conversation with a user. You have been gathering information about the user's goals and aspirations and have created a story of how the users life would look like in the future if they achieved these goals. Your job now is to create a weekly schedule of tasks distrubited throught uniformly throughout the week so that the user can do to achieve these goals. You should create a schedule of tasks that are specific, actionable, and achievable. You should also include a time block for each task across one week. Output this in JSON format for it to be used in google calander API. The format for each event should be {json_format}. Do not add any other text except the JSON. This response needs to be able to be parsed by an API later. This is the conversation you have had: {previous_conversation} The user's first name is {first_name}, last name is {last_name} the users gender is {gender} and they are currently {age} years old. The user lives in {country} and works as {occupation} on a {employmentType} contract. The story you created is: {story_text}. Do not ask for any more information. You should only be creating a list of tasks that the user can do to achieve their goals."
    return prompt


task_agent = Agent(
    name="Task Agent",
    instructions=task_instructions
)

# Define a route that will call the OpenAI API
@app.route('/api/task_agent_api', methods=['POST'])
def call_task_agent_api():

    # Make a call to the OpenAI API
    try:
        response = client.run(
            agent=task_agent,
            messages=[{"role": "user", "content": "Create a weekly schedule of tasks to complete these goals. Do not ask for any more information."}],
            context_variables={"previous_conversation": previous_conversation_to_string(), "first_name": first_name, "last_name": last_name, "gender":gender, "age": age, "country": country, "occupation": occupation, "employmentType": employmentType, "story_text": story_text}
        )

        result_text = response.messages[-1]["content"]

        print(result_text)
        # Remove the ```json and ``` from result_text
        result_text = result_text.strip("```json").strip("```")
        # Parse the result_text as JSON
        parsed_result = json.loads(result_text)

        print(parsed_result)

        # Write the parsed_result to a JSON file
        with open('event_details.json', 'w') as json_file:
            json.dump(parsed_result, json_file, indent=4)

        send_to_google_calander()
     
        return jsonify({"status": "success", "response": result_text})
    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": str(e)})

def send_to_google_calander():
    # Load the OAuth credentials JSON
    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    credentials = service_account.Credentials.from_service_account_file(
        'balmy-parser-441323-n2-f5a5089d889d.json', scopes=SCOPES
    )

    # Initialize the Calendar API
    service = build("calendar", "v3", credentials=credentials)

    calendar_id = "dominic.hill.eng@gmail.com"
    with open('event_details.json', 'r') as file:
        events = json.load(file)

    for event in events:
        event_result = service.events().insert(calendarId=calendar_id, body=event).execute()
        print(f"Event created: {event_result.get('htmlLink')}")





# Run the app

if __name__ == '__main__':
    app.run(debug=True, port=env.get("PORT", 5000))

