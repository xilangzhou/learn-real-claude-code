# s08: Background Runtime

`s01 > s02 > s03 > s04 > s05 > s06 | s07 > [ s08 ] s09 > s10 > s11 > s12`

> *Do not block the main loop on slow commands — run them in a thread, queue results back into the chat.*
>
> **Harness layer**: background — the harness owns lifecycle; the model only issues commands.

## Problem

`pytest`, installs, builds — they take minutes. Blocking the loop means the model waits and the UX feels frozen.

## Approach

`BackgroundManager.run()` starts a daemon thread around `subprocess`, short uuid task id; on completion, push results into a thread-safe queue. On **every LLM request**, `before_request` runs `drain_notifications()` and, if anything completed, appends a user message `<task-notifications>...</task-notifications>`.

`background_check` inspects one task or lists all.

## Behavior

The main scheduling loop stays single-threaded; parallelism is subprocess + result collection. Timeout after 300s is recorded as timeout.

## Changes vs s07

| Piece | s07 | s08 |
|-------|-----|-----|
| Execution | synchronous | + background shell + notifications |
| Tools | task CRUD set | + `background_run`, `background_check` |

## Try it

```sh
cd learn-real-claude-code
python agents/s08_background_tasks.py
```

1. `Run sleep 3 && echo done in background, then do something else until notification appears.`
2. `List background tasks with background_check.`
