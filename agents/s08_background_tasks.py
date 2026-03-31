#!/usr/bin/env python3
# Harness: background runtime -- slow work should not stall the foreground loop.
"""
s08_background_tasks.py - Background Runtime

The old lesson only modeled background shell commands.
This rewrite keeps that core idea, but frames it as a runtime concern:

- foreground reasoning stays responsive
- background tasks produce notifications
- the harness owns task lifecycle, not the model
"""

from __future__ import annotations

import subprocess
import threading
import uuid
from pathlib import Path

from agents._shared import Tool, ToolRegistry, base_tools, get_model, make_client, repl, run_loop


class BackgroundManager:
    def __init__(self, workdir: Path) -> None:
        self.workdir = workdir
        self.tasks: dict[str, dict[str, str | None]] = {}
        self._notifications: list[dict[str, str]] = []
        self._lock = threading.Lock()

    def run(self, command: str) -> str:
        task_id = str(uuid.uuid4())[:8]
        self.tasks[task_id] = {
            "status": "running",
            "command": command,
            "result": None,
        }
        thread = threading.Thread(target=self._execute, args=(task_id, command), daemon=True)
        thread.start()
        return f"Background task {task_id} launched: {command[:80]}"

    def _execute(self, task_id: str, command: str) -> None:
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.workdir,
                capture_output=True,
                text=True,
                timeout=300,
            )
            output = (result.stdout + result.stderr).strip() or "(no output)"
            status = "completed"
        except subprocess.TimeoutExpired:
            output = "Error: Timeout (300s)"
            status = "timeout"
        self.tasks[task_id]["status"] = status
        self.tasks[task_id]["result"] = output[:50_000]
        with self._lock:
            self._notifications.append(
                {
                    "task_id": task_id,
                    "status": status,
                    "result": output[:500],
                }
            )

    def check(self, task_id: str | None = None) -> str:
        if task_id:
            task = self.tasks.get(task_id)
            if not task:
                return f"Error: unknown task {task_id}"
            result = task.get("result")
            if result is None:
                return f"[{task['status']}] (running)"
            return f"[{task['status']}] {result}"
        if not self.tasks:
            return "No background tasks."
        return "\n".join(
            f"{task_id}: [{task['status']}] {task['command']}"
            for task_id, task in sorted(self.tasks.items())
        )

    def drain_notifications(self) -> list[dict[str, str]]:
        with self._lock:
            notifications = list(self._notifications)
            self._notifications.clear()
        return notifications


WORKDIR = Path.cwd()
MODEL = get_model()
CLIENT = make_client()
BG = BackgroundManager(WORKDIR)
SYSTEM = f"""You are a coding agent at {WORKDIR}.
Use background_run for slow commands.
Treat notifications as runtime events injected by the harness."""

REGISTRY = ToolRegistry(
    base_tools(WORKDIR)
    + [
        Tool(
            name="background_run",
            description="Launch a long-running shell command in the background.",
            input_schema={
                "type": "object",
                "properties": {"command": {"type": "string"}},
                "required": ["command"],
            },
            handler=lambda **kw: BG.run(kw["command"]),
        ),
        Tool(
            name="background_check",
            description="Inspect one background task or list them all.",
            input_schema={
                "type": "object",
                "properties": {"task_id": {"type": "string"}},
            },
            handler=lambda **kw: BG.check(kw.get("task_id")),
        ),
    ]
)


def before_request(messages: list[dict[str, object]]) -> None:
    notifications = BG.drain_notifications()
    if not notifications:
        return
    payload = "\n".join(
        f"[bg:{item['task_id']}] {item['status']}: {item['result']}"
        for item in notifications
    )
    messages.append(
        {
            "role": "user",
            "content": f"<task-notifications>\n{payload}\n</task-notifications>",
        }
    )


def run_session(messages: list[dict[str, object]]):
    return run_loop(
        client=CLIENT,
        model=MODEL,
        system_prompt=SYSTEM,
        registry=REGISTRY,
        messages=messages,
        before_request=before_request,
    )


if __name__ == "__main__":
    repl(prompt="\033[36ms08 >> \033[0m", runner=run_session)
