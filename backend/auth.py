from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import secrets, time
from typing import Dict
from .storage import USERS, TOKENS

router = APIRouter()
TOKEN_LIFETIME = 24 * 3600

class Creds(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(creds: Creds):
    u, p = creds.username.strip(), creds.password.strip()
    if not u or not p or u not in USERS or USERS[u]["password"] != p:
        raise HTTPException(status_code=401, detail="Неверные логин или пароль")
    
    token = secrets.token_urlsafe(32)
    TOKENS[token] = {"user": u, "expires": time.time() + TOKEN_LIFETIME}
    return {"token": token, "expires_in": TOKEN_LIFETIME}

@router.post("/refresh")
def refresh(token: str):
    info = TOKENS.get(token)
    if not info or info["expires"] < time.time():
        raise HTTPException(status_code=401, detail="invalid token")
    TOKENS.pop(token, None)
    new_token = secrets.token_urlsafe(32)
    TOKENS[new_token] = {"user": info["user"], "expires": time.time() + TOKEN_LIFETIME}
    return {"token": new_token, "expires_in": TOKEN_LIFETIME}

def verify_token(token: str):
    info = TOKENS.get(token)
    if not info or info["expires"] < time.time():
        return None
    return info["user"]