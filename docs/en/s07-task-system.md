# s07: Persistent Tasks

`s01 > s02 > s03 > s04 > s05 > s06 | [ s07 ] s08 > s09 > s10 > s11 > s12`

> *Tasks live on disk — they do not disappear when the chat is compacted.*
>
> **Harness layer**: durability — `blocked_by` lives in files, not in the model’s head.

## Problem

s03 todos vanish when the session ends; after s06 compaction, task descriptions in chat can vanish too. Real work needs **multi-turn, recoverable** records.

## Approach

`TaskStore` writes under `.lrcc/tasks/<task_list_id>/` (default `default`), one JSON per task: `id`, `subject`, `status`, `owner`, `blocked_by`, timestamps, etc. On `task_update` to completed, `_clear_dependency` removes that id from other tasks’ `blocked_by`.

## Tools

`task_create`, `task_get`, `task_list`, `task_update`. IDs use a high-water mark file to avoid collisions with deleted files.

## Changes vs s06

| Piece | s06 | s07 |
|-------|-----|-----|
| Work units | none | on-disk JSON tasks |
| Dependencies | none | `blocked_by` lists |

## Try it

```sh
cd learn-real-claude-code
python agents/s07_task_system.py
```

1. `Create three tasks A,B,C; make B depend on A, C depend on B.`
2. `Complete A and list — B should be unblocked.`
