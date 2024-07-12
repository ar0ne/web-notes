import logging

from motor.motor_asyncio import AsyncIOMotorClient

from src import config


class DataBase:
    client: AsyncIOMotorClient = None


db = DataBase()


async def get_database() -> AsyncIOMotorClient:
    return db.client


async def connect_to_mongo():
    logging.info("Connecting to database...")
    db.client = AsyncIOMotorClient(
        config.MONGODB_URL,
        maxPoolSize=config.MAX_CONNECTIONS_COUNT,
        minPoolSize=config.MIN_CONNECTIONS_COUNT,
    )
    logging.info("Database connected！")


async def close_mongo_connection():
    logging.info("Closing database connection...")
    db.client.close()
    logging.info("Database closed！")
