# s02: Tool Protocol (工具协议)

`s01 > [ s02 ] s03 > s04 > s05 > s06 | s07 > s08 > s09 > s10 > s11 > s12`

> *「加能力 = 加 Tool，不是改循环」* —— 名字 + schema + handler，统一进 registry。
>
> **Harness 层**：工具分发 —— 扩展模型能安全触达的边界。

## 问题

只靠 bash，读写文件都要拼 shell，路径和引号一乱就容易出错。专用读写工具可以在 **handler 里** 做沙箱和截断，比每次靠模型自觉更稳。

## 解决方案

```
+--------+      +-------+      +------------------+
|  User  | ---> |  LLM  | ---> | ToolRegistry     |
+--------+      +---+---+      |  .call(name,**)  |
                    ^          +--------+---------+
                    |                   |
                    +---- tool_result ---+
```

`run_loop()` 不变；变的是 `ToolRegistry` 里注册了 `bash`、`read_file`、`write_file`、`edit_file`（见 `base_tools()`）。

## 工作原理

`base_tools()` 为每个工具提供 `input_schema` 和闭包 handler（传入 `workdir`）。`safe_path()` 保证路径不逃出工作区；读写在 `_shared.py` 里统一截断长度。

`s02_tool_use.py` 的系统提示会引导：文件操作用专用工具，只有需要 shell 语义时才用 bash。

## 相对 s01 的变更

| 组件 | s01 | s02 |
|------|-----|-----|
| 工具数 | 1 | 4（bash + read/write/edit） |
| 分发 | 隐式只有 bash | `ToolRegistry.call` 按名调用 |
| 路径 | 无沙箱 | `safe_path` |

## 试一试

```sh
cd learn-real-claude-code
python agents/s02_tool_use.py
```

1. `Read README.md (first 40 lines).`
2. `Add a tiny note.txt with today's date.`
3. `Edit note.txt to append one line.`
