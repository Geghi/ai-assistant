import httpx
from contextlib import asynccontextmanager
from typing import AsyncGenerator

class HttpClient:
    _client: httpx.AsyncClient | None = None

    @classmethod
    def get_client(cls) -> httpx.AsyncClient:
        if cls._client is None:
            cls._client = httpx.AsyncClient()
        return cls._client

    @classmethod
    async def close_client(cls):
        if cls._client:
            await cls._client.aclose()
            cls._client = None

async def get_http_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    """
    Dependency to get a shared httpx.AsyncClient instance.
    The client is closed automatically on exit.
    """
    client = HttpClient.get_client()
    yield client
