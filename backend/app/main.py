from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.database import init_db
from app.core.embeddings import EmbeddingService
from app.services.llm import get_llm_service
from app.api.v1.router import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    app.state.embedding_service = EmbeddingService()
    app.state.embedding_service.load()
    app.state.llm_service = get_llm_service()
    yield

app = FastAPI(title="Pathfinder API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"name": "Pathfinder API", "version": "0.1.0"}
