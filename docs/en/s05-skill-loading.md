# s05: Skill Discovery

## Why This Chapter Exists

Packing every domain instruction into the system prompt makes the context heavy and unfocused.

## Core Mechanism

- treat a skill as metadata plus instructions
- discover available skills from directories and conditions
- activate only the relevant skill for the current task
- inject the content late instead of keeping it always in context

## Mapping To The Python Code

`agents/s05_skill_loading.py` keeps the lesson centered on discovery, filtering, and activation rather than on fancy prompt templating.

## What Is Intentionally Simplified

The full product can load from many sources and apply richer matching rules. The teaching version keeps just enough structure to explain why the system exists.

## Try It

- Run `python agents/s05_skill_loading.py` if the filename matches the chapter script, or open the file directly if you are reading first.
- Ask the model to perform one task that clearly needs the new mechanism introduced in this chapter.
- Compare the visible runtime state before and after the tool call or control-flow change.

## Bridge To The Next Chapter

Late-loaded knowledge helps, but long sessions still fail if the harness cannot manage its context window.
