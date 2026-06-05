import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.auth import router as auth_router
from backend.api import router as api_router
from backend.start import router as start_router
from backend.config import settings

app = FastAPI(title="Loadstand")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth")
app.include_router(api_router, prefix="/api")
app.include_router(start_router, prefix="/api")

# Статические файлы
app.mount("/static", StaticFiles(directory=settings.FRONTEND_DIR), name="static")

@app.get("/", include_in_schema=False)
def root():
    return FileResponse(settings.FRONTEND_DIR / "index.html")

@app.get("/api/logo", include_in_schema=False)
def get_logo():
    if not settings.LOGO_PATH.exists():
        return {"error": "logo not found"}
    return FileResponse(settings.LOGO_PATH, media_type="image/svg+xml")

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host=settings.HOST, 
        port=settings.PORT, 
        reload=True
    )