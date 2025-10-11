from fastapi import FastAPI
from pydantic import BaseModel
from .hibp import pwned_count

app = FastAPI(title="PassCheck API", version="0.1.0")

class CheckRequest(BaseModel):
    password: str

@app.post("/check")
def check(req: CheckRequest):
    count = pwned_count(req.password)
    return {"pwned": count > 0, "count": count}
