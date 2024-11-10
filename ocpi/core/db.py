from motor import motor_asyncio, core

from ocpi.core.config import settings


class _MongoClientSingleton:
    mongo_client: motor_asyncio.AsyncIOMotorClient | None

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(_MongoClientSingleton, cls).__new__(cls)
            cls.instance.mongo_client = motor_asyncio.AsyncIOMotorClient(
                settings.MONGODB_URI
            )
        return cls.instance


def get_db() -> core.AgnosticDatabase:
    return _MongoClientSingleton().mongo_client[settings.DB_NAME]


async def ping():
    await get_db().command("ping")


def client_close():
    return _MongoClientSingleton().mongo_client


__all__ = ["client_close", "get_db", "ping"]
