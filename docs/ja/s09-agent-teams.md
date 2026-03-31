# s09: Team Mailboxes（チームメールボックス）

`s01 > s02 > s03 > s04 > s05 > s06 | s07 > s08 > [ s09 ] s10 > s11 > s12`

> *複数人で動くならまずメールボックス —— 身元と JSONL の inbox が共有の脳より観察しやすい。*
>
> **Harness 層**：協働の面 —— リードとメンバーがそれぞれループを回す。

## 問題

s04 の subagent は一回限り。s08 のバックグラウンドはシェルだけ。**複数ターンの協働** には安定した身元と、届け先のある inbox が要る。

## 方針

- **MailboxBus**：`.lrcc/team/inbox/<name>.jsonl`、追記書き、読み取りで **drain**。
- **TeamManager**：`.lrcc/team/config.json` に名簿と状態。`team_spawn` がスレッドで `run_loop` を回し、各リクエスト前に `before_request` で未読 inbox を注入。

リード向けツール：`team_spawn`、`send_message`、`read_inbox`、`team_list`。

## 挙動

メンバー側の registry は基本ツール + 他者への `send_message`。リードの `send_message` は常に `"lead"` から。

## s08 からの差分

| 要素 | s08 | s09 |
|------|-----|-----|
| 並行 | バックグラウンドシェルのみ | スレッドごとに agent loop |
| 通信 | なし | JSONL |

## 試す

```sh
cd learn-real-claude-code
python agents/s09_agent_teams.py
```

1. `Spawn a teammate "alice" with a short coding prompt, then send_message to alice.`
2. `read_inbox` でリードに返信があるか（モデル次第）。
3. `team_list` で状態確認。
