# s05: Skill Discovery（スキル発見と読み込み）

`s01 > s02 > s03 > s04 > [ s05 ] s06 | s07 > s08 > s09 > s10 > s11 > s12`

> *全文を常時プロンプトに載せるのは無駄 —— 見つけて、有効化して、必要なとき読む。*
>
> **Harness 層**：オンデマンド知識 —— 重い本文を固定 system から外す。

## 問題

長いドメイン文を system に全部入れるとトークンも注意も浪費する。モデルに必要なのは **何があるか** と **いつどれを読むか** だけ。

## 方針

`SkillLoader` が `skills/` と `.claude/skills/` の `SKILL.md` を走査し、YAML frontmatter（`name`、`description`、`paths`）を解析。

- `paths` **なし**：最初から **active**。
- `paths` **あり**：ツールで「触ったパス」を渡したときだけ **activate**（部分一致）。

ツール：`activate_skills(paths)`、`load_skill(name)`。**active なスキルだけ** 全文を `load` できる。

## 挙動

system には `list_active()` の短い一覧だけ。本文は `tool_result` で `<skill name="..." source="...">` として届く。

## s04 からの差分

| 要素 | s04 | s05 |
|------|-----|-----|
| 知識 | 構造化なし | メタデータ + 本文 + 条件付き有効化 |
| ツール | 基本 + delegate | + `activate_skills`、`load_skill` |

## 試す

```sh
cd learn-real-claude-code
python agents/s05_skill_loading.py
```

1. `What skills are active?`
2. `Load one active skill by name and summarize its first section.`
3. `paths` に合うファイルを編集したあと `activate_skills` を呼び、スキルが増えるか見る。
