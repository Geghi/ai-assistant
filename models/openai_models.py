from pydantic import BaseModel
from typing import List, Literal

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
