[English](./README.md) | [中文](./README-zh.md) | [日本語](./README-ja.md)

# Learn Real Claude Code

## 这是什么

Learn Real Claude Code 是一个讲 coding agent harness 设计的教学项目。

它的目标不是逐行复刻某个生产系统，而是做一套尽量忠于真实机制的
Python 课程，重点讲清楚这些能力：

- agent loop
- tool protocol
- 会话级状态与持久化任务状态
- delegation 模式
- 按需加载的 skills
- context management
- background runtime
- 多 agent 协作
- worktree 隔离

## 仓库结构

```text
learn-real-claude-code/
├── agents/   # s01-s12 教学脚本 + s_full 参考实现
├── tests/    # 教学脚本 smoke test
└── web/      # 交互式学习站与章节元数据
```

## 课程原则

`agents/` 中的每个脚本都保持“小、可运行、可阅读”。

它们是教学实现，不是假装自己就是生产代码的缩微版。只要真实系统更复杂，
这个仓库就优先遵守三条原则：

1. 架构边界要讲对
2. 实现可以简化
3. 简化之处要说清楚

## 更正后的学习路径

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

## 使用方式

直接运行某一章：

```bash
python agents/s01_agent_loop.py
```

建议严格按顺序学习。后面的章节虽然仍然是单文件实现，但默认你已经掌握前面几章的概念。

## 参考脚本

`agents/s_full.py` 是一份压缩后的参考 harness。它把更正后的教学机制放到同一个文件里，
但它仍然只是教学产物，不代表完整生产实现。
