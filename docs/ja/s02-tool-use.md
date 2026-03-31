# s02: Tool Protocol（ツールプロトコル）

`s01 > [ s02 ] s03 > s04 > s05 > s06 | s07 > s08 > s09 > s10 > s11 > s12`

> *能力追加 = ループを書き換えず Tool を足す —— 名前・schema・handler を registry に。*
>
> **Harness 層**：ディスパッチ —— モデルが安全に触れる範囲を広げる。

## 問題

bash だけだとファイル操作はシェル任せになり、パスやクォートで壊れやすい。専用の read/write/edit なら **handler 内** でサンドボックスと長さ制限ができる。

## 解決の形

```
+--------+      +-------+      +------------------+
|  User  | ---> |  LLM  | ---> | ToolRegistry     |
+--------+      +---+---+      |  .call(name,**)  |
                    ^          +--------+---------+
                    |                   |
                    +---- tool_result ---+
```

`run_loop()` はそのまま。`ToolRegistry` に `bash`、`read_file`、`write_file`、`edit_file` を登録（`base_tools()`）。

## 動き

`base_tools()` が各ツールに `input_schema` と `workdir` を閉じ込めた handler を渡す。`safe_path()` でワークスペース外を防ぎ、読み書きは `_shared.py` で長さを切る。

`s02_tool_use.py` のシステムプロンプトは、ファイルは専用ツール、シェル固有の挙動が必要なときだけ bash。

## s01 からの差分

| 要素 | s01 | s02 |
|------|-----|-----|
| ツール数 | 1 | 4（bash + read/write/edit） |
| 分发 | bash のみ | 名前で `ToolRegistry.call` |
| パス | なし | `safe_path` |

## 試す

```sh
cd learn-real-claude-code
python agents/s02_tool_use.py
```

1. `Read README.md (first 40 lines).`
2. `Add a tiny note.txt with today's date.`
3. `Edit note.txt to append one line.`
