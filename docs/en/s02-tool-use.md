# s02: Tool Protocol

`s01 > [ s02 ] s03 > s04 > s05 > s06 | s07 > s08 > s09 > s10 > s11 > s12`

> *Add capability by adding tools, not by rewriting the loop — name, schema, handler, all in one registry.*
>
> **Harness layer**: dispatch — widen what the model can touch safely.

## Problem

Bash-only means every file op is shell glue; paths and quoting break easily. Dedicated read/write/edit handlers can sandbox and truncate in one place.

## Shape of the solution

```
+--------+      +-------+      +------------------+
|  User  | ---> |  LLM  | ---> | ToolRegistry     |
+--------+      +---+---+      |  .call(name,**)  |
                    ^          +--------+---------+
                    |                   |
                    +---- tool_result ---+
```

`run_loop()` stays the same; `ToolRegistry` now holds `bash`, `read_file`, `write_file`, `edit_file` from `base_tools()`.

## How it works

`base_tools()` wires `input_schema` and closure handlers with `workdir`. `safe_path()` keeps paths inside the workspace; reads/writes are length-capped in `_shared.py`.

`s02_tool_use.py` nudges the model: use file tools for files; use bash only when you need shell semantics.

## Changes vs s01

| Piece | s01 | s02 |
|-------|-----|-----|
| Tool count | 1 | 4 (bash + read/write/edit) |
| Dispatch | bash only | `ToolRegistry.call` by name |
| Paths | none | `safe_path` |

## Try it

```sh
cd learn-real-claude-code
python agents/s02_tool_use.py
```

1. `Read README.md (first 40 lines).`
2. `Add a tiny note.txt with today's date.`
3. `Edit note.txt to append one line.`
