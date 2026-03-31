# s11: Self-Organizing Workers（自己組織化ワーカー）

`s01 > s02 > s03 > s04 > s05 > s06 | s07 > s08 > s09 > s10 > [ s11 ] s12`

> *暇なら待て；仕事があれば取れ。* タスクボード + inbox + `before_request` 注入。
>
> **Harness 層**：自律の入口 —— harness が手がかりを差し出し、動くかはモデル。

## 問題

全部人間が指示しないと、マルチエージェントは別のスクリプトに過ぎない。**未认领のタスク** と **新着メール** を、モデルが最初に見るところに出したい。

## 方針

- **TaskBoard**：`.lrcc/autonomy/tasks/*.json`。`unclaimed()` は `pending` かつ `owner` なし、`blocked_by` なし。
- **Inbox**：`.lrcc/autonomy/inbox/*.jsonl`。メールボックスと同様。
- **`before_request`**：未読 inbox を優先注入。なければ未认领タスクがあれば先頭へ `<auto-claim-opportunity>`。
- ツール：`task_create`、`task_list`、`claim_task`、`send_message`、`idle`（「このターンは一旦.harness に任せる」）。

## 挙動

自律は魔法ではなく、**各リクエスト前に増える構造化メッセージ** である。`claim_task` で owner と状態を書く。

セッション時間や `idle-timeout` の挙動は `s11_autonomous_agents.py` を正とする。

## s10 からの差分

| 要素 | s10 | s11 |
|------|-----|-----|
| タスク源 | 共有ボードなし | `.lrcc/autonomy/tasks` |
| 駆動 | ツールのみ | + `before_request` で機会を注入 |

## 試す

```sh
cd learn-real-claude-code
python agents/s11_autonomous_agents.py
```

1. `task_create` を複数作り、注入後に `claim_task` するか観察。
2. `send_message` で `lead` へ送り、次ターンに `<inbox>` が入るか見る。
