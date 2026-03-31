# s05: Skill Discovery

## なぜこの章が必要か

全てのドメイン指示を system prompt に詰め込むと、文脈が重くなり焦点も失われます。

## コアメカニズム

- skill を metadata と instructions の組にする
- ディレクトリと条件から利用可能 skill を見つける
- 現在タスクに関係あるものだけを activate する
- 常駐させず遅延注入する

## Python コードへの対応

`agents/s05_skill_loading.py` は派手な prompt template ではなく、discovery、filtering、activation を中心に据えます。

## 意図的に単純化している点

製品版は多ソース読み込みやより豊かな matching rule を持てますが、教材版では存在理由を説明する最小構造に絞ります。

## 試してみること

- `agents/` の対応する Python ファイルを開き、追加された class、tool、runtime state を確認する。
- この章の新機構を実際に使わないと進まないタスクを与える。
- 状態がどこに保存され、誰が更新し、誰から見えるかを追う。

## 次章へのつながり

遅延ロードは助けになりますが、文脈窓を管理できなければ長いセッションは依然として壊れます。
