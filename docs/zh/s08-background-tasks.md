# s08: Background Runtime (后台任务)

`s01 > s02 > s03 > s04 > s05 > s06 | s07 > [ s08 ] s09 > s10 > s11 > s12`

> *「慢的别堵在主循环里」* —— 线程跑命令，结果排队注回对话。
>
> **Harness 层**：后台 —— harness 管生命周期，模型只发指令。

## 问题

`pytest`、安装依赖这类命令要跑很久。阻塞式执行的话，模型只能干等，交互很差。

## 解决方案

`BackgroundManager.run()` 起守护线程跑 `subprocess`，任务 id 短 uuid；完成时把结果写进线程安全队列。每次 **LLM 请求前** `before_request` 里 `drain_notifications()`，若有完成项，追加一条 user 消息 `<task-notifications>...</task-notifications>`。

`background_check` 可查单个或全部任务状态。

## 工作原理

主循环仍是单线程调度；并行只发生在子进程与收集结果。超时 300s 会记为 timeout。

## 相对 s07 的变更

| 组件 | s07 | s08 |
|------|-----|-----|
| 执行 | 同步 | + 后台 shell + 通知 |
| 工具 | 任务四件套 | + `background_run`、`background_check` |

## 试一试

```sh
cd learn-real-claude-code
python agents/s08_background_tasks.py
```

1. `Run sleep 3 && echo done in background, then do something else until notification appears.`
2. `List background tasks with background_check.`
