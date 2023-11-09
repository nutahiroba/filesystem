# ファイルパスからそのファイルの文字列を返す

import docx
import MeCab

def getwords(path):
  if ".docx" in str(path):
    tagger = MeCab.Tagger()
    doc = docx.Document(path)
    words = ""
    for par in doc.paragraphs:
      words += par.text.replace("\u2028", "")
  elif ".txt" in path:
    # 行ごとに分割
    with open(path, encoding="utf-8") as f:
      contents = f.readlines()
    words = "".join(contents)
  return words