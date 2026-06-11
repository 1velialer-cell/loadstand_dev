import os
import asyncio
import time
from typing import Dict
from fastapi import HTTPException
from backend.core.config import settings

def _resolve_tool_path(name: str) -> str:
    if name not in settings.ALLOWED_TOOLS:
        raise ValueError("tool_not_allowed")
    candidate = os.path.normpath(os.path.join(settings.TOOLS_DIR, name))
    if not candidate.startswith(str(settings.TOOLS_DIR) + os.sep):
        raise ValueError("invalid_path")
    if not os.path.isfile(candidate):
        raise ValueError("tool_not_found")
    return candidate

async def run_tool(name: str):
    started = time.time()
    script_path = _resolve_tool_path(name)
    proc = await asyncio.create_subprocess_exec("python3",script_path,stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.PIPE,cwd=os.path.dirname(script_path))
    stdout, stderr = await proc.communicate()
    return {
        "return_code": proc.returncode,
        "stdout": stdout.decode("utf-8", errors="ignore"),
        "stderr": stderr.decode("utf-8", errors="ignore"),
        "duration_sec": round(time.time() - started, 3)
    }

    proc = await asyncio.create_subprocess_exec(
        "python3", script_path,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=os.path.dirname(script_path)
    )

    try:
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=settings.TOOL_TIMEOUT)
    except asyncio.TimeoutError:
        proc.kill()
        await proc.communicate()
        return {
            "status": "timeout",
            "stdout": "",
            "stderr": "Выполнение превысило лимит времени",
            "returncode": -1
        }

    return {
        "status": "success" if proc.returncode == 0 else "error",
        "returncode": proc.returncode,
        "stdout": stdout.decode("utf-8", errors="ignore"),
        "stderr": stderr.decode("utf-8", errors="ignore"),
    }