from fastapi import HTTPException, Header
from typing import Optional
from backend.storage import TOKENS
import time

def verify_token(token: str) -> Optional[str]:
    if not token:
        return None
    info = TOKENS.get(token)
    if not info or info["expires"] < time.time():
        return None
    return info["user"]

def get_current_user(authorization: Optional[str] = Header(None, alias="Authorization")):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token missing")
    token = authorization.replace("Bearer ", "").strip()
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="invalid token")
    return user