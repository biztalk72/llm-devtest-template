"""Ollama client for LLM interactions."""

from typing import Any, AsyncIterator, Dict, List, Optional

import ollama
from ollama import AsyncClient

from src.config import Settings


class OllamaService:
    """Service for interacting with Ollama LLMs."""

    def __init__(self, settings: Settings) -> None:
        """Initialize Ollama service."""
        self.settings = settings
        self.client = AsyncClient(host=settings.ollama_host)
        self.model = settings.ollama_model

    async def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Generate text from a prompt."""
        messages: List[Dict[str, str]] = []

        if system:
            messages.append({"role": "system", "content": system})

        messages.append({"role": "user", "content": prompt})

        response = await self.client.chat(
            model=self.model,
            messages=messages,
            options={"temperature": temperature, "num_predict": max_tokens or -1},
        )

        return response["message"]["content"]

    async def generate_stream(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
    ) -> AsyncIterator[str]:
        """Generate text from a prompt with streaming."""
        messages: List[Dict[str, str]] = []

        if system:
            messages.append({"role": "system", "content": system})

        messages.append({"role": "user", "content": prompt})

        async for chunk in await self.client.chat(
            model=self.model,
            messages=messages,
            stream=True,
            options={"temperature": temperature},
        ):
            if "message" in chunk and "content" in chunk["message"]:
                yield chunk["message"]["content"]

    async def list_models(self) -> List[str]:
        """List available models."""
        models = await self.client.list()
        return [model["name"] for model in models.get("models", [])]

    async def health_check(self) -> bool:
        """Check if Ollama is accessible."""
        try:
            await self.list_models()
            return True
        except Exception:
            return False
