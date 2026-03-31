#!/usr/bin/env python3
# Harness: tool protocol -- capabilities grow without changing the loop.
"""
s02_tool_use.py - Tool Protocol

This chapter keeps the same loop from s01 and only changes the tool pool.
That is still the right teaching move.

The update versus the old course is emphasis:
real coding-agent tools behave like protocol objects with schemas, names,
permission hooks, and result mapping. This file keeps only the minimum slice of
that idea.
"""

from __future__ import annotations

from pathlib import Path

from agents._shared import ToolRegistry, base_tools, get_model, make_client, repl, run_loop

WORKDIR = Path.cwd()
MODEL = get_model()
CLIENT = make_client()
SYSTEM = (
    f"You are a coding agent at {WORKDIR}. "
    "Prefer read_file, write_file, and edit_file for filesystem work. "
    "Use bash when you need shell-native behavior."
)

REGISTRY = ToolRegistry(base_tools(WORKDIR))


def run_session(messages: list[dict[str, object]]):
    return run_loop(
        client=CLIENT,
        model=MODEL,
        system_prompt=SYSTEM,
        registry=REGISTRY,
        messages=messages,
    )


if __name__ == "__main__":
    repl(prompt="\033[36ms02 >> \033[0m", runner=run_session)
