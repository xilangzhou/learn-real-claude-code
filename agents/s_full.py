#!/usr/bin/env python3
# Harness: reference integration -- a compact but coherent teaching cockpit.
"""
s_full.py - Reference Teaching Harness

This file is no longer a claim to be a miniature copy of the production code.
Instead it is a compact reference that integrates the corrected lessons:

- loop + tool protocol
- session todos
- fresh/fork delegation
- skills
- context management
- persistent tasks
- background runtime
- team mailboxes
- structured protocols
- worktree isolation
"""

from __future__ import annotations

import json
import subprocess
import threading
import time
import uuid
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

from agents._shared import Tool, ToolRegistry, base_tools, extract_text, get_model, make_client, run_loop

load_dotenv(override=True)

WORKDIR = Path.cwd()
MODEL = get_model()
CLIENT: Anthropic = make_client()


class BackgroundManager:
    def __init__(self, workdir: Path | None = None) -> None:
        self.workdir = workdir or Path.cwd()
        self.tasks: dict[str, dict[str, str | None]] = {}
        self.notifications: list[dict[str, str]] = []
        self._lock = threading.Lock()

    def run(self, command: str) -> str:
        task_id = str(uuid.uuid4())[:8]
        self.tasks[task_id] = {
            "status": "running",
            "command": command,
            "result": None,
        }
        threading.Thread(target=self._execute, args=(task_id, command), daemon=True).start()
        return task_id

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
            self.notifications.append(
                {
                    "task_id": task_id,
                    "status": status,
                    "result": output[:500],
                }
            )

    def drain(self) -> list[dict[str, str]]:
        with self._lock:
            items = list(self.notifications)
            self.notifications.clear()
        return items

    def check(self, task_id: str | None = None) -> str:
        if task_id is not None:
            task = self.tasks.get(task_id)
            if task is None:
                return f"Error: unknown task {task_id}"
            result = task.get("result")
            if result is None:
                return "[running] (running)"
            return f"[{task['status']}] {result}"
        if not self.tasks:
            return "No background tasks."
        return "\n".join(
            f"{task_id}: [{task['status']}] {task['command']}"
            for task_id, task in sorted(self.tasks.items())
        )


BG = BackgroundManager(WORKDIR)
SYSTEM = f"""You are a coding agent at {WORKDIR}.
Use the reference harness features when they help:
todos for short-lived guidance, tasks for durable work, background_run for
slow commands, and compact for explicit context resets."""

_pending_compact = {"requested": False}


def compact_handler() -> str:
    _pending_compact["requested"] = True
    return "Compact requested."


REGISTRY = ToolRegistry(
    base_tools(WORKDIR)
    + [
        Tool(
            name="background_run",
            description="Launch a background shell task.",
            input_schema={
                "type": "object",
                "properties": {"command": {"type": "string"}},
                "required": ["command"],
            },
            handler=lambda **kw: f"Background task {BG.run(kw['command'])} launched",
        ),
        Tool(
            name="background_check",
            description="Inspect background task state.",
            input_schema={
                "type": "object",
                "properties": {"task_id": {"type": "string"}},
            },
            handler=lambda **kw: BG.check(kw.get("task_id")),
        ),
        Tool(
            name="compact",
            description="Request a compact boundary after the current turn.",
            input_schema={"type": "object", "properties": {}},
            handler=lambda **kw: compact_handler(),
        ),
    ]
)


def before_request(messages: list[dict[str, object]]) -> None:
    notifications = BG.drain()
    if notifications:
        payload = "\n".join(
            f"[bg:{item['task_id']}] {item['status']}: {item['result']}"
            for item in notifications
        )
        messages.append({"role": "user", "content": f"<task-notifications>\n{payload}\n</task-notifications>"})


def run_session(messages: list[dict[str, object]]):
    response = run_loop(
        client=CLIENT,
        model=MODEL,
        system_prompt=SYSTEM,
        registry=REGISTRY,
        messages=messages,
        before_request=before_request,
    )
    if _pending_compact["requested"]:
        _pending_compact["requested"] = False
        messages[:] = [
            {
                "role": "user",
                "content": "<compact-boundary>\nReference harness reset. Carry forward only the latest user goal.\n</compact-boundary>",
            }
        ]
    return response


if __name__ == "__main__":
    history: list[dict[str, object]] = []
    while True:
        try:
            query = input("\033[36ms_full >> \033[0m")
        except (EOFError, KeyboardInterrupt):
            break
        if query.strip().lower() in {"q", "quit", "exit", ""}:
            break
        history.append({"role": "user", "content": query})
        response = run_session(history)
        text = extract_text(response.content)
        if text:
            print(text)
        print()
