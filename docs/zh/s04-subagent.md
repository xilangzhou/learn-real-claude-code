# s04: Delegation Modes (委托模式)

`s01 > s02 > s03 > [ s04 ] s05 > s06 | s07 > s08 > s09 > s10 > s11 > s12`

> *「子活独立跑，父对话只收摘要」* —— 但干净上下文和带上下文的 fork 不是一回事。
>
> **Harness 层**：委托 —— 控制子循环用哪种历史。

## 问题

主对话里堆满工具输出时，「帮我去查一下」这类子任务会把噪声全带进主线。你需要子 worker 只回报结论，而不是整段 transcript。

有时子任务又要延续当前讨论：`fresh` 太干，`fork` 更合适。

## 解决方案

一个 `delegate` 工具，参数里选 `mode`：

- **fresh**：子循环从单条 user 消息开始，历史为空。
- **fork**：用 `summarize_messages(parent_messages, keep_last=8)` 压成短摘要，包在 `<inherited-context>` 里再拼指令。

子循环仍走同一个 `run_loop()`，registry 是全套 `base_tools`，没有 `delegate`（避免递归委托）。

## 工作原理

`DelegationRunner` 在每次 `run_session` 时挂上当前父 `messages`，handler 里调 `run_worker(..., parent_messages=self.parent_messages)`。

## 相对 s03 的变更

| 组件 | s03 | s04 |
|------|-----|-----|
| 子任务 | 无 | `delegate` + 子 `run_loop` |
| 上下文 | 单轨 | 父 / 子分离 |

## 试一试

```sh
cd learn-real-claude-code
python agents/s04_subagent.py
```

1. `Delegate in fresh mode: list files in agents/ and return a one-line summary.`
2. `Fork mode: continue from our thread — check whether s04 uses summarize_messages.`
