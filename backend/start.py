from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import os
import asyncio
from typing import Dict
from backend.config import settings

router = APIRouter()

def _resolve_tool_path(name: str) -> str:
    if name not in settings.ALLOWED_TOOLS:
        raise ValueError("not_allowed")
    
    candidate = os.path.normpath(os.path.join(settings.TOOLS_DIR, name))
    if not candidate.startswith(os.path.abspath(settings.TOOLS_DIR) + os.sep):
        raise ValueError("invalid_path")
    if not os.path.isfile(candidate):
        raise ValueError("not_found")
    return candidate

async def _run_script(path: str, timeout: int = settings.TOOL_TIMEOUT) -> Dict:
    proc = await asyncio.create_subprocess_exec(
        "python3", path,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=os.path.dirname(path)
    )
    try:
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
    except asyncio.TimeoutError:
        proc.kill()
        await proc.communicate()
        return {"status": "timeout", "stdout": "", "stderr": "Выполнение превысило лимит времени"}

    return {
        "status": "success" if proc.returncode == 0 else "error",
        "returncode": proc.returncode,
        "stdout": stdout.decode("utf-8", errors="ignore"),
        "stderr": stderr.decode("utf-8", errors="ignore"),
    }

@router.post("/run-tool")
async def run_tool(payload: Dict):
    name = payload.get("name") if isinstance(payload, dict) else None
    if not name:
        raise HTTPException(status_code=400, detail="missing_name")

    try:
        script_path = _resolve_tool_path(name)
    except ValueError as e:
        err = str(e)
        if err == "not_allowed":
            raise HTTPException(status_code=403, detail="tool_not_allowed")
        elif err == "not_found":
            raise HTTPException(status_code=404, detail="tool_not_found")
        else:
            raise HTTPException(status_code=400, detail="invalid_path")

    result = await _run_script(script_path)
    return result