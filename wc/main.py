# メインのプログラムコード
import pathlib
import os
import pass2times as pass2times
import pass2txt
import hashlib
import tfidf as tfidf
import make_wc as make_wc
import wc2html as wc2html
import docx
import database

def PathtoMeta(path):
  doc = docx.Document(path)  # ファイル名を実際のファイル名に置き換える
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
      'file_size':os.path.getsize(path),
      'os_mtime':pass2times.get_ts(path),
  }
  return metadata



def makeDB(folder_path):
  # フォルダの指定
  file_list = folder_path.glob("*.docx")

  wordshash = []
  cutwordslist = []
  with open("dfdict.txt", "w", encoding = "utf-8") as f:
    str_dfdict = f.readline

  all_dfdict = {str_dfdict}

  for path in file_list:
    # メタデータを取得
    metadata = PathtoMeta(path)

    # 内容をDBに保存
    dbval = database.makedb(path)

    if dbval is None:
      continue
    else:
      dfdict, cutwords = dbval
      # フォルダ全体の単語リスト
      all_dfdict.update(dfdict)

      # 単語リスト
      cutwordslist.append(" ".join(cutwords))

  with open("dfdict.txt", "w", encoding = "utf-8") as f:
    print(all_dfdict,file = f)

  return cutwordslist

  # 動かんからパス
  # tfidfdict = tfidf.getvalues(cutwordslist)

def makeWC(para):

  wc = make_wc.get(all_dfdict)

  file_path = "templates\wc3.html"
  wc2html.get(wc, file_path)


p = pathlib.Path(r"C:\Users\nutta\OneDrive\ドキュメント\授業資料")

words = createDB(p)

