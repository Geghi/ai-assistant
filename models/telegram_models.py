from pydantic import BaseModel, Field
from typing import Optional, List

# Basic Telegram Objects

class User(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None

class Chat(BaseModel):
    id: int
    type: str
    title: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class Voice(BaseModel):
    file_id: str
    file_unique_id: str
    duration: int
    mime_type: Optional[str] = None
    file_size: Optional[int] = None

class Message(BaseModel):
    message_id: int
    from_user: Optional[User] = Field(None, alias='from')
    chat: Chat
    date: int
    text: Optional[str] = None
    voice: Optional[Voice] = None

    # Removed Config class, Pydantic V2 uses model_config or Field aliases

class Update(BaseModel):
    update_id: int
    message: Optional[Message] = None
    edited_message: Optional[Message] = None
    channel_post: Optional[Message] = None
    edited_channel_post: Optional[Message] = None

# Custom models for our application

class TelegramWebhook(BaseModel):
    """
    Model for the incoming webhook from Telegram.
    This is the top-level object.
    """
    update: Update
