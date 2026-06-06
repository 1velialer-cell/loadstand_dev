from fastapi import HTTPException
from backend.storage import TOKENS
import time

def verify_token(token: str):
    if not token:
        return None
    info = TOKENS.get(token)
    if not info or info["expires"] < time.time():
        return None
    return info["user"]


def get_current_user(token: str):
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="invalid token")
    return user