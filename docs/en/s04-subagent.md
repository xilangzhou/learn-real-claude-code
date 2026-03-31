# s04: Delegation Modes

`s01 > s02 > s03 > [ s04 ] s05 > s06 | s07 > s08 > s09 > s10 > s11 > s12`

> *Child work runs separately; the parent only gets a summary — but a clean history and a fork with inherited context are different beasts.*
>
> **Harness layer**: delegation — which history the child loop uses.

## Problem

When the main thread is full of tool noise, “go check this for me” drags everything into the child. You want a concise answer, not a full transcript.

Sometimes the child must continue the thread: **fresh** is too bare; **fork** fits.

## Approach

One `delegate` tool with `mode`:

- **fresh**: child starts from a single user message; empty history.
- **fork**: compress recent parent turns with `summarize_messages(parent_messages, keep_last=8)`, wrap in `<inherited-context>`, then add the directive.

The child still uses `run_loop()` with full `base_tools` and **no** `delegate` (no recursive delegation).

## Wiring

`DelegationRunner` snapshots parent `messages` each `run_session`; the handler calls `run_worker(..., parent_messages=self.parent_messages)`.

## Changes vs s03

| Piece | s03 | s04 |
|-------|-----|-----|
| Subtasks | none | `delegate` + child `run_loop` |
| Context | single track | parent / child split |

## Try it

```sh
cd learn-real-claude-code
python agents/s04_subagent.py
```

1. `Delegate in fresh mode: list files in agents/ and return a one-line summary.`
2. `Fork mode: continue from our thread — check whether s04 uses summarize_messages.`
