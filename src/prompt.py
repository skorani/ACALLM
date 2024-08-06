import openai
import json
import os

# Set the API key and base URL
openai.api_key = "nokeyneeded"
openai.api_base = "http://127.0.0.1:11434/v1"

# Read JSON file from the 'data' folder
json_file_path = os.path.join("data", "meetings_data.json")
with open(json_file_path, "r") as f:
    meeting_data = json.load(f)

# Ask user for mood and time zone
mood = input("Please enter your current mood: ")
time_zone = input("Please enter your time zone: ")
filtered_meetings = [
    meeting for meeting in meeting_data if meeting["time_zone"] == time_zone
]

# Refactored lines
prompt = (
    f"You are an ACA flow traveler.\n"
    f"The user is currently feeling {mood}.\n"
    f"The user's time zone is {time_zone}.\n"
    f"Here are the available meetings in the user's time zone: "
    f"{filtered_meetings}\n"
    f"Considering the user's mood and time zone, offer a suitable meeting time "
    f"from the available data.\n"
    f"Think step-by-step to ensure the meeting time is convenient for the user."
)

response = openai.ChatCompletion.create(
    model="llama3.1",
    temperature=0.7,
    n=1,
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": " Meeting Secretary: "},
    ],
)

print("Response:")
print(response.choices[0].message["content"])
