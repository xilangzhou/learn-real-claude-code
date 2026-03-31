# s03: Session State

`s01 > s02 > [ s03 ] s04 > s05 > s06 | s07 > s08 > s09 > s10 > s11 > s12`

> *Multi-step work: write the plan, then execute — session todos navigate the turn, not the durable task graph.*
>
> **Harness layer**: session state — pull “where we are” out of chit-chat.

## Problem

With many steps, the model repeats work or skips steps. Relying on chat memory alone drifts as context grows.

## Approach

Add `todo_write` backed by an in-memory `TodoManager`: `pending` / `in_progress` / `completed`, **only one `in_progress` at a time**, and `in_progress` requires `active_form` (a short line for what is happening now).

Unlike the older course: this repo has **no** “nag after N rounds” logic — validation is schema + system prompt only.

## Behavior

Updates `render()` into readable text in `tool_result`. When everything completes, the list clears.

This is **not** chapter 7’s on-disk task graph: here we keep **this conversation** on track; s07 tracks **cross-session, recoverable** units of work.

## Changes vs s02

| Piece | s02 | s03 |
|-------|-----|-----|
| Tools | base four | + `todo_write` |
| State | none | `TodoManager.items` |

## Try it

```sh
cd learn-real-claude-code
python agents/s03_todo_write.py
```

1. `Refactor a small function: use todo_write to track 3 steps, then execute.`
2. `Fix imports in one file — keep exactly one in_progress item.`
