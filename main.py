import pathlib
import os
import pass2times
import pass2txt
import count_noun
import hashlib
import tfidf



p = pathlib.Path(r"C:\Users\nutta\OneDrive\ドキュメント\授業資料")
file_list = list(p.glob("*.docx"))

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

  dataset[n] = [line.name, make_time, date_size, noundict[:5], words[:20]]
  n += 1

tfidfdict = tfidf.getvalues(cutwordslist)

print(dataset[0])
for id in dataset:
  if id != 0:
    print("{}".format(dataset[id][0]))
    print("")
    print("\t{}".format(dataset[id][3]))
    print("\t{}\n".format(tfidfdict[id]))
    # print(dataset[id])

# print(len(dataset))



# pandasによるテーブル化を断念
# d1 = pd.DataFrame(dataset,columns=["ファイル名", "作成日時","最終更新日時","ファイルサイズ(Byte)","再頻出語(上位3件)", "冒頭"])
# print(d1)