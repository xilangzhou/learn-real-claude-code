# 架构总览

这套课从 `examples/claude-code` 里抽了真实 runtime 关心的事，用 `agents/` 里的 Python 教学实现一层层摊开。写法上对齐 `examples/learn-claude-code`：每章只加一个主机制，但代码路径和目录约定是本仓库自己的（例如 `.lrcc/` 下的状态）。

## 你在学什么

模型会推理，但不会自动读盘、跑命令、改文件。Agent 的起点是 **循环**：发请求 → 模型可能调工具 → 执行 → 结果写回 → 再发请求，直到模型不再要工具。

在这个骨架上，后面章节依次加上：结构化工具、会话内 todo、委托模式、按需 skill、上下文治理、持久任务、后台通知、团队邮箱、协议状态、自组织轮询、以及任务与 worktree 绑定。不是功能清单，而是一条从「能跑」到「能协作、能隔离」的递进路径。

## 仓库怎么读

| 路径 | 作用 |
|------|------|
| `agents/s*.py` | 各章对应的最小可跑 harness |
| `agents/_shared.py` | 共享的 `run_loop`、`ToolRegistry`、基础工具 |
| `docs/en/`、`docs/zh/`、`docs/ja/` | 各语言章节正文（与网页教程同源） |
| `web/` | 课程页与可视化脚本 |

跑某一章时，在项目根目录执行 `python agents/sXX_....py`，环境变量里配好 `MODEL_ID`（以及可选的 `ANTHROPIC_BASE_URL`）。
