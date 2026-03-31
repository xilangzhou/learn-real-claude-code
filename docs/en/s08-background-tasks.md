# s08: Background Runtime

## Why This Chapter Exists

Some operations are too slow to sit inline inside the foreground reasoning loop.

## Core Mechanism

- spawn long work into a background runtime
- return a stable handle immediately
- allow explicit polling
- feed completion notifications back into the foreground conversation

## Mapping To The Python Code

`agents/s08_background_tasks.py` keeps the core lesson focused on handles, polling, and notification reinjection.

## What Is Intentionally Simplified

The teaching runtime is intentionally small. The point is to show why background work needs runtime semantics, not just threads.

## Try It

- Run `python agents/s08_background_tasks.py` if the filename matches the chapter script, or open the file directly if you are reading first.
- Ask the model to perform one task that clearly needs the new mechanism introduced in this chapter.
- Compare the visible runtime state before and after the tool call or control-flow change.

## Bridge To The Next Chapter

If the runtime can own multiple units of work, the next step is to let multiple named workers collaborate on them.
