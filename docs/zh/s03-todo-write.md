# s03: Session State (会话待办)

`s01 > s02 > [ s03 ] s04 > s05 > s06 | s07 > s08 > s09 > s10 > s11 > s12`

> *「多步活，先写清再干」* —— todo 是会话内的导航，不是持久任务系统。
>
> **Harness 层**：会话状态 —— 把「做到哪了」从闲聊里拽出来。

## 问题

步骤一多，模型容易重复劳动或跳步。纯靠对话记忆，长一点就漂。

## 解决方案

加一个 `todo_write` 工具，背后是一个内存里的 `TodoManager`：维护 `pending` / `in_progress` / `completed`，**同一时刻只允许一条 `in_progress`**，`in_progress` 必须带 `active_form`（当前正在做的那句短描述）。

和旧课不同：本仓库 **没有**「几轮不更新就 nag」的逻辑，约束全靠 schema + 系统提示。

## 工作原理

`todos` 更新后 `render()` 成可读文本返回给 `tool_result`。全部完成时列表会清空成「没有未完成项」。

这和第七章的磁盘任务图是两层东西：这里管 **这一轮对话怎么不乱**，第七章管 **跨会话、可恢复的工作单元**。

## 相对 s02 的变更

| 组件 | s02 | s03 |
|------|-----|-----|
| 工具 | 基础四件套 | + `todo_write` |
| 状态 | 无 | `TodoManager.items` |

## 试一试

```sh
cd learn-real-claude-code
python agents/s03_todo_write.py
```

1. `Refactor a small function: use todo_write to track 3 steps, then execute.`
2. `Fix imports in one file — keep exactly one in_progress item.`
