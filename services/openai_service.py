from core.config import settings
from models.openai_models import Transcription, EmailSummary, EmailDraft
import openai

class OpenAIService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY

    async def transcribe_audio(self, audio_file_path: str) -> Transcription:
        """
        Transcribes an audio file using the Whisper API.
        """
        print(f"Transcribing audio file: {audio_file_path}")
        with open(audio_file_path, "rb") as audio_file:
            transcript = await openai.Audio.transcribe(
                model=settings.OPENAI_MODEL_TRANSCRIPTION,
                file=audio_file
            )
        return Transcription(text=transcript.text)

    async def summarize_email_content(self, content: str) -> EmailSummary:
        """
        Summarizes and classifies email content using GPT-4o.
        """
        print("Summarizing email content...")
        # Placeholder for summarization logic
        # This would involve a detailed prompt to classify and summarize.
        return EmailSummary(
            classification="FYI",
            summary="This is a placeholder summary.",
            is_construction_related=False,
            original_sender="sender@example.com",
            original_subject="Placeholder Subject"
        )

    async def draft_email_from_text(self, text: str) -> EmailDraft:
        """
        Drafts a polite, professional email from transcribed text.
        """
        print(f"Drafting email from text: {text}")
        # Placeholder for email drafting logic
        # A prompt would instruct the model to create a formal email.
        return EmailDraft(
            subject="Follow-up",
            body="This is a placeholder email body based on the transcription.",
            recipient="recipient@example.com"
        )
