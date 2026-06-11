import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import api_router
from app.db.connection import get_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_connection()
    yield


app = FastAPI(title="PyVenturer API", version="0.1.0", lifespan=lifespan)

allowed_origins = [
    origin.strip()
    for origin in os.environ.get("PYVENTURER_ALLOWED_ORIGINS", "").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
