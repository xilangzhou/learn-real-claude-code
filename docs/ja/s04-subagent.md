# s04: Delegation Modes（委任モード）

`s01 > s02 > s03 > [ s04 ] s05 > s06 | s07 > s08 > s09 > s10 > s11 > s12`

> *子タスクは別ループ、親には要約だけ —— でもクリーンな履歴と文脈付き fork は別物。*
>
> **Harness 層**：委任 —— 子ループにどの履歴を渡すか。

## 問題

本線にツール出力が積もると、「調べて」と言うだけでノイズごと流れ込む。要約が欲しくて全文 transcript は要らない。

文脈を継続したいときは **fresh** が薄すぎる。**fork** が合う。

## 方針

`delegate` に `mode` を付ける。

- **fresh**：子は単一 user メッセージから。履歴なし。
- **fork**：`summarize_messages(parent_messages, keep_last=8)` を `<inherited-context>` に包んで指令と合わせる。

子も同じ `run_loop()`。registry は `base_tools` のみで **`delegate` なし**（再帰委任を防ぐ）。

## 配線

`DelegationRunner` が各 `run_session` で親 `messages` を渡し、handler から `run_worker(..., parent_messages=...)`。

## s03 からの差分

| 要素 | s03 | s04 |
|------|-----|-----|
| 子タスク | なし | `delegate` + 子 `run_loop` |
| 文脈 | 一本 | 親／子で分離 |

## 試す

```sh
cd learn-real-claude-code
python agents/s04_subagent.py
```

1. `Delegate in fresh mode: list files in agents/ and return a one-line summary.`
2. `Fork mode: continue from our thread — check whether s04 uses summarize_messages.`
