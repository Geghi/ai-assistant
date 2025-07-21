import httpx
from core.config import settings
import logging

class TelegramService:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client
        self.telegram_api_url = f"https://api.telegram.org/bot{settings.telegram_token}"

    async def send_message(self, chat_id: int, text: str):
        """
        Sends a text message to a specified Telegram chat.
        """
        response = await self.client.post(
            f"{self.telegram_api_url}/sendMessage",
            json={"chat_id": chat_id, "text": text},
        )
        if response.status_code != 200:
            logging.error(f"Error sending message to Telegram: {response.text}")
            response.raise_for_status()

    async def get_file_path(self, file_id: str) -> str | None:
        """
        Gets the file path of a file from Telegram.
        """
        response = await self.client.get(f"{self.telegram_api_url}/getFile", params={"file_id": file_id})
        if response.status_code != 200:
            logging.error(f"Could not get file path from Telegram: {response.text}")
            return None
        
        data = response.json()
        return data.get("result", {}).get("file_path")

    async def download_file(self, file_path: str) -> bytes | None:
        """
        Downloads a file from Telegram.
        """
        file_url = f"https://api.telegram.org/file/bot{settings.telegram_token}/{file_path}"
        response = await self.client.get(file_url)
        if response.status_code != 200:
            logging.error(f"Could not download file from Telegram: {response.text}")
            return None
        
        return response.content
