# s10: Team Protocols

## なぜこの章が必要か

チーム内のメッセージは単なるテキストではありません。後で照合すべきライフサイクルを開くものがあります。

## コアメカニズム

- 重要な協調メッセージに request id を付ける
- pending、approved、rejected を追跡する
- plan と shutdown を型付き要求として表す
- ランタイムが protocol state を poll して解決する

## Python コードへの対応

`agents/s10_team_protocols.py` は protocol が本質的に「message + lifecycle state」だと示します。

## 意図的に単純化している点

教材版は少数の protocol に絞ります。大事なのは数ではなく、型付き協調には wording 以上の記憶が必要だと示すことです。

## 試してみること

- `agents/` の対応する Python ファイルを開き、追加された class、tool、runtime state を確認する。
- この章の新機構を実際に使わないと進まないタスクを与える。
- 状態がどこに保存され、誰が更新し、誰から見えるかを追う。

## 次章へのつながり

ランタイムが workers を明示的に協調できるなら、共有状態の周りで自己協調させることもできます。
