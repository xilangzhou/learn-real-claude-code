# s12: Worktree Isolation (Worktree 隔离)

`s01 > s02 > s03 > s04 > s05 > s06 | s07 > s08 > s09 > s10 > s11 > [ s12 ]`

> *「任务管目标，目录管执行」* —— 控制面与执行面分开。
>
> **Harness 层**：隔离 —— 并行时少踩文件。

## 问题

多人同时改同一工作树，未提交改动会互相踩。s11 能认领任务，但若执行仍在同一目录，冲突照旧。

## 解决方案

- **TaskBoard**（`.lrcc/isolation/tasks/`）：任务 JSON 带 `worktree` 字段；`bind(task_id, name)` 时若仍为 `pending` 则置 `in_progress`。
- **WorktreeStore**：在仓库根下 `.lrcc/isolation/worktrees/`，若检测到 git 仓库则 `git worktree add -b wt/<name>`；否则只建目录。`index.json` 登记 name、path、branch、`task_id`。
- **EventLog**：`events.jsonl` 记录 create/remove/task.completed 等。

工具：`task_create`、`task_list`、`worktree_create`（可选 `task_id` 绑定）、`worktree_remove`（可选 `complete_task` 同步完成任务）、`worktree_list`、`worktree_events`。

## 工作原理

`REPO_ROOT = detect_repo_root(cwd) or cwd`，没有 git 时退化为普通目录隔离，课仍能跑。

## 相对 s11 的变更

| 组件 | s11 | s12 |
|------|-----|-----|
| 执行位置 | 共享 cwd | 每 lane 独立 path |
| 磁盘 | autonomy 任务 | + worktree 索引 + 事件流 |

## 试一试

```sh
cd learn-real-claude-code
python agents/s12_worktree_task_isolation.py
```

1. `task_create` 再 `worktree_create` 带上 `task_id`。
2. `worktree_list` / `worktree_events` 看登记与日志。
3. `worktree_remove` 且 `complete_task=true` 收尾。
