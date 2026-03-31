# s09: Team Mailboxes

## Why This Chapter Exists

Adding more agents is not enough. Collaboration only becomes teachable when messages, identity, and routing are explicit.

## Core Mechanism

- give workers stable names
- route communication through mailboxes
- let each worker keep its own loop and state
- treat message passing as the collaboration surface

## Mapping To The Python Code

`agents/s09_agent_teams.py` introduces a mailbox bus and team manager rather than pretending workers share one hidden mind.

## What Is Intentionally Simplified

The message transport is intentionally plain. The teaching target is explicit collaboration, not transport sophistication.

## Try It

- Run `python agents/s09_agent_teams.py` if the filename matches the chapter script, or open the file directly if you are reading first.
- Ask the model to perform one task that clearly needs the new mechanism introduced in this chapter.
- Compare the visible runtime state before and after the tool call or control-flow change.

## Bridge To The Next Chapter

Once messages exist, the runtime can start distinguishing ordinary chat from typed coordination requests.
