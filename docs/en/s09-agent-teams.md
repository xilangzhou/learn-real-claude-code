# s09: Team Mailboxes

`s01 > s02 > s03 > s04 > s05 > s06 | s07 > s08 > [ s09 ] s10 > s11 > s12`

> *More than one worker — you need mailboxes first.* Identity + JSONL inboxes beat a shared implicit mind.
>
> **Harness layer**: collaboration surface — lead and teammates each run their own loop.

## Problem

s04 subagents are one-shot; s08 background is only shell. **Multi-turn collaboration** needs stable identities and addressable inboxes.

## Approach

- **MailboxBus**: `.lrcc/team/inbox/<name>.jsonl`, append on write, **drain** on read.
- **TeamManager**: `.lrcc/team/config.json` roster + status; `team_spawn` starts a teammate thread running `run_loop`, with `before_request` injecting unread inbox before each model call.

Lead tools: `team_spawn`, `send_message` (to a teammate), `read_inbox` (lead’s inbox), `team_list`.

## Behavior

Teammate registry = base tools + `send_message` to others. Lead `send_message` always sends from `"lead"`.

## Changes vs s08

| Piece | s08 | s09 |
|-------|-----|-----|
| Concurrency | background shell only | multiple threads, each an agent loop |
| Comms | none | JSONL mailbox |

## Try it

```sh
cd learn-real-claude-code
python agents/s09_agent_teams.py
```

1. `Spawn a teammate "alice" with a short coding prompt, then send_message to alice.`
2. `read_inbox` to see if the lead got a reply (depends on the model sending back).
3. `team_list` for status.
