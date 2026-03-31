# s06: Context Stack（コンテキストの段階的整理）

`s01 > s02 > s03 > s04 > s05 > [ s06 ] | s07 > s08 > s09 > s10 > s11 > s12`

> *コンテキストは必ず溢れる —— 一発の magic compact ではなく層に分ける。*
>
> **Harness 層**：ガバナンス —— リクエストのたびに履歴を触る。

## 問題

ツール出力が長い、会話が長いと JSON 化したメッセージが膨らむ。**自動トリミング**、**閾値でのリセット**、モデルからの **明示 compact** の道が要る。

## 方針

`ContextManager` + `run_loop(..., before_request=...)`：

1. **結果バジェット**：古い `tool_result` が約 500 文字超なら切り詰め、`[truncated by result budget]` を付ける。
2. **マイクロ要約**：assistant ターンが十分増えたら、古い長い **user 文字列** をプレースホルダに（教材版）。
3. **閾値 compact**：推定トークン（JSON 長 / 4）が 50000 超なら、会話を `.transcripts/compact_*.jsonl` に書き、`summarize_messages` で一本の user メッセージに置き換え。
4. **`compact` ツール**：「このツールターンを終えてから圧縮」と返し、`run_session` がループ後に `compact_now` を実行。

旧教材の「微 + 自動 + 手動」と同じ筋だが、実装は **`before_request`** と **`compact_handler`** に分かれる。コードを追うこと。

## s05 からの差分

| 要素 | s05 | s06 |
|------|-----|-----|
| 履歴 | そのまま増える | `before_request` の多段 + `compact` |
| ディスク | なし | `.transcripts/` に transcript |

## 試す

```sh
cd learn-real-claude-code
python agents/s06_context_compact.py
```

1. ファイルを連続で読み、古い結果が短くなるか見る。
2. 長い会話で閾値を踏むか、`compact` を手で呼ぶ。
