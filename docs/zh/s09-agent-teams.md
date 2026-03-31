# s09: Team Mailboxes (团队邮箱)

`s01 > s02 > s03 > s04 > s05 > s06 | s07 > s08 > [ s09 ] s10 > s11 > s12`

> *「多个人一起干，先要有邮箱」* —— 身份 + JSONL 收件箱，比共享一个大脑好查。
>
> **Harness 层**：协作面 —— lead 与队友各跑各的循环。

## 问题

s04 的子 agent 一次性；s08 的后台只是 shell。要 **多轮协作**，需要持久身份和可投递的收件箱。

## 解决方案

- **MailboxBus**：`.lrcc/team/inbox/<name>.jsonl`，append 写、读时 **drain 清空**。
- **TeamManager**：`.lrcc/team/config.json` 里记名册与状态；`team_spawn` 在线程里跑队友的 `run_loop`，队友每次请求前 `before_request` 把未读 inbox 注入。

Lead 侧工具：`team_spawn`、`send_message`（发向某队友）、`read_inbox`（读 lead 自己的箱）、`team_list`。

## 工作原理

队友线程里 registry = 基础工具 + `send_message`（发给其它人）。Lead 用 `send_message` 时固定从 `"lead"` 发出。

## 相对 s08 的变更

| 组件 | s08 | s09 |
|------|-----|-----|
| 并发 | 仅后台 shell | 多线程各跑 agent loop |
| 通信 | 无 | JSONL mailbox |

## 试一试

```sh
cd learn-real-claude-code
python agents/s09_agent_teams.py
```

1. `Spawn a teammate "alice" with a short coding prompt, then send_message to alice.`
2. `read_inbox` 看 lead 是否收到回复（取决于模型是否回发）。
3. `team_list` 看状态。
