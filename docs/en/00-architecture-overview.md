# Architecture overview

This course pulls the runtime ideas that matter from real `claude-code`-style agents and lays them out in small Python harnesses under `agents/`. The narrative style matches `learn-claude-code` (one main mechanism per chapter), but paths and on-disk layout are this repo’s own (notably state under `.lrcc/`).

## What you are learning

Models reason, but they do not automatically read disks, run commands, or edit files. The starting point for an agent is the **loop**: request → model may call tools → execute → append results → repeat until the model stops asking for tools.

On that skeleton the chapters add: structured tools, session todos, delegation modes, on-demand skills, context governance, durable tasks, background notifications, team mailboxes, protocol state, autonomous polling, and task–worktree binding. It is a path from “runs” to “coordinates and isolates,” not a flat feature list.

## How to read the repo

| Path | Role |
|------|------|
| `agents/s*.py` | Minimal runnable harness per chapter |
| `agents/_shared.py` | Shared `run_loop`, `ToolRegistry`, base tools |
| `docs/{en,zh,ja}/` | Chapter text (same content as the web tutorial) |
| `web/` | Course UI and visualizations |

To run a chapter: from the repo root, `python agents/sXX_....py`, with `MODEL_ID` set (and optional `ANTHROPIC_BASE_URL`).
