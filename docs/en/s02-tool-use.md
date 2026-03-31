# s02: Tool Protocol

## Why This Chapter Exists

A loop with one action surface is real, but still too crude. The next step is to make capabilities explicit and structured.

## Core Mechanism

- define tools as named protocol objects
- give each tool an input schema
- register them in one registry
- let the loop dispatch by tool name

## Mapping To The Python Code

`agents/s02_tool_use.py` keeps the loop unchanged and only swaps the tool pool from one bash tool to a structured registry.

## What Is Intentionally Simplified

The full product tool layer would also care about approvals, rendering, rich outputs, and telemetry. Here we keep only name, schema, and handler.

## Try It

- Run `python agents/s02_tool_use.py` if the filename matches the chapter script, or open the file directly if you are reading first.
- Ask the model to perform one task that clearly needs the new mechanism introduced in this chapter.
- Compare the visible runtime state before and after the tool call or control-flow change.

## Bridge To The Next Chapter

Once tools are stable, the agent can start keeping visible state about its own work.
