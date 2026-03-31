#!/usr/bin/env python3
# Harness: persistent tasks -- durable state outside the conversation transcript.
"""
s07_task_system.py - Persistent Task Runtime

This chapter upgrades the old "task graph in the repo" lesson.
The new teaching version keeps file-backed tasks, but makes the control-plane
idea explicit:

- tasks live outside conversation history
- task-list identity is separate from the session transcript
- dependencies and ownership survive compaction
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from agents._shared import Tool, ToolRegistry, base_tools, get_model, make_client, repl, run_loop


class TaskStore:
    def __init__(self, root: Path, task_list_id: str = "default") -> None:
        self.root = root / ".lrcc" / "tasks" / task_list_id
        self.root.mkdir(parents=True, exist_ok=True)
        self.high_water_mark = self.root / ".high-water-mark"

    def _next_id(self) -> str:
        existing = [int(path.stem) for path in self.root.glob("*.json") if path.stem.isdigit()]
        current_mark = int(self.high_water_mark.read_text() or "0") if self.high_water_mark.exists() else 0
        next_id = max(existing + [current_mark], default=0) + 1
        self.high_water_mark.write_text(str(next_id), encoding="utf-8")
        return str(next_id)

    def _path(self, task_id: str) -> Path:
        return self.root / f"{task_id}.json"

    def create(self, subject: str, description: str = "") -> str:
        task = {
            "id": self._next_id(),
            "subject": subject,
            "description": description,
            "status": "pending",
            "owner": "",
            "blocked_by": [],
            "blocks": [],
            "created_at": time.time(),
            "updated_at": time.time(),
        }
        self._path(task["id"]).write_text(json.dumps(task, indent=2), encoding="utf-8")
        return json.dumps(task, indent=2)

    def get(self, task_id: str) -> str:
        path = self._path(task_id)
        if not path.exists():
            return f"Error: task {task_id} not found"
        return path.read_text(encoding="utf-8")

    def list_all(self) -> str:
        tasks = [
            json.loads(path.read_text(encoding="utf-8"))
            for path in sorted(self.root.glob("*.json"))
            if path.stem.isdigit()
        ]
        if not tasks:
            return "No tasks."
        lines: list[str] = []
        for task in tasks:
            marker = {
                "pending": "[ ]",
                "in_progress": "[>]",
                "completed": "[x]",
            }.get(task["status"], "[?]")
            owner = f" owner={task['owner']}" if task.get("owner") else ""
            blocked = (
                f" blocked_by={task['blocked_by']}"
                if task.get("blocked_by")
                else ""
            )
            lines.append(f"{marker} #{task['id']}: {task['subject']}{owner}{blocked}")
        return "\n".join(lines)

    def update(
        self,
        task_id: str,
        *,
        status: str | None = None,
        owner: str | None = None,
        add_blocked_by: list[str] | None = None,
    ) -> str:
        path = self._path(task_id)
        if not path.exists():
            return f"Error: task {task_id} not found"
        task = json.loads(path.read_text(encoding="utf-8"))
        if status is not None:
            if status not in {"pending", "in_progress", "completed"}:
                return f"Error: invalid status {status!r}"
            task["status"] = status
        if owner is not None:
            task["owner"] = owner
        if add_blocked_by:
            merged = list(dict.fromkeys(task.get("blocked_by", []) + add_blocked_by))
            task["blocked_by"] = merged
        task["updated_at"] = time.time()
        path.write_text(json.dumps(task, indent=2), encoding="utf-8")
        if status == "completed":
            self._clear_dependency(task_id)
        return json.dumps(task, indent=2)

    def _clear_dependency(self, completed_id: str) -> None:
        for path in self.root.glob("*.json"):
            if not path.stem.isdigit():
                continue
            task = json.loads(path.read_text(encoding="utf-8"))
            if completed_id in task.get("blocked_by", []):
                task["blocked_by"] = [item for item in task["blocked_by"] if item != completed_id]
                task["updated_at"] = time.time()
                path.write_text(json.dumps(task, indent=2), encoding="utf-8")


WORKDIR = Path.cwd()
MODEL = get_model()
CLIENT = make_client()
TASKS = TaskStore(WORKDIR)
SYSTEM = f"""You are a coding agent at {WORKDIR}.
Use the persistent task tools for long-lived work tracking.
Remember that tasks outlive the current transcript."""

REGISTRY = ToolRegistry(
    base_tools(WORKDIR)
    + [
        Tool(
            name="task_create",
            description="Create a durable task in the task list.",
            input_schema={
                "type": "object",
                "properties": {
                    "subject": {"type": "string"},
                    "description": {"type": "string"},
                },
                "required": ["subject"],
            },
            handler=lambda **kw: TASKS.create(kw["subject"], kw.get("description", "")),
        ),
        Tool(
            name="task_get",
            description="Read a task by ID.",
            input_schema={
                "type": "object",
                "properties": {"task_id": {"type": "string"}},
                "required": ["task_id"],
            },
            handler=lambda **kw: TASKS.get(kw["task_id"]),
        ),
        Tool(
            name="task_list",
            description="List all tasks in the current task list.",
            input_schema={"type": "object", "properties": {}},
            handler=lambda **kw: TASKS.list_all(),
        ),
        Tool(
            name="task_update",
            description="Update task status, owner, or dependencies.",
            input_schema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string"},
                    "status": {
                        "type": "string",
                        "enum": ["pending", "in_progress", "completed"],
                    },
                    "owner": {"type": "string"},
                    "add_blocked_by": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
                "required": ["task_id"],
            },
            handler=lambda **kw: TASKS.update(
                kw["task_id"],
                status=kw.get("status"),
                owner=kw.get("owner"),
                add_blocked_by=kw.get("add_blocked_by"),
            ),
        ),
    ]
)


def run_session(messages: list[dict[str, object]]):
    return run_loop(
        client=CLIENT,
        model=MODEL,
        system_prompt=SYSTEM,
        registry=REGISTRY,
        messages=messages,
    )


if __name__ == "__main__":
    repl(prompt="\033[36ms07 >> \033[0m", runner=run_session)
