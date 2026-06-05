import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from backend.auth import router as auth_router
from backend.api import router as api_router
from backend.start import router as start_router

app = FastAPI(title="Loadstand")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(auth_router, prefix="/auth")
app.include_router(api_router, prefix="/api")
app.include_router(start_router, prefix="/api")   # ← /api/run-tool будет доступен

# Статические файлы фронтенда
BASE_DIR = os.path.dirname(__file__)
front_dir = os.path.join(BASE_DIR, "frontend")

app.mount("/static", StaticFiles(directory=front_dir), name="static")

@app.get("/", include_in_schema=False)
def root():
    return FileResponse(os.path.join(front_dir, "index.html"))

# Лого
@app.get("/api/logo", include_in_schema=False)
def get_logo():
    logo_path = "/home/redmine/loadstand/logo.svg"
    return FileResponse(logo_path, media_type="image/svg+xml", filename="logo.svg")


if __name__ == "__main__":
    uvicorn.run("main:app", host="192.168.2.128", port=4500, reload=True)