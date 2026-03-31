# s10: Team Protocols (团队协议)

`s01 > s02 > s03 > s04 > s05 > s06 | s07 > s08 > s09 > [ s10 ] s11 > s12`

> *「要握手，就别只靠聊天」* —— request_id + pending/approved/rejected。
>
> **Harness 层**：协议状态 —— 存在内存 + `.lrcc/protocols/` 目录（本课主要用 `ProtocolState` 内存表）。

## 问题

邮箱里随便发一句「关了吧」容易扯皮：谁在等谁、批没批。关机、改计划这类事需要 **可核对的请求 ID**。

## 解决方案

`ProtocolState` 维护两套表：`shutdown_requests`、`plan_requests`，键为短 `request_id`。工具：

- `request_shutdown` / `respond_shutdown`
- `submit_plan` / `review_plan`
- `protocol_state` 查看当前表

`resolve()` 把状态写成 `approved` 或 `rejected`，并可附 `feedback`。

注意：这一版 **没有** 再走邮箱里自定义 message type；协议状态在 `ProtocolState` 里闭环，教学目的是「带 ID 的状态机」，不是完整消息总线。

## 相对 s09 的变更

| 组件 | s09 | s10 |
|------|-----|-----|
| 协调 | 自由文本 | + 结构化 shutdown / plan |
| 追踪 | 无 | `request_id` + 状态字段 |

## 试一试

```sh
cd learn-real-claude-code
python agents/s10_team_protocols.py
```

1. `request_shutdown` 对一个名字，再 `respond_shutdown` 批准或拒绝。
2. `submit_plan` 再 `review_plan` 走通一条计划。
3. `protocol_state` 看两张表。
