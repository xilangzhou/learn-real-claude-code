# s05: Skill Discovery

`s01 > s02 > s03 > s04 > [ s05 ] s06 | s07 > s08 > s09 > s10 > s11 > s12`

> *Listing every skill body in the prompt is wasteful — discover, activate, then load.*
>
> **Harness layer**: on-demand knowledge — keep heavy text out of the static system prompt.

## Problem

Long domain docs in system prompt cost tokens and attention. The model mainly needs **what exists** and **when to read which file**.

## Approach

`SkillLoader` walks `skills/` and `.claude/skills/` for `SKILL.md`, parses YAML frontmatter (`name`, `description`, `paths`).

- Skills **without** `paths`: start **active**.
- Skills **with** `paths`: **activate** only after you call the tool with touched paths (substring match).

Tools: `activate_skills(paths)`, `load_skill(name)`. Only **active** skills can be loaded with full body.

## Behavior

System prompt lists `list_active()` only; bodies arrive via `tool_result` wrapped as `<skill name="..." source="...">`.

## Changes vs s04

| Piece | s04 | s05 |
|-------|-----|-----|
| Knowledge | none structured | metadata + body + conditional activation |
| Tools | base + delegate | + `activate_skills`, `load_skill` |

## Try it

```sh
cd learn-real-claude-code
python agents/s05_skill_loading.py
```

1. `What skills are active?`
2. `Load one active skill by name and summarize its first section.`
3. After editing a file that matches a `paths` pattern, call `activate_skills` and see if more skills turn active.
