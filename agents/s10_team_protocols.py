#!/usr/bin/env python3
# Harness: structured coordination -- request IDs turn messages into protocols.
"""
s10_team_protocols.py - Team Protocols

This chapter keeps the mailbox model from s09 and adds a missing layer:
not every message should be plain chat.

The teaching version introduces two request/response protocols:

- shutdown approval
- plan approval
"""

from __future__ import annotations

import json
import time
import uuid
from pathlib import Path

from agents._shared import Tool, ToolRegistry, base_tools, get_model, make_client, repl, run_loop


class ProtocolState:
    def __init__(self, state_dir: Path) -> None:
        self.state_dir = state_dir
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.shutdown_requests: dict[str, dict[str, object]] = {}
        self.plan_requests: dict[str, dict[str, object]] = {}

    def request_shutdown(self, teammate: str, reason: str = "") -> str:
        request_id = str(uuid.uuid4())[:8]
        self.shutdown_requests[request_id] = {
            "target": teammate,
            "status": "pending",
            "reason": reason,
            "created_at": time.time(),
        }
        return json.dumps(self.shutdown_requests[request_id] | {"request_id": request_id}, indent=2)

    def submit_plan(self, teammate: str, plan: str) -> str:
        request_id = str(uuid.uuid4())[:8]
        self.plan_requests[request_id] = {
            "from": teammate,
            "plan": plan,
            "status": "pending",
            "created_at": time.time(),
        }
        return json.dumps(self.plan_requests[request_id] | {"request_id": request_id}, indent=2)

    def resolve(self, protocol: str, request_id: str, approve: bool, feedback: str = "") -> str:
        table = self.shutdown_requests if protocol == "shutdown" else self.plan_requests
        entry = table.get(request_id)
        if entry is None:
            return f"Error: unknown {protocol} request {request_id}"
        entry["status"] = "approved" if approve else "rejected"
        entry["feedback"] = feedback
        entry["resolved_at"] = time.time()
        return json.dumps(entry | {"request_id": request_id}, indent=2)

    def list_all(self) -> str:
        payload = {
            "shutdown_requests": self.shutdown_requests,
            "plan_requests": self.plan_requests,
        }
        return json.dumps(payload, indent=2) if any(payload.values()) else "No protocol state."


WORKDIR = Path.cwd()
MODEL = get_model()
CLIENT = make_client()
STATE = ProtocolState(WORKDIR / ".lrcc" / "protocols")
SYSTEM = f"""You are a coordinating agent at {WORKDIR}.
Use request IDs for non-trivial coordination.
Prefer structured approval protocols over ambiguous free-form messages."""

REGISTRY = ToolRegistry(
    base_tools(WORKDIR)
    + [
        Tool(
            name="request_shutdown",
            description="Open a structured shutdown request.",
            input_schema={
                "type": "object",
                "properties": {
                    "teammate": {"type": "string"},
                    "reason": {"type": "string"},
                },
                "required": ["teammate"],
            },
            handler=lambda **kw: STATE.request_shutdown(kw["teammate"], kw.get("reason", "")),
        ),
        Tool(
            name="respond_shutdown",
            description="Approve or reject a shutdown request.",
            input_schema={
                "type": "object",
                "properties": {
                    "request_id": {"type": "string"},
                    "approve": {"type": "boolean"},
                    "feedback": {"type": "string"},
                },
                "required": ["request_id", "approve"],
            },
            handler=lambda **kw: STATE.resolve(
                "shutdown",
                kw["request_id"],
                kw["approve"],
                kw.get("feedback", ""),
            ),
        ),
        Tool(
            name="submit_plan",
            description="Open a structured plan approval request.",
            input_schema={
                "type": "object",
                "properties": {
                    "teammate": {"type": "string"},
                    "plan": {"type": "string"},
                },
                "required": ["teammate", "plan"],
            },
            handler=lambda **kw: STATE.submit_plan(kw["teammate"], kw["plan"]),
        ),
        Tool(
            name="review_plan",
            description="Approve or reject a plan request.",
            input_schema={
                "type": "object",
                "properties": {
                    "request_id": {"type": "string"},
                    "approve": {"type": "boolean"},
                    "feedback": {"type": "string"},
                },
                "required": ["request_id", "approve"],
            },
            handler=lambda **kw: STATE.resolve(
                "plan",
                kw["request_id"],
                kw["approve"],
                kw.get("feedback", ""),
            ),
        ),
        Tool(
            name="protocol_state",
            description="Inspect current protocol trackers.",
            input_schema={"type": "object", "properties": {}},
            handler=lambda **kw: STATE.list_all(),
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
    repl(prompt="\033[36ms10 >> \033[0m", runner=run_session)
