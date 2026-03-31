# s11: Self-Organizing Workers

## Why This Chapter Exists

A team still feels scripted if every action comes from the lead. Useful autonomy appears when workers can notice, claim, and continue work on their own.

## Core Mechanism

- maintain a shared task board
- give each worker an inbox
- let workers poll during idle periods
- allow local policies such as auto-claiming open work

## Mapping To The Python Code

`agents/s11_autonomous_agents.py` keeps autonomy legible by grounding it in shared state and small rules instead of mystery.

## What Is Intentionally Simplified

The local policies here are intentionally simple. The lesson is emergence from runtime structure, not optimal scheduling.

## Try It

- Run `python agents/s11_autonomous_agents.py` if the filename matches the chapter script, or open the file directly if you are reading first.
- Ask the model to perform one task that clearly needs the new mechanism introduced in this chapter.
- Compare the visible runtime state before and after the tool call or control-flow change.

## Bridge To The Next Chapter

Once workers can self-organize, the last missing piece is to isolate their execution surfaces so concurrent work does not collide.
