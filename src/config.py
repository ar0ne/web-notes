import logging

from starlette.config import Config

config = Config(".env")

LOG_LEVEL = config("LOG_LEVEL", default=logging.WARNING)
ENV = config("ENV", default="local")

MAX_CONNECTIONS_COUNT = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)
MIN_CONNECTIONS_COUNT = config("MIN_CONNECTIONS_COUNT", cast=int, default=10)

MONGODB_USERNAME = config("MONGODB_USERNAME", default="")
MONGODB_PASSWORD = config("MONGODB_PASSWORD", default="")
MONGODB_HOST = config("MONGODB_HOST", default="")
MONGODB_PORT = config("MONGODB_PORT", cast=int, default=27017)
MONGODB_DATABASE = config("MONGODB_DATABASE", default="app")

MONGODB_URL = f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}/{MONGODB_DATABASE}?retryWrites=true&w=majority&authSource=admin"

MONGODB_NOTE_COLLECTION = config("NOTE_COLLECTION", default="notes")
