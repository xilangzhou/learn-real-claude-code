[English](./README.md) | [中文](./README-zh.md) | [日本語](./README-ja.md)

# Learn Real Claude Code

## このリポジトリについて

Learn Real Claude Code は coding agent harness 設計を学ぶための教材です。

目的は、ある実システムを逐語的に写すことではなく、実際に重要な仕組みへ
忠実な Python カリキュラムを作ることです。主題は次の通りです。

- agent loop
- tool protocol
- セッション状態と永続タスク状態
- delegation のモード
- 遅延ロードされる skills
- context management
- background runtime
- multi-agent coordination
- worktree isolation

## 構成

```text
learn-real-claude-code/
├── agents/   # s01-s12 の教材スクリプト + s_full 参照実装
├── tests/    # 教材スクリプトの smoke test
└── web/      # 学習サイトと章メタデータ
```

## 教材としての方針

`agents/` の各ファイルは小さく、実行可能で、読みやすく保ちます。

これらは教材用実装であり、実運用コードの縮小コピーではありません。実システムが
もっと複雑な場合でも、このリポジトリは次を優先します。

1. アーキテクチャ境界を正しく保つ
2. 実装は簡潔にする
3. 何を簡略化したかを明示する

## 更新後の学習パス

1. `s01` The Agent Loop
2. `s02` Tool Protocol
3. `s03` Session State
4. `s04` Delegation Modes
5. `s05` Skill Discovery
6. `s06` Context Management Stack
7. `s07` Persistent Task Runtime
8. `s08` Background Runtime
9. `s09` Team Mailboxes
10. `s10` Team Protocols
11. `s11` Self-Organizing Workers
12. `s12` Worktree Isolation

## 使い方

各章は直接実行できます。

```bash
python agents/s01_agent_loop.py
```

基本的には順番に進めてください。後半の章も単一ファイルですが、前半の概念を前提にしています。

## 参照スクリプト

`agents/s_full.py` は修正後の教材ハーネスを一つにまとめた参照実装です。
ただし、これはあくまで教材であり、完全な実運用互換を主張するものではありません。
