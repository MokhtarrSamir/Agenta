import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import ValidationError

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.database import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    settings = get_settings()
except ValidationError as exc:
    missing = [str(err["loc"][0]) for err in exc.errors() if err["type"] == "missing"]
    raise SystemExit(
        "Configuration error: missing required environment variable(s): "
        f"{', '.join(missing)}. Set them in the root .env file "
        "(see .env.example) or export them in your shell."
    ) from None
except Exception as exc:
    raise SystemExit(f"Configuration error: {exc}") from None


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await db.connect()
    except Exception:
        logger.exception(
            "Failed to connect to MongoDB/Qdrant at startup; "
            "the /health endpoint will report per-service status."
        )
    yield
    await db.close()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/", tags=["root"])
async def root() -> dict:
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "health": f"{settings.API_V1_PREFIX}/health",
    }