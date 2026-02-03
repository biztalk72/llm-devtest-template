"""Main FastAPI application."""

from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from src.config import get_settings
from src.ollama_client import OllamaService

settings = get_settings()
app = FastAPI(
    title="LLM API with Ollama",
    description="API for interacting with LLMs via Ollama",
    version="0.1.0",
)

ollama_service = OllamaService(settings)


class GenerateRequest(BaseModel):
    """Request model for text generation."""

    prompt: str
    system: Optional[str] = None
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    stream: bool = False


class GenerateResponse(BaseModel):
    """Response model for text generation."""

    text: str


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint."""
    return {
        "message": "LLM API with Ollama",
        "environment": settings.environment,
        "model": settings.ollama_model,
    }


@app.get("/health")
async def health() -> Dict[str, str]:
    """Health check endpoint."""
    is_healthy = await ollama_service.health_check()

    if not is_healthy:
        raise HTTPException(status_code=503, detail="Ollama service unavailable")

    return {"status": "healthy", "ollama": "connected"}


@app.get("/models")
async def list_models() -> Dict[str, Any]:
    """List available models."""
    models = await ollama_service.list_models()
    return {"models": models, "current": settings.ollama_model}


@app.post("/generate")
async def generate(request: GenerateRequest) -> GenerateResponse | StreamingResponse:
    """Generate text from a prompt."""
    try:
        if request.stream:
            return StreamingResponse(
                ollama_service.generate_stream(
                    prompt=request.prompt,
                    system=request.system,
                    temperature=request.temperature,
                ),
                media_type="text/event-stream",
            )

        text = await ollama_service.generate(
            prompt=request.prompt,
            system=request.system,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

        return GenerateResponse(text=text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
    )
