from fastapi import APIRouter, FastAPI

router = APIRouter()

app = FastAPI()


@router.get("/")
async def main_route():
    return {"data": "Hello world"}


app.mount("/api/v1", app=router)
