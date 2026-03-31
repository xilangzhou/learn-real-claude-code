# s07: Persistent Task Runtime

## なぜこの章が必要か

チャット内の checklist は便利ですが、セッションと共に消えます。本格的な仕事追跡には専用の保存先とライフサイクルが必要です。

## コアメカニズム

- タスクをメッセージ履歴の外に永続化する
- task create/get/list/update を支える
- タスクを durable runtime state として扱う
- session todo と概念的に分離する

## Python コードへの対応

`agents/s07_task_system.py` は専用ランタイムフォルダに永続状態を書き込み、task plane がチャット窓に依存しないようにします。

## 意図的に単純化している点

教材版は小さなファイルベース store を使います。ポイントは durability と concern separation であって、製品級オーケストレーションではありません。

## 試してみること

- `agents/` の対応する Python ファイルを開き、追加された class、tool、runtime state を確認する。
- この章の新機構を実際に使わないと進まないタスクを与える。
- 状態がどこに保存され、誰が更新し、誰から見えるかを追う。

## 次章へのつながり

永続状態が整うと、前景ループが進んでも続き得る作業をランタイムが所有できるようになります。
