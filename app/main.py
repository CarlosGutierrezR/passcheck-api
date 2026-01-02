# app/main.py
import logging
from fastapi import FastAPI
from pydantic import BaseModel, Field
from app.service import check_password

# --- Logging básico (consola) ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger("passcheck.api")

app = FastAPI(title="PassCheck API", version="0.2.0")

class CheckRequest(BaseModel):
    password: str = Field(..., min_length=1, max_length=512)

class CheckResponse(BaseModel):
    pwned: bool
    count: int

@app.post("/check", response_model=CheckResponse)
def check(req: CheckRequest):
    logger.info("POST /check request received")
    result = check_password(req.password)
    logger.info("POST /check result pwned=%s count=%d", result["pwned"], result["count"])
    return result

@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
