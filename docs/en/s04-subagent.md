# s04: Delegation Modes

## Why This Chapter Exists

Older teaching material often treats every subagent as a clean-room child. That is too simple to explain modern delegation behavior.

## Core Mechanism

- fresh delegation starts from a clean history
- forked delegation inherits scoped context
- both run a focused child loop
- the parent usually gets back a summary instead of the full child transcript

## Mapping To The Python Code

`agents/s04_subagent.py` models the two modes with one delegate tool so the difference stays visible in the same file.

## What Is Intentionally Simplified

Real systems have more worker types and more careful context inheritance rules. The teaching version keeps only the minimal strategic distinction.

## Try It

- Run `python agents/s04_subagent.py` if the filename matches the chapter script, or open the file directly if you are reading first.
- Ask the model to perform one task that clearly needs the new mechanism introduced in this chapter.
- Compare the visible runtime state before and after the tool call or control-flow change.

## Bridge To The Next Chapter

If workers can be created on demand, the next question is how to load domain knowledge on demand as well.
