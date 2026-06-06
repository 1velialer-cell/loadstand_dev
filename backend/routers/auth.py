from fastapi import APIRouter, HTTPException
from backend.models.schemas import Creds
from backend.storage import USERS, TOKENS
import secrets
import time
from backend.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(creds: Creds):
    u = creds.username.strip()
    p = creds.password.strip()
    
    if not u or not p or u not in USERS or USERS[u]["password"] != p:
        raise HTTPException(status_code=401, detail="Неверные логин или пароль")
    
    token = secrets.token_urlsafe(32)
    TOKENS[token] = {
        "user": u, 
        "expires": time.time() + settings.TOKEN_LIFETIME
    }
    
    return {
        "token": token, 
        "expires_in": settings.TOKEN_LIFETIME,
        "user": u
    }