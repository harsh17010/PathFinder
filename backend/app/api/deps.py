from fastapi import Depends, Request
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.embeddings import EmbeddingService
from app.services.llm import LLMService

def get_embedding_service(request: Request) -> EmbeddingService:
    return request.app.state.embedding_service

def get_llm_service(request: Request) -> LLMService:
    return request.app.state.llm_service
