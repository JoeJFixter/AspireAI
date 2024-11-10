import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json

# Load the OAuth credentials JSON
SCOPES = ["https://www.googleapis.com/auth/calendar"]
credentials = service_account.Credentials.from_service_account_file(
    'balmy-parser-441323-n2-f5a5089d889d.json', scopes=SCOPES
)

# Initialize the Calendar API
service = build("calendar", "v3", credentials=credentials)

# # Example of creating a calendar event
# event = 
# {
#     'summary': 'Meeting with Bob',
#     'location': '123 Main St, Anytown, USA',
#     'description': 'Discuss project updates and next steps.',
#     'start': {
#         'dateTime': '2023-10-01T10:00:00-07:00',
#         'timeZone': 'America/Los_Angeles',
#     },
#     'end': {
#         'dateTime': '2023-10-01T11:00:00-07:00',
#         'timeZone': 'America/Los_Angeles',
#     },
#     'attendees': [
#         {'email': 'bob@example.com'},
#     ],
#     'reminders': {
#         'useDefault': False,
#         'overrides': [
#             {'method': 'email', 'minutes': 24 * 60},
#             {'method': 'popup', 'minutes': 10},
#         ],
#     },
# }
# Load event details from an external JSON file

calendar_id = "dominic.hill.eng@gmail.com"
with open('event_details.json', 'r') as file:
    events = json.load(file)

    for event in events:
        event_result = service.events().insert(calendarId=calendar_id, body=event).execute()
        print(f"Event created: {event_result.get('htmlLink')}")

# # Add the event to the calendar
# calendar_id = "dominic.hill.eng@gmail.com"
# event_result = service.events().insert(calendarId=calendar_id, body=event).execute()
# print(f"Event created: {event_result.get('htmlLink')}")
