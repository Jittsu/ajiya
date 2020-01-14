# あじやのお弁当通知システム
LINE Notifyを用いてあじやのお弁当のメニューを通知できます．

## 前提条件
LINE Notifyに登録して，tokenを取得しておく．

## 使い方(Ubuntu)
```console
$ git clone https://github.com/Jittsu/ajiya
$ cd ajiya
$ pip install -r reqirements.txt
$ vim ajiya_gitshare.py
#dataのpath等を適宜書き換え(フルパスが良い)
$ crontab -e
#開いたファイルの末尾に"0 9 * * * [FULL PATH TO python] [FULL PATH TO ajiya]/ajiya.py >> [FULL PATH TO ajiya]/ajiya.log"を追記
```

※このリポジトリは個人使用であり，あじやエンタープライズ株式会社様とは無関係です．バグ等についてはあじやエンタープライズ株式会社様ではなくこちらのリポジトリのIssueによろしくお願いいたします．
