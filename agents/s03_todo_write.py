#!/usr/bin/env python3
# Harness: session state -- a visible checklist for the current line of work.
"""
s03_todo_write.py - Session State

This chapter keeps TodoWrite, but with a clearer boundary:

- todos are short-lived session guidance
- they are not the durable task graph

That distinction matters later when we add persistent tasks.
"""

from __future__ import annotations

from pathlib import Path

from agents._shared import Tool, ToolRegistry, base_tools, get_model, make_client, repl, run_loop


class TodoManager:
    def __init__(self) -> None:
        self.items: list[dict[str, str]] = []

    def update(self, todos: list[dict[str, str]]) -> str:
        if len(todos) > 20:
            raise ValueError("Max 20 todo items")
        in_progress = 0
        normalized: list[dict[str, str]] = []
        for index, item in enumerate(todos, start=1):
            content = str(item.get("content", "")).strip()
            status = str(item.get("status", "pending")).lower()
            active_form = str(item.get("active_form", "")).strip()
            if not content:
                raise ValueError(f"Todo {index}: content is required")
            if status not in {"pending", "in_progress", "completed"}:
                raise ValueError(f"Todo {index}: invalid status {status!r}")
            if status == "in_progress":
                in_progress += 1
                if not active_form:
                    raise ValueError(f"Todo {index}: active_form required for in_progress")
            normalized.append(
                {
                    "content": content,
                    "status": status,
                    "active_form": active_form,
                }
            )
        if in_progress > 1:
            raise ValueError("Only one todo can be in_progress")
        self.items = [] if normalized and all(t["status"] == "completed" for t in normalized) else normalized
        return self.render()

    def render(self) -> str:
        if not self.items:
            return "No open session todos."
        lines: list[str] = []
        for item in self.items:
            marker = {
                "pending": "[ ]",
                "in_progress": "[>]",
                "completed": "[x]",
            }[item["status"]]
            suffix = f" <- {item['active_form']}" if item["status"] == "in_progress" else ""
            lines.append(f"{marker} {item['content']}{suffix}")
        done = sum(1 for item in self.items if item["status"] == "completed")
        lines.append(f"\n({done}/{len(self.items)} completed)")
        return "\n".join(lines)


WORKDIR = Path.cwd()
MODEL = get_model()
CLIENT = make_client()
SYSTEM = f"""You are a coding agent at {WORKDIR}.
Use todo_write for multi-step work.
Treat the todo list as the session checklist, not the long-lived project task graph.
Keep exactly one item in_progress."""

TODOS = TodoManager()
REGISTRY = ToolRegistry(
    base_tools(WORKDIR)
    + [
        Tool(
            name="todo_write",
            description="Update the session todo list.",
            input_schema={
                "type": "object",
                "properties": {
                    "todos": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "content": {"type": "string"},
                                "status": {
                                    "type": "string",
                                    "enum": ["pending", "in_progress", "completed"],
                                },
                                "active_form": {"type": "string"},
                            },
                            "required": ["content", "status"],
                        },
                    }
                },
                "required": ["todos"],
            },
            handler=lambda **kw: TODOS.update(kw["todos"]),
        )
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
    repl(prompt="\033[36ms03 >> \033[0m", runner=run_session)
