from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.core.config import settings
from backend.routers.auth import router as auth_router
from backend.routers.tools import router as tools_router
from backend.routers.logo import router as logo_router 
from backend.routers.servers import router as servers_router

app = FastAPI(title="LoadStand",version="0.3.0",description="Система запуска smoke/load/stability тестов")
app.mount("/static",StaticFiles(directory=str(settings.FRONTEND_DIR)),name="static")
app.include_router(auth_router, prefix="/api")
app.include_router(servers_router, prefix="/api")
app.include_router(tools_router, prefix="/api")
app.include_router(logo_router, prefix="/api")

@app.get("/")
async def root():
    return FileResponse(settings.FRONTEND_DIR / "index.html")

@app.get("/{path:path}")
async def spa(path: str):
    return FileResponse(settings.FRONTEND_DIR / "index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)