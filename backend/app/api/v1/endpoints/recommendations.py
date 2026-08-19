from fastapi import APIRouter

router = APIRouter()

@router.post("/generate")
async def generate_recommendations():
    return {"message": "coming in Phase 2"}
