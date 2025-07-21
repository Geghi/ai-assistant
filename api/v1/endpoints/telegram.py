from fastapi import APIRouter, Body, HTTPException, Depends
from models.telegram_models import Update
from services.telegram_service import TelegramService
from services.google_service import GoogleService
from services.openai_service import OpenAIService
from core.config import settings
from core.agent_graph import process_telegram_update
from api.v1.dependencies import get_telegram_service, get_google_service, get_openai_service
import logging
import tempfile
import os

router = APIRouter()

async def _transcribe_voice_message(
    update: Update,
    telegram_service: TelegramService,
    google_service: GoogleService,
    openai_service: OpenAIService,
) -> str | None:
    if not update.message or not update.message.voice:
        return None

    file_id = update.message.voice.file_id
    file_path = await telegram_service.get_file_path(file_id)
    if not file_path:
        logging.error("Could not retrieve file path for voice message.")
        return "[Could not retrieve voice message]"

    audio_content = await telegram_service.download_file(file_path)
    if not audio_content:
        logging.error("Could not download voice message.")
        return "[Could not download voice message]"

    logging.info(f"Transcription provider: {settings.LLM_PROVIDER}")

    if settings.LLM_PROVIDER == "google":
        return await google_service.transcribe_audio(audio_content)
    elif settings.LLM_PROVIDER == "openai":
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as temp_audio_file:
            temp_audio_file.write(audio_content)
            temp_audio_path = temp_audio_file.name
        
        try:
            transcription = await openai_service.transcribe_audio(temp_audio_path)
            return transcription.text
        finally:
            os.remove(temp_audio_path)
    else:
        logging.warning(f"Unsupported transcription provider: {settings.LLM_PROVIDER}")
        return "[Unsupported transcription provider]"

@router.post("/telegram/webhook", summary="Telegram Webhook")
async def telegram_webhook(
    update: Update = Body(...),
    telegram_service: TelegramService = Depends(get_telegram_service),
    google_service: GoogleService = Depends(get_google_service),
    openai_service: OpenAIService = Depends(get_openai_service),
):
    """
    Handles incoming updates from the Telegram webhook.
    """
    chat_id = None
    message_text = None
    message_type = "unsupported"

    if update.message:
        chat_id = update.message.chat.id
        if update.message.text:
            message_text = update.message.text
            message_type = "text"
        elif update.message.voice:
            message_text = await _transcribe_voice_message(
                update, telegram_service, google_service, openai_service
            )
            message_type = "voice"
        else:
            logging.info("Unsupported message type.")
            message_text = "[Unsupported message type]"
    
    if not chat_id or not message_text or message_type == "unsupported":
        if chat_id:
            await telegram_service.send_message(chat_id, "I received your message, but could not process it.")
        return {"status": "received_but_not_processed"}

    try:
        agent_response = await process_telegram_update(message_text, message_type)
        if agent_response:
            await telegram_service.send_message(chat_id, agent_response)
        return {"status": "ok"}
    except Exception as e:
        logging.error(f"Error processing Telegram update: {e}", exc_info=True)
        if chat_id:
            try:
                await telegram_service.send_message(chat_id, f"An internal error occurred: {e}")
            except Exception as send_error:
                logging.error(f"Failed to send error message to Telegram: {send_error}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/telegram/health", summary="Health Check")
async def health_check():
    """
    A simple health check endpoint for the Telegram API.
    """
    return {"status": "ok"}
