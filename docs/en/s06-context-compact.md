# s06: Context Stack

`s01 > s02 > s03 > s04 > s05 > [ s06 ] | s07 > s08 > s09 > s10 > s11 > s12`

> *Context fills up — fix it in layers, not with one magic compact.*
>
> **Harness layer**: governance — touch history on every request.

## Problem

Long tool output and long sessions balloon the serialized messages. You need **automatic trimming**, **threshold resets**, and a path for **explicit compact** from the model.

## Approach

`ContextManager` + `run_loop(..., before_request=...)`:

1. **Result budget**: older `tool_result` blobs beyond ~500 chars get truncated with `[truncated by result budget]`.
2. **Micro-summary**: after enough assistant turns, very long legacy **user string** messages collapse to placeholders (teaching version signals “folded”).
3. **Threshold compact**: if estimated tokens (JSON length / 4) > 50000, write the transcript to `.transcripts/compact_*.jsonl` and replace history with one bounded user message from `summarize_messages`.
4. **`compact` tool**: returns “finish this tool turn, then compact”; `run_session` runs `compact_now` after the loop if a manual compact was requested.

Same story as the old “micro + auto + manual” lesson, but the implementation splits across **`before_request`** and **`compact_handler`** — follow the Python when reading.

## Changes vs s05

| Piece | s05 | s06 |
|-------|-----|-----|
| History | grows raw | layered `before_request` + `compact` |
| Disk | none | transcripts under `.transcripts/` |

## Try it

```sh
cd learn-real-claude-code
python agents/s06_context_compact.py
```

1. Read many files in a row and watch older results shrink.
2. Drive a long conversation to hit the threshold, or call the `compact` tool yourself.
