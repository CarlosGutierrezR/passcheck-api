import logging
import os

from fastapi import FastAPI
from pydantic import BaseModel
import redis

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [logger] %(message)s",
)

REDIS_URL = os.getenv("REDIS_URL", "redis://cache:6379/0")
r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

app = FastAPI(title="PassCheck Logger", version="0.1.0")


class LogEntry(BaseModel):
    level: str = "INFO"
    message: str


@app.post("/log")
def log(entry: LogEntry):
    level = getattr(logging, entry.level.upper(), logging.INFO)
    logging.log(level, entry.message)
    r.lpush("passcheck:logs", f"{entry.level.upper()} {entry.message}")
    return {"status": "ok"}
