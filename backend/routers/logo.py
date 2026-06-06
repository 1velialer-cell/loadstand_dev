from fastapi import APIRouter
from fastapi.responses import FileResponse
from backend.core.config import settings

router = APIRouter(tags=["static"])

@router.get("/logo")
async def get_logo():
    if settings.LOGO_PATH.exists():
        return FileResponse(settings.LOGO_PATH)
    else:
        return {"error": "Logo not found"}, 404