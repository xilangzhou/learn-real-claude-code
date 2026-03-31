# s07: Persistent Task Runtime

## Why This Chapter Exists

A checklist inside the chat is useful, but it disappears with the session. Serious work tracking needs its own storage and lifecycle.

## Core Mechanism

- persist tasks outside the message history
- support task create, get, list, and update
- treat tasks as durable runtime state
- keep them conceptually separate from session todos

## Mapping To The Python Code

`agents/s07_task_system.py` writes durable state into a dedicated runtime folder so the task plane survives chat churn.

## What Is Intentionally Simplified

The teaching version uses a compact file-backed store. The point is durability and separation of concerns, not production-grade task orchestration.

## Try It

- Run `python agents/s07_task_system.py` if the filename matches the chapter script, or open the file directly if you are reading first.
- Ask the model to perform one task that clearly needs the new mechanism introduced in this chapter.
- Compare the visible runtime state before and after the tool call or control-flow change.

## Bridge To The Next Chapter

With durable state in place, the runtime can start owning work that continues even when the foreground loop moves on.
