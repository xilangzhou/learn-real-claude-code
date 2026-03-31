# s10: Team Protocols（チームプロトコル）

`s01 > s02 > s03 > s04 > s05 > s06 | s07 > s08 > s09 > [ s10 ] s11 > s12`

> *握手が要るなら雑談だけでは足りない。* `request_id` + pending / approved / rejected。
>
> **Harness 層**：プロトコル状態 —— `ProtocolState` のメモリ上テーブル（`.lrcc/protocols/` は配置用；本課は主にメモリマップ）。

## 問題

「止めて」だけでは誰が待っているか、承認されたか分からない。シャットダウンや計画変更には **突き合わせ可能な request ID** が要る。

## 方針

`ProtocolState` が `shutdown_requests` と `plan_requests` を短い `request_id` で保持。ツール：

- `request_shutdown` / `respond_shutdown`
- `submit_plan` / `review_plan`
- `protocol_state` で両方を表示

`resolve()` が `approved` / `rejected` と任意の `feedback` を書く。

この版は **メールボックスのカスタム message type 経由ではない**。状態は `ProtocolState` に閉じる。教えるのは **ID 付き状態機械** であり、完全なメッセージバスではない。

## s09 からの差分

| 要素 | s09 | s10 |
|------|-----|-----|
| 調整 | 自由文 | shutdown / plan の構造化 |
| 追跡 | なし | `request_id` + 状態フィールド |

## 試す

```sh
cd learn-real-claude-code
python agents/s10_team_protocols.py
```

1. `request_shutdown` してから `respond_shutdown` で承認/拒否。
2. `submit_plan` → `review_plan` で一連の流れ。
3. `protocol_state` で両テーブルを確認。
