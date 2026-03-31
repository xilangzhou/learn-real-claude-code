# s08: Background Runtime（バックグラウンド）

`s01 > s02 > s03 > s04 > s05 > s06 | s07 > [ s08 ] s09 > s10 > s11 > s12`

> *遅い処理でメインループを塞がない —— スレッドで走らせ、結果を会話に戻す。*
>
> **Harness 層**：バックグラウンド —— ライフサイクルは harness、モデルは命令だけ。

## 問題

`pytest` や依存インストールは長い。同期実行だとモデルは待つだけで体験が悪い。

## 方針

`BackgroundManager.run()` が daemon スレッドで `subprocess` を起動し、短い uuid を task id に。完了時はスレッド安全キューへ。**毎回の LLM リクエスト前**に `before_request` で `drain_notifications()` し、あれば user メッセージ `<task-notifications>...</task-notifications>` を追加。

`background_check` で一つまたは一覧を確認。

## 挙動

メインのスケジュールループは単一スレッド。並列は子プロセスと結果集約。300 秒超は timeout。

## s07 からの差分

| 要素 | s07 | s08 |
|------|-----|-----|
| 実行 | 同期 | + バックグラウンドシェル + 通知 |
| ツール | タスク4種 | + `background_run`、`background_check` |

## 試す

```sh
cd learn-real-claude-code
python agents/s08_background_tasks.py
```

1. `Run sleep 3 && echo done in background, then do something else until notification appears.`
2. `List background tasks with background_check.`
