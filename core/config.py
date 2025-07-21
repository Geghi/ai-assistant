from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    """
    Settings for the application.
    Reads environment variables from a .env file.
    """

    # Telegram Bot Token (assuming .env uses 'telegram_token')
    telegram_token: str = Field(..., description="Telegram Bot Token")

    # Telegram Chat ID (if needed globally, otherwise it's dynamic)
    # The error suggests it's in the env, so let's define it.
    telegram_chat_id: Optional[str] = Field(None, description="Default Telegram Chat ID for scheduled reports")

    OPENAI_API_KEY: str = Field(..., description="OpenAI API Key")
    GOOGLE_API_KEY: str = Field(..., description="Google API Key")
    GOOGLE_SERVICE_ACCOUNT_CREDENTIALS_JSON: Optional[str] = Field(None, description="Google Service Account Credentials JSON string")

    # Gmail API credentials
    GMAIL_CREDENTIALS_FILE: str = Field("path/to/your/credentials.json", description="Path to Gmail credentials JSON file")
    TELEGRAM_WEBHOOK_URL: str = Field(..., description="Webhook url")

    # Model configurations
    OPENAI_MODEL_TRANSCRIPTION: str = Field("whisper-1", description="OpenAI model for transcription")
    LLM_PROVIDER: str = Field("google", description="LLM provider ('openai' or 'google')")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

settings = Settings()
