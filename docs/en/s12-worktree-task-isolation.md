# s12: Worktree Isolation

`s01 > s02 > s03 > s04 > s05 > s06 | s07 > s08 > s09 > s10 > s11 > [ s12 ]`

> *Tasks describe intent; directories describe execution.* Split control plane and execution plane.
>
> **Harness layer**: isolation — fewer file collisions when work runs in parallel.

## Problem

Many workers editing one working tree still stomp each other’s uncommitted changes. s11 can claim tasks, but if everyone shares one tree, conflicts remain.

## Approach

- **TaskBoard** (`.lrcc/isolation/tasks/`): task JSON includes `worktree`; `bind(task_id, name)` moves `pending` → `in_progress` when appropriate.
- **WorktreeStore**: under repo root `.lrcc/isolation/worktrees/`, uses `git worktree add -b wt/<name>` when a git repo is detected; otherwise plain directories. `index.json` records name, path, branch, `task_id`.
- **EventLog**: `events.jsonl` for create/remove/task.completed.

Tools: `task_create`, `task_list`, `worktree_create` (optional `task_id`), `worktree_remove` (optional `complete_task` to finish the bound task), `worktree_list`, `worktree_events`.

## Behavior

`REPO_ROOT = detect_repo_root(cwd) or cwd` — without git, directory isolation still teaches the idea.

## Changes vs s11

| Piece | s11 | s12 |
|-------|-----|-----|
| Execution | shared cwd | per-lane path |
| On disk | autonomy tasks | + worktree index + event log |

## Try it

```sh
cd learn-real-claude-code
python agents/s12_worktree_task_isolation.py
```

1. `task_create` then `worktree_create` with `task_id`.
2. `worktree_list` / `worktree_events` for registry and log.
3. `worktree_remove` with `complete_task=true` to finish.
