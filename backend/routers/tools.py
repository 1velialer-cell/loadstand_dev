from fastapi import APIRouter, Depends, HTTPException
from backend.services.tool_executor import run_tool
from backend.core.sec import get_current_user
from backend.models.schemas import ToolRunRequest, ToolResult

router = APIRouter(
    prefix="/tools",
    tags=["tools"]
)
