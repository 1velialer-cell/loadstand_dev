import asyncio
import os
import time
from datetime import datetime
from typing import Dict, List
from fastapi import WebSocket
from sqlalchemy.orm import Session
from backend.core.config import settings
from backend.db.models.run import RunResult
from backend.db.session import SessionLocal
from backend.models.schemas import RunStatus
from backend.repositories.result_repository import RunResultRepository
from backend.repositories.run_repository import RunRepository

MAX_BUFFERED_EVENTS = 300

class RunSession:
    def __init__(self):
        self.clients: List[WebSocket] = []
        self.buffer: List[dict] = []
        self.lock = asyncio.Lock()

    async def add_client(self, websocket: WebSocket):
        async with self.lock:
            self.clients.append(websocket)
            for event in self.buffer:
                await websocket.send_json(event)

    async def remove_client(self, websocket: WebSocket):
        async with self.lock:
            if websocket in self.clients:
                self.clients.remove(websocket)

    async def broadcast(self, event: dict):
        async with self.lock:
            self.buffer.append(event)
            if len(self.buffer) > MAX_BUFFERED_EVENTS:
                self.buffer.pop(0)
            dead = []
            for ws in self.clients:
                try:
                    await ws.send_json(event)
                except Exception:
                    dead.append(ws)
            for ws in dead:
                if ws in self.clients:
                    self.clients.remove(ws)

class RunExecutor:
    def __init__(self):
        self.sessions: Dict[str, RunSession] = {}
        self.tasks: Dict[str, asyncio.Task] = {}

    async def get_session(self, run_id: str) -> RunSession:
        return self.sessions.setdefault(run_id, RunSession())

    async def connect(self, run_id: str, websocket: WebSocket):
        session = await self.get_session(run_id)
        await session.add_client(websocket)

    async def disconnect(self, run_id: str, websocket: WebSocket):
        session = self.sessions.get(run_id)
        if session:
            await session.remove_client(websocket)

    async def _broadcast(self, run_id: str, event: dict):
        session = await self.get_session(run_id)
        await session.broadcast(event)

    async def _status(self, run_id: str, status: str, message: str):
        await self._broadcast(
            run_id,
            {
                "type": "status",
                "status": status,
                "message": message,
            },
        )

    async def _progress(self, run_id: str, value: int):
        await self._broadcast(
            run_id,
            {
                "type": "progress",
                "value": value,
            },
        )

    async def _resolve_tool_path(self, tool_name: str) -> str:
        if tool_name not in settings.ALLOWED_TOOLS:
            raise ValueError("tool_not_allowed")
        candidate = os.path.normpath(os.path.join(settings.TOOLS_DIR, tool_name))
        if not candidate.startswith(str(settings.TOOLS_DIR) + os.sep):
            raise ValueError("invalid_path")
        if not os.path.isfile(candidate):
            raise ValueError("tool_not_found")
        return candidate

    def start_run(self, run_id: str, tool_name: str):
        if run_id in self.tasks:
            return
        self.sessions.setdefault(run_id, RunSession())
        self.tasks[run_id] = asyncio.create_task(self._run_process(run_id, tool_name))

    async def _run_process(self,run_id: str,tool_name: str,):
        db: Session = SessionLocal()
        run_repo = RunRepository(db)
        result_repo = RunResultRepository(db)
        run = run_repo.get(run_id)
        if not run:
            db.close()
            return
        start_time = time.time()
        stdout_chunks: List[str] = []
        stderr_chunks: List[str] = []
        try:
            run.status = RunStatus.RUNNING.value
            run.started_at = datetime.utcnow()
            run_repo.save()
            await self._status(run_id,RunStatus.RUNNING.value,"Run started",)
            await self._progress(run_id, 0)
            script_path = await self._resolve_tool_path(tool_name)
            process = await asyncio.create_subprocess_exec(
                "python3",
                script_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=os.path.dirname(script_path),
            )
            await self._progress(run_id, 10)
            async def stream_reader(stream,stream_type,chunks,):
                while True:
                    line = await stream.readline()
                    if not line:
                        break
                    text = line.decode("utf-8",errors="ignore",)
                    chunks.append(text)
                    await self._broadcast(
                        run_id,
                        {
                            "type": stream_type,
                            "text": text,
                        },
                    )
            stdout_task = asyncio.create_task(
                stream_reader(process.stdout,"stdout",stdout_chunks,))
            stderr_task = asyncio.create_task(
                stream_reader(process.stderr,"stderr",stderr_chunks,))
            while process.returncode is None:
                await asyncio.sleep(1)
                await self._progress(run_id,50,)
                if process.returncode is not None:
                    break
            await process.wait()
            await asyncio.gather(stdout_task,stderr_task,)
            return_code = process.returncode
            duration_sec = round(time.time() - start_time,3,)
            stdout_text = "".join(stdout_chunks)
            stderr_text = "".join(stderr_chunks)
            run.finished_at = datetime.utcnow()
            run.status = (
                RunStatus.FINISHED.value
                if return_code == 0
                else RunStatus.FAILED.value
            )
            run_repo.save()
            result_repo.create(
                RunResult(
                    run_id=run.id,
                    return_code=return_code,
                    stdout=stdout_text,
                    stderr=stderr_text,
                    duration_sec=duration_sec,
                )
            )
            await self._progress(run_id, 100)
            await self._broadcast(
                run_id,
                {
                    "type": "result",
                    "status": run.status,
                    "return_code": return_code,
                    "duration_sec": duration_sec,
                },
            )

            await self._status(
                run_id,
                run.status,
                "Run completed",
            )

        except Exception as exc:
            run.status = RunStatus.FAILED.value
            run.finished_at = datetime.utcnow()
            run_repo.save()
            result_repo.create(
                RunResult(
                    run_id=run.id,
                    return_code=-1,
                    stdout="",
                    stderr=str(exc),
                    duration_sec=round(
                        time.time() - start_time,
                        3,
                    ),
                )
            )
            await self._broadcast(
                run_id,
                {
                    "type": "error",
                    "message": str(exc),
                },
            )
            await self._status(
                run_id,
                RunStatus.FAILED.value,
                "Run failed",
            )
        finally:
            db.close()

run_executor = RunExecutor()