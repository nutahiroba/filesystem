# メインのプログラムコード
import pathlib
import os
import pass2times as pass2times
import pass2txt
import count_noun as count_noun
import hashlib
import tfidf as tfidf
import make_wc as make_wc
import wc2html as wc2html
from docx import Document

def PathtoMeta(path):
  doc = Document(path)  # ファイル名を実際のファイル名に置き換える
  title = str(path).split("\\")[-1]

  # メタデータを取得
  metadata = {
      'Title':title,
      # 'Title': doc.core_properties.title,
      # 'Author': doc.core_properties.author,
      # 'Subject': doc.core_properties.subject,
      # 'Keywords': doc.core_properties.keywords,
      # 'Comments': doc.core_properties.comments,
      # 'Last Modified By': doc.core_properties.last_modified_by,
      'Revision': doc.core_properties.revision,
      'Created': doc.core_properties.created,
      'Modified': doc.core_properties.modified,
  }
  return metadata

def wc(path):
  # フォルダの指定
  file_list = path.glob("*.docx")

  # データセットの作成
  dataset = {}
  dataset[0] = ["ファイル名", "作成日時","最終更新日時","ファイルサイズ(Byte)","再頻出語(上位3件)", "冒頭"]
  n = 1
  wordshash = []
  cutwordslist = []
  all_dfdict = {}

  for path in file_list:

    # 文字列取得
    words = pass2txt.getwords(path)
    # 内容が同じファイルを初めのファイル以外無視する（ハッシュ値）
    hs = hashlib.md5(words.encode()).hexdigest()
    if hs in wordshash:
      # ループの先頭に戻ってやり直す
      continue
    else:
      wordshash.append(hs)


    # メタデータを取得
    metadata = PathtoMeta(path)

    # # タイムスタンプ取得
    # make_time = pass2times.get_ts(path)
    # # ファイルサイズ取得
    # date_size = os.path.getsize(path)

    # 名詞数カウント
    dfdict, cutwords = count_noun.raw_getcount(words)

    for word in dfdict.keys():
      if word in all_dfdict:
        all_dfdict[word] += 1
      else:
        all_dfdict[word] = 1

    cutwordslist.append(" ".join(cutwords))

    # dataset[n] = [path.name, make_time, date_size, noundict[:5], words[:20]]
    # n += 1

  # dfdict, allwords = count_noun.getcount("".join(cutwordslist))

  # file_path = "df.txt"

  # with open(file_path, "w", encoding = "utf-8") as f:
  #   for word in dfdict:
  #     print(word, file = f)

  # 動かんからパス
  # tfidfdict = tfidf.getvalues(cutwordslist)

  wc = make_wc.get(all_dfdict)

  file_path = "templates\wc3.html"
  wc2html.get(wc, file_path)
  return cutwordslist


p = pathlib.Path(r"C:\Users\nutta\OneDrive\ドキュメント\授業資料")

words = wc(p)

