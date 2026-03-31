# s01: The Agent Loop（エージェントループ）

`[ s01 ] s02 > s03 > s04 > s05 > s06 | s07 > s08 > s09 > s10 > s11 > s12`

> *ループとツール面が一つあれば、まずはエージェントとして回せる —— プランナや記憶、マルチエージェントの前に閉ループを通す。*
>
> **Harness 層**：ループ —— モデルと実環境をつなぐ最小配線。

## 問題

モデル単体ではディスクもシェルも触れない。ループがなければ、ツール結果を毎回手で貼り戻すことになる。つまり **人間がループ** になる。

## 解決の形

```
+--------+      +-------+      +---------+
|  User  | ---> |  LLM  | ---> |  Tool   |
| prompt |      |       |      | execute |
+--------+      +---+---+      +----+----+
                    ^                |
                    |   tool_result  |
                    +----------------+
        stop_reason != tool_use で終了
```

## このリポジトリでの動き

ループは `agents/_shared.py` の `run_loop()` に集約される。`messages` を積み、`registry.definitions()` 付きで API を呼ぶ。応答に `tool_use` がなければ return。あれば各ブロックで `registry.call()` し、次の user メッセージとして `tool_result` を足す。

`s01_agent_loop.py` は意図的に **bash だけ** を登録する（`ToolRegistry([base_tools(WORKDIR, include_write=False)[0]])`）。システムプロンプトは「先に動いてから説明」。

## 裸のモデルからの変化

| 要素 | 以前 | s01 以降 |
|------|------|----------|
| 制御 | なし | `while` + `max_turns` 上限 |
| ツール | なし | `bash` のみ |
| メッセージ | なし | assistant / user（tool_result 含む）を蓄積 |

## 試す

```sh
cd learn-real-claude-code
python agents/s01_agent_loop.py
```

プロンプト例（英語の方が安定しやすい）：

1. `List the top-level directories here and say what this repo is for.`
2. `Create a small hello.py and show its contents with cat.`
3. `What git branch are we on?`
