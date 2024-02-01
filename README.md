# プロジェクト名

文書の分析結果に基づく検索機能を備えた個人向け文書管理機能の開発（筑波大学　情報学群　知識情報・図書館学類卒論）

本機能では、docxファイルを対象に検索することができる。

## 実行方法

本システムの実行にはpython実行環境が必要であるほか、以下のpythonパッケージのダウンロードが必要です。
  1 flask(https://flask.palletsprojects.com/) 
  2 flask_SQLAlchemy(https://docs.sqlalchemy.org/en/20/)
  3 python-docx(https://python-docx.readthedocs.io/en/latest/ )
  4 SQLite(https://www.sqlite.org/)
  5 MeCab(https://taku910.github.io/mecab/)
  6 WordCloud作成モジュール(https://amueller.github.io/word_cloud/)
  7 pathlib（python標準モジュール）

以下の通りにファイルを実行します。

①zipファイルを展開する。

②”app2.py”の変数"path"に検索対象となるファイル群のファイルパスを設定する（絶対パス）。その後"app2.py"ファイルを実行する。

③ローカルサーバが起動するので、"http://127.0.0.1:8000/"にアクセスする。

④ワードクラウドのパラメタ調整フォームが表示されるので値を設定し、"Generate"ボタンをクリックする。
  調整できるパラメタには以下のものがある。
  ・高さ…ワードクラウドの縦幅
  ・幅…ワードクラウドの横幅
  ・最大、最小文字サイズ…ワードクラウドに含まれる文字のサイズ
  ・ステップ…ワードクラウドの単語の粗密度
  ・TF値、DF値、TF-IDF値…ワードクラウドを表示する際に参考にする値を選択する。

⑤文書群の分析が終了するとワードクラウドが表示されるので、目的の文書に含まれていそうな単語を選択する。

⑥選択した単語を含む文書が表示されるので、選択する単語を増やしたり減らしたりして目的の文書にたどり着くことができる。

## 詳細機能説明

文書内容を分析し、ワードクラウドを作成し、そこから単語を選択することで手元のMS-Word文書を検索できる

作者の実行環境は以下の通り
  ・OS:Windows 11 Home
  ・python(ver.3.8.10)
  ・Flask(ver.3.0.0)
  ・python-docx(ver.0.8.11)
  ・MeCab(ver.1.0.6)
  ・SQLite(ver.3.39.0)
  ・SQLAlchemy(ver.2.0.23)
  ・WordCloud(ver.1.9.2)


## 作者

筑波大学　情報学群　知識情報・図書館学類　2020年入学
Hiroto Nutaba

Github: @nutahiroba (https://github.com/nutahiroba/filesystem)

mail:nutaba.hiroto.qd@alumni.tsukuba.ac.jp
