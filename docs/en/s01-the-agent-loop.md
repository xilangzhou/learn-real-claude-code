# s01: The Agent Loop

`[ s01 ] s02 > s03 > s04 > s05 > s06 | s07 > s08 > s09 > s10 > s11 > s12`

> *One loop plus one tool surface is enough to behave like an agent — get the closed loop working before planners, memory, or multi-agent.*
>
> **Harness layer**: the loop — the smallest wiring between the model and the real environment.

## Problem

The model cannot touch disk or the shell by itself. Without a loop, you paste every tool result back by hand — *you* are the loop.

## Shape of the solution

```
+--------+      +-------+      +---------+
|  User  | ---> |  LLM  | ---> |  Tool   |
| prompt |      |       |      | execute |
+--------+      +---+---+      +----+----+
                    ^                |
                    |   tool_result  |
                    +----------------+
        exit when stop_reason != tool_use
```

## How it works in this repo

The loop lives in `agents/_shared.py` as `run_loop()`: accumulate `messages`, call the API with `registry.definitions()` each turn; if there is no `tool_use` in the response, return; otherwise call `registry.call()` for each block and append `tool_result` as the next user message.

`s01_agent_loop.py` registers **only bash** (`ToolRegistry([base_tools(WORKDIR, include_write=False)[0]])`) on purpose. The system prompt says: act first, explain after.

## What changed vs a bare model

| Piece | Before | After (s01) |
|-------|--------|-------------|
| Control flow | none | `while` + `max_turns` cap |
| Tools | none | `bash` only |
| Messages | none | growing assistant / user (incl. tool_result) |

## Try it

```sh
cd learn-real-claude-code
python agents/s01_agent_loop.py
```

Example prompts (English usually works best):

1. `List the top-level directories here and say what this repo is for.`
2. `Create a small hello.py and show its contents with cat.`
3. `What git branch are we on?`
