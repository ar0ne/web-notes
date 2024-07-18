import logging

from motor.motor_asyncio import AsyncIOMotorClient

from src.config import get_settings


class DataBase:
    client: AsyncIOMotorClient = None


db = DataBase()


async def get_database() -> AsyncIOMotorClient:
    return db.client


async def connect_to_mongo():
    logging.info("Connecting to database...")
    settings = get_settings()
    db.client = AsyncIOMotorClient(
        settings.mongodb_url,
        maxPoolSize=settings.max_connections_count,
        minPoolSize=settings.min_connections_count,
    )
    logging.info("Database connected！")


async def close_mongo_connection():
    logging.info("Closing database connection...")
    db.client.close()
    logging.info("Database closed！")
