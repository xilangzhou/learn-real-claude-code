# s07: Persistent Tasks (持久任务)

`s01 > s02 > s03 > s04 > s05 > s06 | [ s07 ] s08 > s09 > s10 > s11 > s12`

> *「任务活在磁盘上，不跟对话一起被压缩掉」* —— 控制面先与 transcript 分离。
>
> **Harness 层**：持久化 —— `blocked_by` 在文件里，不在模型脑子里。

## 问题

s03 的 todo 会话结束就没了；s06 压缩后，对话里的任务描述也可能丢。真正干活需要 **跨多轮、可恢复** 的任务记录。

## 解决方案

`TaskStore` 把任务写到 `.lrcc/tasks/<task_list_id>/`（默认 `default`），每任务一个 JSON：`id`、`subject`、`status`、`owner`、`blocked_by`、时间戳等。`task_update` 完成某任务时 `_clear_dependency` 会把该 id 从其它任务的 `blocked_by` 里摘掉。

## 工作原理

工具集：`task_create`、`task_get`、`task_list`、`task_update`。ID 用高水位文件避免和已删文件冲突。

## 相对 s06 的变更

| 组件 | s06 | s07 |
|------|-----|-----|
| 工作单元 | 无 | 磁盘 JSON 任务 |
| 依赖 | 无 | `blocked_by` 列表 |

## 试一试

```sh
cd learn-real-claude-code
python agents/s07_task_system.py
```

1. `Create three tasks A,B,C; make B depend on A, C depend on B.`
2. `Complete A and list — B should be unblocked.`
