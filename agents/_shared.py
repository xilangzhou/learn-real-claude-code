from __future__ import annotations

import os
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv(override=True)

if os.getenv("ANTHROPIC_BASE_URL"):
    os.environ.pop("ANTHROPIC_AUTH_TOKEN", None)


def make_client() -> Anthropic:
    return Anthropic(base_url=os.getenv("ANTHROPIC_BASE_URL"))


def get_model() -> str:
    return os.environ["MODEL_ID"]


def safe_path(workdir: Path, path: str) -> Path:
    resolved = (workdir / path).resolve()
    if not resolved.is_relative_to(workdir):
        raise ValueError(f"Path escapes workspace: {path}")
    return resolved


def run_bash(workdir: Path, command: str, timeout: int = 120) -> str:
    dangerous = ["rm -rf /", "sudo", "shutdown", "reboot", "> /dev/"]
    if any(fragment in command for fragment in dangerous):
        return "Error: Dangerous command blocked"
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=workdir,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return f"Error: Timeout ({timeout}s)"
    output = (result.stdout + result.stderr).strip()
    return output[:50_000] if output else "(no output)"


def run_read(workdir: Path, path: str, limit: int | None = None) -> str:
    try:
        lines = safe_path(workdir, path).read_text(encoding="utf-8").splitlines()
        if limit and limit < len(lines):
            lines = lines[:limit] + [f"... ({len(lines) - limit} more lines)"]
        return "\n".join(lines)[:50_000]
    except Exception as exc:  # pragma: no cover - teaching path
        return f"Error: {exc}"


def run_write(workdir: Path, path: str, content: str) -> str:
    try:
        file_path = safe_path(workdir, path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        return f"Wrote {len(content)} bytes to {path}"
    except Exception as exc:  # pragma: no cover - teaching path
        return f"Error: {exc}"


def run_edit(workdir: Path, path: str, old_text: str, new_text: str) -> str:
    try:
        file_path = safe_path(workdir, path)
        current = file_path.read_text(encoding="utf-8")
        if old_text not in current:
            return f"Error: Text not found in {path}"
        file_path.write_text(current.replace(old_text, new_text, 1), encoding="utf-8")
        return f"Edited {path}"
    except Exception as exc:  # pragma: no cover - teaching path
        return f"Error: {exc}"


@dataclass
class Tool:
    name: str
    description: str
    input_schema: dict[str, Any]
    handler: Callable[..., str]

    def definition(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
        }


class ToolRegistry:
    def __init__(self, tools: list[Tool]):
        self.tools = {tool.name: tool for tool in tools}

    def definitions(self) -> list[dict[str, Any]]:
        return [tool.definition() for tool in self.tools.values()]

    def call(self, tool_name: str, **kwargs: Any) -> str:
        tool = self.tools.get(tool_name)
        if not tool:
            return f"Unknown tool: {tool_name}"
        return str(tool.handler(**kwargs))


def extract_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    parts: list[str] = []
    for block in content or []:
        text = getattr(block, "text", None)
        if text:
            parts.append(text)
    return "\n".join(parts).strip()


def make_tool_result(tool_use_id: str, content: str) -> dict[str, str]:
    return {
        "type": "tool_result",
        "tool_use_id": tool_use_id,
        "content": content,
    }


def base_tools(workdir: Path, *, include_write: bool = True) -> list[Tool]:
    tools = [
        Tool(
            name="bash",
            description="Run a shell command.",
            input_schema={
                "type": "object",
                "properties": {"command": {"type": "string"}},
                "required": ["command"],
            },
            handler=lambda **kw: run_bash(workdir, kw["command"]),
        ),
        Tool(
            name="read_file",
            description="Read file contents.",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "limit": {"type": "integer"},
                },
                "required": ["path"],
            },
            handler=lambda **kw: run_read(workdir, kw["path"], kw.get("limit")),
        ),
    ]
    if include_write:
        tools.extend(
            [
                Tool(
                    name="write_file",
                    description="Write content to a file.",
                    input_schema={
                        "type": "object",
                        "properties": {
                            "path": {"type": "string"},
                            "content": {"type": "string"},
                        },
                        "required": ["path", "content"],
                    },
                    handler=lambda **kw: run_write(workdir, kw["path"], kw["content"]),
                ),
                Tool(
                    name="edit_file",
                    description="Replace an exact string in a file.",
                    input_schema={
                        "type": "object",
                        "properties": {
                            "path": {"type": "string"},
                            "old_text": {"type": "string"},
                            "new_text": {"type": "string"},
                        },
                        "required": ["path", "old_text", "new_text"],
                    },
                    handler=lambda **kw: run_edit(
                        workdir,
                        kw["path"],
                        kw["old_text"],
                        kw["new_text"],
                    ),
                ),
            ]
        )
    return tools


def run_loop(
    *,
    client: Anthropic,
    model: str,
    system_prompt: str,
    registry: ToolRegistry,
    messages: list[dict[str, Any]],
    max_turns: int = 40,
    max_tokens: int = 8_000,
    before_request: Callable[[list[dict[str, Any]]], None] | None = None,
) -> Any:
    turns = 0
    while True:
        turns += 1
        if turns > max_turns:
            raise RuntimeError("Max turns exceeded")
        if before_request:
            before_request(messages)
        response = client.messages.create(
            model=model,
            system=system_prompt,
            messages=messages,
            tools=registry.definitions(),
            max_tokens=max_tokens,
        )
        messages.append({"role": "assistant", "content": response.content})
        tool_uses = [
            block for block in response.content if getattr(block, "type", None) == "tool_use"
        ]
        if not tool_uses:
            return response
        results: list[dict[str, str]] = []
        for block in tool_uses:
            try:
                output = registry.call(block.name, **block.input)
            except Exception as exc:  # pragma: no cover - teaching path
                output = f"Error: {exc}"
            results.append(make_tool_result(block.id, str(output)))
        messages.append({"role": "user", "content": results})


def repl(
    *,
    prompt: str,
    runner: Callable[[list[dict[str, Any]]], Any],
) -> None:
    history: list[dict[str, Any]] = []
    while True:
        try:
            query = input(prompt)
        except (EOFError, KeyboardInterrupt):
            break
        if query.strip().lower() in {"q", "quit", "exit", ""}:
            break
        history.append({"role": "user", "content": query})
        response = runner(history)
        text = extract_text(response.content)
        if text:
            print(text)
        print()


def summarize_messages(messages: list[dict[str, Any]], keep_last: int = 6) -> str:
    lines: list[str] = []
    for message in messages[-keep_last:]:
        role = message["role"]
        content = message["content"]
        if isinstance(content, str):
            snippet = content
        else:
            snippet = extract_text(content) or str(content)
        snippet = " ".join(snippet.split())
        lines.append(f"{role}: {snippet[:180]}")
    return "\n".join(lines) if lines else "(empty conversation)"


def monotonic_id(prefix: str) -> str:
    return f"{prefix}-{int(time.time() * 1000)}"
