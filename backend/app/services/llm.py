import httpx
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from app.core.config import settings

class LLMService(ABC):
    @abstractmethod
    async def generate(self, prompt: str, system_prompt: str) -> str:
        pass
    @abstractmethod
    async def generate_structured(self, prompt: str, schema: Dict[str, Any]) -> dict:
        pass
    @abstractmethod
    async def chat(self, messages: List[Dict[str, str]]) -> str:
        pass

class OllamaProvider(LLMService):
    async def generate(self, prompt: str, system_prompt: str = "") -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{settings.OLLAMA_BASE_URL}/api/chat", json={
                "model": settings.OLLAMA_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "stream": False
            })
            response.raise_for_status()
            return response.json()["message"]["content"]

    async def generate_structured(self, prompt: str, schema: Dict[str, Any]) -> dict:
        # Simple implementation, real one would enforce JSON schema via prompt or tools
        raise NotImplementedError("generate_structured not yet implemented")

    async def chat(self, messages: List[Dict[str, str]]) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{settings.OLLAMA_BASE_URL}/api/chat", json={
                "model": settings.OLLAMA_MODEL,
                "messages": messages,
                "stream": False
            })
            response.raise_for_status()
            return response.json()["message"]["content"]

class ClaudeProvider(LLMService):
    async def generate(self, prompt: str, system_prompt: str) -> str:
        raise NotImplementedError("Claude provider not yet implemented")
    async def generate_structured(self, prompt: str, schema: Dict[str, Any]) -> dict:
        raise NotImplementedError("Claude provider not yet implemented")
    async def chat(self, messages: List[Dict[str, str]]) -> str:
        raise NotImplementedError("Claude provider not yet implemented")

def get_llm_service() -> LLMService:
    return OllamaProvider()
