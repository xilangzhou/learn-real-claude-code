# s06: Context Management Stack

## Why This Chapter Exists

A long-running agent does not have one context problem. It has many: oversized tool outputs, stale history, and moments where the model itself needs a reset.

## Core Mechanism

- trim large tool results before they dominate history
- maintain rolling summaries for continuity
- allow explicit manual compact requests
- treat these as different interventions rather than one button

## Mapping To The Python Code

`agents/s06_context_compact.py` introduces a context manager object that owns the policies instead of hardcoding one compression pass into the loop.

## What Is Intentionally Simplified

The real product can have additional collapse paths and budget heuristics. The teaching version is a stack, but still a simplified stack.

## Try It

- Run `python agents/s06_context_compact.py` if the filename matches the chapter script, or open the file directly if you are reading first.
- Ask the model to perform one task that clearly needs the new mechanism introduced in this chapter.
- Compare the visible runtime state before and after the tool call or control-flow change.

## Bridge To The Next Chapter

Once history can be managed, the runtime is ready to move durable work state out of the transcript entirely.
