# s12: Worktree Isolation

## なぜこの章が必要か

複数の workstream が同じファイルシステム面を触り続けるなら、論理的共有状態だけでは不十分です。

## コアメカニズム

- タスクを分離された worktree に結び付ける
- 分離を operator trick ではなく runtime 能力にする
- event log にライフサイクルを書く
- task state を control plane、filesystem isolation を execution plane とみなす

## Python コードへの対応

`agents/s12_worktree_task_isolation.py` は task board 状態、worktree 作成、event log を結び付け、分離を観測可能にします。

## 意図的に単純化している点

教材版は branch 管理の全 edge case を扱いません。焦点はファイルシステム分離をカリキュラムの一級能力にすることです。

## 試してみること

- `agents/` の対応する Python ファイルを開き、追加された class、tool、runtime state を確認する。
- この章の新機構を実際に使わないと進まないタスクを与える。
- 状態がどこに保存され、誰が更新し、誰から見えるかを追う。

## 次章へのつながり

ここでカリキュラムは信じられる小さなランタイムに到達します。loop、tools、visible state、delegation、memory、tasks、concurrency、collaboration、isolation が揃いました。
