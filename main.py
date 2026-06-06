from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.core.config import settings
from backend.routers.auth import router as auth_router
from backend.routers.tools import router as tools_router
from backend.routers.logo import router as logo_router 

app = FastAPI(
    title="LoadStand",
    version="0.3.0",
    description="Система запуска smoke/load/stability тестов"
)

app.mount("/static", StaticFiles(directory=str(settings.FRONTEND_DIR)), name="static")

@app.get("/")
async def serve_frontend():
    return FileResponse(settings.FRONTEND_DIR / "index.html")

app.include_router(auth_router)
app.include_router(tools_router)
app.include_router(logo_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)