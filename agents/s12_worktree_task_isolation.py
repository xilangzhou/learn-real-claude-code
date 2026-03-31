#!/usr/bin/env python3
# Harness: execution isolation -- worktrees separate where tasks run.
"""
s12_worktree_task_isolation.py - Worktree Isolation

The last chapter keeps the core lesson:
tasks are control-plane state; isolation decides where execution happens.

This version teaches three linked records:

- task record
- worktree record
- lifecycle event log
"""

from __future__ import annotations

import json
import shutil
import subprocess
import time
from pathlib import Path

from agents._shared import Tool, ToolRegistry, base_tools, get_model, make_client, repl, run_loop


def detect_repo_root(cwd: Path) -> Path | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except Exception:
        return None
    if result.returncode != 0:
        return None
    root = Path(result.stdout.strip())
    return root if root.exists() else None


class TaskBoard:
    def __init__(self, root: Path) -> None:
        self.root = root / ".lrcc" / "isolation" / "tasks"
        self.root.mkdir(parents=True, exist_ok=True)

    def create(self, subject: str) -> dict[str, object]:
        next_id = str(max([0] + [int(path.stem) for path in self.root.glob("*.json") if path.stem.isdigit()]) + 1)
        task = {
            "id": next_id,
            "subject": subject,
            "status": "pending",
            "worktree": "",
        }
        (self.root / f"{next_id}.json").write_text(json.dumps(task, indent=2), encoding="utf-8")
        return task

    def bind(self, task_id: str, worktree_name: str) -> dict[str, object]:
        path = self.root / f"{task_id}.json"
        if not path.exists():
            raise ValueError(f"Task {task_id} not found")
        task = json.loads(path.read_text(encoding="utf-8"))
        task["worktree"] = worktree_name
        if task["status"] == "pending":
            task["status"] = "in_progress"
        path.write_text(json.dumps(task, indent=2), encoding="utf-8")
        return task

    def complete(self, task_id: str) -> dict[str, object]:
        path = self.root / f"{task_id}.json"
        task = json.loads(path.read_text(encoding="utf-8"))
        task["status"] = "completed"
        path.write_text(json.dumps(task, indent=2), encoding="utf-8")
        return task

    def list_all(self) -> str:
        tasks = [json.loads(path.read_text(encoding="utf-8")) for path in sorted(self.root.glob("*.json"))]
        return json.dumps(tasks, indent=2) if tasks else "[]"


class EventLog:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("", encoding="utf-8")

    def emit(self, event: str, **payload: object) -> None:
        record = {"event": event, "ts": time.time(), **payload}
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record) + "\n")

    def recent(self, limit: int = 20) -> str:
        lines = self.path.read_text(encoding="utf-8").splitlines()[-limit:]
        return json.dumps([json.loads(line) for line in lines], indent=2) if lines else "[]"


class WorktreeStore:
    def __init__(self, repo_root: Path, tasks: TaskBoard, events: EventLog) -> None:
        self.repo_root = repo_root
        self.base = repo_root / ".lrcc" / "isolation" / "worktrees"
        self.base.mkdir(parents=True, exist_ok=True)
        self.index_path = self.base / "index.json"
        self.tasks = tasks
        self.events = events

    def _load_index(self) -> dict[str, object]:
        if self.index_path.exists():
            return json.loads(self.index_path.read_text(encoding="utf-8"))
        return {"worktrees": []}

    def _save_index(self, data: dict[str, object]) -> None:
        self.index_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def create(self, name: str, task_id: str | None = None) -> str:
        worktree_path = self.base / name
        self.events.emit("worktree.create.before", name=name, task_id=task_id)
        if not worktree_path.exists():
            if detect_repo_root(self.repo_root):
                subprocess.run(
                    ["git", "worktree", "add", str(worktree_path), "-b", f"wt/{name}"],
                    cwd=self.repo_root,
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
            else:
                worktree_path.mkdir(parents=True, exist_ok=True)
        index = self._load_index()
        record = {
            "name": name,
            "path": str(worktree_path),
            "branch": f"wt/{name}",
            "task_id": task_id,
            "status": "active",
        }
        index["worktrees"] = [item for item in index["worktrees"] if item["name"] != name] + [record]
        self._save_index(index)
        if task_id:
            self.tasks.bind(task_id, name)
        self.events.emit("worktree.create.after", worktree=record)
        return json.dumps(record, indent=2)

    def remove(self, name: str, complete_task: bool = False) -> str:
        index = self._load_index()
        record = next((item for item in index["worktrees"] if item["name"] == name), None)
        if record is None:
            return f"Error: worktree {name} not found"
        self.events.emit("worktree.remove.before", worktree=record)
        worktree_path = Path(record["path"])
        if worktree_path.exists() and worktree_path.is_dir():
            shutil.rmtree(worktree_path)
        record["status"] = "removed"
        self._save_index(index)
        if complete_task and record.get("task_id"):
            task = self.tasks.complete(str(record["task_id"]))
            self.events.emit("task.completed", task=task)
        self.events.emit("worktree.remove.after", worktree=record)
        return json.dumps(record, indent=2)

    def list_all(self) -> str:
        return json.dumps(self._load_index(), indent=2)


WORKDIR = Path.cwd()
REPO_ROOT = detect_repo_root(WORKDIR) or WORKDIR
MODEL = get_model()
CLIENT = make_client()
TASKS = TaskBoard(REPO_ROOT)
EVENTS = EventLog(REPO_ROOT / ".lrcc" / "isolation" / "events.jsonl")
WORKTREES = WorktreeStore(REPO_ROOT, TASKS, EVENTS)
SYSTEM = f"""You are a coding agent at {WORKDIR}.
Use task_create for the control plane and worktree_create for execution isolation.
Keep task identity and worktree identity linked."""

REGISTRY = ToolRegistry(
    base_tools(WORKDIR)
    + [
        Tool(
            name="task_create",
            description="Create a task before allocating an isolation lane.",
            input_schema={
                "type": "object",
                "properties": {"subject": {"type": "string"}},
                "required": ["subject"],
            },
            handler=lambda **kw: json.dumps(TASKS.create(kw["subject"]), indent=2),
        ),
        Tool(
            name="task_list",
            description="List task records.",
            input_schema={"type": "object", "properties": {}},
            handler=lambda **kw: TASKS.list_all(),
        ),
        Tool(
            name="worktree_create",
            description="Create an isolated execution lane and optionally bind it to a task.",
            input_schema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "task_id": {"type": "string"},
                },
                "required": ["name"],
            },
            handler=lambda **kw: WORKTREES.create(kw["name"], kw.get("task_id")),
        ),
        Tool(
            name="worktree_remove",
            description="Remove an isolated execution lane.",
            input_schema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "complete_task": {"type": "boolean"},
                },
                "required": ["name"],
            },
            handler=lambda **kw: WORKTREES.remove(kw["name"], kw.get("complete_task", False)),
        ),
        Tool(
            name="worktree_list",
            description="List isolation lanes.",
            input_schema={"type": "object", "properties": {}},
            handler=lambda **kw: WORKTREES.list_all(),
        ),
        Tool(
            name="worktree_events",
            description="Inspect lifecycle events for isolation lanes.",
            input_schema={
                "type": "object",
                "properties": {"limit": {"type": "integer"}},
            },
            handler=lambda **kw: EVENTS.recent(int(kw.get("limit", 20))),
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
    repl(prompt="\033[36ms12 >> \033[0m", runner=run_session)
