# メインのプログラムコード
import pathlib
import os
import pass2times
import pass2txt
import count_noun
import hashlib
import tfidf
import make_wc
import wc2html

# フォルダの指定
p = pathlib.Path(r"C:\Users\nutta\OneDrive\ドキュメント\授業資料")
file_list = list(p.glob("*.docx"))

# データセットの作成
dataset = {}
dataset[0] = ["ファイル名", "作成日時","最終更新日時","ファイルサイズ(Byte)","再頻出語(上位3件)", "冒頭"]
n = 1
wordshash = []
cutwordslist = []

for line in file_list:

  # 文字列取得
  words = pass2txt.docx2words(line)
  # 内容が同じファイルを初めのファイル以外無視する（ハッシュ値）
  hs = hashlib.md5(words.encode()).hexdigest()
  if hs in wordshash:
    # ループの先頭に戻ってやり直す
    continue
  else:
    wordshash.append(hs)
  # タイムスタンプ取得
  make_time = pass2times.get_ts(line)
  # ファイルサイズ取得
  date_size = os.path.getsize(line)
  # 名詞数カウント
  noundict, cutwords = count_noun.getcount(words)
  cutwordslist.append(" ".join(cutwords))

  # dataset[n] = [line.name, make_time, date_size, noundict[:5], words[:20]]
  n += 1

dfdict, allwords = count_noun.getcount("".join(cutwordslist))

file_path = "df.txt"

with open(file_path, "w", encoding = "utf-8") as f:
  for word in dfdict:
    print(word, file = f)

tfidfdict = tfidf.getvalues(cutwordslist)

wc = make_wc.get(dfdict)

wc2html.get(wc, "wc.html")
