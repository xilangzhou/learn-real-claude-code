#!/usr/bin/env python3
# Harness: shared collaboration state -- teammates, inboxes, and team identity.
"""
s09_agent_teams.py - Team Mailboxes

This chapter keeps the durable lesson from the old course:
multi-agent collaboration needs explicit shared state.

The modernized version emphasizes three shared artifacts:

- a team roster
- mailbox files
- a shared task-list identity
"""

from __future__ import annotations

import json
import threading
import time
from pathlib import Path

from agents._shared import Tool, ToolRegistry, base_tools, get_model, make_client, repl, run_loop


class MailboxBus:
    def __init__(self, inbox_dir: Path) -> None:
        self.inbox_dir = inbox_dir
        self.inbox_dir.mkdir(parents=True, exist_ok=True)

    def send(self, sender: str, recipient: str, message: str, summary: str = "") -> str:
        payload = {
            "from": sender,
            "message": message,
            "summary": summary,
            "timestamp": time.time(),
        }
        path = self.inbox_dir / f"{recipient}.jsonl"
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload) + "\n")
        return f"Sent message to {recipient}"

    def read(self, recipient: str) -> list[dict[str, object]]:
        path = self.inbox_dir / f"{recipient}.jsonl"
        if not path.exists():
            return []
        rows = [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        path.write_text("", encoding="utf-8")
        return rows


class TeamManager:
    def __init__(self, root: Path, bus: MailboxBus) -> None:
        self.root = root / ".lrcc" / "team"
        self.root.mkdir(parents=True, exist_ok=True)
        self.config_path = self.root / "config.json"
        self.bus = bus
        self.config = self._load()
        self.threads: dict[str, threading.Thread] = {}

    def _load(self) -> dict[str, object]:
        if self.config_path.exists():
            return json.loads(self.config_path.read_text(encoding="utf-8"))
        return {"team_name": "default", "members": []}

    def _save(self) -> None:
        self.config_path.write_text(json.dumps(self.config, indent=2), encoding="utf-8")

    def spawn(self, name: str, role: str, prompt: str) -> str:
        members = self.config["members"]
        member = next((item for item in members if item["name"] == name), None)
        if member is None:
            member = {"name": name, "role": role, "status": "working"}
            members.append(member)
        else:
            member["role"] = role
            member["status"] = "working"
        self._save()

        def teammate_loop() -> None:
            messages = [{"role": "user", "content": prompt}]
            system = (
                f"You are teammate '{name}' with role '{role}'. "
                "Use send_message to coordinate. Stay focused and concise."
            )
            registry = ToolRegistry(
                base_tools(Path.cwd())
                + [
                    Tool(
                        name="send_message",
                        description="Send a message to another teammate.",
                        input_schema={
                            "type": "object",
                            "properties": {
                                "to": {"type": "string"},
                                "message": {"type": "string"},
                                "summary": {"type": "string"},
                            },
                            "required": ["to", "message"],
                        },
                        handler=lambda **kw: self.bus.send(
                            name,
                            kw["to"],
                            kw["message"],
                            kw.get("summary", ""),
                        ),
                    )
                ]
            )

            def before_request(history: list[dict[str, object]]) -> None:
                inbox = self.bus.read(name)
                if inbox:
                    history.append(
                        {
                            "role": "user",
                            "content": "<inbox>\n" + json.dumps(inbox, indent=2) + "\n</inbox>",
                        }
                    )

            try:
                run_loop(
                    client=make_client(),
                    model=get_model(),
                    system_prompt=system,
                    registry=registry,
                    messages=messages,
                    before_request=before_request,
                    max_turns=20,
                )
            finally:
                member["status"] = "idle"
                self._save()

        thread = threading.Thread(target=teammate_loop, daemon=True)
        self.threads[name] = thread
        thread.start()
        return f"Spawned teammate '{name}' ({role})"

    def list_members(self) -> str:
        members = self.config["members"]
        if not members:
            return "No teammates."
        lines = [f"Team: {self.config['team_name']}"]
        for member in members:
            lines.append(f"- {member['name']} ({member['role']}): {member['status']}")
        return "\n".join(lines)


WORKDIR = Path.cwd()
MODEL = get_model()
CLIENT = make_client()
BUS = MailboxBus(WORKDIR / ".lrcc" / "team" / "inbox")
TEAM = TeamManager(WORKDIR, BUS)
SYSTEM = f"""You are a team lead at {WORKDIR}.
Use team_spawn to create persistent teammates and send_message to coordinate.
Treat mailboxes as shared collaboration state, not ad-hoc chat."""

REGISTRY = ToolRegistry(
    base_tools(WORKDIR)
    + [
        Tool(
            name="team_spawn",
            description="Create or resume a persistent teammate.",
            input_schema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "role": {"type": "string"},
                    "prompt": {"type": "string"},
                },
                "required": ["name", "role", "prompt"],
            },
            handler=lambda **kw: TEAM.spawn(kw["name"], kw["role"], kw["prompt"]),
        ),
        Tool(
            name="send_message",
            description="Send a mailbox message to a teammate.",
            input_schema={
                "type": "object",
                "properties": {
                    "to": {"type": "string"},
                    "message": {"type": "string"},
                    "summary": {"type": "string"},
                },
                "required": ["to", "message"],
            },
            handler=lambda **kw: BUS.send("lead", kw["to"], kw["message"], kw.get("summary", "")),
        ),
        Tool(
            name="read_inbox",
            description="Read and drain the lead inbox.",
            input_schema={"type": "object", "properties": {}},
            handler=lambda **kw: json.dumps(BUS.read("lead"), indent=2) or "[]",
        ),
        Tool(
            name="team_list",
            description="List team members and statuses.",
            input_schema={"type": "object", "properties": {}},
            handler=lambda **kw: TEAM.list_members(),
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
    repl(prompt="\033[36ms09 >> \033[0m", runner=run_session)
