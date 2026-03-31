# s12: Worktree Isolation（Worktree 分離）

`s01 > s02 > s03 > s04 > s05 > s06 | s07 > s08 > s09 > s10 > s11 > [ s12 ]`

> *タスクは目的、ディレクトリは実行。* 制御面と実行面を分ける。
>
> **Harness 層**：隔離 —— 並列でファイルを踏みにくくする。

## 問題

全員が同じ作業ツリーを触ると、未提交の変更が衝突する。s11 でタスクを取っても、実行が同じツリーなら問題は残る。

## 方針

- **TaskBoard**（`.lrcc/isolation/tasks/`）：タスク JSON に `worktree`。`bind(task_id, name)` で適宜 `pending` → `in_progress`。
- **WorktreeStore**：リポジトリ直下の `.lrcc/isolation/worktrees/`。git があれば `git worktree add -b wt/<name>`、なければ通常ディレクトリ。`index.json` に name、path、branch、`task_id`。
- **EventLog**：`events.jsonl` で create/remove/task.completed など。

ツール：`task_create`、`task_list`、`worktree_create`（任意 `task_id`）、`worktree_remove`（任意 `complete_task` で紐づくタスク完了）、`worktree_list`、`worktree_events`。

## 挙動

`REPO_ROOT = detect_repo_root(cwd) or cwd`。git がなくてもディレクトリ隔離で教材は回る。

## s11 からの差分

| 要素 | s11 | s12 |
|------|-----|-----|
| 実行場所 | 共有 cwd | lane ごとの path |
| ディスク | autonomy タスク | + worktree 索引 + イベントログ |

## 試す

```sh
cd learn-real-claude-code
python agents/s12_worktree_task_isolation.py
```

1. `task_create` のあと `task_id` 付きで `worktree_create`。
2. `worktree_list` / `worktree_events` で登録とログ。
3. `complete_task=true` で `worktree_remove` して締める。
