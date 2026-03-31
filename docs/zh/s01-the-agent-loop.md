# s01: The Agent Loop (Agent 循环)

`[ s01 ] s02 > s03 > s04 > s05 > s06 | s07 > s08 > s09 > s10 > s11 > s12`

> *「一个循环 + 一个工具面，就够当 agent 用」* —— 先别谈规划、记忆、多机，先把闭环跑通。
>
> **Harness 层**：循环 —— 模型和真实环境之间的最小接线。

## 问题

模型本身碰不到磁盘和 shell。没有循环，每调一次工具你都要手动把结果贴回对话里——你才是那个循环。

## 解决方案

```
+--------+      +-------+      +---------+
|  User  | ---> |  LLM  | ---> |  Tool   |
| prompt |      |       |      | execute |
+--------+      +---+---+      +----+----+
                    ^                |
                    |   tool_result  |
                    +----------------+
              stop_reason != tool_use 时结束
```

## 工作原理

本仓库里循环集中在 `agents/_shared.py` 的 `run_loop()`：累积 `messages`，每次带上 `registry.definitions()` 调 API；若响应里没有 `tool_use`，直接返回；否则对每个 `tool_use` 调 `registry.call()`，把 `tool_result` 作为下一轮 user 消息。

`s01_agent_loop.py` 只注册 **bash** 一个工具（`ToolRegistry([base_tools(WORKDIR, include_write=False)[0]])`），故意保持最小。系统提示里写明：先动手再解释。

## 相对「裸模型」的变更

| 组件 | 之前 | 之后 (s01) |
|------|------|------------|
| 控制流 | 无 | `while` + `max_turns` 上限 |
| 工具 | 无 | 仅 `bash` |
| 消息 | 无 | 累积 assistant / user（含 tool_result） |

## 试一试

```sh
cd learn-real-claude-code
python agents/s01_agent_loop.py
```

示例 prompt（英文通常更稳，中文也可）：

1. `List the top-level directories here and say what this repo is for.`
2. `Create a small hello.py and show its contents with cat.`
3. `What git branch are we on?`
