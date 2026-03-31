#!/usr/bin/env python3
# Harness: skills -- late-bound knowledge with discovery and activation.
"""
s05_skill_loading.py - Skill Discovery

The old lesson only taught "load a skill by name".
This rewrite keeps that idea but adds the two missing realities:

- skills come from multiple directories
- some skills activate only when matching file paths appear
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from agents._shared import Tool, ToolRegistry, base_tools, get_model, make_client, repl, run_loop

try:
    import yaml
except ImportError:  # pragma: no cover - teaching path
    yaml = None


@dataclass
class Skill:
    name: str
    description: str
    body: str
    source: str
    paths: list[str]


class SkillLoader:
    def __init__(self, workdir: Path) -> None:
        self.workdir = workdir
        self.all_skills: dict[str, Skill] = {}
        self.active_skills: dict[str, Skill] = {}
        self._load_static_sources()

    def _parse_skill(self, file_path: Path) -> Skill:
        raw = file_path.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n(.*)", raw, re.DOTALL)
        frontmatter: dict[str, Any] = {}
        body = raw.strip()
        if match:
            if yaml is not None:
                parsed = yaml.safe_load(match.group(1))
                frontmatter = parsed if isinstance(parsed, dict) else {}
            body = match.group(2).strip()
        name = str(frontmatter.get("name", file_path.parent.name))
        description = str(frontmatter.get("description", "No description provided."))
        paths_raw = frontmatter.get("paths", [])
        if isinstance(paths_raw, str):
            paths = [item.strip() for item in paths_raw.split(",") if item.strip()]
        elif isinstance(paths_raw, list):
            paths = [str(item).strip() for item in paths_raw if str(item).strip()]
        else:
            paths = []
        return Skill(
            name=name,
            description=description,
            body=body,
            source=str(file_path),
            paths=paths,
        )

    def _load_static_sources(self) -> None:
        candidate_dirs = [
            self.workdir / "skills",
            self.workdir / ".claude" / "skills",
        ]
        for directory in candidate_dirs:
            if not directory.exists():
                continue
            for file_path in sorted(directory.rglob("SKILL.md")):
                skill = self._parse_skill(file_path)
                self.all_skills[skill.name] = skill
                if not skill.paths:
                    self.active_skills[skill.name] = skill

    def activate_for_paths(self, paths: list[str]) -> str:
        activated: list[str] = []
        normalized = [path.replace("\\", "/") for path in paths]
        for skill in self.all_skills.values():
            if not skill.paths or skill.name in self.active_skills:
                continue
            for pattern in skill.paths:
                pattern = pattern.replace("\\", "/").strip()
                if not pattern:
                    continue
                if any(pattern in path for path in normalized):
                    self.active_skills[skill.name] = skill
                    activated.append(skill.name)
                    break
        if not activated:
            return "No conditional skills activated."
        return "Activated skills: " + ", ".join(sorted(activated))

    def list_active(self) -> str:
        if not self.active_skills:
            return "(no active skills)"
        return "\n".join(
            f"- {skill.name}: {skill.description}"
            for skill in sorted(self.active_skills.values(), key=lambda item: item.name)
        )

    def load(self, name: str) -> str:
        skill = self.active_skills.get(name)
        if not skill:
            available = ", ".join(sorted(self.active_skills)) or "(none)"
            return f"Error: unknown or inactive skill '{name}'. Active skills: {available}"
        return (
            f"<skill name=\"{skill.name}\" source=\"{skill.source}\">\n"
            f"{skill.body}\n"
            "</skill>"
        )


WORKDIR = Path.cwd()
MODEL = get_model()
CLIENT = make_client()
SKILLS = SkillLoader(WORKDIR)
SYSTEM = f"""You are a coding agent at {WORKDIR}.
Skills are loaded late.
You can inspect active skills in the system prompt, activate conditional skills
from file paths, then load the full body when needed.

Active skills:
{SKILLS.list_active()}"""

REGISTRY = ToolRegistry(
    base_tools(WORKDIR)
    + [
        Tool(
            name="activate_skills",
            description="Activate conditional skills that match touched paths.",
            input_schema={
                "type": "object",
                "properties": {
                    "paths": {
                        "type": "array",
                        "items": {"type": "string"},
                    }
                },
                "required": ["paths"],
            },
            handler=lambda **kw: SKILLS.activate_for_paths(kw["paths"]),
        ),
        Tool(
            name="load_skill",
            description="Load the full body of an active skill.",
            input_schema={
                "type": "object",
                "properties": {"name": {"type": "string"}},
                "required": ["name"],
            },
            handler=lambda **kw: SKILLS.load(kw["name"]),
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
    repl(prompt="\033[36ms05 >> \033[0m", runner=run_session)
