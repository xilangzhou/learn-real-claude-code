# s03: Session State（セッション状態）

`s01 > s02 > [ s03 ] s04 > s05 > s06 | s07 > s08 > s09 > s10 > s11 > s12`

> *複数ステップは先に書いてから実行 —— todo はセッション内の道しるべで、永続タスクシステムではない。*
>
> **Harness 層**：セッション状態 —— 「どこまでやったか」を雑談から引き剥がす。

## 問題

ステップが増えると、重複したり飛んだりしやすい。会話メモリだけだと長くなるほどブレる。

## 方針

`todo_write` とメモリ上の `TodoManager`：`pending` / `in_progress` / `completed`。**同時に `in_progress` は一つだけ**。`in_progress` には必ず `active_form`（今やっている一行）。

旧教材とは違い、**N ラウンドで nag** するロジックはない。schema とシステムプロンプトで縛る。

## 挙動

更新は `render()` で読みやすい文字列として `tool_result` に返る。全部完了するとリストは空になる。

これは第7章のディスク上のタスクグラフとは別物。ここは **この会話を乱さない**、そちらは **セッションをまたぐ仕事**。

## s02 からの差分

| 要素 | s02 | s03 |
|------|-----|-----|
| ツール | 基本4つ | + `todo_write` |
| 状態 | なし | `TodoManager.items` |

## 試す

```sh
cd learn-real-claude-code
python agents/s03_todo_write.py
```

1. `Refactor a small function: use todo_write to track 3 steps, then execute.`
2. `Fix imports in one file — keep exactly one in_progress item.`
