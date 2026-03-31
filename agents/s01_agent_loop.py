#!/usr/bin/env python3
# Harness: the agent loop -- the smallest useful coding agent.
"""
s01_agent_loop.py - The Agent Loop

The first chapter stays intentionally tiny:

    user -> model -> tool_use? -> execute -> tool_result -> loop

The important correction is conceptual, not structural:
the loop is still the heart of the harness, but the real product wraps it in
many surrounding systems. We start with the irreducible core.
"""

from __future__ import annotations

from pathlib import Path

from agents._shared import ToolRegistry, base_tools, get_model, make_client, repl, run_loop

WORKDIR = Path.cwd()
MODEL = get_model()
CLIENT = make_client()
SYSTEM = (
    f"You are a coding agent at {WORKDIR}. "
    "Use bash to inspect the workspace and act before you explain."
)


REGISTRY = ToolRegistry([base_tools(WORKDIR, include_write=False)[0]])


def run_session(messages: list[dict[str, object]]):
    return run_loop(
        client=CLIENT,
        model=MODEL,
        system_prompt=SYSTEM,
        registry=REGISTRY,
        messages=messages,
    )


if __name__ == "__main__":
    repl(prompt="\033[36ms01 >> \033[0m", runner=run_session)
