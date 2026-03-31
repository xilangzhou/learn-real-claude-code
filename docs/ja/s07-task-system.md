# s07: Persistent Tasks（永続タスク）

`s01 > s02 > s03 > s04 > s05 > s06 | [ s07 ] s08 > s09 > s10 > s11 > s12`

> *タスクはディスクに生きる —— 会話が compact されても消えない。*
>
> **Harness 層**：永続化 —— `blocked_by` はファイルにあり、モデルの記憶にない。

## 問題

s03 の todo はセッション終了で消える。s06 の compact 後は会話上のタスク説明も消える。本番の仕事には **複数ターンにまたがり復元できる** 記録が要る。

## 方針

`TaskStore` が `.lrcc/tasks/<task_list_id>/`（既定 `default`）に書き込む。タスクごとに JSON：`id`、`subject`、`status`、`owner`、`blocked_by`、タイムスタンプなど。完了時 `_clear_dependency` で他タスクの `blocked_by` から該当 id を外す。

## ツール

`task_create`、`task_get`、`task_list`、`task_update`。ID は高水位ファイルで衝突を避ける。

## s06 からの差分

| 要素 | s06 | s07 |
|------|-----|-----|
| 作業単位 | なし | ディスク上の JSON タスク |
| 依存 | なし | `blocked_by` リスト |

## 試す

```sh
cd learn-real-claude-code
python agents/s07_task_system.py
```

1. `Create three tasks A,B,C; make B depend on A, C depend on B.`
2. `Complete A and list — B should be unblocked.`
