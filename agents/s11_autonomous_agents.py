#!/usr/bin/env python3
# Harness: self-organizing workers -- agents can poll, claim, and resume.
"""
s11_autonomous_agents.py - Self-Organizing Workers

This chapter updates the old autonomy lesson without pretending that
"autonomy" means magic. The harness supplies:

- an inbox
- a task board
- an idle loop

The model supplies the judgment about what to do next.
"""

from __future__ import annotations

import json
import threading
import time
from pathlib import Path

from agents._shared import Tool, ToolRegistry, base_tools, get_model, make_client, repl, run_loop

POLL_INTERVAL = 5
IDLE_TIMEOUT = 60


class TaskBoard:
    def __init__(self, root: Path) -> None:
        self.root = root / ".lrcc" / "autonomy" / "tasks"
        self.root.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def create(self, subject: str) -> str:
        next_id = str(max([0] + [int(path.stem) for path in self.root.glob("*.json") if path.stem.isdigit()]) + 1)
        task = {
            "id": next_id,
            "subject": subject,
            "status": "pending",
            "owner": "",
            "blocked_by": [],
        }
        (self.root / f"{next_id}.json").write_text(json.dumps(task, indent=2), encoding="utf-8")
        return json.dumps(task, indent=2)

    def unclaimed(self) -> list[dict[str, object]]:
        tasks = []
        for path in sorted(self.root.glob("*.json")):
            task = json.loads(path.read_text(encoding="utf-8"))
            if task["status"] == "pending" and not task["owner"] and not task["blocked_by"]:
                tasks.append(task)
        return tasks

    def claim(self, task_id: str, owner: str) -> str:
        with self._lock:
            path = self.root / f"{task_id}.json"
            if not path.exists():
                return f"Error: task {task_id} not found"
            task = json.loads(path.read_text(encoding="utf-8"))
            if task["owner"]:
                return f"Error: task {task_id} already claimed by {task['owner']}"
            task["owner"] = owner
            task["status"] = "in_progress"
            path.write_text(json.dumps(task, indent=2), encoding="utf-8")
        return json.dumps(task, indent=2)

    def list_all(self) -> str:
        tasks = [json.loads(path.read_text(encoding="utf-8")) for path in sorted(self.root.glob("*.json"))]
        return json.dumps(tasks, indent=2) if tasks else "[]"


class Inbox:
    def __init__(self, root: Path) -> None:
        self.root = root / ".lrcc" / "autonomy" / "inbox"
        self.root.mkdir(parents=True, exist_ok=True)

    def send(self, sender: str, recipient: str, content: str) -> str:
        path = self.root / f"{recipient}.jsonl"
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps({"from": sender, "content": content, "ts": time.time()}) + "\n")
        return f"Sent message to {recipient}"

    def read(self, recipient: str) -> list[dict[str, object]]:
        path = self.root / f"{recipient}.jsonl"
        if not path.exists():
            return []
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        path.write_text("", encoding="utf-8")
        return rows


WORKDIR = Path.cwd()
MODEL = get_model()
CLIENT = make_client()
TASKS = TaskBoard(WORKDIR)
INBOX = Inbox(WORKDIR)
SYSTEM = f"""You are an autonomous coding agent at {WORKDIR}.
When you have no immediate foreground work, you may idle, poll the inbox,
claim an unowned task, and continue."""

REGISTRY = ToolRegistry(
    base_tools(WORKDIR)
    + [
        Tool(
            name="task_create",
            description="Create a task on the shared task board.",
            input_schema={
                "type": "object",
                "properties": {"subject": {"type": "string"}},
                "required": ["subject"],
            },
            handler=lambda **kw: TASKS.create(kw["subject"]),
        ),
        Tool(
            name="task_list",
            description="List the shared task board.",
            input_schema={"type": "object", "properties": {}},
            handler=lambda **kw: TASKS.list_all(),
        ),
        Tool(
            name="claim_task",
            description="Claim a pending task from the board.",
            input_schema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string"},
                    "owner": {"type": "string"},
                },
                "required": ["task_id", "owner"],
            },
            handler=lambda **kw: TASKS.claim(kw["task_id"], kw["owner"]),
        ),
        Tool(
            name="send_message",
            description="Send an inbox message to another agent.",
            input_schema={
                "type": "object",
                "properties": {
                    "to": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["to", "content"],
            },
            handler=lambda **kw: INBOX.send("lead", kw["to"], kw["content"]),
        ),
        Tool(
            name="idle",
            description="Yield control so the harness can poll for new work.",
            input_schema={"type": "object", "properties": {}},
            handler=lambda **kw: "Idle requested. The harness will poll for inbox messages and unclaimed tasks.",
        ),
    ]
)


def before_request(messages: list[dict[str, object]]) -> None:
    inbox = INBOX.read("lead")
    if inbox:
        messages.append({"role": "user", "content": "<inbox>\n" + json.dumps(inbox, indent=2) + "\n</inbox>"})
        return
    pending = TASKS.unclaimed()
    if pending:
        first = pending[0]
        messages.append(
            {
                "role": "user",
                "content": (
                    "<auto-claim-opportunity>\n"
                    f"Unclaimed task #{first['id']}: {first['subject']}\n"
                    "</auto-claim-opportunity>"
                ),
            }
        )


def run_session(messages: list[dict[str, object]]):
    started = time.time()
    response = run_loop(
        client=CLIENT,
        model=MODEL,
        system_prompt=SYSTEM,
        registry=REGISTRY,
        messages=messages,
        before_request=before_request,
    )
    if time.time() - started >= IDLE_TIMEOUT:
        messages.append(
            {
                "role": "user",
                "content": f"<idle-timeout>No new work arrived within {IDLE_TIMEOUT}s.</idle-timeout>",
            }
        )
    else:
        time.sleep(0 if POLL_INTERVAL <= 0 else 0)
    return response


if __name__ == "__main__":
    repl(prompt="\033[36ms11 >> \033[0m", runner=run_session)
