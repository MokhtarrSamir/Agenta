import logging

from motor.motor_asyncio import AsyncIOMotorClient
from qdrant_client import AsyncQdrantClient

from app.core.config import Settings, get_settings

logger = logging.getLogger(__name__)


class Database:
    """Holds the async MongoDB and Qdrant clients plus connectivity checks."""

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()
        self.mongo: AsyncIOMotorClient | None = None
        self.qdrant: AsyncQdrantClient | None = None

    async def connect(self) -> None:
        if self.mongo is None:
            self.mongo = AsyncIOMotorClient(
                self._settings.MONGODB_URI,
                serverSelectionTimeoutMS=3000,
            )
        if self.qdrant is None:
            self.qdrant = AsyncQdrantClient(
                url=self._settings.QDRANT_URL,
                port=self._settings.QDRANT_PORT,
                timeout=3.0,
            )

    async def close(self) -> None:
        if self.mongo is not None:
            self.mongo.close()
            self.mongo = None
        if self.qdrant is not None:
            await self.qdrant.close()
            self.qdrant = None

    async def check_mongo(self) -> bool:
        if self.mongo is None:
            return False
        try:
            await self.mongo.admin.command("ping")
            return True
        except Exception:
            logger.exception("MongoDB connectivity check failed")
            return False

    async def check_qdrant(self) -> bool:
        if self.qdrant is None:
            return False
        try:
            await self.qdrant.get_collections()
            return True
        except Exception:
            logger.exception("Qdrant connectivity check failed")
            return False


db = Database()