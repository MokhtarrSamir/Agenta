from fastapi import APIRouter

from app.core.database import db

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check() -> dict:
    mongo_ok = await db.check_mongo()
    qdrant_ok = await db.check_qdrant()
    return {
        "api": "ok",
        "mongodb": "ok" if mongo_ok else "unreachable",
        "qdrant": "ok" if qdrant_ok else "unreachable",
    }