# s06: Context Stack (上下文治理栈)

`s01 > s02 > s03 > s04 > s05 > [ s06 ] | s07 > s08 > s09 > s10 > s11 > s12`

> *「上下文会满，要分几层收拾」* —— 不是单一 magic compact。
>
> **Harness 层**：治理 —— 在每次请求前动历史。

## 问题

工具输出一长串、会话一久，JSON 序列化后的消息体积暴涨。你需要 **自动裁剪**、**阈值触发重置**，以及 **模型主动喊停** 的通道。

## 解决方案

`ContextManager` + `run_loop(..., before_request=...)`：

1. **结果预算**：较早的 `tool_result` 若超过约 500 字符，截断并加 `[truncated by result budget]`。
2. **微摘要**：assistant 轮数够多以后，把旧的超长 **user 字符串** 消息压成占位片段（教学版用「占位」提示信息被折叠）。
3. **阈值 compact**：若估计 token（JSON 长度 / 4）> 50000，把整个对话写进 `.transcripts/compact_*.jsonl`，用 `summarize_messages` 生成一条带边界的 user 消息替换历史。
4. **compact 工具**：先返回「请在本轮工具结束后压缩」，`run_session` 在循环返回后若检测到 pending，再执行一次 `compact_now`。

这和旧课里「微替换 + 自动摘要 + 手动 compact」讲法一致，但实现上 **拆在 `before_request` 与 `compact_handler` 两处**，读代码时跟紧即可。

## 相对 s05 的变更

| 组件 | s05 | s06 |
|------|-----|-----|
| 历史 | 原样增长 | `before_request` 三层干预 + `compact` |
| 磁盘 | 无 | `.transcripts/` 下 transcript |

## 试一试

```sh
cd learn-real-claude-code
python agents/s06_context_compact.py
```

1. 连续读多个文件，观察旧结果是否被截断。
2. 在对话很长时触发阈值压缩（或手动用 `compact` 工具）。
