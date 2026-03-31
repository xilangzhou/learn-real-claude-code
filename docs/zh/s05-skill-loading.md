# s05: Skill Discovery (Skill 发现与加载)

`s01 > s02 > s03 > s04 > [ s05 ] s06 | s07 > s08 > s09 > s10 > s11 > s12`

> *「目录里全列出来太蠢；用到再加载」* —— 先发现，再激活，最后读正文。
>
> **Harness 层**：按需知识 —— 把重文本从常驻 system 里挪出去。

## 问题

把每个领域的长文都塞进 system prompt，token 贵且干扰注意力。模型其实只需要知道「有哪些 skill」和「什么时候该读哪篇」。

## 解决方案

`SkillLoader` 扫描 `skills/` 与 `.claude/skills/` 下的 `SKILL.md`，解析 YAML frontmatter（`name`、`description`、`paths`）。

- 没有 `paths` 的 skill：默认进 **active**。
- 带 `paths` 的：只有当你用工具声明「碰过这些路径」时才 **activate**（子串匹配）。

两个工具：`activate_skills(paths)`、`load_skill(name)`。只有 **已激活** 的 skill 才能 `load` 出完整正文。

## 工作原理

系统提示里只放 `list_active()` 的短列表；正文通过 `tool_result` 以 `<skill name="..." source="...">` 包进来。

## 相对 s04 的变更

| 组件 | s04 | s05 |
|------|-----|-----|
| 知识 | 无结构化 | Skill 元数据 + 正文 + 条件激活 |
| 工具 | 基础 + delegate | + `activate_skills`、`load_skill` |

## 试一试

```sh
cd learn-real-claude-code
python agents/s05_skill_loading.py
```

1. `What skills are active?`
2. `Load one active skill by name and summarize its first section.`
3. 编辑某个 `paths` 里提到的文件后，调用 `activate_skills` 看是否多激活 skill。
