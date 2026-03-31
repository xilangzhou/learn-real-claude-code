#!/usr/bin/env python3
# Harness: delegation modes -- fresh workers and forked workers are different.
"""
s04_subagent.py - Delegation Modes

The old course treated subagents as always "fresh context".
That is no longer enough.

This chapter now teaches two delegation modes:

- fresh: clean message history, summary return
- fork: inherit recent context, then execute in a narrower scope
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from agents._shared import (
    Tool,
    ToolRegistry,
    base_tools,
    extract_text,
    get_model,
    make_client,
    repl,
    run_loop,
    summarize_messages,
)

WORKDIR = Path.cwd()
MODEL = get_model()
CLIENT = make_client()
SYSTEM = f"""You are a coding agent at {WORKDIR}.
Use delegate for focused subtasks.
Choose mode=\"fresh\" when you want a clean worker.
Choose mode=\"fork\" when the worker should inherit recent context."""
SUBAGENT_SYSTEM = (
    f"You are a delegated coding worker at {WORKDIR}. "
    "Stay inside scope. Use tools directly, then return one concise report."
)


def run_worker(
    *,
    prompt: str,
    mode: str,
    parent_messages: list[dict[str, Any]],
) -> str:
    if mode not in {"fresh", "fork"}:
        return f"Error: unknown delegation mode {mode!r}"
    worker_messages: list[dict[str, Any]]
    if mode == "fresh":
        worker_messages = [{"role": "user", "content": prompt}]
    else:
        inherited = summarize_messages(parent_messages, keep_last=8)
        worker_messages = [
            {
                "role": "user",
                "content": (
                    "<inherited-context>\n"
                    f"{inherited}\n"
                    "</inherited-context>\n\n"
                    f"<directive>{prompt}</directive>"
                ),
            }
        ]
    worker_response = run_loop(
        client=CLIENT,
        model=MODEL,
        system_prompt=SUBAGENT_SYSTEM,
        registry=ToolRegistry(base_tools(WORKDIR)),
        messages=worker_messages,
        max_turns=20,
    )
    return extract_text(worker_response.content) or "(worker returned no summary)"


class DelegationRunner:
    def __init__(self) -> None:
        self.parent_messages: list[dict[str, Any]] = []

    def delegate(self, prompt: str, mode: str = "fresh") -> str:
        return run_worker(prompt=prompt, mode=mode, parent_messages=self.parent_messages)


RUNNER = DelegationRunner()
REGISTRY = ToolRegistry(
    base_tools(WORKDIR)
    + [
        Tool(
            name="delegate",
            description="Run a focused worker in fresh or fork mode.",
            input_schema={
                "type": "object",
                "properties": {
                    "prompt": {"type": "string"},
                    "mode": {
                        "type": "string",
                        "enum": ["fresh", "fork"],
                    },
                },
                "required": ["prompt"],
            },
            handler=lambda **kw: RUNNER.delegate(
                kw["prompt"],
                kw.get("mode", "fresh"),
            ),
        )
    ]
)


def run_session(messages: list[dict[str, object]]):
    RUNNER.parent_messages = messages
    return run_loop(
        client=CLIENT,
        model=MODEL,
        system_prompt=SYSTEM,
        registry=REGISTRY,
        messages=messages,
    )


if __name__ == "__main__":
    repl(prompt="\033[36ms04 >> \033[0m", runner=run_session)
