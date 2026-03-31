# s11: Self-Organizing Workers

`s01 > s02 > s03 > s04 > s05 > s06 | s07 > s08 > s09 > s10 > [ s11 ] s12`

> *Idle is fine; when there is work, claim it.* Task board + inbox + `before_request` injection.
>
> **Harness layer**: autonomy entry — the harness feeds hints; the model decides whether to act.

## Problem

If every action needs a human instruction, multi-agent is just scripts with different voices. You want **unclaimed tasks** and **new mail** to show up when the model “opens its eyes”.

## Approach

- **TaskBoard**: `.lrcc/autonomy/tasks/*.json`; `unclaimed()` picks `pending`, no `owner`, no `blocked_by`.
- **Inbox**: `.lrcc/autonomy/inbox/*.jsonl`, same pattern as mailboxes.
- **`before_request`**: inject unread inbox first; else if there is an unclaimed task, inject `<auto-claim-opportunity>` for the first one.
- Tools: `task_create`, `task_list`, `claim_task`, `send_message`, `idle` (“pause this turn for the harness”).

## Behavior

Autonomy is not magic — it is **extra structured user messages before each request**. `claim_task` writes owner + status.

For session timing and `idle-timeout` behavior, see `s11_autonomous_agents.py` as source of truth.

## Changes vs s10

| Piece | s10 | s11 |
|-------|-----|-----|
| Task source | no shared board | `.lrcc/autonomy/tasks` |
| Drive | tools only | + `before_request` opportunities |

## Try it

```sh
cd learn-real-claude-code
python agents/s11_autonomous_agents.py
```

1. Create several `task_create` items and watch for `claim_task` after injection.
2. `send_message` to `lead` and see whether the next turn includes `<inbox>`.
