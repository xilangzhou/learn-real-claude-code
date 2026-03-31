# Architecture Overview

This project is no longer trying to imitate a large coding agent line by line. It teaches a smaller Python runtime whose mechanism boundaries were corrected against the source we studied.

## What the course is optimizing for

- Mechanism accuracy over superficial similarity
- Teaching clarity over product-level complexity
- A learning path that introduces one runtime concern at a time

## The five layers

- Tools and execution: how the model touches the outside world
- Planning and coordination: how work is shaped and delegated
- Memory management: how long sessions stay coherent
- Concurrency: how slow work continues without blocking the foreground loop
- Collaboration: how multiple workers share state, protocols, and isolation

## How to read the repo

- `agents/` contains the chapter-sized Python teaching implementations
- `docs/` contains the chapter text in three locales
- `web/` renders the curriculum, source views, comparisons, and visualizations
- `tests/` gives a small safety net around the teaching runtime
