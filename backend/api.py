from fastapi import APIRouter, Header, HTTPException, Depends
from .auth import verify_token
from pydantic import BaseModel

router = APIRouter()

def require_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="missing token")
    token = authorization.split(" ", 1)[1]
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="invalid token")
    return user

class Status(BaseModel):
    value: float

state = {
    "smoke": 0.0,
    "loading": 0.0,
    "stability": 0.0
}

@router.get("/status")
def get_status(user=Depends(require_user)):
    return state

@router.post("/status/{field}")
def set_status(field: str, payload: Status, user=Depends(require_user)):
    if field not in state:
        raise HTTPException(status_code=400, detail="unknown field")
    state[field] = payload.value
    return {"ok": True}


