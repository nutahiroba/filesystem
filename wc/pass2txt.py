# ファイルパスからそのファイルの文字列を返す

import docx
import MeCab

def docx2words(filepass):
  tagger = MeCab.Tagger()
  doc = docx.Document(filepass)
  words = ""

  for par in doc.paragraphs:
    words += par.text.replace("\u2028", "")
  
  return words

def text2words(filepass):
  # 行ごとに分割
  with open(filepass, encoding="utf-8") as f:
    contents = f.readlines()
  words = "".join(contents)

  return words

def getwords(filepass):
  if ".docx" in filepass:
    words = docx2words(filepass)
  elif ".txt" in filepass:
    words = text2words(filepass)
  return words
