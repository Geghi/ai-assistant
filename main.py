from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.v1.endpoints import telegram
from services.scheduler_service import start_scheduler, shutdown_scheduler
from utils.http_client import HttpClient

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager to handle startup and shutdown events.
    """
    start_scheduler()
    yield
    shutdown_scheduler()
    await HttpClient.close_client()

app = FastAPI(
    title="AI Assistant POC",
    description="A Proof of Concept for an AI assistant using FastAPI, Telegram, and OpenAI.",
    version="0.1.0",
    lifespan=lifespan
)

# Include the API router
app.include_router(telegram.router, prefix="/api/v1", tags=["telegram"])

@app.get("/", tags=["Root"])
async def read_root():
    """
    Root endpoint to check if the API is running.
    """
    return {"message": "Welcome to the AI Assistant API"}
