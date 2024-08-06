import os
import requests
import fitz  # PyMuPDF
import json


class MeetingInfoExtractor:
    def __init__(self, url, pdf_path, json_path):
        self.url = url
        self.pdf_path = pdf_path
        self.json_path = json_path

    def fetch_data(self):
        response = requests.get(self.url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch the URL: {response.status_code}")
        if "application/pdf" not in response.headers["Content-Type"]:
            raise Exception(
                f"Unexpected Content-Type: {response.headers['Content-Type']}"
            )
        return response.content

    def save_pdf(self, content):
        with open(self.pdf_path, "wb") as f:
            f.write(content)

    def extract_text_from_pdf(self):
        pdf_document = fitz.open(self.pdf_path)
        text = ""
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
        return text.encode("utf-8").decode("utf-8")

    def parse_text(self, text):
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
        return data

    def save_to_json(self, data):
        os.makedirs(os.path.dirname(self.json_path), exist_ok=True)
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def run(self):
        content = self.fetch_data()
        self.save_pdf(content)
        text = self.extract_text_from_pdf()
        data = self.parse_text(text)
        self.save_to_json(data)
        print(f"Extracted text has been saved to {self.json_path}")


if __name__ == "__main__":
    url = "https://adultchildren.org/meetings.php?meetingFilter=all"
    pdf_path = "meetings_data.pdf"
    json_path = os.path.join("data", "meetings_data.json")

    extractor = MeetingInfoExtractor(url, pdf_path, json_path)
    extractor.run()
