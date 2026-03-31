# s11: Self-Organizing Workers (自组织工作者)

`s01 > s02 > s03 > s04 > s05 > s06 | s07 > s08 > s09 > s10 > [ s11 ] s12`

> *「没活可以闲，有活自己领」* —— 看板 + 收件箱 + `before_request` 注入。
>
> **Harness 层**：自治入口 —— harness 塞线索，模型决定动不动手。

## 问题

若每件事都要人下指令，多 agent 只是脚本换人跑。你希望 **未认领任务** 和 **新邮件** 在模型睁眼时就能看见。

## 解决方案

- **TaskBoard**：`.lrcc/autonomy/tasks/*.json`，`unclaimed()` 找 `pending`、无 `owner`、无 `blocked_by`。
- **Inbox**：`.lrcc/autonomy/inbox/*.jsonl`，逻辑同邮箱。
- **`before_request`**：优先注入未读 inbox；否则若存在未认领任务，注入 `<auto-claim-opportunity>` 提示第一条。
- 工具：`task_create`、`task_list`、`claim_task`、`send_message`、`idle`（表示「本轮先停，交给 harness」）。

## 工作原理

自治不是模型「变聪明了」，而是 **每轮请求前** 多了一段结构化输入。认领用 `claim_task` 写回 owner 与状态。

（实现里还有会话时长与 `idle-timeout` 的占位逻辑，读代码时以 `s11_autonomous_agents.py` 为准。）

## 相对 s10 的变更

| 组件 | s10 | s11 |
|------|-----|-----|
| 任务来源 | 无共享看板 | `.lrcc/autonomy/tasks` |
| 驱动方式 | 纯工具 | + `before_request` 注入机会 |

## 试一试

```sh
cd learn-real-claude-code
python agents/s11_autonomous_agents.py
```

1. `task_create` 几条，再观察模型是否在注入提示后 `claim_task`。
2. 用 `send_message` 给 `lead` 发信，看下一轮是否进 `<inbox>`。
