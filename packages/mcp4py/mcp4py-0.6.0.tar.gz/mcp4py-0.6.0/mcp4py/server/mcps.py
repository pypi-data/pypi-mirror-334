from fastapi import FastAPI
from .api import items
from .config import settings

app = FastAPI(
    title=settings.app_name,
    description="A simple mcp4py server.",
    version="0.1.0",
)

app.include_router(items.router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}