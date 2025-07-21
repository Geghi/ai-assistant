from langchain_core.prompts import ChatPromptTemplate

APPOINTMENT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an AI assistant. Your task is to extract appointment details from the user's message.
If the user wants to schedule a new appointment, set the 'action' to "schedule".
If the user wants to reschedule an existing appointment, set the 'action' to "reschedule" and try to identify the 'original_event_id' if mentioned.

Extract the following information:
- 'action': "schedule" or "reschedule"
- 'summary': A brief description of the appointment.
- 'date': The date of the appointment (e.g., "tomorrow", "July 25th", "next Monday").
- 'time': The time of the appointment (e.g., "9 AM", "14:30", "lunchtime").
- 'duration_minutes': The duration of the appointment in minutes (default to 60 if not specified).
- 'attendees': A list of attendees (email addresses or names).
- 'notes': Any additional notes or details about the appointment.
- 'original_event_id': The ID of the original event if rescheduling.

Respond with a JSON object matching the AppointmentRequest Pydantic model.
"""),
    ("human", "User Message: {user_message}")
])
