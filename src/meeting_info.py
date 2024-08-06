import requests
import fitz  # PyMuPDF
import json
import os

# URL to fetch the data
url = "https://adultchildren.org/meetings.php?meetingFilter=all"
response = requests.get(url)

# Check response status
if response.status_code != 200:
    print(f"Failed to fetch the URL: {response.status_code}")
    exit()

# Verify Content-Type
if "application/pdf" not in response.headers["Content-Type"]:
    print(f"Unexpected Content-Type: {response.headers['Content-Type']}")
    exit()

# Save the PDF content to a file
pdf_path = "meetings_data.pdf"
with open(pdf_path, "wb") as f:
    f.write(response.content)

# Open the PDF file
pdf_document = fitz.open(pdf_path)

# Extract text from the PDF
text = ""
for page_num in range(len(pdf_document)):
    page = pdf_document.load_page(page_num)
    text += page.get_text()

# Ensure the text is UTF-8 encoded
text = text.encode("utf-8").decode("utf-8")

# Structure the data into a nested JSON-compatible format
lines = text.split("\n")
data = {}
current_meeting_id = None

for line in lines:
    if line.strip():  # Skip empty lines
        if "Meeting ID:" in line:
            current_meeting_id = line.split(":", 1)[1].strip()
            data[current_meeting_id] = {
                "MeetingID": current_meeting_id,
                "MeetingTime": {},
                "Notes": [],
                "AdditionalInfo": {},
            }
        elif current_meeting_id:
            key_value = line.split(":", 1)
            if len(key_value) == 2:
                key = key_value[0].strip()
                value = key_value[1].strip()
                if key == "ZoomLink":
                    data[current_meeting_id]["ZoomLink"] = value
                elif key == "Meeting Local Time":
                    data[current_meeting_id]["LocalTime"] = value
                elif key == "Focus":
                    data[current_meeting_id]["Focus"] = value
                elif key == "Format":
                    data[current_meeting_id]["Format"] = value
                elif key == "Notes":
                    data[current_meeting_id]["Notes"].append(value)
                elif key in [
                    "Link",
                    "Email",
                    "email",
                    "MeetingPassword",
                    "Telegram",
                    "Pass-code",
                    "Passcode",
                ]:
                    data[current_meeting_id]["AdditionalInfo"][key] = value
                elif key.startswith("Meeting Time"):
                    # Assuming the format is "Meeting Time (Timezone): Time"
                    timezone = key.split("(", 1)[1].rstrip(")")
                    data[current_meeting_id]["MeetingTime"][timezone] = value
                elif key == "Day":
                    data[current_meeting_id]["Day"] = value

# Ensure the 'data' directory exists
os.makedirs("data", exist_ok=True)

# Save the structured data to a JSON file in the 'data' directory
json_file_path = os.path.join("data", "meetings_data.json")
with open(json_file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Extracted text has been saved to {json_file_path}")
