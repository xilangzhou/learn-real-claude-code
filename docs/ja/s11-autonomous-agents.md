# s11: Self-Organizing Workers

## なぜこの章が必要か

チーム内の全ての動きが lead の指示から来るなら、まだ scripted です。役に立つ自律性は、worker が自分で見つけ、引き受け、続けられるときに現れます。

## コアメカニズム

- 共有 task board を持つ
- 各 worker に inbox を与える
- idle 期間に polling させる
- open work の auto-claim のような local policy を許す

## Python コードへの対応

`agents/s11_autonomous_agents.py` は自律性を神秘化せず、共有状態と小さな規則に落とします。

## 意図的に単純化している点

ここでの local policy は意図的に単純です。焦点は最適スケジューリングではなく、ランタイム構造からの創発です。

## 試してみること

- `agents/` の対応する Python ファイルを開き、追加された class、tool、runtime state を確認する。
- この章の新機構を実際に使わないと進まないタスクを与える。
- 状態がどこに保存され、誰が更新し、誰から見えるかを追う。

## 次章へのつながり

workers が自己組織化できるようになったら、最後に必要なのは実行面を分離して並行作業の衝突を避けることです。
