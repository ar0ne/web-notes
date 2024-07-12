from fastapi import FastAPI

from src.api import api_router
from src.database import connect_to_mongo, close_mongo_connection

app = FastAPI()

api = FastAPI(
    title="webnotes",
    description="Welcome to Web note's API documentation!",
    root_path="/api/v1",
    docs_url=None,
    openapi_url="/docs/openapi.json",
    redoc_url="/docs",
)

# hooks for mongo
app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

# we add all API routes to the Web API framework
api.include_router(api_router)
app.mount("/api/v1", app=api)
