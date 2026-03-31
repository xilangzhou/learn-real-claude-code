# s10: Team Protocols

`s01 > s02 > s03 > s04 > s05 > s06 | s07 > s08 > s09 > [ s10 ] s11 > s12`

> *If you need a handshake, plain chat is not enough.* `request_id` + pending / approved / rejected.
>
> **Harness layer**: protocol state — in-memory tables under `ProtocolState` (directory `.lrcc/protocols/` exists for storage layout; this lesson uses the in-memory maps).

## Problem

“Please shut down” in a free-form message is ambiguous: who is waiting, was it approved? Shutdown and plan changes need **correlatable request IDs**.

## Approach

`ProtocolState` holds `shutdown_requests` and `plan_requests` keyed by short `request_id`. Tools:

- `request_shutdown` / `respond_shutdown`
- `submit_plan` / `review_plan`
- `protocol_state` to dump both tables

`resolve()` sets `approved` or `rejected` and optional `feedback`.

This version does **not** route protocol over custom mailbox message types; state lives in `ProtocolState`. The teaching point is an **ID’d state machine**, not a full message bus.

## Changes vs s09

| Piece | s09 | s10 |
|-------|-----|-----|
| Coordination | free text | structured shutdown / plan |
| Tracking | none | `request_id` + status fields |

## Try it

```sh
cd learn-real-claude-code
python agents/s10_team_protocols.py
```

1. `request_shutdown` for a name, then `respond_shutdown` approve or reject.
2. `submit_plan` then `review_plan` for one plan.
3. `protocol_state` to inspect both tables.
