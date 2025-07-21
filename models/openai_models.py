from pydantic import BaseModel
from typing import List, Literal, Optional

class EmailSummary(BaseModel):
    """
    Represents the summary of a single email.
    """
    classification: Literal["Urgent", "FYI", "Spam", "Unknown"]
    summary: str
    is_construction_related: bool
    original_sender: str
    original_subject: str

class DailySummary(BaseModel):
    """
    Represents the daily summary of all processed emails.
    """
    summaries: List[EmailSummary]
    total_emails_processed: int
    report_date: str

class Transcription(BaseModel):
    """
    Represents the transcription of a voice note.
    """
    text: str

class EmailDraft(BaseModel):
    """
    Represents a drafted email based on a voice note.
    """
    subject: str
    body: str
    recipient: str # The user might specify this in the voice note

class AppointmentRequest(BaseModel):
    """
    Represents a request to schedule or reschedule an appointment.
    """
    action: Literal["schedule", "reschedule"]
    summary: str
    date: str # e.g., "tomorrow", "July 25th", "next Monday"
    time: str # e.g., "9 AM", "14:30", "lunchtime"
    duration_minutes: int = 60
    attendees: List[str] = [] # Email addresses or names
    notes: str = ""
    original_event_id: Optional[str] = None # For rescheduling

class ConstructionIssue(BaseModel):
    """
    Represents a reported construction site issue.
    """
    urgency: Literal["urgent", "routine"]
    description: str
    location: str # e.g., "Site A", "Building 3, Floor 2"
    reported_by: str # Name or email of the person reporting
    action_required: str # e.g., "notify site manager", "schedule for daily briefing"
