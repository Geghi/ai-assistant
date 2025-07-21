from fastapi import Depends
from httpx import AsyncClient
from services.telegram_service import TelegramService
from services.google_service import GoogleService
from services.openai_service import OpenAIService
from utils.http_client import get_http_client
from typing import AsyncGenerator

def get_telegram_service(client: AsyncClient = Depends(get_http_client)) -> TelegramService:
    return TelegramService(client)

def get_google_service() -> GoogleService:
    return GoogleService()

def get_openai_service() -> OpenAIService:
    return OpenAIService()
