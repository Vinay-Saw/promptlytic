from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from .settings import settings
from .quiz_solver import solve_chain

app = FastAPI(title="Promptlytic Agent")

class RunPayload(BaseModel):
    email: str
    secret: str
    url: str

@app.post("/run")
async def run(payload: RunPayload, request: Request):
    body = await request.body()
    if len(body) > settings.MAX_PAYLOAD_BYTES:
        raise HTTPException(status_code=400, detail="Payload too large")
    valid = [s.strip() for s in settings.VALID_SECRETS.split(",") if s.strip()]
    if payload.secret not in valid:
        raise HTTPException(status_code=403, detail="Invalid secret")
    try:
        result = solve_chain(payload.url, max_total_seconds=settings.MAX_EXECUTION_SECONDS)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Solver crashed: {e}")
    return JSONResponse(result)
