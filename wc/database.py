# 文字列の単語数をカウントして辞書とリストを返す
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import MeCab
import random
import string
from pprint import pprint
import docx
import hashlib

engine = create_engine('sqlite:///words.db', echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()
class Files(Base):
  __tablename__ = "files"
  id = Column(String, primary_key=True)
  path = Column(String, unique=True)
  cutwords = Column(String)
  dfdict = Column(String)

  def __init__(self,id, path, cutwords, dfdict):
    self.id = id
    self.path = path
    self.cutwords = cutwords
    self.dfdict = dfdict

  def __str__(self):
    return f"id:{self.id},path:{self.path},cutwords:{self.cutwords},dfdict:{self.dfdict}"

Base.metadata.create_all(engine)


def PathtoTxt(path):
  if ".docx" in str(path):
    doc = docx.Document(path)
    words = ""
    for par in doc.paragraphs:
      words += par.text.replace("\u2028", "")
  elif ".txt" in str(path):
    # 行ごとに分割
    with open(path, encoding="utf-8") as f:
      contents = f.readlines()
    words = "".join(contents)
  return words

def converttostr(input_list):
  return ' '.join(map(str, input_list))

def converttolist(input_str):
  return input_str.split()

#指定されたパスのドキュメントがすでに存在するかをチェックする関数
def ispath_exists(path):
  path = str(path)
  exists = session.query(Files).filter(Files.path == path).count()
  if exists != 0:
    return True
  # ループがすべてのファイルを検査し終えても一致するものが見つからない場合
  return False

def dbgetfile(path):
  path = str(path)
  file = session.query(Files).filter(Files.path == path).first()
  if file is not None:
    return file.cutwords, file.dfdict
  else:
    print("404 指定されたパスのドキュメントが見つかりませんでした")
    return None

def genid(length=8):
    characters = string.ascii_letters + string.digits
    random_id = ''.join(random.choice(characters) for _ in range(length))
    return random_id

def regtodb(path, cutwords, dfdict):
    path_str = str(path)
    # 辞書オブジェクトを文字列に変換
    dfdict_str = converttostr(dfdict)
    cutwords_str = converttostr(cutwords)
    id = genid()
    #DBに登録
    file = Files(id=id, path=path_str, cutwords=cutwords_str, dfdict=dfdict_str)
    session.add(file)
    session.commit()

def makedb(path):
  # dbfile = dbgetfile(path)
  if ispath_exists(path):
    return None

  with open(r"C:\Users\nutta\myProject\FileSystem\wc\stopword.txt", "r",encoding="utf-8") as f:
    stopwords = f.readlines()
  stopwords = [string.strip() for string in stopwords if string.strip()]

  # 文字列取得
  words = PathtoTxt(path)

  tagger = MeCab.Tagger()
  cutwords = []
  dfdict = {}
  node = tagger.parseToNode(words)
  while node:
    word = node.surface
    hinshi = node.feature.split(",")[0]
    if hinshi == "名詞" and word not in stopwords:
      cutwords.append(word)

    if word in dfdict.keys():
      dfdict[word] += 1
    elif hinshi == "名詞" and len(word) != 1 and word not in stopwords:
      dfdict[word] = 1
    else:
      pass
    node = node.next
  # dfdict = sorted(dfdict.items(), key = lambda x:x[1], reverse=True)
  regtodb(path, dfdict, cutwords)
  return dfdict, cutwords

def getval(path):
  return 0



# DBに依存しないタイプ
def raw_getcount(words):
  tagger = MeCab.Tagger()
  cutwords = []

  with open(r"C:\Users\nutta\myProject\FileSystem\wc\stopword.txt", "r",encoding="utf-8") as f:
    stopwords = f.readlines()
  stopwords = [string.strip() for string in stopwords if string.strip()]

  dfdict = {}
  node = tagger.parseToNode(words)
  while node:
    word = node.surface
    hinshi = node.feature.split(",")[0]
    if hinshi == "名詞" and word not in stopwords:
      cutwords.append(word)

    if hinshi == "名詞" and word in dfdict.keys():
      dfdict[word] += 1
    elif hinshi == "名詞" and len(word) != 1 and word not in stopwords:
      dfdict[word] = 1
    else:
      pass
    node = node.next
  # dfdict = sorted(dfdict.items(), key = lambda x:x[1], reverse=True)
  return dfdict, cutwords
