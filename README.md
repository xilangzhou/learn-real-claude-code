[English](./README.md) | [中文](./README-zh.md) | [日本語](./README-ja.md)

# Learn Real Claude Code

## What This Repo Is

Learn Real Claude Code is a teaching project about coding-agent harness design.

The goal is not to reproduce a production system line by line. The goal is to
teach the mechanisms that still matter when the product gets large:

- the agent loop
- tool protocols
- session state vs persistent task state
- delegation modes
- late-bound skills
- context management
- background runtime
- multi-agent coordination
- worktree isolation

## Repository Shape

```text
learn-real-claude-code/
├── agents/   # s01-s12 teaching scripts + s_full reference harness
├── tests/    # smoke checks for the teaching scripts
└── web/      # interactive learning site and chapter metadata
```

## Course Design

Each script in `agents/` is intentionally small and runnable.

They are teaching implementations, not miniature copies of a product build.
Whenever the real system is more complex, this repo prefers:

1. keeping the correct architectural boundary
2. simplifying the implementation
3. saying clearly what was simplified

## Updated Learning Path

1. `s01` The Agent Loop
2. `s02` Tool Protocol
3. `s03` Session State
4. `s04` Delegation Modes
5. `s05` Skill Discovery
6. `s06` Context Management Stack
7. `s07` Persistent Task Runtime
8. `s08` Background Runtime
9. `s09` Team Mailboxes
10. `s10` Team Protocols
11. `s11` Self-Organizing Workers
12. `s12` Worktree Isolation

## How To Use It

Run a chapter directly:

```bash
python agents/s01_agent_loop.py
```

Then move forward in order. The later chapters assume the vocabulary from the
earlier ones even when the code stays self-contained.

## Reference Script

`agents/s_full.py` is the compact reference harness. It combines the corrected
teaching ideas in one file, but it is still a teaching artifact, not a claim of
full production parity.

## Acknowledgement

This project is based on [shareAI-lab/learn-claude-code](https://github.com/shareAI-lab/learn-claude-code).
We appreciate their work and thank them for their contributions.
