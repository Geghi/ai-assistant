import logging
import os.path
from typing import List, Dict, Any, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

class CalendarService:
    def __init__(self):
        logging.info("Initializing CalendarService.")
        self.creds = self._authenticate()
        self.service = build("calendar", "v3", credentials=self.creds)

    def _authenticate(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        return creds

    def create_event(self, summary: str, start_time: str, end_time: str, attendees: List[str], description: Optional[str] = None) -> Dict[str, Any]:
        """
        Creates a new calendar event.
        start_time and end_time should be in ISO format (e.g., '2025-07-25T09:00:00-07:00')
        """
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_time,
                'timeZone': 'Europe/Rome', # Assuming a default timezone
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'Europe/Rome',
            },
            'attendees': [{'email': att} for att in attendees],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
        try:
            event = self.service.events().insert(calendarId='primary', body=event).execute()
            logging.info(f"Event created: {event.get('htmlLink')}")
            return {"status": "success", "message": f"Event created: {event.get('htmlLink')}", "event_id": event.get('id')}
        except HttpError as error:
            logging.error(f"An error occurred: {error}")
            return {"status": "error", "message": f"Failed to create event: {error}"}

    def find_available_slots(self, start_time: str, end_time: str, duration_minutes: int, attendees: List[str]) -> List[str]:
        """
        Finds available time slots for a meeting.
        This is a more complex operation requiring free/busy queries.
        For simplicity, this will return dummy data or require more detailed implementation.
        """
        logging.warning("find_available_slots is a placeholder and needs full implementation.")
        # Example of a free/busy query structure
        body = {
            "timeMin": start_time,
            "timeMax": end_time,
            "items": [{"id": 'primary'}] + [{"id": att} for att in attendees]
        }
        try:
            response = self.service.freebusy().query(body=body).execute()
            # Process response to find actual free slots
            # This is a simplified placeholder
            return ["2025-07-22T10:00:00Z", "2025-07-22T14:00:00Z"]
        except HttpError as error:
            logging.error(f"An error occurred: {error}")
            return []

    def reschedule_event(self, event_id: str, new_start_time: str, new_end_time: str) -> Dict[str, Any]:
        """
        Reschedules an existing calendar event.
        """
        try:
            event = self.service.events().get(calendarId='primary', eventId=event_id).execute()
            event['start']['dateTime'] = new_start_time
            event['end']['dateTime'] = new_end_time
            updated_event = self.service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
            logging.info(f"Event rescheduled: {updated_event.get('htmlLink')}")
            return {"status": "success", "message": f"Event rescheduled: {updated_event.get('htmlLink')}"}
        except HttpError as error:
            logging.error(f"An error occurred: {error}")
            return {"status": "error", "message": f"Failed to reschedule event: {error}"}

    def delete_event(self, event_id: str) -> Dict[str, Any]:
        """
        Deletes a calendar event.
        """
        try:
            self.service.events().delete(calendarId='primary', eventId=event_id).execute()
            logging.info(f"Event {event_id} deleted.")
            return {"status": "success", "message": f"Event {event_id} deleted."}
        except HttpError as error:
            logging.error(f"An error occurred: {error}")
            return {"status": "error", "message": f"Failed to delete event: {error}"}
