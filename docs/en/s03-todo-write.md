# s03: Session State

## Why This Chapter Exists

Without visible short-horizon state, the model often drifts between subtasks and forgets what it intended to do next.

## Core Mechanism

- store a short checklist outside the hidden reasoning
- limit the list to a human-sized plan
- allow only one active item
- treat it as session guidance rather than durable project state

## Mapping To The Python Code

`agents/s03_todo_write.py` keeps a `TodoManager` in memory and exposes it through `todo_write` as the visible session checklist.

## What Is Intentionally Simplified

The important correction is conceptual: this is not yet the durable task runtime. It is only the current session guide.

## Try It

- Run `python agents/s03_todo_write.py` if the filename matches the chapter script, or open the file directly if you are reading first.
- Ask the model to perform one task that clearly needs the new mechanism introduced in this chapter.
- Compare the visible runtime state before and after the tool call or control-flow change.

## Bridge To The Next Chapter

The moment work can be externalized, delegation stops being magical and starts becoming a runtime design choice.
