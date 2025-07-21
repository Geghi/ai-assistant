from google.cloud import speech
from google.oauth2 import service_account
import json
import logging
from core.config import settings

class GoogleService:
    def __init__(self):
        self.credentials = None
        if settings.GOOGLE_SERVICE_ACCOUNT_CREDENTIALS_JSON:
            try:
                info = json.loads(settings.GOOGLE_SERVICE_ACCOUNT_CREDENTIALS_JSON)
                self.credentials = service_account.Credentials.from_service_account_info(info)
            except json.JSONDecodeError as e:
                logging.error(f"Error decoding Google service account credentials JSON: {e}")
                raise ValueError("Invalid Google service account credentials JSON format.")
            except Exception as e:
                logging.error(f"Error loading Google service account credentials: {e}")
                raise

    async def transcribe_audio(self, audio_content: bytes) -> str:
        """
        Transcribes the given audio content using Google Cloud Speech-to-Text.
        """
        logging.info("Start google transcription...")

        if self.credentials:
            client = speech.SpeechAsyncClient(credentials=self.credentials)
        else:
            client = speech.SpeechAsyncClient()

        audio = speech.RecognitionAudio(content=audio_content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
            sample_rate_hertz=48000,
            language_code="en-US",
        )

        response = await client.recognize(config=config, audio=audio)
        logging.info(f"Transcribed text: {response}")

        if not response.results:
            return ""

        return response.results[0].alternatives[0].transcript
