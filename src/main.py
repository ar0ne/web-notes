from fastapi import FastAPI

from src.api import api_router

app = FastAPI()

api = FastAPI(
    title="webnotes",
    description="Welcome to Web note's API documentation!",
    root_path="/api/v1",
    docs_url=None,
    openapi_url="/docs/openapi.json",
    redoc_url="/docs",
)
# we add all API routes to the Web API framework
api.include_router(api_router)
app.mount("/api/v1", app=api)
