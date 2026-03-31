# s12: Worktree Isolation

## Why This Chapter Exists

Shared logical state is not enough if multiple workstreams still mutate the same filesystem surface.

## Core Mechanism

- bind a task to an isolated worktree
- make isolation part of the runtime rather than an operator trick
- record lifecycle events in an event log
- treat task state as control plane and filesystem isolation as execution plane

## Mapping To The Python Code

`agents/s12_worktree_task_isolation.py` ties together task board state, worktree provisioning, and an event log to make isolation inspectable.

## What Is Intentionally Simplified

The teaching version does not need every branch-management edge case. The point is to make filesystem isolation a first-class part of the curriculum.

## Try It

- Run `python agents/s12_worktree_task_isolation.py` if the filename matches the chapter script, or open the file directly if you are reading first.
- Ask the model to perform one task that clearly needs the new mechanism introduced in this chapter.
- Compare the visible runtime state before and after the tool call or control-flow change.

## Bridge To The Next Chapter

At this point the curriculum has reached a believable small runtime: loop, tools, visible state, delegation, memory, tasks, concurrency, collaboration, and isolation.
