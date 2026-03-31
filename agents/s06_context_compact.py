#!/usr/bin/env python3
# Harness: context management -- not one compact, but a stack of interventions.
"""
s06_context_compact.py - Context Management Stack

The correction here is the biggest one in the course.
We no longer teach a single three-stage compact pipeline as if that were the
whole story. Instead we model a stack:

- tool-result budgeting for oversized history
- micro summaries for stale detail
- manual compaction for explicit resets
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from agents._shared import (
    Tool,
    ToolRegistry,
    base_tools,
    get_model,
    make_client,
    repl,
    run_loop,
    summarize_messages,
)


class ContextManager:
    def __init__(self, workdir: Path) -> None:
        self.workdir = workdir
        self.transcript_dir = workdir / ".transcripts"
        self.transcript_dir.mkdir(exist_ok=True)

    def estimate_tokens(self, messages: list[dict[str, Any]]) -> int:
        return len(json.dumps(messages, default=str, ensure_ascii=False)) // 4

    def apply_result_budget(self, messages: list[dict[str, Any]]) -> None:
        tool_results: list[dict[str, Any]] = []
        for message in messages:
            if message["role"] == "user" and isinstance(message.get("content"), list):
                for part in message["content"]:
                    if isinstance(part, dict) and part.get("type") == "tool_result":
                        tool_results.append(part)
        for part in tool_results[:-4]:
            content = part.get("content")
            if isinstance(content, str) and len(content) > 500:
                part["content"] = content[:240] + "\n...[truncated by result budget]"

    def apply_micro_summary(self, messages: list[dict[str, Any]]) -> None:
        assistant_turns = [msg for msg in messages if msg["role"] == "assistant"]
        if len(assistant_turns) < 8:
            return
        for message in messages[:-6]:
            if message["role"] != "user":
                continue
            content = message.get("content")
            if isinstance(content, str) and len(content) > 300:
                message["content"] = content[:180] + "\n...[micro-summary placeholder]"

    def compact_now(self, messages: list[dict[str, Any]], reason: str) -> str:
        transcript_path = self.transcript_dir / f"compact_{int(time.time())}.jsonl"
        with transcript_path.open("w", encoding="utf-8") as handle:
            for message in messages:
                handle.write(json.dumps(message, default=str, ensure_ascii=False) + "\n")
        summary = summarize_messages(messages, keep_last=10)
        messages[:] = [
            {
                "role": "user",
                "content": (
                    "<compact-boundary>\n"
                    f"Reason: {reason}\n"
                    f"Transcript: {transcript_path}\n"
                    "Recent continuity summary:\n"
                    f"{summary}\n"
                    "</compact-boundary>"
                ),
            }
        ]
        return f"Conversation compacted. Transcript saved to {transcript_path}"


WORKDIR = Path.cwd()
MODEL = get_model()
CLIENT = make_client()
CTX = ContextManager(WORKDIR)
SYSTEM = f"""You are a coding agent at {WORKDIR}.
Manage context strategically.
Assume the harness can trim old tool results, replace stale detail with
micro-summaries, and compact the session when asked."""

_pending_manual_compact = {"reason": None}


def compact_handler(reason: str = "manual compact requested") -> str:
    _pending_manual_compact["reason"] = reason
    return "Compact requested. Finish the current tool turn, then reset the active context."


REGISTRY = ToolRegistry(
    base_tools(WORKDIR)
    + [
        Tool(
            name="compact",
            description="Create a compact boundary and keep only a continuity summary in context.",
            input_schema={
                "type": "object",
                "properties": {"reason": {"type": "string"}},
            },
            handler=lambda **kw: compact_handler(kw.get("reason", "manual compact requested")),
        )
    ]
)


def before_request(messages: list[dict[str, Any]]) -> None:
    CTX.apply_result_budget(messages)
    CTX.apply_micro_summary(messages)
    if CTX.estimate_tokens(messages) > 50_000:
        CTX.compact_now(messages, "token threshold crossed")


def run_session(messages: list[dict[str, object]]):
    response = run_loop(
        client=CLIENT,
        model=MODEL,
        system_prompt=SYSTEM,
        registry=REGISTRY,
        messages=messages,
        before_request=before_request,
    )
    if _pending_manual_compact["reason"]:
        reason = str(_pending_manual_compact["reason"])
        _pending_manual_compact["reason"] = None
        CTX.compact_now(messages, reason)
    return response


if __name__ == "__main__":
    repl(prompt="\033[36ms06 >> \033[0m", runner=run_session)
