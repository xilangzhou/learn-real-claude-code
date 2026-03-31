# s10: Team Protocols

## Why This Chapter Exists

Not every message in a team is just text. Some messages open a lifecycle that the runtime must remember and match later.

## Core Mechanism

- add request ids to important coordination messages
- track pending, approved, and rejected states
- model plan and shutdown as typed requests
- let the runtime poll and resolve protocol state

## Mapping To The Python Code

`agents/s10_team_protocols.py` keeps the lesson grounded by showing that a protocol is just message plus lifecycle state.

## What Is Intentionally Simplified

The teaching version contains only a small set of protocols. The key lesson is that typed coordination needs memory, not just better wording.

## Try It

- Run `python agents/s10_team_protocols.py` if the filename matches the chapter script, or open the file directly if you are reading first.
- Ask the model to perform one task that clearly needs the new mechanism introduced in this chapter.
- Compare the visible runtime state before and after the tool call or control-flow change.

## Bridge To The Next Chapter

If the runtime can coordinate workers explicitly, it can also let them self-coordinate around shared state.
