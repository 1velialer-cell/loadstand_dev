import asyncio
import uuid
from dataclasses import dataclass, field
from typing import Dict, Optional

import asyncssh
import json
from pathlib import Path
from backend.db.models.node import Node

@dataclass
class CommandHandle:
    node_id: str
    command_id: str
    command: str
    process: asyncssh.SSHClientProcess
    stdout: str = ""
    stderr: str = ""
    return_code: Optional[int] = None
    completed: bool = False
    started_at: float = field(default_factory=asyncio.get_event_loop().time)
    finished_at: Optional[float] = None

class SSHExecutor:
    def __init__(self):
        self.connections: Dict[str, asyncssh.SSHClientConnection] = {}
        self.commands: Dict[str, CommandHandle] = {}
        self.lock = asyncio.Lock()

    async def _connect(self, node: Node) -> asyncssh.SSHClientConnection:
        login = getattr(node, "ssh_login", None)
        password = getattr(node, "ssh_password", None)

        if not login or not password:
            raise ValueError("SSH credentials missing for node")

        return await asyncssh.connect(
            node.host,
            port=node.port,
            username=login,
            password=password,
            known_hosts=None,
            client_keys=None,
            keepalive_interval=30,
            keepalive_count_max=3,
        )

    async def _is_connection_active(self, conn: asyncssh.SSHClientConnection) -> bool:
        is_closing = getattr(conn, "is_closing", None)
        if callable(is_closing):
            return not is_closing()
        return True

    async def get_connection(self, node: Node) -> asyncssh.SSHClientConnection:
        async with self.lock:
            conn = self.connections.get(node.id)
            if conn is None or not await self._is_connection_active(conn):
                conn = await self._connect(node)
                self.connections[node.id] = conn
            return conn

    async def execute_command(self, node: Node, command: str, timeout: int = 300) -> dict:
        conn = await self.get_connection(node)
        process = await conn.create_process(command)
        command_id = str(uuid.uuid4())
        handle = CommandHandle(
            node_id=node.id,
            command_id=command_id,
            command=command,
            process=process,
        )
        self.commands[command_id] = handle
        asyncio.create_task(self._monitor_process(handle, timeout))
        return {"command_id": command_id, "status": "running"}

    async def _monitor_process(self, handle: CommandHandle, timeout: int):
        try:
            stdout_task = asyncio.create_task(handle.process.stdout.read())
            stderr_task = asyncio.create_task(handle.process.stderr.read())
            done, pending = await asyncio.wait(
                {stdout_task, stderr_task, asyncio.create_task(handle.process.wait())},
                return_when=asyncio.ALL_COMPLETED,
                timeout=timeout,
            )

            if stdout_task in done:
                handle.stdout = stdout_task.result() or ""
            if stderr_task in done:
                handle.stderr = stderr_task.result() or ""

            if handle.process.exit_status is not None:
                handle.return_code = handle.process.exit_status
            else:
                await self._close_process(handle)
                handle.return_code = handle.process.exit_status

        except asyncio.TimeoutError:
            await self._close_process(handle)
            handle.stderr += "\nCommand timed out."
            handle.return_code = -1
        except Exception as exc:
            handle.stderr += f"\nSSH executor error: {exc}"
            handle.return_code = -1
        finally:
            handle.completed = True
            handle.finished_at = asyncio.get_event_loop().time()

    async def _close_process(self, handle: CommandHandle):
        try:
            if handle.process and not handle.process.stdout.at_eof():
                handle.process.terminate()
                await handle.process.wait()
        except Exception:
            try:
                handle.process.kill()
            except Exception:
                pass

    async def stop_command(self, command_id: str) -> dict:
        handle = self.commands.get(command_id)
        if not handle:
            raise KeyError("command_not_found")
        if handle.completed:
            return {
                "command_id": command_id,
                "status": "completed",
                "stdout": handle.stdout,
                "stderr": handle.stderr,
                "return_code": handle.return_code,
            }

        await self._close_process(handle)
        handle.completed = True
        handle.return_code = handle.process.exit_status
        handle.finished_at = asyncio.get_event_loop().time()
        return {
            "command_id": command_id,
            "status": "stopped",
            "stdout": handle.stdout,
            "stderr": handle.stderr,
            "return_code": handle.return_code,
        }

    def get_command(self, command_id: str) -> dict:
        handle = self.commands.get(command_id)
        if not handle:
            raise KeyError("command_not_found")
        return {
            "command_id": handle.command_id,
            "node_id": handle.node_id,
            "command": handle.command,
            "status": "completed" if handle.completed else "running",
            "stdout": handle.stdout,
            "stderr": handle.stderr,
            "return_code": handle.return_code,
            "started_at": handle.started_at,
            "finished_at": handle.finished_at,
        }

executor = SSHExecutor()
