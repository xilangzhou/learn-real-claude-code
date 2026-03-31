# s01: The Agent Loop

## Why This Chapter Exists

A coding agent does not start as a planner, a team, or a workflow graph. It starts as a loop that can observe and act.

## Core Mechanism

- append the user message to history
- call the model with tools
- if the model asks for a tool, execute it and append the result
- if not, return the final answer

## Mapping To The Python Code

`agents/s01_agent_loop.py` keeps only the visible teaching shell while `agents/_shared.py` carries the reusable loop helper.

## What Is Intentionally Simplified

The real system contains streaming, retries, permissions, token budgeting, and interruption logic. This chapter intentionally ignores all of that so the invariant stays visible.

## Try It

- Run `python agents/s01_the_agent_loop.py` if the filename matches the chapter script, or open the file directly if you are reading first.
- Ask the model to perform one task that clearly needs the new mechanism introduced in this chapter.
- Compare the visible runtime state before and after the tool call or control-flow change.

## Bridge To The Next Chapter

Once the loop exists, the next question is not how to rewrite it, but how to add new capabilities without touching it.
